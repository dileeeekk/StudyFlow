$ErrorActionPreference = 'Stop'
$projectRoot = 'C:\Users\admin\AndroidStudioProjects\StudyFlowApp'
$backupRoot = Join-Path $PSScriptRoot ('backup-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
$files = @{
    'MainActivity.kt' = 'app\src\main\java\com\example\studyflowapp\MainActivity.kt'
    'ic_splash_placeholder.xml' = 'app\src\main\res\drawable\ic_splash_placeholder.xml'
    'studyflow_splash_theme.xml' = 'app\src\main\res\values-v31\studyflow_splash_theme.xml'
}
foreach ($name in $files.Keys) {
    $dest = Join-Path $projectRoot $files[$name]
    if (Test-Path -LiteralPath $dest) {
        $backup = Join-Path $backupRoot $files[$name]
        New-Item -ItemType Directory -Path (Split-Path -Parent $backup) -Force | Out-Null
        Copy-Item -LiteralPath $dest -Destination $backup
    }
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot $name) -Destination $dest -Force
}
Write-Output "Updated launch flow. Backup: $backupRoot"
$env:JAVA_HOME = 'C:\Program Files\Android\Android Studio\jbr'
& (Join-Path $projectRoot 'gradlew.bat') -p $projectRoot --offline --console=plain assembleDebug lintDebug
if ($LASTEXITCODE -ne 0) { throw 'Build failed' }
