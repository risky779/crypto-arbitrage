@echo off
cd /d "%~dp0"
chcp 65001 >nul
echo ================================================
echo 3-Exchange Arbitrage Monitor Starting
echo OKX / Upbit / Bithumb
echo Press Ctrl+C to exit
echo ================================================
echo.
python -u arbitrage_monitor_okx.py
pause
