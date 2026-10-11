@echo off
title Network Fault AI - Frontend Dashboard
cd /d "%~dp0frontend"
echo ========================================================
echo Starting Network Fault AI Frontend (React + Vite)
echo ========================================================

cmd.exe /c "npx vite --host"
pause
