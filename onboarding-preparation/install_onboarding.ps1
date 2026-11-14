$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath('C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
$packageRoot = Join-Path $PSScriptRoot 'StudyFlowApp-onboarding'
$backupRoot = Join-Path $PSScriptRoot ('backup-before-onboarding-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
$expectedFiles = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'expected-source.json') -Raw | ConvertFrom-Json
foreach ($entry in $expectedFiles.PSObject.Properties) {
    $dest = [IO.Path]::GetFullPath((Join-Path $projectRoot $entry.Name))
    if (-not $dest.StartsWith($projectRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw "Outside project: $dest" }
    if (Test-Path -LiteralPath $dest) {
        if ((Get-FileHash -LiteralPath $dest -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.Value) { throw "File changed since preparation: $dest" }
    } elseif ($null -ne $entry.Value) { throw "Missing expected file: $dest" }
}
foreach ($entry in $expectedFiles.PSObject.Properties) {
    $dest = Join-Path $projectRoot $entry.Name
    if (Test-Path -LiteralPath $dest) {
        $backup = Join-Path $backupRoot $entry.Name
        New-Item -ItemType Directory -Path (Split-Path -Parent $backup) -Force | Out-Null
        Copy-Item -LiteralPath $dest -Destination $backup
    }
    New-Item -ItemType Directory -Path (Split-Path -Parent $dest) -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $packageRoot $entry.Name) -Destination $dest -Force
}
Write-Output "Installed $(@($expectedFiles.PSObject.Properties).Count) files. Backup: $backupRoot"
$env:JAVA_HOME = 'C:\Program Files\Android\Android Studio\jbr'
Push-Location -LiteralPath $projectRoot
try {
    & '.\gradlew.bat' --offline --console=plain assembleDebug lintDebug
    if ($LASTEXITCODE -ne 0) { throw "Gradle failed: $LASTEXITCODE" }
} finally { Pop-Location }
