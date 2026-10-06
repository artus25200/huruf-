#!/usr/bin/env python3
"""Télécharge les sons des 28 lettres dans un dossier 'audio' à côté de ce script.
Place ce script dans le même dossier que huruf.html, puis lance :  python3 download_audio.py
Pour usage personnel uniquement."""
import os, sys, urllib.request

BASE = "https://www.arabicreadingcourse.com/"
SLUGS = ["alif","ba","ta","tha","jiim","hha","kha","daal","thaal","ra","zay","siin","shiin",
         "saad","daad","taa","thaa","ayn","ghayn","fa","qaf","kaf","lam","miim","nuun","ha","waw","ya"]
here = os.path.dirname(os.path.abspath(__file__))
ok = fail = 0
for kind in ("audio/isolated-letters/", "audio/"):
    os.makedirs(os.path.join(here, kind), exist_ok=True)
    for s in SLUGS:
        rel = f"{kind}{s}.mp3"
        dest = os.path.join(here, rel)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            ok += 1
            continue
        try:
            req = urllib.request.Request(BASE + rel, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as f:
                f.write(r.read())
            ok += 1
        except Exception as e:
            fail += 1
            print(f"Échec : {rel} ({e})", file=sys.stderr)
print(f"Terminé : {ok} fichiers présents, {fail} échecs.")
