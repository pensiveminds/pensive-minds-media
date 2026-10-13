"""Heel & Serpent design variants: same words, same palette and type, different composition.

Every variant keeps the rules: one command, one verse with its reference shown, one ember word,
series name top left, the mark top right, handle bottom left.

  ground(kind)                 'iron' (default), 'bone' (light), 'forge' (iron with a low ember glow)
  mo_classic(...)              the original centred still
  mo_bone(...)                 light ground, iron type: the "daylight" still
  mo_ledger(...)               left-aligned, editorial; an ember rule runs down the left margin
  mo_engraved(...)             inset double frame with the seal as a faint watermark behind the type
  mo_forge(...)                one giant cropped word behind the command, warm glow from below
"""
import io, os, re, sys
import numpy as np
import cairosvg
from xml.sax.saxutils import escape
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make_posts import (text_block, line_svg, measure, mark, CROSS, SEAL, HANDLE, SERIF, SANS,
                        IRON, BONE, EMBER, ASH, marching_orders)

W, Hh = 1080, 1350
INK_ON_BONE, ASH_ON_BONE = IRON, "#6B655F"


def _swap(inner):
    """Logo drawn for an iron ground -> logo for a bone ground (iron strokes, bone knockouts)."""
    return inner.replace(BONE, "#@@@@@@").replace(IRON, BONE).replace("#@@@@@@", IRON)


def ground(kind="iron", w=W, h=Hh, seed=3):
    rng = np.random.default_rng(seed)
    if kind == "bone":
        a = np.empty((h, w, 3), "float32"); a[:] = (236, 230, 218)
        a += rng.normal(0, 5, (h, w))[..., None]
        img = Image.fromarray(a.clip(0, 255).astype("uint8"))
        v = Image.new("L", (w, h), 0); ImageDraw.Draw(v).ellipse((-w * .3, -h * .25, w * 1.3, h * 1.25), fill=255)
        return Image.composite(img, Image.new("RGB", (w, h), (214, 206, 192)), v.filter(ImageFilter.GaussianBlur(w / 5)))
    a = np.full((h, w, 3), 26, "float32") + rng.normal(0, 7, (h, w))[..., None]
    if kind == "forge":
        yy, xx = np.mgrid[0:h, 0:w]
        g = np.exp(-(((xx - w / 2) / (w * .62)) ** 2 + ((yy - h * 1.12) / (h * .40)) ** 2))
        a += g[..., None] * np.array([95, 32, 6], "float32")
    img = Image.fromarray(a.clip(0, 255).astype("uint8"))
    v = Image.new("L", (w, h), 0); ImageDraw.Draw(v).ellipse((-w * .25, -h * .2, w * 1.25, h * 1.2), fill=255)
    return Image.composite(img, Image.new("RGB", (w, h), "#0d0d0d"), v.filter(ImageFilter.GaussianBlur(w / 6)))


def render_on(svg_text, path, kind="iron"):
    base = ground(kind)
    fg = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg_text.encode(), output_width=W))).convert("RGBA")
    base.paste(fg, (0, 0), fg); base.save(path, quality=94)


def _frame(series, inner, ink=BONE, ash=ASH, cross=CROSS, page=None):
    m = 80
    pg = (f'<text x="{W-m}" y="{Hh-72}" text-anchor="end" font-family="{SANS}" font-weight="600" font-size="22" '
          f'letter-spacing="4" fill="{ash}">{page}</text>') if page else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}">
{inner}
<text x="{m}" y="104" font-family="{SANS}" font-weight="700" font-size="24" letter-spacing="7" fill="{EMBER}">{escape(series.upper())}</text>
{mark(cross, W-m-84, 46, 92)}
<line x1="{m}" y1="150" x2="{W-m}" y2="150" stroke="{ash}" stroke-width="1.5"/>
<line x1="{m}" y1="{Hh-120}" x2="{W-m}" y2="{Hh-120}" stroke="{ash}" stroke-width="1.5"/>
<text x="{m}" y="{Hh-72}" font-family="{SANS}" font-weight="600" font-size="22" letter-spacing="4" fill="{ash}">{HANDLE}</text>
{pg}
</svg>'''


def _left_block(lines, x, y, size, family=SERIF, weight=500, spacing=0, italic=False, color=BONE, lead=1.18, max_w=820):
    plain = [re.sub(r"[\[\]]", "", l) for l in lines]
    while size > 20 and max(measure(p, family, size, weight, spacing, italic) for p in plain) > max_w:
        size -= 2
    out = []
    for i, (ln, p) in enumerate(zip(lines, plain)):
        wdt = measure(p, family, size, weight, spacing, italic)
        out.append(line_svg(ln, x + wdt / 2, y + i * size * lead, size, family, weight, spacing, italic, color)[0])
    return "\n".join(out), y + (len(lines) - 1) * size * lead


def _centre(inner, top, bottom, mid=690):
    return f'<g transform="translate(0,{mid - (top + bottom) / 2:.0f})">{inner}</g>'


# ---------------------------------------------------------------- Marching Orders variants

def mo_classic(command, verse_lines, ref, sub=None):
    return marching_orders(command, verse_lines, ref, sub=sub), "iron"


def mo_bone(command, verse_lines, ref, sub=None):
    size = 104
    big, end = text_block(command, 0, size, spacing=10, lead=1.12, color=INK_ON_BONE)
    parts = [big]; y = end + 80
    if sub:
        s_, end = text_block(sub, y, 40, weight=400, color=ASH_ON_BONE, spacing=1); parts.append(s_); y = end + 70
    parts.append(f'<line x1="500" y1="{y:.0f}" x2="580" y2="{y:.0f}" stroke="{EMBER}" stroke-width="2"/>'); y += 110
    v, end = text_block(verse_lines, y, 46, italic=True, weight=400, color=INK_ON_BONE, lead=1.3); parts.append(v)
    r = text_block([ref.upper()], end + 74, 22, family=SANS, weight=600, spacing=6, color=ASH_ON_BONE)[0]; parts.append(r)
    inner = _centre("\n".join(parts), -size * .72, end + 74)
    return _frame("Marching Orders", inner, ink=INK_ON_BONE, ash=ASH_ON_BONE, cross=_swap(CROSS)), "bone"


def mo_ledger(command, verse_lines, ref, sub=None):
    x = 150; size = 118
    big, end = _left_block(command, x, 0, size, spacing=8, lead=1.08, max_w=800)
    parts = [big]; y = end + 70
    if sub:
        s_, end = _left_block(sub, x, y, 40, weight=400, color=ASH, max_w=800); parts.append(s_); y = end + 120
    v, end2 = _left_block(verse_lines, x, y, 44, italic=True, weight=400, lead=1.3, max_w=800); parts.append(v)
    r = _left_block([ref.upper()], x, end2 + 70, 22, family=SANS, weight=600, spacing=6, color=ASH)[0]; parts.append(r)
    top, bottom = -size * .72, end2 + 70
    shift = 690 - (top + bottom) / 2
    rule = (f'<line x1="104" y1="{top + shift:.0f}" x2="104" y2="{bottom + shift:.0f}" stroke="{EMBER}" stroke-width="3"/>')
    inner = rule + _centre("\n".join(parts), top, bottom)
    return _frame("Marching Orders", inner), "iron"


def mo_engraved(command, verse_lines, ref, sub=None):
    frame = (f'<rect x="56" y="186" width="{W-112}" height="{Hh-342}" fill="none" stroke="{ASH}" stroke-width="1.2"/>'
             f'<rect x="68" y="198" width="{W-136}" height="{Hh-366}" fill="none" stroke="{ASH}" stroke-width="0.6"/>')
    water = f'<g opacity="0.045">{mark(SEAL, 140, 290, 800)}</g>'
    size = 100
    big, end = text_block(command, 0, size, spacing=12, lead=1.12, max_w=820)
    parts = [big]; y = end + 76
    if sub:
        s_, end = text_block(sub, y, 38, weight=400, color=ASH, spacing=1, max_w=820); parts.append(s_); y = end + 66
    dots = (f'<circle cx="510" cy="{y:.0f}" r="3" fill="{EMBER}"/><circle cx="540" cy="{y:.0f}" r="3" fill="{EMBER}"/>'
            f'<circle cx="570" cy="{y:.0f}" r="3" fill="{EMBER}"/>'); parts.append(dots); y += 104
    v, end = text_block(verse_lines, y, 44, italic=True, weight=400, lead=1.3, max_w=820); parts.append(v)
    r = text_block([ref.upper()], end + 72, 22, family=SANS, weight=600, spacing=6, color=ASH)[0]; parts.append(r)
    inner = frame + water + _centre("\n".join(parts), -size * .72, end + 72)
    return _frame("Marching Orders", inner), "iron"


def mo_forge(command, verse_lines, ref, sub=None, ghost=None):
    """ghost: the one word set huge and cropped behind the command (defaults to the ember word)."""
    if ghost is None:
        m = re.search(r"\[([^\]]+)\]", " ".join(command)); ghost = (m.group(1) if m else command[-1]).strip(".")
    g = (f'<text x="{W/2:.0f}" y="760" text-anchor="middle" font-family="{SERIF}" font-weight="600" font-size="430" '
         f'letter-spacing="10" fill="none" stroke="{EMBER}" stroke-opacity="0.28" stroke-width="2">{escape(ghost)}</text>')
    size = 108
    big, end = text_block(command, 0, size, spacing=10, lead=1.1)
    parts = [big]; y = end + 80
    if sub:
        s_, end = text_block(sub, y, 40, weight=400, color=ASH, spacing=1); parts.append(s_); y = end + 70
    parts.append(f'<line x1="500" y1="{y:.0f}" x2="580" y2="{y:.0f}" stroke="{EMBER}" stroke-width="2"/>'); y += 110
    v, end = text_block(verse_lines, y, 46, italic=True, weight=400, lead=1.3); parts.append(v)
    r = text_block([ref.upper()], end + 74, 22, family=SANS, weight=600, spacing=6, color=ASH)[0]; parts.append(r)
    inner = g + _centre("\n".join(parts), -size * .72, end + 74)
    return _frame("Marching Orders", inner), "forge"


VARIANTS = {"classic": mo_classic, "bone": mo_bone, "ledger": mo_ledger, "engraved": mo_engraved, "forge": mo_forge}


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "design", "variants")
    os.makedirs(out, exist_ok=True)
    args = (["MASTER", "YOUR [BODY]."], ["“…I discipline my body and bring it", "under strict control…”"],
            "1 Corinthians 9:27, CSB")
    kw = dict(sub=["Move before you scroll. Sweat before you sit."])
    for name, fn in VARIANTS.items():
        svg, kind = fn(*args, **kw)
        render_on(svg, os.path.join(out, f"mo_{name}.jpg"), kind)
        print(name)
