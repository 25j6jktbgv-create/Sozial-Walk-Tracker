#!/usr/bin/env python3
"""Erzeugt die Sozial-Walk-Installationsanleitung als einseitiges A4-PDF
im Design der Website (Teal/Orange, Hundetraining Susi Zednik)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

OUT = "Installationsanleitung.pdf"
APP_URL = "https://25j6jktbgv-create.github.io/Sozial-Walk-Tracker/"

TEAL   = HexColor("#15715E")
TEAL_D = HexColor("#0C5446")
TEAL_2 = HexColor("#2E9A7F")
ORANGE = HexColor("#F2954A")
CORAL  = HexColor("#EF6F53")
AMBER  = HexColor("#F5BF06")
INK    = HexColor("#15241F")
GRAY   = HexColor("#6E807A")
LIGHT  = HexColor("#F2EFE8")
GREEN  = HexColor("#34C759")
BLUE   = HexColor("#007AFF")
WHITE  = HexColor("#FFFFFF")

W, H = A4          # 595.27 x 841.89
M = 48

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Sozial Walk – Installationsanleitung")
c.setAuthor("Hundetraining Susi Zednik")
c.setSubject("So installierst du die Stempelkarten-App auf deinem iPhone")


def wrap(text, font, size, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if stringWidth(t, font, size) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def paw(cx, cy, s, col=WHITE, alpha=1.0):
    """Kleine Pfote, s = Skalierung."""
    c.saveState()
    c.setFillColor(col)
    c.setFillAlpha(alpha)
    c.ellipse(cx - 7.8*s, cy - 9*s, cx + 7.8*s, cy - 9*s + 12.8*s, stroke=0, fill=1)   # Ballen
    for dx, dy, rx, ry in [(-8.4, 6.4, 3.4, 4.2), (-2.6, 10.2, 3.2, 4.0),
                           (3.4, 10.2, 3.2, 4.0), (8.4, 6.4, 3.4, 4.2)]:
        c.ellipse(cx + (dx-rx)*s, cy + (dy-ry)*s, cx + (dx+rx)*s, cy + (dy+ry)*s, stroke=0, fill=1)
    c.restoreState()


# ---------- Kopfband (Teal-Verlauf) ----------
BAND_Y = 672
steps_grad = 60
for i in range(steps_grad):
    t = i / (steps_grad - 1)
    y0 = BAND_Y + (H - BAND_Y) * i / steps_grad
    r = TEAL_2.red + (TEAL_D.red - TEAL_2.red) * t
    g = TEAL_2.green + (TEAL_D.green - TEAL_2.green) * t
    b = TEAL_2.blue + (TEAL_D.blue - TEAL_2.blue) * t
    c.setFillColorRGB(r, g, b)
    c.rect(0, y0, W, (H - BAND_Y) / steps_grad + 1, stroke=0, fill=1)

# dezente Deko-Kreise / Pfoten aufs Band geclippt
c.saveState()
p = c.beginPath(); p.rect(0, BAND_Y, W, H - BAND_Y); c.clipPath(p, stroke=0, fill=0)
for (x, y, r, col, a) in [
    (95, 832, 46, WHITE, .07), (215, 690, 26, AMBER, .12),
    (330, 818, 20, WHITE, .09), (440, 686, 40, ORANGE, .12),
    (560, 806, 58, WHITE, .06),
]:
    c.setFillColor(col); c.setFillAlpha(a); c.circle(x, y, r, stroke=0, fill=1)
c.setFillAlpha(1)
paw(150, 700, 1.5, WHITE, .10)
paw(500, 730, 1.2, WHITE, .10)
c.restoreState()

# App-Icon rechts oben: weiße Kachel mit Teal-Pfote
ix, iy, isz = W - M - 70, 718, 70
c.setFillColor(WHITE); c.roundRect(ix, iy, isz, isz, 16, stroke=0, fill=1)
paw(ix + isz/2, iy + isz/2 - 4, 1.95, TEAL)

# Kopfband-Texte
c.setFillColor(WHITE); c.setFillAlpha(.9)
c.setFont("Helvetica-Bold", 9.5)
c.drawString(M, 792, "S O Z I A L   W A L K   ·   S T E M P E L K A R T E N")
c.setFillAlpha(1)
c.setFont("Helvetica-Bold", 27)
c.drawString(M, 758, "So installierst du")
c.drawString(M, 726, "deine Stempelkarten-App")
c.setFillAlpha(.92); c.setFont("Helvetica", 11.5)
c.drawString(M, 696, "In einer Minute auf dem Home-Bildschirm – ganz ohne App Store.")
c.setFillAlpha(1)

# ---------- Link-Box ----------
c.setFillColor(LIGHT); c.roundRect(M, 622, W - 2*M, 40, 12, stroke=0, fill=1)
c.setFillColor(TEAL); c.setFont("Helvetica-Bold", 11)
c.drawString(M + 18, 637, "App-Link:")
c.setFillColor(INK); c.setFont("Helvetica-Bold", 11)
c.drawString(M + 86, 637, APP_URL)

# ---------- Mini-Icons ----------
def icon_compass(x, y):
    c.setStrokeColor(BLUE); c.setLineWidth(2); c.circle(x, y, 11, stroke=1, fill=0)
    c.setFillColor(BLUE)
    p = c.beginPath(); p.moveTo(x+5, y+5); p.lineTo(x-1.5, y-1.5); p.lineTo(x-5, y-5); p.lineTo(x+1.5, y+1.5); p.close()
    c.drawPath(p, stroke=0, fill=1)

def icon_share(x, y):
    c.setStrokeColor(BLUE); c.setLineWidth(2); c.setLineCap(1); c.setLineJoin(1)
    c.roundRect(x-8, y-11, 16, 16, 3, stroke=1, fill=0)
    c.setFillColor(WHITE); c.rect(x-3.5, y+2.5, 7, 5, stroke=0, fill=1)
    c.setStrokeColor(BLUE)
    c.line(x, y-3, x, y+12); c.line(x, y+12, x-4, y+8); c.line(x, y+12, x+4, y+8)

def icon_plus(x, y):
    c.setStrokeColor(INK); c.setLineWidth(2); c.setLineCap(1)
    c.roundRect(x-10, y-10, 20, 20, 5, stroke=1, fill=0)
    c.line(x-4.5, y, x+4.5, y); c.line(x, y-4.5, x, y+4.5)

def icon_check(x, y):
    c.setFillColor(GREEN); c.circle(x, y, 11, stroke=0, fill=1)
    c.setStrokeColor(WHITE); c.setLineWidth(2.4); c.setLineCap(1); c.setLineJoin(1)
    c.line(x-5, y, x-1.5, y-4); c.line(x-1.5, y-4, x+5.5, y+4.5)

# ---------- Schritt-Karten ----------
c.setFillColor(TEAL); c.setFont("Helvetica-Bold", 12)
c.drawString(M, 594, "iPhone & iPad – Installation mit Safari")

steps = [
    ("Link in Safari öffnen",
     "Tippe den Link oben in die Adressleiste – wichtig: Safari verwenden, nicht Chrome.",
     icon_compass),
    ("Teilen-Symbol antippen",
     "Das Quadrat mit dem Pfeil nach oben, unten in der Mitte der Safari-Leiste.",
     icon_share),
    ("„Zum Home-Bildschirm“ wählen",
     "Im Teilen-Menü etwas nach unten scrollen, dann oben rechts mit „Hinzufügen“ bestätigen.",
     icon_plus),
    ("Fertig – einmal öffnen!",
     "Beim ersten Start kurz online sein, danach läuft die App auch komplett offline.",
     icon_check),
]

CARD_W, CARD_H, GAP = W - 2*M, 62, 10
top = 584
for i, (title, desc, icon) in enumerate(steps):
    cy0 = top - CARD_H - i * (CARD_H + GAP)
    mid = cy0 + CARD_H / 2
    c.setFillColor(LIGHT); c.roundRect(M, cy0, CARD_W, CARD_H, 12, stroke=0, fill=1)
    c.setFillColor(TEAL); c.circle(M + 28, mid, 13, stroke=0, fill=1)
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(M + 28, mid - 4.5, str(i + 1))
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 12)
    c.drawString(M + 52, cy0 + 36, title)
    c.setFillColor(GRAY); c.setFont("Helvetica", 10)
    for j, ln in enumerate(wrap(desc, "Helvetica", 10, CARD_W - 52 - 64)[:2]):
        c.drawString(M + 52, cy0 + 21 - j * 12, ln)
    icon(M + CARD_W - 30, mid)

# ---------- Untere Spalten ----------
COL_W = (CARD_W - 12) / 2
COL_H, COL_Y = 122, 146

def bullets(x0, y0, w, items, start_y):
    c.setFont("Helvetica", 9.5)
    yy = start_y
    for it in items:
        c.setFillColor(ORANGE); c.rect(x0 + 16, yy + 2.5, 4, 4, stroke=0, fill=1)
        c.setFillColor(GRAY); last = 0
        for j, ln in enumerate(wrap(it, "Helvetica", 9.5, w - 44)):
            c.drawString(x0 + 28, yy - j * 11.5, ln); last = j
        yy -= 11.5 * (last + 1) + 7

for (x0, head, items) in [
    (M, "Android & Desktop", [
        "Android (Chrome): Drei-Punkte-Menü öffnen und „App installieren“ bzw. „Zum Startbildschirm hinzufügen“ wählen.",
        "Desktop (Chrome/Edge): Installations-Symbol rechts in der Adressleiste anklicken.",
    ]),
    (M + COL_W + 12, "Gut zu wissen", [
        "Läuft komplett offline – ideal unterwegs.",
        "Alle Kundendaten bleiben auf deinem Gerät, kein Konto nötig.",
        "Updates meldet die App von selbst – einfach „Aktualisieren“ tippen.",
    ]),
]:
    c.setFillColor(LIGHT); c.roundRect(x0, COL_Y, COL_W, COL_H, 12, stroke=0, fill=1)
    c.setFillColor(TEAL); c.setFont("Helvetica-Bold", 11.5)
    c.drawString(x0 + 16, COL_Y + COL_H - 24, head)
    bullets(x0, COL_Y, COL_W, items, COL_Y + COL_H - 46)

# ---------- Fußzeile ----------
c.setStrokeColor(HexColor("#E5E0DC")); c.setLineWidth(1)
c.line(M, 108, W - M, 108)
c.setFillColor(GRAY); c.setFont("Helvetica", 9)
c.drawCentredString(W / 2, 88, "Sozial Walk · Stempelkarten · Version v1 · Stand: Juni 2026")
c.setFillColor(TEAL); c.setFont("Helvetica-Bold", 9)
c.drawCentredString(W / 2, 73, "Hundetraining Susi Zednik")

c.save()
print("OK ->", OUT)
