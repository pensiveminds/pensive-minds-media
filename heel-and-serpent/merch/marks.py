"""Heel & Serpent merch marks: the locked logos recoloured for garments.

Each mark is drawn by brand/logos.py and only recoloured here, so the merch
always matches the page. Outputs transparent SVG + PNG into merch/marks/.

  python merch/marks.py

Colour terms
  fg     thread / ink colour of the mark
  knock  the garment colour (fills the cut-outs: the cross outline, the eye)
  ember  EMBER for the one hidden detail, or fg to run single colour
"""
import os, re, sys
import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "brand"))
from logos import concept_b, concept_c, concept_d, IRON, BONE, EMBER, ASH

OUT = os.path.join(HERE, "marks")

# Garment grounds and threads
GROUND = {"iron": IRON, "bone": BONE}
TONAL = {"iron": "#3B3936", "bone": "#CFC7B8"}   # tonal thread: a shade off the garment


def _strip(s):
    s = s.replace(f'<rect width="1000" height="1000" fill="{IRON}"/>', "", 1)
    return s


def _color(s, fg, knock, ember, ash=None):
    # placeholders first so swaps don't collide
    for k, v in ((BONE, "@FG@"), (IRON, "@KN@"), (EMBER, "@EM@"), (ASH, "@AS@")):
        s = s.replace(f'"{k}"', f'"{v}"')
    return (s.replace('"@FG@"', f'"{fg}"').replace('"@KN@"', f'"{knock}"')
             .replace('"@EM@"', f'"{ember}"').replace('"@AS@"', f'"{ash or fg}"'))


def cross_serpent(fg, knock, ember):
    s = _strip(concept_b())
    s = re.sub(r'<circle cx="500" cy="500" r="4[45][05]".*?/>', "", s)   # drop the rings
    return _color(s, fg, knock, ember)


def monogram(fg, knock, ember):
    s = _strip(concept_d())
    s = re.sub(r'<circle cx="500" cy="500" r="455".*?/>', "", s)
    s = re.sub(r'<text x="500" y="770".*?</text>', "", s, flags=re.S)
    return _color(s, fg, knock, ember)


def seal(fg, knock, ember, ash=None):
    return _color(_strip(concept_c()), fg, knock, ember, ash)


def line(text, fg, size=86, spacing=26, w=1600, h=200, italic=False):
    st = ' font-style="italic"' if italic else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<text x="{w/2}" y="{h/2 + size*0.34:.0f}" text-anchor="middle" font-family="EB Garamond" '
            f'font-weight="500" font-size="{size}" letter-spacing="{spacing}" fill="{fg}"{st}>{text}</text></svg>')


LINES = {"bruised": "BRUISED, NOT BEATEN.", "heeldown": "HEEL DOWN.",
         "crush": "CRUSH THE HEAD.", "genesis": "GENESIS III · XV"}


def build():
    os.makedirs(OUT, exist_ok=True)
    jobs = {}
    for g in ("iron", "bone"):
        kn, tn = GROUND[g], TONAL[g]
        contrast = BONE if g == "iron" else IRON
        jobs[f"cross_serpent_tonal_on_{g}"] = cross_serpent(tn, kn, tn)
        jobs[f"cross_serpent_contrast_on_{g}"] = cross_serpent(contrast, kn, EMBER)
        jobs[f"monogram_tonal_on_{g}"] = monogram(tn, kn, EMBER)       # ember ampersand kept: the hidden detail
        jobs[f"monogram_contrast_on_{g}"] = monogram(contrast, kn, EMBER)
        jobs[f"seal_contrast_on_{g}"] = seal(contrast, kn, EMBER, ASH)
        jobs[f"seal_tonal_on_{g}"] = seal(tn, kn, EMBER, tn)
        for k, t in LINES.items():
            jobs[f"line_{k}_tonal_on_{g}"] = line(t, tn)
            jobs[f"line_{k}_contrast_on_{g}"] = line(t, contrast if k != "genesis" else ASH)
    # leather patch: the Seal debossed (dark tan on tan, no ember)
    jobs["seal_leather"] = seal(LEATHER_DEEP, LEATHER, LEATHER_DEEP, LEATHER_DEEP)
    for name, s in jobs.items():
        open(f"{OUT}/{name}.svg", "w").write(s)
        cairosvg.svg2png(bytestring=s.encode(), write_to=f"{OUT}/{name}.png", output_width=1600)
    knit("cross_serpent_contrast_on_iron", "knit_cross_serpent_on_iron")
    return sorted(jobs) + ["knit_cross_serpent_on_iron"]


LEATHER, LEATHER_DEEP = "#8B5E3C", "#5C3B24"


def knit(src, name, stitches=44):
    """Snap a mark to a knit grid (one pixel = one stitch) so it reads as it will on a sock."""
    from PIL import Image
    im = Image.open(f"{OUT}/{src}.png").convert("RGBA")
    a = im.getchannel("A").point(lambda v: 255 if v > 90 else 0)
    im.putalpha(a)
    small = im.resize((stitches, stitches), Image.BOX)
    px = small.load()
    bone = tuple(int(BONE[i:i+2], 16) for i in (1, 3, 5))
    for y in range(stitches):          # two yarns only: bone stitch or the sock's own iron
        for x in range(stitches):
            r, g, b, al = px[x, y]
            lit = al > 50 and (r + g + b) * al / 255 > 160
            px[x, y] = bone + (255,) if lit else (0, 0, 0, 0)
    small.resize((1600, 1600), Image.NEAREST).save(f"{OUT}/{name}.png")


if __name__ == "__main__":
    print("\n".join(build()))
