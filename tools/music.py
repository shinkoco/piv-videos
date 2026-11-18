"""Original royalty-free tracks for Partners in Vice edits.
usage: python3 music.py STYLE OUT.wav SECONDS [seed]
STYLE: outrun 118, heist 108, miami 92 (planant), drive 140 (darksynth), funk 112 (groove 80s), sunset 104 (synthwave lumineuse, arpèges), tension 88 (suspense). phonk existe mais est INTERDIT.
"""
import sys, wave
import numpy as np

style, out, secs = sys.argv[1], sys.argv[2], float(sys.argv[3])
rng = np.random.default_rng(int(sys.argv[4]) if len(sys.argv) > 4 else 11)
SR = 44100
P = {
    "outrun": dict(bpm=118, chords=[[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]], lead=True, cow=False, b808=False, pump=0.55),
    "phonk": dict(bpm=130, chords=[[50, 53, 57], [50, 53, 57], [46, 50, 53], [48, 52, 55]], lead=False, cow=True, b808=True, pump=0.35),
    "heist": dict(bpm=108, chords=[[52, 55, 59], [48, 52, 55], [50, 53, 57], [47, 50, 54]], lead=True, cow=False, b808=True, pump=0.45),
    "miami": dict(bpm=92, chords=[[53, 57, 60, 64], [50, 53, 57, 60], [46, 50, 53, 57], [48, 52, 55, 59]], lead=True, cow=False, b808=False, pump=0.3, half=True, leadsteps=4, bassmode="whole"),
    "drive": dict(bpm=140, chords=[[45, 48, 52], [41, 45, 48], [43, 47, 50], [40, 43, 47]], lead=True, cow=False, b808=False, pump=0.6, leadsteps=16, bassmode="16th"),
    "funk": dict(bpm=112, chords=[[50, 53, 57, 60], [55, 59, 62, 65], [52, 55, 59, 62], [57, 61, 64, 67]], lead=False, cow=False, b808=False, pump=0.25, bassmode="funk", stabs=True, hats16=True),
    "sunset": dict(bpm=104, chords=[[52, 56, 59, 63], [49, 52, 56, 59], [45, 49, 52, 56], [47, 51, 54, 57]], lead=True, cow=False, b808=False, pump=0.5, leadsteps=16, bassmode="8th"),
    "tension": dict(bpm=88, chords=[[45, 48, 52], [46, 49, 53], [45, 48, 52], [44, 47, 51]], lead=False, cow=False, b808=False, pump=0.35, half=True, bassmode="pulse", nosnare=True),
}[style]
P.setdefault("half", False); P.setdefault("leadsteps", 8); P.setdefault("bassmode", "8th"); P.setdefault("stabs", False); P.setdefault("hats16", False); P.setdefault("nosnare", False)
beat = 60 / P["bpm"]
bar = 4 * beat
n = int(SR * secs)
music = np.zeros(n)
drums = np.zeros(n)


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def saw(f, tt):
    return 2 * (tt * f - np.floor(0.5 + tt * f))


def env(L, a=0.005, r=0.1):
    e = np.ones(L)
    ai, ri = max(1, int(a * SR)), int(r * SR)
    e[:ai] = np.linspace(0, 1, ai)
    if 0 < ri < L:
        e[-ri:] = np.linspace(1, 0, ri)
    return e


def onepole(x, a):
    # vectorised-ish one pole low-pass via scipy-free recursion on chunks
    y = np.empty_like(x); acc = 0.0
    for i in range(0, len(x)):
        acc += a * (x[i] - acc); y[i] = acc
    return y


def put(buf, sig, start):
    s = int(start * SR)
    if s >= n: return
    e = min(n, s + len(sig)); buf[s:e] += sig[: e - s]


nb = int(secs / bar) + 1
intro = 2  # bars before the drop
melody = [0, 3, 7, 10, 7, 3, 5, 7]
for b in range(nb):
    ch = P["chords"][b % 4]
    t0 = b * bar
    drop = b >= intro
    L = int(bar * SR); tt = np.arange(L) / SR
    pad = sum(saw(hz(m), tt) + saw(hz(m) * 1.006, tt) for m in ch) / 6
    put(music, onepole(pad, 0.05) * env(L, 0.2, 0.3) * (0.25 if drop else 0.35), t0)
    if drop:
        for k in range(8):  # bass
            Lb = int(beat / 2 * SR); tb = np.arange(Lb) / SR
            if P["b808"]:
                if k in (0, 3, 6):
                    L8 = int(beat * 1.4 * SR); t8 = np.arange(L8) / SR
                    f = hz(ch[0] - 24) * (1 + 0.8 * np.exp(-t8 * 40))
                    s8 = np.tanh(2.5 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t8 * 2.2)
                    put(music, s8 * 0.55, t0 + k * beat / 2)
            elif P["bassmode"] == "8th":
                m = ch[0] - 12 + (12 if k % 2 else 0)
                put(music, onepole(saw(hz(m), tb), 0.15) * env(Lb, 0.003, 0.06) * 0.35, t0 + k * beat / 2)
        if P["bassmode"] == "16th":
            for k in range(16):
                Lb = int(beat / 4 * SR); tb = np.arange(Lb) / SR
                put(music, onepole(saw(hz(ch[0] - 12), tb), 0.2) * env(Lb, 0.002, 0.03) * 0.33, t0 + k * beat / 4)
        elif P["bassmode"] == "whole":
            Lb = int(bar * SR); tb = np.arange(Lb) / SR
            put(music, onepole(saw(hz(ch[0] - 12), tb), 0.06) * env(Lb, 0.05, 0.4) * 0.35, t0)
        elif P["bassmode"] == "pulse":
            for k in range(8):
                Lb = int(beat / 2 * SR); tb = np.arange(Lb) / SR
                put(music, np.sin(2 * np.pi * hz(ch[0] - 24) * tb) * env(Lb, 0.01, 0.15) * (0.5 if k % 2 == 0 else 0.25), t0 + k * beat / 2)
        elif P["bassmode"] == "funk":
            for k, (st, o) in enumerate([(0, 0), (0.75, 12), (1.5, 0), (2, 7), (2.75, 12), (3.25, 10), (3.5, 0)]):
                Lb = int(beat * 0.3 * SR); tb = np.arange(Lb) / SR
                put(music, np.tanh(2 * onepole(saw(hz(ch[0] - 12 + o), tb), 0.3)) * np.exp(-tb * 9) * 0.4, t0 + st * beat)
        if P["stabs"]:
            for k in (1.5, 3.5):
                Ls = int(beat * 0.25 * SR); ts_ = np.arange(Ls) / SR
                st_ = sum(np.sign(np.sin(2 * np.pi * hz(m) * ts_)) for m in ch) / len(ch)
                put(music, onepole(st_, 0.4) * np.exp(-ts_ * 14) * 0.16, t0 + k * beat)
        if P["lead"]:
            ls = P["leadsteps"]
            for k in range(ls):
                Ll = int(bar / ls * SR); tl = np.arange(Ll) / SR
                m = ch[0] + 12 + melody[int(rng.integers(0, 8)) if ls == 4 else (k + b * 3) % 8]
                sq = np.sign(np.sin(2 * np.pi * hz(m) * tl)) * 0.5 + saw(hz(m) * 2.003, tl) * 0.5
                put(music, onepole(sq, 0.25 if ls >= 8 else 0.08) * env(Ll, 0.005 if ls >= 8 else 0.08, 0.12 if ls >= 8 else 0.6) * (0.11 if ls >= 8 else 0.14), t0 + k * bar / ls)
        if P["cow"]:
            for k in range(16):
                if k in (0, 3, 6, 8, 10, 13):
                    Lc = int(0.18 * SR); tc = np.arange(Lc) / SR
                    m = ch[0] + 24 + (7 if k in (6, 13) else 0)
                    cw = (np.sign(np.sin(2 * np.pi * hz(m) * tc)) + np.sign(np.sin(2 * np.pi * hz(m) * 1.48 * tc))) * np.exp(-tc * 22)
                    put(music, onepole(cw, 0.35) * 0.12, t0 + k * beat / 4)
        for k in range(4):  # drums
            Lk = int(0.3 * SR); tk = np.arange(Lk) / SR
            kick = np.tanh(3 * np.sin(2 * np.pi * (45 + 140 * np.exp(-tk * 35)) * tk)) * np.exp(-tk * 8)
            if not (P["half"] and k % 2):
                put(drums, kick * 0.85, t0 + k * beat)
            if (k == 2 if P["half"] else k % 2) and not P["nosnare"]:
                Ls = int(0.35 * SR)
                sn = rng.standard_normal(Ls) * np.exp(-np.arange(Ls) / SR * (9 if style == "heist" else 14))
                tone = np.sin(2 * np.pi * 190 * np.arange(Ls) / SR) * np.exp(-np.arange(Ls) / SR * 30)
                put(drums, (onepole(sn, 0.55) * 0.5 + tone * 0.35), t0 + k * beat)
            for h in range(4 if (style == "phonk" or P["hats16"]) else 2):
                Lh = int(0.04 * SR)
                hh = rng.standard_normal(Lh) * np.exp(-np.arange(Lh) / SR * 90)
                put(drums, (hh - onepole(hh, 0.3)) * 0.16, t0 + k * beat + (h + 0.5) * beat / (4 if (style == "phonk" or P["hats16"]) else 2))
    else:  # intro riser
        Lr = int(bar * SR)
        nz = rng.standard_normal(Lr) * np.linspace(0, 1, Lr) ** 2
        put(music, (nz - onepole(nz, 0.2)) * (0.08 if b == intro - 1 else 0.02), t0)

# sidechain pump on music from kicks
pump = np.ones(n)
L = int(beat * SR)
shape = 1 - P["pump"] * np.exp(-np.arange(L) / SR * 9)
for b in range(intro, nb):
    for k in range(4):
        s = int((b * bar + k * beat) * SR)
        if s < n:
            e = min(n, s + L); pump[s:e] = shape[: e - s]
mix = music * pump + drums
d = int(beat * 0.75 * SR); echo = np.zeros(n); echo[d:] = music[:-d] * pump[:-d] * 0.18
mix += echo
mix = np.tanh(mix * 1.4)
f = int(1.5 * SR); mix[-f:] *= np.linspace(1, 0, f)
mix = mix / np.max(np.abs(mix)) * 0.9
st = np.stack([mix, np.roll(mix, 220)], 1)
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
print("ok", style, P["bpm"], "bpm", secs, "s")
