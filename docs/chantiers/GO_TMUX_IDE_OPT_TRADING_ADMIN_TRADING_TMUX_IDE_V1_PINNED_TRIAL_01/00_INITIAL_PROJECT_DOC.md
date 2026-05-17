# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Ouvrir `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_V1_PINNED_TRIAL_01` pour tester de facon controlee `tmux-ide@1.3.1` sur `admin-trading`.

## WHY

Le flux P0 actif `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` a etabli la trajectoire TMUX IDE. Les probes precedents ont confirme que `tmux-ide@latest` / `2.x` echouent sur `admin-trading` Linux x64 a cause d'une dependance Darwin arm64, tandis que `tmux-ide@1.3.1 --version` a deja donne un signal positif.

Ce GO verifie uniquement le mode pinne `tmux-ide@1.3.1`, sans installation durable et sans creation `ide.yml`.

## 3_INITIAL_NEED

- Confirmer la baseline environnement sur `admin-trading`.
- Tester `npx -y tmux-ide@1.3.1 --version`.
- Tester `npx -y tmux-ide@1.3.1 --help`.
- Documenter la gate avant tout `ide.yml`.

## 5_GO_SCOPE

Ce GO couvre :

- probes SSH read-only ;
- commandes shell non destructives autorisees ;
- evaluation du binaire pinne via `npx -y` ;
- decision de gate pour une suite eventuelle.

Ce GO ne couvre pas :

- `npm install -g` ;
- installation systeme ;
- creation ou modification `ide.yml` ;
- lancement d'une session tmux-ide ;
- modification runtime durable ;
- modification `GO_INDEX`, `ACTIVE_STREAMS`, `REPRISE` ou `BRANCH_STATE`.

## 7_CANONICAL_STATE

Etat de depart :

- chaines `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR*` : `CLOSED_FINAL`, exclues ;
- `student / Ollama` : `CLOSED_FINAL`, exclu ;
- P0 actif : TMUX IDE ;
- topologie : `cursor-ai -> SSH -> admin-trading` ;
- blocage precedent : packaging `tmux-ide@2.x` incompatible Linux x64 ;
- signal compatible precedent : `tmux-ide@1.3.1 --version` PASS.

## 8_VALIDATED_PLAN

1. Creer une branche dediee depuis `origin/sot/mainline`.
2. Relire `MACHINE_WORK_SPLIT`, `ACTIVE_STREAMS` et le GO de compatibilite Linux x64.
3. Executer uniquement les commandes autorisees sur `admin-trading`.
4. Documenter baseline, resultat trial et gate.
5. Interdire `ide.yml` dans ce GO.

## 12_INVARIANTS

- Aucun `npm install -g`.
- Aucun `apt install`.
- Aucun changement durable sur `admin-trading`.
- Aucun `ide.yml`.
- Aucun melange avec `student`, `fantome`, `db-layer` ou OpenClaw static validator.
- Aucun index global modifie.

## 17_RESUME_POINT

```text
REPRISE:
GO ouvert dans C:\wtmuxv1.
Probe admin-trading effectue avec commandes autorisees.

NEXT:
relire 20_PINNED_TRIAL_RESULTS.md et 30_GATE_DECISION.md avant tout GO ide.yml.
```

## 18_VERDICT

```text
WIP / PINNED_TRIAL_OPENED
```
