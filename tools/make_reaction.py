"""Template « Réaction PIV » — ZONES SÛRES TikTok (corrigées 21/11, mesurées sur iPhone) : les écrans 19,5:9 ROGNENT ~110 px à gauche ET à droite. Tout texte doit tenir dans x 130→950 (largeur max 800, centré), y 230→1500 ; colonne d'icônes à droite : rien au-delà de x=930 entre y=1000 et 1700.
Template « Réaction PIV » (validé le 20/11/2026).
usage: python3 make_reaction.py spec.json out.mp4

spec.json :
{
  "hook": "Anyme vs GTA 6 🚨",            # 3-4 mots + 1 emoji, pastille blanche en haut
  "cam": [0, 0, 425, 300],                # x, y, w, h de la webcam dans la source 1920x1080
  "parts": [                              # 2-3 clips du même streamer, total >= 60 s
    {"src": "a.mp4",
     "subs": [[5.4, 8.6, "« Pardon, ", "pardon", " ! »"]],   # avant, MOT ROSE, après
     "emojis": [[9, 10.6, "😳"]],
     "pops": [[5.5, 7, "OUPS !"]],
     "bw": [[19.5, 24.5]]}                # noir et blanc sur les moments de désolation
  ]
}
Repères 1/3 2/3 3/3 calculés sur la durée totale ; outro endcard.py de 3 s ajoutée.
Option par part : "cut": [début, fin] en secondes (les temps des subs/emojis/pops sont alors RELATIFS au début du cut).
CLIP COURT : ajouter "short": true (15-25 s, 1 seule part, pas de repères, pas d'outro, couper juste avant la fin pour la boucle).
"""
import json, os, random, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
spec, out = json.load(open(sys.argv[1])), sys.argv[2]
# VARIATION OBLIGATOIRE (21/11) : chaque clip tire un style différent (palette, bulle, position de l'accroche, filet)
STYLES = [
  {"bubble": [255,255,255,255], "grad": [[123,63,228],[229,46,158],[255,61,168]], "line": "0xE52E9E", "tag": (123,63,228), "pink": (255,61,168), "hook_y": 230},
  {"bubble": [12,8,24,235], "grad": [[255,255,255],[255,200,240],[255,61,168]], "line": "0xFFFFFF", "tag": (229,46,158), "pink": (255,214,0), "hook_y": 230},
  {"bubble": [123,63,228,240], "grad": [[255,255,255],[255,255,255],[255,230,250]], "line": "0x7B3FE4", "tag": (20,20,30), "pink": (0,229,255), "hook_y": 900},
  {"bubble": [255,214,0,255], "grad": [[20,20,30],[60,20,80],[123,63,228]], "line": "0xFFD600", "tag": (229,46,158), "pink": (255,214,0), "hook_y": 230},
  {"bubble": [0,0,0,0], "grad": [[255,255,255],[255,255,255],[255,255,255]], "line": "0x00E5FF", "tag": (0,150,170), "pink": (0,229,255), "hook_y": 900},
]
ST = STYLES[spec["style"]] if "style" in spec else random.choice(STYLES)
os.environ["PIV_BUBBLE"] = json.dumps(ST["bubble"]); os.environ["PIV_GRAD"] = json.dumps(ST["grad"])
tmp = tempfile.mkdtemp()
fp = subprocess.run(["fc-match", "-f", "%{file}", "Inter:bold"], capture_output=True, text=True).stdout


def run(c): subprocess.run(c, check=True)


def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)


def sub_png(a, pink, b, path):
    parts = [(a, 0), (pink, 1), (b, 0)]; size = 46
    while True:
        f = ImageFont.truetype(fp, size); w = sum(f.getlength(t) for t, _ in parts) + 56
        if w <= 800 or size <= 30: break
        size -= 2
    im = Image.new("RGBA", (int(w), 84), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, 83], 18, fill=(0, 0, 0, 190)); x = 28
    for t, p in parts:
        d.text((x, 14), t, font=f, fill=ST["pink"] if p else (255, 255, 255)); x += f.getlength(t)
    im.save(path)


def chap_png(i, path):
    f = ImageFont.truetype(fp, 40); t = f"{i}/3"; w = int(f.getlength(t)) + 36
    im = Image.new("RGBA", (w, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, 63], 14, fill=ST["tag"]); d.text((18, 8), t, font=f, fill="white"); im.save(path)


hook = f"{tmp}/hook.png"; run(["python3", f"{HERE}/title_png.py", spec["hook"], hook, "800"])
for i in (1, 2, 3): chap_png(i, f"{tmp}/c{i}.png")
x, y, w, h = spec["cam"]
for k, p in enumerate(spec["parts"]):
    if p.get("cut"):
        a, b = p["cut"]; cutf = f"{tmp}/cut{k}.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", p["src"], "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", cutf]); p["src"] = cutf
total = sum(dur(p["src"]) for p in spec["parts"]); t0 = 0; pieces = []
for k, p in enumerate(spec["parts"]):
    d = dur(p["src"]); ins = ["-i", p["src"], "-loop", "1", "-i", hook]; ov = []
    for c in (() if spec.get("short") else (1, 2, 3)):
        a, b = total * (c - 1) / 3 - t0, total * c / 3 - t0
        if b > 0 and a < d:
            ins += ["-loop", "1", "-i", f"{tmp}/c{c}.png"]; ov.append(("130:800", max(a, 0), min(b, d)))
    for j, (a, b, s1, pk, s2) in enumerate(p.get("subs", [])):
        f = f"{tmp}/s{k}_{j}.png"; sub_png(s1, pk, s2, f); ins += ["-loop", "1", "-i", f]; ov.append(("(W-w)/2:660", a, b))
    for j, (a, b, e) in enumerate(p.get("emojis", [])):
        f = f"{tmp}/e{k}_{j}.png"; run(["python3", f"{HERE}/emoji_png.py", e, f, "210"]); ins += ["-loop", "1", "-i", f]; ov.append(("(W-w)/2:1150", a, b))
    for j, (a, b, t) in enumerate(p.get("pops", [])):
        f = f"{tmp}/p{k}_{j}.png"; run(["python3", f"{HERE}/title_png.py", t, f, "560"]); ins += ["-loop", "1", "-i", f]; ov.append(("(W-w)/2:1250", a, b))
    fc = (f"[0:v]split[a][b];[a]crop={w}:{h}:{x}:{y},scale=1080:762[cam];[b]scale=-2:1152,crop=1080:1152[game];"
          f"color=c={ST["line"]}:s=1080x6:d={d + 1}[line];[cam][line][game]vstack=3,fps=30,format=yuv420p,setsar=1[v0];")
    bw = "+".join(f"between(t,{a},{b})" for a, b in p.get("bw", []))
    fc += f"[v0]hue=s=0:enable='{bw}'[v1];" if bw else "[v0]null[v1];"
    fc += f"[v1][1:v]overlay=(W-w)/2:{ST['hook_y']}:shortest=1[v2];"; last = "v2"
    for n, (pos, a, b) in enumerate(ov):
        fc += f"[{last}][{n + 2}:v]overlay={pos}:enable='between(t,{a:.2f},{b:.2f})'[o{n}];"; last = f"o{n}"
    part = f"{tmp}/part{k}.mp4"; pieces.append(part)
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc.rstrip(";"), "-map", f"[{last}]", "-map", "0:a",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-c:a", "aac", "-ar", "48000", "-ac", "2", "-shortest", part])
    t0 += d
if not spec.get("short"):
  end = f"{tmp}/end.png"; run(["python3", f"{HERE}/endcard.py", end]); endv = f"{tmp}/end.mp4"; pieces.append(endv)
  run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", "3", "-i", end, "-f", "lavfi", "-t", "3", "-i", "anullsrc=r=48000:cl=stereo",
     "-vf", "scale=1080:1920,fps=30,format=yuv420p,setsar=1", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-c:a", "aac", "-shortest", endv])
n = len(pieces); args = sum((["-i", p] for p in pieces), [])
run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", "".join(f"[{i}:v][{i}:a]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]",
     "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-c:a", "aac", out])
print("OK", out, round(dur(out), 1), "s")
