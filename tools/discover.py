"""List recent GTA VODs for the streamers in streamers.json.
usage: python3 discover.py [max_age_hours]   -> prints JSON lines
"""
import json, subprocess, sys, os, time

HERE = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(HERE, "streamers.json")))
max_age = float(sys.argv[1]) if len(sys.argv) > 1 else 36
now = time.time()
for s in cfg["streamers"]:
    if s["login"] in cfg.get("blocked", []):
        continue
    url = (f"https://www.twitch.tv/{s['login']}/videos?filter=archives" if s["platform"] == "twitch"
           else f"https://kick.com/{s['login']}/videos")
    r = subprocess.run(["yt-dlp", "--no-warnings", "--playlist-items", "1:3", "--print",
                        "%(id)s\t%(title)s\t%(duration)s\t%(timestamp)s\t%(webpage_url)s", url],
                       capture_output=True, text=True, timeout=180)
    for line in r.stdout.strip().splitlines():
        try:
            vid, title, dur, ts, wurl = line.split("\t")
        except ValueError:
            continue
        age = (now - float(ts)) / 3600 if ts not in ("NA", "") else None
        if "gta" not in title.lower():
            continue
        if age is not None and age > max_age:
            continue
        print(json.dumps({"streamer": s["name"], "login": s["login"], "platform": s["platform"],
                          "lang": s["lang"], "cam": s["cam"], "id": vid, "title": title,
                          "duration": dur, "age_h": round(age, 1) if age else None, "url": wurl},
                         ensure_ascii=False))
    if r.returncode and not r.stdout:
        print(json.dumps({"streamer": s["name"], "error": r.stderr.strip()[-300:]}), file=sys.stderr)
