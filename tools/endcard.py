"""Charte v2 end card: violet background, round avatar, white pill « Abonne-toi pour la suite ».
usage: python3 endcard.py out.png"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
fp = subprocess.run(["fc-match", "-f", "%{file}", "Inter Display:bold"], capture_output=True, text=True).stdout
W, H = 1080, 1920
im = Image.new("RGBA", (W, H), (27, 10, 60, 255))
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse((240, 520, 840, 1120), fill=(123, 63, 228, 150))
im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(90)))
av = Image.open(os.path.join(HERE, "avatar_v2.png")).convert("RGBA").resize((520, 520), Image.LANCZOS)
mk = Image.new("L", (520, 520), 0); ImageDraw.Draw(mk).ellipse((0, 0, 519, 519), fill=255)
im.paste(av, (280, 560), mk)
font = ImageFont.truetype(fp, 60); txt = "Abonne-toi pour la suite"
d = ImageDraw.Draw(im); w = d.textlength(txt, font=font) + 120; x = (W - w) / 2; y = 1190
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x, y + 12, x + w, y + 162), 80, fill=(10, 0, 30, 140))
im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
d.rounded_rectangle((x, y, x + w, y + 150), 75, fill=(255, 255, 255, 255))
d.text((W / 2, y + 75), txt, font=font, fill=(27, 10, 60), anchor="mm")
im.convert("RGB").save(sys.argv[1]); print("OK", sys.argv[1])
