"""Photo carousel (1080x1350, works on TikTok photo mode and Instagram).
usage: python3 make_carousel.py spec.json
spec: {"out_dir":..., "slides":[{"img":path, "text":"... emoji ok", "pos":"top|bottom", "focus":0.5}], "end":{"img":..., "text":...}}
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
spec = json.load(open(sys.argv[1]))
W, H = 1080, 1350
os.makedirs(spec["out_dir"], exist_ok=True)
fp = subprocess.run(["fc-match", "-f", "%{file}", "Inter Display:bold"], capture_output=True, text=True).stdout
wm_font = ImageFont.truetype(fp, 34)


def bubble(text, maxw=900):
    tmp = os.path.join(spec["out_dir"], "_t.png")
    subprocess.run(["python3", os.path.join(HERE, "title_png.py"), text, tmp, str(maxw)], check=True, capture_output=True)
    return Image.open(tmp).convert("RGBA")


def cover(img, focus=0.5):
    im = Image.open(img).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    x = int((im.width - W) * focus)
    return im.crop((x, (im.height - H) // 2, x + W, (im.height - H) // 2 + H)).convert("RGBA")


def watermark(c):
    d = ImageDraw.Draw(c)
    t = "@partnersinvicefr"
    w = d.textlength(t, font=wm_font)
    d.text(((W - w) / 2, H - 70), t, font=wm_font, fill=(255, 255, 255, 170), stroke_width=2, stroke_fill=(0, 0, 0, 120))


slides = spec["slides"] + ([spec["end"]] if spec.get("end") else [])
for i, s in enumerate(slides):
    c = cover(s["img"], s.get("focus", 0.5))
    # soft dark gradient where the text sits
    g = Image.new("L", (1, H))
    top = s.get("pos", "bottom") == "top"
    for y in range(H):
        r = (1 - y / (H * 0.4)) if top else ((y - H * 0.55) / (H * 0.45))
        g.putpixel((0, y), int(150 * max(0, min(1, r))))
    shade = Image.new("RGBA", (W, H), (10, 4, 25, 255))
    shade.putalpha(g.resize((W, H)))
    c = Image.alpha_composite(c, shade)
    if s.get("text"):
        b = bubble(s["text"], 1000 if i == 0 else 1150)
        k = 1.0 if i == 0 else 0.78
        if b.width * k > W - 60: k = (W - 60) / b.width
        b = b.resize((int(b.width * k), int(b.height * k)), Image.LANCZOS)
        y = 70 if top else H - b.height - 120
        c.alpha_composite(b, ((W - b.width) // 2, y))
    if s.get("sub"):
        f = ImageFont.truetype(fp, 46)
        d = ImageDraw.Draw(c)
        for k, line in enumerate(s["sub"].split("\n")):
            w = d.textlength(line, font=f)
            d.text(((W - w) / 2, H - 330 + k * 60), line, font=f, fill="white", stroke_width=4, stroke_fill=(0, 0, 0))
    watermark(c)
    c.convert("RGB").save(os.path.join(spec["out_dir"], f"{i+1:02d}.jpg"), quality=92)
print("OK", len(slides), spec["out_dir"])
