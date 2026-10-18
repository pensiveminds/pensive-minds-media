"""Ranks & Reason Story: the Great Chain at West Point (Myth vs record).
Sources: Albany Institute, "Iron Link from the Great Chain Across the Hudson River" (1778, about 65 tons);
Wikipedia, "Hudson River Chains" (1778 installation, Great Chain at West Point);
West Point Press, "Key of America" (British never attacked West Point);
American Battlefield Trust, "West Point: The Gibraltar of the Hudson" (Arnold took command Aug 3, 1780, sought to surrender it)."""
import pathlib, sys
sys.argv = [sys.argv[0], "/dev/null"]
here = pathlib.Path(__file__).resolve().parent
exec(compile((here.parent / "launch" / "make_stories.py").read_text().split("# 1. Welcome")[0], "make_stories", "exec"))
OUT = here

img = base(); d = ImageDraw.Draw(img)
header(d, "MYTH vs RECORD", "WEST POINT · 1778")
center(d, 470, "THE MYTH", sans(32, 700), RED)
center(d, 530, "A chain stopped", serif(88), BONE)
center(d, 635, "the British fleet.", serif(88), BONE)
rule(d, 800)
center(d, 850, "THE RECORD", sans(32, 700), BRASS)
rich_line(d, 910, [("The British ", BONE), ("never", BRASS)], serif(88))
center(d, 1030, "attacked West Point.", serif(88), BONE)
center(d, 1215, "65 tons of iron across the Hudson, 1778.", serif(46, True), MUTED)
center(d, 1370, "Two years later, its own commander", serif(52), BONE)
center(d, 1440, "tried to hand it to them.", serif(52), BONE)
center(d, 1545, "ALBANY INSTITUTE · WEST POINT PRESS", sans(24, 500), MUTED)
center(d, 1580, "AMERICAN BATTLEFIELD TRUST", sans(24, 500), MUTED)
save(img, "rr_story_07_west_point_chain.jpg")
