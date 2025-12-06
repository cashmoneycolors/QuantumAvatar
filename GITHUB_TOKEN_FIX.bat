@echo off
echo GITHUB TOKEN FIX - QUANTUM AVATAR V5.0
echo =====================================

echo Clearing invalid GitHub token...
set GITHUB_TOKEN=

echo Re-authenticating with GitHub CLI...
gh auth login --web

echo Creating repository with fresh authentication...
gh repo create quantum-avatar-v5 --public --description "QUANTUM AVATAR V5.0 - MAXIMALE QUANTUM STUFE AUTONOM - €100M COMPANY BUILDING" --push --source=.

echo QUANTUM AVATAR V5.0 - GITHUB DEPLOYMENT COMPLETE!
pause