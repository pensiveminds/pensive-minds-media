"""Story set "First light", Wed Oct 14, 2026, early morning. Four Story videos, ONE continuous score
(make_reel.build_story_set with score_drive), in the one-off "dawn" palette (Chris, Oct 14: a single
break from the iron/ember grid, not a change to the brand).

    python3 stories/2026-10-14-first-light/build.py

Scripture: Mark 1:35, CSB, checked verbatim against BibleGateway (CSB) on Oct 14, 2026
(context read: Mark 1:32-39; he rose to pray the morning after healing the whole town late into the night).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from make_reel import Scene, build_story_set, use_palette

STORIES = {
    "01_still_dark": [
        Scene("big", 2.8, ["IT'S STILL", "[DARK]."]),
        Scene("big", 2.8, ["THE HOUSE", "IS [QUIET]."]),
    ],
    "02_before_the_noise": [
        Scene("big", 2.6, ["BEFORE THE", "PHONE."]),
        Scene("big", 2.6, ["BEFORE THE", "[NOISE]."]),
    ],
    "03_mark_1_35": [
        Scene("verse", 7.0, ["“Very early in the morning,", "while it was still dark,", "he got up, went out,",
                             "and made his way to a deserted place;", "and there he was praying.”"], ref="Mark 1:35, CSB"),
    ],
    "04_meet_him_first": [
        Scene("big", 2.6, ["MISSED IT", "YESTERDAY?"], sub=["It's still dark today."]),
        Scene("seal", 3.2, ["MEET HIM", "[FIRST]."]),
    ],
}

if __name__ == "__main__":
    use_palette("dawn")
    for name, mp4, a, b in build_story_set(STORIES, HERE):
        print(name, round(a, 2), round(b, 2))
