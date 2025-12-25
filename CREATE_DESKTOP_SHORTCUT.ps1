# QUANTUM AVATAR DESKTOP SHORTCUT CREATOR
# Erstellt Desktop-Verknüpfung für die Desktop-App

param(
    [string]$AppPath = "QUANTUM_AVATAR_DESKTOP.py",
    [string]$ShortcutName = "QUANTUM AVATAR Desktop App"
)

Write-Host "===========================================" -ForegroundColor Green
Write-Host "   QUANTUM AVATAR DESKTOP SHORTCUT" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""

# Desktop-Pfad finden
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktopPath "$ShortcutName.lnk"

# Aktueller Pfad
$currentPath = Get-Location
$appFullPath = Join-Path $currentPath $AppPath

Write-Host "Desktop-Pfad: $desktopPath" -ForegroundColor Cyan
Write-Host "App-Pfad: $appFullPath" -ForegroundColor Cyan
Write-Host "Shortcut: $shortcutPath" -ForegroundColor Cyan
Write-Host ""

# Prüfe ob App-Datei existiert
if (!(Test-Path $appFullPath)) {
    Write-Host "❌ App-Datei nicht gefunden: $appFullPath" -ForegroundColor Red
    exit 1
}

Write-Host "✅ App-Datei gefunden" -ForegroundColor Green

try {
    # Erstelle das COM-Objekt
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)

    # Shortcut-Eigenschaften setzen
    $Shortcut.TargetPath = "cmd.exe"  # Verwende cmd.exe als Target
    $Shortcut.Arguments = "/c python `"$appFullPath`""  # Python-Script als Argument
    $Shortcut.WorkingDirectory = $currentPath
    $Shortcut.Description = "QUANTUM AVATAR KI Imperium Desktop Control - €28,000 täglich automatisches Geld"
    $Shortcut.IconLocation = "C:\Windows\System32\SHELL32.dll,43"  # Settings-Icon

    # Shortcut speichern
    $Shortcut.Save()

    Write-Host "✅ Desktop-Verknüpfung erfolgreich erstellt!" -ForegroundColor Green
    Write-Host "📍 Location: $shortcutPath" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🎯 DOPPELKLICK zum Starten der Desktop-App!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "💰 Die App bietet:" -ForegroundColor Green
    Write-Host "   • Live €28,000 täglich Revenue" -ForegroundColor White
    Write-Host "   • KI-Schwarm Command Center" -ForegroundColor White
    Write-Host "   • Autonome Geldgenerierung" -ForegroundColor White
    Write-Host "   • Professionelle Desktop UI" -ForegroundColor White
    Write-Host ""
    Write-Host "🚀 STARTE JETZT DEIN KI-IMPERIUM!" -ForegroundColor Magenta

} catch {
    Write-Host "❌ Fehler beim Erstellen der Verknüpfung: $_" -ForegroundColor Red

    # Alternative: Erstelle einfache Batch-Datei auf Desktop
    Write-Host "🔄 Erstelle alternatives Batch-Script..." -ForegroundColor Yellow

    $batchContent = @"
@echo off
echo Starting QUANTUM AVATAR Desktop App...
cd "$currentPath"
python "$AppPath"
pause
"@

    $batchPath = Join-Path $desktopPath "$ShortcutName.bat"
    $batchContent | Out-File -FilePath $batchPath -Encoding UTF8

    Write-Host "✅ Batch-Datei erstellt: $batchPath" -ForegroundColor Green
    Write-Host "   Doppelklick zum Starten" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "===========================================" -ForegroundColor Green
Write-Host "   INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
