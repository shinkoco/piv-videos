"""Build a 60s+ vertical 'Top N' compilation with FR captions, hook, context cards,
zoom punches, progress bar and end card.  usage: python3 make_compil.py spec.json"""
import json, subprocess, sys, os

spec = json.load(open(sys.argv[1]))
SRC, OUT, HOOK = spec.get("src"), spec["out"], spec["hook"]
AVATAR = spec["avatar"]
W, H = 1080, 1920
LAYOUT = spec.get("layout", "classic")
CAM = spec.get("cam")  # [x, y, w, h] webcam box in source pixels
if LAYOUT == "split":
    GH, CH = 1100, 820          # gameplay top height, facecam bottom height
    FY, FH, FW = 0, GH, W
    CAPY, CTXY, NUMY, BARY = GH + 40, 470, 345, GH - 6
else:
    FW, FH, FY = 1080, 608, 640
    CAPY, CTXY, NUMY, BARY = 1330, 470, 560, FY + FH
FONT = "Inter Display"
tmp = os.path.join(os.path.dirname(OUT) or ".", "_build")
os.makedirs(tmp, exist_ok=True)


def run(cmd):
    subprocess.run(cmd, check=True)


def ts(t):
    t = max(t, 0)
    return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"


def esc(s):
    return s.replace("{", "(").replace("}", ")")


HEAD = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{FONT},78,&H00FFFFFF,&H00A83DFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,7,0,8,110,150,{CAPY},1
Style: Ctx,{FONT},56,&H00FFFFFF,&H00FFFFFF,&H003C0A1B,&HCC3C0A1B,1,0,0,0,100,100,0,0,3,18,0,8,120,150,{CTXY},1
Style: Num,{FONT},120,&H009E2EE5,&H009E2EE5,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,8,0,7,70,50,{NUMY},1
Style: React,{FONT},130,&H00FFFFFF,&H00FFFFFF,&H00E43F7B,&H00000000,1,0,0,0,100,100,0,0,1,10,0,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

EMOJI_SETS = [["🔥", "😱"], ["💀", "😂"], ["🚨", "🔥"], ["😳", "💥"], ["🤣", "💀"]]
parts = []
for i, m in enumerate(spec["moments"]):
    a, b = m["start"], m["end"]
    d = b - a
    ass = HEAD
    ass += f"Dialogue: 2,{ts(0)},{ts(d)},Num,,0,0,0,,{{\\fad(150,0)}}#{m['rank']}\n"
    ass += f"Dialogue: 1,{ts(0.2)},{ts(3.6)},Ctx,,0,0,0,,{{\\fad(200,200)}}{esc(m['context'])}\n"
    caps = m["captions"]
    for ci, c in enumerate(caps):
        s, e, txt = c[0] - a, c[1] - a, c[2]
        nxt = caps[ci + 1][0] - a if ci + 1 < len(caps) else d
        words = txt.split()
        dur = max(e - s, 0.4)
        k = max(int(dur * 100 / len(words)), 8)
        kar = " ".join(f"{{\\k{k}}}{esc(w)}" for w in words)
        ass += f"Dialogue: 0,{ts(s)},{ts(min(max(e, s + 0.9), nxt))},Cap,,0,0,0,,{{\\fscx80\\fscy80\\t(0,120,\\fscx100\\fscy100)}}{kar}\n"
    p = m["peak"] - a
    ass += (f"Dialogue: 3,{ts(p)},{ts(p + 1.4)},React,,0,0,0,,"
            f"{{\\pos({W//2},{FY + (int(FH*0.55) if LAYOUT=="split" else FH//2)})\\frz-6\\fscx30\\fscy30\\t(0,140,\\fscx115\\fscy115)\\t(140,260,\\fscx100\\fscy100)\\fad(0,250)}}{esc(m['reaction'])}\n")
    assf = os.path.join(tmp, f"m{i}.ass")
    open(assf, "w").write(ass)
    seg = os.path.join(tmp, f"m{i}.mp4")
    zoom = f"if(between(in_time,{p:.2f},{p+1.5:.2f}),1.22,1)"
    if LAYOUT == "split":
        cx, cy, cw, ch = CAM
        sw = int(720 * W / GH)  # source crop width for gameplay (center)
        tw = int(ch * W / CH)   # cam crop width matching panel aspect
        tx = cx + (cw - tw) // 2
        fc = (f"[0:v]fps=30,split[a][b];"
              f"[a]crop={sw}:720:(iw-{sw})/2:0,scale={W}:{GH}:flags=lanczos,"
              f"zoompan=z='{zoom}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{GH}:fps=30[g];"
              f"[b]crop={tw}:{ch}:{tx}:{cy},scale={W}:{CH}:flags=lanczos,unsharp=5:5:0.8[c];"
              f"[g][c]vstack,"
              f"drawbox=x=0:y=0:w={W}:h={GH}:color=white@0.55:t=fill:enable='between(t,{p:.2f},{p+0.12:.2f})',"
              f"subtitles={assf}[v]")
    else:
        fc = (f"[0:v]fps=30,split[a][b];"
              f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=25:3,eq=brightness=-0.12[bg];"
              f"[b]scale={FW}:{FH},zoompan=z='{zoom}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={FW}x{FH}:fps=30[fg];"
              f"[bg][fg]overlay=0:{FY},"
              f"drawbox=x=0:y={FY}:w={W}:h={FH}:color=white@0.55:t=fill:enable='between(t,{p:.2f},{p+0.12:.2f})',"
              f"subtitles={assf}[v]")
    # emojis autour du mot-réaction (gratuit : rendu local)
    EMO = m.get("emojis") or EMOJI_SETS[i % len(EMOJI_SETS)]
    ey = FY + (int(FH*0.55) if LAYOUT == "split" else FH//2) - 85
    extra_in, chain = [], "[s0]"
    fc = fc.replace(f"subtitles={assf}[v]", f"subtitles={assf}[s0]")
    for j, (emo, ex) in enumerate(zip(EMO[:2], [90, W - 260])):
        ep = os.path.join(tmp, f"e{i}_{j}.png")
        run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "emoji_png.py"), emo, ep, "170"])
        extra_in += ["-loop", "1", "-i", ep]
        t0 = p + 0.08 * j
        nxt = "[v]" if j == min(len(EMO), 2) - 1 else f"[s{j+1}]"
        fc += (f";[{j+1}:v]format=rgba,rotate='{(-0.25 if j == 0 else 0.25)}*sin(2*PI*t)':c=none:ow=rotw(0.3):oh=roth(0.3)[em{j}];"
               f"{chain}[em{j}]overlay=x={ex}:y='{ey}-70*max(0,t-{t0:.2f})':enable='between(t,{t0:.2f},{t0+1.3:.2f})':shortest=1{nxt}")
        chain = nxt
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(d), "-i", m.get("src", SRC), *extra_in,
         "-filter_complex", fc, "-map", "[v]", "-map", "0:a",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-c:a", "aac", "-ar", "48000", "-ac", "2", seg])
    parts.append(seg)

# end card (charte v2)
endpng = os.path.join(tmp, "end.png")
run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "endcard.py"), endpng])
endseg = os.path.join(tmp, "end.mp4")
run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-i", endpng,
     "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
     "-vf", "fade=in:st=0:d=0.25,format=yuv420p", "-map", "0:v", "-map", "1:a", "-t", "3",
     "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-c:a", "aac", "-ar", "48000", "-ac", "2", endseg])
parts.append(endseg)

lst = os.path.join(tmp, "list.txt")
open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
joined = os.path.join(tmp, "joined.mp4")
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined])
D = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", joined],
                         capture_output=True, text=True).stdout)
hookass = os.path.join(tmp, "hook.ass")
open(hookass, "w").write(HEAD.replace("Style: Num", f"Style: Hook,{FONT},74,&H00E43F7B,&H00E43F7B,&H00FFFFFF,&H00000000,1,0,0,0,100,100,0,0,3,16,0,8,130,150,{150 if LAYOUT=='split' else 230},1\nStyle: WM,{FONT},46,&H8CFFFFFF,&H8CFFFFFF,&HB4000000,&H00000000,1,0,0,0,100,100,1,0,1,2.5,0,5,0,0,0,1\nStyle: Num") +
    f"Dialogue: 0,{ts(0)},{ts(D - 3)},WM,,0,0,0,,{{\\pos({W//2},{FY + int(FH*0.78)})}}@partnersinvicefr\n")
HERE = os.path.dirname(os.path.abspath(__file__))
MUSIC = spec.get("music", os.path.join(HERE, "music_outrun.wav"))  # null = no music (streamer already has music)
LVL = float(spec.get("music_level", 0.13))
hookpng = os.path.join(tmp, "hook.png")
run(["python3", os.path.join(HERE, "title_png.py"), HOOK, hookpng, "900"])
HY = 120 if LAYOUT == 'split' else 200
vf = (f"[0:v]subtitles={hookass},drawbox=x=0:y={BARY}:w={W}:h=12:color=black@0.5:t=fill[b0];"
      f"[b0][2:v]overlay=x=(W-w)/2:y={HY}:enable='lt(t,{D-3:.2f})'[base];"
      f"[base][1:v]overlay=x='-{W}+{W}*t/{D:.2f}':y={BARY}:shortest=1[v]")
cmd = ["ffmpeg", "-v", "error", "-y", "-i", joined, "-f", "lavfi", "-i", f"color=c=0xE52E9E:s={W}x12:r=30", "-i", hookpng]
if MUSIC:
    cmd += ["-stream_loop", "-1", "-i", MUSIC]
    af = (f"[0:a]asplit=2[voice][key];"
          f"[3:a]atrim=0:{D:.2f},asetpts=PTS-STARTPTS,volume='if(gte(t,{D-3:.2f}),0.9,{LVL})':eval=frame,"
          f"afade=t=in:d=0.6,afade=t=out:st={D-1.2:.2f}:d=1.2[mus];"
          f"[mus][key]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=450:makeup=1[duck];"
          f"[voice][duck]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]")
    cmd += ["-filter_complex", vf + ";" + af, "-map", "[v]", "-map", "[a]", "-c:a", "aac", "-b:a", "192k"]
else:
    cmd += ["-filter_complex", vf, "-map", "[v]", "-map", "0:a", "-c:a", "copy"]
cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "21", OUT]
run(cmd)
print("OK", round(D, 1), "s ->", OUT)
