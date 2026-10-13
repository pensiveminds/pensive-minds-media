"""Ranks & Reason feed carousel (1080x1350): the Melian Dialogue. Thucydides 5.84-116, tr. Richard Crawley, 1874."""
import pathlib, sys
sys.argv = [sys.argv[0], "/dev/null"]
here = pathlib.Path(__file__).resolve().parent
exec(compile((here.parent.parent / "stories" / "launch" / "make_stories.py").read_text().split("# 1. Welcome")[0], "make_stories", "exec"))
OUT = here
W, H = 1080, 1350


def base():
    img = Image.new("RGB", (W, H), BG)
    a = np.asarray(img).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    dd = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.75)) ** 2)
    a *= (1 - 0.55 * np.clip(dd, 0, 1) ** 2)[..., None]
    a += rng.normal(0, 7, (H, W, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")


def frame(page):
    img = base(); d = ImageDraw.Draw(img)
    d.text((80, 80), "IDEAS THAT SHAPED WAR", font=sans(30, 700), fill=BRASS)
    d.text((80, 122), "MELOS · 416 BC", font=sans(26, 500), fill=MUTED)
    d.text((W - 80, 80), "RANKS & REASON", font=sans(28, 700), fill=MUTED, anchor="ra")
    d.text((80, H - 90), "@ranksandreason", font=sans(26, 500), fill=MUTED)
    d.text((W - 80, H - 90), f"{page} / 4", font=sans(26, 700), fill=MUTED, anchor="ra")
    return img, d


# 1. Hook
img, d = frame(1)
center(d, 380, "416 BC.", serif(84), BRASS)
center(d, 500, "The greatest navy", serif(92), BONE)
center(d, 610, "in Greece lands on", serif(92), BONE)
center(d, 720, "a tiny island.", serif(92), BONE)
rule(d, 880)
center(d, 930, "Melos wanted to stay neutral.", serif(54), MUTED)
center(d, 1000, "Athens gave it one choice.", serif(54, True), MUTED)
center(d, 1130, "SWIPE", sans(30, 700), BRASS)
save(img, "rr_melos_1.jpg")

# 2. The quote
img, d = frame(2)
center(d, 260, "“", serif(200), BRASS)
center(d, 440, "The strong", serif(112), BONE)
center(d, 570, "do what they can,", serif(90), BONE)
center(d, 700, "and the weak", serif(112), BONE)
rich_line(d, 805, [("suffer what they ", BONE), ("must.", BRASS)], serif(90))
rule(d, 990)
center(d, 1030, "THE ATHENIAN ENVOYS · THUCYDIDES 5.89", sans(28, 700), BONE)
center(d, 1076, "tr. Richard Crawley, 1874", sans(26, 500), MUTED)
save(img, "rr_melos_2.jpg")

# 3. The answer
img, d = frame(3)
center(d, 330, "Melos answered:", serif(70), MUTED)
rich_line(d, 440, [("700", BRASS), (" years free.", BONE)], serif(110))
center(d, 590, "They would not give it up", serif(80), BONE)
center(d, 690, "in a moment.", serif(80), BONE)
rule(d, 860)
center(d, 910, "They trusted in fortune", serif(54), MUTED)
center(d, 980, "and in Sparta.", serif(54), MUTED)
center(d, 1110, "THUCYDIDES 5.112", sans(26, 700), MUTED)
save(img, "rr_melos_3.jpg")

# 4. The ending
img, d = frame(4)
rich_line(d, 270, [("Sparta never ", BONE), ("came.", RED)], serif(100))
center(d, 460, "Melos fell that winter.", serif(70), BONE)
center(d, 540, "Athens planted 500 colonists", serif(54), MUTED)
center(d, 610, "on the island.", serif(54), MUTED)
rule(d, 760)
center(d, 810, "The next summer, Athens", serif(70), BONE)
rich_line(d, 885, [("sailed for ", BONE), ("Sicily.", BRASS)], serif(70))
center(d, 1030, "It would not end the way they planned.", serif(46, True), MUTED)
center(d, 1130, "THUCYDIDES 5.116, 6.30 · FOLLOW FOR MORE", sans(26, 700), MUTED)
save(img, "rr_melos_4.jpg")
