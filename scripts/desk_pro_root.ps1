<#
.SYNOPSIS
    Desk Pro Root Wrapper (PowerShell)
.DESCRIPTION
    Delegates commands to the Python desk_pro_runner module.
.EXAMPLE
    .\desk_pro_root.ps1 status
    .\desk_pro_root.ps1 run-and-show
#>

param (
    [string]$Command = "status",
    [string[]]$ExtraArgs
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir

Set-Location $RootDir

# Check for Python
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Error "Python not found. Please install Python 3."
}

# Construct arguments
$PyArgs = @("-m", "modules.desk_pro_runner.app.desk_pro_runner", $Command) + $ExtraArgs

# Execute
python @PyArgs
