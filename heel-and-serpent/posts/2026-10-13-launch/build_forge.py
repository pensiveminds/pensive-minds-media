"""Marching Orders #1 (Proverbs 24:16) rebuilt in the Forge look for Wed Oct 14, 2026, 6:45 AM.

    python3 posts/2026-10-13-launch/build_forge.py

Same words as the launch still in make_posts.py. Scripture checked against BibleGateway (CSB) Oct 13, 2026.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from make_variants import mo_look, render_looks

SET = {"01_marching_orders_proverbs24-16_forge.jpg": mo_look("forge",
    ["YOU FELL.", "GET [UP]."],
    ["“Though a righteous person falls", "seven times, he will get up…”"],
    "Proverbs 24:16, CSB",
    sub=["Make the bed. Open the Book. Go to work."])}

if __name__ == "__main__":
    print("\n".join(render_looks(SET, HERE)))
