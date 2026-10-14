"""Story burst "Before you sleep", Tue Oct 13, 2026, about 8:15-8:28 PM, leading into the 8:30 Elijah post.

    python3 stories/2026-10-13-before-you-sleep/build.py

Scripture: Lamentations 3:22-23, CSB, checked verbatim against BibleGateway (CSB) on Oct 13, 2026. Logged in SOURCES.md.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from make_variants import story_look, render_story

FRAMES = {
    "01_before_you_sleep.jpg": story_look("classic", ["BEFORE YOU", "[SLEEP]."], body=["Three questions.", "Answer them honestly."], kicker="Night watch"),
    "02_q1_word.jpg": story_look("bone", ["Did you keep", "your [word]", "today?"], kicker="1 of 3"),
    "03_q2_present.jpg": story_look("ledger", ["Did the people", "at home get", "the [real] you?"], kicker="2 of 3"),
    "04_q3_tomorrow.jpg": story_look("bone", ["What’s one thing", "you’ll do [better]", "tomorrow?"], kicker="3 of 3"),
    "05_new_every_morning.jpg": story_look("forge", ["WHATEVER THE", "ANSWERS, GET", "[UP] TOMORROW."],
        verse_lines=["“…his mercies never end.", "They are new every morning;", "great is your faithfulness!”"],
        ref="Lamentations 3:22–23, CSB"),
    "06_on_the_feed.jpg": story_look("engraved", ["THE LIE:", "YOU’RE THE", "ONLY [ONE]."], body=["New on the feed at 8:30."], kicker="Tonight", seal=True),
}

if __name__ == "__main__":
    for name, (svg, kind) in FRAMES.items():
        render_story(svg, os.path.join(HERE, name), kind); print(name)
