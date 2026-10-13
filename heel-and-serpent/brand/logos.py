"""Heel & Serpent logo marks, drawn in code.

B  Cross & Serpent  (header mark)
C  The Seal         (merch, launch post, watermark)
D  Monogram         (profile picture)
A  Crushed S        (unused alternate)

Run directly to render a contact sheet of all four into brand/concepts/."""
import math, io, os, sys
import cairosvg
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from shapes import bez, ribbon, IRON, BONE, EMBER, ASH


def snake(pts, w0, w1, fg=BONE, knock=IRON, hl=1.0, tongue=True):
    """Body ribbon plus a head grown from the end of the centreline, so neck and head are one shape."""
    (xa, ya), (xb, yb) = pts[-4], pts[-1]
    L = math.hypot(xb-xa, yb-ya); ux, uy = (xb-xa)/L, (yb-ya)/L
    hlen = w1 * 3.1 * hl
    hp = [(xb + ux*hlen*t/40, yb + uy*hlen*t/40) for t in range(41)]
    allp = pts + hp[1:]
    n = len(pts); m = len(hp) - 1; N = n + m
    def w(i):
        if i < n:
            return w0 + (w1-w0) * ((i/(n-1)) ** 1.0)
        t = (i-n+1)/m                     # 0..1 along the head
        if t < 0.45: return w1 * (1 + 0.42*math.sin(t/0.45*math.pi/2))
        return w1 * 1.42 * math.cos((t-0.45)/0.55*math.pi/2) ** 0.7 + 0.5
    left, right = [], []
    for i, (x, y) in enumerate(allp):
        xa2, ya2 = allp[max(i-1, 0)]; xb2, yb2 = allp[min(i+1, N-1)]
        dx, dy = xb2-xa2, yb2-ya2; LL = math.hypot(dx, dy) or 1
        nx, ny = -dy/LL, dx/LL; hw = w(i)/2
        left.append((x+nx*hw, y+ny*hw)); right.append((x-nx*hw, y-ny*hw))
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in left + right[::-1]) + " Z"
    nose = allp[-1]; ex = xb + ux*hlen*0.62; ey = yb + uy*hlen*0.62
    nx, ny = -uy, ux
    eye = f'<circle cx="{ex+nx*w1*0.32:.1f}" cy="{ey+ny*w1*0.32:.1f}" r="{max(3, w1*0.12):.1f}" fill="{knock}"/>'
    tg = ""
    if tongue:
        t0 = (nose[0]+ux*4, nose[1]+uy*4); t1 = (nose[0]+ux*w1*0.9, nose[1]+uy*w1*0.9)
        f1 = (t1[0]+(ux+nx*0.6)*w1*0.45, t1[1]+(uy+ny*0.6)*w1*0.45)
        f2 = (t1[0]+(ux-nx*0.6)*w1*0.45, t1[1]+(uy-ny*0.6)*w1*0.45)
        tg = (f'<path d="M {t0[0]:.1f} {t0[1]:.1f} L {t1[0]:.1f} {t1[1]:.1f} L {f1[0]:.1f} {f1[1]:.1f} '
              f'M {t1[0]:.1f} {t1[1]:.1f} L {f2[0]:.1f} {f2[1]:.1f}" stroke="{EMBER}" stroke-width="{max(2.5, w1*0.09):.1f}" '
              f'fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    return f'<path d="{d}" fill="{fg}"/>{eye}{tg}', (nose, (ux, uy), hlen)


def svg(inner, bg=IRON):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">'
            f'<rect width="1000" height="1000" fill="{bg}"/>{inner}</svg>')


# A. Crushed S: the serpent is the letter S; a single heavy bar (the heel) pins its head.
def concept_a(fg=BONE):
    pts = bez((300, 812), (450, 892), (760, 840), (712, 662), 60)
    pts += bez((712, 662), (668, 506), (318, 560), (308, 404), 60)[1:]
    pts += bez((308, 404), (298, 266), (440, 238), (590, 262), 60)[1:]
    sn, (nose, u, hl) = snake(pts, 4, 40, fg)
    # the heel: one heavy bar laid across the back of the head
    return svg(f'''
{sn}
<rect x="548" y="212" width="196" height="34" fill="{fg}" stroke="{IRON}" stroke-width="8" paint-order="stroke"/>
<circle cx="500" cy="500" r="455" fill="none" stroke="{fg}" stroke-width="3"/>
<circle cx="500" cy="500" r="440" fill="none" stroke="{fg}" stroke-width="1.2"/>
''')


# B. Cross & Serpent: a slender cross with a sword point driven onto the serpent's head.
def cross_and_serpent(fg=BONE, s=1.0, ty=0):
    cross = ("M 484 140 L 516 140 L 516 280 L 630 280 L 630 312 L 516 312 "
             "L 516 700 L 500 752 L 484 700 L 484 312 L 370 312 L 370 280 L 484 280 Z")
    cx, cy, rx, ry = 500, 826, 218, 62
    # tail at the upper right, round the bottom and left, neck rising at top-left, head heading right under the point
    pts = [(cx + rx*math.cos(math.radians(a)), cy + ry*math.sin(math.radians(a)))
           for a in [-38 + 300 * i / 199 for i in range(200)]]
    sn, _ = snake(pts, 3, 34, fg, hl=1.05)
    return f'''<g transform="translate({500-500*s},{ty}) scale({s})">
{sn}
<path d="{cross}" fill="{fg}" stroke="{IRON}" stroke-width="10" paint-order="stroke" stroke-linejoin="miter"/>
</g>'''


def concept_b(fg=BONE):
    return svg(cross_and_serpent(fg) + f'''
<circle cx="500" cy="500" r="455" fill="none" stroke="{fg}" stroke-width="3"/>
<circle cx="500" cy="500" r="440" fill="none" stroke="{fg}" stroke-width="1.2"/>''')


# C. The Seal: whiskey-label / signet ring. Engraved text ring around the cross-and-serpent.
def concept_c(fg=BONE):
    return svg(f'''
<defs><path id="top" d="M 118 500 A 382 382 0 0 1 882 500"/><path id="bot" d="M 88 500 A 412 412 0 0 0 912 500"/></defs>
<circle cx="500" cy="500" r="468" fill="none" stroke="{fg}" stroke-width="5"/>
<circle cx="500" cy="500" r="456" fill="none" stroke="{fg}" stroke-width="1.5"/>
<circle cx="500" cy="500" r="330" fill="none" stroke="{fg}" stroke-width="1.5"/>
<text font-family="EB Garamond" font-weight="500" font-size="62" letter-spacing="17" fill="{fg}">
<textPath href="#top" startOffset="51.5%" text-anchor="middle">HEEL &amp; SERPENT</textPath></text>
<text font-family="EB Garamond" font-size="40" letter-spacing="12" fill="{ASH}">
<textPath href="#bot" startOffset="51%" text-anchor="middle">GENESIS III · XV</textPath></text>
<circle cx="120" cy="500" r="7" fill="{EMBER}"/><circle cx="880" cy="500" r="7" fill="{EMBER}"/>
{cross_and_serpent(fg, s=0.56, ty=212)}
''')


# D. Monogram: H & S engraved in Garamond, the S replaced by a serpent; ampersand in ember.
def concept_d(fg=BONE):
    dx = 26
    pts = bez((594+dx, 640), (700+dx, 690), (820+dx, 650), (790+dx, 560), 50)
    pts += bez((790+dx, 560), (760+dx, 470), (610+dx, 500), (610+dx, 410), 50)[1:]
    pts += bez((610+dx, 410), (610+dx, 340), (690+dx, 322), (740+dx, 340), 50)[1:]
    sn, _ = snake(pts, 4, 28, fg)
    return svg(f'''
<text x="290" y="650" text-anchor="middle" font-family="EB Garamond" font-weight="500" font-size="420" fill="{fg}">H</text>
<text x="514" y="560" text-anchor="middle" font-family="EB Garamond" font-style="italic" font-size="150" fill="{EMBER}">&amp;</text>
{sn}
<line x1="150" y1="700" x2="850" y2="700" stroke="{fg}" stroke-width="2"/>
<text x="500" y="770" text-anchor="middle" font-family="EB Garamond" font-size="40" letter-spacing="22" fill="{ASH}">EST. MMXXVI</text>
<circle cx="500" cy="500" r="455" fill="none" stroke="{fg}" stroke-width="3"/>
''')


if __name__ == "__main__":
    out = os.path.join(HERE, "concepts")
    os.makedirs(out, exist_ok=True)
    names = [("A", "Crushed S", concept_a), ("B", "Cross & Serpent", concept_b),
             ("C", "The Seal", concept_c), ("D", "Monogram", concept_d)]
    tiles = []
    for k, label, fn in names:
        s = fn()
        open(f"{out}/{k}.svg", "w").write(s)
        png = cairosvg.svg2png(bytestring=s.encode(), output_width=1000)
        open(f"{out}/{k}.png", "wb").write(png)
        tiles.append((k, label, Image.open(io.BytesIO(png)).convert("RGB")))
    sheet = Image.new("RGB", (2 * 820 + 60, 2 * 900 + 40), "#0f0f0f")
    f = ImageFont.truetype(os.path.join(HERE, "..", "fonts", "EBGaramond.ttf"), 44)
    d = ImageDraw.Draw(sheet)
    for i, (k, label, im) in enumerate(tiles):
        x = 20 + (i % 2) * 840; y = 20 + (i // 2) * 900
        sheet.paste(im.resize((800, 800), Image.LANCZOS), (x, y))
        d.text((x + 400, y + 840), f"{k}  ·  {label}", fill=BONE, font=f, anchor="mm")
    sheet.save(f"{out}/hs_concepts_sheet.png")
