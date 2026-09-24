# Check the actual one-file build from outside the project directory.
$ErrorActionPreference = 'Stop'
$exePath = (Resolve-Path (Join-Path $PSScriptRoot '..\dist\d44.exe')).Path
$startedAt = Get-Date
$launcher = Start-Process -FilePath $exePath -WorkingDirectory $env:TEMP -WindowStyle Hidden -PassThru
try {
    $deadline = (Get-Date).AddSeconds(40)
    $gameProcess = $null
    do {
        Start-Sleep -Milliseconds 500
        $gameProcess = Get-Process -Name d44 -ErrorAction SilentlyContinue |
            Where-Object { $_.Path -eq $exePath -and $_.StartTime -ge $startedAt -and $_.MainWindowTitle -eq 'Deletion 44' } |
            Select-Object -First 1
        if ($launcher.HasExited) { throw "Executable exited during startup: $($launcher.ExitCode)" }
    } while (-not $gameProcess -and (Get-Date) -lt $deadline)
    if (-not $gameProcess) { throw 'The packaged game did not open its Deletion 44 window.' }
    Start-Sleep -Seconds 3
    $gameProcess.Refresh()
    if ($gameProcess.HasExited -or -not $gameProcess.Responding) {
        throw 'The packaged game stopped responding after startup.'
    }
    if (-not $gameProcess.CloseMainWindow()) { throw 'Could not close the test window.' }
    if (-not $launcher.WaitForExit(10000)) { throw 'The executable did not shut down cleanly.' }
    if ($launcher.ExitCode -ne 0) { throw "Executable returned $($launcher.ExitCode)" }
    Write-Host 'PASS: packaged executable starts outside the project, opens the game window, responds, and exits cleanly.'
}
finally {
    # Only clean up processes started by this check, never a pre-existing game.
    Get-Process -Name d44 -ErrorAction SilentlyContinue |
        Where-Object { $_.Path -eq $exePath -and $_.StartTime -ge $startedAt } |
        Stop-Process -ErrorAction SilentlyContinue
}
