"""Build the queued Strike Reel for a date (used by the daily scheduled task).

    python3 build_queued_reel.py 2026-10-16          # builds, logs SOURCES/SONGS, marks it built
    python3 build_queued_reel.py 2026-10-16 --print  # prints the Metricool payload fields as JSON

Uses voice/queue/<date>.wav if present (already disguised with make_reel.voice_fx). Never invents verses:
every verse comes from REEL_QUEUE.json, which was scripted from VERSE_BANK.json (CSB, verified).
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
RAW = "https://raw.githubusercontent.com/pensiveminds/pensive-minds-media/main/heel-and-serpent/"


def entry(date):
    q = json.load(open(os.path.join(HERE, "REEL_QUEUE.json")))
    for r in q["reels"]:
        if r["date"] == date:
            return q, r
    raise SystemExit(f"No queued Reel for {date}. Write one into REEL_QUEUE.json from VERSE_BANK.json first.")


def payload(r):
    d = f"reels/{r['date']}-{r['slug']}/"; n = f"strike_{r['slug']}"
    return {"date": f"{r['date']}T{r['post_time']}:00-05:00", "media": RAW + d + n + ".mp4", "cover": RAW + d + n + "_cover.jpg",
            "text": r["caption"], "alt": r["alt"], "voice": r.get("voice_used", False)}


def build(date):
    from make_reel import Scene, build_reel
    q, r = entry(date)
    if r.get("built"):
        print("already built", r["built"]); return r
    scenes = []
    for sc in r["scenes"]:
        kind, secs, lines = sc[0], sc[1], sc[2]
        ref = sc[3] if len(sc) > 3 else None; sub = sc[4] if len(sc) > 4 else None
        scenes.append(Scene(kind, secs, lines, ref=ref, sub=sub))
    out = os.path.join(HERE, "reels", f"{r['date']}-{r['slug']}")
    voice = os.path.join(HERE, "voice", "queue", f"{date}.wav")
    voice = voice if os.path.exists(voice) else None
    build_reel(scenes, out, f"strike_{r['slug']}", fade=0.25, motion=True, voice=voice)
    open(os.path.join(out, "CAPTIONS.md"), "w").write(f"# Strike ({r['date']}): {r['slug']}\n\n{r['caption']}\n")
    # SOURCES.md: one row per verse use, running total updated
    p = os.path.join(HERE, "SOURCES.md"); s = open(p).read()
    add = 0
    for verse, ctx, n in r["sources"]:
        row = f"| {r['date']} Strike Reel ({r['slug']}) | {verse} | {ctx} | {n} |\n"
        s = s.replace("| Brand anchors (bible, not posts) |", row + "| Brand anchors (bible, not posts) |", 1); add += n
    m = re.search(r"\*\*Running total on posts: (\d+) verses\.\*\*", s)
    s = s.replace(m.group(0), f"**Running total on posts: {int(m.group(1)) + add} verses.**"); open(p, "w").write(s)
    p = os.path.join(HERE, "SONGS.md")
    open(p, "a").write(f"| {r['date']} 3:30 PM | Strike Reel ({r['slug']}) | Original score (built in){' + voice' if voice else ''} | Reels carry their own score |\n")
    r["built"] = date; r["voice_used"] = bool(voice)
    json.dump(q, open(os.path.join(HERE, "REEL_QUEUE.json"), "w"), ensure_ascii=False, indent=1)
    return r


if __name__ == "__main__":
    date = sys.argv[1]
    if "--print" in sys.argv:
        print(json.dumps(payload(entry(date)[1]), ensure_ascii=False))
    else:
        r = build(date); print(json.dumps(payload(r), ensure_ascii=False))
