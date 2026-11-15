"""Fetch Twitch VOD chat replay counts per second between start/end offsets.
usage: python3 chat.py VOD_ID START END OUT.json
"""
import json, sys, urllib.request

vod, start, end, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
H = {"Client-ID": "kd1unb4b3q4t58fwlpcbzcbnm76a8fp", "Content-Type": "application/json"}
Q = "query($id:ID!,$o:Int){video(id:$id){comments(contentOffsetSeconds:$o){edges{node{contentOffsetSeconds message{fragments{text}}}}pageInfo{hasNextPage}}}}"
counts, msgs = {}, []
o = start
while o < end:
    body = json.dumps({"query": Q, "variables": {"id": vod, "o": o}}).encode()
    r = json.load(urllib.request.urlopen(urllib.request.Request("https://gql.twitch.tv/gql", body, H), timeout=20))
    edges = r["data"]["video"]["comments"]["edges"]
    if not edges:
        o += 5
        continue
    last = o
    for e in edges:
        t = e["node"]["contentOffsetSeconds"]
        if t >= end:
            break
        counts[t] = counts.get(t, 0) + 1
        txt = "".join(f["text"] for f in e["node"]["message"]["fragments"])
        msgs.append([t, txt])
        last = t
    o = max(last + 1, o + 1)
json.dump({"counts": counts, "msgs": msgs}, open(out, "w"))
print(len(msgs), "messages")
