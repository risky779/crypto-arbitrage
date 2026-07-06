import ccxt, os
from dotenv import load_dotenv
load_dotenv()
upbit = ccxt.upbit({'apiKey': os.getenv('UPBIT_ACCESS_KEY'), 'secret': os.getenv('UPBIT_SECRET_KEY')})
okx = ccxt.okx({'apiKey': os.getenv('OKX_API_KEY'), 'secret': os.getenv('OKX_SECRET_KEY'), 'password': os.getenv('OKX_PASSPHRASE')})
ub = upbit.fetch_balance()
ob = okx.fetch_balance()
print(f'업비트 KRW: {ub["KRW"]["free"]:,.0f}원')
print(f'OKX USDT: ${ob["USDT"]["free"]:.2f}')
for coin in ['ALGO', 'ID', 'BCH', 'XRP', 'XLM', 'MMT', 'BAT']:
    bal = ob.get(coin, {}).get('free', 0)
    if bal > 0.0001:
        print(f'OKX {coin}: {bal:.6f}')
