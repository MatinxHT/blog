param(
    [Parameter(Position = 0)]
    [ValidateSet('serve', 'test')]
    [string]$Mode = 'serve'
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$version = '0.166.0'
$localHugo = Join-Path $root ".tools/hugo/$version/hugo.exe"
Set-Location $root

if (-not (Test-Path 'themes/PaperMod/theme.toml')) {
    Write-Host 'Initializing the Hugo theme submodule...'
    & git submodule update --init --recursive
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

$hugo = $null
if (Test-Path $localHugo) {
    $hugo = $localHugo
} else {
    $installed = Get-Command hugo -ErrorAction SilentlyContinue
    if ($installed -and ((& $installed.Source version) -match "hugo v$([regex]::Escape($version))\b")) {
        $hugo = $installed.Source
    }
}

if (-not $hugo) {
    $hugoDir = Split-Path -Parent $localHugo
    $archive = Join-Path $hugoDir 'hugo.zip'
    New-Item -ItemType Directory -Path $hugoDir -Force | Out-Null
    $url = "https://github.com/gohugoio/hugo/releases/download/v$version/hugo_${version}_windows-amd64.zip"
    Write-Host "Downloading Hugo $version to $hugoDir ..."
    try {
        Invoke-WebRequest -Uri $url -OutFile $archive
        Expand-Archive -Path $archive -DestinationPath $hugoDir -Force
    } finally {
        Remove-Item -LiteralPath $archive -ErrorAction SilentlyContinue
    }
    $hugo = $localHugo
}

if (-not (Test-Path $hugo)) { throw "Hugo executable not found: $hugo" }

if ($Mode -eq 'serve') {
    Write-Host 'Preview: http://localhost:1313/ (Ctrl+C to stop)'
    & $hugo server --buildDrafts
    exit $LASTEXITCODE
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { throw 'Python is required for scripts/check_site.py. Install Python and retry.' }

$trackedExports = & git ls-files | Where-Object { $_ -match '(?i)\.(xml|wxr)$' }
if ($LASTEXITCODE -ne 0) { throw 'Could not inspect tracked files with git.' }
if ($trackedExports) { throw "WordPress export files are tracked: $($trackedExports -join ', ')" }

& $hugo --cleanDestinationDir --gc --minify --panicOnWarning
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $python.Source scripts/check_site.py
exit $LASTEXITCODE
