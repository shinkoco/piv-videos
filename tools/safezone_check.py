"""usage: python3 safezone_check.py video.mp4 secondes out.jpg — exporte une image avec le cadre des zones sûres TikTok (vert = autorisé)."""
import subprocess, sys
v, t, out = sys.argv[1:4]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", t, "-i", v, "-frames:v", "1", "-vf",
  "drawbox=x=130:y=230:w=820:h=1270:color=lime@0.9:t=4,drawbox=x=930:y=1000:w=150:h=700:color=red@0.5:t=fill,scale=540:-1", out], check=True)
print("OK", out)
