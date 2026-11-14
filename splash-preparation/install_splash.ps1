$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath('C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
$packageRoot = Join-Path $PSScriptRoot 'StudyFlowApp-splash'
$backupRoot = Join-Path $PSScriptRoot ('backup-before-splash-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
$expectedFiles = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'expected-source.json') -Raw | ConvertFrom-Json

# Validate every destination and detect edits made since preparation.
foreach ($entry in $expectedFiles.PSObject.Properties) {
    $destination = [IO.Path]::GetFullPath((Join-Path $projectRoot $entry.Name))
    if (-not $destination.StartsWith($projectRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Destination outside StudyFlowApp: $destination"
    }
    if (Test-Path -LiteralPath $destination) {
        $actualHash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actualHash -ne $entry.Value) { throw "File changed since preparation: $destination" }
    } elseif ($null -ne $entry.Value) {
        throw "Expected existing file is missing: $destination"
    }
}

foreach ($entry in $expectedFiles.PSObject.Properties) {
    $destination = Join-Path $projectRoot $entry.Name
    if (Test-Path -LiteralPath $destination) {
        $backupFile = Join-Path $backupRoot $entry.Name
        New-Item -ItemType Directory -Path (Split-Path -Parent $backupFile) -Force | Out-Null
        Copy-Item -LiteralPath $destination -Destination $backupFile
    }
    New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $packageRoot $entry.Name) -Destination $destination -Force
}
Write-Output "Installed $(@($expectedFiles.PSObject.Properties).Count) prepared files. Backup: $backupRoot"

$env:JAVA_HOME = 'C:\Program Files\Android\Android Studio\jbr'
Push-Location -LiteralPath $projectRoot
try {
    & '.\gradlew.bat' --offline --console=plain assembleDebug lintDebug
    if ($LASTEXITCODE -ne 0) { throw "Gradle failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}
