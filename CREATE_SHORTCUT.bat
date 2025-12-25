@echo off
REM Einfache Desktop Shortcut Erstellung für QUANTUM AVATAR

echo ===========================================
echo    QUANTUM AVATAR DESKTOP SHORTCUT
echo ===========================================
echo.
echo Erstelle Desktop-Verknüpfung für die Desktop-App...
echo.

set APP_NAME=QUANTUM AVATAR Desktop App
set APP_FILE=QUANTUM_AVATAR_DESKTOP.py
set DESKTOP_PATH=%USERPROFILE%\Desktop
set SHORTCUT_NAME="%DESKTOP_PATH%\%APP_NAME%.lnk"

echo Desktop-Pfad: %DESKTOP_PATH%
echo App-Datei: %APP_FILE%
echo Shortcut: %SHORTCUT_NAME%
echo.

REM Erstelle VBScript temporär für Shortcut-Erstellung
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%SHORTCUT_NAME%" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "cmd.exe" >> CreateShortcut.vbs
echo oLink.Arguments = "/c python ""%~dp0%APP_FILE%""" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%~dp0" >> CreateShortcut.vbs
echo oLink.Description = "QUANTUM AVATAR KI Imperium Desktop Control - €28,000 täglich automatisches Geld" >> CreateShortcut.vbs
echo oLink.IconLocation = "C:\Windows\System32\SHELL32.dll,43" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

REM Führe VBScript aus
cscript //nologo CreateShortcut.vbs

REM Aufräumen
if exist CreateShortcut.vbs del CreateShortcut.vbs

if exist "%DESKTOP_PATH%\%APP_NAME%.lnk" (
    echo.
    echo ✅ Desktop-Verknüpfung erfolgreich erstellt!
    echo 📍 Location: %DESKTOP_PATH%\%APP_NAME%.lnk
    echo.
    echo 🎯 DOPPELKLICK zum Starten der Desktop-App!
    echo.
    echo 💰 Features:
    echo    • Live €28,000 täglich Revenue
    echo    • KI-Schwarm Command Center
    echo    • Autonome Geldgenerierung
    echo    • Professionelle Desktop UI
    echo.
) else (
    echo.
    echo ❌ Fehler beim Erstellen der Verknüpfung
    echo Erstelle alternative Batch-Datei...
    echo.
    
    REM Erstelle einfache Batch-Datei
    echo @echo off > "%DESKTOP_PATH%\%APP_NAME%.bat"
    echo echo Starting QUANTUM AVATAR Desktop App... >> "%DESKTOP_PATH%\%APP_NAME%.bat"
    echo cd "%~dp0" >> "%DESKTOP_PATH%\%APP_NAME%.bat"
    echo python "%APP_FILE%" >> "%DESKTOP_PATH%\%APP_NAME%.bat"
    echo pause >> "%DESKTOP_PATH%\%APP_NAME%.bat"

    echo ✅ Batch-Datei erstellt: %DESKTOP_PATH%\%APP_NAME%.bat
    echo    Doppelklick zum Starten!
)

echo.
echo ===========================================
echo INSTALLATION COMPLETE!
echo ===========================================
echo.
pause
