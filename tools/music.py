"""Original royalty-free tracks for Partners in Vice edits.
usage: python3 music.py STYLE OUT.wav SECONDS [seed]
STYLE: outrun (118 bpm synthwave, pumping), phonk (130 bpm drift-phonk, 808 + cowbell), heist (108 bpm dark, big snare)
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
}[style]
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
            else:
                m = ch[0] - 12 + (12 if k % 2 else 0)
                put(music, onepole(saw(hz(m), tb), 0.15) * env(Lb, 0.003, 0.06) * 0.35, t0 + k * beat / 2)
        if P["lead"]:
            for k in range(8):
                Ll = int(beat / 2 * SR); tl = np.arange(Ll) / SR
                m = ch[0] + 12 + melody[(k + b * 3) % 8]
                sq = np.sign(np.sin(2 * np.pi * hz(m) * tl)) * 0.5 + saw(hz(m) * 2.003, tl) * 0.5
                put(music, onepole(sq, 0.25) * env(Ll, 0.005, 0.12) * 0.11, t0 + k * beat / 2)
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
            put(drums, kick * 0.85, t0 + k * beat)
            if k % 2:
                Ls = int(0.35 * SR)
                sn = rng.standard_normal(Ls) * np.exp(-np.arange(Ls) / SR * (9 if style == "heist" else 14))
                tone = np.sin(2 * np.pi * 190 * np.arange(Ls) / SR) * np.exp(-np.arange(Ls) / SR * 30)
                put(drums, (onepole(sn, 0.55) * 0.5 + tone * 0.35), t0 + k * beat)
            for h in range(2 if style != "phonk" else 4):
                Lh = int(0.04 * SR)
                hh = rng.standard_normal(Lh) * np.exp(-np.arange(Lh) / SR * 90)
                put(drums, (hh - onepole(hh, 0.3)) * 0.16, t0 + k * beat + (h + 0.5) * beat / (2 if style != "phonk" else 4))
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
