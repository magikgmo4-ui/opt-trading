---
doc_id: GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01_MACHINE_QUALIFICATION_PLAN

doc_type: qualification_plan
repo: opt-trading
project: opt-trading
module: local-ai

go_id: GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01
status: draft
lifecycle_stage: qualification_plan
topic_keys:
  - ollama
  - machines
  - student
  - admin-trading
  - db-layer
  - cursor-ai
  - benchmark
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/02_MACHINE_QUALIFICATION_PLAN.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/00_PARENT_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/01_SYNTHESE_OLLAMA_LOCAL.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/03_SECURITY_BASELINE.md
---

# 02_MACHINE_QUALIFICATION_PLAN

## 1_MASTER_TARGET

Définir un plan de qualification reproductible pour savoir où Ollama peut tourner dans l'écosystème `opt-trading` : `student`, `admin-trading`, `db-layer`, `cursor-ai`.

Ce document ne lance aucune installation. Il prépare les commandes et critères de décision pour un sous-GO machine dédié.

## 3_INITIAL_NEED

Qualifier les machines candidates avant tout choix d'adoption Ollama :

- ressources CPU/RAM/GPU ;
- OS ;
- stockage ;
- sécurité réseau ;
- performance modèle ;
- pertinence par rôle machine ;
- risques pour services existants.

## 6_FINAL_TARGET

À la fin d'un sous-GO de qualification, produire un tableau clair :

| Machine | Rôle retenu | Ollama autorisé ? | Usage recommandé | Limite principale | Verdict |
|---|---|---:|---|---|---|
| student | lab IA local | à valider | modèles légers/moyens | RAM/GPU | TBD |
| admin-trading | serveur trading | prudent | non prioritaire | risque services | TBD |
| db-layer | backend/data | à valider | RAG/agents backend | charge + sécurité | TBD |
| cursor-ai | Windows IDE | à valider | orchestration/dev | Windows/GPU | TBD |

## 7_CANONICAL_STATE

Hypothèses connues au démarrage :

- `student` : Debian 12, cible expérimentale possible pour Ollama/DeepSeek ; upgrade RAM envisagé jusqu'à 64 GB.
- `admin-trading` : serveur Linux `/opt/trading`, services systemd critiques trading ; éviter charge IA lourde sans isolation.
- `db-layer` : MSI Ubuntu, cible OpenClaw déjà explorée ; pourrait servir backend IA/RAG si ressources suffisantes.
- `cursor-ai` : Windows, surface IDE/GUI ; utile pour orchestration et tests dev.

Ces éléments doivent être revalidés machine par machine.

## 8_VALIDATED_PLAN

Plan en quatre passes :

1. inventaire système ;
2. inventaire GPU/RAM/stockage ;
3. installation/test Ollama si sous-GO validé ;
4. mini benchmark ;
5. verdict par machine.

## 12_INVARIANTS

- Ne pas installer Ollama depuis le parent.
- Ne pas activer d'exposition LAN par défaut.
- Ne pas tester sur `admin-trading` si la charge risque de perturber les services trading.
- Ne pas utiliser de secrets dans les prompts benchmark.
- Ne pas télécharger de modèles lourds sans vérifier disque/RAM.
- Ne pas confondre performance ponctuelle et capacité production.

## 13_ESTABLISHED

Critères minimaux à mesurer :

- OS et kernel ;
- CPU modèle/coeurs ;
- RAM totale/disponible ;
- GPU détecté ;
- VRAM si disponible ;
- disque libre ;
- port `11434` ;
- version Ollama ;
- modèles installés ;
- vitesse tokens/s approximative ;
- latence premier token ;
- stabilité sous 3 requêtes répétées.

## 14_HYPOTHESIS

Hypothèses de rôle :

### student

Candidat principal pour laboratoire local IA.

Usages possibles :
- modèles légers/moyens ;
- RAG documentaire ;
- tests vision ;
- benchmark DeepSeek/Qwen/Gemma ;
- formation expérimentale.

### admin-trading

Candidat faible pour charge IA lourde, car serveur de services trading.

Usages possibles :
- client vers autre Ollama ;
- tests courts hors heures critiques ;
- génération locale très légère seulement si ressources libres.

### db-layer

Candidat intéressant pour backend RAG/agents si ressources suffisantes.

Usages possibles :
- index documentaire ;
- vector DB ;
- OpenClaw gateway local ;
- embeddings ;
- analyses batch.

### cursor-ai

Candidat pour poste opérateur/dev Windows.

Usages possibles :
- IDE local ;
- OpenCode/Codex clients ;
- tests avec GPU Windows si disponible ;
- interface WebUI.

## 16_TODO — Commandes de qualification

### 16.1 Linux — inventaire système

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

hostnamectl || true
uname -a
lsb_release -a 2>/dev/null || cat /etc/os-release
nproc
lscpu | sed -n '1,40p'
free -h
df -h / /opt /home 2>/dev/null || df -h
```

### 16.2 Linux — inventaire GPU

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

command -v nvidia-smi && nvidia-smi || true
command -v rocm-smi && rocm-smi || true
lspci | grep -Ei 'vga|3d|display|nvidia|amd|intel' || true
ls /dev/dri 2>/dev/null || true
```

### 16.3 Linux — réseau / port Ollama

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

ss -lntp | grep 11434 || true
curl -sS http://127.0.0.1:11434/api/version || true
ollama --version || true
ollama list || true
ollama ps || true
```

### 16.4 Windows PowerShell — inventaire système

```powershell
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

Get-ComputerInfo | Select-Object CsName, OsName, OsVersion, CsProcessors, CsTotalPhysicalMemory
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors
Get-CimInstance Win32_PhysicalMemory | Measure-Object Capacity -Sum
Get-PSDrive -PSProvider FileSystem
```

### 16.5 Windows PowerShell — GPU

```powershell
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion
nvidia-smi
if ($LASTEXITCODE -ne 0) { Write-Host 'nvidia-smi unavailable or no NVIDIA GPU' }
```

### 16.6 Windows PowerShell — Ollama

```powershell
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

ollama --version
ollama list
ollama ps
Invoke-RestMethod http://127.0.0.1:11434/api/version
Get-NetTCPConnection -LocalPort 11434 -ErrorAction SilentlyContinue
```

## 20_BENCHMARK_MINIMAL

### 20.1 Modèles candidats légers

- `llama3.2` ;
- `gemma3` si disponible ;
- `qwen3` selon disponibilité ;
- `nomic-embed-text` pour embeddings.

### 20.2 Prompt benchmark chat

```bash
curl -sS http://127.0.0.1:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [{"role":"user","content":"Résume en 5 points les risques d exposer un serveur LLM local."}],
  "stream": false,
  "options": {"temperature": 0}
}'
```

### 20.3 Prompt benchmark JSON

```bash
curl -sS http://127.0.0.1:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [{"role":"user","content":"Retourne un JSON avec fields: status, risk_level, next_action."}],
  "format": "json",
  "stream": false,
  "options": {"temperature": 0}
}'
```

### 20.4 Benchmark embeddings

```bash
curl -sS http://127.0.0.1:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01 qualification machine"
}' | head -c 500
```

## 21_DECISION_CRITERIA

### ADOPT_NOW

Conditions :

- performance acceptable ;
- RAM/VRAM suffisante ;
- pas d'impact service ;
- port local seulement ;
- modèles utiles confirmés ;
- logs disponibles.

### ADOPT_WITH_LIMITS

Conditions :

- utile pour tâches légères ;
- pas assez solide pour agents lourds ;
- usage borné à chat/RAG simple/logs.

### LAB_ONLY

Conditions :

- instable ou lent ;
- utile pour apprendre/tester ;
- non retenu pour workflow opérateur.

### REJECT_FOR_NOW

Conditions :

- ressources insuffisantes ;
- risque service ;
- sécurité non maîtrisée ;
- usage mieux couvert par cloud/API.

## 22_MACHINE_OUTPUT_TEMPLATE

À produire pour chaque machine :

```text
MACHINE=<name>
OS=<value>
CPU=<value>
RAM_TOTAL=<value>
GPU=<value>
VRAM=<value>
DISK_FREE=<value>
OLLAMA_VERSION=<value>
PORT_11434=<localhost|lan|absent>
MODEL_TESTED=<value>
CHAT_RESULT=<PASS|FAIL>
JSON_RESULT=<PASS|FAIL>
EMBEDDINGS_RESULT=<PASS|FAIL|N/A>
AVG_LATENCY=<value>
RISKS=<value>
VERDICT=<ADOPT_NOW|ADOPT_WITH_LIMITS|LAB_ONLY|REJECT_FOR_NOW>
NEXT_GO=<value>
```

## 17_RESUME_POINT

Reprise :

- fichier : `02_MACHINE_QUALIFICATION_PLAN.md` ;
- état : plan de qualification prêt ;
- prochaine action : ouvrir un sous-GO machine avant exécution ;
- sous-GO recommandé : `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_MACHINE_QUALIFICATION_01`.
