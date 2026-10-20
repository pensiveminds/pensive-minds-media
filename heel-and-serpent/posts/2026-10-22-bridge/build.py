"""Bridge set: Thu Oct 22 and Fri Oct 23, 2026, the first days on the one-feed-post-a-day schedule
(Chris, Oct 20, 2026). From Oct 24 the weekly scheduled task builds the feed.

    python3 posts/2026-10-22-bridge/build.py

Scripture: CSB, from VERSE_BANK.json (checked verbatim against BibleGateway on Oct 20, 2026). Partial verses
are marked with an ellipsis. Every verse is logged in SOURCES.md.

  Thu Oct 22, 7:15 PM  Get Back Up: Gideon, hiding in the winepress (get back up) [Classic]
  Fri Oct 23, 6:45 AM  Marching Orders: Luke 9:23 (discipline) [Ledger]
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from make_variants import mo_look, carousel, render_looks

SET = {}
SET.update(carousel("classic", "01_thu_get_back_up_gideon", "Get Back Up", [
    dict(title=["HIDING IN THE", "[WINEPRESS]"], body=["Gideon. Swipe."], cover=True),
    dict(title=["He was hiding."], body=["Doing his work where the enemy couldn’t see."],
         verse_lines=["“…Gideon was threshing wheat", "in the winepress in order to hide it", "from the Midianites.”"],
         ref="Judges 6:11, CSB"),
    dict(title=["God called him", "what he wasn’t [yet]."],
         verse_lines=["“…The LORD is with you,", "valiant warrior.”"], ref="Judges 6:12, CSB"),
    dict(title=["He gave every", "[excuse]."],
         verse_lines=["“…Look, my family is the weakest", "in Manasseh, and I am the youngest", "in my father’s family.”"],
         ref="Judges 6:15, CSB"),
    dict(title=["God didn’t argue.", "He [promised]."],
         verse_lines=["“But I will be with you,”", "the LORD said to him…"], ref="Judges 6:16, CSB"),
    dict(title=["GO IN THE", "STRENGTH", "YOU [HAVE]."], body=["Get back up."], close=True),
]))
SET["02_fri_marching_orders_luke9-23_ledger.jpg"] = mo_look("ledger",
    ["TAKE IT UP", "[DAILY]."],
    ["“…let him deny himself, take up", "his cross daily, and follow me.”"],
    "Luke 9:23, CSB",
    sub=["Not once. Every morning."])

if __name__ == "__main__":
    print("\n".join(render_looks(SET, HERE)))
