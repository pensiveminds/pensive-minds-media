"""Heel & Serpent Reel builder (Strike).

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
        size = 62
        v, end = text_block(scene.lines, 0, size, italic=True, weight=400, lead=1.32, max_w=760)
        r = text_block([scene.ref.upper()], end + 92, 26, family=SANS, weight=600, spacing=6, color=ASH)[0]
        parts = [v, r]
        top, bottom = -size * 0.72, end + 92
    else:  # seal
        parts.append(mark(SEAL, 340, -420, 400))
        size = 100
        t, end = text_block(scene.lines, 70, size, spacing=9, lead=1.14, max_w=720); parts.append(t)
        h = text_block([HANDLE.upper()], end + 110, 26, family=SANS, weight=600, spacing=6, color=ASH)[0]
        parts.append(h)
        top, bottom = -420, end + 110
    shift = MID - (top + bottom) / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<g transform="translate(0,{shift:.0f})">{"".join(parts)}</g></svg>')


def _layer(scene):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=_svg(scene).encode(), output_width=W))).convert("RGBA")


def _grounds(n=3):
    """Grained, vignetted iron grounds. The Reel holds one still: moving grain bloats the file for little gain."""
    out = []
    v = Image.new("L", (W, H), 0)
    ImageDraw.Draw(v).ellipse((-W * 0.3, -H * 0.15, W * 1.3, H * 1.15), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(W / 5))
    for i in range(n):
        a = np.full((H, W, 3), 26, "int16") + np.random.default_rng(7 + i).normal(0, 7, (H, W))[..., None]
        base = Image.fromarray(a.clip(0, 255).astype("uint8"))
        out.append(Image.composite(base, Image.new("RGB", (W, H), "#0d0d0d"), v))
    return out


# ---------------------------------------------------------------- score

def _env(n, a, r):
    e = np.ones(n)
    a, r = int(a * SR), int(r * SR)
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


def score(cuts, length, seed=11):
    """cuts: scene start times. Last scene is the resolve. Returns stereo int16 array."""
    total = int(length * SR)
    rng = np.random.default_rng(seed)
    chans = []
    for ch, det in enumerate((-0.0015, 0.0015)):
        x = np.zeros(total)
        verse_at, seal_at = cuts[-2], cuts[-1]
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
        for c in cuts[:-2]:
            x += _boom(c + 0.02, total, 0.55)
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


# ---------------------------------------------------------------- build

def build_reel(scenes, out_dir, name, fade=0.4):
    os.makedirs(out_dir, exist_ok=True)
    layers = [_layer(s) for s in scenes]
    grounds = _grounds()
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
            a = min(1.0, local / fade)
            if k < len(scenes) - 1:
                a = min(a, (dur - local) / fade)
            a = max(0.0, min(1.0, a))
            frame = grounds[0].copy()
            lay = layers[k]
            if a < 1:
                lay = lay.copy(); lay.putalpha(lay.getchannel("A").point(lambda p: int(p * a)))
            frame.paste(lay, (0, 0), lay)
            frame.save(os.path.join(tmp, f"f{f:04d}.jpg"), quality=92)
        audio = score(cuts, length)
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
