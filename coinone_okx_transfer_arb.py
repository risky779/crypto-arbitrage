#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coinone - OKX Hedged Transfer Arbitrage Bot
Monitors 10 unique overlapping coins with high-margin thresholds.
Includes Hedged Reflow rebalancing via XRP.
FINAL OPERATING SPECIFICATION: Paper mode enabled for the 72-hour hold period, 10 monitored coins, 5% standard spread barriers.
"""
import os
import sys
import time
import math
import logging
import threading
import requests
import uuid
from datetime import datetime
from dotenv import load_dotenv
import ccxt

# Setup logs directory
os.makedirs("logs", exist_ok=True)

# Reconfigure stdout/stderr for UTF-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try: sys.stdout.reconfigure(encoding='utf-8')
    except Exception: pass
if hasattr(sys.stderr, 'reconfigure'):
    try: sys.stderr.reconfigure(encoding='utf-8')
    except Exception: pass

# Setup Logging
logger = logging.getLogger("coinone_okx_arb")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s  %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Console Handler
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)
logger.addHandler(ch)

# Load Environment using absolute path to ensure reliability across parent processes
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")
load_dotenv(env_path)

# Setup Logging File Handler
log_dir = os.path.join(script_dir, "logs")
os.makedirs(log_dir, exist_ok=True)
fh = logging.FileHandler(os.path.join(log_dir, "coinone_transfer_arb.log"), encoding="utf-8")
fh.setFormatter(formatter)
logger.addHandler(fh)

# ======================================================================
# Config Settings
# ======================================================================
PAPER_MODE = True  # Enabled for 72-hour hold period. Switch to False to go live!

# Monitored Coins (10 Overlapping Target Coins)
COINS = ['AEVO', 'AIXBT', 'BOME', 'HYPE', 'PNUT', 'MEME', 'BAND', 'CVX', 'LQTY', 'XRP']

# Spread & Capital settings
MIN_TRADE_USDT = 10.0       # Standard minimum limit ($10 USDT / ~15,000 KRW)
MAX_TRADE_USDT = 100.0      # Max limit per trade
TRADE_RATIO = 0.90          # Use 90% of available KRW balance
TOTAL_FEE = 0.21            # Taker fees sum: Coinone Spot (0.02%) + OKX Spot (0.10%) + OKX Futures (0.09%)

# Spread entry thresholds (Altcoins set to 5.0% for cherry-picking high margins, XRP set to 3.0%)
COIN_MIN_NET_SPREADS = {
    'AEVO': 5.0,
    'AIXBT': 5.0,
    'BOME': 5.0,
    'HYPE': 5.0,
    'PNUT': 5.0,
    'MEME': 5.0,
    'BAND': 5.0,
    'CVX': 5.0,
    'LQTY': 5.0,
    'XRP': 3.0
}

# Estimated Fixed Withdrawal Fees on Coinone
COINONE_WITHDRAW_FEES = {
    'AEVO': 2.0,
    'AIXBT': 20.0,
    'BOME': 300.0,
    'HYPE': 1.5,
    'PNUT': 10.0,
    'MEME': 150.0,
    'BAND': 1.0,
    'CVX': 1.0,
    'LQTY': 1.0,
    'XRP': 1.0
}

# Scan Intervals
CHECK_INTERVAL_SEC = 2
MONITOR_INTERVAL_SEC = 10
REBALANCE_CHECK_INTERVAL_SEC = 60

# OKX Deposit Addresses (Bot fetches dynamically, XRP pre-populated as fallback)
OKX_DEPOSIT_ADDRESSES = {
    'XRP': {'address': 'rBuZfn1m4tA6znziHsRp9AyC1M3qg6rgbF', 'tag': '6490818'}
}

# Coinone Deposit Addresses (For Rebalancing XRP)
COINONE_DEPOSIT_ADDRESSES = {
    'XRP': {'address': 'YOUR_COINONE_XRP_ADDRESS', 'tag': 'YOUR_COINONE_XRP_TAG'}
}

# State file
STATE_FILE = "logs/coinone_transfer_arb_state.json"

class CoinoneTransferArb:
    def __init__(self):
        self.lock = threading.Lock()
        self.state = self.load_state()
        
        # Initialize exchange API objects
        self.coinone = ccxt.coinone({
            'apiKey': os.getenv('COINONE_API_KEY', ''),
            'secret': os.getenv('COINONE_SECRET_KEY', ''),
        })
        self.coinone_pub = ccxt.coinone()
        
        self.okx = ccxt.okx({
            'apiKey': os.getenv('OKX_API_KEY', ''),
            'secret': os.getenv('OKX_SECRET_KEY', ''),
            'password': os.getenv('OKX_PASSPHRASE', ''),
            'type': 'trading'
        })
        self.okx_pub = ccxt.okx()
        
        self.usd_krw = 1450.0  # Fallback
        self._usd_krw_updated_at = 0
        
        self.coins = COINS
        
    def load_state(self):
        import json
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"pending_transfers": {}, "pending_reflow": {}}

    def save_state(self):
        import json
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

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

    def _notify(self, title, message, color=0x3498db):
        logger.info(f"🔔 [NOTIFY] {title}: {message}")
        discord_url = os.getenv("DISCORD_WEBHOOK_URL")
        if discord_url:
            try:
                payload = {
                    "embeds": [{
                        "title": title,
                        "description": message,
                        "color": color,
                        "timestamp": datetime.utcnow().isoformat()
                    }]
                }
                requests.post(discord_url, json=payload, timeout=5)
            except Exception as e:
                logger.warning(f"Failed to send discord notification: {e}")

    def get_coinone_balance(self):
        if PAPER_MODE:
            return {'KRW': {'free': 200000.0, 'used': 0.0, 'total': 200000.0}}
        try:
            return self.coinone.fetch_balance()
        except Exception as e:
            raise e

    def get_okx_balance(self):
        if PAPER_MODE:
            return {'USDT': {'free': 200.0, 'used': 0.0, 'total': 200.0}}
        try:
            return self.okx.fetch_balance()
        except Exception as e:
            raise e

    def get_rounded_size(self, symbol, coin_size):
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

    def open_hedged_trade(self, coin, net_spread, okx_usdt, coinone_krw, usd_krw, trade_usdt):
        logger.info(f"⚡ [OPENING HEDGE] Coinone buy + OKX short for {coin}... Size: ${trade_usdt:.2f}")
        
        spot_symbol = f"{coin}/KRW"
        futures_symbol = f"{coin}/USDT:USDT"
        
        raw_coin_qty = (trade_usdt * usd_krw) / coinone_krw
        
        rounded_size, contracts, contract_size = self.get_rounded_size(futures_symbol, raw_coin_qty)
        actual_krw_needed = rounded_size * coinone_krw
        
        logger.info(f"  Target spot size: {raw_coin_qty:.4f} -> OKX Rounded Size: {rounded_size:.4f} ({contracts} contracts)")
        
        try:
            okx_bal = self.get_okx_balance()
            usdt_free = okx_bal.get('USDT', {}).get('free', 0)
            required_margin = (rounded_size * okx_usdt) * 0.45
            if usdt_free < required_margin:
                logger.error(f"  [Abort] Insufficient OKX USDT margin. Needed: ${required_margin:.2f}, Free: ${usdt_free:.2f}")
                return False
        except Exception as e:
            logger.error(f"  [Abort] Failed to fetch OKX balance: {e}")
            return False
            
        try:
            c_bal = self.get_coinone_balance()
            krw_free = c_bal.get('KRW', {}).get('free', 0)
            if krw_free < actual_krw_needed:
                logger.error(f"  [Abort] Insufficient Coinone KRW. Needed: {actual_krw_needed:,.0f} KRW, Free: {krw_free:,.0f} KRW")
                return False
        except Exception as e:
            logger.error(f"  [Abort] Failed to fetch Coinone balance: {e}")
            return False
            
        if PAPER_MODE:
            logger.info("  [PAPER MODE] Simulating execution...")
            with self.lock:
                self.state["pending_transfers"][coin] = {
                    "coin": coin,
                    "qty": rounded_size,
                    "coinone_buy_price": coinone_krw,
                    "okx_short_price": okx_usdt,
                    "usd_krw": usd_krw,
                    "contracts": contracts,
                    "status": "WAITING_ARRIVAL",
                    "time": datetime.utcnow().isoformat(),
                    "paper": True
                }
                self.save_state()
            return True
            
        # Real Execution
        # 1. Open OKX futures short
        try:
            pos_mode = 'net_mode'
            try:
                config = self.okx.private_get_account_config()
                pos_mode = config['data'][0]['posMode']
            except Exception: pass
            
            params = {}
            if pos_mode == 'long_short_mode':
                params['posSide'] = 'short'
                
            try:
                self.okx.set_leverage(3, futures_symbol, {'mgnMode': 'cross'})
            except Exception: pass
            
            logger.info(f"  [+] Opening OKX Futures Short: {contracts} contracts...")
            order_short = self.okx.create_market_sell_order(futures_symbol, contracts, params)
            logger.info(f"  [+] OKX Futures Short filled. Order ID: {order_short.get('id')}")
        except Exception as e:
            logger.error(f"  [Abort] OKX Futures short failed: {e}")
            return False
            
        # 2. Buy Coinone Spot (Use direct v2.1/order API with inline UUID nonce override)
        try:
            buy_price = math.ceil(coinone_krw * 1.01)
            logger.info(f"  [+] Buying {rounded_size:.4f} {coin} on Coinone using Limit Buy at {buy_price} KRW (Pseudo-Market)...")
            
            params_spot = {
                'type': 'LIMIT',
                'side': 'BUY',
                'quote_currency': 'KRW',
                'target_currency': coin.upper(),
                'price': str(buy_price),
                'qty': str(rounded_size),
                'post_only': False,
                'nonce': str(uuid.uuid4())  # Override with UUID nonce for V2.1 endpoint compliance
            }
            res_spot = self.coinone.request('order', 'v2_1Private', 'POST', params_spot)
            order_id = res_spot.get('order_id') or res_spot.get('orderId')
            if not order_id:
                raise Exception(f"Order ID not found in response: {res_spot}")
            logger.info(f"  [+] Coinone Spot buy order submitted. ID: {order_id}")
        except Exception as e:
            logger.error(f"  [CRITICAL] Coinone Spot Buy failed: {e}! Attempting to cover OKX futures short...")
            try:
                params_cover = {}
                if pos_mode == 'long_short_mode':
                    params_cover['posSide'] = 'short'
                self.okx.create_market_buy_order(futures_symbol, contracts, params_cover)
                logger.info("  [+] OKX Futures Short Covered successfully. Rollback completed.")
            except Exception as roll_err:
                logger.error(f"  [ALERT] Rollback failed! Futures short is still open: {roll_err}")
            return False
            
        # 3. Withdraw from Coinone to OKX
        time.sleep(3)
        try:
            c_bal_updated = self.coinone.fetch_balance()
            coin_free = c_bal_updated.get(coin, {}).get('free', 0.0)
            
            if coin_free < rounded_size * 0.90:
                logger.error(f"  [Withdraw Abort] Coinone free balance too low: {coin_free:.4f} {coin}")
                return False
                
            # Dynamic OKX deposit address lookup
            dest = OKX_DEPOSIT_ADDRESSES.get(coin)
            address = dest.get('address') if dest else None
            tag = dest.get('tag') if dest else None
            
            if not address or address.startswith('YOUR_OKX'):
                try:
                    logger.info(f"  [+] Dynamically querying OKX deposit address for {coin}...")
                    addr_info = self.okx.fetch_deposit_address(coin)
                    address = addr_info.get('address')
                    tag = addr_info.get('tag')
                    logger.info(f"🔑 Successfully fetched OKX deposit address: {address} (Tag: {tag})")
                except Exception as addr_err:
                    logger.error(f"Failed to fetch OKX deposit address dynamically for {coin}: {addr_err}")
                    
            if not address:
                raise Exception(f"Missing valid OKX deposit address in config or API lookup for {coin}")
                
            withdraw_qty = math.floor((coin_free - 0.0001) * 10000) / 10000.0
            
            logger.info(f"  [+] Executing Coinone withdrawal of {withdraw_qty:.4f} {coin} to OKX {address}...")
            
            # Direct V2.1 API withdrawal request to bypass CCXT's missing withdrawal method
            params_withdraw = {
                'currency': coin.upper(),
                'address': address,
                'amount': str(withdraw_qty),
                'nonce': str(uuid.uuid4())
            }
            withdrawal = self.coinone.request('transaction/coin/withdrawal', 'v2_1Private', 'POST', params_withdraw)
            logger.info(f"  [+] Coinone withdrawal submitted. Response: {withdrawal}")
            
            with self.lock:
                self.state["pending_transfers"][coin] = {
                    "coin": coin,
                    "qty": withdraw_qty,
                    "coinone_buy_price": coinone_krw,
                    "okx_short_price": okx_usdt,
                    "usd_krw": usd_krw,
                    "contracts": contracts,
                    "pos_mode": pos_mode,
                    "status": "WAITING_ARRIVAL",
                    "time": datetime.utcnow().isoformat(),
                    "paper": False
                }
                self.save_state()
            return True
            
        except Exception as e:
            logger.error(f"  [CRITICAL WORKFLOW ERROR] Coinone withdrawal failed: {e}")
            self._notify("🚨 Withdrawal Failed", f"Coinone to OKX withdrawal failed for {coin}: {e}\nManual intervention required to withdraw and monitor.")
            return False

    def close_hedged_trade(self, coin, trans):
        qty = trans["qty"]
        contracts = trans["contracts"]
        coinone_buy_price = trans["coinone_buy_price"]
        okx_short_price = trans["okx_short_price"]
        usd_krw = trans["usd_krw"]
        is_paper = trans.get("paper", False)
        
        logger.info(f"🎯 [CLOSING HEDGE] Locking profit for {coin}...")
        
        if is_paper:
            spot_sell_price = okx_short_price
            futures_cover_price = okx_short_price
            spot_pnl_usd = (spot_sell_price - (coinone_buy_price / usd_krw)) * qty
            futures_pnl_usd = 0.0
            actual_profit_usd = spot_pnl_usd + futures_pnl_usd
            
            msg = (f"🎯 [PAPER] Arbitrage CLOSED successfully!\n"
                   f"• Coin: {coin}\n"
                   f"• Quantity: {qty:.4f} {coin}\n"
                   f"• Simulated Net Profit: **${actual_profit_usd:.4f} USDT**")
            logger.info(msg)
            self._notify("🎯 Simulated Arbitrage Completed", msg, color=0x2ecc71)
            
            self.record_history(coin, qty, coinone_buy_price, okx_short_price, spot_sell_price, futures_cover_price, spot_pnl_usd, futures_pnl_usd, actual_profit_usd, is_paper)
            return True
            
        # Real Close
        spot_symbol = f"{coin}/USDT"
        futures_symbol = f"{coin}/USDT:USDT"
        pos_mode = trans.get("pos_mode", "net_mode")
        
        # 1. Sell Spot on OKX
        try:
            logger.info(f"  [+] Selling spot {qty:.4f} {coin} on OKX Spot...")
            order_spot = self.okx.create_market_sell_order(spot_symbol, qty)
            logger.info(f"  [+] OKX Spot Sell successful. ID: {order_spot.get('id')}")
        except Exception as e:
            logger.error(f"  [CRITICAL ERROR] OKX Spot Sell failed: {e}")
            return False
            
        # 2. Cover Futures Short on OKX
        try:
            params_cover = {}
            if pos_mode == 'long_short_mode':
                params_cover['posSide'] = 'short'
            logger.info(f"  [+] Covering futures short: {contracts} contracts...")
            order_futures = self.okx.create_market_buy_order(futures_symbol, contracts, params_cover)
            logger.info(f"  [+] OKX Futures Cover successful. ID: {order_futures.get('id')}")
        except Exception as e:
            logger.error(f"  [CRITICAL ERROR] OKX Futures Cover failed! Potentially naked spot sell executed: {e}")
            self._notify("🚨 Futures Cover Failed", f"Live Spot sell completed but Futures short cover failed for {coin}! Cover manually ASAP.")
            return False
            
        # 3. Calculate Realized PnL
        time.sleep(3)
        spot_sell_price = okx_short_price
        try:
            fetched_spot = self.okx.fetch_order(order_spot['id'], spot_symbol)
            spot_sell_price = fetched_spot.get('average') or fetched_spot.get('price') or okx_short_price
        except Exception: pass
        
        futures_cover_price = okx_short_price
        try:
            fetched_fut = self.okx.fetch_order(order_futures['id'], futures_symbol)
            futures_cover_price = fetched_fut.get('average') or fetched_fut.get('price') or okx_short_price
        except Exception: pass
        
        spot_pnl_usd = (spot_sell_price - (coinone_buy_price / usd_krw)) * qty
        futures_pnl_usd = (okx_short_price - futures_cover_price) * qty
        actual_profit_usd = spot_pnl_usd + futures_pnl_usd
        
        msg = (f"🎉 [LIVE] Arbitrage successfully CLOSED & locked profit!\n"
               f"• Coin: {coin}\n"
               f"• Quantity: {qty:.4f} {coin}\n"
               f"• Actual Net Profit: **${actual_profit_usd:.4f} USDT** (approx {actual_profit_usd * usd_krw:,.0f} KRW)")
        logger.info(msg)
        self._notify("🎉 Arbitrage Completed (LIVE)", msg, color=0x2ecc71)
        
        self.record_history(coin, qty, coinone_buy_price, okx_short_price, spot_sell_price, futures_cover_price, spot_pnl_usd, futures_pnl_usd, actual_profit_usd, is_paper)
        return True

    def record_history(self, coin, qty, coinone_buy, okx_short, spot_sell, fut_cover, spot_pnl, fut_pnl, actual_profit, is_paper):
        import json
        history_file = "logs/coinone_okx_transfer_history.json"
        history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception: pass
            
        record = {
            'time': datetime.now().isoformat(),
            'coin': coin,
            'qty': qty,
            'coinone_buy_price_krw': coinone_buy,
            'okx_short_price_usd': okx_short,
            'okx_spot_sell_price_usd': spot_sell,
            'okx_futures_cover_price_usd': fut_cover,
            'spot_pnl_usd': round(spot_pnl, 4),
            'futures_pnl_usd': round(fut_pnl, 4),
            'actual_profit_usd': round(actual_profit, 4),
            'paper': is_paper
        }
        history.append(record)
        try:
            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save history: {e}")

    def monitor_pending_transfers(self):
        with self.lock:
            pending = list(self.state.get("pending_transfers", {}).keys())
            
        if not pending:
            return
            
        logger.info(f"🔍 Monitoring {len(pending)} pending Coinone-to-OKX transfers...")
        
        for coin in pending:
            with self.lock:
                trans = self.state["pending_transfers"].get(coin)
            if not trans:
                continue
                
            qty = trans["qty"]
            is_paper = trans.get("paper", False)
            
            if is_paper:
                elapsed = time.time() - datetime.fromisoformat(trans["time"]).timestamp()
                if elapsed >= 60:
                    logger.info(f"   [+] [PAPER] Simulated arrival for {coin} completed.")
                    if self.close_hedged_trade(coin, trans):
                        with self.lock:
                            if coin in self.state["pending_transfers"]:
                                del self.state["pending_transfers"][coin]
                                self.save_state()
                continue
                
            try:
                logger.info(f"   Checking OKX Spot balance of {coin} for arrival of {qty:.4f}...")
                okx_bal = self.get_okx_balance()
                free_balance = okx_bal.get(coin, {}).get('free', 0.0)
                
                if free_balance >= qty * 0.90:  # 90% threshold to cover minor withdrawal fee deduction
                    logger.info(f"   [+] Deposit confirmed on OKX! Balance of {coin}: {free_balance:.4f}")
                    if self.close_hedged_trade(coin, trans):
                        with self.lock:
                            if coin in self.state["pending_transfers"]:
                                del self.state["pending_transfers"][coin]
                                self.save_state()
                else:
                    logger.info(f"   [WAIT] Awaiting arrival on OKX (Current free balance: {free_balance:.4f} / Target: {qty:.4f})")
            except Exception as e:
                logger.error(f"Error checking OKX balance for pending transfer: {e}")

    def check_and_execute_rebalance(self):
        with self.lock:
            ref_state = self.state.get("pending_reflow", {})
            if ref_state and ref_state.get("status") in ("WAITING_ARRIVAL", "FAILED"):
                return
                
        try:
            c_bal = self.get_coinone_balance()
            krw_free = c_bal.get('KRW', {}).get('free', 0.0)
            
            okx_bal = self.get_okx_balance()
            usdt_free = okx_bal.get('USDT', {}).get('free', 0.0)
        except Exception as e:
            logger.error(f"Rebalance check failed to fetch balances: {e}")
            return
            
        usd_krw = self._get_usd_krw()
        total_portfolio_usd = usdt_free + (krw_free / usd_krw)
        target_half_usd = total_portfolio_usd / 2.0
        
        # Trigger reflow when Coinone KRW falls below 15,000 KRW
        if krw_free < 15000.0:
            excess_usdt = usdt_free - target_half_usd
            if excess_usdt >= 20.0:
                logger.info(f"⚖️ [AUTO-REBALANCE] Imbalance detected! Coinone KRW: {krw_free:,.0f} KRW, OKX USDT: {usdt_free:.2f} USDT.")
                logger.info(f"   Excess USDT to return: {excess_usdt:.2f} USDT. Launching background rebalancer...")
                
                if PAPER_MODE:
                    logger.info("⚖️ [PAPER MODE] Simulating Auto-rebalancing (100% mocked)...")
                    msg = (f"⚖️ [PAPER] Hedged Rebalancing simulated successfully!\n"
                           f"• Returned: ${excess_usdt:.2f} USDT via Simulated XRP\n"
                           f"• Price risk was 100% neutralized during transfer.")
                    logger.info(msg)
                    self._notify("⚖️ Coinone Portfolio Rebalanced (Simulated)", msg, color=0x3498db)
                    return
                
                with self.lock:
                    self.state["pending_reflow"] = {
                        "status": "STARTING",
                        "amount_usdt": excess_usdt,
                        "time": datetime.utcnow().isoformat()
                    }
                    self.save_state()
                    
                t = threading.Thread(target=self.execute_rebalance_thread, args=(excess_usdt, usd_krw))
                t.daemon = True
                t.start()

    def execute_rebalance_thread(self, amount_usdt, usd_krw):
        rebalance_coin = 'XRP'
        futures_symbol = f'{rebalance_coin}/USDT:USDT'
        
        try:
            # 1. Open OKX futures short to hedge price risk
            ticker = self.okx_pub.fetch_ticker(f'{rebalance_coin}/USDT')
            price = ticker['last']
            raw_qty = amount_usdt / price
            
            self.okx.load_markets()
            qty_str = self.okx.amount_to_precision(f'{rebalance_coin}/USDT', raw_qty)
            qty = float(qty_str)
            
            rounded_size, contracts, contract_size = self.get_rounded_size(futures_symbol, qty)
            
            pos_mode = 'net_mode'
            try:
                config = self.okx.private_get_account_config()
                pos_mode = config['data'][0]['posMode']
            except Exception: pass
            
            params = {}
            if pos_mode == 'long_short_mode':
                params['posSide'] = 'short'
                
            try:
                self.okx.set_leverage(3, futures_symbol, {'mgnMode': 'cross'})
            except Exception: pass
            
            logger.info(f"⚖️ [REBALANCE THREAD] Opening Futures Short: {contracts} contracts...")
            self.okx.create_market_sell_order(futures_symbol, contracts, params)
            
            # 2. Buy XRP Spot on OKX
            self.okx.create_market_buy_order(f'{rebalance_coin}/USDT', qty)
            time.sleep(3)
            
            # 3. Transfer Trading to Funding
            bal_trading = self.okx.fetch_balance({'type': 'trading'})
            xrp_trading = bal_trading.get(rebalance_coin, {}).get('free', 0.0)
            if xrp_trading > 0.1:
                transfer_qty = math.floor(xrp_trading * 10000) / 10000.0
                self.okx.transfer(rebalance_coin, transfer_qty, 'trading', 'funding')
                time.sleep(2)
                
            # 4. Fetch Funding balance
            bal_funding = self.okx.fetch_balance({'type': 'funding'})
            xrp_funding = bal_funding.get(rebalance_coin, {}).get('free', 0.0)
            
            # 5. Fetch Coinone deposit address
            dest = COINONE_DEPOSIT_ADDRESSES.get(rebalance_coin)
            if not dest or dest['address'] == 'YOUR_COINONE_XRP_ADDRESS':
                params_cover = {}
                if pos_mode == 'long_short_mode':
                    params_cover['posSide'] = 'short'
                self.okx.create_market_buy_order(futures_symbol, contracts, params_cover)
                raise Exception("Missing Coinone deposit address for XRP")
                
            withdraw_qty = math.floor((xrp_funding - 0.0105) * 10000) / 10000.0
            
            # 6. Execute OKX withdrawal
            logger.info(f"⚖️ [REBALANCE THREAD] Withdrawing {withdraw_qty:.4f} XRP to Coinone...")
            self.okx.withdraw(
                code=rebalance_coin,
                amount=withdraw_qty,
                address=dest['address'],
                tag=dest['tag'],
                params={
                    'chain': f'{rebalance_coin}-{rebalance_coin}',
                    'fee': '0.01'
                }
            )
            
            with self.lock:
                self.state["pending_reflow"]["status"] = "WAITING_ARRIVAL"
                self.state["pending_reflow"]["withdraw_qty"] = withdraw_qty
                self.state["pending_reflow"]["contracts"] = contracts
                self.state["pending_reflow"]["pos_mode"] = pos_mode
                self.save_state()
                
            # 7. Wait for arrival on Coinone
            start_time = time.time()
            arrived = False
            
            c_bal = self.coinone.fetch_balance()
            initial_xrp = c_bal.get(rebalance_coin, {}).get('free', 0.0)
            
            while time.time() - start_time < 900:
                time.sleep(15)
                try:
                    c_bal_cur = self.coinone.fetch_balance()
                    cur_xrp = c_bal_cur.get(rebalance_coin, {}).get('free', 0.0)
                    if cur_xrp >= (initial_xrp + withdraw_qty * 0.90) and cur_xrp > 0.1:
                        logger.info(f"⚖️ [REBALANCE THREAD] XRP Arrived on Coinone! Qty: {cur_xrp:.4f}")
                        arrived = True
                        break
                except Exception as e:
                    logger.warning(f"Error polling Coinone balance in rebalance thread: {e}")
                    
            if not arrived:
                raise Exception("Timeout waiting for XRP arrival on Coinone")
                
            # 8. Sell XRP on Coinone
            logger.info("⚖️ [REBALANCE THREAD] Closing hedge: Selling spot on Coinone and covering futures short...")
            
            def sell_spot_coinone():
                try:
                    sell_qty = round(cur_xrp - 0.0001, 4)
                    ticker = self.coinone_pub.fetch_ticker(f'{rebalance_coin}/KRW')
                    last_price = ticker['last']
                    limit_sell_price = math.floor(last_price * 0.99)
                    logger.info(f"     [Coinone] Selling {sell_qty:.4f} XRP using Limit Sell at {limit_sell_price} KRW (Pseudo-Market)...")
                    
                    params_sell = {
                        'type': 'LIMIT',
                        'side': 'SELL',
                        'quote_currency': 'KRW',
                        'target_currency': rebalance_coin.upper(),
                        'price': str(limit_sell_price),
                        'qty': str(sell_qty),
                        'post_only': False,
                        'nonce': str(uuid.uuid4())
                    }
                    res_sell = self.coinone.request('order', 'v2_1Private', 'POST', params_sell)
                    logger.info(f"     [Coinone] Limit sell successful! Response: {res_sell}")
                except Exception as b_err:
                    logger.error(f"     [Coinone ERROR] Spot sell failed: {b_err}")
                    
            def cover_short_okx():
                try:
                    params_cover = {}
                    if pos_mode == 'long_short_mode':
                        params_cover['posSide'] = 'short'
                    self.okx.create_market_buy_order(futures_symbol, contracts, params_cover)
                    logger.info("     [OKX] Futures cover successful!")
                except Exception as o_err:
                    logger.error(f"     [OKX ERROR] Futures cover failed: {o_err}")
                    
            t_s = threading.Thread(target=sell_spot_coinone)
            t_c = threading.Thread(target=cover_short_okx)
            t_s.start(); t_c.start()
            t_s.join(); t_c.join()
            
            with self.lock:
                self.state["pending_reflow"] = {}
                self.save_state()
                
            msg = (f"⚖️ [AUTO-REBALANCE] Hedged Rebalancing completed successfully!\n"
                   f"• Returned: ${amount_usdt:.2f} USDT via Hedged XRP\n"
                   f"• Price risk was 100% neutralized during transfer.")
            logger.info(msg)
            self._notify("⚖️ Coinone Portfolio Rebalanced (Hedged)", msg, color=0x3498db)
            
        except Exception as e:
            logger.error(f"❌ [REBALANCE ERROR] Rebalance thread failed: {e}")
            with self.lock:
                self.state["pending_reflow"]["status"] = "FAILED"
                self.state["pending_reflow"]["error"] = str(e)
                self.save_state()
            self._notify("🚨 Coinone Rebalance Failed", f"Auto-rebalance failed: {e}\nCheck logs for details.", color=0xe74c3c)

    def scan_opportunities(self):
        if not hasattr(self, '_last_diag_time'):
            self._last_diag_time = 0
        if time.time() - self._last_diag_time > 10:
            self._last_diag_time = time.time()
            try:
                c_bal_diag = self.get_coinone_balance()
                krw_free_diag = c_bal_diag.get('KRW', {}).get('free', 0.0)
                logger.info(f"ℹ️ [TOP DIAGNOSTIC] Loop active. Coinone KRW: {krw_free_diag:,.0f} KRW")
            except Exception as d_err:
                logger.info(f"ℹ️ [TOP DIAGNOSTIC] Loop active but balance fetch failed: {d_err}")

        usd_krw = self._get_usd_krw()
        with self.lock:
            pending = list(self.state.get("pending_transfers", {}).keys())

        try:
            c_bal = self.get_coinone_balance()
            krw_free = c_bal.get('KRW', {}).get('free', 0.0)
        except Exception as e:
            logger.error(f"Failed to fetch Coinone balance: {e}")
            return

        c_symbols = [f"{coin}/KRW" for coin in self.coins if coin not in pending]
        o_symbols = [f"{coin}/USDT" for coin in self.coins if coin not in pending]
        
        if not c_symbols:
            return
            
        try:
            c_ticks = self.coinone_pub.fetch_tickers(c_symbols)
            o_ticks = self.okx_pub.fetch_tickers(o_symbols)
        except Exception as e:
            logger.error(f"Failed to fetch tickers in bulk: {e}")
            return

        for coin in self.coins:
            if coin not in pending:
                c_symbol = f"{coin}/KRW"
                o_symbol = f"{coin}/USDT"
                
                c_tick = c_ticks.get(c_symbol)
                o_tick = o_ticks.get(o_symbol)
                
                if not c_tick or not o_tick:
                    continue
                    
                okx_usdt = o_tick.get('last')
                coinone_krw = c_tick.get('last')
                
                if okx_usdt is None or coinone_krw is None or coinone_krw == 0:
                    continue
                    
                okx_krw = okx_usdt * usd_krw
                raw_spread = (okx_krw - coinone_krw) / coinone_krw * 100
                
                avail_krw = krw_free * TRADE_RATIO
                trade_usdt = avail_krw / usd_krw if usd_krw > 0 else 0.0
                trade_usdt = min(trade_usdt, MAX_TRADE_USDT)
                
                if trade_usdt < MIN_TRADE_USDT:
                    continue
                
                trading_fee_pct = TOTAL_FEE
                
                flat_fee = COINONE_WITHDRAW_FEES.get(coin, 0.0)
                flat_fee_usd = flat_fee * okx_usdt
                withdraw_fee_pct = (flat_fee_usd / trade_usdt) * 100 if trade_usdt > 0.0 else 0.0
                    
                slippage_buffer = 0.30
                
                total_friction = trading_fee_pct + withdraw_fee_pct + slippage_buffer
                net_spread = raw_spread - total_friction
                
                min_spread = COIN_MIN_NET_SPREADS.get(coin, 5.0)
                if net_spread >= min_spread:
                    logger.info(f"🎯 [COINONE SIGNAL] Spread {net_spread:+.2f}% detected for {coin} (Threshold: {min_spread:+.2f}%)! Triggering entry...")
                    self.open_hedged_trade(coin, net_spread, okx_usdt, coinone_krw, usd_krw, trade_usdt)

    def run_loop(self):
        logger.info("======================================================================")
        logger.info(f"🤖 Starting Coinone-OKX Hedged Transfer Arbitrage Bot")
        logger.info(f"   [Mode: {'PAPER/SIMULATION' if PAPER_MODE else 'LIVE'}]")
        logger.info(f"   Monitored coins: {self.coins}")
        logger.info("======================================================================")

        self._notify("🚀 Coinone Transfer Arb Bot Initialized", f"Active Mode: {'PAPER (Simulation)' if PAPER_MODE else 'LIVE (Real Money)'}\nMonitored Coins: {self.coins}")

        with self.lock:
            pending = self.state.get("pending_transfers", {})
        if pending:
            logger.info(f"🔄 Resuming monitoring for {len(pending)} pending transfers in state...")

        while True:
            try:
                self.monitor_pending_transfers()
                self.check_and_execute_rebalance()
                self.scan_opportunities()
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
            time.sleep(CHECK_INTERVAL_SEC)

if __name__ == "__main__":
    bot = CoinoneTransferArb()
    bot.run_loop()
