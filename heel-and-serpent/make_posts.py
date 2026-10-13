"""Heel & Serpent post builder.

Templates (all SVG -> PNG with grain and vignette):
  marching_orders(...)  1080x1350 still: big command line + verse
  carousel(...)         1080x1350 slides for Get Back Up / Armor Check
  story(...)            1080x1920 Story slide

Text markup: wrap the single highlight word in [brackets] to set it in ember.
Run:  python3 make_posts.py <out_dir>   (renders the launch set defined at the bottom)
"""
import io, os, re, sys
from xml.sax.saxutils import escape
import numpy as np
import cairosvg
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "brand"))
from logos import concept_b, concept_c, IRON, BONE, EMBER, ASH

HANDLE = "@heelandserpent"
SERIF, SANS = "EB Garamond", "Inter"


def _inner(svg_text):
    """Body of a 1000x1000 concept SVG without its background rect."""
    body = svg_text.split(">", 1)[1].rsplit("</svg>", 1)[0]
    return body.replace(f'<rect width="1000" height="1000" fill="{IRON}"/>', "", 1)


CROSS = _inner(concept_b())
SEAL = _inner(concept_c())


def mark(inner, x, y, size):
    return f'<g transform="translate({x},{y}) scale({size/1000})">{inner}</g>'


FONT_FILES = {SERIF: os.path.join(HERE, "fonts", "EBGaramond.ttf"), SANS: os.path.join(HERE, "fonts", "Inter.ttf")}
_font_cache = {}


def _font(family, size, weight, italic=False):
    from PIL import ImageFont
    key = (family, size, weight)
    if key not in _font_cache:
        f = ImageFont.truetype(FONT_FILES[family], size)
        try:
            f.set_variation_by_axes([weight] if family == SERIF else [14, weight])
        except Exception:
            pass
        _font_cache[key] = f
    return _font_cache[key]


def measure(text, family, size, weight, spacing, italic=False):
    w = _font(family, size, weight).getlength(text) + spacing * len(text)
    return w * (0.97 if italic else 1.0)


def line_svg(line, x, y, size, family, weight, spacing, italic, color):
    """Lay out one line manually (cairosvg mis-places mixed tspans), centred on x."""
    parts = [(p[1:-1], EMBER) if p.startswith("[") else (p, color)
             for p in re.split(r"(\[[^\]]+\])", line) if p]
    total = sum(measure(t, family, size, weight, spacing, italic) for t, _ in parts)
    cx = x - total / 2
    style = 'font-style="italic"' if italic else ""
    out = []
    for t, c in parts:
        out.append(f'<text x="{cx:.1f}" y="{y:.0f}" font-family="{family}" font-weight="{weight}" '
                   f'font-size="{size}" letter-spacing="{spacing}" fill="{c}" {style} xml:space="preserve">{escape(t)}</text>')
        cx += measure(t, family, size, weight, spacing, italic)
    return "".join(out), total


def text_block(lines, y, size, family=SERIF, spacing=0, italic=False, color=BONE,
               lead=1.18, weight=500, x=540, max_w=920):
    """Lines centred on x, first baseline at y. Shrinks to fit max_w. Returns (svg, last baseline)."""
    while size > 20 and max(measure(re.sub(r"[\[\]]", "", l), family, size, weight, spacing, italic)
                             for l in lines) > max_w:
        size -= 2
    out = [line_svg(ln, x, y + i*size*lead, size, family, weight, spacing, italic, color)[0]
           for i, ln in enumerate(lines)]
    return "\n".join(out), y + (len(lines)-1)*size*lead


def frame(w, h, series, page=None, inner=""):
    m = 80
    pg = (f'<text x="{w-m}" y="{h-72}" text-anchor="end" font-family="{SANS}" font-weight="600" '
          f'font-size="22" letter-spacing="4" fill="{ASH}">{page}</text>') if page else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<text x="{m}" y="104" font-family="{SANS}" font-weight="700" font-size="24" letter-spacing="7" fill="{EMBER}">{escape(series.upper())}</text>
{mark(CROSS, w-m-84, 46, 92)}
<line x1="{m}" y1="150" x2="{w-m}" y2="150" stroke="{ASH}" stroke-width="1.5"/>
{inner}
<line x1="{m}" y1="{h-120}" x2="{w-m}" y2="{h-120}" stroke="{ASH}" stroke-width="1.5"/>
<text x="{m}" y="{h-72}" font-family="{SANS}" font-weight="600" font-size="22" letter-spacing="4" fill="{ASH}">{HANDLE}</text>
{pg}
</svg>'''


def verse(lines, ref, y):
    v, end = text_block(lines, y, 46, italic=True, weight=400, color=BONE, lead=1.3)
    r = text_block([ref.upper()], end + 74, 22, family=SANS, weight=600, spacing=6, color=ASH)[0]
    return v + "\n" + r, end + 74


def rule(y):
    return f'<line x1="500" y1="{y:.0f}" x2="580" y2="{y:.0f}" stroke="{EMBER}" stroke-width="2"/>'


def centred(inner, top, bottom, mid=690):
    """Shift a block so its visual middle sits at mid (the band between header and footer rules)."""
    return f'<g transform="translate(0,{mid - (top + bottom) / 2:.0f})">{inner}</g>'


def marching_orders(command, verse_lines, ref, sub=None):
    """Daily still. command: 1-3 lines of spaced capitals; sub: optional plain line under it."""
    y0 = 0; size = 104
    big, end = text_block(command, y0, size, spacing=10, lead=1.12)
    parts = [big]; y = end + 80
    if sub:
        s_, end = text_block(sub, y, 40, weight=400, color=ASH, spacing=1)
        parts.append(s_); y = end + 70
    parts.append(rule(y)); y += 110
    v, end = verse(verse_lines, ref, y); parts.append(v)
    inner = centred("\n".join(parts), y0 - size*0.72, end)
    return frame(1080, 1350, "Marching Orders", inner=inner)


def slide(series, page, title=None, body=None, verse_lines=None, ref=None, cover=False, close=False):
    parts = []
    if cover:
        size = 100
        t, end = text_block(title, 0, size, spacing=10, lead=1.12); parts.append(t)
        y = end + 70; parts.append(rule(y)); end = y
        if body:
            b, end = text_block(body, y + 90, 40, weight=400, color=ASH, spacing=2); parts.append(b)
    elif close:
        size = 92
        t, end = text_block(title, 0, size, spacing=9, lead=1.15); parts.append(t)
        if body:
            b, end = text_block(body, end + 100, 42, weight=400, color=ASH); parts.append(b)
        parts.append(mark(SEAL, 440, end + 70, 200)); end = end + 270
    else:
        size = 76
        t, end = text_block(title, 0, size, spacing=6, lead=1.2); parts.append(t)
        y = end
        if body:
            b, y = text_block(body, y + 90, 40, weight=400, color=ASH, lead=1.35); parts.append(b)
        end = y
        if verse_lines:
            parts.append(rule(y + 70))
            v, end = verse(verse_lines, ref, y + 180); parts.append(v)
    inner = centred("\n".join(parts), -size*0.72, end)
    return frame(1080, 1350, series, page=page, inner=inner)


def story(title, body=None, w=1080, h=1920):
    """Story slide: all type inside y 260-1600 so Instagram's bars never cover it."""
    t, end = text_block(title, 1010, 92, spacing=9, lead=1.15)
    b = text_block(body, end + 110, 42, weight=400, color=ASH)[0] if body else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
{mark(SEAL, 290, 300, 500)}
{t}
{b}
<text x="540" y="1560" text-anchor="middle" font-family="{SANS}" font-weight="600" font-size="24" letter-spacing="6" fill="{ASH}">{HANDLE.upper()}</text>
</svg>'''


def render(svg_text, path, quality=94):
    """Rasterise onto a grained, vignetted iron ground."""
    w, h = (int(v) for v in re.search(r'viewBox="0 0 (\d+) (\d+)"', svg_text).groups())
    a = np.full((h, w, 3), 26, "int16") + np.random.default_rng(abs(hash(path)) % 2**32).normal(0, 7, (h, w))[..., None]
    base = Image.fromarray(a.clip(0, 255).astype("uint8"))
    v = Image.new("L", (w, h), 0)
    ImageDraw.Draw(v).ellipse((-w*0.25, -h*0.2, w*1.25, h*1.2), fill=255)
    base = Image.composite(base, Image.new("RGB", (w, h), "#0d0d0d"), v.filter(ImageFilter.GaussianBlur(w/6)))
    fg = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg_text.encode(), output_width=w))).convert("RGBA")
    base.paste(fg, (0, 0), fg)
    base.save(path, quality=quality)


# ---------------------------------------------------------------- launch set
# Scripture: CSB, quoted verbatim (partial verses marked with an ellipsis). See SOURCES.md.
LAUNCH = {
    "00_story_welcome.jpg": story(["KNOCKED DOWN.", "NOT [OUT]."],
        ["Faith, discipline and fatherhood", "for men who get back up."]),
    "01_marching_orders_proverbs24-16.jpg": marching_orders(
        ["YOU FELL.", "GET [UP]."],
        ["\u201cThough a righteous person falls", "seven times, he will get up\u2026\u201d"],
        "Proverbs 24:16, CSB",
        sub=["Make the bed. Open the Book. Go to work."]),
    "02_get_back_up_peter_1.jpg": slide("Get Back Up", "1 / 6",
        title=["THE MAN WHO", "DENIED HIM", "[THREE] TIMES"], body=["Peter. Swipe."], cover=True),
    "02_get_back_up_peter_2.jpg": slide("Get Back Up", "2 / 6",
        title=["He swore he would", "never fall."],
        verse_lines=["\u201cEven if I have to die with you,\u201d", "Peter told him, \u201cI will never deny you.\u201d"],
        ref="Matthew 26:35, CSB"),
    "02_get_back_up_peter_3.jpg": slide("Get Back Up", "3 / 6",
        title=["Before the rooster", "crowed, he denied", "Him [three] times."],
        verse_lines=["\u201cAnd he went outside", "and wept bitterly.\u201d"], ref="Luke 22:62, CSB"),
    "02_get_back_up_peter_4.jpg": slide("Get Back Up", "4 / 6",
        title=["Jesus didn\u2019t write", "him off."],
        body=["Three denials. Three questions.", "Three times restored."],
        verse_lines=["\u201cFeed my sheep,\u201d Jesus said."], ref="John 21:17, CSB"),
    "02_get_back_up_peter_5.jpg": slide("Get Back Up", "5 / 6",
        title=["Weeks later, the man", "who ran stood up", "and [preached]."],
        verse_lines=["\u201c\u2026that day about three thousand", "people were added to them.\u201d"], ref="Acts 2:41, CSB"),
    "02_get_back_up_peter_6.jpg": slide("Get Back Up", "6 / 6",
        title=["YOUR WORST NIGHT", "ISN\u2019T YOUR", "LAST [WORD]."], body=["Get back up."], close=True),
}

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "posts", "2026-10-13-launch")
    os.makedirs(out, exist_ok=True)
    for name, svg_text in LAUNCH.items():
        render(svg_text, os.path.join(out, name))
    print("\n".join(sorted(os.listdir(out))))
