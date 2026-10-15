"""Strike #4: James 4:7. First Reel with the Buzzfy changes: verse split into two quick shots, on-screen call
to action under the seal, motion (punch-in, embers, seal stamp). ~10.6 s.

    python3 reels/2026-10-15-james4-7/build.py

Scripture: CSB, checked verbatim against BibleGateway (CSB) on Oct 15, 2026 (context: James 4:1-10).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from make_reel import Scene, build_reel

SCENES = [
    Scene("big", 1.8, ["THE ENEMY", "IS BETTING", "YOU’LL [QUIT]."]),
    Scene("big", 1.4, ["[DON’T]."]),
    Scene("verse", 2.2, ["“Therefore,", "submit to God."]),
    Scene("verse", 2.6, ["Resist the devil,", "and he will flee", "from you.”"], ref="James 4:7, CSB"),
    Scene("seal", 2.6, ["STAND [FIRM]."], sub=["Send this to a brother."]),
]

if __name__ == "__main__":
    mp4, cuts, length = build_reel(SCENES, HERE, "strike_james4-7", fade=0.25, motion=True)
    print(mp4, cuts, length)
