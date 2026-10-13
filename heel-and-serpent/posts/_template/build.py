"""Template for a new post set. Copy this folder to posts/<YYYY-MM-DD>-<set>/, fill in SET, run it.

    python3 posts/2026-10-19-week1/build.py

Rules: CSB verses verbatim (check the wording against a published CSB source), reference shown
as "Book C:V, CSB", one [bracketed] ember word per line, and log every verse in SOURCES.md.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from make_posts import marching_orders, slide, story, render_set

SET = {
    # "01_mon_marching_orders.jpg": marching_orders(
    #     ["COMMAND LINE.", "WITH ONE [WORD]."],
    #     ["“Verse line one,", "verse line two.”"],
    #     "Book 1:1, CSB",
    #     sub=["Optional plain line."]),
    # "02_mon_get_back_up_1.jpg": slide("Get Back Up", "1 / 6", title=["COVER", "[TITLE]"], body=["Swipe."], cover=True),
    # "02_mon_get_back_up_2.jpg": slide("Get Back Up", "2 / 6", title=["Story beat."],
    #     verse_lines=["“Verse.”"], ref="Book 1:1, CSB"),
    # "02_mon_get_back_up_6.jpg": slide("Get Back Up", "6 / 6", title=["CLOSING", "[LINE]."], body=["Get back up."], close=True),
}

if __name__ == "__main__":
    print("\n".join(render_set(SET, HERE)))
