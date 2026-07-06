#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bithumb - OKX Automated Hybrid Arbitrage Bot
--------------------------------------------
Monitors spreads between Bithumb KRW market and OKX USDT market.
Executes simultaneous riskless arbitrage orders using:
- ccxt.okx for OKX orders (USDT futures/spot)
- BithumbAPIv2 for Bithumb orders (Bearer Token based API 2.0)
"""

import os
import sys
import io
import time
import json
import threading
import requests
from datetime import datetime, date
from pathlib import Path
from dotenv import load_dotenv
import ccxt

from bithumb_api_v2 import BithumbAPIv2

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

ENV_PATH = Path("D:/work/crypto-arbitrage/.env")
load_dotenv(ENV_PATH)

# ========== BOT SETTINGS ==========
PAPER_MODE = True           # Safe Default: Simulation mode (Dry-run) first
COINS = ['ALLO', 'MMT', 'ACE'] # High yield coins monitored by default

MIN_TRADE_USDT = 4.0        # Minimum order size (about 6,000 KRW)
MAX_TRADE_USDT = 50.0       # Max safety limit per position
TRADE_RATIO = 0.90          # Use 90% of available free balance
MIN_NET_SPREAD_KIMP = 1.0   # Min profit threshold for Kimchi Premium trade (Bithumb > OKX)
MIN_NET_SPREAD_RKIMP = 1.5  # Min profit threshold for Reverse Kimchi Premium (OKX > Bithumb)
CHECK_INTERVAL = 5          # Price check interval (seconds)

BITHUMB_FEE = 0.04          # Bithumb fee % (assuming coupon is applied)
OKX_FEE = 0.10              # OKX taker fee %
TOTAL_FEE = BITHUMB_FEE + OKX_FEE

LOG_FILE = 'okx_bithumb_arb_log.json'
SNAP_FILE = 'okx_bithumb_snapshot.json'

RESTOCK_THRESHOLD_USDT = 15.0 # Auto re-stock if inventory drops below this value
RESTOCK_AMOUNT_USDT = 20.0    # Restock amount in USDT

# Trend Filter
TREND_SHORT_MIN = 5
TREND_LONG_MIN = 30
TREND_THRESHOLD = -0.5      # Avoid entry if price drops > 0.5% in short term
# ==================================

class BithumbOKXArbitrage:
    def __init__(self):
        # Initialize clients
        self.okx = ccxt.okx({
            'apiKey': os.getenv('OKX_API_KEY'),
            'secret': os.getenv('OKX_SECRET_KEY'),
            'password': os.getenv('OKX_PASSPHRASE'),
            'enableRateLimit': True,
        })
        self.bithumb = BithumbAPIv2()
        
        # Public scanner client
        self.okx_pub = ccxt.okx({'enableRateLimit': True})
        self.bithumb_pub = ccxt.bithumb({'enableRateLimit': True})
        
        self.usd_krw = 1380.0
        self._usd_krw_updated_at = 0
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        
        self.cooldowns = {}
        self.restock_cooldowns = {}
        self.daily_reset_date = date.today()
        self.price_history = {coin: [] for coin in COINS}
        
        self.trades = self._load_trades()
        self.lock = threading.Lock()
        
        self.value_at_start = self._total_value_usdt()
        self.total_profit_usdt = 0.0
        self.session_trades = 0
        
        today_str = date.today().isoformat()
        self.daily_trades = sum(
            1 for t in self.trades
            if t.get('success') and t.get('time', '').startswith(today_str)
        )

    def _notify(self, title, msg, color=0x00b0f4):
        if not self.webhook_url:
            print(f"[{title}] {msg}")
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
            print(f"Notification error: {e}")

    def _load_trades(self):
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def _save_trades(self):
        try:
            with open(LOG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.trades, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f'Error saving trade log: {e}')

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

    def _total_value_usdt(self):
        """Calculates total valuation of Bithumb + OKX in USDT."""
        try:
            ob = self.okx.fetch_balance()
            bb = self.bithumb.get_balance()
            usd_krw = self._get_usd_krw()
            
            total = ob.get('USDT', {}).get('total', 0)
            total += bb.get('KRW', {}).get('free', 0) / usd_krw
            
            for coin in COINS:
                try:
                    price_usdt = self.okx_pub.fetch_ticker(f'{coin}/USDT')['last']
                    
                    # OKX Coin
                    total += ob.get(coin, {}).get('total', 0) * price_usdt
                    
                    # Bithumb Coin
                    b_coin = bb.get(coin, {})
                    b_qty = b_coin.get('free', 0) + b_coin.get('locked', 0)
                    total += b_qty * price_usdt
                except Exception:
                    pass
            return total
        except Exception as e:
            print(f"Valuation Snapshot Error: {e}")
            return 0.0

    def _save_snapshot(self):
        try:
            total = self._total_value_usdt()
            usd_krw = self._get_usd_krw()
            
            snap = {
                'time': datetime.now().isoformat(),
                'usd_krw': round(usd_krw, 1),
                'total_usdt': round(total, 2),
                'total_krw': round(total * usd_krw),
            }
            
            try:
                snaps = json.loads(Path(SNAP_FILE).read_text(encoding="utf-8"))
            except Exception:
                snaps = []
            snaps.append(snap)
            Path(SNAP_FILE).write_text(json.dumps(snaps, indent=2), encoding="utf-8")
            print(f'[Snapshot] Total valuation: ${total:.2f} ({total*usd_krw:,.0f} KRW)', flush=True)
        except Exception as e:
            print(f'[Snapshot Error] {e}', flush=True)

    # ── Trend Filter ──
    def _record_price(self, coin, price):
        now = time.time()
        self.price_history[coin].append((now, price))
        cutoff = now - TREND_LONG_MIN * 60
        self.price_history[coin] = [
            (t, p) for t, p in self.price_history[coin] if t >= cutoff
        ]

    def _get_ma(self, coin, window_min):
        now = time.time()
        cutoff = now - window_min * 60
        prices = [p for t, p in self.price_history.get(coin, []) if t >= cutoff]
        return sum(prices) / len(prices) if prices else None

    def _is_downtrend(self, coin, current_price):
        ma_short = self._get_ma(coin, TREND_SHORT_MIN)
        ma_long = self._get_ma(coin, TREND_LONG_MIN)
        if ma_short is None or ma_long is None:
            return False
        gap_pct = (ma_short - ma_long) / ma_long * 100
        return gap_pct <= TREND_THRESHOLD

    def get_spread(self, coin):
        usd_krw = self._get_usd_krw()
        o_tick = self.okx_pub.fetch_ticker(f'{coin}/USDT')
        b_tick = self.bithumb_pub.fetch_ticker(f'{coin}/KRW')
        
        okx_usdt = o_tick['last']
        bithumb_krw = b_tick['last']
        
        okx_krw = okx_usdt * usd_krw
        raw_spread = (bithumb_krw - okx_krw) / okx_krw * 100
        net_spread = raw_spread - TOTAL_FEE
        
        return net_spread, okx_usdt, bithumb_krw, usd_krw

    def get_trade_amount(self, coin, direction, okx_usdt, bithumb_krw, usd_krw):
        try:
            ob = self.okx.fetch_balance()
            bb = self.bithumb.get_balance()
            
            usdt_free = ob.get('USDT', {}).get('free', 0)
            coin_okx = ob.get(coin, {}).get('free', 0)
            
            krw_free = bb.get('KRW', {}).get('free', 0)
            coin_bithumb = bb.get(coin, {}).get('free', 0)
            
            if direction == 'BUY_OKX_SELL_BITHUMB':
                okx_limit = usdt_free * TRADE_RATIO
                b_limit = coin_bithumb * okx_usdt * TRADE_RATIO
                trade_usdt = min(okx_limit, b_limit, MAX_TRADE_USDT)
                if usdt_free < MIN_TRADE_USDT:
                    return 0, f"OKX USDT insufficient ({usdt_free:.2f})"
                if coin_bithumb * okx_usdt < MIN_TRADE_USDT:
                    return 0, f"Bithumb {coin} inventory insufficient ({coin_bithumb:.4f} Qty)"
            else: # BUY_BITHUMB_SELL_OKX
                b_limit = krw_free / usd_krw * TRADE_RATIO
                okx_limit = coin_okx * okx_usdt * TRADE_RATIO
                trade_usdt = min(b_limit, okx_limit, MAX_TRADE_USDT)
                if krw_free / usd_krw < MIN_TRADE_USDT:
                    return 0, f"Bithumb KRW cash insufficient ({krw_free:,.0f} KRW)"
                if coin_okx * okx_usdt < MIN_TRADE_USDT:
                    return 0, f"OKX {coin} inventory insufficient ({coin_okx:.4f} Qty)"
                    
            if trade_usdt < MIN_TRADE_USDT:
                return 0, f"Calculated trade size too small (${trade_usdt:.2f})"
            return trade_usdt, "OK"
        except Exception as e:
            return 0, f"Balance check failed: {e}"

    # ── Order Placement ──
    def _buy_okx(self, coin, okx_usdt, trade_usdt, out):
        try:
            qty = trade_usdt / okx_usdt
            if PAPER_MODE:
                out['okx'] = {'status': 'paper', 'price': okx_usdt, 'amount': qty, 'cost_usdt': trade_usdt}
                return
            order = self.okx.create_market_buy_order(f'{coin}/USDT', qty)
            out['okx'] = {
                'status': 'ok',
                'order_id': order['id'],
                'price': order.get('average') or okx_usdt,
                'amount': order.get('filled') or qty,
                'cost_usdt': order.get('cost') or trade_usdt,
            }
        except Exception as e:
            out['okx'] = {'status': 'error', 'error': str(e)}

    def _sell_okx(self, coin, coin_amount, okx_usdt, out):
        try:
            if PAPER_MODE:
                out['okx'] = {'status': 'paper', 'price': okx_usdt, 'amount': coin_amount, 'proceeds_usdt': okx_usdt * coin_amount}
                return
            order = self.okx.create_market_sell_order(f'{coin}/USDT', coin_amount)
            out['okx'] = {
                'status': 'ok',
                'order_id': order['id'],
                'price': order.get('average') or okx_usdt,
                'amount': order.get('filled') or coin_amount,
                'proceeds_usdt': order.get('cost') or okx_usdt * coin_amount,
            }
        except Exception as e:
            out['okx'] = {'status': 'error', 'error': str(e)}

    def _buy_bithumb(self, coin, krw_amount, bithumb_krw, out):
        try:
            market = f'KRW-{coin}'
            if PAPER_MODE:
                out['bithumb'] = {'status': 'paper', 'price': bithumb_krw, 'amount': krw_amount / bithumb_krw, 'cost_krw': krw_amount}
                return
            res = self.bithumb.market_buy(market, krw_amount)
            out['bithumb'] = {
                'status': 'ok',
                'order_id': res.get('order_id', 'N/A'),
                'price': bithumb_krw,
                'amount': krw_amount / bithumb_krw,
                'cost_krw': krw_amount
            }
        except Exception as e:
            out['bithumb'] = {'status': 'error', 'error': str(e)}

    def _sell_bithumb(self, coin, coin_amount, bithumb_krw, out):
        try:
            market = f'KRW-{coin}'
            if PAPER_MODE:
                out['bithumb'] = {'status': 'paper', 'price': bithumb_krw, 'amount': coin_amount, 'proceeds_krw': coin_amount * bithumb_krw}
                return
            res = self.bithumb.market_sell(market, coin_amount)
            out['bithumb'] = {
                'status': 'ok',
                'order_id': res.get('order_id', 'N/A'),
                'price': bithumb_krw,
                'amount': coin_amount,
                'proceeds_krw': coin_amount * bithumb_krw
            }
        except Exception as e:
            out['bithumb'] = {'status': 'error', 'error': str(e)}

    def execute_trade(self, coin, direction, net_spread, okx_usdt, bithumb_krw, usd_krw, trade_usdt):
        coin_amount = trade_usdt / okx_usdt
        krw_amount = trade_usdt * usd_krw
        out = {}
        
        value_before = self._total_value_usdt()
        
        if direction == 'BUY_OKX_SELL_BITHUMB':
            t1 = threading.Thread(target=self._buy_okx, args=(coin, okx_usdt, trade_usdt, out))
            t2 = threading.Thread(target=self._sell_bithumb, args=(coin, coin_amount, bithumb_krw, out))
        else: # BUY_BITHUMB_SELL_OKX
            t1 = threading.Thread(target=self._buy_bithumb, args=(coin, krw_amount, bithumb_krw, out))
            t2 = threading.Thread(target=self._sell_okx, args=(coin, coin_amount, okx_usdt, out))
            
        t1.start(); t2.start()
        t1.join(); t2.join()
        
        okx_ok = out.get('okx', {}).get('status') in ('ok', 'paper')
        bithumb_ok = out.get('bithumb', {}).get('status') in ('ok', 'paper')
        success = okx_ok and bithumb_ok
        
        if not success:
            print(f"[Warning] Arb execution failed! OKX: {okx_ok} | Bithumb: {bithumb_ok}", flush=True)
            self._notify("🚨 Arbitrage Failed (One side failure)", f"Coin: {coin}\nDirection: {direction}\nOKX Status: {out.get('okx')}\nBithumb Status: {out.get('bithumb')}", color=0xff0000)
            return
            
        value_after = self._total_value_usdt()
        trade_profit = value_after - value_before
        
        record = {
            'time': datetime.now().isoformat(),
            'coin': coin,
            'direction': direction,
            'net_spread_pct': round(net_spread, 4),
            'okx_price_usdt': okx_usdt,
            'bithumb_price_krw': bithumb_krw,
            'usd_krw': usd_krw,
            'trade_usdt': round(trade_usdt, 4),
            'estimated_profit_usdt': round(trade_profit, 4) if not PAPER_MODE else round(trade_usdt * abs(net_spread)/100, 4),
            'paper': PAPER_MODE,
            'success': success,
            'okx_result': out.get('okx'),
            'bithumb_result': out.get('bithumb')
        }
        
        with self.lock:
            self.trades.append(record)
            if success:
                self.daily_trades += 1
                self.total_profit_usdt += record['estimated_profit_usdt']
            self._save_trades()
            
        mode_str = "[PAPER]" if PAPER_MODE else "[LIVE]"
        msg = (f"{mode_str} Arbitrage successfully filled!\n"
               f"• Coin: {coin} ({direction})\n"
               f"• Net Spread: {net_spread:+.2f}%\n"
               f"• Size: ${trade_usdt:.2f} ({coin_amount:.4f} {coin})\n"
               f"• Profit Est: ${record['estimated_profit_usdt']:.4f}")
        print(f"{msg}", flush=True)
        self._notify("🎉 Arbitrage Execution Filled!", msg, color=0x00ff00)

    def run(self):
        print("="*80)
        print(f"🤖 Starting Bithumb-OKX Arbitrage Bot (Paper Mode: {PAPER_MODE})")
        print(f"   Coins Monitored: {COINS}")
        print("="*80)
        
        self._save_snapshot()
        
        while True:
            try:
                # 1. Check daily resets
                today = date.today()
                if today != self.daily_reset_date:
                    self.daily_trades = 0
                    self.daily_reset_date = today
                    
                # 2. Iterate coins
                for coin in COINS:
                    net_spread, okx_usdt, bithumb_krw, usd_krw = self.get_spread(coin)
                    self._record_price(coin, okx_usdt)
                    
                    # 3. Detect trend to prevent buying into a crashing market
                    if self._is_downtrend(coin, okx_usdt):
                        print(f"[{coin}] Downtrend detected. Skipping opportunities.", flush=True)
                        continue
                        
                    direction = None
                    if net_spread >= MIN_NET_SPREAD_KIMP:
                        direction = 'BUY_OKX_SELL_BITHUMB'
                    elif net_spread <= -MIN_NET_SPREAD_RKIMP:
                        direction = 'BUY_BITHUMB_SELL_OKX'
                        
                    if direction:
                        trade_usdt, status = self.get_trade_amount(coin, direction, okx_usdt, bithumb_krw, usd_krw)
                        if trade_usdt > 0:
                            print(f"[SIGNAL] {coin} spread {net_spread:+.2f}% triggers {direction}. Trading ${trade_usdt:.2f}.", flush=True)
                            self.execute_trade(coin, direction, net_spread, okx_usdt, bithumb_krw, usd_krw, trade_usdt)
                        else:
                            print(f"[{coin}] Signal {net_spread:+.2f}% ({direction}) skipped: {status}", flush=True)
                    else:
                        print(f"[{coin}] Monitoring spread: {net_spread:+.2f}% | OKX: ${okx_usdt:.4f} | Bithumb: {bithumb_krw:,.0f} KRW (No Trigger)", flush=True)
            except Exception as e:
                print(f"Error in main loop cycle: {e}", flush=True)
            time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    bot = BithumbOKXArbitrage()
    bot.run()
