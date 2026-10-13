"""Ranks & Reason, Campaign No. 1: Marathon. 1080x1920 @30fps, narrated, animated battle map, synthesized drum score."""
import json, math, subprocess, wave, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = pathlib.Path("/home/claude/rr/c001")
W, H, FPS = 1080, 1920, 30
SR = 44100
SERIF = "/home/claude/fonts/DMSerifDisplay-Regular.ttf"
SERIF_I = "/home/claude/fonts/DMSerifDisplay-Italic.ttf"
SANS = "/home/claude/fonts/DMSans-VF.ttf"
BG, BONE, BRASS, RED, SEA, MUTED = (17, 18, 20), (233, 228, 216), (196, 146, 66), (178, 52, 40), (22, 38, 44), (132, 128, 120)
rng = np.random.default_rng(1)

def sans(size, weight=700):
    f = ImageFont.truetype(SANS, size)
    try: f.set_variation_by_axes([weight if a.get("name") in (b"Weight", "Weight") else a["default"] for a in f.get_variation_axes()])
    except Exception: pass
    return f

# ---------------- timeline ----------------
beats = json.load(open(D / "beats.json"))
LEAD, GAP, TAIL = 0.7, 0.4, 2.2
t = LEAD
for b in beats:
    w = wave.open(str(D / f"vo/b{b['id']}.wav")); b["dur"] = w.getnframes() / w.getframerate(); b["vsr"] = w.getframerate()
    b["t0"] = t; b["t1"] = t + b["dur"]; t = b["t1"] + GAP
DUR = beats[-1]["t1"] + TAIL
N = int(DUR * FPS)
def beat_at(tt):
    cur = beats[0]
    for b in beats:
        if tt >= b["t0"] - 0.2: cur = b
    return cur
def prog(tt, b, a=0.0, z=1.0):  # progress within a sub-window of a beat (fractions of its duration)
    s, e = b["t0"] + a * b["dur"], b["t0"] + z * b["dur"]
    return float(np.clip((tt - s) / max(e - s, 1e-3), 0, 1))
def ease(x): return x * x * (3 - 2 * x)
def B(i): return beats[i - 1]

# ---------------- audio ----------------
def build_audio():
    n = int(DUR * SR); mix = np.zeros(n, np.float32)
    # narration
    for b in beats:
        w = wave.open(str(D / f"vo/b{b['id']}.wav")); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        x = np.interp(np.arange(0, len(x), b["vsr"] / SR), np.arange(len(x)), x)  # resample to 44.1k
        i0 = int(b["t0"] * SR); mix[i0:i0 + len(x)] += x[: n - i0] * 1.0
    voice = mix.copy()
    music = np.zeros(n, np.float32)
    def tom(at, f0=62, dur=0.9, amp=0.55, drop=0.45):
        i0 = int(at * SR); L = int(dur * SR); tt = np.arange(L) / SR
        f = f0 * (1 + drop * np.exp(-tt * 18)); ph = 2 * np.pi * np.cumsum(f) / SR
        s = np.sin(ph) * np.exp(-tt * 5.5) * amp
        s += rng.normal(0, 1, L).astype(np.float32) * np.exp(-tt * 60) * amp * 0.25
        e = min(n, i0 + L); music[i0:e] += s[: e - i0]
    def boom(at, amp=0.9):
        i0 = int(at * SR); L = int(2.6 * SR); tt = np.arange(L) / SR
        s = np.sin(2 * np.pi * 38 * tt * (1 + 0.6 * np.exp(-tt * 8))) * np.exp(-tt * 2.2) * amp
        noise = rng.normal(0, 1, L) * np.exp(-tt * 7) * amp * 0.35
        k = np.ones(60) / 60; noise = np.convolve(noise, k, "same")
        e = min(n, i0 + L); music[i0:e] += (s + noise)[: e - i0]
    # low drone under everything
    tt = np.arange(n) / SR
    drone = (np.sin(2 * np.pi * 41.2 * tt) + 0.6 * np.sin(2 * np.pi * 41.9 * tt) + 0.3 * np.sin(2 * np.pi * 82.4 * tt)) * 0.06
    swell = np.clip(tt / 3, 0, 1) * np.clip((DUR - tt) / 2, 0, 1)
    music += drone * swell
    # hits on each beat start
    for b in beats: tom(b["t0"] - 0.05, f0=58, amp=0.5)
    tom(B(1)["t0"] + 0.02, f0=48, amp=0.75, dur=1.4)
    # war drums build through beat 3 and the charge in beat 4
    t = B(3)["t0"] + B(3)["dur"] * 0.5; step = 0.48
    while t < B(4)["t1"]:
        tom(t, f0=70, amp=0.28 + 0.25 * (t - B(3)["t0"]) / (B(4)["t1"] - B(3)["t0"]), dur=0.5)
        t += step; step = max(0.16, step * 0.93)
    # trap slam
    boom(B(5)["t0"] + B(5)["dur"] * 0.42)
    boom(B(6)["t0"] - 0.05, amp=0.6)
    # silence then final hit
    tom(B(7)["t1"] - 0.9, f0=44, amp=0.9, dur=1.8)
    # duck music under voice
    env = np.abs(voice); k = int(0.08 * SR); env = np.convolve(env, np.ones(k) / k, "same")
    duck = 1 - 0.55 * np.clip(env * 12, 0, 1)
    out = voice * 1.0 + music * duck
    out = np.tanh(out * 1.1) * 0.92
    a = (np.clip(out, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(D / "mix.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.tobytes())

# ---------------- map ----------------
MX, MY, MW, MH = 40, 270, 1000, 900   # map viewport on screen
def make_terrain():
    a = np.full((MH, MW, 3), (30, 31, 33), np.float32)
    yy, xx = np.mgrid[0:MH, 0:MW].astype(np.float32)
    coast = 690 + 35 * np.sin(xx / 140) + 18 * np.sin(xx / 47 + 1)
    sea = yy > coast
    a[sea] = SEA
    hills = yy < 150 + 30 * np.sin(xx / 90)
    a[hills] = (38, 37, 34)
    img = Image.fromarray(a.astype(np.uint8)); d = ImageDraw.Draw(img)
    for k in range(5):  # contour lines in the hills
        pts = [(x, 30 + k * 26 + 22 * math.sin(x / 90 + k)) for x in range(0, MW + 10, 10)]
        d.line(pts, fill=(70, 62, 48), width=2)
    for k in range(9):  # waves
        y0 = 740 + k * 22
        for x0 in range(int(rng.uniform(-60, 0)), MW, 120):
            d.arc([x0, y0, x0 + 50, y0 + 14], 200, 340, fill=(48, 72, 80), width=2)
    coast_pts = [(x, 690 + 35 * math.sin(x / 140) + 18 * math.sin(x / 47 + 1)) for x in range(0, MW + 5, 5)]
    d.line(coast_pts, fill=(92, 110, 112), width=3)
    lf = sans(22, 600)
    d.text((24, 40), "MOUNTAINS", font=lf, fill=(110, 100, 82))
    d.text((24, 800), "BAY OF MARATHON", font=lf, fill=(80, 108, 112))
    d.text((24, 420), "PLAIN OF MARATHON", font=lf, fill=(80, 78, 74))
    return img
TERRAIN = make_terrain()

# unit layout in map coords
def greek_units(t):
    """Return list of (x, y, w, h, alpha) for Greek blocks given time."""
    p3 = ease(prog(t, B(3), 0.25, 0.85)) if t >= B(3)["t0"] else 0
    p4 = ease(prog(t, B(4), 0.15, 0.7)) if t >= B(4)["t0"] else 0
    p5a = ease(prog(t, B(5), 0.05, 0.4)) if t >= B(5)["t0"] else 0
    p5b = ease(prog(t, B(5), 0.42, 0.9)) if t >= B(5)["t0"] else 0
    y_line = 250 + 210 * p4 - 40 * p5a
    units = []
    cols = 15
    for c in range(cols):
        x = 140 + c * 52
        wing = 0 if c < 5 else (1 if c < 10 else 2)
        ranks = 2 + (2 * p3 if wing != 1 else -1 * p3)
        n_r = int(math.ceil(ranks))
        for r in range(n_r):
            a = min(1.0, ranks - r)
            yy = y_line - r * 30
            xx = x
            if wing == 1:   # center gives ground under the Persian push
                yy -= 70 * p5a
            else:           # wings swing in around the flanks
                side = -1 if wing == 0 else 1
                k = (abs(c - 7) - 2) / 5
                xx = x - side * 150 * p5b * (0.6 + 0.4 * k)
                yy = yy + 210 * p5b * (0.4 + 0.6 * k)
            units.append((xx, yy, 40, 22, a))
    return units

def persian_units(t):
    p2 = ease(prog(t, B(2), 0.05, 0.6)) if t >= B(2)["t0"] - 0.2 else 0
    p5a = ease(prog(t, B(5), 0.05, 0.4)) if t >= B(5)["t0"] else 0
    p6 = ease(prog(t, B(6), 0.0, 0.5)) if t >= B(6)["t0"] else 0
    units = []
    for c in range(16):
        x = 110 + c * 52
        center = 5 <= c <= 10
        for r in range(4):
            y = 560 + r * 30 + (1 - p2) * 420
            jitter = math.sin(c * 1.7 + r) * 4
            if center: y -= 150 * p5a
            a = p2 * (1 - 0.85 * p6) * (1 - (0.6 * p5a if not center else 0))
            # flanks rout toward the sea
            if not center and t >= B(5)["t0"]:
                y += 120 * ease(prog(t, B(5), 0.45, 1.0))
            units.append((x + jitter, y, 40, 22, a))
    return units

def arrows(t, d, ox, oy, z):
    if not (B(4)["t0"] < t < B(4)["t1"]): return
    p = prog(t, B(4), 0.1, 0.75)
    if p <= 0 or p >= 1: return
    rr = np.random.default_rng(int(t * 30))
    for _ in range(40):
        x = rr.uniform(140, 900); y0 = rr.uniform(300, 520)
        L = 26
        d.line([(ox + x * z, oy + y0 * z), (ox + (x - 6) * z, oy + (y0 - L) * z)], fill=(200, 190, 170), width=2)

def to_screen(x, y, z, cx, cy):
    return MX + (x - cx) * z + MW / 2, MY + (y - cy) * z + MH / 2

# ---------------- text helpers ----------------
def draw_center(d, text, font, y, fill, x=None):
    w = d.textlength(text, font=font); d.text(((W - w) / 2 if x is None else x, y), text, font=font, fill=fill)

def caption(img, t):
    b = None
    for bb in beats:
        if bb["t0"] - 0.1 <= t <= bb["t1"] + 0.3: b = bb
    if not b: return
    a = min(1, (t - (b["t0"] - 0.1)) / 0.25, (b["t1"] + 0.3 - t) / 0.25)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f = ImageFont.truetype(SERIF, 86)
    y = 1250
    lines = b["cap"]
    # reveal lines progressively across the beat
    for i, ln in enumerate(lines):
        if t < b["t0"] + b["dur"] * (i / len(lines)) * 0.9: break
        words = ln.split(" "); total = sum(d.textlength(w + " ", font=f) for w in words) - d.textlength(" ", font=f)
        x = (W - total) / 2
        for w_ in words:
            col = BRASS if b["hi"] in w_ else BONE
            d.text((x + 3, y + 4), w_, font=f, fill=(0, 0, 0, 160))
            d.text((x, y), w_, font=f, fill=col)
            x += d.textlength(w_ + " ", font=f)
        y += 100
    al = lay.getchannel("A").point(lambda v: int(v * a)); lay.putalpha(al)
    img.alpha_composite(lay)

GRAIN = [rng.normal(0, 9, (H, W, 1)).astype(np.float32) for _ in range(4)]
YY, XX = np.mgrid[0:H, 0:W]
VIG = (1 - 0.5 * np.clip(np.sqrt(((XX - W / 2) / (W / 2)) ** 2 + ((YY - H / 2) / (H / 2)) ** 2) / 1.42, 0, 1) ** 1.8)[..., None].astype(np.float32)

def frame(i):
    t = i / FPS
    img = Image.new("RGBA", (W, H), BG + (255,)); d = ImageDraw.Draw(img)
    # camera: slow push in, shake on impacts
    z = 1.0 + 0.10 * min(1, t / DUR * 1.4)
    cx, cy = MW / 2, MH / 2 + 30 * ease(prog(t, B(4), 0.1, 0.8)) if t >= B(4)["t0"] else MH / 2
    shake = 0
    for at, s in [(B(1)["t0"], 10), (B(5)["t0"] + B(5)["dur"] * 0.42, 22), (B(6)["t0"], 12)]:
        if at <= t < at + 0.5: shake = s * (1 - (t - at) / 0.5)
    sx, sy = (rng.normal(0, shake), rng.normal(0, shake)) if shake else (0, 0)
    map_alpha = ease(min(1, t / 0.9)) * (1 - 0.65 * ease(prog(t, B(7), 0.0, 0.25)) if t >= B(7)["t0"] else 1)
    # terrain (zoomed crop)
    cw, ch = MW / z, MH / z
    bx = min(max(cx - cw / 2, 0), MW - cw); by = min(max(cy - ch / 2, 0), MH - ch)
    crop = TERRAIN.resize((MW, MH), Image.BICUBIC, box=(bx, by, bx + cw, by + ch))
    m = Image.new("L", (MW, MH), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, MW - 1, MH - 1], 22, fill=int(255 * map_alpha))
    img.paste(crop, (int(MX + sx), int(MY + sy)), m)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    def rect(u, col):
        x, y, w, h, a = u
        if a <= 0.01: return
        X, Y = to_screen(x, y, z, cx, cy); X += sx; Y += sy
        if not (MY - 30 < Y < MY + MH): return
        ld.rectangle([X - w * z / 2, Y - h * z / 2, X + w * z / 2, Y + h * z / 2], fill=col + (int(255 * a * map_alpha),))
    if t >= B(2)["t0"] - 0.2:
        for u in persian_units(t): rect(u, RED)
    for u in greek_units(t):
        if t < 0.3: break
        rect(u, BONE)
    arrows(t, ld, MX - (cx - MW / 2) * z + sx, MY - (cy - MH / 2) * z + sy, z)
    # annotations
    lf = sans(30, 800)
    if B(3)["t0"] + B(3)["dur"] * 0.35 < t < B(4)["t0"] + 0.4:
        a = int(255 * map_alpha * min(1, (t - B(3)["t0"] - B(3)["dur"] * 0.35) / 0.3))
        X, Y = to_screen(470, 285, z, cx, cy); ld.text((X, Y), "THIN", font=lf, fill=BRASS + (a,))
        X, Y = to_screen(150, 92, z, cx, cy); ld.text((X, Y), "STACKED", font=lf, fill=BRASS + (a,))
        X, Y = to_screen(670, 92, z, cx, cy); ld.text((X, Y), "STACKED", font=lf, fill=BRASS + (a,))
    if B(4)["t0"] < t < B(4)["t0"] + B(4)["dur"] * 0.35:
        a = int(255 * map_alpha * min(1, (t - B(4)["t0"]) / 0.3))
        X1, Y1 = to_screen(940, 270, z, cx, cy); X2, Y2 = to_screen(940, 550, z, cx, cy)
        ld.line([(X1, Y1), (X2, Y2)], fill=BRASS + (a,), width=4)
        ld.line([(X1 - 14, Y1), (X1 + 14, Y1)], fill=BRASS + (a,), width=4); ld.line([(X2 - 14, Y2), (X2 + 14, Y2)], fill=BRASS + (a,), width=4)
        ld.text((X1 - 150, (Y1 + Y2) / 2 - 18), "≈1.4 KM", font=lf, fill=BRASS + (a,))
    if t >= B(1)["t0"] + 1.2 and t < B(3)["t0"]:
        a = int(255 * map_alpha * min(1, (t - B(1)["t0"] - 1.2) / 0.3))
        X, Y = to_screen(370, 185, z, cx, cy); ld.text((X, Y - 30), "ATHENS ~10,000", font=lf, fill=BONE + (a,))
    if t >= B(2)["t0"] + 1.2 and t < B(3)["t0"]:
        a = int(255 * map_alpha * min(1, (t - B(2)["t0"] - 1.2) / 0.3))
        X, Y = to_screen(440, 700, z, cx, cy); ld.text((X, Y), "PERSIA", font=lf, fill=RED + (a,))
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    # header
    d.text((60, 120), "CAMPAIGN No. 1", font=sans(30, 800), fill=BRASS)
    d.text((60, 162), "MARATHON · 490 BC", font=sans(30, 600), fill=MUTED)
    rw = d.textlength("RANKS & REASON", font=sans(26, 700)); d.text((W - 60 - rw, 126), "RANKS & REASON", font=sans(26, 700), fill=MUTED)
    # opening stamp
    if t < B(1)["t0"] + 1.6:
        a = ease(min(1, t / 0.25)) * (1 - ease(prog(t, B(1), 0.18, 0.32)))
        if a > 0:
            f = ImageFont.truetype(SERIF, int(300 - 60 * min(1, t / 0.4)))
            st = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
            draw_center(sd, "490 BC", f, 560, BONE + (int(255 * a),))
            img.alpha_composite(st)
    # casualty counters
    if t >= B(6)["t0"] and t < B(7)["t0"] + 0.6:
        p = ease(prog(t, B(6), 0.05, 0.45)); fade = 1 - ease(prog(t, B(7), 0.0, 0.12)) if t >= B(7)["t0"] else 1
        st = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        n1 = int(6400 * p); f = ImageFont.truetype(SERIF, 190)
        draw_center(sd, f"{n1:,}", f, 430, RED + (int(255 * fade),))
        draw_center(sd, "PERSIAN DEAD", sans(34, 800), 650, MUTED + (int(255 * fade),))
        p2 = ease(prog(t, B(6), 0.5, 0.8))
        if p2 > 0:
            draw_center(sd, f"{int(192 * p2)}", f, 760, BONE + (int(255 * fade),))
            draw_center(sd, "ATHENIAN DEAD", sans(34, 800), 980, MUTED + (int(255 * fade),))
            draw_center(sd, "per Herodotus", sans(26, 500), 1040, MUTED + (int(200 * fade),))
        # dim map behind numbers
        dim = Image.new("RGBA", (W, H), (10, 10, 12, int(228 * min(1, p * 3) * fade)))
        img.alpha_composite(dim); img.alpha_composite(st)
    # closer
    if t >= B(7)["t0"]:
        img.alpha_composite(Image.new("RGBA", (W, H), (10, 10, 12, int(225 * ease(prog(t, B(7), 0.0, 0.25))))))
        st = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        p = ease(prog(t, B(7), 0.25, 0.5)); q = ease(prog(t, B(7), 0.75, 0.95))
        draw_center(sd, "THE RUN THAT", sans(54, 800), 480, BONE + (int(255 * p),))
        draw_center(sd, "MATTERED", sans(54, 800), 548, BONE + (int(255 * p),))
        f = ImageFont.truetype(SERIF, 210)
        draw_center(sd, "150 mi", f, 640, BRASS + (int(255 * p),))
        draw_center(sd, "PART 2 →", sans(64, 800), 920, BONE + (int(255 * q),))
        if t > B(7)["t1"]:
            draw_center(sd, "Follow so you don't miss it.", sans(36, 500), 1010, MUTED + (int(255 * min(1, (t - B(7)["t1"]) / 0.4)),))
        img.alpha_composite(st)
    caption(img, t if t < B(7)["t0"] else -1)
    # flash on the trap
    at = B(5)["t0"] + B(5)["dur"] * 0.42
    if at <= t < at + 0.25:
        fl = Image.new("RGBA", (W, H), (255, 240, 220, int(110 * (1 - (t - at) / 0.25)))); img.alpha_composite(fl)
    out = np.asarray(img.convert("RGB")).astype(np.float32) * VIG + GRAIN[i % 4]
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))

if __name__ == "__main__":
    build_audio()
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", str(D / "mix.wav"), "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", "-movflags", "+faststart", str(D / "c001_marathon.mp4")], stdin=subprocess.PIPE)
    checks = {round(b["t0"] + b["dur"] * f, 1) for b in beats for f in (0.3, 0.8)}
    for i in range(N):
        fr = frame(i); enc.stdin.write(fr.tobytes())
        if round(i / FPS, 1) in checks and i % 3 == 0: fr.save(D / f"chk_{i/FPS:05.1f}.png")
    enc.stdin.close(); enc.wait()
    print("done", round(DUR, 2), "s")
