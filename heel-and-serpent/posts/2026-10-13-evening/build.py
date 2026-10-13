"""Two evening posts, Tue Oct 13, 2026 (first posts in the rotating looks).

    python3 posts/2026-10-13-evening/build.py

  5:45 PM  Marching Orders (Bone): warrior father, Deuteronomy 6:7
  8:30 PM  Get Back Up (Ledger): the lie "you're the only one" (Elijah, 1 Kings 19; Ecclesiastes 4:10)

Scripture: CSB, checked verbatim against BibleGateway (CSB) on Oct 13, 2026. Logged in SOURCES.md.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from make_variants import mo_look, carousel, render_looks

SET = {}
SET["01_tue_marching_orders_deut6-7_bone.jpg"] = mo_look("bone",
    ["BE HOME", "WHEN YOU’RE [HOME]."],
    ["“Repeat them to your children.", "Talk about them when you sit", "in your house…”"],
    "Deuteronomy 6:7, CSB",
    sub=["Phone in the drawer. Eyes on your kids."])

SET.update(carousel("ledger", "02_tue_get_back_up_only_one", "Get Back Up", [
    dict(title=["THE LIE:", "YOU’RE THE", "ONLY [ONE]."], body=["Swipe."], cover=True),
    dict(title=["Elijah believed", "it [too]."], body=["Worn out, afraid, hiding in a cave."],
         verse_lines=["“…I alone am left, and they are", "looking for me to take my life.”"], ref="1 Kings 19:10, CSB"),
    dict(title=["God didn’t lecture", "him. He [fed] him."],
         verse_lines=["“…Suddenly, an angel touched him.", "The angel told him, ‘Get up and eat.’”"], ref="1 Kings 19:5, CSB"),
    dict(title=["Then He told him", "the [truth]."],
         verse_lines=["“But I will leave seven thousand", "in Israel—every knee that has not", "bowed to Baal…”"],
         ref="1 Kings 19:18, CSB"),
    dict(title=["You weren’t built", "to fight [alone]."],
         verse_lines=["“For if either falls, his companion", "can lift him up; but pity the one", "who falls without another", "to lift him up.”"],
         ref="Ecclesiastes 4:10, CSB"),
    dict(title=["CALL A", "BROTHER", "[TONIGHT]."], body=["Get back up."], close=True),
]))

if __name__ == "__main__":
    print("\n".join(render_looks(SET, HERE)))
