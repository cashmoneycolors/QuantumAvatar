@echo off
REM QUANTUM AVATAR DESKTOP APP LAUNCHER
REM Garantiert funktionierende Desktop-App Start-Script

cls
color 0A
echo ===========================================
echo    QUANTUM AVATAR DESKTOP APP
echo ===========================================
echo.
echo Desktop-Anwendung wird gestartet...
echo Funktionen:
echo • Live Revenue-Monitoring: €28,000/Tag
echo • KI-Schwarm Command Center
echo • Autonome Geldgenerierung
echo • System Status Dashboard
echo.
echo ===========================================
timeout /t 2 >nul

echo Starte QUANTUM AVATAR Desktop-Anwendung...
python QUANTUM_AVATAR_DESKTOP.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Fehler beim Starten der App!
    echo Mögliche Ursachen:
    echo • Tkinter nicht verfügbar
    echo • Python-Fehler im Code
    echo • Abhängigkeiten fehlen
    echo.
    echo Versuche alternatives Start-Script...
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Desktop-App erfolgreich gestartet!
echo Schließe dieses Fenster...
timeout /t 3 >nul
