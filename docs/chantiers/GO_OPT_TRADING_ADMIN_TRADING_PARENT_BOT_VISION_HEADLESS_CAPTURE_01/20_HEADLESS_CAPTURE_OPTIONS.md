---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01_OPTIONS
doc_type: options_comparison
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01
status: open
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 20_HEADLESS_CAPTURE_OPTIONS

## Option 1: ShareX (statut quo)

| Critere | Valeur |
| --- | --- |
| Machine | Windows/cursor-ai |
| Protocole | SFTP -> vision_inbox |
| Avantage | Deja en place, pas d'installation |
| Inconvenient | Windows-only, SFTP fragile, fichiers 0-byte |
| Viabilite | BASSE (produit final veut sortir de ShareX) |

## Option 2: Playwright + Chromium headless (RECOMMANDE)

| Critere | Valeur |
| --- | --- |
| Machine | admin-trading (autonome) |
| Outils | Node.js 18.20.4 + npm -> playwright + chromium |
| Capture | page.screenshot() -> fichier local -> atomic write -> vision_inbox |
| Avantage | Cross-platform, mature, screenshots full-page/selector, pas de SFTP |
| Inconvenient | Installation chromium (~300 MB), memoire ~150 MB par instance |
| Complexite | MOYENNE |
| Viabilite | HAUTE (Node deja present, npm dispo) |

## Option 3: Xvfb + browser (alternative Linux)

| Critere | Valeur |
| --- | --- |
| Machine | admin-trading |
| Outils | Xvfb + chromium-browser ou google-chrome |
| Capture | xvfb-run chromium --headless --screenshot |
| Avantage | Pas de Node/Playwright requis |
| Inconvenient | Xvfb absent, chromium-browser absent, complexite display virtuel |
| Complexite | ELEVEE (Xvfb + display + browser) |
| Viabilite | MOYENNE |

## Option 4: ffmpeg/scrot/maim

| Critere | Valeur |
| --- | --- |
| Machine | admin-trading |
| Outils | ffmpeg, scrot, maim |
| Capture | Capture d'ecran locale X11 |
| Avantage | Leger, natif Linux |
| Inconvenient | Necessite display X11 actif, pas headless |
| Viabilite | BASSE (admin-trading est headless, pas de display) |

## Option 5: Hybride Playwright + atomique

| Critere | Valeur |
| --- | --- |
| Combinaison | Playwright pour capture + script wrapper pour ecriture atomique |
| Atomicite | Ecrire .uploading -> mv vers .png final |
| Garde-fou | Verifier taille > 0 avant mv |
| Complexite | MOYENNE |
| Viabilite | HAUTE (recommande) |

## Recommandation

**Option 5 (Hybride Playwright + atomique)**:
- Playwright/Chromium pour la capture headless
- Script wrapper Node.js pour l'ecriture atomique (uploading -> rename)
- Garde-fou anti 0-byte integre
- Systemd timer pour declenchement periodique
- Sortie directe vers vision_inbox
- Aucun SFTP, aucun Windows requis
