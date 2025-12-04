@echo off
echo QUANTUM AVATAR - Python Access Fix
echo ===================================

echo 1. Checking Windows Defender...
powershell -Command "Get-MpPreference | Select-Object -Property ExclusionPath"

echo.
echo 2. Adding Python to Windows Defender Exclusions...
powershell -Command "Add-MpPreference -ExclusionPath 'C:\Python314'"
powershell -Command "Add-MpPreference -ExclusionPath 'C:\QuantumAvatar'"

echo.
echo 3. Testing Python access...
C:\Python314\python.exe --version

echo.
echo 4. If still blocked, manually add to antivirus exclusions:
echo    - C:\Python314\
echo    - C:\QuantumAvatar\
echo.
pause