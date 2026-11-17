#!/usr/bin/env python3
"""Turn carousel slides (1080x1350 JPGs) into a 9:16 slideshow video with our music.

Usage: python3 make_slideshow.py OUT.mp4 MUSIC.wav BPM slide1.jpg slide2.jpg ...
Each slide lasts 6 beats, with a slow zoom over a blurred background; the music fades out at the end.
"""
import subprocess, sys

out, music, bpm = sys.argv[1], sys.argv[2], float(sys.argv[3])
slides = sys.argv[4:]
d = round(6 * 60 / bpm, 3)
total = d * len(slides)
inputs, parts = [], []
for i, s in enumerate(slides):
    inputs += ["-loop", "1", "-t", str(d), "-i", s]
    fr = int(d * 30)
    parts.append(
        f"[{i}:v]split=2[b{i}][f{i}];"
        f"[b{i}]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.15[bb{i}];"
        f"[f{i}]scale=1080:-2,zoompan=z='1+0.04*on/{fr}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1350:fps=30[ff{i}];"
        f"[bb{i}][ff{i}]overlay=0:285,format=yuv420p,setsar=1[v{i}]"
    )
n = len(slides)
fc = ";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v];"
fc += f"[{n}:a]atrim=0:{total},afade=t=in:d=0.5,afade=t=out:st={total-1.5}:d=1.5,volume=0.8[a]"
cmd = ["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", music,
       "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-r", "30",
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
       "-t", str(total), "-movflags", "+faststart", out]
subprocess.run(cmd, check=True)
print("OK", total, out)
