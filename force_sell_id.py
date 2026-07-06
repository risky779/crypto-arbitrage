#!/usr/bin/env python3
import ccxt, os
from dotenv import load_dotenv
load_dotenv()

okx = ccxt.okx({'apiKey': os.getenv('OKX_API_KEY'), 'secret': os.getenv('OKX_SECRET_KEY'), 'password': os.getenv('OKX_PASSPHRASE')})

bal = okx.fetch_balance()
id_qty = bal['ID']['free']
print(f'ID: {id_qty:.2f}개')

if id_qty > 0.1:
    sell = okx.create_market_sell_order('ID/USDT', id_qty)
    print(f'매도 완료')

bal = okx.fetch_balance()
print(f"USDT: ${bal['USDT']['free']:.2f}")
