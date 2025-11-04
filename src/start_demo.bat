@echo off
echo ============================================================
echo        Gamify Achievement System - Demo Launcher
echo ============================================================
echo.
echo Este script iniciara la aplicacion de demo Flask
echo Asegurate de que Django este corriendo en http://localhost:8000
echo.
pause
echo.
echo Iniciando Flask Demo App...
echo.
cd /d "%~dp0"
uv run python demo_app.py
