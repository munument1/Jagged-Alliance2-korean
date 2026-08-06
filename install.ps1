[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$GamePath
)

$ErrorActionPreference = 'Stop'
$resolvedGamePath = (Resolve-Path -LiteralPath $GamePath).Path
$patchPath = Join-Path $PSScriptRoot 'Patch'
$iniPath = Join-Path $resolvedGamePath 'Ja2.ini'
$exePath = Join-Path $resolvedGamePath 'ja2.exe'
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'

if (-not (Test-Path -LiteralPath $patchPath -PathType Container)) {
    throw "Patch 폴더를 찾을 수 없습니다: $patchPath"
}
if (-not (Test-Path -LiteralPath $iniPath -PathType Leaf)) {
    throw "Ja2.ini를 찾을 수 없습니다: $iniPath"
}

if (Test-Path -LiteralPath $exePath -PathType Leaf) {
    Copy-Item -LiteralPath $exePath -Destination "$exePath.backup_$stamp" -Force
}
Copy-Item -LiteralPath $iniPath -Destination "$iniPath.backup_$stamp" -Force

Get-ChildItem -LiteralPath $patchPath -Force | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $resolvedGamePath -Recurse -Force
}

$fontSettings = [ordered]@{
    'LargeFont1'            = @('Name = Galmuri11Bitmap', 'Height = -11')
    'SmallFont1'            = @('Name = Galmuri9Bitmap', 'Height = -9')
    'TinyFont1'             = @('Name = Galmuri9Bitmap', 'Height = -9')
    '12PointFont1'          = @('Name = Galmuri11Bitmap', 'Height = -11')
    'CompFont'              = @('Name = Galmuri9Bitmap', 'Height = -9')
    'SmallCompFont'         = @('Name = Galmuri9Bitmap', 'Height = -9')
    '10PointRoman'          = @('Name = Galmuri9Bitmap', 'Height = -9')
    '12PointRoman'          = @('Name = Galmuri11Bitmap', 'Height = -11')
    '14PointSansSerif'      = @('Name = Galmuri14Bitmap', 'Height = -14')
    '10PointArial'          = @('Name = Galmuri11Bitmap Condensed', 'Height = -11')
    '14PointArial'          = @('Name = Galmuri14Bitmap', 'Height = -14')
    '12PointArial'          = @('Name = Galmuri11Bitmap', 'Height = -11')
    'BlockyFont'            = @('Name = Galmuri11Bitmap', 'Height = -11', 'Weight = 700')
    'BlockyFont2'           = @('Name = Galmuri11Bitmap', 'Height = -11')
    '10PointArialBold'      = @('Name = Galmuri11Bitmap Condensed', 'Height = -11', 'Weight = 700')
    '12PointArialFixedFont' = @('Name = Galmuri11Bitmap', 'Height = -11')
    '16PointArial'          = @('Name = Galmuri14Bitmap', 'Height = -14')
    'BlockFontNarrow'       = @('Name = Galmuri9Bitmap', 'Height = -9')
    '14PointHumanist'       = @('Name = Galmuri14Bitmap', 'Height = -14')
    'HugeFont'              = @('Name = Galmuri14Bitmap', 'Height = -14')
}

$ini = [System.IO.File]::ReadAllText($iniPath)
$ini = [regex]::Replace($ini, '(?m)^USE_WINFONTS\s*=.*$', 'USE_WINFONTS = 1')
$ini = [regex]::Replace($ini, '(?m)^WIN_FONT_ADJUST\s*=.*$', 'WIN_FONT_ADJUST = 0')

foreach ($section in $fontSettings.Keys) {
    $body = ($fontSettings[$section] -join "`r`n")
    $pattern = '(?ms)^\[' + [regex]::Escape($section) + '\]\s*.*?(?=^\[|\z)'
    $replacement = "[$section]`r`n$body`r`n"
    if ([regex]::IsMatch($ini, $pattern)) {
        $ini = [regex]::Replace($ini, $pattern, $replacement, 1)
    } else {
        $ini += "`r`n$replacement"
    }
}

[System.IO.File]::WriteAllText($iniPath, $ini, [System.Text.UTF8Encoding]::new($false))
Write-Host "한국어 패치 설치 완료: $resolvedGamePath"
Write-Host "백업 시각: $stamp"

