<#
.SYNOPSIS
    Merges a profile (and optional GPU overlay) into Rust's client.cfg.
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\apply.ps1                         # interactive
    powershell -ExecutionPolicy Bypass -File tools\apply.ps1 -Preset low -Gpu gtx-1650
    powershell -ExecutionPolicy Bypass -File tools\apply.ps1 -Restore                # undo
#>
[CmdletBinding(DefaultParameterSetName = 'Apply')]
param(
    [Parameter(ParameterSetName = 'Apply')]
    [Alias('Profile')]   # old name kept; $Profile would shadow the automatic $PROFILE
    [ValidateSet('ultra-low', 'low', 'balanced', 'quality')]
    [string]$Preset,

    [Parameter(ParameterSetName = 'Apply')]
    [ValidatePattern('^[a-z0-9-]+$')]
    [string]$Gpu,

    [Parameter(ParameterSetName = 'Apply')]
    [ValidateRange(256, 8192)]
    [int]$GcBuffer,

    [string]$RustPath,

    [Parameter(ParameterSetName = 'Apply')]
    [switch]$DryRun,

    [Parameter(ParameterSetName = 'Restore')]
    [switch]$Restore,

    [Parameter(ParameterSetName = 'Restore')]
    [switch]$Original
)

$ErrorActionPreference = 'Stop'
$repoRoot    = Split-Path -Parent $PSScriptRoot
$linePattern = '^\s*([A-Za-z0-9_\.]+)\s+"(.*)"\s*$'
$utf8NoBom   = New-Object System.Text.UTF8Encoding($false)
$keepBackups = 5

function Fail([string]$msg) {
    Write-Host ''
    Write-Host "ERROR: $msg" -ForegroundColor Red
    exit 1
}

function Read-Utf8Lines([string]$path) {
    # PS 5.1 Get-Content defaults to the ANSI code page; Rust and Steam write UTF-8.
    $text = [System.IO.File]::ReadAllText($path, $utf8NoBom)   # still honours a BOM if present
    return , ($text -split "`r?`n")
}

function Find-RustPath {
    $roots = @()
    foreach ($k in 'HKCU:\Software\Valve\Steam', 'HKLM:\SOFTWARE\WOW6432Node\Valve\Steam') {
        $p = Get-ItemProperty $k -ErrorAction SilentlyContinue
        if ($p.SteamPath)   { $roots += $p.SteamPath }
        if ($p.InstallPath) { $roots += $p.InstallPath }
    }
    $libraries = @()
    foreach ($steam in ($roots | Select-Object -Unique)) {
        $libraries += $steam
        $vdf = Join-Path $steam 'steamapps\libraryfolders.vdf'
        if (Test-Path -LiteralPath $vdf) {
            $text = [System.IO.File]::ReadAllText($vdf, $utf8NoBom)
            # New format: "path" "D:\\Lib"; old format (pre-2021): "1" "D:\\Lib"
            foreach ($m in [regex]::Matches($text, '"(?:path|\d+)"\s+"([A-Za-z]:[^"]+)"')) {
                $libraries += ($m.Groups[1].Value -replace '\\\\', '\')
            }
        }
    }
    foreach ($lib in ($libraries | Select-Object -Unique)) {
        # appmanifest proves Rust is actually installed there, not a leftover folder
        if (-not (Test-Path -LiteralPath (Join-Path $lib 'steamapps\appmanifest_252490.acf'))) { continue }
        $candidate = Join-Path $lib 'steamapps\common\Rust'
        if (Test-Path -LiteralPath (Join-Path $candidate 'cfg')) { return $candidate }
    }
    return $null
}

function Read-Convars([string]$path) {
    $result = [ordered]@{}
    foreach ($line in (Read-Utf8Lines $path)) {
        if ($line -match $linePattern) { $result[$Matches[1]] = $Matches[2] }
    }
    return $result
}

function Get-GpuSuggestion {
    # Win32_VideoController.AdapterRAM is a uint32 (caps at 4 GB); the driver key has the real size.
    $class = 'HKLM:\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}'
    $gpus = Get-ChildItem $class -ErrorAction SilentlyContinue | ForEach-Object {
        $p = Get-ItemProperty $_.PSPath -ErrorAction SilentlyContinue
        if ($p.DriverDesc) {
            # Some drivers store the size as a QWORD, others as raw bytes or not at all.
            $bytes = 0
            foreach ($name in 'HardwareInformation.qwMemorySize', 'HardwareInformation.MemorySize') {
                $v = $p.$name
                if ($v -is [byte[]]) { $v = if ($v.Length -ge 8) { [BitConverter]::ToUInt64($v, 0) } elseif ($v.Length -ge 4) { [BitConverter]::ToUInt32($v, 0) } else { 0 } }
                try { if ([double]$v -gt $bytes) { $bytes = [double]$v } } catch { }
            }
            [pscustomobject]@{ Name = $p.DriverDesc; VramGB = [math]::Round($bytes / 1GB) }
        }
    }
    if (-not $gpus) {
        $gpus = Get-CimInstance Win32_VideoController | ForEach-Object {
            [pscustomobject]@{ Name = $_.Name; VramGB = [math]::Round($_.AdapterRAM / 1GB) } }
    }
    $map = [ordered]@{
        'GTX 1050 Ti' = 'gtx-1050-ti'; 'GTX 1060.*3\s?GB' = 'gtx-1060-3gb'; 'GTX 1060' = 'gtx-1060-6gb'
        'GTX 1650' = 'gtx-1650'; 'GTX 1660 (SUPER|Ti)' = 'gtx-1660-super'; 'RTX 2060' = 'rtx-2060'
        'RTX 3050' = 'rtx-3050'; 'RTX 3060(?! Ti)' = 'rtx-3060'; 'RTX 4060(?! Ti)' = 'rtx-4060'
        'RTX 5060 Ti' = 'rtx-5060-ti'; 'RTX 5060' = 'rtx-5060'; 'RTX 5070(?! Ti)' = 'rtx-5070'
        'RX 580' = 'rx-580-8gb'; 'RX 6600(?! XT)' = 'rx-6600'; 'RX 9070 XT' = 'rx-9070-xt'
    }
    # Prefer a discrete card over integrated graphics (laptops often have both).
    $ranked = $gpus | Where-Object { $_.Name -notmatch 'Microsoft Basic|Remote|Virtual|Parsec' } |
        Sort-Object @{ e = { $_.Name -match 'NVIDIA|Radeon RX|Radeon Pro|Arc' }; Descending = $true },
                    @{ e = { $_.VramGB }; Descending = $true }
    $gpu = $ranked | Select-Object -First 1
    if (-not $gpu) { return $null }
    $slug = $null
    foreach ($re in $map.Keys) { if ($gpu.Name -match $re) { $slug = $map[$re]; break } }
    if ($slug -eq 'rx-580-8gb' -and $gpu.VramGB -le 4) { $slug = 'rx-580-4gb' }
    if (-not $slug) {
        $slug = if ($gpu.Name -match 'NVIDIA') { 'nvidia' }
                elseif ($gpu.Name -match 'Radeon RX') { 'amd' }
                elseif ($gpu.Name -match 'Intel') { 'intel-igpu' }
    }
    [pscustomobject]@{ Name = $gpu.Name; VramGB = $gpu.VramGB; Overlay = $slug }
}

function Get-CardProfile([string]$slug, [int]$column) {
    # Reads the recommendation from gpu\cards\README.md: | name | VRAM | `slug` | `1080p` | `1440p` |
    $readme = Join-Path $repoRoot 'gpu\cards\README.md'
    foreach ($line in (Read-Utf8Lines $readme)) {
        if ($line -match "\|\s*``$([regex]::Escape($slug))``\s*\|\s*``([a-z-]+)``\s*\|\s*``([a-z-]+)``") {
            return $Matches[$column]
        }
    }
    return $null
}

function Ask([string]$question, [string[]]$choices, [string]$default) {
    while ($true) {
        $a = Read-Host "$question [$($choices -join '/')] (Enter = $default)"
        if (-not $a) { return $default }
        if ($choices -contains $a) { return $a }
        Write-Host "  Please type one of: $($choices -join ', ')" -ForegroundColor Yellow
    }
}

# --- Locate client.cfg ---
if (-not $RustPath) { $RustPath = Find-RustPath }
if (-not $RustPath) {
    Fail ('Could not find Rust automatically. In Steam: right-click Rust > Manage > Browse local files, ' +
          'copy the folder path, and run again with -RustPath "<that path>".')
}
$cfgPath = Join-Path $RustPath 'cfg\client.cfg'
if (-not (Test-Path -LiteralPath $cfgPath)) { Fail "client.cfg not found at $cfgPath. Start Rust once, quit, then try again." }
if (-not $DryRun -and (Get-Process -Name 'RustClient' -ErrorAction SilentlyContinue)) {
    Fail 'Rust is running. Quit Rust completely (not just to the main menu), then run this again.'
}

# --- Restore ---
if ($Restore) {
    $originalBak = "$cfgPath.original.bak"
    $pick = if ($Original) { Get-Item -LiteralPath $originalBak -ErrorAction SilentlyContinue }
            else { Get-ChildItem -LiteralPath (Split-Path $cfgPath) -Filter 'client.cfg.*.bak' |
                   Where-Object Name -ne 'client.cfg.original.bak' | Sort-Object Name -Descending | Select-Object -First 1 }
    if (-not $pick) { Fail 'No backup found to restore.' }
    Set-ItemProperty -LiteralPath $cfgPath -Name IsReadOnly -Value $false
    Copy-Item -LiteralPath $pick.FullName -Destination $cfgPath -Force
    Write-Host "Restored $($pick.Name) -> client.cfg" -ForegroundColor Green
    exit 0
}

# --- Interactive mode when no profile was given ---
if (-not $Preset) {
    $s = Get-GpuSuggestion
    if ($s) { Write-Host "Detected graphics card: $($s.Name) ($($s.VramGB) GB)" -ForegroundColor Cyan }
    $res = Ask 'Your screen resolution: 1080p or lower (1), or 1440p and up (2)?' @('1', '2') '1'
    $suggested = if ($s -and $s.Overlay) { Get-CardProfile $s.Overlay ([int]$res) }
    if (-not $suggested) { $suggested = 'low' }
    if (-not $Gpu -and $s) { $Gpu = $s.Overlay }
    $Preset = Ask 'Profile' @('ultra-low', 'low', 'balanced', 'quality') $suggested
    if ($Gpu) { $Gpu = Ask "GPU overlay ('none' to skip)" @($Gpu, 'none') $Gpu }
    if ($Gpu -eq 'none') { $Gpu = $null }
}

# --- Collect the settings to apply (later sources win) ---
$settings = [ordered]@{}
$sources = @(Join-Path $repoRoot "profiles\$Preset.cfg")
if ($Gpu) {
    $overlay = @("gpu\cards\$Gpu.cfg", "gpu\$Gpu.cfg") | ForEach-Object { Join-Path $repoRoot $_ } |
        Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if (-not $overlay) {
        $available = Get-ChildItem (Join-Path $repoRoot 'gpu'), (Join-Path $repoRoot 'gpu\cards') -Filter *.cfg | ForEach-Object BaseName
        Fail "Unknown -Gpu '$Gpu'. Valid names: $($available -join ', ')"
    }
    $sources += $overlay
}
foreach ($src in $sources) {
    $convars = Read-Convars $src
    foreach ($key in $convars.Keys) { $settings[$key] = $convars[$key] }
}
if ($GcBuffer) { $settings['gc.buffer'] = "$GcBuffer" }

# --- Merge (keeps encoding-safe UTF-8, original line endings, and updates duplicate keys) ---
$raw = [System.IO.File]::ReadAllText($cfgPath, $utf8NoBom)
$eol = if ($raw -match "`r`n") { "`r`n" } else { "`n" }
$lines = New-Object System.Collections.Generic.List[string]
foreach ($l in ($raw -split "`r?`n")) { $lines.Add($l) }
if ($lines.Count -gt 0 -and $lines[$lines.Count - 1] -eq '') { $lines.RemoveAt($lines.Count - 1) }

$changes = @()
foreach ($key in $settings.Keys) {
    $found = $false
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match $linePattern -and $Matches[1] -eq $key) {
            $found = $true
            $old = $Matches[2]
            if ($old -ne $settings[$key]) {
                $changes += [pscustomobject]@{ Setting = $key; Before = $old; After = $settings[$key] }
                $lines[$i] = "$key `"$($settings[$key])`""
            }
        }
    }
    if (-not $found) {
        $changes += [pscustomobject]@{ Setting = $key; Before = '(not set)'; After = $settings[$key] }
        $lines.Add("$key `"$($settings[$key])`"")
    }
}

Write-Host "Rust config: $cfgPath"
Write-Host "Applying:    profile '$Preset'$(if ($Gpu) { " + overlay '$Gpu'" })"
if ($changes.Count -eq 0) { Write-Host 'Nothing to change: your config already matches.' -ForegroundColor Green; exit 0 }
$changes | Format-Table -AutoSize | Out-String | Write-Host
if ($DryRun) { Write-Host "Dry run: $($changes.Count) change(s) shown, nothing written."; exit 0 }

# --- Backup: keep the very first state forever, plus the last $keepBackups ---
$dir = Split-Path $cfgPath
$originalBak = "$cfgPath.original.bak"
if (-not (Test-Path -LiteralPath $originalBak)) { Copy-Item -LiteralPath $cfgPath -Destination $originalBak }
$backup = "$cfgPath.$(Get-Date -Format 'yyyyMMdd-HHmmss-fff').bak"
Copy-Item -LiteralPath $cfgPath -Destination $backup
Get-ChildItem -LiteralPath $dir -Filter 'client.cfg.2*.bak' | Sort-Object Name -Descending |
    Select-Object -Skip $keepBackups | Remove-Item

# --- Write atomically; handle the common "made client.cfg read-only" tip ---
$item = Get-Item -LiteralPath $cfgPath
$wasReadOnly = $item.IsReadOnly
try {
    if ($wasReadOnly) { $item.IsReadOnly = $false }
    $tmp = "$cfgPath.tmp"
    [System.IO.File]::WriteAllText($tmp, (($lines -join $eol) + $eol), $utf8NoBom)
    Move-Item -LiteralPath $tmp -Destination $cfgPath -Force
    if ($wasReadOnly) { (Get-Item -LiteralPath $cfgPath).IsReadOnly = $true }
} catch {
    Fail "Could not write client.cfg ($($_.Exception.Message)). Your original is safe in: $backup"
}

Write-Host "Done: $($changes.Count) setting(s) changed." -ForegroundColor Green
Write-Host "Backup:  $backup"
Write-Host 'Next:    start Rust. To check, press F1 and type:  graphics.drawdistance  (it should show the new value).'
Write-Host 'Undo:    run this again with -Restore   (or double-click install.bat and pick Restore).'
Write-Host "Note:    picking a Quality preset in Rust's Graphics menu overwrites these values; just re-run this."
