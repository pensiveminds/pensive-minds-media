"""Rise, Wed Oct 28, 2026 (Chris asked for a Marching Orders post right away).

    python3 posts/2026-10-28-rise/build.py

Scripture: CSB, from VERSE_BANK.json (checked verbatim against BibleGateway, Oct 20, 2026). Logged in SOURCES.md.

  Wed Oct 28, ~5:00 PM  Marching Orders: Romans 12:21 (enemy) [Bone]
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from make_variants import mo_look, render_looks

SET = {}
SET["01_wed_marching_orders_rom12-21_bone.jpg"] = mo_look("bone",
    ["ANSWER IT", "WITH [GOOD]."],
    ["“Do not be conquered by evil,", "but conquer evil with good.”"],
    "Romans 12:21, CSB",
    sub=["Start with the man who wronged you."])

if __name__ == "__main__":
    print("\n".join(render_looks(SET, HERE)))
