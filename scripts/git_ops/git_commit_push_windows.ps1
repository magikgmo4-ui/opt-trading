<#
.SYNOPSIS
    Git Commit & Push (Windows)
.DESCRIPTION
    Adds specified paths, commits with a message, and pushes to origin.
    Or displays git status.
.EXAMPLE
    .\git_commit_push_windows.ps1 -Paths "scripts/student", "docs/my_doc.md" -CommitMessage "Update student scripts"
.EXAMPLE
    .\git_commit_push_windows.ps1 -ShowStatusOnly
#>

[CmdletBinding(DefaultParameterSetName="CommitPush")]
param (
    [Parameter(Mandatory=$true, ParameterSetName="CommitPush", ValueFromRemainingArguments=$true)]
    [string[]]$Paths,
    
    [Parameter(Mandatory=$true, ParameterSetName="CommitPush")]
    [string]$CommitMessage,
    
    [Parameter(Mandatory=$true, ParameterSetName="StatusOnly")]
    [switch]$ShowStatusOnly,

    [Parameter(ParameterSetName="CommitPush")]
    [switch]$NoPush = $false
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent (Split-Path -Parent $ScriptDir)

Set-Location $RootDir

Write-Host "=== Git Commit & Push (Windows) ===" -ForegroundColor Cyan
Write-Host "Repo Root: $RootDir"

# 1. Check Git Status (Show Only)
if ($PsCmdlet.ParameterSetName -eq "StatusOnly") {
    Write-Host "Current Status:"
    git status --short
    Write-Host "-----------------------------"
    Write-Host "Last Commit:"
    git log -1 --oneline --no-decorate --color=always
    exit 0
}

Write-Host "Message:   $CommitMessage"
Write-Host "-----------------------------"

# 2. Process and Add Paths
# Normalize Paths: Handle array input OR comma/semicolon separated strings
$NormalizedPaths = @()
foreach ($P in $Paths) {
    # Split by comma or semicolon, trim spaces and quotes
    $SplitParts = $P -split '[,;]'
    foreach ($Part in $SplitParts) {
        $CleanPart = $Part.Trim().Trim('"').Trim("'")
        if (-not [string]::IsNullOrWhiteSpace($CleanPart)) {
            $NormalizedPaths += $CleanPart
        }
    }
}

$AddedCount = 0
foreach ($Path in $NormalizedPaths) {
    if (Test-Path $Path) {
        Write-Host "Adding: $Path"
        git add $Path
        $AddedCount++
    } else {
        Write-Warning "Path not found: $Path (Skipping)"
    }
}

if ($AddedCount -eq 0) {
    Write-Error "FAIL: No valid paths found to add."
    exit 1
}

# 3. Commit (if changes staged)
$StatusStaged = git diff --cached --name-only
if ($StatusStaged) {
    Write-Host "Committing changes..."
    git commit -m "$CommitMessage"
    Write-Host "PASS: Commit created." -ForegroundColor Green
} else {
    Write-Warning "No changes to commit (already staged or empty)."
}

# 4. Push (if requested)
if (-not $NoPush) {
    Write-Host "Pushing to origin..."
    try {
        git push
        Write-Host "PASS: Push successful." -ForegroundColor Green
    } catch {
        Write-Error "FAIL: Push failed. Check remote access."
        exit 1
    }
} else {
    Write-Host "Skipping push (-NoPush used)."
}

Write-Host "-----------------------------"
Write-Host "SUCCESS: Operation complete." -ForegroundColor Green
Write-Host "Update on Linux with:"
Write-Host "bash scripts/git_ops/git_pull_update_linux.sh" -ForegroundColor Yellow
