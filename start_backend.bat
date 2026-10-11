@echo off
title Network Fault AI - Backend Server
cd /d "%~dp0backend"
echo ========================================================
echo Starting Network Fault AI Backend (FastAPI + WebSockets)
echo ========================================================

set PYTHONIOENCODING=utf-8
set PYTHONPATH=%CD%

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
