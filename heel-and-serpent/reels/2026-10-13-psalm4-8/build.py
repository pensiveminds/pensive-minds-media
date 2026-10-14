"""Strike #2: Psalm 4:8 (night). Original score, built by make_reel.score().

    python3 reels/2026-10-13-psalm4-8/build.py

Scripture: CSB, checked verbatim against BibleGateway (CSB) on Oct 13, 2026 (context read: Psalm 4:6-8; Psalm 121:1-4).
"HE NEVER SLEEPS" paraphrases Psalm 121:4, which the caption quotes with its reference.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from make_reel import Scene, build_reel

SCENES = [
    Scene("big", 2.6, ["YOU CARRIED IT", "ALL [DAY]."]),
    Scene("big", 2.4, ["SET IT", "[DOWN]."]),
    Scene("big", 2.4, ["HE NEVER", "[SLEEPS]."]),
    Scene("verse", 5.8, ["“I will both lie down", "and sleep in peace,", "for you alone, LORD,", "make me live in safety.”"],
          ref="Psalm 4:8, CSB"),
    Scene("seal", 3.2, ["REST. THEN [RISE]."]),
]

if __name__ == "__main__":
    mp4, cuts, length = build_reel(SCENES, HERE, "strike_psalm4-8")
    print(mp4, cuts, length)
