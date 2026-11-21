"""Couverture « actu » validée le 20/11/2026 (option A, Inter Display Black en majuscules).
usage: python3 make_cover.py fond.jpg "SUJET" "CATÉGORIE" "LIGNE 1" "LIGNE 2" "sous-titre rose" out.jpg
ex.   python3 make_cover.py visuals/rockstar/x.jpg ARGENT "GTA 6 · ARGENT" ARGENT ILLIMITÉ "5 astuces cachées dans GTA 6" cover.jpg
Utiliser comme 1re image des diaporamas (et miniature). Fond = visuel officiel choisi via visuals_used.json.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

bg, topic, cat, l1, l2, sub, out = sys.argv[1:8]
F = "/usr/share/fonts/opentype/inter/"
HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
VIO, MAG, PINK = (123, 63, 228), (229, 46, 158), (255, 61, 168)


def f(n, s): return ImageFont.truetype(F + n, s)


im = Image.open(bg).convert("RGB"); r = max(W / im.width, H / im.height)
im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1)); x = (im.width - W) // 2
im = im.crop((x, 0, x + W, H)).convert("RGBA")
g = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(g); s = int(H * 0.42)
for y in range(s, H): d.line([(0, y), (W, y)], fill=(18, 6, 40, min(245, int(300 * (y - s) / (H - s)))))
im.alpha_composite(g); d = ImageDraw.Draw(im)
d.rounded_rectangle((140, 230, W - 140, 278), 24, fill=(255, 255, 255, 220))
d.text((W / 2, 254), f"ACTU GTA VI  ·  {topic.upper()}", font=f("Inter-SemiBold.otf", 26), fill=VIO, anchor="mm")
ft = f("Inter-SemiBold.otf", 32); w = d.textlength(cat, font=ft) + 48
d.rounded_rectangle(((W - w) / 2, 1180, (W + w) / 2, 1236), 28, fill=MAG); d.text((W / 2, 1208), cat, font=ft, fill="white", anchor="mm")
for i, line in enumerate((l1, l2)):
    size = 160
    while d.textlength(line.upper(), font=f("InterDisplay-Black.otf", size)) > 800: size -= 6
    d.text((W / 2, 1260 + i * 170), line.upper(), font=f("InterDisplay-Black.otf", size), fill="white", anchor="mt")
d.text((W / 2, 1625), sub, font=f("InterDisplay-SemiBold.otf", 40), fill=PINK, anchor="mt")
a = Image.open(os.path.join(HERE, "avatar_v2.png")).convert("RGBA").resize((96, 96))
m = Image.new("L", (96, 96)); ImageDraw.Draw(m).ellipse((0, 0, 95, 95), fill=255); im.paste(a, ((W - 96) // 2, 1740), m)
im.convert("RGB").save(out, quality=92); print("OK", out)
