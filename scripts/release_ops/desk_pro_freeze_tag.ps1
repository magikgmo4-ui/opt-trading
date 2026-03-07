<#
.SYNOPSIS
    Desk Pro Freeze & Tag (Windows)
.DESCRIPTION
    Creates an annotated Git tag and pushes it to origin.
    Ensures the working tree is clean before tagging.
.EXAMPLE
    .\desk_pro_freeze_tag.ps1 -TagName "desk_pro_v1.0" -TagMessage "Initial release"
#>

param (
    [Parameter(Mandatory=$true)]
    [string]$TagName,
    
    [Parameter(Mandatory=$true)]
    [string]$TagMessage,
    
    [switch]$Force = $false
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent (Split-Path -Parent $ScriptDir)

Set-Location $RootDir

Write-Host "=== Desk Pro Freeze & Tag ===" -ForegroundColor Cyan
Write-Host "Repo Root: $RootDir"
Write-Host "Tag Name:  $TagName"
Write-Host "Message:   $TagMessage"
Write-Host "-----------------------------"

# 1. Check Git Status
$Status = git status --porcelain
if ($Status -and -not $Force) {
    Write-Error "FAIL: Working tree is not clean. Commit or stash changes first."
    Write-Host "Changes detected:" -ForegroundColor Yellow
    $Status
    exit 1
} elseif ($Status -and $Force) {
    Write-Warning "Working tree is dirty, but -Force used. Proceeding..."
} else {
    Write-Host "PASS: Working tree is clean." -ForegroundColor Green
}

# 2. Check Existing Tag
if (git tag -l $TagName) {
    Write-Error "FAIL: Tag '$TagName' already exists locally."
    exit 1
}

# 3. Create Tag
Write-Host "Creating annotated tag..."
try {
    git tag -a $TagName -m "$TagMessage"
    Write-Host "PASS: Tag created locally." -ForegroundColor Green
} catch {
    Write-Error "FAIL: Git tag creation failed."
    exit 1
}

# 4. Push Tag
Write-Host "Pushing tag to origin..."
try {
    git push origin $TagName
    Write-Host "PASS: Tag pushed successfully." -ForegroundColor Green
} catch {
    Write-Warning "Push failed. Check remote access."
    Write-Host "You can push manually later: git push origin $TagName"
}

Write-Host "-----------------------------"
Write-Host "SUCCESS: Release '$TagName' frozen." -ForegroundColor Green
Write-Host "Verify on Linux with:"
Write-Host "bash scripts/release_ops/desk_pro_verify_tag_linux.sh $TagName" -ForegroundColor Yellow
