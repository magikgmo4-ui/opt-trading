# PROJECT_CARD_BOT_VISION_INGESTION_01

Date: 2026-04-14

## 1. Objet

Figer une fiche compacte de reprise pour Bot Vision / ingestion desk, afin de rendre retrouvables en un seul point:
- le but final retenu;
- le plan validé;
- l’état établi;
- le non établi;
- le point de reprise.

Cette fiche agrège volontairement:
- les artefacts repo déjà présents;
- la continuité validée en séance quand le plan suivi n’existe pas encore comme doc source unique.

Elle ne remplace pas les closings, rapports machine ni scripts runtime détaillés.

## 2. But final

Construire une chaîne opératoire de vision desk qui transforme:
- une capture écran Desk Pro côté Windows;
- en fichier transféré et vérifié côté Linux;
- puis en snapshots desk structurés et `latest.json`;
- puis en sortie exploitable par `/analyze` via photo + texte utile.

L’objectif n’est pas seulement d’envoyer une image Telegram, mais de disposer d’une chaîne stable allant de la capture jusqu’à une entrée desk structurée consommable par l’analyse.

## 3. Plan validé

1. Obtenir une capture opératoire simple et répétable côté Windows via ShareX.
2. Fiabiliser la chaîne de transit Windows -> Linux avec timeouts, vérification et absence de zombies.
3. Alimenter un inbox / processed côté Linux puis déclencher un bridge de découpe / ingestion.
4. Produire des snapshots desk structurés et un `latest.json` unique.
5. Faire consommer ce `latest.json` par `/analyze` pour renvoyer une photo fraîche et un texte utile.
6. Enrichir ensuite prudemment le texte d’analyse avec des données réelles sans rouvrir toute la chaîne.

## 4. ETABLI

- Une note `ETABLI_BOT_VISION` fixe déjà des faits prouvés sur la chaîne complète.
- `bot_vision_step2` tourne sur `admin-trading` via systemd, poll Telegram et accepte un `chat_id` allowlisté.
- `/analyze` envoie une photo JPEG récente et un texte basé sur `desk_analyze/analyze_latest.py` alimenté par `latest.json`.
- La chaîne Windows est établie comme:
  - ShareX AutoCapture;
  - `sharex_action_chain.bat`;
  - `send_vision_inbox.ps1`;
  - SCP/SSH vers `admin-trading`.
- Le bridge Linux est établi avec `bridge_vision_to_desk_inbox.sh`, crop en quadrants, alimentation snapshots desk puis mise à jour de `latest.json` via ingestion.
- `desk_bridge.timer` est établi comme timer systemd actif.
- Un closeout final a retenu un verdict global PASS sur la chaîne bout-en-bout Bot Vision.
- Un closeout plus récent `OT_BOT_VISION_REAL_DATA_01_CLOSING.txt` a établi un enrichissement réel du texte d’analyse dans `analyze_latest.py`, remplaçant des placeholders par:
  - présence image runtime;
  - données Binance Futures publiques pour les perps crypto supportés;
  - fallback explicite pour les symboles non supportés comme `XAUUSD`.

## 5. NON ETABLI

- Il n’existe pas encore, dans une fiche courte unique avant celle-ci, une vue programme consolidée résumant la chaîne complète capture -> transfert -> bridge -> latest.json -> /analyze.
- La chaîne n’est pas encore accompagnée ici d’une couche de monitoring / alerting figée pour les arrêts AutoCapture, timeouts SCP/SSH ou retard d’ingestion.
- L’enrichissement market réel de `analyze_latest.py` reste partiel:
  - pas d’intégration Coinglass API prouvée dans cette V1;
  - pas de données liquidation robustes en V1;
  - pas de support market externe complet pour `XAUUSD`.
- Cette fiche ne remplace pas les preuves runtime machine par machine.

## 6. Reprise

### GO porteur
`GO_PROJECT_CARDS_FREEZE_01`

### Point de reprise Bot Vision / ingestion
Par défaut, la reprise logique suivante est:
`GO_OT_BOT_VISION_REAL_DATA_02`

### Pourquoi
Parce que:
- la chaîne bout-en-bout est déjà prouvée PASS;
- le dernier closeout a déjà ouvert une suite bornée sur la donnée réelle exposée par `/analyze`;
- le prochain gain utile peut rester local et minimal sans refondre ShareX, le bridge ni l’ingestion.

### Branche parallèle utile mais non prioritaire dans cette fiche
- monitoring / alerting de la chaîne si AutoCapture s’arrête, si le bridge retarde, ou si SCP/SSH timeout se déclenche.

## 7. Périmètre de la fiche

Cette fiche:
- fige la compréhension validée de Bot Vision / ingestion desk;
- ne modifie aucun runtime;
- n’ajoute aucune nouvelle donnée live;
- n’ouvre pas automatiquement un patch d’implémentation;
- sert de support de reprise compact.

## 8. Liens repo utiles

- `docs/ot/reports/OT_PROJECT_PORTFOLIO_OBJECTIVES_VALIDATED_PLANS_01.md`
- `docs/ot/closings/bot_vision/ETABLI_BOT_VISION.txt`
- `docs/ot/closings/bot_vision/CLOSEOUT_FINAL_BOT_VISION.txt`
- `docs/ot/closings/OT_BOT_VISION_REAL_DATA_01_CLOSING.txt`
- `scripts/desk_bridge/bridge_vision_to_desk_inbox.sh`

## 9. ETABLI

- la troisième `PROJECT_CARD` issue du gel portefeuille est ouverte pour Bot Vision / ingestion desk;
- le but final, le plan validé, le non établi et la reprise sont désormais figés dans une fiche compacte dédiée;
- la lacune documentaire est recentrée sur l’observabilité et l’enrichissement de la couche d’analyse plus que sur la chaîne de base elle-même.

## 10. TODO

- produire la fiche équivalente pour OpenClaw;
- produire ensuite, si utile, une fiche courte sur `validated_prompt_factory` ou `module_contextuals_shell`.

## 11. REPRISE

Point de reprise documentaire:
`PROJECT_CARD_BOT_VISION_INGESTION_01`

Point de reprise chantier logique:
`GO_OT_BOT_VISION_REAL_DATA_02`

## 12. MEM_CANDIDATE

Utile seulement sur demande explicite:
- pour Bot Vision / ingestion desk, la chaîne de base est déjà prouvée PASS; le prochain manque structurant n’est plus le transport, mais l’enrichissement borné des données d’analyse et l’observabilité.
