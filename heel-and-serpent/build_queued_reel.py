"""Build the queued Strike Reel for a date.

    python3 build_queued_reel.py 2026-10-21          # builds, logs SOURCES/SONGS, marks it built, prints the payload
    python3 build_queued_reel.py 2026-10-21 --print  # prints the Metricool payload fields as JSON
    python3 build_queued_reel.py --next              # the earliest unbuilt date in the queue

Every Reel gets a new original score (score_engine.py; Chris, Oct 20, 2026): the style is never one of the last
three used, and the key and tempo are seeded by the slug. Pace comes from the entry: 'fast' keeps the scenes as
written (two-shot verse, motion, 0.25 s fades); 'slow' is the original Strike #1-2 style (longer holds, one verse
shot, 0.4 s fades, no motion). No voice. Never invents verses: every verse comes from REEL_QUEUE.json, which is
scripted from VERSE_BANK.json (CSB, verified).
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
RAW = "https://raw.githubusercontent.com/pensiveminds/pensive-minds-media/main/heel-and-serpent/"
QUEUE = os.path.join(HERE, "REEL_QUEUE.json")


def load():
    return json.load(open(QUEUE))


def entry(date):
    q = load()
    for r in q["reels"]:
        if r["date"] == date:
            return q, r
    raise SystemExit(f"No queued Reel for {date}. Script one into REEL_QUEUE.json from VERSE_BANK.json first.")


def payload(r):
    d = f"reels/{r['date']}-{r['slug']}/"; n = f"strike_{r['slug']}"
    return {"date": f"{r['date']}T{r['post_time']}:00", "timezone": "America/Chicago", "media": RAW + d + n + ".mp4",
            "cover": RAW + d + n + "_cover.jpg", "text": r["caption"], "alt": alt(r), "pace": r.get("pace", "fast"),
            "score": r.get("score")}


def alt(r):
    a = r["alt"]
    if r.get("pace") == "slow":
        a = a.replace("drifting embers and ", "").replace("with drifting embers ", "").replace(" in two shots", "")
    return a


def slow_scenes(raw):
    """Original style: hook 2.6 s, second line 2.4 s, the verse in one shot (5.8-6.4 s), the seal 3.2 s."""
    out, verse, ref = [], [], None
    bigs = 0
    for sc in raw:
        kind = sc[0]
        if kind == "verse":
            verse += sc[2]; ref = sc[3] if len(sc) > 3 and sc[3] else ref
            continue
        if verse:
            out.append(["verse", 5.8 if len(verse) <= 5 else 6.4, verse, ref]); verse = []
        if kind == "big":
            out.append(["big", 2.6 if bigs == 0 else 2.4, sc[2]]); bigs += 1
        elif kind == "seal":
            out.append(["seal", 3.2, sc[2], None, sc[4] if len(sc) > 4 else None])
    if verse:
        out.append(["verse", 6.0, verse, ref])
    return out


def build(date):
    from make_reel import Scene, build_reel
    from score_engine import creative_score, pick_score
    q, r = entry(date)
    if r.get("built"):
        print("already built", r["built"]); return r
    pace = r.get("pace", "fast")
    raw = slow_scenes(r["scenes"]) if pace == "slow" else r["scenes"]
    scenes = [Scene(sc[0], sc[1], sc[2], ref=sc[3] if len(sc) > 3 else None, sub=sc[4] if len(sc) > 4 else None) for sc in raw]
    used = [x["score"]["style"] for x in sorted(q["reels"], key=lambda x: x["date"]) if x.get("built") and x.get("score")]
    spec = r.get("score") or pick_score(r["slug"], used)
    cuts, t = [], 0.0
    for s in scenes:
        cuts.append(t); t += s.secs
    vi = next(i for i, s in enumerate(scenes) if s.kind == "verse")
    fn = lambda c, L: creative_score(c, L, verse_at=c[vi], **spec)
    out = os.path.join(HERE, "reels", f"{r['date']}-{r['slug']}")
    if pace == "slow":
        build_reel(scenes, out, f"strike_{r['slug']}", fade=0.4, motion=False, score_fn=fn)
    else:
        build_reel(scenes, out, f"strike_{r['slug']}", fade=0.25, motion=True, score_fn=fn)
    hhmm = r["post_time"]; h, m = map(int, hhmm.split(":")); when = f"{(h - 1) % 12 + 1}:{m:02d} {'AM' if h < 12 else 'PM'}"
    open(os.path.join(out, "CAPTIONS.md"), "w").write(
        f"# Strike ({r['date']}, {when} CT): {r['slug']}\n\nPace: {pace}. Score: {spec['style']}, {spec['key']}, {spec['bpm']} bpm (original, score_engine.py).\n\n"
        f"## Caption\n\n{r['caption']}\n\n## Alt text\n\n{alt(r)}\n")
    p = os.path.join(HERE, "SOURCES.md"); s = open(p).read(); add = 0
    for verse, ctx, n in r["sources"]:
        row = f"| {r['date']} Strike Reel ({r['slug']}) | {verse} | {ctx} | {n} |\n"
        s = s.replace("| Brand anchors (bible, not posts) |", row + "| Brand anchors (bible, not posts) |", 1); add += n
    m = re.search(r"\*\*Running total on posts: (\d+) verses\.\*\*", s)
    s = s.replace(m.group(0), f"**Running total on posts: {int(m.group(1)) + add} verses.**"); open(p, "w").write(s)
    with open(os.path.join(HERE, "SONGS.md"), "a") as f:
        f.write(f"| {r['date']} {when} | Strike Reel ({r['slug']}, {pace}) | Original score: {spec['style']}, {spec['key']}, {spec['bpm']} bpm (built in) | Reels carry their own score |\n")
    bank = os.path.join(HERE, "VERSE_BANK.json"); b = json.load(open(bank))
    for v in b["verses"]:
        if any(v["ref"] in src[0] for src in r["sources"]) and not v.get("used"):
            v["used"] = f"{r['date']} Strike Reel ({r['slug']})"
    json.dump(b, open(bank, "w"), ensure_ascii=False, indent=1)
    r["built"] = date; r["score"] = spec
    json.dump(q, open(QUEUE, "w"), ensure_ascii=False, indent=1)
    return r


if __name__ == "__main__":
    if sys.argv[1] == "--next":
        print(min((x["date"] for x in load()["reels"] if not x.get("built")), default="none")); sys.exit()
    date = sys.argv[1]
    if "--print" in sys.argv:
        print(json.dumps(payload(entry(date)[1]), ensure_ascii=False))
    else:
        r = build(date); print(json.dumps(payload(r), ensure_ascii=False))
