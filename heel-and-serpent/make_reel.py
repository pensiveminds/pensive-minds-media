"""Heel & Serpent Reel builder (Strike).

Pacing (from day-1 data, Oct 14, 2026: avg watch ~4 s on 16 s Reels): hook line fully on at frame 0, 1.5-1.8 s per
line, verse landing by ~5 s, 10-12 s total, fade=0.25.

A Reel is a list of scenes, each shown for a set time with soft fades, over the grained iron ground.
The score is original, synthesized here, and timed to the scene cuts: a low drone in D minor,
a heartbeat pulse, impacts on each cut, a swell into the verse and a resolve to D major on the seal.

    from make_reel import Scene, build_reel
    build_reel(scenes, out_dir, name)

All type sits inside y 300-1450 and x 110-970 so Instagram's Reels UI never covers it.
"""
import io, os, re, subprocess, sys, tempfile, wave
import numpy as np
import cairosvg
from PIL import Image, ImageDraw, ImageFilter
from scipy.signal import butter, sosfilt, fftconvolve

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make_posts import text_block, mark, SEAL, CROSS, HANDLE, SANS, SERIF, ASH, EMBER, BONE, rule

W, H, FPS, SR = 1080, 1920, 30, 44100
MID = 875  # visual centre of the safe zone


class Scene:
    """kind: 'big' (spaced capitals), 'verse' (italic Scripture + reference) or 'seal' (closing line + seal)."""
    def __init__(self, kind, secs, lines, ref=None, sub=None):
        self.kind, self.secs, self.lines, self.ref, self.sub = kind, secs, lines, ref, sub


def _svg(scene):
    parts = []
    if scene.kind == "big":
        size = 112
        t, end = text_block(scene.lines, 0, size, spacing=10, lead=1.14, max_w=740)
        parts.append(t); top, bottom = -size * 0.72, end
        if scene.sub:
            s_, end = text_block(scene.sub, end + 90, 44, weight=400, color=ASH, max_w=840); parts.append(s_); bottom = end
    elif scene.kind == "verse":
        size = 72 if len(scene.lines) <= 3 else 62   # two-shot verses carry fewer words, so set them larger
        v, end = text_block(scene.lines, 0, size, italic=True, weight=400, lead=1.32, max_w=760)
        parts = [v]; bottom = end
        if scene.ref:   # a verse split across two shots shows its reference on the last shot
            r = text_block([scene.ref.upper()], end + 92, 26, family=SANS, weight=600, spacing=6, color=ASH)[0]
            parts.append(r); bottom = end + 92
        top = -size * 0.72
    else:  # seal
        parts.append(mark(SEAL, 340, -420, 400))
        size = 100
        t, end = text_block(scene.lines, 70, size, spacing=9, lead=1.14, max_w=720); parts.append(t)
        if scene.sub:   # on-screen call to action, e.g. "Send this to a brother."
            c_, end = text_block(scene.sub, end + 96, 46, weight=400, color=BONE, max_w=760); parts.append(c_)
        h = text_block([HANDLE.upper()], end + 110, 26, family=SANS, weight=600, spacing=6, color=ASH)[0]
        parts.append(h)
        top, bottom = -420, end + 110
    shift = MID - (top + bottom) / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<g transform="translate(0,{shift:.0f})">{"".join(parts)}</g></svg>')


# One-off palettes (Chris asks for these by name; the brand palette stays the default).
# ground/edge: the vignetted ground; text/accent/label replace bone/ember/ash; glow: optional low light.
PALETTE = None
PALETTES = {
    "dawn": dict(ground=(29, 36, 51), edge="#0E121B", text="#EDE6D8", accent="#D4A55A",
                 label="#8C95A6", glow=(205, 150, 82), glow_strength=0.34),
}


def use_palette(name=None):
    """use_palette('dawn') for a one-off set; use_palette() to return to the brand palette."""
    global PALETTE
    PALETTE = PALETTES[name] if name else None


def _recolor(svg):
    if not PALETTE:
        return svg
    g = "#%02X%02X%02X" % PALETTE["ground"]
    for old, new in ((BONE, "@T@"), (EMBER, "@A@"), (ASH, "@L@"), ("#1A1A1A", "@G@")):
        svg = svg.replace(old, new).replace(old.lower(), new)
    return svg.replace("@T@", PALETTE["text"]).replace("@A@", PALETTE["accent"]).replace("@L@", PALETTE["label"]).replace("@G@", g)


def _layer(scene):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=_recolor(_svg(scene)).encode(), output_width=W))).convert("RGBA")


def _grounds(n=3):
    """Grained, vignetted iron grounds. The Reel holds one still: moving grain bloats the file for little gain."""
    out = []
    v = Image.new("L", (W, H), 0)
    ImageDraw.Draw(v).ellipse((-W * 0.3, -H * 0.15, W * 1.3, H * 1.15), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(W / 5))
    gr = PALETTE["ground"] if PALETTE else (26, 26, 26)
    edge = PALETTE["edge"] if PALETTE else "#0d0d0d"
    for i in range(n):
        a = np.array(gr, "int16")[None, None, :] + np.random.default_rng(7 + i).normal(0, 7, (H, W))[..., None]
        base = Image.fromarray(a.clip(0, 255).astype("uint8"))
        img = Image.composite(base, Image.new("RGB", (W, H), edge), v)
        if PALETTE and PALETTE.get("glow"):   # low first-light glow, laid over the vignette so it stays warm
            b = np.asarray(img).astype("float32")
            yy = np.linspace(0, 1, H)[:, None, None]
            xx = np.linspace(-1, 1, W)[None, :, None]
            g = np.exp(-((1.0 - yy) / 0.30) ** 2) * np.exp(-(xx / 1.1) ** 2) * PALETTE["glow_strength"]
            b = b + g * (np.array(PALETTE["glow"], "float32")[None, None, :] - b)
            img = Image.fromarray(b.clip(0, 255).astype("uint8"))
        out.append(img)
    return out


# ---------------------------------------------------------------- score

def _env(n, a, r):
    e = np.ones(n)
    a, r = min(int(a * SR), n // 2), min(int(r * SR), n // 2)
    if a: e[:a] = np.linspace(0, 1, a)
    if r: e[-r:] *= np.linspace(1, 0, r)
    return e


def _lp(x, hz, order=2):
    return sosfilt(butter(order, hz, "low", fs=SR, output="sos"), x)


def _boom(t0, total, gain=1.0):
    n = int(2.2 * SR); t = np.arange(n) / SR
    f = 38 + 52 * np.exp(-t * 9)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.1)
    nz = _lp(np.random.default_rng(int(t0 * 100)).normal(0, 1, n), 900) * np.exp(-t * 9) * 0.35
    out = np.zeros(total); i = int(t0 * SR); seg = (s + nz) * gain
    out[i:i + n] += seg[:max(0, total - i)]
    return out


def _pad(freqs, start, end, total, gain, a=1.2, r=1.2, detune=0.0):
    out = np.zeros(total); i0, i1 = int(start * SR), min(total, int(end * SR)); n = i1 - i0
    t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * (1 + detune) * t) + 0.3 * np.sin(2 * np.pi * 2 * f * (1 + detune) * t + 0.7)
            for f in freqs) / len(freqs)
    trem = 1 + 0.08 * np.sin(2 * np.pi * 0.21 * t)
    out[i0:i1] = s * trem * _env(n, a, r) * gain
    return out


def score(cuts, length, seed=11, verse_at=None):
    """cuts: scene start times. Last scene is the resolve. verse_at: when the (first) verse shot starts
    (defaults to the second-to-last cut). Returns stereo int16 array."""
    total = int(length * SR)
    rng = np.random.default_rng(seed)
    chans = []
    for ch, det in enumerate((-0.0015, 0.0015)):
        x = np.zeros(total)
        seal_at = cuts[-1]
        verse_at = cuts[-2] if verse_at is None else verse_at
        # drone: D minor until the seal, then D major (the Picardy third: the turn from down to up)
        x += _pad([73.42, 110.0], 0, length, total, 0.30, a=1.5, r=1.6, detune=det)
        x += _pad([174.61], 0.6, seal_at + 0.3, total, 0.10, a=1.5, r=0.6, detune=det)
        x += _pad([146.83, 185.0, 220.0, 293.66], seal_at - 0.2, length, total, 0.16, a=0.8, r=1.6, detune=det)
        # heartbeat under the opening lines, fading as the verse arrives
        t = 0.35
        while t < verse_at + 1.5:
            g = 0.55 if t < verse_at else 0.55 * max(0, 1 - (t - verse_at) / 1.5)
            for off, gg in ((0, 1.0), (0.17, 0.6)):
                n = int(0.35 * SR); tt = np.arange(n) / SR
                beat = np.sin(2 * np.pi * 52 * tt) * np.exp(-tt * 14) * g * gg
                i = int((t + off) * SR); x[i:i + n] += beat[:max(0, total - i)]
            t += 1.25
        # impacts on the opening cuts and on the seal
        for c in cuts[:-1]:
            if c < verse_at:
                x += _boom(c + 0.02, total, 0.55)
            elif c > verse_at:
                x += _boom(c + 0.02, total, 0.25)   # a light hit on the second verse shot
        x += _boom(seal_at + 0.02, total, 0.75)
        # riser into the verse: filtered noise swelling for 1.6 s
        n = int(1.6 * SR); i = int((verse_at - 1.6) * SR)
        sw = _lp(rng.normal(0, 1, n), 2400) * np.linspace(0, 1, n) ** 2.2 * 0.22
        x[i:i + n] += sw
        # high shimmer under the verse
        x += _pad([587.33, 880.0], verse_at, seal_at + 0.4, total, 0.035, a=1.0, r=0.8, detune=det)
        chans.append(x)
    st = np.stack(chans, 1)
    # room: a short dark reverb
    ir_n = int(2.4 * SR); ir_t = np.arange(ir_n) / SR
    ir = _lp(rng.normal(0, 1, ir_n), 3000) * np.exp(-ir_t * 2.6); ir /= np.abs(ir).sum() / 6
    wet = np.stack([fftconvolve(st[:, c], ir)[:total] for c in range(2)], 1)
    mix = st * 0.78 + wet * 0.32
    mix *= _env(total, 0.05, 1.4)[:, None]
    mix /= np.abs(mix).max() / 0.89  # peak about -1 dBFS
    return (mix * 32767).astype("int16")


def score_drive(cuts, length, seed=21, bpm=104):
    """Motivational, dramatic score for Stories: D major, a driving eighth-note pulse, drum hits on the beat,
    a lift into every cut and a big resolve on the last scene. Bright, not moody. Returns stereo int16."""
    total = int(length * SR); rng = np.random.default_rng(seed)
    beat = 60.0 / bpm
    prog = [[73.42, 146.83, 185.0, 220.0], [61.74, 123.47, 146.83, 185.0],   # D, Bm
            [49.0, 98.0, 123.47, 146.83], [55.0, 110.0, 138.59, 164.81]]      # G, A
    chans = []
    for det in (-0.0012, 0.0012):
        x = np.zeros(total)
        # chord pads, one chord per two beats, cycling I-vi-IV-V; last scene holds D major with the octave
        t = 0.0; i = 0; last = cuts[-1]
        while t < last:
            end = min(last, t + 2 * beat)
            x += _pad(prog[i % 4][1:], t, end + 0.25, total, 0.11, a=0.25, r=0.35, detune=det)
            x += _pad([prog[i % 4][0]], t, end + 0.25, total, 0.16, a=0.1, r=0.35, detune=det)
            t = end; i += 1
        x += _pad([73.42, 146.83, 185.0, 220.0, 293.66, 440.0], last - 0.05, length, total, 0.17, a=0.3, r=1.4, detune=det)
        # driving eighth-note pulse on the chord root, an octave up, plucked
        n8 = int(beat / 2 * SR); tt = np.arange(n8) / SR
        k = 0; t = 0.0
        while t < last:
            root = prog[int(t // (2 * beat)) % 4][1]
            pl = (np.sin(2 * np.pi * root * tt) + 0.4 * np.sin(2 * np.pi * 2 * root * tt)) * np.exp(-tt * 18) * 0.18
            i0 = int(t * SR); x[i0:i0 + n8] += pl[:max(0, total - i0)]
            t += beat / 2; k += 1
        # drums: low hit on beats 1 and 3, a snappier hit on 2 and 4
        t = 0.0; b = 0
        while t < last:
            if b % 2 == 0:
                x += _boom(t, total, 0.32)
            else:
                nn = int(0.25 * SR); tn = np.arange(nn) / SR
                sn = _lp(rng.normal(0, 1, nn), 5000) * np.exp(-tn * 22) * 0.16
                i0 = int(t * SR); x[i0:i0 + nn] += sn[:max(0, total - i0)]
            t += beat; b += 1
        # lift into each cut, impact on each cut, biggest on the last
        for c in cuts[1:]:
            n = int(1.0 * SR); i0 = int((c - 1.0) * SR)
            if i0 > 0:
                x[i0:i0 + n] += _lp(rng.normal(0, 1, n), 6000) * np.linspace(0, 1, n) ** 2.5 * 0.16
            x += _boom(c + 0.01, total, 0.5 if c != last else 0.8)
        # a high shimmer over the final resolve
        x += _pad([880.0, 1174.66], last, length, total, 0.03, a=0.6, r=1.0, detune=det)
        chans.append(x)
    st = np.stack(chans, 1)
    ir_n = int(1.6 * SR); ir_t = np.arange(ir_n) / SR
    ir = _lp(rng.normal(0, 1, ir_n), 6000) * np.exp(-ir_t * 3.5); ir /= np.abs(ir).sum() / 5
    wet = np.stack([fftconvolve(st[:, c], ir)[:total] for c in range(2)], 1)
    mix = st * 0.85 + wet * 0.22
    mix *= _env(total, 0.03, 1.0)[:, None]
    mix /= np.abs(mix).max() / 0.89
    return (mix * 32767).astype("int16")


# ---------------------------------------------------------------- motion and voice

def _punch(lay, s):
    """Scale a full-frame layer about its centre (s > 1 zooms in), cropped back to the frame."""
    if s <= 1.001:
        return lay
    w, h = int(W * s), int(H * s)
    big = lay.resize((w, h), Image.BILINEAR)
    x, y = (w - W) // 2, (h - H) // 2
    return big.crop((x, y, x + W, y + H))


def _embers(n=42, seed=5):
    rng = np.random.default_rng(seed)
    return [dict(x=rng.uniform(90, 990), y=rng.uniform(900, 2100), v=rng.uniform(60, 140), r=rng.uniform(2.6, 6.0),
                 sway=rng.uniform(8, 26), ph=rng.uniform(0, 6.28), a=rng.uniform(110, 210)) for _ in range(n)]


def _draw_embers(frame, parts, t):
    """Faint ember sparks drifting up from the bottom, behind the type."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    col = PALETTE["accent"] if PALETTE else EMBER
    rgb = tuple(int(col.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    for p in parts:
        y = (p["y"] - p["v"] * t) % 2100 - 100
        x = p["x"] + p["sway"] * np.sin(t * 1.3 + p["ph"])
        fade = max(0.0, min(1.0, (y - 250) / 900))          # die out as they rise
        a = int(p["a"] * fade)
        if a > 4:
            d.ellipse((x - p["r"], y - p["r"], x + p["r"], y + p["r"]), fill=rgb + (a,))
    frame.paste(ov, (0, 0), ov)


def voice_fx(src, dst, semitones=-2.5, formant=True):
    """Disguise a voice memo: pitch shift (formants shifted with it, so the timbre changes, not just the pitch),
    clean up rumble and hiss, warm it slightly, add a short room and even out the level.
    Writes a 44.1 kHz stereo WAV. It lowers recognisability; it does not make a voice anonymous."""
    ratio = 2 ** (semitones / 12)
    af = (f"highpass=f=80,lowpass=f=9000,rubberband=pitch={ratio:.5f}" + (":formant=shifted" if formant else ":formant=preserved") +
          ",equalizer=f=180:t=q:w=1:g=2,equalizer=f=3200:t=q:w=1.2:g=-2,aecho=0.8:0.5:35:0.12,"
          "loudnorm=I=-16:TP=-1.5:LRA=7")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", af, "-ar", str(SR), "-ac", "2", dst], check=True)
    return dst


def _mix_voice(audio, voice_wav, at=0.0, duck=0.35):
    """Lay a processed voice over the score, ducking the score under the voice."""
    with wave.open(voice_wav) as w:
        v = np.frombuffer(w.readframes(w.getnframes()), "int16").reshape(-1, 2).astype("float32")
    a = audio.astype("float32"); i = int(at * SR)
    v = v[:max(0, len(a) - i)]
    env = np.abs(v).mean(1); env = np.convolve(env, np.ones(4410) / 4410, "same"); env = np.clip(env / (env.max() + 1e-9) * 4, 0, 1)
    gain = 1 - (1 - duck) * env
    a[i:i + len(v)] *= gain[:, None]
    a[i:i + len(v)] += v * 0.95
    a /= max(1.0, np.abs(a).max() / (0.89 * 32767))
    return a.astype("int16")


# ---------------------------------------------------------------- build

def build_reel(scenes, out_dir, name, fade=0.4, score_fn=None, audio=None, motion=False, voice=None, voice_at=0.0):
    """audio: a ready stereo int16 array for this clip (used by build_story_set); otherwise score_fn makes one.
    motion: punch-in on each scene, drifting embers, a harder stamp on the seal (Buzzfy feedback, Oct 15, 2026).
    voice: a processed voice WAV (see voice_fx) mixed over the score from voice_at seconds, score ducked under it."""
    os.makedirs(out_dir, exist_ok=True)
    layers = [_layer(s) for s in scenes]
    grounds = _grounds()
    parts = _embers() if motion else None
    cuts, t = [], 0.0
    for s in scenes:
        cuts.append(t); t += s.secs
    length = t
    with tempfile.TemporaryDirectory() as tmp:
        nframes = int(round(length * FPS))
        for f in range(nframes):
            tt = f / FPS
            k = max(i for i, c in enumerate(cuts) if c <= tt)
            local, dur = tt - cuts[k], scenes[k].secs
            a = 1.0 if k == 0 else min(1.0, local / fade)   # hook: first scene is fully on from frame 0
            if k < len(scenes) - 1:
                a = min(a, (dur - local) / fade)
            a = max(0.0, min(1.0, a))
            frame = grounds[0].copy()
            lay = layers[k]
            if motion:
                _draw_embers(frame, parts, tt)
                amt = 0.12 if scenes[k].kind == "seal" else 0.05
                lay = _punch(lay, 1 + amt * max(0.0, 1 - local / 0.35) ** 2)
            if a < 1:
                lay = lay.copy(); lay.putalpha(lay.getchannel("A").point(lambda p: int(p * a)))
            frame.paste(lay, (0, 0), lay)
            frame.save(os.path.join(tmp, f"f{f:04d}.jpg"), quality=92)
        if audio is None:
            if score_fn is None:
                vi = next((i for i, sc in enumerate(scenes) if sc.kind == "verse"), len(scenes) - 2)
                audio = score(cuts, length, verse_at=cuts[vi])
            else:
                audio = score_fn(cuts, length)
        if voice:
            audio = _mix_voice(audio, voice, voice_at)
        wav = os.path.join(tmp, "score.wav")
        with wave.open(wav, "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(audio.tobytes())
        mp4 = os.path.join(out_dir, name + ".mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%04d.jpg"),
                        "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "slow", "-maxrate", "8M", "-bufsize", "16M",
                        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", mp4], check=True)
        import shutil
        shutil.copy(wav, os.path.join(out_dir, name + "_score.wav"))
    # cover: the first scene at full strength
    cover = grounds[0].copy(); cover.paste(layers[0], (0, 0), layers[0])
    cover.save(os.path.join(out_dir, name + "_cover.jpg"), quality=94)
    return mp4, cuts, length


def build_story_set(stories, out_dir, score_fn=None, edge=0.012):
    """Build a multi-frame Story with ONE continuous score.

    stories: ordered dict {frame_name: [Scene, ...]} in posting order. The score is written once for the
    whole set (one intro, lifts on every cut across all frames, one resolve on the last frame), then sliced
    so frame 2 picks up exactly where frame 1 left off. Instagram plays the frames back to back, so the music
    carries across the taps instead of restarting on each frame. Each slice gets a few ms of fade at its
    edges to avoid clicks. Returns [(name, mp4, start, end)]."""
    score_fn = score_fn or score_drive
    names = list(stories)
    cuts, starts, t = [], [], 0.0
    for n in names:
        starts.append(t)
        for sc in stories[n]:
            cuts.append(t); t += sc.secs
    length = t
    full = score_fn(cuts, length).astype("float32")
    e = int(edge * SR); ramp = np.linspace(0, 1, e, dtype="float32")[:, None]
    out = []
    for k, n in enumerate(names):
        a = starts[k]; b = starts[k + 1] if k + 1 < len(names) else length
        seg = full[int(round(a * SR)):int(round(b * SR))].copy()
        if k > 0:
            seg[:e] *= ramp
        if k < len(names) - 1:
            seg[-e:] *= ramp[::-1]
        mp4, _, _ = build_reel(stories[n], out_dir, n, audio=seg.astype("int16"))
        out.append((n, mp4, a, b))
    with wave.open(os.path.join(out_dir, "_set_score.wav"), "wb") as w:   # the whole score, for reference
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(full.astype("int16").tobytes())
    return out
