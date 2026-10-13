"""Intro carousel, posted Oct 13, 2026 (pin to the top of the profile).

    python3 posts/2026-10-13-intro/build.py

Scripture: CSB, checked verbatim against BibleGateway (CSB) on Oct 13, 2026. Logged in SOURCES.md.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from make_posts import slide, render_set

S = "Start Here"
SET = {
    "01_intro_1.jpg": slide(S, "1 / 6", title=["WHY HEEL", "& [SERPENT]"], body=["Start here. Swipe."], cover=True),
    "01_intro_2.jpg": slide(S, "2 / 6", title=["It starts in", "a [garden]."],
        body=["The first promise after the fall."],
        verse_lines=["“…He will strike your head,", "and you will strike his heel.”"], ref="Genesis 3:15, CSB"),
    "01_intro_3.jpg": slide(S, "3 / 6", title=["The heel gets", "[bruised].", "The head gets crushed."],
        body=["A wound isn’t a defeat."]),
    "01_intro_4.jpg": slide(S, "4 / 6", title=["Won at the", "[cross]."],
        body=["The fight is spiritual. The ending is settled."],
        verse_lines=["“The God of peace will soon crush", "Satan under your feet…”"], ref="Romans 16:20, CSB"),
    "01_intro_5.jpg": slide(S, "5 / 6", title=["What you’ll", "find [here]."],
        body=["Mornings: Marching Orders.", "Evenings: Get Back Up.", "Sundays: Armor Check."]),
    "01_intro_6.jpg": slide(S, "6 / 6", title=["BRUISED,", "NOT [BEATEN]."], body=["Follow. Then get back up."], close=True),
}

if __name__ == "__main__":
    print("\n".join(render_set(SET, HERE)))
