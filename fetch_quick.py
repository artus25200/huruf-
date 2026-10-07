import re, json, os, time, urllib.request, urllib.parse
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36", "Accept": "*/*"}
BASE = "https://arabicquick.com"
IDS = ["alif","ba","ta","tha","jeem","hha","kha","dal","thal","ra","zay","seen","sheen","saad","daad","toh","thoh","ayn","ghayn","fa","qaf","kaf","lam","meem","noon","ha","wow","ya"]
def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        d = r.read()
    time.sleep(0.12)
    return d if binary else d.decode("utf-8", "replace")
def dl(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    data = get(urllib.parse.quote(url, safe=":/%"), True)
    if len(data) < 500: raise Exception("too small %d" % len(data))
    open(dest, "wb").write(data)
manifest, log = {}, []
ok = fail = 0
for sid in IDS:
    words = []
    try:
        html = get(f"{BASE}/learn/{sid}").replace('\\"', '"')
        for m in re.finditer(r'\{[^{}]*"audio":"(/sample-words/audio/[^"]+)"[^{}]*\}', html):
            try: o = json.loads(m.group(0))
            except Exception: continue
            w = {"a": o.get("arabic"), "e": o.get("english"), "f": o["audio"].replace("/sample-words/audio/", "")}
            if w not in words: words.append(w)
    except Exception as e:
        log.append(f"PAGE FAIL {sid} {e}")
    manifest[sid] = words
    for suf in ["", "-fatha", "-damma", "-kasra"]:
        n = sid + suf
        try: dl(f"{BASE}/audio/{n}.mp3", f"audio/q/{n}.mp3"); ok += 1
        except Exception as e: fail += 1; log.append(f"FAIL audio/{n}.mp3 {e}")
    for w in words:
        try: dl(f"{BASE}/sample-words/audio/{w['f']}", f"audio/qw/{w['f']}"); ok += 1
        except Exception as e: fail += 1; log.append(f"FAIL word {w['f']} {e}")
json.dump(manifest, open("quick_manifest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
log.append(f"DONE ok={ok} fail={fail} words={sum(len(v) for v in manifest.values())}")
open("quick_log.txt", "w", encoding="utf-8").write("\n".join(log))
print("\n".join(log))
