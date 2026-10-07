import re, json, urllib.request, urllib.parse
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36", "Accept": "*/*"}
AUD = re.compile(r'["\'(`]([^"\'()`\s<>]+\.(?:mp3|m4a|ogg|wav|aac|webm|opus))', re.I)
def get(url, ua=UA):
    req = urllib.request.Request(url, headers=ua)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")
print("=== PART A: arabicquick audio discovery")
for page in ["https://arabicquick.com/alphabet-chart", "https://arabicquick.com/learn/ba"]:
    try:
        html = get(page)
        print(page, "len", len(html))
        found = sorted(set(AUD.findall(html)))
        print(" audio refs in html:", len(found)); [print("  ", f) for f in found[:40]]
        for m in list(re.finditer(r'data-(?:audio|src|sound)[^=]*=["\']([^"\']+)', html))[:15]:
            print("  data-attr:", m.group(0)[:160])
        scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)', html)
        print(" scripts:", scripts[:15])
        for sc in scripts[:15]:
            u = urllib.parse.urljoin(page, sc)
            try:
                js = get(u)
                fj = sorted(set(AUD.findall(js)))
                ctx = [js[max(0, m.start()-80):m.end()+120].replace("\n", " ") for m in re.finditer(r'audio', js)][:6]
                print("  JS", u, len(js), "audio refs:", fj[:20])
                for c in ctx: print("     ctx:", c)
            except Exception as e:
                print("  JS fail", u, e)
        for m in list(re.finditer(r'audio', html))[:8]:
            print("  html ctx:", html[max(0, m.start()-100):m.end()+160].replace("\n", " "))
    except Exception as e:
        print("FAIL", page, e)
print("=== PART B: Wikimedia Commons Lingua Libre")
WUA = {"User-Agent": "huruf-personal-learning-app/1.0 (personal use; github.com/artus25200/huruf-)"}
words = "أسد بيت تفاح ثعلب جمل حليب خبز درس ذهب رجل زهرة سمك شمس صباح ضوء طاولة ظل عين غابة فيل قمر كتاب ليل ماء نجم هلال وردة يد".split()
for w in words:
    q = urllib.parse.urlencode({"action": "query", "list": "search", "srnamespace": 6, "srlimit": 15, "format": "json", "srsearch": "LL-Q13955 " + w})
    try:
        d = json.loads(get("https://commons.wikimedia.org/w/api.php?" + q, WUA))
        titles = [x["title"] for x in d["query"]["search"] if x["title"].endswith("-" + w + ".wav") or x["title"].endswith("-" + w + ".ogg") or x["title"].endswith("-" + w + ".mp3")]
        print(w, "->", titles[:3] if titles else "MISS (%d hits)" % len(d["query"]["search"]))
    except Exception as e:
        print(w, "ERR", e)
