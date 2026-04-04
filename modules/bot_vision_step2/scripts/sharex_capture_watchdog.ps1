param(
    [string]$WatchPath = "C:\monitor\screens",
    [string]$Pattern = "screen_*.png",
    [int]$MaxAgeMinutes = 15,
    [string]$NowIso = ""
)

$ErrorActionPreference = "Stop"

function Resolve-NowUtc {
    param([string]$RawNowIso)
    if ([string]::IsNullOrWhiteSpace($RawNowIso)) {
        return [DateTime]::UtcNow
    }
    return [DateTime]::Parse($RawNowIso).ToUniversalTime()
}

function Emit-Status {
    param(
        [string]$Status,
        [int]$ExitCode,
        [string]$Message,
        [string]$WatchPathValue,
        [string]$PatternValue,
        [string]$LatestFile,
        [Nullable[DateTime]]$LatestWriteTimeUtc,
        [Nullable[int]]$AgeSeconds,
        [int]$ThresholdMinutes
    )

    Write-Output ("STATUS: {0}" -f $Status)
    Write-Output ("MESSAGE: {0}" -f $Message)
    Write-Output ("WATCH_PATH: {0}" -f $WatchPathValue)
    Write-Output ("PATTERN: {0}" -f $PatternValue)
    Write-Output ("THRESHOLD_MINUTES: {0}" -f $ThresholdMinutes)
    if ($LatestFile) {
        Write-Output ("LATEST_FILE: {0}" -f $LatestFile)
    }
    if ($LatestWriteTimeUtc.HasValue) {
        Write-Output ("LATEST_WRITE_UTC: {0}" -f $LatestWriteTimeUtc.Value.ToString("o"))
    }
    if ($AgeSeconds.HasValue) {
        Write-Output ("AGE_SECONDS: {0}" -f $AgeSeconds.Value)
    }
    exit $ExitCode
}

$nowUtc = Resolve-NowUtc -RawNowIso $NowIso

if (-not (Test-Path -LiteralPath $WatchPath)) {
    Emit-Status -Status "ALERT" -ExitCode 1 -Message "watch path not found" -WatchPathValue $WatchPath -PatternValue $Pattern -LatestFile "" -LatestWriteTimeUtc $null -AgeSeconds $null -ThresholdMinutes $MaxAgeMinutes
}

$latest = Get-ChildItem -LiteralPath $WatchPath -Filter $Pattern -File | Sort-Object LastWriteTimeUtc -Descending | Select-Object -First 1

if (-not $latest) {
    Emit-Status -Status "ALERT" -ExitCode 1 -Message "no matching screenshot found" -WatchPathValue $WatchPath -PatternValue $Pattern -LatestFile "" -LatestWriteTimeUtc $null -AgeSeconds $null -ThresholdMinutes $MaxAgeMinutes
}

$latestWriteUtc = $latest.LastWriteTimeUtc
$ageSeconds = [int][Math]::Floor(($nowUtc - $latestWriteUtc).TotalSeconds)
$thresholdSeconds = $MaxAgeMinutes * 60

if ($ageSeconds -gt $thresholdSeconds) {
    Emit-Status -Status "ALERT" -ExitCode 1 -Message "latest screenshot is older than threshold" -WatchPathValue $WatchPath -PatternValue $Pattern -LatestFile $latest.FullName -LatestWriteTimeUtc $latestWriteUtc -AgeSeconds $ageSeconds -ThresholdMinutes $MaxAgeMinutes
}

Emit-Status -Status "OK" -ExitCode 0 -Message "latest screenshot is fresh" -WatchPathValue $WatchPath -PatternValue $Pattern -LatestFile $latest.FullName -LatestWriteTimeUtc $latestWriteUtc -AgeSeconds $ageSeconds -ThresholdMinutes $MaxAgeMinutes
