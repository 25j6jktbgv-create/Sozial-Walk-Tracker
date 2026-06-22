#!/usr/bin/env python3
"""Erzeugt die App-Icons aus dem runden Website-Logo (logo-src.png):
- apple-touch-icon.png (180) : vollflächige Beeren-Kachel mit Logo (iOS rundet selbst)
- icon-512.png (512)         : maskable Variante fürs PWA-Manifest
- logo.png (256)             : rundes Logo mit transparenten Ecken für den App-Header
"""
from PIL import Image

BERRY = (124, 52, 71)          # #7C3447 – Grundfarbe aus dem Logo
SRC = "logo-src.png"

src = Image.open(SRC).convert("RGBA")

def tile(size, scale=1.08):
    """Vollflächige Beeren-Kachel mit dem echten Logo in Originalproportion
    (der Kreisrand läuft nahtlos in die gleichfarbige Kachel; iOS rundet selbst)."""
    canvas = Image.new("RGBA", (size, size), BERRY + (255,))
    s = int(size * scale)
    logo = src.resize((s, s), Image.LANCZOS)
    off = (size - s) // 2
    canvas.alpha_composite(logo, (off, off))
    return canvas.convert("RGB")

tile(180).save("apple-touch-icon.png")
tile(512).save("icon-512.png")

# Rundes Logo (transparente Ecken) für den Header in der App
src.resize((256, 256), Image.LANCZOS).save("logo.png")

print("OK -> apple-touch-icon.png, icon-512.png, logo.png")
