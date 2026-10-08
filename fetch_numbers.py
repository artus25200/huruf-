import os, re, json, time, subprocess, urllib.request, urllib.parse, urllib.error
WUA = {"User-Agent": "huruf-personal-learning-app/1.0 (personal use; github.com/artus25200/huruf-)"}
NUMS = [("0","صفر"),("1","واحد"),("2","اثنان"),("3","ثلاثة"),("4","أربعة"),("5","خمسة"),("6","ستة"),("7","سبعة"),("8","ثمانية"),("9","تسعة"),("10","عشرة")]
PREF = ["Zinou2go", "Ov3for"]
log = []
def get(url, binary=False):
    for attempt in range(5):
        time.sleep(6)
        try:
            req = urllib.request.Request(url, headers=WUA)
            with urllib.request.urlopen(req, timeout=60) as r:
                d = r.read()
            return d if binary else d.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 4:
                log.append(f"429, retry {attempt+1}"); time.sleep(20 * (attempt + 1)); continue
            raise
os.makedirs("audio/nums", exist_ok=True)
for n, w in NUMS:
    if os.path.exists(f'audio/nums/{n}.mp3'):
        log.append(f'skip {n} (already there)'); continue
    try:
        q = urllib.parse.urlencode({"action": "query", "list": "search", "srnamespace": 6, "srlimit": 30, "format": "json", "srsearch": "LL-Q13955 " + w})
        d = json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))
        titles = [x["title"] for x in d["query"]["search"] if re.search(r"-" + re.escape(w) + r"\.(wav|ogg|mp3|flac)$", x["title"])]
        pick = next((t for s in PREF for t in titles if f"-{s}-" in t), titles[0] if titles else None)
        if not pick: log.append(f"MISS {n} {w}"); continue
        url = "https://commons.wikimedia.org/wiki/Special:FilePath/" + urllib.parse.quote(pick[len("File:"):])
        raw = get(url, True)
        ext = pick.rsplit(".", 1)[1]
        tmp = f"/tmp/num{n}.{ext}"
        open(tmp, "wb").write(raw)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-ac", "1", "-ar", "44100", "-b:a", "64k", f"audio/nums/{n}.mp3"], check=True)
        log.append(f"ok {n} {w} <- {pick} ({len(raw)} bytes) -> {os.path.getsize(f'audio/nums/{n}.mp3')} bytes")
    except Exception as e:
        log.append(f"FAIL {n} {w} {e}")
log.append("DONE")
open("nums_log.txt", "w", encoding="utf-8").write("\n".join(log))
print("\n".join(log))
