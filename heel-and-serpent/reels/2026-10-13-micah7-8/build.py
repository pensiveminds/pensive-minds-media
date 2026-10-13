"""Strike #1: Micah 7:8. Original score, built by make_reel.score().

    python3 reels/2026-10-13-micah7-8/build.py

Scripture: CSB, checked verbatim against BibleGateway (CSB) on Oct 13, 2026 (context read: Micah 7:7-9).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from make_reel import Scene, build_reel

SCENES = [
    Scene("big", 2.6, ["YOU’RE", "[DOWN]."]),
    Scene("big", 2.6, ["HE THINKS", "IT’S [OVER]."]),
    Scene("big", 2.2, ["IT [ISN’T]."]),
    Scene("verse", 5.8, ["“Do not rejoice over me,", "my enemy!", "Though I have fallen,", "I will stand up;",
                         "though I sit in darkness,", "the LORD will be my light.”"], ref="Micah 7:8, CSB"),
    Scene("seal", 3.2, ["GET BACK [UP]."]),
]

if __name__ == "__main__":
    mp4, cuts, length = build_reel(SCENES, HERE, "strike_micah7-8")
    print(mp4, cuts, length)
