"""
Bithumb-OKX Hedged Transfer Arbitrage Bot Watchdog
Monitors okx_bithumb_transfer_arb.py process.
If the bot process dies, it automatically restarts it.
"""
import subprocess
import sys
import time
import os
from datetime import datetime, timezone
from pathlib import Path

# Reconfigure stdout and stderr to use UTF-8 (fixes cp949 encoding errors on Windows)
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


BOT_SCRIPT = "okx_bithumb_transfer_arb.py"
LOG_FILE = "logs/transfer_arb.log"
ERR_LOG = "logs/transfer_arb_err.log"
WATCHDOG_LOG = Path("logs/bithumb_watchdog.log")
BOT_DIR = r"D:\work\crypto-arbitrage"
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

CHECK_SEC = 30  # Check every 30 seconds

def log_event(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(WATCHDOG_LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception as e:
        print(f"Failed to write to watchdog log: {e}")

def get_bot_pid():
    """Returns the PID of the currently running okx_bithumb_transfer_arb.py process."""
    try:
        out = subprocess.check_output(
            ["wmic", "process", "where",
             f"name='python.exe' and commandline like '%{BOT_SCRIPT}%'",
             "get", "processid"], stderr=subprocess.DEVNULL).decode()
        for line in out.splitlines():
            line = line.strip()
            if line.isdigit():
                return int(line)
    except Exception:
        pass
    return None

def start_bot():
    """Launches the Bithumb bot in a hidden background process."""
    log_event("Attempting to start the Bithumb arbitrage bot...")
    try:
        creationflags = 0
        if os.name == 'nt':  # Windows
            creationflags = 0x08000000  # CREATE_NO_WINDOW
            
        log_out = open(Path(BOT_DIR) / LOG_FILE, "a", encoding="utf-8")
        log_err = open(Path(BOT_DIR) / ERR_LOG, "a", encoding="utf-8")
        
        proc = subprocess.Popen(
            [sys.executable, "-u", BOT_SCRIPT],
            cwd=BOT_DIR,
            stdout=log_out,
            stderr=log_err,
            creationflags=creationflags
        )
        pid = proc.pid
        log_event(f"Successfully started Bithumb bot with PID: {pid}")
        return pid
    except Exception as e:
        log_event(f"Failed to start Bithumb bot: {e}")
        return None

def main():
    log_event("=== Bithumb Watchdog Monitoring Started ===")
    while True:
        try:
            pid = get_bot_pid()
            if not pid:
                log_event("Bithumb bot process not found. Restarting...")
                start_bot()
            else:
                # Bot is running fine
                pass
        except Exception as e:
            log_event(f"Error in watchdog loop: {e}")
            
        time.sleep(CHECK_SEC)

if __name__ == "__main__":
    main()
