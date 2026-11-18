"""Beat-synced vertical montage of official stills with slow pans.
usage: python3 make_montage.py spec.json
spec: {"images":[...], "out":..., "music":..., "hook":..., "big":"J-3", "labels":[...optional per image], "avatar":..., "seg":2.4}
"""
import json, os, subprocess, sys

spec = json.load(open(sys.argv[1]))
W, H, FPS = 1080, 1920, 30
SEG = spec.get("seg") or 4 * 60 / spec.get("bpm", 118)
tmp = os.path.join(os.path.dirname(os.path.abspath(spec["out"])), "_mbuild")
os.makedirs(tmp, exist_ok=True)
FONT = "Inter Display"


def run(c):
    subprocess.run(c, check=True)


def ts(t):
    return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"


parts = []
labels = spec.get("labels") or []
for i, img in enumerate(spec["images"]):
    o = os.path.join(tmp, f"s{i}.mp4")
    sw = int(H * 16 / 9)  # scaled width
    span = sw - W
    a, b = (0.1, 0.7) if i % 2 == 0 else (0.9, 0.3)
    x = f"({span}*({a}+({b}-{a})*t/{SEG}))"
    zoom = 1.0 + (0.06 if i % 3 == 0 else 0)
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", str(SEG), "-i", img, "-vf",
         f"scale={int(sw*zoom)}:{int(H*zoom)},crop={W}:{H}:x='{x}':y=(ih-{H})/2,fps={FPS},format=yuv420p",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", o])
    parts.append(o)

lst = os.path.join(tmp, "l.txt")
open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
body = os.path.join(tmp, "body.mp4")
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", body])
D = SEG * len(parts)

ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,{FONT},74,&H00111111,&H00111111,&H00FFFFFF,&H00000000,1,0,0,0,100,100,0,0,3,16,0,8,130,150,230,1
Style: Big,{FONT},300,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,14,0,5,0,0,0,1
Style: Lab,{FONT},62,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,6,0,2,120,150,560,1
Style: WM,{FONT},46,&H8CFFFFFF,&H8CFFFFFF,&HB4000000,&H00000000,1,0,0,0,100,100,1,0,1,2.5,0,5,0,0,0,1
Style: End,{FONT},78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,7,0,8,60,60,1330,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 1,{ts(0.1)},{ts(SEG*2)},Big,,0,0,0,,{{\\pos({W//2},{H//2})\\fscx40\\fscy40\\t(0,250,\\fscx110\\fscy110)\\t(250,400,\\fscx100\\fscy100)\\fad(0,300)}}{spec['big']}
Dialogue: 0,{ts(0)},{ts(D)},WM,,0,0,0,,{{\\pos({W//2},{int(H*0.70)})}}@partnersinvicefr
"""
for i, lab in enumerate(labels):
    if lab:
        ass += f"Dialogue: 2,{ts(i*SEG+0.15)},{ts((i+1)*SEG-0.1)},Lab,,0,0,0,,{{\\fad(150,150)}}{lab}\n"
assf = os.path.join(tmp, "m.ass")
open(assf, "w").write(ass)

# end card (charte v2)
endpng = os.path.join(tmp, "end.png")
run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "endcard.py"), endpng])
endv = os.path.join(tmp, "end.mp4")
run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", endpng, "-vf", "fade=in:st=0:d=0.25,format=yuv420p",
     "-t", "3", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", endv])

withtxt = os.path.join(tmp, "txt.mp4")
run(["ffmpeg", "-v", "error", "-y", "-i", body, "-vf", f"subtitles={assf}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", withtxt])
open(lst, "w").write(f"file '{withtxt}'\nfile '{endv}'\n")
silent = os.path.join(tmp, "silent.mp4")
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent])
T = D + 3
title = os.path.join(tmp, "title.png")
run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "title_png.py"), spec["hook"], title, "940"])
B = 60 / spec.get("bpm", 118)
sc = f"(min(1,0.35+t*2.6))*(1+0.06*exp(-mod(t,{B:.4f})*9))"
run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", spec["music"], "-loop", "1", "-i", title,
     "-filter_complex",
     f"[2:v]format=rgba,scale=w='iw*{sc}':h=-1:eval=frame[tt];"
     f"[0:v][tt]overlay=x='(W-w)/2':y='230-(h-260)/2':enable='lt(t,{D:.2f})':shortest=1[v];"
     f"[1:a]atrim=0:{T},afade=t=out:st={T-2}:d=2[a]",
     "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-c:a", "aac", "-b:a", "192k", "-t", str(T), spec["out"]])
print("OK", T, spec["out"])
