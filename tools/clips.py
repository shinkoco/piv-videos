"""Top viewer-made Twitch clips of GTA VI for the streamers in streamers.json
(works even when VODs are subscriber-only).
usage: python3 clips.py [LAST_DAY|LAST_WEEK] [game substring]  -> JSON lines
"""
import json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(HERE, "streamers.json")))
period = sys.argv[1] if len(sys.argv) > 1 else "LAST_DAY"
game = (sys.argv[2] if len(sys.argv) > 2 else "Grand Theft Auto VI").lower()
H = {"Client-ID": "kd1unb4b3q4t58fwlpcbzcbnm76a8fp", "Content-Type": "application/json"}
Q = ("query($l:String!,$p:ClipsPeriod){user(login:$l){clips(first:20,criteria:{period:$p,sort:VIEWS_DESC})"
     "{edges{node{slug title viewCount durationSeconds createdAt game{name} url}}}}}")
for s in cfg["streamers"]:
    if s["platform"] != "twitch" or s["login"] in cfg.get("blocked", []):
        continue
    body = json.dumps({"query": Q, "variables": {"l": s["login"], "p": period}}).encode()
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request("https://gql.twitch.tv/gql", body, H), timeout=20))
        edges = r["data"]["user"]["clips"]["edges"]
    except Exception as e:
        print(json.dumps({"streamer": s["name"], "error": str(e)}), file=sys.stderr)
        continue
    for e in edges:
        n = e["node"]
        if game not in ((n.get("game") or {}).get("name") or "").lower():
            continue
        print(json.dumps({"streamer": s["name"], "login": s["login"], "lang": s["lang"], "cam": s["cam"],
                          "title": n["title"], "views": n["viewCount"], "duration": n["durationSeconds"],
                          "created": n["createdAt"], "url": n["url"]}, ensure_ascii=False))
