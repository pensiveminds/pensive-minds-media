"""Heel & Serpent embroidery-ready marks (soft drape tee and French terry hood).

Each mark is redrawn at its real stitched size so it meets embroidery limits (Printful, Oct 2026):
  lettering at least 0.25 in tall, lines at least 0.05 in thick, no tiny gaps, <= 6 thread colours,
  transparent PNG at 300 DPI, flat colour only.
We build to a little over those limits (MIN_CAP, MIN_LINE, MIN_GAP below).

    python merch/embroidery.py      -> merch/embroidery/*.png, *_check.png, contact_sheet.png

Changes from the screen marks, all forced by thread:
  - Monogram: the rule under it is dropped; the serpent's tail is thickened to the minimum line;
    the forked tongue is dropped (too fine to stitch; the ember ampersand carries the colour);
    the eye is enlarged so it stays an open knockout.
  - Seal: 4.5 in (up from about 4) so its ring lettering can stand 0.31 in tall in Garamond ExtraBold;
    the double rings become single rings; the serpent's eye is dropped;
    the serpent coil is near-uniform weight; the gap around the cross point is widened.
  - Small lines (nape, sleeve) are set in Inter Black, the brand's label face: Garamond's hairlines
    can't hold at 1/4 in.
Colours are quantised to the thread palette, so every pixel is a thread colour or transparent.
"""
import io, math, os, re, sys
import numpy as np
import cairosvg
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "brand"))
from logos import snake, bez, IRON, BONE, EMBER, ASH

OUT = os.path.join(HERE, "embroidery")
DPI = 300
MIN_LINE, MIN_CAP, MIN_GAP = 0.055, 0.27, 0.035      # inches
KNOCK = "#FF00FF"                                     # knockouts: become transparent (bare garment)
TONAL = {"iron": "#3B3936", "bone": "#CFC7B8"}        # tonal thread, a shade off the garment
GARMENT = {"iron": IRON, "bone": BONE}
SERIF, SANS = "EB Garamond", "Inter"


def _svg(inner, vb=(0, 0, 1000, 1000)):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" '
            f'width="{vb[2]}" height="{vb[3]}">{inner}</svg>')


def _rgba(svg, px_w):
    return np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=int(px_w)))).convert("RGBA"))


def _bbox_units(svg, vb_w):
    a = _rgba(svg, 1000)[..., 3]
    ys, xs = np.nonzero(a > 40)
    k = vb_w / 1000
    return xs.min() * k, ys.min() * k, (xs.max() + 1) * k, (ys.max() + 1) * k


def _quantise(rgba, colours):
    """Every pixel -> nearest thread colour, or transparent. KNOCK -> transparent."""
    pal = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in colours + [KNOCK]], float)
    rgb = rgba[..., :3].astype(float); a = rgba[..., 3]
    d = ((rgb[:, :, None, :] - pal[None, None]) ** 2).sum(-1)
    idx = d.argmin(-1)
    out = np.zeros(rgba.shape, "uint8")
    solid = (a >= 128) & (idx < len(colours))
    out[solid, :3] = pal[idx[solid]].astype("uint8"); out[solid, 3] = 255
    return out


def build(name, svg_fn, width_in, colours, vb=(0, 0, 1000, 1000)):
    """svg_fn(s) -> inner svg, where s = inches per unit. Two passes: measure, then draw to the real scale."""
    s = width_in / 900.0
    for _ in range(3):                                   # settle the scale (thickness depends on it)
        x0, y0, x1, y1 = _bbox_units(_svg(svg_fn(s), vb), vb[2])
        s = width_in / (x1 - x0)
    inner = svg_fn(s)
    x0, y0, x1, y1 = _bbox_units(_svg(inner, vb), vb[2])
    pad = 0.06 / s
    box = (x0 - pad, y0 - pad, x1 - x0 + 2 * pad, y1 - y0 + 2 * pad)
    svg = _svg(inner, box)
    px_w = round(box[2] * s * DPI)
    q = _quantise(_rgba(svg, px_w * 2), colours)       # draw at 2x, quantise, then halve with no blending
    img = Image.fromarray(q).resize((px_w, round(px_w * box[3] / box[2])), Image.NEAREST)
    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, name + ".png"), dpi=(DPI, DPI))
    return img, s


# ---------------------------------------------------------------- marks

def monogram(fg, amp):
    def f(s):
        minw = MIN_LINE / s
        dx = 26
        pts = bez((594 + dx, 640), (700 + dx, 690), (820 + dx, 650), (790 + dx, 560), 50)
        pts += bez((790 + dx, 560), (760 + dx, 470), (610 + dx, 500), (610 + dx, 410), 50)[1:]
        pts += bez((610 + dx, 410), (610 + dx, 340), (690 + dx, 322), (740 + dx, 340), 50)[1:]
        sn, _ = snake(pts, max(4, minw), max(28, minw * 1.6), fg, knock=KNOCK, tongue=False)
        sn = re.sub(r'(<circle [^>]*?)r="[\d.]+"', lambda m: m.group(1) + f'r="{max(3.4, minw * 0.62):.1f}"', sn)
        hs = max(0, minw * 0.35)                       # a light outline thickens the serifs
        as_ = max(0, minw * 0.55)                      # more on the italic ampersand, whose hairlines are finest
        return (f'<text x="290" y="650" text-anchor="middle" font-family="{SERIF}" font-weight="600" font-size="420" '
                f'fill="{fg}" stroke="{fg}" stroke-width="{hs:.1f}" stroke-linejoin="round">H</text>'
                f'<text x="514" y="560" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-weight="700" '
                f'font-size="150" fill="{amp}" stroke="{amp}" stroke-width="{as_:.1f}" stroke-linejoin="round">&amp;</text>'
                f'{sn}')
    return f


def seal(fg, ember, label, cap_in=0.31):
    CROSS = ("M 484 140 L 516 140 L 516 280 L 630 280 L 630 312 L 516 312 "
             "L 516 700 L 500 752 L 484 700 L 484 312 L 370 312 L 370 280 L 484 280 Z")

    def f(s):
        minw, cap, gap = MIN_LINE / s, cap_in / s, MIN_GAP / s
        font = cap / 0.66                              # Garamond cap height is about 0.66 em
        R, r = 462, 330
        mid = (R + r) / 2
        rt, rb = mid - cap / 2, mid + cap / 2          # top text grows outward from rt; bottom inward from rb
        ts = max(0, minw * 0.7)
        sc = 0.56; tx, ty = 500 - 500 * sc, 212
        cx, cy, rx, ry = 500, 826, 218, 62
        pts = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))
               for a in [-30 + 290 * i / 199 for i in range(200)]]
        wmin = minw / sc
        sn, _ = snake(pts, wmin, max(34, wmin * 1.35), fg, knock=KNOCK, hl=1.05, tongue=False)
        sn = re.sub(r'<circle [^>]*?/>', '', sn)        # no eye at this size: it would split the head
        knock_w = 2 * (gap / sc) + 2                   # stroke is centred, so half of it is the gap
        dot = max(9, minw * 0.8)
        return f'''
<defs><path id="t" d="M {500 - rt} 500 A {rt} {rt} 0 0 1 {500 + rt} 500"/><path id="b" d="M {500 - rb} 500 A {rb} {rb} 0 0 0 {500 + rb} 500"/></defs>
<circle cx="500" cy="500" r="{R}" fill="none" stroke="{fg}" stroke-width="{minw * 1.15:.1f}"/>
<circle cx="500" cy="500" r="{r}" fill="none" stroke="{fg}" stroke-width="{minw:.1f}"/>
<text font-family="{SERIF}" font-weight="800" font-size="{font:.1f}" letter-spacing="{font * 0.13:.1f}" fill="{fg}" stroke="{fg}" stroke-width="{ts:.1f}" stroke-linejoin="round">
<textPath href="#t" startOffset="50%" text-anchor="middle">HEEL &amp; SERPENT</textPath></text>
<text font-family="{SERIF}" font-weight="800" font-size="{font:.1f}" letter-spacing="{font * 0.11:.1f}" fill="{label}" stroke="{label}" stroke-width="{ts:.1f}" stroke-linejoin="round">
<textPath href="#b" startOffset="50%" text-anchor="middle">GENESIS III · XV</textPath></text>
<circle cx="{500 - mid}" cy="500" r="{dot:.1f}" fill="{ember}"/><circle cx="{500 + mid}" cy="500" r="{dot:.1f}" fill="{ember}"/>
<g transform="translate({tx},{ty}) scale({sc})">{sn}
<path d="{CROSS}" fill="none" stroke="{KNOCK}" stroke-width="{knock_w:.1f}" stroke-linejoin="miter"/>
<path d="{CROSS}" fill="{fg}" stroke="{fg}" stroke-width="{max(0, minw / sc - 32) + 2:.1f}" stroke-linejoin="miter"/></g>'''
    return f


def lettering(lines, fg, spacing=0.22, cap_in=0.30):
    """Small stitched lines in Inter Black, one or two lines, centred."""
    def f(s):
        cap = cap_in / s
        font = cap / 0.727                             # Inter cap height is 0.727 em
        lead = font * 1.55
        out = ""
        for i, ln in enumerate(lines):
            y = 500 + i * lead
            out += (f'<text x="1500" y="{y:.1f}" text-anchor="middle" font-family="{SANS}" font-weight="900" '
                    f'font-size="{font:.1f}" letter-spacing="{font * spacing:.1f}" fill="{fg}">{ln}</text>')
        return out
    return f


# ---------------------------------------------------------------- checks

def check(img, name):
    """Red: strokes thinner than the minimum line. Blue: gaps narrower than the minimum gap."""
    a = np.asarray(img)[..., 3] > 0
    def disk(d_in):
        r = max(1, int(round(d_in * DPI / 2)))
        yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
        return xx ** 2 + yy ** 2 <= r * r
    thin = a & ~ndimage.binary_opening(a, disk(MIN_LINE * 0.9))
    gaps = ndimage.binary_closing(a, disk(MIN_GAP * 0.9)) & ~a
    lab, n = ndimage.label(gaps)
    if n:
        sizes = ndimage.sum(gaps, lab, range(1, n + 1))
        keep = np.isin(lab, 1 + np.nonzero(sizes > (MIN_GAP * DPI) ** 2 * 1.5)[0])
        gaps = gaps & keep
    base = np.asarray(img).copy()
    shown = np.zeros(a.shape + (3,), "uint8"); shown[:] = (60, 58, 56)
    shown[a] = base[a, :3]
    shown[thin] = (255, 40, 40); shown[gaps] = (40, 120, 255)
    Image.fromarray(shown).save(os.path.join(OUT, name + "_check.png"))
    return thin.sum() / max(1, a.sum()), int(gaps.sum())


JOBS = [
    # name, builder, width (in), garment
    ("tee_chest_monogram_iron",   monogram(TONAL["iron"], EMBER),       3.0, "iron"),
    ("tee_chest_monogram_bone",   monogram(IRON, EMBER),                3.0, "bone"),
    ("tee_back_seal_iron",        seal(BONE, EMBER, ASH),               4.5, "iron"),
    ("tee_nape_bruised_bone",     lettering(["BRUISED,", "NOT BEATEN."], IRON), None, "bone"),
    ("hood_chest_monogram_iron",  monogram(TONAL["iron"], EMBER),       3.5, "iron"),
    ("hood_chest_monogram_bone",  monogram(IRON, EMBER),                3.5, "bone"),
    ("hood_sleeve_heeldown_iron", lettering(["HEEL DOWN."], TONAL["iron"]), None, "iron"),
    ("hood_sleeve_heeldown_bone", lettering(["HEEL DOWN."], TONAL["bone"]), None, "bone"),
    ("hood_back_seal_iron",       seal(BONE, EMBER, ASH),               4.5, "iron"),
]


def _colours(fn):
    return sorted(set(re.findall(r'(?:fill|stroke)="(#[0-9A-Fa-f]{6})"', fn(0.004))) - {KNOCK})


def _lettering_width(fn):
    """Lettering is sized by its cap height, so its width falls out of the type."""
    s = 0.004
    x0, y0, x1, y1 = _bbox_units(_svg(fn(s), (0, 0, 3000, 1500)), 3000)
    return (x1 - x0) * s


if __name__ == "__main__":
    rows = []
    for name, fn, w, garment in JOBS:
        vb = (0, 0, 1000, 1000)
        if w is None:
            vb = (0, 0, 3000, 1500); w = _lettering_width(fn)
        cols = _colours(fn)
        img, s = build(name, fn, w, cols, vb)
        thin, gaps = check(img, name)
        h = img.size[1] / DPI
        rows.append((name, garment, w, h, cols, thin, gaps))
        print(f"{name:28s} {w:4.2f} x {h:4.2f} in  threads {cols}  thin {thin:.3%}  gap px {gaps}")
