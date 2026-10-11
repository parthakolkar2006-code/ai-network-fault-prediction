@echo off
title Network Fault AI - Orchestrator
cd /d "%~dp0"
echo ========================================================
echo Launching Explainable AI Network Monitoring Platform
echo ========================================================

echo Starting Backend Server on http://localhost:8000 ...
start "Network Fault AI - Backend" cmd /k "start_backend.bat"

timeout /t 3 /nobreak >nul

echo Starting Frontend NOC Dashboard on http://localhost:5173 ...
start "Network Fault AI - Frontend" cmd /k "start_frontend.bat"

echo.
echo System launched!
echo Access Dashboard: http://localhost:5173
echo Access API Docs:  http://localhost:8000/docs
echo.
pause
