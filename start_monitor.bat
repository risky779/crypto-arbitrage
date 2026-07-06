@echo off
cd /d "%~dp0"
chcp 65001 >nul
echo ================================================
echo 3-Exchange Arbitrage Monitor Starting
echo Binance / Upbit / Bithumb
echo Press Ctrl+C to exit
echo ================================================
echo.
python -u arbitrage_monitor.py
pause
