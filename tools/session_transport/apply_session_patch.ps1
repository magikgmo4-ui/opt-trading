param(
  [Parameter(Mandatory = $true)]
  [string]$PatchPath,

  [Parameter(Mandatory = $false)]
  [string]$Branch = ""
)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

function Invoke-Checked {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Description,

    [Parameter(Mandatory = $true)]
    [scriptblock]$Command
  )

  & $Command
  if ($LASTEXITCODE -ne 0) {
    throw "$Description failed with exit code $LASTEXITCODE"
  }
}

if (-not (Test-Path -LiteralPath $PatchPath)) {
  throw "Patch file not found: $PatchPath"
}

$RepoRoot = git rev-parse --show-toplevel
if ($LASTEXITCODE -ne 0) {
  throw "Not inside a Git repository"
}

Set-Location $RepoRoot
Write-Host "REPO_ROOT=$RepoRoot"

git diff --quiet
if ($LASTEXITCODE -ne 0) {
  git status --short
  throw "Tracked working tree changes detected before patch. Commit/stash/clean first."
}

git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
  git status --short
  throw "Staged changes detected before patch. Commit/stash/clean first."
}

if ($Branch -ne "") {
  git switch $Branch 2>$null
  if ($LASTEXITCODE -ne 0) {
    Invoke-Checked "git switch -c $Branch" { git switch -c $Branch }
  }
}

$CurrentBranch = git branch --show-current
Write-Host "BRANCH=$CurrentBranch"
Write-Host "PATCH_FILE=$PatchPath"

Invoke-Checked "git apply --check" { git apply --check $PatchPath }
Invoke-Checked "git apply" { git apply $PatchPath }
Invoke-Checked "git diff --check" { git diff --check }

Write-Host ""
Write-Host "FILES_CHANGED:"
git diff --name-only

Write-Host ""
Write-Host "ROOT_PATCHES_REMAINING:"
Get-ChildItem -Path . -Filter "*.patch" -File | ForEach-Object { $_.FullName }

Write-Host ""
Write-Host "STATUS:"
git status --short --untracked-files=all

Write-Host ""
Write-Host "NEXT:"
Write-Host "Inspect the diff, run no-secret checks if needed, ensure root patches are not staged, then commit manually."
