#!/usr/bin/env python3
"""Genere le zip SPECIAL itch.io : le joueur tombe sur la landing (index.html),
et le bouton JOUER de cette landing renvoie sur le site officiel en nouvel onglet.

Ne modifie PAS le depot du jeu : le patch est applique uniquement dans le zip.
Usage : python3 builds/make-itch-zip.py
"""
import io, os, re, subprocess, zipfile

JEU = '/workspace/github__Mayeul200__Starcruiser-Clicker'
DST = os.path.join(os.path.dirname(__file__), 'starcruiser-clicker-itch.zip')
OFFICIAL = 'https://starcruiserclicker.com/game.html?utm_source=itchio'
EXCLUDE = ('.git/', 'tools/', 'server/', 'out/', 'node_modules/', '.github/', 'README.md', '.gitignore')

def main():
    subprocess.run(['git', '-C', JEU, 'archive', '--format=zip', '-o', '/tmp/sc-src.zip', 'HEAD'], check=True)
    with zipfile.ZipFile('/tmp/sc-src.zip') as zin, zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if any(item.filename.startswith(e) or item.filename.endswith(e) for e in EXCLUDE):
                continue
            data = zin.read(item.filename)
            # Patch UNIQUEMENT la landing : les liens vers game.html deviennent le site officiel (nouvel onglet)
            if item.filename == 'index.html':
                s = data.decode('utf-8')
                s = re.sub(r'href="game\.html"',
                           f'href="{OFFICIAL}" target="_blank" rel="noopener"', s)
                data = s.encode('utf-8')
            zout.writestr(item, data)
    print('zip itch special genere :', DST, os.path.getsize(DST) // 1024 // 1024, 'Mo')

if __name__ == '__main__':
    main()
