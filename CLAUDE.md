# CLAUDE.md — Sozial Walk · Stempelkarten

Mini-Kundenverwaltung für **Hundetraining Susi Zednik**: pro Kunde eine digitale
Stempelkarte mit 5 Einheiten, um die Ausgabe von **Sozial-Walk-Gutscheinen** zu
überwachen. Single-File-**PWA**, läuft offline, installierbar aufs iPhone wie eine App.

## Aufbau

- `index.html` — die komplette App (HTML + CSS + JS, kein Build-Schritt)
- `sw.js` — Service Worker (Offline-Cache + Update-Flow)
- `manifest.json` — PWA-Manifest
- `icon.svg` / `apple-touch-icon.png` — App-Icons (Pfote auf Teal)
- `make_icon.py` — erzeugt `apple-touch-icon.png` (Pillow)
- `make_anleitung.py` — erzeugt `Installationsanleitung.pdf` (reportlab), Website-Look
- `Installationsanleitung.pdf` — fertige Anleitung zum Weitergeben

## Starten / Vorschau

Preview-Server `sozial-walk-tracker` (Port **8080**), siehe `../.claude/launch.json`.
Lieber `preview_start` mit dem Config-Namen nutzen als Server manuell starten.

## Wichtige Konventionen

- **Version bei jedem Deploy in ZWEI synchronen Stellen erhöhen:**
  `APP_VERSION` in `index.html` **und** `CACHE` in `sw.js` (aktuell `v1`).
  Eine Abweichung bricht das Service-Worker-Update.
- Bei einer neuen Version zusätzlich einen Eintrag oben in das `VERSIONS`-Array
  in `index.html` setzen (Versionsverlauf + „Was ist neu"). `CHANGES` zeigt immer
  auf den neuesten Eintrag.
- Datenmodell in `localStorage` unter Schlüssel `sozial-walk`:
  `{ v, pup, pin, customers:[{ id, name, dog, phone, note, stamps:[iso…], redeemed:[{date, stamps[]}] }] }`.
  `stamps` = aktuelle Karte (max 5); beim Einlösen wandert sie nach `redeemed` und die Karte wird geleert.
- PDF/Icon nach Inhaltsänderung neu erzeugen: `python3 make_icon.py && python3 make_anleitung.py`.

## Design (an Website hundetraining-susizednik.com angelehnt)

Teal/Waldgrün `#15715E` (Primär), Orange/Koralle `#F2954A` / `#EF6F53` (Akzente),
warmes Off-White `#F5F2EC`, Pfoten-Motiv. Große, fingerfreundliche Flächen für iPhone.

## Hosting

GitHub: `25j6jktbgv-create/Sozial-Walk-Tracker`. Geplante GitHub-Pages-URL:
`https://25j6jktbgv-create.github.io/Sozial-Walk-Tracker/` (Pages muss in den
Repo-Einstellungen auf Branch `main` aktiviert werden).
