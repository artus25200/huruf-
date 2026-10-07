import re, json, time, urllib.request, urllib.parse
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36", "Accept": "*/*"}
def get(url, ua=UA):
    req = urllib.request.Request(url, headers=ua)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")
print("=== A: arabicquick links about numbers")
for page in ["https://arabicquick.com/", "https://arabicquick.com/sitemap.xml", "https://arabicquick.com/alphabet-chart"]:
    try:
        h = get(page).replace('\\"', '"')
        hrefs = sorted(set(re.findall(r'(?:href|loc)["=>\s]+"?(?:https://arabicquick\.com)?(/[^"\s<>]*|[^"\s<>]*number[^"\s<>]*)', h)))
        print(page, len(h), "links:", len(hrefs))
        for x in hrefs:
            if re.search(r'number|count|digit|num', x, re.I): print("  NUM:", x)
        print("  sample links:", hrefs[:40])
    except Exception as e:
        print("FAIL", page, e)
print("=== B: guess number pages")
for u in ["/numbers", "/learn/numbers", "/learn/number", "/arabic-numbers", "/numbers-chart", "/learn/numbers-0-10", "/vocabulary/numbers", "/learn/vocabulary/numbers"]:
    try:
        h = get("https://arabicquick.com" + u)
        aud = sorted(set(re.findall(r'["\'(`]([^"\'()`\s<>]+\.(?:mp3|m4a|ogg|wav))', h.replace('\\"', '"'))))
        print("OK", u, len(h), aud[:20])
    except Exception as e:
        print("no", u, str(e)[:40])
print("=== C: Wikimedia Commons (slow, polite)")
WUA = {"User-Agent": "huruf-personal-learning-app/1.0 (personal use; github.com/artus25200/huruf-)"}
words = "صفر واحد اثنان ثلاثة أربعة خمسة ستة سبعة ثمانية تسعة عشرة".split()
for w in words:
    time.sleep(2.5)
    q = urllib.parse.urlencode({"action": "query", "list": "search", "srnamespace": 6, "srlimit": 30, "format": "json", "srsearch": "LL-Q13955 " + w})
    try:
        d = json.loads(get("https://commons.wikimedia.org/w/api.php?" + q, WUA))
        titles = [x["title"] for x in d["query"]["search"] if re.search(r"-" + re.escape(w) + r"\.(wav|ogg|mp3|flac)$", x["title"])]
        print(w, "->", titles[:3] if titles else "MISS (%d hits)" % len(d["query"]["search"]))
    except Exception as e:
        print(w, "ERR", str(e)[:60])
