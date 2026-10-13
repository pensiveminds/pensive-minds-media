"""Ranks & Reason avatar options, 1080x1080 (Instagram crops to a circle)."""
import math, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 1080
OUT = pathlib.Path("/home/claude/rr"); OUT.mkdir(exist_ok=True)
SERIF = "/home/claude/fonts/DMSerifDisplay-Regular.ttf"
SERIF_I = "/home/claude/fonts/DMSerifDisplay-Italic.ttf"
BG, BONE, BRASS = (18, 20, 22), (233, 228, 216), (190, 142, 64)
rng = np.random.default_rng(9)

def base():
    a = np.full((S, S, 3), BG, np.float32)
    yy, xx = np.mgrid[0:S, 0:S]
    d = np.hypot(xx - S / 2, yy - S / 2) / (S / 2)
    a *= (1.12 - 0.35 * np.clip(d, 0, 1) ** 2)[..., None]
    a += rng.normal(0, 5, (S, S, 1))
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")

def chevrons(d, cx, top, w, h, n, gap, color, thick):
    for i in range(n):
        y = top + i * gap
        pts = [(cx - w / 2, y + h), (cx, y), (cx + w / 2, y + h), (cx + w / 2, y + h + thick), (cx, y + thick), (cx - w / 2, y + h + thick)]
        d.polygon(pts, fill=color)

def laurel(d, cx, cy, r, side, color, leaves=9):
    for i in range(leaves):
        t = math.radians(200 + i * 15) if side < 0 else math.radians(-20 - i * 15)
        x, y = cx + r * math.cos(t), cy - r * math.sin(t)
        ang = t + (math.pi / 2 if side < 0 else -math.pi / 2)
        L, Wd = 46, 18
        pts = []
        for k in range(24):
            u = k / 23 * 2 * math.pi
            px, py = L * math.cos(u), Wd * math.sin(u)
            pts.append((x + px * math.cos(ang + 0.5 * side) - py * math.sin(ang + 0.5 * side),
                        y + px * math.sin(ang + 0.5 * side) + py * math.cos(ang + 0.5 * side)))
        d.polygon(pts, fill=color)

def centered(d, text, font, y, fill):
    w = d.textlength(text, font=font); d.text(((S - w) / 2, y), text, font=font, fill=fill)

# A: three brass chevrons over an R&R monogram
img = base(); d = ImageDraw.Draw(img)
chevrons(d, S / 2, 250, 380, 120, 3, 62, BRASS, 34)
f = ImageFont.truetype(SERIF, 230); fa = ImageFont.truetype(SERIF_I, 230)
wR = d.textlength("R", font=f); wA = d.textlength("&", font=fa)
x = (S - (2 * wR + wA + 20)) / 2; y = 520
d.text((x, y), "R", font=f, fill=BONE); d.text((x + wR + 10, y), "&", font=fa, fill=BRASS); d.text((x + wR + wA + 20, y), "R", font=f, fill=BONE)
img.convert("RGB").save(OUT / "avatar_A_chevrons.png")

# B: chevrons + monogram inside a brass ring
img = base(); d = ImageDraw.Draw(img)
d.ellipse([90, 90, S - 90, S - 90], outline=BRASS, width=14)
chevrons(d, S / 2, 290, 320, 100, 3, 52, BRASS, 28)
f = ImageFont.truetype(SERIF, 200); fa = ImageFont.truetype(SERIF_I, 200)
wR = d.textlength("R", font=f); wA = d.textlength("&", font=fa)
x = (S - (2 * wR + wA + 20)) / 2; y = 520
d.text((x, y), "R", font=f, fill=BONE); d.text((x + wR + 10, y), "&", font=fa, fill=BRASS); d.text((x + wR + wA + 20, y), "R", font=f, fill=BONE)
img.convert("RGB").save(OUT / "avatar_B_ring_chevrons.png")

# C: bold monogram only, brass ring
img = base(); d = ImageDraw.Draw(img)
d.ellipse([90, 90, S - 90, S - 90], outline=BRASS, width=14)
d.ellipse([130, 130, S - 130, S - 130], outline=(110, 84, 40), width=3)
f = ImageFont.truetype(SERIF, 300); fa = ImageFont.truetype(SERIF_I, 260)
wR = d.textlength("R", font=f); wA = d.textlength("&", font=fa)
x = (S - (2 * wR + wA + 10)) / 2; y = 360
d.text((x, y), "R", font=f, fill=BONE); d.text((x + wR + 5, y + 30), "&", font=fa, fill=BRASS); d.text((x + wR + wA + 10, y), "R", font=f, fill=BONE)
img.convert("RGB").save(OUT / "avatar_C_ring.png")

# preview as circles
prev = Image.new("RGB", (3 * 360 + 40, 400), (240, 240, 240))
for i, n in enumerate(["avatar_A_chevrons", "avatar_B_ring_chevrons", "avatar_C_ring"]):
    im = Image.open(OUT / f"{n}.png").resize((340, 340), Image.LANCZOS)
    m = Image.new("L", (340, 340), 0); ImageDraw.Draw(m).ellipse([0, 0, 339, 339], fill=255)
    prev.paste(im, (20 + i * 360, 30), m)
prev.save(OUT / "avatar_preview.png"); print("ok")
