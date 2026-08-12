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
    throw "Patch folder was not found: $patchPath"
}
if (-not (Test-Path -LiteralPath $iniPath -PathType Leaf)) {
    throw "Ja2.ini was not found: $iniPath"
}

if (Test-Path -LiteralPath $exePath -PathType Leaf) {
    Copy-Item -LiteralPath $exePath -Destination "$exePath.backup_$stamp" -Force
}
Copy-Item -LiteralPath $iniPath -Destination "$iniPath.backup_$stamp" -Force

Get-ChildItem -LiteralPath $patchPath -Force | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $resolvedGamePath -Recurse -Force
}

# Older alpha builds accidentally shipped placeholder CIV EDT files. Remove only
# those recognizable placeholders so a real loose NPCData override is not touched.
$npcDataPath = Join-Path $resolvedGamePath 'Data\NPCData'
if (Test-Path -LiteralPath $npcDataPath -PathType Container) {
    Get-ChildItem -LiteralPath $npcDataPath -Filter 'civ*.edt' -File | ForEach-Object {
        if ($_.Length -eq 4800) {
            $bytes = [System.IO.File]::ReadAllBytes($_.FullName)
            if ($bytes.Length -ge 12) {
                $prefix = [System.Text.Encoding]::Unicode.GetString($bytes, 0, 12)
                if ($prefix.StartsWith('rvpuf ')) {
                    Remove-Item -LiteralPath $_.FullName -Force
                    Write-Host "Removed legacy CIV placeholder: $($_.Name)"
                }
            }
        }
    }
}

# r7609's JA2113 VFS resolves Data-1.13 above Data. Mirror the Korean taunts to
# the higher-priority layer and normalize two malformed censorship-tag patterns
# found in the generated translation files.
$tauntSourcePath = Join-Path $resolvedGamePath 'Data\TableData\EnemyTaunts'
$tauntTargetPath = Join-Path $resolvedGamePath 'Data-1.13\TableData\EnemyTaunts'
if (Test-Path -LiteralPath $tauntSourcePath -PathType Container) {
    New-Item -ItemType Directory -Path $tauntTargetPath -Force | Out-Null

    Get-ChildItem -LiteralPath $tauntSourcePath -Filter 'EnemyTaunts*.xml' -File | ForEach-Object {
        $sourceFile = $_.FullName
        $sourceName = $_.Name
        $text = [System.IO.File]::ReadAllText($sourceFile)
        $text = $text.Replace('<szTextCensored>', '<szCensoredText>')
        $text = $text.Replace('</szTextCensored>', '</szCensoredText>')

        $text = [regex]::Replace(
            $text,
            '(?s)<TAUNT>.*?</TAUNT>',
            {
                param($match)
                $block = $match.Value
                $normalTexts = [regex]::Matches($block, '<szText>.*?</szText>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
                $censoredTexts = [regex]::Matches($block, '<szCensoredText>.*?</szCensoredText>', [System.Text.RegularExpressions.RegexOptions]::Singleline)

                if ($normalTexts.Count -gt 2) {
                    throw "EnemyTaunts XML contains a TAUNT with more than two szText elements: $sourceFile"
                }
                if ($normalTexts.Count -eq 2) {
                    if ($censoredTexts.Count -ne 0) {
                        throw "EnemyTaunts XML contains duplicate szText and szCensoredText elements: $sourceFile"
                    }
                    $second = $normalTexts[1]
                    $replacement = $second.Value.Replace('<szText>', '<szCensoredText>').Replace('</szText>', '</szCensoredText>')
                    $block = $block.Remove($second.Index, $second.Length).Insert($second.Index, $replacement)
                }
                return $block
            }
        )

        # Parse before writing so a malformed file cannot silently replace r7609 data.
        $xmlCheck = New-Object System.Xml.XmlDocument
        $xmlCheck.PreserveWhitespace = $true
        $xmlCheck.LoadXml($text)

        $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllText($sourceFile, $text, $utf8NoBom)
        $targetFile = Join-Path $tauntTargetPath $sourceName
        [System.IO.File]::WriteAllText($targetFile, $text, $utf8NoBom)
    }
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
Write-Host "Korean patch installation completed: $resolvedGamePath"
Write-Host "Backup timestamp: $stamp"
