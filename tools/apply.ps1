<#
.SYNOPSIS
    Merges a profile (and optional GPU overlay) into Rust's client.cfg.

.DESCRIPTION
    Only the keys present in the profile/overlay are changed; every other line
    in client.cfg is kept. A timestamped backup is written next to client.cfg.
    Rust overwrites client.cfg on exit, so the game must be closed.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\apply.ps1 -Profile low -Gpu nvidia
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('ultra-low', 'low', 'balanced', 'quality')]
    [string]$Profile,

    # Vendor overlay (gpu\<name>.cfg) or card overlay (gpu\cards\<name>.cfg)
    [string]$Gpu,

    [ValidateRange(256, 8192)]
    [int]$GcBuffer,

    [string]$RustPath,

    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$linePattern = '^\s*([A-Za-z0-9_\.]+)\s+"(.*)"\s*$'

function Find-RustPath {
    $steam = (Get-ItemProperty -Path 'HKCU:\Software\Valve\Steam' -Name SteamPath -ErrorAction SilentlyContinue).SteamPath
    if (-not $steam) { return $null }

    $libraries = @($steam)
    $vdf = Join-Path $steam 'steamapps\libraryfolders.vdf'
    if (Test-Path $vdf) {
        foreach ($m in [regex]::Matches((Get-Content $vdf -Raw), '"path"\s+"([^"]+)"')) {
            $libraries += $m.Groups[1].Value -replace '\\\\', '\'
        }
    }

    foreach ($lib in ($libraries | Select-Object -Unique)) {
        $candidate = Join-Path $lib 'steamapps\common\Rust'
        if (Test-Path (Join-Path $candidate 'cfg')) { return $candidate }
    }
    return $null
}

function Read-Convars([string]$path) {
    $result = [ordered]@{}
    foreach ($line in Get-Content $path) {
        if ($line -match $linePattern) { $result[$Matches[1]] = $Matches[2] }
    }
    return $result
}

# --- Collect the settings to apply (later sources win) ---
$settings = [ordered]@{}
$sources = @(Join-Path $repoRoot "profiles\$Profile.cfg")
if ($Gpu) {
    $overlay = @("gpu\$Gpu.cfg", "gpu\cards\$Gpu.cfg") |
        ForEach-Object { Join-Path $repoRoot $_ } |
        Where-Object { Test-Path $_ } |
        Select-Object -First 1
    if (-not $overlay) {
        $available = Get-ChildItem (Join-Path $repoRoot 'gpu'), (Join-Path $repoRoot 'gpu\cards') -Filter *.cfg |
            ForEach-Object { $_.BaseName }
        throw "Unknown -Gpu '$Gpu'. Available: $($available -join ', ')"
    }
    $sources += $overlay
}
foreach ($src in $sources) {
    $convars = Read-Convars $src
    foreach ($key in $convars.Keys) { $settings[$key] = $convars[$key] }
}
if ($GcBuffer) { $settings['gc.buffer'] = "$GcBuffer" }

# --- Locate client.cfg ---
if (-not $RustPath) { $RustPath = Find-RustPath }
if (-not $RustPath) { throw 'Could not find Rust. Pass -RustPath "<...>\steamapps\common\Rust".' }
$cfgPath = Join-Path $RustPath 'cfg\client.cfg'
if (-not (Test-Path $cfgPath)) { throw "client.cfg not found at $cfgPath. Launch Rust once so it creates one." }

if (-not $DryRun -and (Get-Process -Name 'RustClient' -ErrorAction SilentlyContinue)) {
    throw 'Rust is running. Close it first: Rust overwrites client.cfg on exit.'
}

# --- Merge ---
$lines = New-Object System.Collections.Generic.List[string]
foreach ($line in @(Get-Content $cfgPath)) { $lines.Add($line) }
$changes = @()
foreach ($key in $settings.Keys) {
    $newLine = "$key `"$($settings[$key])`""
    $index = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match $linePattern -and $Matches[1] -eq $key) { $index = $i; break }
    }
    if ($index -ge 0) {
        $old = ([regex]::Match($lines[$index], $linePattern)).Groups[2].Value
        if ($old -ne $settings[$key]) {
            $changes += [pscustomobject]@{ Convar = $key; Old = $old; New = $settings[$key] }
            $lines[$index] = $newLine
        }
    } else {
        $changes += [pscustomobject]@{ Convar = $key; Old = '(missing)'; New = $settings[$key] }
        $lines.Add($newLine)
    }
}

Write-Host "Config:  $cfgPath"
Write-Host "Profile: $Profile$(if ($Gpu) { " + gpu/$Gpu" })"
if ($changes.Count -eq 0) {
    Write-Host 'Nothing to change: client.cfg already matches.'
    return
}
$changes | Format-Table -AutoSize | Out-String | Write-Host

if ($DryRun) {
    Write-Host "Dry run: $($changes.Count) change(s) not written."
    return
}

$backup = "$cfgPath.$(Get-Date -Format 'yyyyMMdd-HHmmss').bak"
Copy-Item $cfgPath $backup
[System.IO.File]::WriteAllLines($cfgPath, $lines, (New-Object System.Text.UTF8Encoding($false)))
Write-Host "Applied $($changes.Count) change(s). Backup: $backup"
