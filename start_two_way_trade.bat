@echo off
chcp 65001 > nul
echo ========================================
echo Two-Way Trading Bot (No Transfer)
echo ========================================
echo.

python -u two_way_trade_okx.py

pause
