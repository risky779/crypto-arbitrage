@echo off
cd /d "%~dp0"
chcp 65001 >nul
echo ================================================
echo Semi-Automated Trading Bot
echo ================================================
echo.
python -u trading_bot.py
pause
