@echo off
REM Windows-friendly file counting
echo Counting Python files...
for /f %%c in ('dir /b /s *.py 2^>nul ^| find /c ".py"') do echo Total Python files: %%c

echo.
echo Listing main project files...
dir /b *.py *.md *.json *.bat *.txt 2>nul | findstr /v /i "cache" | findstr /v /i "pyc"
