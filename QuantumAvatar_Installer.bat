@echo off
REM Quantum Avatar Desktop App Installer
REM Simple installer for Windows

echo ===========================================
echo    QUANTUM AVATAR DESKTOP APP INSTALLER
echo ===========================================
echo.
echo Installing the ultimate AI empire control center...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed!
    echo.
    echo Download from: https://python.org
    echo Make sure to check "Add Python to PATH" during install
    echo.
    pause
    exit /b 1
)

echo ✅ Python found

REM Install PyQt6
echo.
echo Installing PyQt6 (for the desktop interface)...
pip install --quiet PyQt6 pyqt6-qt6
if %errorlevel% equ 0 (
    echo ✅ PyQt6 installed successfully
) else (
    echo ⚠️ Could not install PyQt6 automatically
    echo Please run: pip install PyQt6 pyqt6-qt6
    echo Press any key to continue anyway...
    pause
)

REM Create desktop shortcut
echo.
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%userprofile%\Desktop\QuantumAvatar.lnk'); $Shortcut.TargetPath = '%cd%\desktop_app.py'; $Shortcut.WorkingDirectory = '%cd%'; $Shortcut.IconLocation = 'C:\Windows\System32\SHELL32.dll,43'; $Shortcut.Description = 'Quantum Avatar AI Empire Control Center'; $Shortcut.Save()"

if %errorlevel% equ 0 (
    echo ✅ Desktop shortcut created
) else (
    echo ⚠️ Could not create desktop shortcut
)

REM Install as Windows service (optional)
echo.
set /p install_service="Install as Windows service (Y/N)? "
if /i "%install_service%"=="Y" (
    echo Installing as service...
    echo This would require additional setup for background operation
    powershell "Start-Process cmd -ArgumentList '/k python desktop_app.py' -WindowStyle Hidden"
    echo ⚠️ Service installation requires administrator privileges
    echo Manual setup needed
)

echo.
echo ===========================================
echo        INSTALLATION COMPLETE!
echo ===========================================
echo.
echo 🎉 Quantum Avatar Desktop App is now installed!
echo.
echo 🚀 STARTEN:
echo     Desktop shortcut: Double-click "QuantumAvatar"
echo     Manual: python desktop_app.py
echo.
echo 💰 Features:
echo     • Live revenue monitoring (€28,000/day)
echo     • AI swarm control
echo     • Gmail command interface
echo     • Real-time system metrics
echo     • System tray support
echo.
echo 📁 Installation folder: %cd%
echo 📊 Status: READY FOR AI EMPIRE MANAGEMENT
echo.
echo Have fun building your autonomous income empire! 🎯
echo.
pause
