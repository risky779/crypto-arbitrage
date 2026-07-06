@echo off
chcp 65001 > nul
echo ========================================
echo Auto Trading Bot (OKX)
echo ========================================
echo.
echo Starting automatic arbitrage trading...
echo.

python -u auto_trade_okx.py

pause
