$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

$GoId = 'GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01'
$BatchGoId = 'GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01'
$Branch = 'go/GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01'
$Today = '2026-04-26'

function Fail($Message) {
  throw "[INDEX_AGGREGATION_BATCH] $Message"
}

function Read-Text($Path) {
  if (-not (Test-Path $Path)) { Fail "Missing file: $Path" }
  return Get-Content -Raw -Encoding UTF8 $Path
}

function Write-Text($Path, $Content) {
  Set-Content -Path $Path -Value $Content -Encoding UTF8 -NoNewline
}

function Ensure-Contains($Content, $Needle, $Label) {
  if ($Content -notlike "*$Needle*") { Fail "Anchor not found in ${Label}: $Needle" }
}

function Insert-BeforeAnchor($Path, $Anchor, $Block, $UniqueNeedle) {
  $content = Read-Text $Path
  if ($content -like "*$UniqueNeedle*") {
    Write-Host "SKIP already present: $Path -> $UniqueNeedle"
    return
  }
  Ensure-Contains $content $Anchor $Path
  $updated = $content.Replace($Anchor, "$Block`r`n$Anchor")
  Write-Text $Path $updated
  Write-Host "PATCHED: $Path"
}

function Insert-AfterAnchor($Path, $Anchor, $Block, $UniqueNeedle) {
  $content = Read-Text $Path
  if ($content -like "*$UniqueNeedle*") {
    Write-Host "SKIP already present: $Path -> $UniqueNeedle"
    return
  }
  Ensure-Contains $content $Anchor $Path
  $updated = $content.Replace($Anchor, "$Anchor`r`n$Block")
  Write-Text $Path $updated
  Write-Host "PATCHED: $Path"
}

$branchName = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0) { Fail 'git branch failed' }
if ($branchName -ne $Branch) { Fail "Expected branch $Branch but got $branchName" }

$required = @(
  'docs/index/GO_INDEX.md',
  'docs/index/ACTIVE_STREAMS.md',
  'docs/index/NEXT_GO_CANDIDATES.md',
  'docs/index/REPRISE.md',
  "docs/chantiers/$GoId/INDEX_PATCH.md",
  "docs/index/inbox/$GoId.md"
)
foreach ($p in $required) {
  if (-not (Test-Path $p)) { Fail "Required file missing: $p" }
}

$goIndexBlock = @'
| GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 | GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 | — | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/00_INITIAL_PROJECT_DOC.md`<br>`docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md`<br>`docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/INDEX_PATCH.md` |
'@

$activeBlock = @'
### GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
- statut : active
- repo : opt-trading
- branche : `go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`
- dernier point établi : chantier parent doc-only mergé pour canoniser la doctrine multi-agents, avec continuité parent locale et inbox atomique
- prochaine action : appliquer le présent batch d'agrégation, puis ouvrir `GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01` seulement si une promotion additionnelle est requise
- blocages : aucun runtime ; entrée agrégée depuis `INDEX_PATCH.md`
'@

$nextBlock = @'
| `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | open | P1 | `GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01` | canoniser ou confirmer la méthode parent-local + inbox + batch après pilote ; aucun runtime OpenClaw | `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md`; `docs/governance/PARENT_CONTINUITY_INDEX_INBOX_METHOD_01.md` |
'@

$repriseBlock = @'
| `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | open | P1 | `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md`; `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/INDEX_PATCH.md`; `docs/governance/PARENT_CONTINUITY_INDEX_INBOX_METHOD_01.md` | continuité parent locale complète posée ; méthode local-first et inbox atomique mergées ; OpenClaw borné hors runtime dans ce chantier | entrée d'index agrégée par `GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01`; closeout final éventuel à produire | ouvrir `GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01` seulement si une promotion additionnelle est requise, sinon surveiller les prochains INDEX_PATCH |
'@

# GO_INDEX: insert after canonical table header separator.
Insert-AfterAnchor `
  -Path 'docs/index/GO_INDEX.md' `
  -Anchor '| --- | --- | --- | --- | --- | --- |' `
  -Block $goIndexBlock `
  -UniqueNeedle '| GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 | GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 |'

# ACTIVE_STREAMS: insert at top of Flux actifs.
Insert-AfterAnchor `
  -Path 'docs/index/ACTIVE_STREAMS.md' `
  -Anchor '## Flux actifs' `
  -Block "`r`n$activeBlock" `
  -UniqueNeedle '### GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01'

# NEXT_GO_CANDIDATES: insert after table header separator.
Insert-AfterAnchor `
  -Path 'docs/index/NEXT_GO_CANDIDATES.md' `
  -Anchor '| --- | --- | --- | --- | --- | --- |' `
  -Block $nextBlock `
  -UniqueNeedle '| `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | open | P1 |'

# REPRISE: insert after matrix table header separator.
Insert-AfterAnchor `
  -Path 'docs/index/REPRISE.md' `
  -Anchor '| --- | --- | --- | --- | --- | --- | --- | --- |' `
  -Block $repriseBlock `
  -UniqueNeedle '| `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | open | P1 |'

# Mark inbox applied.
$inboxPath = "docs/index/inbox/$GoId.md"
$inbox = Read-Text $inboxPath
$inbox = $inbox.Replace('status: ready', 'status: applied')
$inbox = $inbox.Replace('lifecycle_stage: inbox', 'lifecycle_stage: aggregated')
$inbox = $inbox.Replace('  - aggregation:pending', '  - aggregation:applied')
$inbox = $inbox.Replace('  - index:local_first', '  - index:global_synced')
$inbox = $inbox.Replace("updated_at: 2026-04-26`nlinks:", "updated_at: 2026-04-26`napplied_at: 2026-04-26`napplied_by_go: $BatchGoId`narchive_after_apply: false`nlinks:")
$inbox = $inbox.Replace('aggregation_status: pending', 'aggregation_status: applied')
Write-Text $inboxPath $inbox
Write-Host "PATCHED: $inboxPath"

# Create closeout.
$closeoutPath = "docs/chantiers/$BatchGoId/90_CLOSEOUT.md"
$closeout = @"
---
doc_id: OPT_TRADING_INDEX_AGGREGATION_BATCH_01_CLOSEOUT
doc_type: closeout
repo: opt-trading
project: opt-trading
module: indexation
go_id: $BatchGoId
status: pass
lifecycle_stage: closeout
topic_keys:
  - opt-trading
  - indexation
  - aggregation
  - closeout
search_tags:
  - surface:chantier
  - doc_role:closeout
  - aggregation:applied
  - index:global_synced
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: docs/index/REPRISE.md
updated_at: $Today
links:
  - docs/chantiers/$GoId/INDEX_PATCH.md
  - docs/index/inbox/$GoId.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/REPRISE.md
---

# 90_CLOSEOUT — $BatchGoId

## Verdict

PASS.

## Entrée agrégée

- $GoId

## Index globaux patchés

- docs/index/GO_INDEX.md
- docs/index/ACTIVE_STREAMS.md
- docs/index/NEXT_GO_CANDIDATES.md
- docs/index/REPRISE.md

## Inbox

- docs/index/inbox/$GoId.md marque applied.

## Non-objectifs respectés

- aucun runtime touché ;
- aucun OpenClaw runtime ;
- aucun trading live ;
- aucune agrégation d'autres GO.

## Point de reprise

Reprendre depuis docs/index/REPRISE.md ou surveiller les prochaines entrées docs/index/inbox/*.md.
"@
Write-Text $closeoutPath $closeout
Write-Host "CREATED: $closeoutPath"

Write-Host '--- git diff --stat ---'
git diff --stat
if ($LASTEXITCODE -ne 0) { Fail 'git diff --stat failed' }

Write-Host 'Batch application completed. Review diff, then git add/commit/push.'

