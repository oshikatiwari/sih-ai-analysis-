@echo off
title SIH26003 Dementia Platform - Local AI Demo Launcher
cls
echo =========================================================================
echo   SIH26003: AI Cognitive Gaming & Memory Platform - Local Launcher
echo =========================================================================
echo.
echo [1/2] Opening Interactive Live Web Demo in your default browser...
start "" "%~dp0open_web_demo.html"
echo [2/2] Launching Python AI Telemetry Evaluation Suite...
echo.
cd /d "%~dp0ml_engine"
python evaluate_telemetry.py
echo.
echo =========================================================================
echo  Launching Live Interactive Python AI Tester...
echo =========================================================================
echo.
python interactive_test.py
pause
