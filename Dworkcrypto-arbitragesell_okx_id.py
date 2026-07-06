#!/usr/bin/env python3
import ccxt, os, sys, io, time
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

okx = ccxt.okx({'apiKey': os.getenv('OKX_API_KEY'), 'secret': os.getenv('OKX_SECRET_KEY'), 'password': os.getenv('OKX_PASSPHRASE')})

print("=== OKX ID 매도 판단 ===\n", flush=True)

# 현재 잔고
bal = okx.fetch_balance()
id_qty = bal.get('ID', {}).get('free', 0)
usdt_before = bal['USDT']['free']

print(f"현재 보유: {id_qty:.2f}개", flush=True)
print(f"현재 USDT: ${usdt_before:.2f}\n", flush=True)

# 현재 가격
ticker = okx.fetch_ticker('ID/USDT')
current_price = ticker['last']

# 매수가 계산 (231.84개를 $10에 샀음)
bought_qty = 231.84
bought_cost = 10.0
avg_buy_price = bought_cost / bought_qty

print(f"매수가: ${avg_buy_price:.6f}", flush=True)
print(f"현재가: ${current_price:.6f}", flush=True)

change_pct = ((current_price - avg_buy_price) / avg_buy_price) * 100
print(f"변동: {change_pct:+.2f}%\n", flush=True)

if current_price > avg_buy_price:
    print(f"✅ 가격 상승 → 매도 진행", flush=True)

    # 전량 매도
    sell_qty = id_qty * 0.99
    expected_usdt = sell_qty * current_price * 0.999  # 수수료 0.1% 제외

    print(f"매도 수량: {sell_qty:.2f}개", flush=True)
    print(f"예상 수익: ${expected_usdt:.2f} (약 ${expected_usdt - bought_cost:.2f} 수익)\n", flush=True)

    try:
        result = okx.create_market_sell_order('ID/USDT', sell_qty)
        print(f"✅ 매도 성공", flush=True)
        print(f"  주문 ID: {result.get('id', 'N/A')}", flush=True)

        time.sleep(1)

        # 최종 잔고
        bal_after = okx.fetch_balance()
        usdt_after = bal_after['USDT']['free']
        id_after = bal_after.get('ID', {}).get('free', 0)

        actual_profit = usdt_after - usdt_before

        print(f"\n최종 잔고:", flush=True)
        print(f"  USDT: ${usdt_after:.2f} (+${actual_profit:.2f})", flush=True)
        print(f"  ID: {id_after:.2f}개", flush=True)

    except Exception as e:
        print(f"❌ 매도 실패: {e}", flush=True)

else:
    print(f"❌ 가격 하락 중 → 매도 보류", flush=True)
    print(f"  손실: ${(current_price - avg_buy_price) * id_qty:.2f}", flush=True)
    print(f"  가격이 ${avg_buy_price:.6f} 이상 오를 때까지 대기", flush=True)
