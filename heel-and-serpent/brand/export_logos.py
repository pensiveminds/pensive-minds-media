"""Final Heel & Serpent logo system exports.

D Monogram  -> profile picture (reads best at avatar size)
C Seal      -> brand seal for merch, launch post, watermark on carousels
B Cross & Serpent -> post header mark and favicon-sized uses
"""
import io, os, re, sys
import numpy as np
import cairosvg
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from logos import concept_b, concept_c, concept_d, IRON, BONE, EMBER

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logos")
os.makedirs(OUT, exist_ok=True)


def transparent(svg_text):
    """Drop the iron background rect so the mark sits on anything."""
    return svg_text.replace(f'<rect width="1000" height="1000" fill="{IRON}"/>', "", 1)


def recolor(svg_text, fg):
    return svg_text.replace(f'"{BONE}"', f'"{fg}"')


def profile_d():
    s = concept_d()
    s = s.replace(f'<circle cx="500" cy="500" r="455" fill="none" stroke="{BONE}" stroke-width="3"/>', "")
    s = re.sub(r'<text x="500" y="770".*?</text>', "", s, flags=re.S)
    body = s.split(f'<rect width="1000" height="1000" fill="{IRON}"/>', 1)[1].rsplit("</svg>", 1)[0]
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">'
         f'<g transform="translate(500,520) scale(1.12) translate(-500,-500)">{body}</g></svg>')
    return s


def textured(svg_text, size=1080):
    a = np.full((size, size, 3), 26, "int16") + np.random.default_rng(7).normal(0, 8, (size, size))[..., None]
    base = Image.fromarray(a.clip(0, 255).astype("uint8"))
    v = Image.new("L", (size, size), 0)
    ImageDraw.Draw(v).ellipse((-200, -200, size + 200, size + 200), fill=255)
    base = Image.composite(base, Image.new("RGB", (size, size), "#0e0e0e"), v.filter(ImageFilter.GaussianBlur(180)))
    m = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg_text.encode(), output_width=size))).convert("RGBA")
    base.paste(m, (0, 0), m)
    return base


def save(name, svg_text, px=2000):
    open(f"{OUT}/{name}.svg", "w").write(svg_text)
    cairosvg.svg2png(bytestring=svg_text.encode(), write_to=f"{OUT}/{name}.png", output_width=px)


if __name__ == "__main__":
    textured(profile_d()).save(f"{OUT}/hs_profile_monogram_1080.png")
    save("hs_monogram_bone", transparent(concept_d()))
    save("hs_seal_bone", transparent(concept_c()))
    save("hs_seal_ember", recolor(transparent(concept_c()), EMBER))
    textured(concept_c()).save(f"{OUT}/hs_seal_on_iron_1080.png")
    save("hs_cross_serpent_bone", transparent(concept_b()))
    print(sorted(os.listdir(OUT)))
