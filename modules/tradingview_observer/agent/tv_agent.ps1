# TradingView Orchestrator Agent - cursor-ai desktop session
# Runs as a scheduled task (OnLogon) in the interactive session.
# Watches jobs/pending/ for tv_job_v1 packets, executes via tradingview-mcp CLI,
# writes results to jobs/done/ or jobs/failed/.
#
# Install: see install_agent.ps1 in this directory.
# Manual run: powershell -File tv_agent.ps1
param(
    [int]$PollIntervalMs = 2000,
    [switch]$Once
)

$ErrorActionPreference = 'Continue'

$AGENT_ROOT  = Split-Path $PSScriptRoot -Parent
$JOBS_PENDING = Join-Path $AGENT_ROOT "jobs\pending"
$JOBS_DONE    = Join-Path $AGENT_ROOT "jobs\done"
$JOBS_FAILED  = Join-Path $AGENT_ROOT "jobs\failed"
$TV_CLI       = "$env:USERPROFILE\.claude\tools\tradingview-mcp\src\cli\index.js"
$LOG_FILE     = Join-Path $AGENT_ROOT "agent\tv_agent.log"

foreach ($d in @($JOBS_PENDING, $JOBS_DONE, $JOBS_FAILED)) {
    if (-not (Test-Path $d)) { New-Item -ItemType Directory -Force $d | Out-Null }
}

function Coalesce($a, $b) { if ($null -ne $a -and $a -ne '') { $a } else { $b } }

function Log($msg) {
    $line = "$(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss') $msg"
    Write-Host $line
    Add-Content -Path $LOG_FILE -Value $line -Encoding UTF8 -ErrorAction SilentlyContinue
}

function Tv {
    param([string[]]$Args)
    $raw = & node $TV_CLI @Args 2>&1 | Out-String
    try   { $raw | ConvertFrom-Json }
    catch { @{success=$false; error="json_parse_failed"; raw=$raw.Trim()} }
}

function CheckCdp {
    # Use TCP probe (Invoke-WebRequest hangs on MSIX loopback in non-desktop sessions)
    $tcp = Test-NetConnection -ComputerName 127.0.0.1 -Port 9222 `
               -WarningAction SilentlyContinue -InformationLevel Quiet
    if ($tcp) { return @{ok=$true; browser="TradingView:9222"} }
    return @{ok=$false; error="Port 9222 not listening"}
}

function ExecJob($job) {
    $type   = $job.type
    $params = $job.params
    if (-not $params) { $params = @{} }

    switch ($type) {
        "snapshot" {
            @{
                status  = Tv status
                quote   = Tv quote
                state   = Tv state
                alerts  = Tv alert list
                values  = Tv values
            }
        }
        "alert.list" { Tv alert list }
        "alert.create" {
            $flags = @("-c", (Coalesce $params.condition "crossing"))
            if ($params.price)   { $flags += @("-p", "$($params.price)") }
            if ($params.message) {
                $msg = if ($params.message -is [string]) { $params.message }
                       else { $params.message | ConvertTo-Json -Compress }
                $flags += @("-m", $msg)
            }
            Tv alert create @flags
        }
        "alert.delete" {
            Tv alert delete "--id" $params.alert_id
        }
        "alert.rotate_webhook_key" {
            $newKey = $params.new_key_value
            if (-not $newKey) {
                return @{success=$false; error="new_key_value missing from params"}
            }
            $list = Tv alert list
            $rotated = 0; $skipped = 0
            foreach ($a in $list.alerts) {
                try {
                    $msg = $a.message | ConvertFrom-Json -ErrorAction Stop
                    if ($msg.PSObject.Properties.Name -contains 'key') {
                        $msg.key = $newKey
                        $newMsg = $msg | ConvertTo-Json -Compress
                        Tv alert delete "--id" $a.id | Out-Null
                        Tv alert create "-c" "crossing" "-m" $newMsg | Out-Null
                        $rotated++
                    } else { $skipped++ }
                } catch { $skipped++ }
            }
            @{success=$true; rotated=$rotated; skipped=$skipped}
        }
        "indicator.add" {
            $flags = @($params.name)
            if ($params.pane) { $flags += @("--pane", $params.pane) }
            Tv indicator add @flags
        }
        "indicator.remove" { Tv indicator remove $params.entity_id }
        "indicator.set" {
            $flags = @($params.entity_id)
            foreach ($k in $params.inputs.PSObject.Properties.Name) {
                $flags += @("--input", "$k=$($params.inputs.$k)")
            }
            Tv indicator set @flags
        }
        "symbol.set"    { Tv symbol $params.symbol }
        "timeframe.set" { Tv timeframe $params.timeframe }
        "pine.set" {
            $tmpPine = [System.IO.Path]::GetTempFileName() + ".pine"
            Set-Content -Path $tmpPine -Value $params.source -Encoding UTF8
            $result = Tv pine set "--file" $tmpPine
            Remove-Item $tmpPine -Force -ErrorAction SilentlyContinue
            $result
        }
        "pine.save"     { Tv pine save }
        "screenshot" {
            $outPath = Coalesce $params.output_path (Join-Path $AGENT_ROOT "output\screenshot_$(Get-Date -Format 'yyyyMMdd_HHmmss').png")
            Tv screenshot "--file" $outPath
        }
        "layout.switch" { Tv layout switch $params.name }
        default { @{success=$false; error="unknown job type: $type"} }
    }
}

function ProcessJob($file) {
    $jobId = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    Log "Processing job: $jobId ($($file.Name))"

    try {
        $job = Get-Content $file.FullName -Raw | ConvertFrom-Json
    } catch {
        Log "FAIL parse JSON: $($file.Name) - $_"
        Move-Item $file.FullName (Join-Path $JOBS_FAILED $file.Name) -Force
        return
    }

    $cdp = CheckCdp
    if (-not $cdp.ok) {
        Log "WARN: CDP not available - $($cdp.error)"
        $result = @{success=$false; error="CDP_UNAVAILABLE: $($cdp.error)"}
    } else {
        try {
            $output = ExecJob $job
            $result = @{
                success     = $true
                job_id      = $job.id
                job_type    = $job.type
                executed_at = (Get-Date -Format 'o')
                output      = $output
            }
            Log "PASS: $jobId type=$($job.type)"
        } catch {
            $result = @{success=$false; job_id=$job.id; error="$_"; executed_at=(Get-Date -Format 'o')}
            Log "FAIL: $jobId - $_"
        }
    }

    $resultJson = $result | ConvertTo-Json -Depth 15
    $resultFile = Join-Path $JOBS_DONE "$jobId.result.json"
    Set-Content -Path $resultFile -Value $resultJson -Encoding UTF8
    Move-Item $file.FullName (Join-Path $JOBS_DONE "$($file.Name).done") -Force -ErrorAction SilentlyContinue
}

Log "TV Agent started - polling $JOBS_PENDING every ${PollIntervalMs}ms"
Log "CLI: $TV_CLI"

$cdp = CheckCdp
if ($cdp.ok) { Log "CDP OK: $($cdp.browser)" }
else         { Log "WARN: CDP not available at startup - will retry per job" }

if ($Once) {
    $files = Get-ChildItem $JOBS_PENDING -Filter "*.json" | Sort-Object LastWriteTime
    foreach ($f in $files) { ProcessJob $f }
    Log "Agent --once done"
    exit 0
}

while ($true) {
    try {
        $files = Get-ChildItem $JOBS_PENDING -Filter "*.json" | Sort-Object LastWriteTime
        foreach ($f in $files) { ProcessJob $f }
    } catch {
        Log "ERROR in poll loop: $_"
    }
    Start-Sleep -Milliseconds $PollIntervalMs
}
