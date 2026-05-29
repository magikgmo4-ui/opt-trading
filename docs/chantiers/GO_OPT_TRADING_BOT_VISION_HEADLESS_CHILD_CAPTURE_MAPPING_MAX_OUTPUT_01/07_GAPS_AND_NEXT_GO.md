# 07_GAPS_AND_NEXT_GO

## 13_ESTABLISHED

- `PF_BOT_VISION_HEADLESS` n'est pas clos
- le vrai besoin est un pipeline vision headless de production
- le mapping URL et capture n'est pas encore stabilise
- Data Center est l'aval de reference, Telegram et DeskPro sont des sorties/consumers

## 14_HYPOTHESIS

- le parent correct reste `PF_BOT_VISION_HEADLESS`
- `visual_context` est la premiere jointure locale la plus utile pour DeskPro
- `market_metrics.v1` ne couvre qu'une partie des sorties vision
- Telegram doit rester un canal filtre, pas le stockage canonique

## 15_REMAINING_GAP

1. mapping URL non stabilise
2. liste des screenshots obligatoires non figee
3. types de screen non normalises dans le runtime
4. analyseurs par type d'ecran non definis en code
5. trigger engine non cadre en implementation
6. contrat Data Center incomplet pour captures visuelles
7. Telegram pas encore filtre par importance
8. DeskPro pas encore relie au maximum output

## 16_TODO

1. figer le `CAPTURE_MAP` source par source
2. choisir les ecrans P0/P1 effectivement obligatoires
3. normaliser `screen_type` dans les sidecars / payloads
4. definir l'analyseur dedie pour chaque family d'ecran
5. choisir les triggers implables sans bruit excessif
6. relier les payloads derives a Data Center / Telegram / DeskPro

## 17_RESUME_POINT

```text
Le prochain GO ne ferme rien.
Il sert a stabiliser un plan de capture maximaliste :
capture -> analyse -> JSON -> Data Center -> Telegram -> DeskPro.
```
