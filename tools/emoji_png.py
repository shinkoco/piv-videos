"""Render one colour emoji to a transparent PNG. usage: python3 emoji_png.py 🔥 out.png [size]"""
import sys
from PIL import Image, ImageDraw, ImageFont
e, out = sys.argv[1], sys.argv[2]; size = int(sys.argv[3]) if len(sys.argv) > 3 else 170
f = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
g = Image.new("RGBA", (160, 160), (0, 0, 0, 0)); ImageDraw.Draw(g).text((0, 0), e, font=f, embedded_color=True)
g = g.crop(g.getbbox()); g.resize((size, int(size * g.height / g.width)), Image.LANCZOS).save(out)
