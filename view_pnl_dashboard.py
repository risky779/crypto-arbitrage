#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arbitrage & Polymarket Portfolio PnL Dashboard
Aggregates:
  - Bithumb-OKX Arbitrage Bot (빗썸 ARB)
  - Coinone-OKX Arbitrage Bot (코인원 ARB)
  - Polymarket Copybot (폴리마켓 카피봇)
Calculates daily PnL, cumulative yields, asset fluctuations, and progress targets.
"""
import os
import sys
import json
import requests
import psutil
import ccxt
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Fix encoding for Windows console
if hasattr(sys.stdout, 'reconfigure'):
    try: sys.stdout.reconfigure(encoding='utf-8')
    except Exception: pass

# Load environment variables
load_dotenv("D:/work/crypto-arbitrage/.env")

# Try importing Bithumb v2 API
try:
    sys.path.append("D:/work/crypto-arbitrage")
    from bithumb_api_v2 import BithumbAPIv2
except Exception:
    BithumbAPIv2 = None

def get_usd_krw():
    try:
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=5)
        rate = r.json().get("rates", {}).get("KRW")
        if rate:
            return float(rate)
    except Exception:
        pass
    return 1530.0  # Fallback

def load_history(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
    return []

def load_jsonl(filepath):
    trades = []
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        trades.append(json.loads(line))
        except Exception as e:
            print(f"Error loading JSONL {filepath}: {e}")
    return trades

def resolve_market_dynamic(condition_id):
    try:
        r = requests.get(f"https://clob.polymarket.com/markets/{condition_id}", timeout=5)
        if r.ok:
            return r.json()
    except Exception:
        pass
    return None

def is_bot_running(script_name):
    try:
        for proc in psutil.process_iter(['cmdline']):
            cmdline = proc.info.get('cmdline')
            if cmdline and any(script_name in part for part in cmdline):
                return True
    except Exception:
        pass
    return False

def get_bithumb_actual_krw():
    if BithumbAPIv2 is None:
        return None
    try:
        api = BithumbAPIv2()
        b_bal = api.get_balance()
        return float(b_bal.get('KRW', {}).get('free', 0.0))
    except Exception as e:
        print(f"Failed to fetch Bithumb balance dynamically: {e}")
        return None

def get_okx_actual_usd_value():
    try:
        okx = ccxt.okx({
            'apiKey': os.getenv('OKX_API_KEY'),
            'secret': os.getenv('OKX_SECRET_KEY'),
            'password': os.getenv('OKX_PASSPHRASE'),
            'enableRateLimit': True,
        })
        
        total_usd = 0.0
        
        # 1. Fetch balances from both Trading and Funding accounts
        o_bal_trading = okx.fetch_balance({'type': 'trading'})
        o_bal_funding = okx.fetch_balance({'type': 'funding'})
        
        # Collect non-zero coins
        coins = set()
        for b in [o_bal_trading, o_bal_funding]:
            for coin, info in b.items():
                if isinstance(info, dict) and info.get('total', 0) > 0.0001:
                    coins.add(coin)
        
        # Fetch tickers for non-stable coins to value them in USD
        prices = {'USDT': 1.0, 'USDC': 1.0}
        for coin in coins:
            if coin in ['USDT', 'USDC']:
                continue
            try:
                ticker = okx.fetch_ticker(f"{coin}/USDT")
                prices[coin] = float(ticker.get('last', 0.0))
            except Exception:
                prices[coin] = 0.0
                
        # Calculate total value in USD
        for b in [o_bal_trading, o_bal_funding]:
            for coin, info in b.items():
                if isinstance(info, dict) and info.get('total', 0) > 0.0001:
                    total_coin = float(info['total'])
                    price = prices.get(coin, 0.0)
                    total_usd += total_coin * price
                    
        return total_usd
    except Exception as e:
        print(f"Failed to fetch OKX balance dynamically: {e}")
        return None

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Multi-Bot Portfolio Dashboard")
    # Default fallback Bithumb seed in KRW
    parser.add_argument("--seed-bithumb", type=float, default=128745.0, help="빗썸 ARB Bithumb seed capital in KRW")
    parser.add_argument("--seed-coinone", type=float, default=200000.0, help="코인원 ARB Coinone seed capital in KRW")
    parser.add_argument("--seed-poly", type=float, default=5.48, help="폴리마켓 카피봇 Polymarket seed capital in USD")
    args = parser.parse_args()

    usd_krw = get_usd_krw()
    
    # Log Paths
    bithumb_path = "okx_bithumb_transfer_history.json"
    coinone_path = "logs/coinone_okx_transfer_history.json"
    poly_settled_path = "../polymarket-smart-money-bot/logs/crypto_copy_settled.jsonl"
    poly_trades_path = "../polymarket-smart-money-bot/logs/crypto_copy_trades.jsonl"

    bithumb_raw = load_history(bithumb_path)
    coinone_raw = load_history(coinone_path)
    poly_settled_raw = load_jsonl(poly_settled_path)
    poly_trades_raw = load_jsonl(poly_trades_path)

    # 1. Parse Bithumb Trades & Calculate Cumulative Profit in USD first
    trades = []
    tot_a_usd = 0.0
    for t in bithumb_raw:
        try:
            if t.get("paper", False):
                continue
            dt = datetime.fromisoformat(t["time"])
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            dt_kst = dt.astimezone(timezone(timedelta(hours=9)))
            p_usd = float(t["actual_profit_usd"])
            tot_a_usd += p_usd
            trades.append({
                "time": dt_kst,
                "date": dt_kst.strftime("%Y-%m-%d"),
                "plan": "빗썸 ARB",
                "coin": t["coin"],
                "profit_usd": p_usd,
                "paper": False
            })
        except Exception: pass

    # Dynamically resolve Bithumb Seed based on actual balances (including XRP in funding account)
    bithumb_actual_krw = get_bithumb_actual_krw()
    okx_actual_usd = get_okx_actual_usd_value()
    
    tot_a_krw_profit = tot_a_usd * usd_krw
    
    if bithumb_actual_krw is not None and okx_actual_usd is not None:
        actual_assets_krw = bithumb_actual_krw + (okx_actual_usd * usd_krw)
        # Seed = Actual Assets - Cumulative Profit
        seed_a_krw = actual_assets_krw - tot_a_krw_profit
        print(f"Dynamic Bithumb Seed resolved from actual balances: {seed_a_krw:,.0f} KRW (Bithumb KRW: {bithumb_actual_krw:,.0f}, OKX USD Value: ${okx_actual_usd:.2f})")
    else:
        seed_a_krw = args.seed_bithumb
        print(f"Using default/fallback Bithumb Seed: {seed_a_krw:,.0f} KRW")

    # Seeds Setup
    seed_b_krw = args.seed_coinone
    seed_c_usd = args.seed_poly
    seed_c_krw = seed_c_usd * usd_krw
    
    total_seed_krw = seed_a_krw + seed_b_krw + seed_c_krw
    total_seed_usd = total_seed_krw / usd_krw

    # 2. Parse Coinone Trades
    last_trade_time = {}
    for t in coinone_raw:
        try:
            if not t.get("paper", False):
                continue
            dt = datetime.fromisoformat(t["time"])
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            dt_kst = dt.astimezone(timezone(timedelta(hours=9)))
            
            # Start from today KST
            if dt_kst.date() < datetime(2026, 7, 6).date():
                continue
                
            coin = t["coin"]
            # Throttle: at least 30 minutes must pass between paper trades of the same coin
            if coin in last_trade_time:
                time_diff = dt_kst - last_trade_time[coin]
                if time_diff < timedelta(minutes=30):
                    continue
            
            last_trade_time[coin] = dt_kst
            trades.append({
                "time": dt_kst,
                "date": dt_kst.strftime("%Y-%m-%d"),
                "plan": "코인원 ARB",
                "coin": coin,
                "profit_usd": float(t["actual_profit_usd"]),
                "paper": True
            })
        except Exception: pass

    # 3. Parse Polymarket Trades
    settled_keys = {}
    for t in poly_settled_raw:
        try:
            settled_keys[t['trade_key']] = t
        except Exception: pass

    market_cache = {}
    for t in poly_trades_raw:
        try:
            if t.get("dry_run", True):
                continue
            
            # Generate trade key
            key = f"{t.get('timestamp')}_{t.get('condition_id')[:16]}_{t.get('outcome')}"
            
            dt_str = t.get("settled_at") or t.get("time") or datetime.fromtimestamp(t.get("timestamp"), tz=timezone.utc).isoformat()
            dt = datetime.fromisoformat(dt_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            dt_kst = dt.astimezone(timezone(timedelta(hours=9)))
            
            pnl_usd = 0.0
            is_settled = False
            
            if key in settled_keys:
                pnl_usd = settled_keys[key]["pnl_usd"]
                is_settled = True
            else:
                # Active/Unsettled in file, check if dynamically resolved via CLOB API
                if t.get('status') in ('matched', 'live') and t.get('filled'):
                    cid = t['condition_id']
                    if cid not in market_cache:
                        market_cache[cid] = resolve_market_dynamic(cid)
                    
                    m = market_cache[cid]
                    if m:
                        tokens = m.get("tokens", [])
                        final_price = None
                        for tk in tokens:
                            if tk.get("outcome", "").lower() == t["outcome"].lower():
                                final_price = float(tk.get("price", 0))
                                break
                        
                        if final_price in (0.0, 1.0):
                            entry_price = t.get("exec_price") or t.get("whale_price", 0.5)
                            if entry_price <= 0:
                                entry_price = 0.5
                            tokens_bought = t.get("size_usd", 1.0) / entry_price
                            pnl_usd = ((final_price - entry_price) * tokens_bought) - 0.01 # gas fee
                            is_settled = True
            
            if is_settled:
                trades.append({
                    "time": dt_kst,
                    "date": dt_kst.strftime("%Y-%m-%d"),
                    "plan": "폴리마켓 카피봇",
                    "coin": "POLY",
                    "profit_usd": pnl_usd,
                    "paper": False
                })
        except Exception: pass

    # Sort trades by timestamp
    trades.sort(key=lambda x: x["time"])

    if not trades:
        print("No trade history files found.")
        return

    total_trades_count = len(trades)
    
    # Initialize daily bucket
    daily_stats = {}
    dates = []
    
    for t in trades:
        d = t["date"]
        p_usd = t["profit_usd"]
        is_paper = t["paper"]
        plan = t["plan"]
        
        if d not in daily_stats:
            dates.append(d)
            daily_stats[d] = {
                "date": d,
                "a_usd": 0.0,
                "b_usd": 0.0,
                "c_usd": 0.0,
                "total_usd": 0.0,
                "trades": 0,
                "live": 0,
                "paper": 0
            }
            
        if plan == "빗썸 ARB":
            daily_stats[d]["a_usd"] += p_usd
        elif plan == "코인원 ARB":
            daily_stats[d]["b_usd"] += p_usd
        else:
            daily_stats[d]["c_usd"] += p_usd
            
        daily_stats[d]["total_usd"] += p_usd
        daily_stats[d]["trades"] += 1
        if is_paper:
            daily_stats[d]["paper"] += 1
        else:
            daily_stats[d]["live"] += 1

    dates.sort()
    operating_days = len(dates)

    # Accumulate yields and asset fluctuations
    cum_a_usd = 0.0
    cum_b_usd = 0.0
    cum_c_usd = 0.0
    
    daily_pnl_chart_data = []
    
    for d in dates:
        s = daily_stats[d]
        cum_a_usd += s["a_usd"]
        cum_b_usd += s["b_usd"]
        cum_c_usd += s["c_usd"]
        
        # Current asset values
        asset_a_krw = seed_a_krw + (cum_a_usd * usd_krw)
        asset_b_krw = seed_b_krw + (cum_b_usd * usd_krw)
        asset_c_usd = seed_c_usd + cum_c_usd
        asset_c_krw = asset_c_usd * usd_krw
        total_asset_krw = asset_a_krw + asset_b_krw + asset_c_krw
        
        daily_pnl_chart_data.append({
            "date": d,
            "a_usd": s["a_usd"],
            "b_usd": s["b_usd"],
            "c_usd": s["c_usd"],
            "total_usd": s["total_usd"],
            "cum_a_krw": cum_a_usd * usd_krw,
            "cum_b_krw": cum_b_usd * usd_krw,
            "cum_c_krw": cum_c_usd * usd_krw,
            "cum_total_krw": (cum_a_usd + cum_b_usd + cum_c_usd) * usd_krw,
            "asset_a_krw": asset_a_krw,
            "asset_b_krw": asset_b_krw,
            "asset_c_krw": asset_c_krw,
            "total_asset_krw": total_asset_krw,
            "yield_pct": (s["total_usd"] * usd_krw / total_seed_krw) * 100,
            "trades": s["trades"],
            "live": s["live"],
            "paper": s["paper"]
        })

    # Summary calculations
    tot_a_krw = cum_a_usd * usd_krw
    tot_b_krw = cum_b_usd * usd_krw
    tot_c_krw = cum_c_usd * usd_krw
    tot_c_usd = cum_c_usd
    tot_combined_krw = tot_a_krw + tot_b_krw + tot_c_krw
    tot_combined_usd = tot_combined_krw / usd_krw
    
    yield_a = (tot_a_krw / seed_a_krw) * 100 if seed_a_krw > 0 else 0.0
    yield_b = (tot_b_krw / seed_b_krw) * 100 if seed_b_krw > 0 else 0.0
    yield_c = (tot_c_usd / seed_c_usd) * 100 if seed_c_usd > 0 else 0.0
    yield_total = (tot_combined_krw / total_seed_krw) * 100 if total_seed_krw > 0 else 0.0
    
    avg_yield_a = yield_a / operating_days if operating_days > 0 else 0.0
    avg_yield_b = yield_b / operating_days if operating_days > 0 else 0.0
    avg_yield_c = yield_c / operating_days if operating_days > 0 else 0.0
    avg_yield_total = yield_total / operating_days if operating_days > 0 else 0.0

    # Get running status of bots
    bot_status = {
        "bithumb": is_bot_running("okx_bithumb_transfer_arb.py"),
        "coinone": is_bot_running("coinone_okx_transfer_arb.py"),
        "polymarket": is_bot_running("crypto_copy_bot.py")
    }

    # Print summary console view
    print("=" * 115)
    print(f"                       📈 PORTFOLIO ASSET & PERFORMANCE MONITORING DASHBOARD")
    print(f"   USD/KRW Rate: {usd_krw:,.2f} KRW | Target Daily Yield: 1.00% ({total_seed_krw * 0.01:,.0f} KRW)")
    print(f"   Total Portfolio Seed: {total_seed_krw:,.0f} KRW (A: {seed_a_krw/10000:.1f}만 | B: {seed_b_krw/10000:.1f}만 | C: {seed_c_usd:,.0f} USD)")
    print(f"   Bot Status: Bithumb={'RUNNING' if bot_status['bithumb'] else 'STOPPED'} | Coinone={'RUNNING' if bot_status['coinone'] else 'STOPPED'} | Polymarket={'RUNNING' if bot_status['polymarket'] else 'STOPPED'}")
    print("=" * 115)
    print(f"{'Date (KST)':<12} | {'빗썸 ARB':<17} | {'코인원 ARB':<17} | {'폴리마켓 카피봇 (Poly)':<17} | {'Total Profit':<16} | {'Daily Yield'}")
    print("-" * 115)

    for s in daily_pnl_chart_data:
        d = s["date"]
        a_krw = s["a_usd"] * usd_krw
        b_krw = s["b_usd"] * usd_krw
        c_krw = s["c_usd"] * usd_krw
        tot_krw = s["total_usd"] * usd_krw
        y_pct = s["yield_pct"]
        target_check = "✅ " if y_pct >= 1.0 else "   "
        print(f"{d:<12} | {a_krw:>7,.0f} KRW (${s['a_usd']:>4.1f}) | {b_krw:>7,.0f} KRW (${s['b_usd']:>4.1f}) | {c_krw:>7,.0f} KRW (${s['c_usd']:>4.1f}) | {tot_krw:>7,.0f} KRW (${s['total_usd']:>4.1f}) {target_check}| {y_pct:>9.2f}%")

    print("-" * 115)
    print(f"📌 PLAN-BY-PLAN METRICS SUMMARY:")
    print(f"  * 빗썸 ARB     : Total PnL: +{tot_a_krw:,.0f} KRW | Total Yield: {yield_a:.2f}% | Daily Avg: {avg_yield_a:.2f}%")
    print(f"  * 코인원 ARB     : Total PnL: +{tot_b_krw:,.0f} KRW | Total Yield: {yield_b:.2f}% | Daily Avg: {avg_yield_b:.2f}%")
    print(f"  * 폴리마켓 카피봇  : Total PnL: +{tot_c_krw:,.0f} KRW (${tot_c_usd:,.2f}) | Total Yield: {yield_c:.2f}% | Daily Avg: {avg_yield_c:.2f}%")
    print("-" * 115)
    print(f"📊 COMBINED PORTFOLIO SUMMARY:")
    print(f"• Total Cumulative Profit : {tot_combined_krw:,.0f} KRW (${tot_combined_usd:,.2f})")
    print(f"• Current Portfolio Asset : {total_seed_krw + tot_combined_krw:,.0f} KRW (A: {seed_a_krw+tot_a_krw:,.0f} | B: {seed_b_krw+tot_b_krw:,.0f} | C: {(seed_c_usd+tot_c_usd)*usd_krw:,.0f})")
    print(f"• Cumulative Return Yield : {yield_total:.2f}%")
    print(f"• Average Daily Yield     : {avg_yield_total:.2f}%  (Target: 1.00%)")
    print(f"• Projected Monthly Return: {avg_yield_total * 30:.2f}% (Approx {total_seed_krw * (avg_yield_total * 30/100):,.0f} KRW)")
    print("=" * 115)

    # Save reports
    os.makedirs("logs", exist_ok=True)
    artifact_dir = "C:/Users/ryu/.gemini/antigravity-cli/brain/9a2df478-6b21-4d1d-a826-5673a18045f8"
    os.makedirs(artifact_dir, exist_ok=True)
    os.makedirs(os.path.join(artifact_dir, "logs"), exist_ok=True)
    
    paths = ["logs/dashboard_report.md", os.path.join(artifact_dir, "dashboard_report.md")]
    for path in paths:
        with open(path, "w", encoding="utf-8") as md:
            md.write(f"# 📈 Multi-Bot Portfolio Performance Dashboard\n\n")
            md.write(f"*   **Updated At**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} KST\n")
            md.write(f"*   **USD/KRW Rate**: {usd_krw:,.2f} KRW\n")
            md.write(f"*   **Total Portfolio Seed**: {total_seed_krw:,.0f} KRW\n\n")
            
            md.write(f"## 📌 Combined Portfolio Performance Summary\n\n")
            md.write(f"| Metric | KRW Value | USD Value | Performance |\n")
            md.write(f"| :--- | :--- | :--- | :--- |\n")
            md.write(f"| **Total Cumulative Profit** | **{tot_combined_krw:,.0f} KRW** | **${tot_combined_usd:,.2f}** | Cumulative gain |\n")
            md.write(f"| **Total Operating Seed** | {total_seed_krw:,.0f} KRW | ${total_seed_usd:,.2f} | Initial capital allocation |\n")
            md.write(f"| **Current Portfolio Asset** | **{total_seed_krw + tot_combined_krw:,.0f} KRW** | **${(total_seed_krw + tot_combined_krw)/usd_krw:,.2f}** | Capital + Profit |\n")
            md.write(f"| **Average Daily Yield** | **{avg_yield_total:.2f}%** | - | Target: 1.00% daily |\n")
            md.write(f"| **Projected Monthly Return** | **{avg_yield_total * 30:.2f}%** | - | Approx {total_seed_krw * (avg_yield_total * 30/100):,.0f} KRW |\n\n")
            
            md.write(f"## ⚙️ Plan-by-Plan Performance Breakdown\n\n")
            md.write(f"| Plan Name | Operating Seed | Profit Amount | Total Return Yield | Average Daily Yield |\n")
            md.write(f"| :--- | :--- | :--- | :---: | :---: |\n")
            md.write(f"| **빗썸 ARB** | {seed_a_krw:,.0f} KRW | +{tot_a_krw:,.0f} KRW | {yield_a:.2f}% | {avg_yield_a:.2f}% |\n")
            md.write(f"| **코인원 ARB** | {seed_b_krw:,.0f} KRW | +{tot_b_krw:,.0f} KRW | {yield_b:.2f}% | {avg_yield_b:.2f}% |\n")
            md.write(f"| **폴리마켓 카피봇** | ${seed_c_usd:,.2f} ({seed_c_krw:,.0f} KRW) | +{tot_c_krw:,.0f} KRW (${tot_c_usd:,.2f}) | {yield_c:.2f}% | {avg_yield_c:.2f}% |\n\n")

            md.write(f"## 📊 Daily Profit & Yield Breakdown\n\n")
            md.write(f"| Date (KST) | 빗썸 ARB 수익 | 코인원 ARB 수익 | 폴리마켓 카피봇 수익 | Total Daily Profit | Daily Yield | Status |\n")
            md.write(f"| :--- | :--- | :--- | :--- | :--- | :---: | :---: |\n")
            
            for s in daily_pnl_chart_data:
                a_krw = s["a_usd"] * usd_krw
                b_krw = s["b_usd"] * usd_krw
                c_krw = s["c_usd"] * usd_krw
                tot_krw = s["total_usd"] * usd_krw
                y_pct = s["yield_pct"]
                status_emoji = "✅ Target Met (>=1%)" if y_pct >= 1.0 else "⏳ Below Target"
                md.write(f"| {s['date']} | {a_krw:,.0f} KRW | {b_krw:,.0f} KRW | {c_krw:,.0f} KRW | **{tot_krw:,.0f} KRW** | {y_pct:.2f}% | {status_emoji} |\n")

    # Export JavaScript PnL Data Object
    pnl_data_obj = {
        "usd_krw": usd_krw,
        "seed_krw": total_seed_krw,
        "seeds": {
            "a": seed_a_krw,
            "b": seed_b_krw,
            "c_krw": seed_c_krw,
            "c_usd": seed_c_usd
        },
        "balances": {
            "bithumb_krw": bithumb_actual_krw,
            "okx_usd": okx_actual_usd
        },
        "bot_status": bot_status,
        "summary": {
            "total_profit_krw": tot_combined_krw,
            "total_profit_usd": tot_combined_usd,
            "operating_days": operating_days,
            "total_trades": total_trades_count,
            "avg_daily_yield": avg_yield_total,
            "projected_monthly_yield": avg_yield_total * 30,
            
            "tot_a_krw": tot_a_krw,
            "yield_a": yield_a,
            "avg_yield_a": avg_yield_a,
            
            "tot_b_krw": tot_b_krw,
            "yield_b": yield_b,
            "avg_yield_b": avg_yield_b,
            
            "tot_c_krw": tot_c_krw,
            "tot_c_usd": tot_c_usd,
            "yield_c": yield_c,
            "avg_yield_c": avg_yield_c
        },
        "daily": daily_pnl_chart_data
    }

    js_content = f"const pnlData = {json.dumps(pnl_data_obj, indent=2)};"
    js_paths = ["logs/pnl_data.js", os.path.join(artifact_dir, "logs/pnl_data.js")]
    for js_path in js_paths:
        with open(js_path, "w", encoding="utf-8") as js_file:
            js_file.write(js_content)

if __name__ == "__main__":
    main()
