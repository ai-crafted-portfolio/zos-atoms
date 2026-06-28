@echo off
chcp 932 > nul
title zos_site_push2

set "LOG=C:\kvba\zos-atoms-site\push2.log"

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Remove-Item -Force -ErrorAction SilentlyContinue 'C:\kvba\zos-atoms-site\.git\index.lock'" > "%LOG%" 2>&1

cd /d "C:\kvba\zos-atoms-site"

git config user.email "shuichisueyoshi@users.noreply.github.com" >> "%LOG%" 2>&1
git config user.name "shuichisueyoshi" >> "%LOG%" 2>&1

git add docs/atoms/ >> "%LOG%" 2>&1
git status --short >> "%LOG%" 2>&1
git commit -m "docs: refresh 62 z/OS atoms + add 14 new atoms (ADR-0108/0109)" >> "%LOG%" 2>&1
set "RC_COMMIT=%errorlevel%"
echo commit RC=%RC_COMMIT% >> "%LOG%"

git push origin main >> "%LOG%" 2>&1
set "RC_PUSH=%errorlevel%"
echo push RC=%RC_PUSH% >> "%LOG%"

echo === DONE %DATE% %TIME% === >> "%LOG%"
exit /b %RC_PUSH%
