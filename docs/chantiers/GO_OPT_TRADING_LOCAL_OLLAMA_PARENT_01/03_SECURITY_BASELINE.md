---
doc_id: GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01_SECURITY_BASELINE

doc_type: security_baseline
repo: opt-trading
project: opt-trading
module: local-ai

go_id: GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01
status: draft
lifecycle_stage: security_design
topic_keys:
  - ollama
  - security
  - localhost
  - firewall
  - reverse-proxy
  - logs
  - agents
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/03_SECURITY_BASELINE.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/00_PARENT_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/01_SYNTHESE_OLLAMA_LOCAL.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/02_MACHINE_QUALIFICATION_PLAN.md
---

# 03_SECURITY_BASELINE

## 1_MASTER_TARGET

Définir la baseline sécurité minimale avant tout usage Ollama dans `opt-trading`, particulièrement avant exposition LAN, intégration agent, accès fichiers, tool calling ou usage Telegram.

## 3_INITIAL_NEED

Ollama expose un serveur local. Si mal configuré, il peut devenir une surface d'attaque :

- port `11434` accessible au réseau ;
- absence d'authentification native complète selon configuration ;
- agents capables d'appeler des outils ;
- prompts pouvant contenir secrets ou chemins sensibles ;
- accès à fichiers locaux via wrapper externe ;
- reverse proxy ou Docker exposé par erreur.

## 4_SECURITY_MODEL

Découpage sécurité :

```text
Utilisateur
  -> interface / agent / script
    -> proxy ou localhost
      -> Ollama :11434
        -> modèle chargé
          -> réponse texte / JSON / tool proposal
```

Point clé : Ollama génère ou sert une réponse. Les actions dangereuses viennent surtout du code hôte : agent, shell, lecture fichiers, réseau, bot, intégration IDE.

## 7_CANONICAL_STATE

Baseline au démarrage :

- autorisé : `localhost` ;
- interdit par défaut : exposition publique ;
- exposition LAN : seulement après sous-GO sécurité ;
- tool calling : seulement avec allowlist ;
- accès shell : interdit par défaut ;
- accès fichiers : borné par dossier ;
- trading autonome : hors périmètre.

## 8_VALIDATED_PLAN

Ordre de validation sécurité :

1. confirmer bind réseau ;
2. confirmer firewall ;
3. confirmer absence d'exposition publique ;
4. définir users/groups ;
5. définir logs ;
6. définir reverse proxy si nécessaire ;
7. définir allowlist tools ;
8. tester refus des actions interdites.

## 12_INVARIANTS

- Ne jamais exposer `11434` directement à Internet.
- Ne jamais binder sur `0.0.0.0` sans firewall et justification.
- Ne jamais connecter un agent shell libre à Ollama.
- Ne jamais injecter secrets/API keys dans les prompts.
- Ne jamais laisser Telegram déclencher une commande système non allowlistée.
- Ne jamais permettre à un modèle de décider seul d'une action trading.
- Toujours distinguer réponse modèle et action réelle.

## 13_ESTABLISHED

Contrôles minimaux :

```bash
ss -lntp | grep 11434 || true
curl -sS http://127.0.0.1:11434/api/version || true
curl -sS --max-time 2 http://$(hostname -I | awk '{print $1}'):11434/api/version || true
```

Lecture :

- si `127.0.0.1:11434` répond : local OK ;
- si IP LAN répond : exposition LAN active ;
- si IP publique répond : FAIL critique.

## 14_HYPOTHESIS

Hypothèse recommandée pour `opt-trading` :

- `student` : localhost seulement au début ;
- `db-layer` : LAN possible plus tard via reverse proxy interne ;
- `admin-trading` : éviter serveur Ollama exposé ;
- `cursor-ai` : localhost Windows ou client vers serveur interne.

## 15_REMAINING_GAP

À valider avant adoption :

- user Linux exécutant Ollama ;
- politique systemd ;
- firewall UFW/nftables ;
- reverse proxy éventuel ;
- logs ;
- rotation logs ;
- limites de ressources ;
- permissions des dossiers RAG ;
- séparation secrets ;
- allowlist tools.

## 16_TODO — Règles réseau

### 16.1 Mode autorisé par défaut

```text
BIND=127.0.0.1
EXTERNAL_ACCESS=NO
LAN_ACCESS=NO
AUTH_PROXY=NO
TOOLS=NO
```

### 16.2 Mode LAN contrôlé

Seulement si sous-GO sécurité :

```text
BIND=127.0.0.1 ou reverse proxy local
LAN_ACCESS=YES via proxy interne
AUTH_PROXY=YES
FIREWALL=YES
LOGS=YES
ALLOWLIST=YES
```

### 16.3 Mode interdit

```text
BIND=0.0.0.0
PUBLIC_ACCESS=YES
AUTH=NO
FIREWALL=NO
TOOLS=YES
```

Verdict : FAIL.

## 20_FIREWALL_BASELINE_LINUX

### UFW exemple LAN strict

À adapter seulement après sous-GO :

```bash
sudo ufw status verbose
sudo ufw deny 11434/tcp
sudo ufw allow from 192.168.16.0/24 to any port 11434 proto tcp
sudo ufw status numbered
```

Règle plus sûre : ne pas exposer Ollama directement ; utiliser un proxy interne.

## 21_REVERSE_PROXY_BASELINE

Si exposition LAN nécessaire :

- proxy local Nginx/Caddy ;
- auth basique ou token ;
- allowlist IP ;
- TLS si hors localhost ;
- logs access/error ;
- rate limit ;
- pas d'accès public.

Architecture recommandée :

```text
client LAN
  -> reverse proxy :PORT_AUTH
    -> 127.0.0.1:11434
```

Interdit :

```text
client Internet
  -> 0.0.0.0:11434 direct
```

## 22_LOGGING_BASELINE

Journaliser :

- timestamp ;
- client ;
- modèle ;
- endpoint ;
- taille prompt approximative ;
- statut ;
- durée ;
- usage tool si applicable ;
- erreur.

Ne pas journaliser :

- secrets ;
- API keys ;
- tokens ;
- prompts contenant données privées non nécessaires.

## 23_AGENT_TOOL_BASELINE

Pour tout agent :

### Autorisé

- lire fichiers dans dossier allowlist ;
- écrire dans dossier output dédié ;
- appeler scripts explicitement allowlistés ;
- retourner JSON validé ;
- demander validation humaine avant action Git ou système.

### Interdit

- shell libre ;
- suppression fichiers ;
- accès `$HOME` entier ;
- accès `.ssh`, `.env`, secrets ;
- commandes réseau arbitraires ;
- modification repo sans revue ;
- trading live.

## 24_SEPARATION_AGENTS_OUTILS

Rôles séparés :

| Rôle | Autorisation |
|---|---|
| Chat local | texte uniquement |
| RAG reader | lecture docs allowlist |
| Log analyst | lecture logs filtrés |
| Code assistant | suggestions, pas application automatique |
| Tool agent | allowlist stricte |
| Trading analyzer | lecture/diagnostic, pas exécution |
| Telegram bot | entrée/sortie bornée, pas shell |

## 25_PROMPT_SAFETY

Règles prompt :

- pas de secrets ;
- pas de clés API ;
- pas de mots de passe ;
- pas de tokens GitHub ;
- pas de chemins sensibles sauf nécessaires ;
- pas de logs bruts contenant credentials ;
- minimiser contexte injecté.

## 26_ACCEPTANCE_TESTS

Avant validation sécurité :

```text
TEST_LOCAL_API=PASS
TEST_LAN_ACCESS_EXPECTED=PASS_OR_BLOCKED_BY_DESIGN
TEST_PUBLIC_ACCESS=BLOCKED
TEST_FIREWALL=PASS
TEST_PROXY_AUTH=PASS_IF_PROXY
TEST_LOGGING=PASS
TEST_TOOL_ALLOWLIST=PASS_IF_AGENT
TEST_SECRET_EXCLUSION=PASS
```

## 27_VERDICT_INITIAL

Verdict initial : `SAFE_ONLY_IF_LOCALHOST`.

Ollama est acceptable pour usage local contrôlé. Toute exposition LAN ou intégration agent doit passer par sous-GO sécurité et validation explicite.

## 17_RESUME_POINT

Reprise :

- fichier : `03_SECURITY_BASELINE.md` ;
- état : baseline sécurité initiale posée ;
- prochain geste : vérifier bind/firewall sur machine candidate dans un sous-GO ;
- interdit : exposition réseau directe sans proxy/firewall/logs.
