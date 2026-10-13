"""Ranks & Reason Story: the deciding vote at Marathon (Herodotus 6.109-110, tr. A. D. Godley, 1920)."""
import pathlib, sys
sys.argv = [sys.argv[0], "/dev/null"]  # keep the launch builder from writing its own slides
here = pathlib.Path(__file__).resolve().parent
exec(compile((here.parent / "launch" / "make_stories.py").read_text().split("# 1. Welcome")[0], "make_stories", "exec"))
OUT = here

img = base(); d = ImageDraw.Draw(img)
header(d, "COMMANDERS & CHOICES", "MARATHON · 490 BC")
center(d, 470, "Ten generals.", serif(104), BONE)
rich_line(d, 580, [("A ", BONE), ("divided", BRASS), (" vote.", BONE)], serif(104))
center(d, 770, "The deciding ballot belonged to one man:", serif(46), MUTED)
center(d, 840, "Callimachus, the war archon.", serif(46, True), MUTED)
rule(d, 970)
center(d, 1010, "“", serif(170), BRASS)
center(d, 1150, "It is now in your hands", serif(74), BONE)
center(d, 1240, "to enslave Athens", serif(74), BONE)
rich_line(d, 1310, [("or make her ", BONE), ("free.", BRASS)], serif(74))
center(d, 1470, "MILTIADES TO CALLIMACHUS · HERODOTUS 6.109 · tr. A. D. GODLEY", sans(24, 700), MUTED)
center(d, 1560, "HE VOTED TO FIGHT. TOMORROW, 10 AM CT.", sans(36, 700), BRASS)
save(img, "rr_story_05_callimachus.jpg")
