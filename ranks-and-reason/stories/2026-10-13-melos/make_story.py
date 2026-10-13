"""Ranks & Reason Story: the Melian Dialogue (Thucydides 5.89, tr. Richard Crawley, 1874)."""
import pathlib, sys
sys.argv = [sys.argv[0], "/dev/null"]
here = pathlib.Path(__file__).resolve().parent
exec(compile((here.parent / "launch" / "make_stories.py").read_text().split("# 1. Welcome")[0], "make_stories", "exec"))
OUT = here

img = base(); d = ImageDraw.Draw(img)
header(d, "IDEAS THAT SHAPED WAR", "MELOS · 416 BC")
center(d, 430, "“", serif(220), BRASS)
center(d, 640, "The strong", serif(120), BONE)
center(d, 780, "do what they can,", serif(96), BONE)
center(d, 920, "and the weak", serif(120), BONE)
rich_line(d, 1040, [("suffer what they ", BONE), ("must.", BRASS)], serif(96))
rule(d, 1230)
center(d, 1270, "ATHENIAN ENVOYS TO THE MELIANS", sans(30, 700), BONE)
center(d, 1316, "THUCYDIDES 5.89 · tr. Richard Crawley, 1874", sans(26, 500), MUTED)
center(d, 1420, "Melos refused to bend. Athens took the island.", serif(44, True), MUTED)
center(d, 1540, "CAMPAIGN No. 1 · TOMORROW, 10 AM CT", sans(34, 700), BRASS)
save(img, "rr_story_06_melos.jpg")
