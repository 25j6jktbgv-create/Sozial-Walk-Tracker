#!/usr/bin/env python3
"""Erzeugt die App-Icons aus dem runden Website-Logo (logo-src.png).
Das runde Beeren-Logo mit der weißen Hunde-Silhouette wird auf eine weiße Kachel
gesetzt, damit die Silhouette auch als kleines App-Icon klar sichtbar bleibt.
- apple-touch-icon.png (180) : weiße Kachel, Logo zentriert (iOS rundet selbst)
- icon-512.png (512)         : maskable Variante (Logo im sicheren Mittelbereich)
- logo.png (256)             : rundes Logo mit transparenten Ecken für den App-Header
"""
from PIL import Image

WHITE = (255, 255, 255)
SRC = "logo-src.png"
src = Image.open(SRC).convert("RGBA")


def tile(size, scale):
    """Weiße Kachel mit zentriertem runden Logo (Hunde-Silhouette sichtbar)."""
    canvas = Image.new("RGBA", (size, size), WHITE + (255,))
    s = int(size * scale)
    logo = src.resize((s, s), Image.LANCZOS)
    off = (size - s) // 2
    canvas.alpha_composite(logo, (off, off))
    return canvas.convert("RGB")


tile(180, 0.92).save("apple-touch-icon.png")     # iOS Home-Bildschirm
tile(512, 0.78).save("icon-512.png")             # maskable: Logo im 80%-Sicherheitsbereich

# Rundes Logo (transparente Ecken) für den Header in der App
src.resize((256, 256), Image.LANCZOS).save("logo.png")

print("OK -> apple-touch-icon.png, icon-512.png, logo.png")
