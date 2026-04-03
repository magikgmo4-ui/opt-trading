# TRADING DUAL STACK — LAB + REAL-TIME V1

Date (America/Montreal) : 2026-04-03

## 1. RÔLE DU DOCUMENT

Ce document fixe le **cadrage canonique V1** d’un système trading à deux niveaux :

1. un niveau **LAB** pour backtester, simuler, comparer et journaliser ;
2. un niveau **REAL-TIME** pour appliquer les mêmes stratégies dans le réel, d’abord en observation, puis avec validation, puis éventuellement en autonomie partielle.

Ce document sert aussi de **verdict d’analyse multi-rôles** sur le plan initial.

---

## 2. VERDICT GLOBAL

### Décision
Le plan est **bon, cohérent, et supérieur à un bot “full auto direct”**.

### Pourquoi
Parce qu’il vise :
- un **cadre trader humain discipliné** ;
- une **recherche quant testable** ;
- une **continuité stricte** entre recherche, validation et exécution ;
- une **journalisation exploitable** au lieu d’un simple bot opaque.

### Formulation canonique
Le projet ne doit pas être pensé comme :
- un bot miracle ;
- un algo libre ;
- un moteur qui trade partout et tout le temps.

Le projet doit être pensé comme :
- un **moteur de discipline trader** ;
- un **framework de recherche + exécution** ;
- une **architecture duale Lab + Real-Time** partageant le même noyau de règles.

---

## 3. ANALYSE MULTI-RÔLES

## 3.1 Architecte système trading — points forts

### Établi
- séparation claire **LAB / REAL-TIME** ;
- volonté de partager le même cadre de règles ;
- distinction entre **détection**, **validation**, **exécution** et **analyse** ;
- approche compatible avec une montée en puissance progressive.

### Verdict
Très bon niveau de base.

### Réserve
Le vrai risque serait de laisser diverger :
- un moteur “lab” d’un côté,
- un moteur “live” de l’autre,
- des logs différents,
- des configs différentes,
- des interprétations différentes d’un même setup.

### Règle canonique
**Un seul noyau de règles.**
La différence LAB vs REAL-TIME doit venir seulement de :
- la source de données ;
- le mode d’exécution ;
- le temps (historique vs live).

---

## 3.2 Quant / Lab designer — points forts

### Établi
Le plan met au centre :
- les variantes de setup ;
- la comparaison statistique ;
- les logs ;
- la segmentation par session, jour, setup et résultat.

### Verdict
C’est la bonne direction pour éviter le “je crois que ça marche”.

### Réserve
Un lab trop propre donnera des résultats trompeurs.

### Correction canonique
Le LAB doit intégrer dès V1 ou V1.1 :
- slippage simulé ;
- spread variable ;
- latence / retard d’entrée simulé ;
- cas non remplis / trade manqué si besoin ;
- règles de stop session / max trades / cooldown.

Sans cela, le lab sera utile, mais trop optimiste.

---

## 3.3 Risk manager — points forts

### Établi
Le plan inclut déjà l’idée de :
- fenêtres horaires ;
- kill zones ;
- max trades ;
- risk par trade ;
- progression observation → validation → autonomie.

### Verdict
Très bon point de départ.

### Réserve
Le plus gros danger n’est pas la stratégie ;
le plus gros danger est l’absence de garde-fous communs entre test et réel.

### Règles canoniques minimales
Le cadre commun doit imposer :
- timezone : `America/Montreal` ;
- sessions autorisées ;
- kill zones ;
- `max_trades_per_session` ;
- `max_trades_per_day` ;
- `risk_per_trade_pct` ;
- `rr_min` ;
- `stop_day_after_losses` ;
- `cooldown_after_trade` ;
- interdiction de re-entry immédiat non prévu ;
- interdiction de trade hors session si non explicitement autorisé.

---

## 3.4 Trader discret / opérateur réel — points forts

### Établi
Le plan respecte une vérité terrain :
- les meilleures méthodes simples sont souvent des méthodes très cadrées ;
- beaucoup de valeur vient de la répétition du même setup dans les mêmes fenêtres ;
- la discipline vaut plus que la multiplication des signaux.

### Verdict
Le plan est compatible avec une logique “boring trader”.

### Réserve
Un bot qui voit un signal technique valide n’a pas forcément raison en réel.

### Ce qui doit rester explicitement séparé
- **signal mécanique** ;
- **qualité contextuelle** ;
- **permission d’exécuter**.

Le mode validation humaine reste donc une étape normale, pas un échec du projet.

---

## 3.5 Auditeur critique — ce qui casserait le plan

Le plan casserait si on fait l’une de ces erreurs :
- lancer le full auto avant d’avoir une base de logs propre ;
- coder des règles différentes entre lab et réel ;
- mélanger le cadre trader avec la logique de setup dans un seul bloc opaque ;
- faire des journaux trop pauvres ;
- tester trop de variantes sans contrat commun ;
- considérer le backtest comme une preuve suffisante sans confrontation live.

---

## 4. CE QUE JE GARDE DU PLAN INITIAL

### À garder tel quel
- architecture duale **Lab + Real-Time** ;
- logique de **cadre trader** (session, kill zone, risk, boring trader) ;
- progression **Observation → Validation → Exécution autonome** ;
- importance centrale des logs et des comparaisons ;
- volonté de faire du système un outil de recherche, pas juste un bot.

---

## 5. CE QUE JE MODIFIERAIS IMMÉDIATEMENT

## 5.1 Séparer 4 couches au lieu d’un seul bloc

Le plan doit être découpé ainsi :

### A. Trader Frame
Règles disciplinaires communes.

### B. Strategy Engine
Détection et qualification du setup.

### C. Execution Mode
Observation / validation / exécution autonome.

### D. Analytics
Logs, stats, rapports, comparaisons, dérive lab/live.

### Pourquoi
Parce qu’un bon setup dans un mauvais cadre n’est pas acceptable ;
et un bon cadre avec une mauvaise exécution reste insuffisant.

---

## 5.2 Introduire un contrat commun obligatoire

Le système doit partager :
- le même format de config ;
- le même format de signal ;
- le même format de trade ;
- le même format d’événements ;
- le même format de rapport.

### Pourquoi
Sinon le LAB et le REAL-TIME deviennent deux mondes différents.

---

## 5.3 Démarrer par un sous-périmètre très étroit

### Recommandation canonique V1
Commencer par :
- **Gold / XAUUSD** ;
- fenêtres `18:00` et `00:00` ;
- timezone `America/Montreal` ;
- setup centré sur open/session logic ;
- variantes MIMO/FVG/sweep clairement classées.

### Pourquoi
Le périmètre étroit donne :
- des logs plus comparables ;
- moins de bruit ;
- moins de dispersion ;
- une meilleure lecture des résultats.

---

## 5.4 Prévoir la comparaison LAB vs LIVE dès le début

Ce n’est pas une amélioration “plus tard”.
C’est un invariant du système.

### À comparer
- nombre de signaux ;
- nombre de trades exécutables ;
- winrate ;
- expectancy ;
- MFE / MAE ;
- slippage ;
- dérive de résultat ;
- dérive par session ;
- dérive par setup.

### Pourquoi
Le but final n’est pas “un beau backtest”.
Le but final est **la continuité fiable entre lab et réel**.

---

## 6. ARCHITECTURE CANONIQUE V1

## 6.1 Principe

Le système repose sur un **noyau partagé**.

### Noyau partagé
- règles de session ;
- règles de risque ;
- règles disciplinaires ;
- logique de stratégie ;
- structure des événements ;
- structure des logs.

### Ce qui change entre LAB et REAL-TIME
- la source des données ;
- la cadence ;
- le mode d’exécution ;
- les contraintes d’infrastructure.

---

## 6.2 Niveaux

### Niveau 1 — LAB
Rôle :
- backtester ;
- simuler ;
- comparer ;
- scorer ;
- logguer ;
- produire les rapports de vérité.

### Niveau 2 — REAL-TIME
Rôle :
- détecter en direct ;
- appliquer le même cadre ;
- observer, faire valider, ou exécuter ;
- logguer dans le même format ;
- mesurer la dérive réelle.

---

## 6.3 Modes d’exécution temps réel

### Mode A — OBSERVATION
- détecte ;
- classe ;
- log ;
- n’exécute pas.

### Mode B — VALIDATION
- détecte ;
- calcule entrée / SL / TP / taille ;
- attend validation ;
- exécute si validé.

### Mode C — AUTONOMIE CIBLÉE
- détecte ;
- exécute ;
- gère ;
- log ;
- uniquement sur un sous-ensemble statistiquement validé.

### Décision canonique
Le système doit **naître en Observation**, passer ensuite en **Validation**, puis seulement ouvrir des cas d’**Autonomie ciblée**.

---

## 7. CADRE TRADER COMMUN — V1 MINIMUM

## 7.1 Sessions

### Référence initiale retenue
- session `gold_open_18h`
- session `midnight_00h`
- timezone : `America/Montreal`

### Fenêtres de départ
- `18:00` → fenêtre active bornée
- `00:00` → fenêtre active bornée

### Règle
Aucun trade hors fenêtre, sauf exception explicitement déclarée dans la config.

---

## 7.2 Discipline

### Champs minimaux
- `max_trades_per_session`
- `max_trades_per_day`
- `stop_day_after_losses`
- `cooldown_after_trade`
- `allow_reentry_same_setup`
- `allow_outside_sessions`

### Philosophie
Le moteur doit empêcher mécaniquement les écarts disciplinaires les plus fréquents.

---

## 7.3 Risk management

### Champs minimaux
- `risk_per_trade_pct`
- `rr_min`
- `move_be_at_r`
- `partial_tp_plan`
- `max_stop_distance`
- `min_valid_stop_distance`

### Décision
Le **risk engine** doit être commun aux deux niveaux.
Il ne doit pas exister une logique risk “lab” et une logique risk “live”.

---

## 8. STRATEGY ENGINE — LOGIQUE CANONIQUE

## 8.1 Règle structurelle

La stratégie doit être décrite comme un objet lisible, pas comme un bloc de code opaque.

### Exemple de composants
- session requise ;
- sweep requis ou non ;
- FVG requis ou non ;
- reclaim requis ou non ;
- direction bullish / bearish ;
- filtre HTF ;
- filtre spread ;
- filtre news si activé.

---

## 8.2 Variantes

Une variante doit être identifiable et comparable.

### Exemples de familles à comparer
- `sweep + FVG + reclaim`
- `no_sweep + FVG + reclaim`
- `sweep only`
- `open drive / breakout encadré`

### Règle
Chaque variante doit avoir :
- un `variant_id` ;
- une définition courte ;
- un cadre d’activation ;
- ses métriques propres.

---

## 9. JOURNALISATION CANONIQUE

## 9.1 Minimum obligatoire

Le système doit logguer au moins :
- `event_id`
- `strategy_id`
- `variant_id`
- `mode`
- `symbol`
- `session_name`
- `date`
- `timezone`
- `signal_ts`
- `entry_ts`
- `direction`
- `entry`
- `sl`
- `tp_plan`
- `risk_pct`
- `rr_planned`
- `result`
- `r_realized`
- `mfe`
- `mae`
- `time_in_trade`
- `reason_entry`
- `reason_exit`
- `filters_state`

---

## 9.2 Event journal avant trade journal

### Décision canonique
Le système doit d’abord produire un **journal d’événements**, puis dériver un **journal de trades**.

### Pourquoi
Parce que tout ne finit pas en trade.
Il faut aussi pouvoir étudier :
- setup détecté mais refusé ;
- setup valide mais bloqué par le cadre ;
- setup observé mais non exécuté ;
- divergence entre signal et exécution.

---

## 10. MÉTRIQUES À RENDRE OBLIGATOIRES

## 10.1 Au niveau trade
- win / loss / scratch
- R réalisé
- MAE
- MFE
- durée
- slippage

## 10.2 Au niveau variante
- winrate
- expectancy
- profit factor
- max drawdown
- distribution par jour
- distribution par session
- taille d’échantillon

## 10.3 Au niveau lab vs live
- dérive d’exécution
- dérive de fréquence
- dérive de résultat
- dérive de setup

---

## 11. DÉPLOIEMENT RECOMMANDÉ

## 11.1 Séquence recommandée

### Étape 1
Développement et tests initiaux sur la machine la plus adaptée au travail de labo.

### Étape 2
Observation live sans exécution.

### Étape 3
Validation humaine en conditions réelles.

### Étape 4
Autonomie ciblée seulement sur les variantes déjà prouvées.

---

## 11.2 Principe multi-machine

Alignement recommandé avec l’existant projet :
- **LAB / recherche / simulation** d’abord sur l’environnement de travail le plus adapté au test ;
- **REAL-TIME / runtime / supervision** ensuite sur l’environnement opératoire cible.

Le plus important n’est pas la machine elle-même, mais :
- la stabilité du noyau partagé ;
- la continuité de config ;
- la compatibilité des logs ;
- la reproductibilité des résultats.

---

## 12. CE QU’IL NE FAUT PAS FAIRE

### Interdictions canoniques
- ne pas lancer le full auto avant une vraie base statistique ;
- ne pas mélanger UI et logique de stratégie ;
- ne pas coder les règles seulement dans l’exécution ;
- ne pas limiter les logs au résultat final ;
- ne pas changer le cadre selon l’humeur ou la session ;
- ne pas valider une variante sur une taille d’échantillon ridicule ;
- ne pas traiter le backtest comme une preuve finale.

---

## 13. VERSION V1 RECOMMANDÉE

## 13.1 Focus V1

### Instrument
- XAUUSD / Gold

### Sessions
- `18:00`
- `00:00`

### Cadre
- timezone `America/Montreal`
- fenêtres bornées
- 1 trade max par session au départ
- risk fixe
- RR minimum explicite

### Mode
- LAB complet
- REAL-TIME en observation puis validation

### Famille de setup
- open/session
- MIMO / FVG / sweep classifiés mécaniquement

---

## 13.2 Pourquoi ce focus
- il respecte le plan utilisateur réel ;
- il réduit le bruit ;
- il permet une base statistique exploitable ;
- il favorise une mise en production prudente.

---

## 14. POINT DE REPRISE CANONIQUE

### Trigger proposé
`GO_OT_TRADING_DUAL_STACK_V1_01`

### Objet du trigger
1. figer le schéma commun `frame / strategy / execution / analytics` ;
2. définir la structure de config V1 ;
3. définir le schéma d’événements et de trade V1 ;
4. cadrer la première famille de variantes Gold session ;
5. ouvrir l’implémentation LAB avant toute exécution live.

---

## 15. RÉSUMÉ EXÉCUTIF

### Ce qui est validé
Le plan de départ est bon.

### Ce qui est gardé
- architecture duale ;
- cadre trader discipliné ;
- logs ;
- progression observation → validation → autonomie.

### Ce qui est renforcé
- noyau partagé obligatoire ;
- contrat commun ;
- journal d’événements avant journal de trades ;
- friction réaliste dans le lab ;
- comparaison lab/live comme invariant.

### Décision finale
Construire **un framework trading dual Lab + Real-Time**, centré d’abord sur Gold/session, avec un seul noyau de règles, une montée en puissance prudente, et une journalisation suffisamment riche pour décider objectivement ce qui mérite d’être exécuté dans le réel.
