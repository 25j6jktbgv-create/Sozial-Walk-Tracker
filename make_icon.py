#!/usr/bin/env python3
"""Erzeugt die App-Icons aus dem runden Website-Logo (logo-src.png).

Im Logo ist der Hund eine AUSGESTANZTE (transparente) Silhouette in einer beerenroten
Scheibe – nicht weiß gefärbt. Auf beerenrotem Grund verschwindet er also. Lösung:
Hund freistellen und groß & weiß auf eine durchgehend beerenrote Kachel malen
(keine weißen Ecken) -> Silhouette klar sichtbar, auch als kleines App-Icon.

- apple-touch-icon.png (180) : beerenrote Kachel, große weiße Hunde-Silhouette
- icon-512.png (512)         : dasselbe in 512 (maskable)
- logo.png (256)             : rundes Logo (für den App-Header auf weißem Kreis)
"""
from PIL import Image, ImageDraw, ImageChops

BERRY = (124, 52, 71)            # #7C3447
src = Image.open("logo-src.png").convert("RGBA")
W, H = src.size

# 1) Logo auf Weiß -> Hund wird weiß, Scheibe bleibt beere
comp = Image.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, 255)), src).convert("RGB")
L = comp.convert("L")

# 2) Kreis-Maske der Scheibe (schließt die weißen Ecken aus)
berry_mask = L.point(lambda v: 255 if 55 <= v <= 105 else 0)
bb = berry_mask.getbbox()
cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
R = min(bb[2] - bb[0], bb[3] - bb[1]) / 2
circle = Image.new("L", (W, H), 0)
ImageDraw.Draw(circle).ellipse([cx - R + 6, cy - R + 6, cx + R - 6, cy + R - 6], fill=255)

# 3) Weiche Hund-Maske (Anti-Aliasing erhalten), nur innerhalb der Scheibe
white_ramp = L.point(lambda v: 0 if v < 150 else min(255, int((v - 150) * 4)))
dog_mask = ImageChops.multiply(white_ramp, circle)

# 4) Durchgehend beere, Hund weiß einmalen -> keine weißen Ecken
full = Image.new("RGB", (W, H), BERRY)
full.paste(Image.new("RGB", (W, H), (255, 255, 255)), (0, 0), dog_mask)

db = dog_mask.getbbox()
pad = int(max(db[2] - db[0], db[3] - db[1]) * 0.12)
crop = full.crop((max(0, db[0] - pad), max(0, db[1] - pad),
                  min(W, db[2] + pad), min(H, db[3] + pad)))


def tile(size, frac):
    canvas = Image.new("RGB", (size, size), BERRY)
    target = int(size * frac)
    cw, ch = crop.size
    sc = target / max(cw, ch)
    r = crop.resize((max(1, int(cw * sc)), max(1, int(ch * sc))), Image.LANCZOS)
    canvas.paste(r, ((size - r.size[0]) // 2, (size - r.size[1]) // 2))
    return canvas


tile(180, 0.78).save("apple-touch-icon.png")
tile(512, 0.74).save("icon-512.png")
src.resize((256, 256), Image.LANCZOS).save("logo.png")   # Header (auf weißem Kreis)
print("OK -> dog bbox", db, "| apple-touch-icon.png, icon-512.png, logo.png")
