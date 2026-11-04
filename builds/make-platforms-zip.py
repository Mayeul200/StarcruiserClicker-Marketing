#!/usr/bin/env python3
"""Genere le zip PLATEFORMES (CrazyGames, Poki, GameJolt, Newgrounds, itch.io si besoin).

Patchs appliques UNIQUEMENT dans ce zip (le site officiel reste intact) :
1. index.html auto-redirige vers game.html (les plateformes lancent index.html,
   le jeu se charge direct dans l'iframe, meme origine).
2. Le bouton "Site officiel" (game.html + toutes les landings) est TOUJOURS
   visible (plus de display:none ni de detection de domaine) : le joueur
   voit en permanence le lien vers https://starcruiserclicker.com.

Usage : python3 builds/make-platforms-zip.py
"""
import os, re, subprocess, zipfile

JEU = '/workspace/github__Mayeul200__Starcruiser-Clicker'
DST = os.path.join(os.path.dirname(__file__), 'starcruiser-clicker-platforms.zip')
EXCLUDE = ('.git/', 'tools/', 'server/', 'out/', 'node_modules/', '.github/', 'README.md', '.gitignore')

REDIRECT = ("    <script>/* plateformes lancent index.html : on charge le jeu direct "
            "(meme iframe, meme origine) */location.replace('game.html');</script>\n")

def patch_html(name, data):
    s = data.decode('utf-8')
    # 1) redirect index.html -> game.html
    if name == 'index.html':
        anchor = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        if "location.replace('game.html')" not in s:
            s = s.replace(anchor, anchor + '\n' + REDIRECT, 1)
    # 2) bouton Site officiel toujours visible
    s = s.replace('id="official-site-btn" style="display:none"', 'id="official-site-btn"')
    # neutraliser la detection de domaine dans le script inline des landings
    s = re.sub(r'if \(!embedded\) return;', '/* embarque: bouton toujours visible */', s)
    return s.encode('utf-8')

def main():
    subprocess.run(['git', '-C', JEU, 'archive', '--format=zip', '-o', '/tmp/sc-raw.zip', 'HEAD'], check=True)
    with zipfile.ZipFile('/tmp/sc-raw.zip') as zin, zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if any(item.filename.startswith(e) or item.filename.endswith(e) for e in EXCLUDE):
                continue
            data = zin.read(item.filename)
            if item.filename.endswith('.html'):
                data = patch_html(item.filename, data)
            zout.writestr(item, data)
    # vérif
    z = zipfile.ZipFile(DST)
    g = z.read('game.html').decode('utf-8')
    i = z.read('index.html').decode('utf-8')
    print('zip genere:', DST, os.path.getsize(DST)//1024//1024, 'Mo')
    print('  redirect index->game:', "location.replace('game.html')" in i)
    print('  bouton visible permanent (game.html):', 'id="official-site-btn" style="display:none"' not in g)
    print('  bouton visible permanent (index.html):', 'id="official-site-btn" style="display:none"' not in i)

if __name__ == '__main__':
    main()
