#!/usr/bin/env python3
"""Erzeugt das apple-touch-icon.png (180x180) – Teal-Kachel mit weißer Pfote."""
from PIL import Image, ImageDraw

SZ = 180
SS = 4                      # Supersampling für glatte Kanten
W = SZ * SS
img = Image.new("RGB", (W, W), "#15715E")
d = ImageDraw.Draw(img)

# Sanfter Diagonal-Verlauf Teal -> dunkles Teal
top = (46, 154, 127)       # #2E9A7F
bot = (12, 84, 70)         # #0C5446
for y in range(W):
    t = y / W
    r = int(top[0] + (bot[0]-top[0]) * t)
    g = int(top[1] + (bot[1]-top[1]) * t)
    b = int(top[2] + (bot[2]-top[2]) * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))


def paw(cx, cy, rx, ry):
    d.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], fill="white")


# Pfote (an icon.svg angelehnt), zentriert & leicht nach oben
S = SS
ox, oy = 0, -6 * S
paw(256*S+ox, 300*S+oy, 78*S, 64*S)        # Ballen
paw(168*S+ox, 232*S+oy, 34*S, 42*S)        # Zehen
paw(232*S+ox, 190*S+oy, 32*S, 40*S)
paw(304*S+ox, 190*S+oy, 32*S, 40*S)
paw(356*S+ox, 232*S+oy, 34*S, 42*S)

img = img.resize((SZ, SZ), Image.LANCZOS)
img.save("apple-touch-icon.png")
print("OK -> apple-touch-icon.png")
