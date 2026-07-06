#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bithumb - OKX Hedged Transfer Arbitrage Bot
------------------------------------------
Performs transfer-based arbitrage with delta-neutral price risk mitigation:
1. Signal: Bithumb Price (Spot) < OKX Price (Futures/Spot) by >= 2.5%
2. Open: Buy Spot on Bithumb + Short Futures on OKX (Delta Neutral)
3. Transfer: Withdraw from Bithumb to OKX deposit address
4. Await: Periodically checks OKX balances for deposit confirmation
5. Close: Sell Spot on OKX + Cover Futures Short on OKX -> Locks in profit in USDT.
"""

import os
import sys
import io
import time
import json
import logging
import threading
import requests
from pathlib import Path
from datetime import datetime, timezone
import math
from dotenv import load_dotenv
import ccxt

from bithumb_api_v2 import BithumbAPIv2
from auth import generate_token

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Setup Logging
LOG_DIR = Path("D:/work/crypto-arbitrage/logs")
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("D:/work/crypto-arbitrage/logs/transfer_arb.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

ENV_PATH = Path("D:/work/crypto-arbitrage/.env")
load_dotenv(ENV_PATH)

# ========== BOT SETTINGS ==========
PAPER_MODE = False          # Real money execution enabled

COINS = ['MMT', 'SUI', 'XRP', 'TRX', 'SOL', 'ADA']
BITHUMB_NET_TYPES = {
    'MMT': 'SUI',
    'SUI': 'SUI',
    'XRP': 'XRP',
    'TRX': 'TRX',
    'SOL': 'SOL',
    'ADA': 'ADA'
}
BITHUMB_WITHDRAW_FEES = {
    'MMT': 0.0,
    'SUI': 0.009,
    'XRP': 0.4,
    'TRX': 0.9,
    'SOL': 0.009,
    'ADA': 0.45
}

# Travel Rule recipient settings (required for Bithumb withdrawals to external exchanges)
TRAVEL_RULE_EXCHANGE = 'OKX'
TRAVEL_RULE_RECEIVER_TYPE = 'personal'
TRAVEL_RULE_RECEIVER_KO_NAME = '류명하'
TRAVEL_RULE_RECEIVER_EN_NAME = 'MYUNGHA RYU'



MIN_TRADE_USDT = 4.0        # Minimum order size (about 6,000 KRW)
MAX_TRADE_USDT = 50.0       # Max limit per trade
TRADE_RATIO = 0.90          # Use 90% of available KRW balance
COIN_MIN_NET_SPREADS = {
    'MMT': 3.0,
    'SUI': 2.0,
    'XRP': 2.0,
    'TRX': 2.0,
    'SOL': 2.0,
    'ADA': 2.0
}
CHECK_INTERVAL_SEC = 2      # Signal scan interval
MONITOR_INTERVAL_SEC = 10   # Pending transfer monitor interval
REBALANCE_CHECK_INTERVAL_SEC = 60 # Check rebalance every 60 seconds

# OKX Deposit Addresses (For actual transfers - Add your actual OKX deposit addresses here if running in Live)
# Note: Keep tags/memo if coin requires it (e.g. XRP/XLM)
OKX_DEPOSIT_ADDRESSES = {
    'ALLO': os.getenv('OKX_DEPOSIT_ADDR_ALLO', ''),
    'MMT': os.getenv('OKX_DEPOSIT_ADDR_MMT', ''),
    'ACE': os.getenv('OKX_DEPOSIT_ADDR_ACE', ''),
}

BITHUMB_FEE = 0.04          # Bithumb spot buy fee %
OKX_SPOT_FEE = 0.10         # OKX spot sell fee %
OKX_FUTURES_FEE = 0.05      # OKX futures open/close fee %
# Sum of all execution fees (Buy Spot + Sell Spot + Open Short + Cover Short)
TOTAL_FEE = BITHUMB_FEE + OKX_SPOT_FEE + (OKX_FUTURES_FEE * 2)

STATE_FILE = Path("D:/work/crypto-arbitrage/logs/transfer_arb_state.json")
LOG_HISTORY_FILE = 'okx_bithumb_transfer_history.json'
# ==================================

class HedgedTransferArb:
    def __init__(self):
        self.okx = ccxt.okx({
            'apiKey': os.getenv('OKX_API_KEY'),
            'secret': os.getenv('OKX_SECRET_KEY'),
            'password': os.getenv('OKX_PASSPHRASE'),
            'enableRateLimit': True,
        })
        self.bithumb = BithumbAPIv2()
        
        # Public clients for scanning
        self.okx_pub = ccxt.okx({'enableRateLimit': True})
        self.bithumb_pub = ccxt.bithumb({'enableRateLimit': True})
        
        self.usd_krw = 1380.0
        self._usd_krw_updated_at = 0
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        
        # Use Reentrant Lock to allow same-thread multiple acquisitions
        self.lock = threading.RLock()
        self.state = self.load_state()
        
        # Verify and filter coins that have futures markets on OKX
        self.coins = COINS
        try:
            logger.info("🔍 Checking OKX futures markets compatibility...")
            self.okx_pub.load_markets()
            valid_coins = []
            for coin in COINS:
                futures_symbol = f"{coin}/USDT:USDT"
                if futures_symbol in self.okx_pub.markets:
                    valid_coins.append(coin)
                else:
                    logger.warning(f"⚠️ Excluding {coin}: OKX does not have futures symbol {futures_symbol}")
            self.coins = valid_coins
            logger.info(f"✅ Verified coins for arbitrage: {self.coins}")
        except Exception as e:
            logger.error(f"❌ Failed to load OKX markets for coin filtering: {e}. Will monitor all configured coins.")

    def load_state(self):
        with self.lock:
            if STATE_FILE.exists():
                try:
                    return json.loads(STATE_FILE.read_text(encoding="utf-8"))
                except Exception:
                    pass
            return {"pending_transfers": {}}

    def save_state(self):
        with self.lock:
            STATE_FILE.write_text(json.dumps(self.state, indent=2), encoding="utf-8")

    def _notify(self, title, msg, color=0x00b0f4):
        if not self.webhook_url:
            logger.info(f"[{title}] {msg}")
            return
        try:
            payload = {
                'embeds': [{
                    'title': title,
                    'description': msg,
                    'color': color,
                    'timestamp': datetime.utcnow().isoformat()
                }]
            }
            requests.post(self.webhook_url, json=payload, timeout=5)
        except Exception as e:
            logger.error(f"Failed to send discord notification: {e}")

    def _get_usd_krw(self):
        if time.time() - self._usd_krw_updated_at > 60:
            try:
                r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=5)
                rate = r.json().get("rates", {}).get("KRW")
                if rate:
                    self.usd_krw = float(rate)
                    self._usd_krw_updated_at = time.time()
            except Exception:
                pass
        return self.usd_krw

    def get_rounded_size(self, symbol, coin_size):
        """Rounds size to match OKX contract size requirements."""
        self.okx_pub.load_markets()
        market = self.okx_pub.market(symbol)
        contract_size = market.get('contractSize', 1.0)
        
        raw_contracts = coin_size / contract_size
        rounded_contracts = float(self.okx_pub.amount_to_precision(symbol, raw_contracts))
        
        min_contracts = market.get('limits', {}).get('amount', {}).get('min', 1.0)
        if rounded_contracts < min_contracts:
            rounded_contracts = min_contracts
            
        rounded_size = rounded_contracts * contract_size
        return rounded_size, rounded_contracts, contract_size

    def check_spread(self, coin):
        usd_krw = self._get_usd_krw()
        o_tick = self.okx_pub.fetch_ticker(f'{coin}/USDT')
        b_tick = self.bithumb_pub.fetch_ticker(f'{coin}/KRW')
        
        okx_usdt = o_tick.get('last')
        bithumb_krw = b_tick.get('last')
        
        if okx_usdt is None or bithumb_krw is None or bithumb_krw == 0:
            return 0.0, 0.0, 0.0, usd_krw
            
        okx_krw = okx_usdt * usd_krw
        raw_spread = (okx_krw - bithumb_krw) / bithumb_krw * 100
        net_spread = raw_spread - TOTAL_FEE
        
        return net_spread, okx_usdt, bithumb_krw, usd_krw

    def get_entry_amount(self, coin, usd_krw):
        try:
            bb = self.bithumb.get_balance()
            krw_free = bb.get('KRW', {}).get('free', 0)
            
            # Use TRADE_RATIO
            avail_krw = krw_free * TRADE_RATIO
            trade_usdt = avail_krw / usd_krw
            
            # Apply bounds
            trade_usdt = min(trade_usdt, MAX_TRADE_USDT)
            
            if trade_usdt < MIN_TRADE_USDT:
                return 0, f"Insufficient Bithumb KRW cash: {krw_free:,.0f} KRW"
            return trade_usdt, "OK"
        except Exception as e:
            return 0, f"Failed to check Bithumb balance: {e}"

    def open_hedged_trade(self, coin, net_spread, okx_usdt, bithumb_krw, usd_krw, trade_usdt):
        logger.info(f"⚡ [OPENING HEDGE] Bithumb buy + OKX short for {coin}... Size: ${trade_usdt:.2f}")
        
        spot_symbol = f"KRW-{coin}"
        futures_symbol = f"{coin}/USDT:USDT"
        
        raw_coin_qty = (trade_usdt * usd_krw) / bithumb_krw
        
        # Round OKX futures contracts size
        rounded_size, contracts, contract_size = self.get_rounded_size(futures_symbol, raw_coin_qty)
        actual_krw_needed = rounded_size * bithumb_krw
        
        logger.info(f"  Target spot size: {raw_coin_qty:.4f} -> OKX Rounded Size: {rounded_size:.4f} ({contracts} contracts)")
        
        # Check OKX USDT margin
        try:
            okx_bal = self.okx.fetch_balance()
            usdt_free = okx_bal.get('USDT', {}).get('free', 0)
            required_margin = (rounded_size * okx_usdt) * 0.45 # 45% margin safety buffer
            if usdt_free < required_margin:
                logger.error(f"  [Abort] Insufficient OKX USDT margin. Needed: ${required_margin:.2f}, Free: ${usdt_free:.2f}")
                return False
        except Exception as e:
            logger.error(f"  [Abort] Failed to fetch OKX balance: {e}")
            return False

        out = {}
        # Double check execution threads
        def buy_bithumb_thread():
            try:
                if PAPER_MODE:
                    out['bithumb'] = {'status': 'paper', 'amount': rounded_size, 'cost_krw': actual_krw_needed}
                    return
                res = self.bithumb.market_buy(spot_symbol, actual_krw_needed)
                out['bithumb'] = {
                    'status': 'ok',
                    'order_id': res.get('order_id', 'N/A'),
                    'amount': rounded_size,
                    'cost_krw': actual_krw_needed
                }
            except Exception as e:
                out['bithumb'] = {'status': 'error', 'error': str(e)}

        def short_okx_thread():
            try:
                if PAPER_MODE:
                    out['okx'] = {'status': 'paper', 'contracts': contracts, 'price': okx_usdt}
                    return
                # Check pos mode (long_short_mode vs net_mode)
                pos_mode = 'net_mode'
                try:
                    config = self.okx.private_get_account_config()
                    pos_mode = config['data'][0]['posMode']
                except Exception:
                    pass
                params = {}
                if pos_mode == 'long_short_mode':
                    params['posSide'] = 'short'
                
                # Set leverage to 3x
                try:
                    self.okx.set_leverage(3, futures_symbol, {'mgnMode': 'cross'})
                except Exception:
                    pass
                    
                order = self.okx.create_market_sell_order(futures_symbol, contracts, params)
                out['okx'] = {
                    'status': 'ok',
                    'order_id': order['id'],
                    'price': order.get('average') or okx_usdt,
                    'contracts': contracts
                }
            except Exception as e:
                out['okx'] = {'status': 'error', 'error': str(e)}

        t1 = threading.Thread(target=buy_bithumb_thread)
        t2 = threading.Thread(target=short_okx_thread)
        t1.start(); t2.start()
        t1.join(); t2.join()

        bithumb_ok = out.get('bithumb', {}).get('status') in ('ok', 'paper')
        okx_ok = out.get('okx', {}).get('status') in ('ok', 'paper')
        success = bithumb_ok and okx_ok

        if not success:
            logger.critical(f"🚨 ENTRY FAILURE on one side! Bithumb Spot Buy: {bithumb_ok} | OKX Futures Short: {okx_ok}")
            # Try manual rollback
            try:
                if bithumb_ok and not okx_ok and not PAPER_MODE:
                    logger.info("  Attempting rollback: Selling Bithumb Spot...")
                    self.bithumb.market_sell(spot_symbol, rounded_size)
                elif not bithumb_ok and okx_ok and not PAPER_MODE:
                    logger.info("  Attempting rollback: Covering OKX Short...")
                    pos_mode = 'net_mode'
                    try:
                        config = self.okx.private_get_account_config()
                        pos_mode = config['data'][0]['posMode']
                    except Exception:
                        pass
                    params = {}
                    if pos_mode == 'long_short_mode':
                        params['posSide'] = 'short'
                    self.okx.create_market_buy_order(futures_symbol, contracts, params)
            except Exception as rollback_err:
                logger.critical(f"  [CRITICAL] Rollback failed! Manual resolution required: {rollback_err}")
            return False

        # Save pending transfer state thread-safely
        with self.lock:
            self.state["pending_transfers"][coin] = {
                "coin": coin,
                "qty": rounded_size,
                "contracts": contracts,
                "bithumb_buy_price": bithumb_krw,
                "okx_short_price": okx_usdt if PAPER_MODE else out['okx']['price'],
                "usd_krw": usd_krw,
                "net_spread": net_spread,
                "status": "WAITING_WITHDRAW",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "paper": PAPER_MODE
            }
            self.save_state()

        mode_str = "[PAPER]" if PAPER_MODE else "[LIVE]"
        msg = (f"🎉 {mode_str} Hedge Entry successfully opened!\n"
               f"• Coin: {coin}\n"
               f"• Bought Spot (Bithumb): {rounded_size:.4f} {coin} @ {bithumb_krw:,.0f} KRW\n"
               f"• Shorted Futures (OKX): {contracts} contracts @ ${okx_usdt:.4f}\n"
               f"• Est Net Spread: {net_spread:+.2f}%")
        logger.info(msg)
        self._notify("🔓 Hedged Arbitrage Opened", msg, color=0x00ff00)
        
        # Initiate transfer (separate thread/step)
        threading.Thread(target=self.process_withdrawal, args=(coin,), daemon=True).start()
        return True

    def process_withdrawal(self, coin, force_retry=False):
        with self.lock:
            p = self.state["pending_transfers"].get(coin)
            if not p:
                return
            if not force_retry and p["status"] != "WAITING_WITHDRAW":
                return
            qty = p["qty"]

        logger.info(f"📤 [WITHDRAW PROCESS] Initiating withdrawal of {qty} {coin} from Bithumb to OKX...")
        
        if PAPER_MODE:
            logger.info("  [PAPER] Simulating withdrawal transaction. Moving to WAITING_CONFIRM...")
            with self.lock:
                p_curr = self.state["pending_transfers"].get(coin)
                if p_curr:
                    p_curr["status"] = "WAITING_CONFIRM"
                    p_curr["withdraw_tx_simulated_time"] = time.time()
                    self.save_state()
            return

        # Real Mode Withdrawal
        address = OKX_DEPOSIT_ADDRESSES.get(coin)
        tag = None
        
        # On-the-fly OKX deposit address lookup if not configured in .env
        if not address:
            try:
                addr_info = self.okx.fetch_deposit_address(coin)
                address = addr_info.get('address')
                tag = addr_info.get('tag')
                logger.info(f"🔑 Dynamically fetched OKX deposit address for {coin}: {address} (Tag: {tag})")
            except Exception as e:
                logger.error(f"Failed to fetch OKX deposit address dynamically for {coin}: {e}")
                
        if not address:
            logger.error(f"  [Withdraw Abort] OKX Deposit Address not found for {coin}. Please manually transfer!")
            self._notify("⚠️ Withdrawal Address Missing", f"OKX deposit address for {coin} could not be resolved.\nPlease manually transfer {qty:.4f} {coin} immediately to avoid carry costs!", color=0xffa500)
            with self.lock:
                p_curr = self.state["pending_transfers"].get(coin)
                if p_curr:
                    p_curr["status"] = "MANUAL_TRANSFER_REQUIRED"
                    self.save_state()
            return

        try:
            # Query actual free balance of the coin on Bithumb to withdraw maximum amount subtracting fee
            bal = self.bithumb.get_balance()
            coin_free = bal.get(coin, {}).get('free', 0)
            if coin_free <= 0:
                raise Exception(f"No free balance of {coin} found on Bithumb. Balance: {bal}")
                
            if coin == 'MMT':
                # 1.0% proportional fee + buffer
                withdraw_qty = coin_free / 1.011
            else:
                fee = BITHUMB_WITHDRAW_FEES.get(coin, 0.0)
                withdraw_qty = coin_free - fee
                
            withdraw_qty = round(withdraw_qty, 4)
            if withdraw_qty <= 0:
                raise Exception(f"Calculated withdrawable quantity {withdraw_qty} is <= 0 (Free: {coin_free})")

            logger.info(f"📤 [WITHDRAW PROCESS] Executing Bithumb withdrawal of {withdraw_qty} {coin} (Free balance: {coin_free})...")

            # Execute Bithumb Withdraw with network type and Travel Rule recipient details
            net_type = BITHUMB_NET_TYPES.get(coin, coin)
            res = self.bithumb.withdraw(
                coin, withdraw_qty, address, net_type,
                secondary_address=tag,
                exchange_name=TRAVEL_RULE_EXCHANGE,
                receiver_type=TRAVEL_RULE_RECEIVER_TYPE,
                receiver_ko_name=TRAVEL_RULE_RECEIVER_KO_NAME,
                receiver_en_name=TRAVEL_RULE_RECEIVER_EN_NAME
            )

            logger.info(f"  ✅ [Withdraw Successful] Bithumb Tx ID: {res.get('txid', 'N/A')}")
            with self.lock:
                p_curr = self.state["pending_transfers"].get(coin)
                if p_curr:
                    p_curr["status"] = "WAITING_CONFIRM"
                    p_curr["qty"] = withdraw_qty # Update state to actual withdrawn amount
                    p_curr["bithumb_withdraw_result"] = res
                    self.save_state()
        except Exception as e:
            logger.error(f"  [Withdraw Failed] Bithumb withdraw request failed: {e}. Please withdraw MANUALLY immediately!")
            self._notify("🚨 Bithumb Withdraw Request Failed", f"Failed to withdraw {qty:.4f} {coin} automatically: {e}.\nPlease manually withdraw to OKX address '{address}' IMMEDIATELY!", color=0xff0000)
            with self.lock:
                p_curr = self.state["pending_transfers"].get(coin)
                if p_curr:
                    p_curr["status"] = "MANUAL_TRANSFER_REQUIRED"
                    self.save_state()

    def check_incoming_deposits(self):
        """Monitors pending transfers and triggers closures if deposit is confirmed."""
        with self.lock:
            pending = list(self.state.get("pending_transfers", {}).keys())
        
        if not pending:
            return

        for coin in pending:
            with self.lock:
                p = self.state["pending_transfers"].get(coin)
                if not p:
                    continue
                status = p["status"]
                is_paper = p.get("paper", True)
                qty = p["qty"]
                ts_str = p.get("timestamp")
            
            # Auto-retry withdrawal if 24 hours have elapsed
            if status == "MANUAL_TRANSFER_REQUIRED" and not is_paper and ts_str:
                try:
                    from datetime import datetime, timezone
                    entry_time = datetime.fromisoformat(ts_str)
                    elapsed = (datetime.now(timezone.utc) - entry_time).total_seconds()
                    # 24 hours + 5 minutes buffer = 86700 seconds
                    if elapsed >= 86700:
                        last_retry = p.get("last_withdraw_retry_time", 0)
                        if time.time() - last_retry > 1800: # Retry every 30 minutes
                            logger.info(f"🔄 [AUTO-RETRY WITHDRAW] 24 hours elapsed. Retrying automatic Bithumb-to-OKX withdrawal for {qty:.4f} {coin}...")
                            with self.lock:
                                p_curr = self.state["pending_transfers"].get(coin)
                                if p_curr:
                                    p_curr["last_withdraw_retry_time"] = time.time()
                                    self.save_state()
                            threading.Thread(target=self.process_withdrawal, args=(coin, True), daemon=True).start()
                except Exception as e:
                    logger.error(f"Error checking withdrawal retry: {e}")
            
            if status == "WAITING_WITHDRAW":
                continue
                
            if status in ("WAITING_CONFIRM", "MANUAL_TRANSFER_REQUIRED"):
                logger.info(f"⏳ Monitoring Deposit: Awaiting {qty:.4f} {coin} on OKX (Status: {status})...")
                
                if is_paper:
                    # In paper mode, simulate transfer taking 60 seconds
                    sim_time = p.get("withdraw_tx_simulated_time", 0)
                    if time.time() - sim_time > 60:
                        logger.info(f"  [PAPER] Simulation deposit confirmed for {coin}!")
                        with self.lock:
                            p_curr = self.state["pending_transfers"].get(coin)
                            if p_curr and p_curr["status"] in ("WAITING_CONFIRM", "MANUAL_TRANSFER_REQUIRED"):
                                p_curr["status"] = "ARRIVED"
                                self.save_state()
                else:
                    # Real Mode: Fetch OKX spot balance to confirm deposit
                    try:
                        okx_bal = self.okx.fetch_balance()
                        free_qty = okx_bal.get(coin, {}).get('free', 0)
                        
                        if free_qty >= qty * 0.98:
                            logger.info(f"  ✅ [Deposit Confirmed] {free_qty:.4f} {coin} detected in OKX Spot Balance!")
                            with self.lock:
                                p_curr = self.state["pending_transfers"].get(coin)
                                if p_curr and p_curr["status"] in ("WAITING_CONFIRM", "MANUAL_TRANSFER_REQUIRED"):
                                    p_curr["status"] = "ARRIVED"
                                    self.save_state()
                        else:
                            # Keep waiting
                            pass
                    except Exception as e:
                        logger.warning(f"  Failed to fetch OKX balance to check deposit: {e}")

            # Check if status has become ARRIVED, and if so, close the hedge
            with self.lock:
                p_curr = self.state["pending_transfers"].get(coin)
                is_arrived = p_curr and p_curr["status"] == "ARRIVED"
                
            if is_arrived:
                self.close_hedged_trade(coin)

    def close_hedged_trade(self, coin):
        with self.lock:
            p = self.state["pending_transfers"].get(coin)
            if not p:
                return
            qty = p["qty"]
            contracts = p["contracts"]
            is_paper = p.get("paper", True)
            bithumb_buy_price = p['bithumb_buy_price']
            okx_short_price = p['okx_short_price']
            usd_krw = p['usd_krw']
            net_spread = p['net_spread']
            
        spot_symbol = f"{coin}/USDT"
        futures_symbol = f"{coin}/USDT:USDT"
        
        logger.info(f"🔒 [CLOSING HEDGE] Taking profit for {coin} on OKX... Size: {qty} (Contracts: {contracts})")
        
        out = {}
        
        def sell_spot_okx_thread():
            try:
                if is_paper:
                    ticker = self.okx_pub.fetch_ticker(spot_symbol)
                    out['spot'] = {'status': 'paper', 'price': ticker['last'], 'proceeds_usdt': qty * ticker['last']}
                    return
                order = self.okx.create_market_sell_order(spot_symbol, qty)
                out['spot'] = {
                    'status': 'ok',
                    'order_id': order['id'],
                    'price': order.get('average') or order.get('price'),
                    'proceeds_usdt': order.get('cost')
                }
            except Exception as e:
                out['spot'] = {'status': 'error', 'error': str(e)}

        def cover_short_okx_thread():
            try:
                if is_paper:
                    ticker = self.okx_pub.fetch_ticker(futures_symbol)
                    out['futures'] = {'status': 'paper', 'price': ticker['last']}
                    return
                pos_mode = 'net_mode'
                try:
                    config = self.okx.private_get_account_config()
                    pos_mode = config['data'][0]['posMode']
                except Exception:
                    pass
                params = {}
                if pos_mode == 'long_short_mode':
                    params['posSide'] = 'short'
                
                order = self.okx.create_market_buy_order(futures_symbol, contracts, params)
                out['futures'] = {
                    'status': 'ok',
                    'order_id': order['id'],
                    'price': order.get('average') or order.get('price')
                }
            except Exception as e:
                out['futures'] = {'status': 'error', 'error': str(e)}

        t1 = threading.Thread(target=sell_spot_okx_thread)
        t2 = threading.Thread(target=cover_short_okx_thread)
        t1.start(); t2.start()
        t1.join(); t2.join()

        spot_ok = out.get('spot', {}).get('status') in ('ok', 'paper')
        futures_ok = out.get('futures', {}).get('status') in ('ok', 'paper')
        success = spot_ok and futures_ok

        if not success:
            logger.critical(f"🚨 [CRITICAL ALERT] Profit taking close failed on one side! Spot Sell: {spot_ok} | Futures Cover: {futures_ok}")
            self._notify("🚨 PROFIT TAKING CLOSE FAILURE!", f"Arbitrage leg close failed for {coin}.\nSpot status: {out.get('spot')}\nFutures status: {out.get('futures')}\nMANUAL RESOLUTION REQUIRED IMMEDIATELY!", color=0xff0000)
            with self.lock:
                p_curr = self.state["pending_transfers"].get(coin)
                if p_curr:
                    p_curr["status"] = "CLOSE_FAILED"
                    self.save_state()
            return

        # Calculate Profit with fallback for None prices
        spot_sell_price = out['spot'].get('price')
        if spot_sell_price is None:
            try:
                order_id = out['spot'].get('order_id')
                if order_id and not is_paper:
                    fetched_order = self.okx.fetch_order(order_id, spot_symbol)
                    spot_sell_price = fetched_order.get('average') or fetched_order.get('price')
            except Exception as e:
                logger.warning(f"Failed to fetch spot order details for price fallback: {e}")
            if spot_sell_price is None:
                try:
                    ticker = self.okx_pub.fetch_ticker(spot_symbol)
                    spot_sell_price = ticker['last']
                except Exception as e:
                    logger.warning(f"Failed to fetch spot ticker for price fallback: {e}")
                    spot_sell_price = okx_short_price

        futures_cover_price = out['futures'].get('price')
        if futures_cover_price is None:
            try:
                order_id = out['futures'].get('order_id')
                if order_id and not is_paper:
                    fetched_order = self.okx.fetch_order(order_id, futures_symbol)
                    futures_cover_price = fetched_order.get('average') or fetched_order.get('price')
            except Exception as e:
                logger.warning(f"Failed to fetch futures order details for price fallback: {e}")
            if futures_cover_price is None:
                try:
                    ticker = self.okx_pub.fetch_ticker(futures_symbol)
                    futures_cover_price = ticker['last']
                except Exception as e:
                    logger.warning(f"Failed to fetch futures ticker for price fallback: {e}")
                    futures_cover_price = okx_short_price
        
        spot_pnl_usd = (spot_sell_price - (bithumb_buy_price / usd_krw)) * qty
        futures_pnl_usd = (okx_short_price - futures_cover_price) * qty
        actual_profit_usd = spot_pnl_usd + futures_pnl_usd
        
        history_record = {
            'time': datetime.now().isoformat(),
            'coin': coin,
            'qty': qty,
            'bithumb_buy_price_krw': bithumb_buy_price,
            'okx_short_price_usd': okx_short_price,
            'okx_spot_sell_price_usd': spot_sell_price,
            'okx_futures_cover_price_usd': futures_cover_price,
            'spot_pnl_usd': round(spot_pnl_usd, 4),
            'futures_pnl_usd': round(futures_pnl_usd, 4),
            'actual_profit_usd': round(actual_profit_usd, 4),
            'net_spread_entered': net_spread,
            'paper': is_paper
        }
        
        try:
            history = json.loads(Path(LOG_HISTORY_FILE).read_text(encoding="utf-8"))
        except Exception:
            history = []
        history.append(history_record)
        Path(LOG_HISTORY_FILE).write_text(json.dumps(history, indent=2), encoding="utf-8")

        # Delete pending transfer thread-safely
        with self.lock:
            if coin in self.state["pending_transfers"]:
                del self.state["pending_transfers"][coin]
                self.save_state()

        mode_str = "[PAPER]" if is_paper else "[LIVE]"
        msg = (f"🎉 {mode_str} Arbitrage successfully CLOSED & locked profit!\n"
               f"• Coin: {coin}\n"
               f"• Quantity: {qty:.4f} {coin}\n"
               f"• Actual Net Profit: **${actual_profit_usd:.4f} USDT** (approx {actual_profit_usd * usd_krw:,.0f} KRW)")
        logger.info(msg)
        self._notify("🔒 Hedged Arbitrage Closed (Profit Locked)", msg, color=0x00ff00)

    def check_and_execute_rebalance(self):
        # Only run in LIVE mode, not in paper mode
        if PAPER_MODE:
            return
            
        # If there are any pending transfers in progress, don't rebalance
        # to avoid locking up USDT that might be needed as collateral
        with self.lock:
            if self.state.get("pending_transfers"):
                return
            if self.state.get("pending_reflow"):
                # We already have a pending reflow in progress!
                return
                
        # Fetch balances
        try:
            # 1. Bithumb KRW
            b_bal = self.bithumb.get_balance()
            bithumb_krw = b_bal.get('KRW', {}).get('free', 0.0)
            
            # 2. OKX USDT Trading & Funding
            o_bal_trading = self.okx.fetch_balance({'type': 'trading'})
            o_bal_funding = self.okx.fetch_balance({'type': 'funding'})
            
            okx_usdt_trading = o_bal_trading.get('USDT', {}).get('free', 0.0)
            okx_usdt_funding = o_bal_funding.get('USDT', {}).get('free', 0.0)
            okx_usdt_total = okx_usdt_trading + okx_usdt_funding
        except Exception as e:
            logger.warning(f"Rebalance check failed to fetch balances: {e}")
            return
            
        usd_krw = self._get_usd_krw()
        total_usd = (bithumb_krw / usd_krw) + okx_usdt_total
        target_okx_usdt = total_usd / 2.0
        
        # We need to transfer back if Bithumb KRW is low (e.g. < 15,000 KRW)
        # AND OKX USDT is significantly above target (e.g. okx_usdt_total - target_okx_usdt > 20.0 USD)
        excess_usdt = okx_usdt_total - target_okx_usdt
        
        if bithumb_krw < 15000 and excess_usdt >= 20.0:
            logger.info(f"⚖️ [AUTO-REBALANCE] Imbalance detected! Bithumb KRW: {bithumb_krw:,.0f} KRW, OKX USDT: {okx_usdt_total:.2f} USDT.")
            logger.info(f"   Excess USDT to return: {excess_usdt:.2f} USDT. Launching background rebalancer...")
            
            # Set state to indicate pending reflow to prevent concurrent triggers
            with self.lock:
                self.state["pending_reflow"] = {
                    "status": "INITIATED",
                    "amount_usdt": excess_usdt,
                    "timestamp": datetime.now().isoformat()
                }
                self.save_state()
                
            # Spawn background thread to perform the transfer
            threading.Thread(target=self.execute_rebalance_thread, args=(excess_usdt, usd_krw), daemon=True).start()

    def get_bithumb_deposit_address(self, coin):
        try:
            api_key = os.getenv("BITHUMB_API_KEY")
            secret_key = os.getenv("BITHUMB_SECRET_KEY")
            
            query = ""
            token = generate_token(api_key, secret_key, query)
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            }
            
            # Get addresses
            r = requests.get("https://api.bithumb.com/v1/deposits/coin_addresses", headers=headers)
            if r.status_code == 200:
                addresses = r.json()
                for addr in addresses:
                    if addr.get('currency') == coin:
                        return addr.get('deposit_address'), addr.get('secondary_address')
                        
            # If not found, generate it!
            logger.info(f"   [+] Deposit address not found for {coin}. Generating new deposit address...")
            query = f"currency={coin}&net_type={coin}"
            token = generate_token(api_key, secret_key, query)
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            }
            body = {
                "currency": coin,
                "net_type": coin
            }
            r = requests.post("https://api.bithumb.com/v1/deposits/generate_coin_address", headers=headers, json=body)
            if r.status_code == 201:
                data = r.json()
                return data.get('deposit_address'), data.get('secondary_address')
                
        except Exception as e:
            logger.error(f"Failed to get or generate Bithumb deposit address for {coin}: {e}")
            
        return None, None

    def execute_rebalance_thread(self, amount_usdt, usd_krw):
        rebalance_coin = 'XRP' # We use XRP as the rebalance vehicle due to very cheap fees and fast speeds
        futures_symbol = f'{rebalance_coin}/USDT:USDT'
        
        try:
            # Check if this is a resumed operation
            with self.lock:
                status = self.state.get("pending_reflow", {}).get("status")
                
            if status != "WAITING_ARRIVAL":
                logger.info(f"⚖️ [REBALANCE THREAD] Buying {amount_usdt:.2f} USDT worth of {rebalance_coin} on OKX Spot + Opening Futures Short...")
                
                # Fetch spot price
                ticker = self.okx_pub.fetch_ticker(f'{rebalance_coin}/USDT')
                price = ticker['last']
                raw_qty = amount_usdt / price
                
                self.okx.load_markets()
                qty_str = self.okx.amount_to_precision(f'{rebalance_coin}/USDT', raw_qty)
                qty = float(qty_str)
                
                # Calculate contract size for hedging
                rounded_size, contracts, contract_size = self.get_rounded_size(futures_symbol, qty)
                
                # 1. Open short position on OKX futures to hedge price risk
                pos_mode = 'net_mode'
                try:
                    config = self.okx.private_get_account_config()
                    pos_mode = config['data'][0]['posMode']
                except Exception:
                    pass
                params = {}
                if pos_mode == 'long_short_mode':
                    params['posSide'] = 'short'
                
                try:
                    self.okx.set_leverage(3, futures_symbol, {'mgnMode': 'cross'})
                except Exception:
                    pass
                
                logger.info(f"   [+] Opening OKX Futures Short: {contracts} contracts ({rounded_size} {rebalance_coin})...")
                order_short = self.okx.create_market_sell_order(futures_symbol, contracts, params)
                logger.info(f"   [+] OKX Futures Short successful. Order ID: {order_short.get('id')}")
                
                # 2. Place market buy order on OKX spot
                order_spot = self.okx.create_market_buy_order(f'{rebalance_coin}/USDT', qty)
                logger.info(f"   [+] OKX Spot Buy successful. Order ID: {order_spot.get('id')}")
                time.sleep(3)
                
                # 3. Get the actual amount of XRP in Trading Account
                bal_trading = self.okx.fetch_balance({'type': 'trading'})
                xrp_trading = bal_trading.get(rebalance_coin, {}).get('free', 0.0)
                
                # 4. Transfer from Trading to Funding
                if xrp_trading > 0.1:
                    transfer_qty = math.floor(xrp_trading * 10000) / 10000.0
                    logger.info(f"   [+] Transferring {transfer_qty:.4f} {rebalance_coin} from Trading to Funding account...")
                    self.okx.transfer(rebalance_coin, transfer_qty, 'trading', 'funding')
                    time.sleep(2)
                    
                # 5. Fetch Funding balance of XRP
                bal_funding = self.okx.fetch_balance({'type': 'funding'})
                xrp_funding = bal_funding.get(rebalance_coin, {}).get('free', 0.0)
                
                # 6. Fetch Bithumb XRP deposit address
                logger.info("   [+] Fetching Bithumb XRP deposit address...")
                bithumb_address, bithumb_tag = self.get_bithumb_deposit_address(rebalance_coin)
                if not bithumb_address:
                    # In case of address failure, try to close the short to avoid holding directional risk
                    logger.warning("   [!] Address lookup failed. Attempting to emergency cover futures short...")
                    params_cover = {}
                    if pos_mode == 'long_short_mode':
                        params_cover['posSide'] = 'short'
                    self.okx.create_market_buy_order(futures_symbol, contracts, params_cover)
                    raise Exception("Failed to get Bithumb deposit address for rebalancing")
                    
                # 7. Execute OKX withdrawal
                withdraw_qty = math.floor((xrp_funding - 0.0105) * 10000) / 10000.0
                logger.info(f"   [+] Executing OKX withdrawal of {withdraw_qty:.4f} {rebalance_coin} to Bithumb {bithumb_address} (Tag: {bithumb_tag})...")
                
                withdrawal = self.okx.withdraw(
                    code=rebalance_coin,
                    amount=withdraw_qty,
                    address=bithumb_address,
                    tag=bithumb_tag,
                    params={
                        'chain': f'{rebalance_coin}-{rebalance_coin}',
                        'fee': '0.01'
                    }
                )
                logger.info(f"   [+] OKX Withdrawal submitted. ID: {withdrawal.get('id')}")
                
                # Update state status to WAITING_ARRIVAL with hedge info
                with self.lock:
                    self.state["pending_reflow"]["status"] = "WAITING_ARRIVAL"
                    self.state["pending_reflow"]["withdraw_qty"] = withdraw_qty
                    self.state["pending_reflow"]["contracts"] = contracts
                    self.state["pending_reflow"]["pos_mode"] = pos_mode
                    self.save_state()
            else:
                with self.lock:
                    p_ref = self.state.get("pending_reflow", {})
                    withdraw_qty = p_ref.get("withdraw_qty", 10.0)
                    contracts = p_ref.get("contracts", 0.0)
                    pos_mode = p_ref.get("pos_mode", "net_mode")
                logger.info(f"⚖️ [REBALANCE THREAD] Resuming monitoring for {withdraw_qty:.4f} {rebalance_coin} arrival (Hedge: {contracts} contracts)...")
                
            # 8. Wait for arrival on Bithumb
            start_time = time.time()
            arrived = False
            
            # Query initial balance of XRP on Bithumb
            b_bal = self.bithumb.get_balance()
            initial_xrp = b_bal.get(rebalance_coin, {}).get('free', 0.0)
            
            while time.time() - start_time < 900: # 15 mins timeout
                time.sleep(15)
                try:
                    c_bal = self.bithumb.get_balance()
                    c_xrp = c_bal.get(rebalance_coin, {}).get('free', 0.0)
                    if c_xrp >= (initial_xrp + withdraw_qty * 0.90) and c_xrp > 0.1:
                        logger.info(f"   [+] {rebalance_coin} Arrived on Bithumb! Quantity: {c_xrp:.4f}")
                        arrived = True
                        break
                except Exception as e:
                    logger.warning(f"Error polling Bithumb balance in rebalance thread: {e}")
                    
            if not arrived:
                raise Exception(f"Timeout waiting for {rebalance_coin} to arrive on Bithumb")
                
            # 9. Sell XRP on Bithumb Spot + Cover OKX Futures Short
            logger.info("   [+] Closing hedge: Selling spot on Bithumb and covering futures short on OKX...")
            
            def sell_spot_bithumb():
                try:
                    sell_qty = round(c_xrp - 0.0001, 4)
                    logger.info(f"     [Bithumb] Selling {sell_qty:.4f} {rebalance_coin}...")
                    self.bithumb.market_sell(f'KRW-{rebalance_coin}', sell_qty)
                    logger.info("     [Bithumb] Market sell successful!")
                except Exception as b_err:
                    logger.error(f"     [Bithumb ERROR] Spot sell failed: {b_err}")
                    
            def cover_short_okx():
                try:
                    params_cover = {}
                    if pos_mode == 'long_short_mode':
                        params_cover['posSide'] = 'short'
                    logger.info(f"     [OKX] Covering {contracts} contracts short on futures...")
                    self.okx.create_market_buy_order(futures_symbol, contracts, params_cover)
                    logger.info("     [OKX] Futures short cover successful!")
                except Exception as o_err:
                    logger.error(f"     [OKX ERROR] Futures cover failed: {o_err}")
                    
            t_s = threading.Thread(target=sell_spot_bithumb)
            t_c = threading.Thread(target=cover_short_okx)
            t_s.start(); t_c.start()
            t_s.join(); t_c.join()
            
            # Clean up rebalance state
            with self.lock:
                if "pending_reflow" in self.state:
                    del self.state["pending_reflow"]
                    self.save_state()
                
            msg = (f"⚖️ [AUTO-REBALANCE] Hedged Rebalancing completed successfully!\n"
                   f"• Returned: ${amount_usdt:.2f} USDT via Hedged {rebalance_coin}\n"
                   f"• Price risk was 100% neutralized during transfer.")
            logger.info(msg)
            self._notify("⚖️ Portfolio Rebalanced (Hedged)", msg, color=0x3498db)
            
        except Exception as e:
            logger.error(f"❌ [REBALANCE ERROR] Rebalance thread failed: {e}")
            # Reset reflow state so we can retry or alert user
            with self.lock:
                if "pending_reflow" in self.state:
                    self.state["pending_reflow"]["status"] = "FAILED"
                    self.state["pending_reflow"]["error"] = str(e)
                    self.save_state()
            self._notify("🚨 Rebalance Failed", f"Auto-rebalance failed: {e}\nCheck logs for details.", color=0xe74c3c)

    def scan_opportunities(self):
        usd_krw = self._get_usd_krw()
        with self.lock:
            pending = list(self.state.get("pending_transfers", {}).keys())

        # 1. Fetch available Bithumb KRW balance (1 private call)
        try:
            b_bal = self.bithumb.get_balance()
            krw_free = b_bal.get('KRW', {}).get('free', 0.0)
        except Exception as e:
            logger.error(f"Failed to fetch Bithumb balance: {e}")
            return

        # 2. Fetch all tickers in bulk (1 Bithumb call + 1 OKX call)
        b_symbols = [f"{coin}/KRW" for coin in self.coins if coin not in pending]
        o_symbols = [f"{coin}/USDT" for coin in self.coins if coin not in pending]
        
        if not b_symbols:
            return
            
        try:
            b_ticks = self.bithumb_pub.fetch_tickers(b_symbols)
            o_ticks = self.okx_pub.fetch_tickers(o_symbols)
        except Exception as e:
            logger.error(f"Failed to fetch tickers in bulk: {e}")
            return

        # 3. Process each coin using cached data
        for coin in self.coins:
            if coin in pending:
                continue
                
            b_symbol = f"{coin}/KRW"
            o_symbol = f"{coin}/USDT"
            
            b_tick = b_ticks.get(b_symbol)
            o_tick = o_ticks.get(o_symbol)
            
            if not b_tick or not o_tick:
                continue
                
            okx_usdt = o_tick.get('last')
            bithumb_krw = b_tick.get('last')
            
            if okx_usdt is None or bithumb_krw is None or bithumb_krw == 0:
                continue
                
            okx_krw = okx_usdt * usd_krw
            raw_spread = (okx_krw - bithumb_krw) / bithumb_krw * 100
            
            # Calculate trade size based on Bithumb cash
            avail_krw = krw_free * TRADE_RATIO
            trade_usdt = avail_krw / usd_krw if usd_krw > 0 else 0.0
            trade_usdt = min(trade_usdt, MAX_TRADE_USDT)
            
            # Check if trade size is enough
            if trade_usdt < MIN_TRADE_USDT:
                continue # Skip signal check since balance is too low
            
            # 1. Trading Fees Friction (Spot Buy + Spot Sell + Futures Open/Close)
            trading_fee_pct = TOTAL_FEE  # 0.24%
            
            # 2. Bithumb Withdrawal Fee Friction (Dynamic % based on Trade Size)
            if coin == 'MMT':
                withdraw_fee_pct = 1.10
            else:
                flat_fee = BITHUMB_WITHDRAW_FEES.get(coin, 0.0)
                flat_fee_usd = flat_fee * okx_usdt
                withdraw_fee_pct = (flat_fee_usd / trade_usdt) * 100 if trade_usdt > 0.0 else 0.0
                
            # 3. Expected Slippage Buffer
            slippage_buffer = 0.15 if coin == 'MMT' else 0.05
            
            total_friction = trading_fee_pct + withdraw_fee_pct + slippage_buffer
            net_spread = raw_spread - total_friction
            
            min_spread = COIN_MIN_NET_SPREADS.get(coin, 2.0)
            if net_spread >= min_spread:
                logger.info(f"🎯 [SIGNAL] Bithumb-OKX Spread {net_spread:+.2f}% detected for {coin} (Threshold: {min_spread:+.2f}%)! Triggering entry...")
                self.open_hedged_trade(coin, net_spread, okx_usdt, bithumb_krw, usd_krw, trade_usdt)

    def run_loop(self):
        logger.info("======================================================================")
        logger.info(f"🤖 Starting Bithumb-OKX Hedged Transfer Arbitrage Bot")
        logger.info(f"   [Mode: {'PAPER/SIMULATION' if PAPER_MODE else 'LIVE'}]")
        logger.info(f"   Monitored coins: {self.coins}")
        logger.info("======================================================================")

        self._notify("🚀 Hedged Transfer Arb Bot Initialized", f"Active Mode: {'PAPER (Simulation)' if PAPER_MODE else 'LIVE (Real Money)'}\nMonitored Coins: {self.coins}")

        # Try to resume withdrawal/monitoring of any pending transactions in state file
        with self.lock:
            pending = self.state.get("pending_transfers", {})
        if pending:
            logger.info(f"🔄 Resuming monitoring for {len(pending)} pending transfers in state...")
            for coin in pending:
                with self.lock:
                    p = pending[coin]
                    status = p["status"]
                if status == "WAITING_WITHDRAW":
                    threading.Thread(target=self.process_withdrawal, args=(coin,), daemon=True).start()

        # Try to resume monitoring of any pending rebalance reflow
        with self.lock:
            pending_reflow = self.state.get("pending_reflow")
        if pending_reflow and pending_reflow.get("status") == "WAITING_ARRIVAL":
            logger.info("🔄 Resuming monitoring for pending rebalance reflow...")
            threading.Thread(target=self.execute_rebalance_thread, args=(pending_reflow.get("amount_usdt", 60.0), self._get_usd_krw()), daemon=True).start()

        last_scan_time = 0
        last_deposit_check_time = 0
        last_rebalance_time = 0

        while True:
            now = time.time()
            
            # 1. Scan for new entries
            if now - last_scan_time >= CHECK_INTERVAL_SEC:
                try:
                    self.scan_opportunities()
                except Exception as e:
                    logger.error(f"Error in scan cycle: {e}")
                last_scan_time = now

            # 2. Check incoming deposits to lock profit
            if now - last_deposit_check_time >= MONITOR_INTERVAL_SEC:
                try:
                    self.check_incoming_deposits()
                except Exception as e:
                    logger.error(f"Error in deposit check cycle: {e}")
                last_deposit_check_time = now

            # 3. Check and execute auto-rebalancing
            if now - last_rebalance_time >= REBALANCE_CHECK_INTERVAL_SEC:
                try:
                    self.check_and_execute_rebalance()
                except Exception as e:
                    logger.error(f"Error in rebalance cycle: {e}")
                last_rebalance_time = now

            time.sleep(1)

if __name__ == '__main__':
    bot = HedgedTransferArb()
    bot.run_loop()
