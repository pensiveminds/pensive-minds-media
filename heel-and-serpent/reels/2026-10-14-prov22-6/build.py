"""Strike #3: Proverbs 22:6 (fathers). Fast pacing: hook on frame 0, verse by ~5 s, ~11 s total.

    python3 reels/2026-10-14-prov22-6/build.py

Scripture: CSB, checked verbatim against BibleGateway (CSB) on Oct 14, 2026 (context read: Proverbs 22:1-6).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from make_reel import Scene, build_reel

SCENES = [
    Scene("big", 1.8, ["YOUR KIDS", "ARE", "[WATCHING]."]),
    Scene("big", 1.5, ["NOT YOUR", "[WORDS]."]),
    Scene("big", 1.5, ["YOUR [HABITS]."]),
    Scene("verse", 4.2, ["“Start a youth out on his way;", "even when he grows old", "he will not depart from it.”"],
          ref="Proverbs 22:6, CSB"),
    Scene("seal", 2.2, ["SHOW THEM [HOW]."]),
]

if __name__ == "__main__":
    mp4, cuts, length = build_reel(SCENES, HERE, "strike_prov22-6", fade=0.25)
    print(mp4, cuts, length)
