param(
  [Parameter(Mandatory = $true)]
  [string]$PatchPath,

  [Parameter(Mandatory = $true)]
  [string]$GoId,

  [Parameter(Mandatory = $false)]
  [string]$Slug = "session_patch"
)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

if (-not (Test-Path -LiteralPath $PatchPath)) {
  throw "Patch file not found: $PatchPath"
}

$RepoRoot = git rev-parse --show-toplevel
if ($LASTEXITCODE -ne 0) {
  throw "Not inside a Git repository"
}

Set-Location $RepoRoot

$DateStamp = Get-Date -Format "yyyyMMdd"
$SafeSlug = ($Slug -replace "\s+", "_" -replace "[^A-Za-z0-9._-]", "")
$DestDir = Join-Path -Path "bundles/$GoId" -ChildPath "patches"
$DestFile = Join-Path -Path $DestDir -ChildPath "${DateStamp}_${GoId}_${SafeSlug}.patch"

New-Item -ItemType Directory -Force $DestDir | Out-Null

$SrcResolved = (Resolve-Path -LiteralPath $PatchPath).Path
$DestFull = Join-Path -Path $RepoRoot -ChildPath $DestFile

if ($SrcResolved -eq $DestFull) {
  Write-Host "Patch already in canonical location: $DestFile"
  exit 0
}

Copy-Item -LiteralPath $SrcResolved -Destination $DestFull -Force

$SrcParent = Split-Path -Parent $SrcResolved
$RepoRootResolved = (Resolve-Path -LiteralPath $RepoRoot).Path

if ($SrcParent -eq $RepoRootResolved) {
  Remove-Item -LiteralPath $SrcResolved -Force
  Write-Host "Moved root patch to: $DestFile"
} else {
  Write-Host "Copied patch to: $DestFile"
}

Write-Host "PATCH_CANONICAL_PATH=$DestFile"
