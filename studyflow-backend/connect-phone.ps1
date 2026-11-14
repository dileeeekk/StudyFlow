param([string]$DeviceSerial = '')
$ErrorActionPreference = 'Stop'
$backendRoot = $PSScriptRoot
$backendPython = Join-Path $backendRoot '.venv\Scripts\python.exe'
$backendAdb = Join-Path $env:LOCALAPPDATA 'Android\Sdk\platform-tools\adb.exe'
if (-not (Test-Path -LiteralPath $backendPython)) { throw 'Backend environment is missing. Follow README.md first.' }
if (-not (Test-Path -LiteralPath $backendAdb)) { throw 'Android SDK adb.exe was not found.' }

$deviceOutput = & $backendAdb devices
if ($LASTEXITCODE -ne 0) { throw 'Could not list Android devices.' }
$readyDevices = @($deviceOutput | ForEach-Object {
    if ($_ -match '^(\S+)\s+device$') { $Matches[1] }
})
if (-not $DeviceSerial) {
    if ($readyDevices.Count -ne 1) {
        throw 'Connect one USB device and allow USB debugging, or pass -DeviceSerial SERIAL.'
    }
    $DeviceSerial = $readyDevices[0]
}
if ($DeviceSerial -notin $readyDevices) { throw 'The selected device is not connected or USB debugging is not authorized.' }

function Get-BackendStatus {
    try {
        $response = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/auth/me/' -UseBasicParsing -TimeoutSec 3
        return [int]$response.StatusCode
    } catch {
        if ($_.Exception.Response) { return [int]$_.Exception.Response.StatusCode }
        return 0
    }
}

$backendStatus = Get-BackendStatus
if ($backendStatus -eq 0) {
    Push-Location -LiteralPath $backendRoot
    try {
        & $backendPython bootstrap.py
        if ($LASTEXITCODE -ne 0) { throw 'Could not prepare local keys.' }
        & $backendPython manage.py migrate
        if ($LASTEXITCODE -ne 0) { throw 'Database migration failed.' }
        $server = Start-Process -FilePath $backendPython -ArgumentList '-u','manage.py','runserver','127.0.0.1:8000','--noreload' `
            -WorkingDirectory $backendRoot -WindowStyle Hidden -PassThru `
            -RedirectStandardOutput (Join-Path $backendRoot 'server-connect-output.log') `
            -RedirectStandardError (Join-Path $backendRoot 'server-connect-error.log')
        for ($attempt = 0; $attempt -lt 10; $attempt++) {
            Start-Sleep -Seconds 1
            $backendStatus = Get-BackendStatus
            if ($backendStatus -ne 0) { break }
            if ($server.HasExited) { throw 'Django stopped. Check server-connect-error.log.' }
        }
    } finally { Pop-Location }
}
if ($backendStatus -ne 401) { throw "Unexpected backend response: $backendStatus. Check port 8000 and the Django log." }
& $backendAdb -s $DeviceSerial reverse tcp:8000 tcp:8000
if ($LASTEXITCODE -ne 0) { throw 'USB port forwarding failed.' }
Write-Host 'StudyFlow is ready. Open the app on your phone.'
Write-Host 'Keep USB connected and the computer running. Run this script again after reconnecting USB or restarting the computer.'
Write-Host 'The app must use STUDYFLOW_API_URL=http://127.0.0.1:8000/api/ (already configured on this computer).'
