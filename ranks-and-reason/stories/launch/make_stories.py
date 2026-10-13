"""Ranks & Reason launch stories (1080x1920). Text kept inside y 260-1600 (clear of IG story UI)."""
import pathlib, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
STILL = sys.argv[2] if len(sys.argv) > 2 else None
F = pathlib.Path("/home/claude/fonts")
SERIF, SERIF_I, SANS = str(F / "DMSerifDisplay-Regular.ttf"), str(F / "DMSerifDisplay-Italic.ttf"), str(F / "DMSans-VF.ttf")
W, H = 1080, 1920
BG, BONE, BRASS, RED, MUTED = (17, 18, 20), (233, 228, 216), (196, 146, 66), (178, 52, 40), (132, 128, 120)
rng = np.random.default_rng(7)


def sans(size, weight=700):
    f = ImageFont.truetype(SANS, size)
    try:
        f.set_variation_by_axes([weight if a.get("name") in (b"Weight", "Weight") else a["default"] for a in f.get_variation_axes()])
    except Exception:
        pass
    return f


def serif(size, italic=False):
    return ImageFont.truetype(SERIF_I if italic else SERIF, size)


def base():
    img = Image.new("RGB", (W, H), BG)
    a = np.asarray(img).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.75)) ** 2)
    a *= (1 - 0.55 * np.clip(d, 0, 1) ** 2)[..., None]
    a += rng.normal(0, 7, (H, W, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")


def header(d, left="RANKS & REASON", sub=None):
    d.text((80, 270), left, font=sans(34, 700), fill=BRASS)
    if sub:
        d.text((80, 316), sub, font=sans(30, 500), fill=MUTED)
    d.text((W - 80, 270), "@ranksandreason", font=sans(30, 500), fill=MUTED, anchor="ra")


def center(d, y, text, font, fill):
    d.text((W / 2, y), text, font=font, fill=fill, anchor="mt")


def rich_line(d, y, parts, font):
    """parts: list of (text, color). Centered on one line."""
    total = sum(d.textlength(t, font=font) for t, _ in parts)
    x = (W - total) / 2
    for t, c in parts:
        d.text((x, y), t, font=font, fill=c)
        x += d.textlength(t, font=font)


def rule(d, y, w=120):
    d.line([(W / 2 - w / 2, y), (W / 2 + w / 2, y)], fill=BRASS, width=3)


def chevrons(d, cx, cy, s=1.0):
    for i in range(3):
        y = cy + i * 46 * s
        d.line([(cx - 90 * s, y + 40 * s), (cx, y), (cx + 90 * s, y + 40 * s)], fill=BRASS, width=int(14 * s), joint="curve")


def save(img, name):
    p = OUT / name
    img.convert("RGB").save(p, quality=92)
    print(p)


# 1. Welcome
img = base(); d = ImageDraw.Draw(img)
header(d)
chevrons(d, W / 2, 560, 1.1)
center(d, 800, "Ranks", serif(150), BONE)
center(d, 960, "& Reason", serif(150), BONE)
rule(d, 1170)
center(d, 1220, "War, history & philosophy", serif(64), BONE)
rich_line(d, 1300, [("in ", BONE), ("under a minute.", BRASS)], serif(64))
center(d, 1460, "ONE CAMPAIGN AT A TIME", sans(34, 700), MUTED)
save(img, "rr_story_01_welcome.jpg")

# 2. Campaign No. 1 teaser (uses a still from the Reel)
img = base(); d = ImageDraw.Draw(img)
header(d, "CAMPAIGN No. 1", "MARATHON · 490 BC")
if STILL:
    m = Image.open(STILL).convert("RGBA").crop((40, 270, 1040, 1170)).resize((880, 792))
    mask = Image.new("L", m.size, 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, m.size[0] - 1, m.size[1] - 1], 24, fill=255)
    img.paste(m, (100, 420), mask)
d = ImageDraw.Draw(img)
rich_line(d, 1250, [("10,000", BRASS), (" Athenians.", BONE)], serif(76))
center(d, 1375, "The largest empire on Earth.", serif(60), BONE)
center(d, 1462, "One general's gamble.", serif(60, True), MUTED)
center(d, 1580, "DROPS WEDNESDAY · 10 AM CT", sans(36, 700), BRASS)
save(img, "rr_story_02_campaign1.jpg")

# 3. Ideas that shaped war: Sun Tzu (Giles translation, 1910, public domain)
img = base(); d = ImageDraw.Draw(img)
header(d, "IDEAS THAT SHAPED WAR")
center(d, 560, "“", serif(260), BRASS)
center(d, 820, "All warfare", serif(124), BONE)
center(d, 960, "is based on", serif(124), BONE)
center(d, 1100, "deception.", serif(124), BRASS)
rule(d, 1300)
center(d, 1340, "SUN TZU, THE ART OF WAR, I.18", sans(32, 700), BONE)
center(d, 1392, "tr. Lionel Giles, 1910", sans(28, 500), MUTED)
save(img, "rr_story_03_suntzu.jpg")

# 4. Myth vs record teaser for Part 2
img = base(); d = ImageDraw.Draw(img)
header(d, "MYTH vs RECORD")
center(d, 560, "The famous run", serif(96), BONE)
center(d, 670, "from Marathon to Athens?", serif(80), BONE)
rule(d, 830)
rich_line(d, 900, [("Herodotus ", BONE), ("never", RED), (" mentions it.", BONE)], serif(72))
center(d, 1060, "The run he did record", serif(58), MUTED)
center(d, 1140, "was longer, and it mattered more.", serif(58), MUTED)
center(d, 1330, "PART 2 THIS WEEK", sans(40, 700), BRASS)
center(d, 1390, "Follow so you don't miss it.", sans(32, 500), MUTED)
save(img, "rr_story_04_myth.jpg")
