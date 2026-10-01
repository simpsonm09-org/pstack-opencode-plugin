[CmdletBinding()]
param(
    [string] $Clone = (Join-Path $env:LOCALAPPDATA 'maxstack\pstack-claude')
)

# Vendors the pinned pstack-claude skills and the adapter skills into skills/.
# The package repo is the source of truth; this only regenerates the vendored tree.

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$lock = Get-Content -LiteralPath (Join-Path $repoRoot 'pstack.lock.json') -Raw | ConvertFrom-Json
$upstreamSkills = Join-Path $Clone $lock.skillsPath
$adapterSkills = Join-Path $repoRoot 'adapter\skills'
$skillsTarget = Join-Path $repoRoot 'skills'
$utf8 = New-Object System.Text.UTF8Encoding($false)
$binaryExtensions = @('.png', '.jpg', '.jpeg', '.gif', '.ico', '.webp', '.woff', '.woff2', '.ttf', '.otf', '.pdf', '.zip', '.gz', '.tgz', '.bz2', '.7z', '.exe', '.dll', '.so', '.dylib', '.bin', '.wasm', '.mp4', '.mov')

function Write-TextFile {
    param([string] $Path)

    if ($binaryExtensions -contains ([IO.Path]::GetExtension($Path).ToLowerInvariant())) { return }
    $text = [IO.File]::ReadAllText($Path).Replace("`r`n", "`n")
    [IO.File]::WriteAllText($Path, $text, $utf8)
}

function Invoke-Git {
    param([string[]] $Arguments)

    $result = & git @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Git command failed: git $($Arguments -join ' ')" }
    return ($result -join "`n").Trim()
}

function Copy-Tree {
    param([string] $Source, [string] $Destination)

    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    Get-ChildItem -LiteralPath $Source -Recurse -Force | ForEach-Object {
        $relative = $_.FullName.Substring($Source.Length).TrimStart('\')
        $target = Join-Path $Destination $relative
        if ($_.PSIsContainer) {
            New-Item -ItemType Directory -Path $target -Force | Out-Null
            return
        }
        New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
        Copy-Item -LiteralPath $_.FullName -Destination $target -Force
        Write-TextFile -Path $target
    }
}

if (-not (Test-Path -LiteralPath (Join-Path $Clone '.git'))) {
    throw "Pinned source clone not found at $Clone. Run the pinned clone step first."
}
if ((Invoke-Git @('-C', $Clone, 'remote', 'get-url', 'origin')) -ne $lock.repository) {
    throw "Unexpected upstream origin at $Clone"
}
if ((Invoke-Git @('-C', $Clone, 'rev-parse', 'HEAD')) -ne $lock.commit) {
    throw "Clone is not at the pinned commit $($lock.commit): $Clone"
}
if (Invoke-Git @('-C', $Clone, 'status', '--porcelain')) {
    throw "Pinned source clone has local changes: $Clone"
}
if (-not (Test-Path -LiteralPath $upstreamSkills -PathType Container)) {
    throw "Pinned skills directory not found: $upstreamSkills"
}

if (Test-Path -LiteralPath $skillsTarget) { Remove-Item -LiteralPath $skillsTarget -Recurse -Force }
New-Item -ItemType Directory -Path $skillsTarget -Force | Out-Null

$upstreamNames = @()
Get-ChildItem -LiteralPath $upstreamSkills -Directory | ForEach-Object {
    Copy-Tree -Source $_.FullName -Destination (Join-Path $skillsTarget $_.Name)
    $upstreamNames += $_.Name
}

$adapterNames = @()
Get-ChildItem -LiteralPath $adapterSkills -Directory | ForEach-Object {
    Copy-Tree -Source $_.FullName -Destination (Join-Path $skillsTarget $_.Name)
    $adapterNames += $_.Name
}

Copy-Item -LiteralPath (Join-Path $Clone 'NOTICE-skills.md') -Destination (Join-Path $repoRoot 'NOTICE') -Force
Copy-Item -LiteralPath (Join-Path $Clone 'LICENSE') -Destination (Join-Path $repoRoot 'LICENSE') -Force
Copy-Item -LiteralPath (Join-Path $Clone 'LICENSE-cursor-team-kit') -Destination (Join-Path $repoRoot 'LICENSE-cursor-team-kit') -Force
Copy-Item -LiteralPath (Join-Path $Clone 'NOTICE.md') -Destination (Join-Path $repoRoot 'NOTICE-port.md') -Force
foreach ($name in @('NOTICE', 'LICENSE', 'LICENSE-cursor-team-kit', 'NOTICE-port.md')) {
    Write-TextFile -Path (Join-Path $repoRoot $name)
}

$fileCount = (Get-ChildItem -LiteralPath $skillsTarget -Recurse -File | Measure-Object).Count
Write-Host "Vendored $($upstreamNames.Count) upstream skills and $($adapterNames.Count) adapter skills ($fileCount files) from $($lock.commit.Substring(0, 12))."
