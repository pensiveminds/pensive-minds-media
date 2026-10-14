"""Story set "Tomorrow starts tonight", Tue Oct 13, 2026, ~10:20 PM. Three Story videos with the
motivational score (make_reel.score_drive).

    python3 stories/2026-10-13-tomorrow-starts-tonight/build.py

Scripture: Isaiah 40:31, CSB, checked verbatim against BibleGateway (CSB) on Oct 13, 2026 (context: Isaiah 40:28-31).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from make_reel import Scene, build_reel, score_drive

STORIES = {
    "01_tomorrow_starts_tonight": [
        Scene("big", 2.9, ["TOMORROW", "STARTS", "[TONIGHT]."]),
        Scene("big", 2.9, ["ALARM [SET].", "PHONE ACROSS", "THE ROOM."]),
    ],
    "02_lay_it_out": [
        Scene("big", 2.9, ["BIBLE ON THE", "[NIGHTSTAND]."]),
        Scene("big", 2.9, ["BOOTS BY", "THE [DOOR]."]),
    ],
    "03_rise": [
        Scene("verse", 5.8, ["“…those who trust in the LORD", "will renew their strength;", "they will soar on wings like eagles;",
                             "they will run and not become weary,", "they will walk and not faint.”"], ref="Isaiah 40:31, CSB"),
        Scene("seal", 3.0, ["RISE [EARLY]."]),
    ],
}

if __name__ == "__main__":
    for name, scenes in STORIES.items():
        mp4, cuts, length = build_reel(scenes, HERE, name, score_fn=score_drive)
        print(name, cuts, length)
