"""Render a white-bubble title with colour emoji to a transparent PNG.
usage: python3 title_png.py "TEXTE 🔥" out.png [max_width]"""
import sys, subprocess
from PIL import Image, ImageDraw, ImageFont

text, out = sys.argv[1], sys.argv[2]
maxw = int(sys.argv[3]) if len(sys.argv) > 3 else 860
fp = subprocess.run(["fc-match", "-f", "%{file}", "Inter Display:black"], capture_output=True, text=True).stdout
font = ImageFont.truetype(fp, 82)
efont = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
ES = 82 / 109


def is_emoji(c):
    o = ord(c)
    return o >= 0x1F000 or 0x2600 <= o <= 0x27BF or 0x2300 <= o <= 0x23FF or 0x2B00 <= o <= 0x2BFF or o in (0xFE0F, 0x200D)


def runs(s):
    out, cur, emo = [], "", None
    for c in s:
        e = is_emoji(c)
        if emo is None or e == emo: cur += c
        else: out.append((cur, emo)); cur = c
        emo = e
    if cur: out.append((cur, emo))
    return out


def width(s):
    w = 0
    for r, e in runs(s):
        if e:
            w += sum(int(efont.getlength(ch) * ES) for ch in r.replace("️", "") if ch != "‍") + 6
        else:
            w += font.getlength(r)
    return w


# wrap words
words, lines, cur = text.split(), [], ""
for wd in words:
    t = (cur + " " + wd).strip()
    if width(t) <= maxw or not cur: cur = t
    else: lines.append(cur); cur = wd
lines.append(cur)
LH, PADX, PADY = 104, 34, 16
W = int(max(width(l) for l in lines) + 2 * PADX)
H = LH * len(lines) + 2 * PADY
img = Image.new("RGBA", (W + 20, H + 20), (0, 0, 0, 0))
tmask = Image.new("L", img.size, 0); tm = ImageDraw.Draw(tmask)
d = ImageDraw.Draw(img)
for i, l in enumerate(lines):
    lw = width(l)
    x0 = (W - lw) / 2 - PADX + 10
    y0 = 10 + PADY + i * LH
    d.rounded_rectangle([x0, y0 - 8, x0 + lw + 2 * PADX, y0 + LH - 4], radius=26, fill=(255, 255, 255, 255))
    x = x0 + PADX
    for r, e in runs(l):
        if e:
            for ch in r:
                if ch in ("️", "‍"): continue
                g = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
                ImageDraw.Draw(g).text((0, 0), ch, font=efont, embedded_color=True)
                bb = g.getbbox()
                if not bb: continue
                g = g.crop(bb); s = 82 / 109
                g = g.resize((int(g.width * s), int(g.height * s)), Image.LANCZOS)
                img.alpha_composite(g, (int(x + 3), int(y0 + (LH - g.height) / 2 - 4)))
                x += g.width + 6
        else:
            tm.text((x, y0 + 4), r, font=font, fill=255)
            x += font.getlength(r)
# charte v2 : texte en dégradé violet -> magenta -> rose
import numpy as np
cols = [(123, 63, 228), (229, 46, 158), (255, 61, 168)]
g = np.zeros((img.height, img.width, 3), np.uint8)
for i in range(img.width):
    t = i / max(1, img.width - 1); k = min(int(t * 2), 1); u = t * 2 - k
    g[:, i] = [int(cols[k][j] * (1 - u) + cols[k + 1][j] * u) for j in range(3)]
img.paste(Image.fromarray(g).convert("RGBA"), (0, 0), tmask)
img.save(out)
print(out, img.size)
