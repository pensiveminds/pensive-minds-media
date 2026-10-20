"""Heel & Serpent: a new original score for every Reel (Chris, Oct 20, 2026: "a creative score each time").

    from score_engine import creative_score, pick_score
    spec = pick_score(slug, used)            # style, key, mode, tempo, seed; avoids the last styles used
    audio = creative_score(cuts, length, verse_at, **spec)

Six styles, each with its own instruments and arc. Every one opens with a hit on frame 0 (the hook),
builds through the opening lines, lifts into the verse and resolves to a major chord on the seal:

  anthem    piano eighth-note ostinato, strings, kick building, crash on the seal. Motivational.
  hymn      choir and organ chords, timpani swells, solemn; minor turning major on the seal.
  march     snare cadence, taiko, low brass stabs; minor to major. A warrior's walk.
  dawn      plucked arpeggio and warm pad; bright and rising, like first light.
  pulse     staccato string ostinato in sixteenths, heartbeat kick, risers; cinematic drive.
  nocturne  solo piano melody over a cello drone; calm and close, like Strike #2 (Psalm 4:8).

Everything is synthesized here: no samples and no outside audio, so every score is ours.
"""
import hashlib
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100
STYLES = ["anthem", "hymn", "march", "dawn", "pulse", "nocturne"]
TEMPO = {"anthem": (86, 98), "hymn": (60, 70), "march": (100, 112), "dawn": (72, 84), "pulse": (118, 130), "nocturne": (64, 74)}
KEYS = {"C": 130.81, "D": 146.83, "Eb": 155.56, "E": 164.81, "F": 174.61, "G": 98.00, "A": 110.00, "Bb": 116.54}
MAJOR = [0, 2, 4, 5, 7, 9, 11]
MINOR = [0, 2, 3, 5, 7, 8, 10]


# ------------------------------------------------------------------ helpers

def _env(n, a, r):
    e = np.ones(n)
    a, r = min(int(a * SR), n // 2), min(int(r * SR), n // 2)
    if a: e[:a] = np.linspace(0, 1, a)
    if r: e[-r:] *= np.linspace(1, 0, r)
    return e


def _filt(x, hz, kind="low", order=2):
    return sosfilt(butter(order, hz, kind, fs=SR, output="sos"), x)


def _bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def _add(buf, seg, t0, pan=0.0, gain=1.0):
    """Mix a mono segment into a stereo buffer at t0 with constant-power pan (-1 left, +1 right)."""
    i = int(t0 * SR)
    if i >= len(buf) or i + len(seg) <= 0:
        return
    if i < 0:
        seg, i = seg[-i:], 0
    seg = seg[:len(buf) - i] * gain
    th = (pan + 1) * np.pi / 4
    buf[i:i + len(seg), 0] += seg * np.cos(th)
    buf[i:i + len(seg), 1] += seg * np.sin(th)


def _hz(root, semis):
    return root * 2 ** (semis / 12)


def _chord(root, mode, deg, octave=0, size=3, major_override=False):
    """Triad (or 7th with size=4) on scale degree deg (0-based) of the key."""
    sc = MAJOR if (mode == "major" or major_override) else MINOR
    out = []
    for k in range(size):
        idx = deg + 2 * k
        semis = sc[idx % 7] + 12 * (idx // 7) + 12 * octave
        out.append(_hz(root, semis))
    return out


# ------------------------------------------------------------------ instruments (mono, numpy)

def piano(f, dur, vel=1.0):
    n = int((dur + 1.2) * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for k in range(1, 9):
        fk = f * k * (1 + 0.00035 * k * k)
        if fk > SR / 2.2: break
        s += (0.62 ** (k - 1)) * np.sin(2 * np.pi * fk * t) * np.exp(-t * (1.1 + 0.55 * k) * (f / 260) ** 0.3)
    s += 0.04 * np.sin(2 * np.pi * f * 9.1 * t) * np.exp(-t * 70)            # hammer
    damp = np.ones(n); d0 = int(dur * SR); damp[d0:] = np.exp(-np.arange(n - d0) / SR * 7)
    return s * damp * _env(n, 0.003, 0.05) * vel * 0.32


def pluck(f, dur, vel=1.0, bright=0.5, seed=0):
    """Karplus-Strong, computed one period at a time."""
    n = int((dur + 0.8) * SR); P = max(2, int(SR / f))
    rng = np.random.default_rng(seed + int(f))
    y = np.zeros(n + P + 1)
    y[:P] = _filt(rng.uniform(-1, 1, P + 64), 1500 + 6000 * bright)[64:64 + P] if P > 8 else rng.uniform(-1, 1, P)
    dec = 0.996 if f < 300 else 0.993
    i = P
    while i < n:
        j = min(n, i + P)
        y[i:j] = dec * 0.5 * (y[i - P:j - P] + y[i - P - 1:j - P - 1] if i - P - 1 >= 0 else y[i - P:j - P] * 2)
        i = j
    s = y[:n]
    s *= _env(n, 0.001, 0.3)
    return s / (np.abs(s).max() + 1e-9) * vel * 0.30


def strings(f, dur, vel=1.0, a=0.35, r=0.6, vib=5.2, bright=3200, seed=0):
    n = int((dur + r) * SR); t = np.arange(n) / SR
    rng = np.random.default_rng(seed + int(f * 10))
    s = np.zeros(n)
    for v, det in enumerate((-0.004, 0.0, 0.0045)):                         # a small section, not one player
        ph = rng.uniform(0, 6.28); vibr = 1 + 0.0028 * np.sin(2 * np.pi * (vib + 0.3 * v) * t + ph) * np.clip(t / 0.5, 0, 1)
        inst = np.cumsum(f * (1 + det) * vibr) / SR
        for k in range(1, 14):
            if f * k > SR / 2.2: break
            s += np.sin(2 * np.pi * k * inst + ph * k) / k
    s = _filt(s, bright)
    return s * _env(n, a, r) * vel * 0.055


def staccato(f, dur, vel=1.0):
    return strings(f, dur, vel, a=0.008, r=0.06, vib=0.01, bright=4200) * 1.5


def brass(f, dur, vel=1.0, a=0.06, r=0.35):
    """Additive, with the upper harmonics swelling in after the lower ones: the 'blat' of low brass."""
    n = int((dur + r) * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for k in range(1, 16):
        if f * k > SR / 2.2: break
        bloom = np.clip((t - 0.012 * k) / (0.05 + 0.02 * k), 0, 1)
        s += np.sin(2 * np.pi * f * k * t) / k ** 0.9 * bloom
    s = _filt(s, 2600)
    return s * _env(n, a, r) * vel * 0.07


def choir(f, dur, vel=1.0, a=0.5, r=0.9, seed=0):
    """'Ah': detuned voices through two vowel formants."""
    n = int((dur + r) * SR); t = np.arange(n) / SR
    rng = np.random.default_rng(seed + int(f * 7))
    s = np.zeros(n)
    for det in (-0.006, -0.002, 0.003, 0.007):
        ph = rng.uniform(0, 6.28)
        vib = 1 + 0.003 * np.sin(2 * np.pi * rng.uniform(4.6, 5.6) * t + ph)
        inst = np.cumsum(f * (1 + det) * vib) / SR
        for k in range(1, 18):
            if f * k > SR / 2.2: break
            s += np.sin(2 * np.pi * k * inst + ph) / k
    s = 0.7 * _bp(s, 600, 900) + 0.45 * _bp(s, 1050, 1350) + 0.2 * _filt(s, 400)
    return s * _env(n, a, r) * vel * 0.10


def organ(f, dur, vel=1.0, a=0.08, r=0.5):
    n = int((dur + r) * SR); t = np.arange(n) / SR
    s = sum(w * np.sin(2 * np.pi * f * m * t) for m, w in ((0.5, 0.5), (1, 1.0), (2, 0.55), (3, 0.25), (4, 0.18)) if f * m < SR / 2.2)
    s *= 1 + 0.05 * np.sin(2 * np.pi * 6.1 * t)                              # slow rotary wobble
    return s * _env(n, a, r) * vel * 0.07


def bell(f, dur, vel=1.0):
    n = int((dur + 2.0) * SR); t = np.arange(n) / SR
    s = sum(w * np.sin(2 * np.pi * f * m * t) * np.exp(-t * d) for m, w, d in
            ((1, 1, 1.4), (2.0, 0.5, 2.0), (2.76, 0.4, 2.8), (5.4, 0.2, 4.5), (8.93, 0.1, 7)) if f * m < SR / 2.2)
    return s * _env(n, 0.002, 0.4) * vel * 0.12


def drone(f, dur, vel=1.0, a=1.2, r=1.2):
    """Cello-ish low drone: strings, darker, slow."""
    return strings(f, dur, vel, a=a, r=r, vib=4.6, bright=1400) * 1.6


# ------------------------------------------------------------------ percussion

def kick(vel=1.0, tune=48):
    n = int(0.5 * SR); t = np.arange(n) / SR
    f = tune + 110 * np.exp(-t * 32)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    s += _filt(np.random.default_rng(1).normal(0, 1, n), 3000) * np.exp(-t * 120) * 0.15
    return s * vel * 0.8


def snare(vel=1.0, seed=0):
    n = int(0.3 * SR); t = np.arange(n) / SR
    nz = _bp(np.random.default_rng(seed).normal(0, 1, n), 1500, 9000) * np.exp(-t * 18)
    tone = np.sin(2 * np.pi * 185 * t) * np.exp(-t * 30)
    return (nz * 0.6 + tone * 0.5) * vel * 0.45


def taiko(vel=1.0, tune=62, seed=0):
    n = int(1.4 * SR); t = np.arange(n) / SR
    f = tune + 40 * np.exp(-t * 20)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.6)
    s += _filt(np.random.default_rng(seed).normal(0, 1, n), 600) * np.exp(-t * 16) * 0.5
    return s * vel * 0.75


def boom(vel=1.0):
    """Cinematic sub impact."""
    n = int(2.4 * SR); t = np.arange(n) / SR
    f = 34 + 56 * np.exp(-t * 8)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.9)
    s += _filt(np.random.default_rng(3).normal(0, 1, n), 900) * np.exp(-t * 8) * 0.35
    return s * vel * 0.9


def crash(vel=1.0, seed=0):
    n = int(3.0 * SR); t = np.arange(n) / SR
    s = _filt(np.random.default_rng(seed).normal(0, 1, n), 4500, "high") * np.exp(-t * 1.5)
    return s * _env(n, 0.002, 0.8) * vel * 0.16


def riser(dur, vel=1.0, seed=0):
    n = int(dur * SR)
    s = _filt(np.random.default_rng(seed).normal(0, 1, n), 2600) * np.linspace(0, 1, n) ** 2.4
    return s * vel * 0.22


def heartbeat(vel=1.0):
    n = int(0.55 * SR); t = np.arange(n) / SR
    a = np.sin(2 * np.pi * 52 * t) * np.exp(-t * 14)
    b = np.zeros(n); o = int(0.17 * SR); b[o:] = a[:n - o] * 0.6
    return (a + b) * vel * 0.6


def timpani_roll(dur, f, vel=1.0):
    n = int((dur + 1.0) * SR); out = np.zeros(n); t = 0.0; k = 0
    while t < dur:
        g = 0.25 + 0.75 * (t / dur) ** 1.6
        h = taiko(g, tune=f, seed=k)[: n - int(t * SR)]
        out[int(t * SR):int(t * SR) + len(h)] += h * 0.6
        t += 0.075; k += 1
    return out * vel


# ------------------------------------------------------------------ the score

def pick_score(slug, used=()):
    """Choose a style not used in the last five Reels (all six cycle before one repeats), and a key, mode and tempo seeded by the slug,
    so a rebuild of the same Reel gives the same score but every Reel gets its own."""
    h = int(hashlib.sha1(slug.encode()).hexdigest(), 16)
    recent = list(used)[-5:]
    options = [s for s in STYLES if s not in recent] or STYLES
    style = options[h % len(options)]
    key = list(KEYS)[(h // 7) % len(KEYS)]
    lo, hi = TEMPO[style]
    bpm = lo + (h // 101) % (hi - lo + 1)
    return {"style": style, "key": key, "bpm": int(bpm), "seed": h % 100000}


def creative_score(cuts, length, verse_at=None, style="anthem", key="D", bpm=92, seed=1):
    """cuts: scene start times (the last is the seal). Returns stereo int16 at 44.1 kHz."""
    rng = np.random.default_rng(seed)
    total = int(length * SR) + 1
    buf = np.zeros((total, 2))
    root = KEYS[key]
    seal = cuts[-1]
    verse_at = cuts[-2] if verse_at is None else verse_at
    beat = 60.0 / bpm
    mode = "major" if style in ("anthem", "dawn") else "minor"
    # progressions as scale degrees, one chord per bar (4 beats) before the seal; the seal is always the major tonic
    progs = {"major": [[0, 4, 5, 3], [5, 3, 0, 4], [0, 5, 3, 4], [3, 0, 4, 5]],
             "minor": [[0, 5, 6, 0], [0, 3, 5, 4], [0, 5, 2, 6], [0, 6, 5, 4]]}
    prog = progs[mode][rng.integers(4)]
    bar = 4 * beat if style not in ("hymn", "nocturne") else 2 * beat * 2
    def chord_at(t, size=3, octave=0):
        return _chord(root, mode, prog[int(t // bar) % 4], octave, size)
    tonic_major = _chord(root, "major", 0, 0, 3)

    # ---- frame 0: the hook lands with a hit (every style)
    _add(buf, boom(0.9 if style != "nocturne" else 0.55), 0.0)
    if style in ("anthem", "march", "pulse"):
        _add(buf, crash(0.5, seed), 0.0, pan=0.2)

    # ---- bed and rhythm up to the seal
    t = 0.0
    while t < seal:
        end = min(seal, t + bar)
        c = chord_at(t)
        bass = c[0] / 2 if c[0] > 90 else c[0]
        build = 0.6 + 0.4 * min(1.0, t / max(verse_at, 0.1))          # gets fuller toward the verse
        if style == "anthem":
            for f in c: _add(buf, strings(f, end - t + 0.1, 0.8 * build, seed=seed), t, pan=rng.uniform(-0.5, 0.5))
            _add(buf, strings(bass, end - t + 0.1, 0.9, bright=1600), t)
        elif style == "hymn":
            for f in c: _add(buf, choir(f, end - t + 0.2, 0.9 * build, seed=seed), t, pan=rng.uniform(-0.6, 0.6))
            _add(buf, organ(bass, end - t + 0.2, 0.9), t)
        elif style == "march":
            _add(buf, brass(bass, beat * 0.7, 1.0), t, pan=-0.1)
            _add(buf, brass(bass, beat * 0.7, 0.8), t + 2.5 * beat, pan=-0.1)
            for f in c: _add(buf, strings(f / 2, end - t + 0.1, 0.5 * build, bright=1800), t, pan=rng.uniform(-0.5, 0.5))
        elif style == "dawn":
            for f in c: _add(buf, strings(f, end - t + 0.3, 0.55 * build, a=0.8, r=0.8, bright=2400), t, pan=rng.uniform(-0.6, 0.6))
            _add(buf, drone(bass, end - t + 0.2, 0.6), t)
        elif style == "pulse":
            _add(buf, drone(bass, end - t + 0.1, 0.8 * build), t)
        elif style == "nocturne":
            _add(buf, drone(root / 2, end - t + 0.4, 0.75), t)
            _add(buf, piano(c[0], bar * 0.95, 0.55), t, pan=-0.15)
            _add(buf, piano(c[1], bar * 0.95, 0.45), t + 0.03, pan=-0.05)
        t = end

    # ---- ostinato / percussion grid up to the seal
    step = {"anthem": beat / 2, "pulse": beat / 4, "dawn": beat / 2, "march": beat / 4}.get(style)
    if step:
        t = 0.0; k = 0
        while t < seal - 0.02:
            c = chord_at(t, size=3, octave=1 if style != "pulse" else 0)
            pattern = [0, 1, 2, 1] if style != "dawn" else [0, 1, 2, 3 % 3, 2, 1]
            f = c[pattern[k % len(pattern)] % 3]
            build = 0.55 + 0.45 * min(1.0, t / max(verse_at, 0.1))
            if style == "anthem":
                _add(buf, piano(f, step * 0.9, 0.55 * build * (1.15 if k % 2 == 0 else 0.9)), t, pan=0.25)
                if k % 4 == 0 and t > beat: _add(buf, kick(0.55 * build), t)
            elif style == "pulse":
                _add(buf, staccato(f, step * 0.6, 0.8 * build * (1.2 if k % 4 == 0 else 0.85)), t, pan=0.3 if k % 2 else -0.3)
                if k % 4 == 0: _add(buf, heartbeat(0.7) if t < verse_at else kick(0.65), t)
            elif style == "dawn":
                _add(buf, pluck(f * 2, step * 1.6, 0.6 * build, bright=0.6, seed=k), t, pan=0.35 if k % 2 else -0.2)
            elif style == "march":
                accent = (k % 8 == 0) or (k % 8 == 6)
                if k % 2 == 0 or rng.random() < 0.35:
                    _add(buf, snare(0.55 * build * (1.4 if accent else 0.7), seed=k), t, pan=0.15)
                if k % 8 == 0: _add(buf, taiko(0.9, tune=root / 2 if root / 2 > 50 else root, seed=k), t, pan=-0.2)
                if k % 8 == 4: _add(buf, taiko(0.6, tune=70, seed=k), t, pan=0.25)
            t += step; k += 1
    if style == "hymn":                                                        # timpani swells into each cut
        for c0 in cuts[1:]:
            if c0 - 1.0 > 0: _add(buf, timpani_roll(1.0, root / 2 if root / 2 > 45 else root, 0.5), c0 - 1.0)

    # ---- melody under the verse (anthem, hymn, dawn, nocturne): chord tones on the beat, a step at the end
    if style in ("anthem", "hymn", "dawn", "nocturne"):
        inst = {"anthem": strings, "hymn": choir, "dawn": bell, "nocturne": piano}[style]
        t = verse_at; prev = None
        dur_note = beat if style != "hymn" else 2 * beat
        while t < seal - 0.1:
            c = chord_at(t, size=3, octave=1)
            opts = sorted(c, key=lambda x: abs(x - prev)) if prev else c
            f = opts[0] if (prev and rng.random() < 0.6) else opts[rng.integers(len(opts))]
            if style == "nocturne": f = f * (2 if f < 300 else 1)
            kw = {"seed": seed} if inst in (strings, choir) else {}
            _add(buf, inst(f, dur_note * 0.95, 0.85, **kw), t, pan=0.1)
            prev = f; t += dur_note

    # ---- impacts on the cuts, riser into the verse
    for c0 in cuts[1:-1]:
        g = 0.55 if c0 < verse_at - 0.01 else (0.75 if abs(c0 - verse_at) < 0.01 else 0.3)
        _add(buf, boom(g * (0.7 if style in ("nocturne", "dawn") else 1.0)), c0)
    rd = min(1.6, max(0.6, verse_at - 0.2))
    _add(buf, riser(rd, 0.9 if style not in ("nocturne",) else 0.5, seed), verse_at - rd)
    _add(buf, riser(min(1.2, seal - verse_at), 0.7, seed + 1), seal - min(1.2, seal - verse_at))

    # ---- the seal: major tonic, full, sustained to the end
    hold = length - seal + 0.2
    _add(buf, boom(1.0), seal)
    if style != "nocturne": _add(buf, crash(0.8, seed + 2), seal, pan=-0.15)
    full = tonic_major + [tonic_major[0] * 2]
    if style == "anthem":
        for f in full: _add(buf, strings(f, hold, 1.0, a=0.05, r=1.2), seal, pan=rng.uniform(-0.5, 0.5))
        for f in tonic_major: _add(buf, piano(f * 2, hold, 0.7), seal, pan=0.2)
        _add(buf, kick(0.9), seal)
    elif style == "hymn":
        for f in full: _add(buf, choir(f, hold, 1.1, a=0.15, seed=seed), seal, pan=rng.uniform(-0.6, 0.6))
        _add(buf, organ(root / 2, hold, 1.0, a=0.05), seal)
    elif style == "march":
        for f in tonic_major: _add(buf, brass(f / 2, hold, 1.0, a=0.03, r=1.0), seal, pan=rng.uniform(-0.4, 0.4))
        _add(buf, taiko(1.2, tune=58, seed=99), seal)
        _add(buf, strings(tonic_major[0], hold, 0.8, a=0.05, r=1.0), seal)
    elif style == "dawn":
        for f in full: _add(buf, strings(f, hold, 0.8, a=0.15, r=1.2, bright=3000), seal, pan=rng.uniform(-0.6, 0.6))
        for i, f in enumerate(tonic_major + [tonic_major[0] * 2]): _add(buf, bell(f * 2, 1.0, 0.8), seal + i * beat / 2, pan=0.3)
    elif style == "pulse":
        for f in full: _add(buf, strings(f, hold, 1.0, a=0.04, r=1.2), seal, pan=rng.uniform(-0.5, 0.5))
        _add(buf, brass(tonic_major[0] / 2, hold, 0.9, a=0.03, r=1.0), seal)
    elif style == "nocturne":
        for i, f in enumerate(tonic_major): _add(buf, piano(f * 2, hold, 0.7), seal + i * 0.06, pan=0.1)
        _add(buf, drone(root / 2, hold, 0.9, a=0.3), seal)
        _add(buf, strings(tonic_major[2], hold, 0.5, a=0.5, r=1.2), seal, pan=0.4)

    # ---- room, glue and level
    ir_n = int((2.6 if style in ("hymn", "nocturne", "dawn") else 1.8) * SR); ir_t = np.arange(ir_n) / SR
    ir = _filt(np.random.default_rng(seed).normal(0, 1, ir_n), 5000) * np.exp(-ir_t * 2.4)
    ir /= np.abs(ir).sum() / 5
    wet = np.stack([fftconvolve(buf[:, c], ir)[:total] for c in range(2)], 1)
    mix = buf * 0.82 + wet * (0.34 if style in ("hymn", "nocturne", "dawn") else 0.24)
    mix = _filt(mix.T, 30, "high").T                                          # no sub rumble below 30 Hz
    mix *= _env(total, 0.004, 1.3)[:, None]
    mix /= np.abs(mix).max() + 1e-9
    mix = np.tanh(1.8 * mix) / np.tanh(1.8)                                   # gentle glue, louder on phones
    mix *= 0.89
    return (mix[: int(length * SR)] * 32767).astype("int16")
