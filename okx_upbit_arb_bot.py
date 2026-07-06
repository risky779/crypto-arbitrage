#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OKX-업비트 동시 차익거래 봇
원리: 양쪽에 미리 자금 예치 후, 스프레드 포착 시 동시 주문 실행 (전송 불필요)
"""

import ccxt, os, sys, io, time, json, threading, requests
from datetime import datetime, date
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

# ========== 설정 ==========
PAPER_MODE = False          # True: 모의거래 / False: 실거래 (주의!)

COINS = ['BCH', 'DOGE']      # 모니터링 코인 (보유 재고 기준)

MIN_TRADE_USDT = 4.0        # 최소 거래 금액 (업비트 5,000원 기준)
MAX_TRADE_USDT = 50.0       # 최대 거래 금액 (안전 상한선)
TRADE_RATIO    = 0.9        # 가용 잔고 중 사용 비율 (90%)
MIN_NET_SPREAD_KIMP  = 0.8  # 김프 최소 순수익률 (업비트 > OKX) - KRW 확보 우선
MIN_NET_SPREAD_Rkimp = 1.5  # 역프 최소 순수익률 (OKX > 업비트)
COOLDOWN_SEC = 0            # 쿨다운 없음 (잔고/스프레드 조건이 실질 제한)
MAX_DAILY_TRADES = 9999     # 사실상 무제한 (잔고/스프레드 조건이 실질 한도)
CHECK_INTERVAL = 3          # 가격 조회 주기 (초)

OKX_FEE   = 0.10            # OKX 거래 수수료 %
UPBIT_FEE = 0.05            # 업비트 거래 수수료 %
TOTAL_FEE = OKX_FEE + UPBIT_FEE  # 합산 수수료 (전송 없으므로 입출금 수수료 없음)

LOG_FILE = 'okx_upbit_arb_log.json'

# OKX 재고 자동 보충 설정
RESTOCK_THRESHOLD_USDT = 15.0  # OKX 코인 재고가 이 금액 이하면 자동 보충
RESTOCK_AMOUNT_USDT    = 20.0  # 1회 보충 금액 (USDT)

# 하락장 필터 설정 (MA 기반)
TREND_SHORT_MIN  = 5      # 단기 MA 윈도우 (분)
TREND_LONG_MIN   = 30     # 장기 MA 윈도우 (분)
TREND_THRESHOLD  = -0.5   # 단기MA/장기MA 괴리 기준 (%) - 이 이상 하락 시 차단
# ==========================


class ArbitrageBot:
    def __init__(self):
        self.okx = ccxt.okx({
            'apiKey':    os.getenv('OKX_API_KEY'),
            'secret':    os.getenv('OKX_SECRET_KEY'),
            'password':  os.getenv('OKX_PASSPHRASE'),
            'enableRateLimit': True,
        })
        self.upbit = ccxt.upbit({
            'apiKey': os.getenv('UPBIT_ACCESS_KEY'),
            'secret': os.getenv('UPBIT_SECRET_KEY'),
            'enableRateLimit': True,
            'options': {'createMarketBuyOrderRequiresPrice': False},
        })

        self.usd_krw = 1380
        self._usd_krw_updated_at = 0
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

        self.cooldowns = {}          # coin -> datetime
        self.restock_cooldowns = {}  # coin -> datetime (재보충 쿨다운 10분)
        self.daily_reset_date = date.today()
        self.total_restock_loss = 0.0
        # 코인별 가격 히스토리: {coin: [(timestamp, price), ...]}
        self.price_history = {coin: [] for coin in COINS}
        self.trades = self._load_trades()
        self.lock = threading.Lock()
        self._low_inventory_alerted = set()  # 중복 알림 방지

        # 시작 시점 총 계좌 가치 스냅샷 (세션 기준점)
        self.value_at_start    = self._total_value_usdt()
        self.total_profit_usdt = 0.0  # 거래 수익 누적 (가격변동 제외)
        self.session_trades    = 0

        today_str = date.today().isoformat()
        self.daily_trades = sum(
            1 for t in self.trades
            if t.get('success') and t.get('time', '').startswith(today_str)
        )
        self.total_restock_loss = sum(
            t.get('restock_loss_usdt', 0) for t in self.trades
        )

        # OKX 코인별 평균 매입단가 추적 (김프 거래 기준)
        # {coin: {'avg': 평균단가(USDT), 'qty': 누적수량}}
        self.okx_avg_cost = {}
        for t in self.trades:
            if t.get('success') and t.get('direction') == 'BUY_OKX_SELL_UPBIT':
                self._update_okx_avg_cost(
                    t['coin'],
                    t['okx_price_usdt'],
                    t.get('okx_result', {}).get('amount') or 0
                )
        # 재고 없는 코인 OKX 단가 리셋
        try:
            for coin in list(self.okx_avg_cost.keys()):
                free = ob_bal.get(coin, {}).get('free', 0) if 'ob_bal' in dir() else 0
                if free < 0.0001:
                    del self.okx_avg_cost[coin]
        except Exception:
            pass

        # 업비트 코인별 평균 매입단가 추적 (역프 거래 기준)
        # 단, 현재 업비트 재고가 없는 코인은 단가 리셋
        self.upbit_avg_cost = {}
        for t in self.trades:
            if t.get('success') and t.get('direction') == 'BUY_UPBIT_SELL_OKX':
                self._update_upbit_avg_cost(
                    t['coin'],
                    t['upbit_price_krw'],
                    t.get('upbit_result', {}).get('amount') or 0
                )
        # 재고 없는 코인 평균단가 리셋
        try:
            ub_bal = self.upbit.fetch_balance()
            for coin in list(self.upbit_avg_cost.keys()):
                free = ub_bal.get(coin, {}).get('free', 0)
                if free < 0.0001:
                    del self.upbit_avg_cost[coin]
                    print(f'[단가 리셋] 업비트 {coin} 재고 없음 → 평균단가 초기화', flush=True)
        except Exception:
            pass

    # ── 디스코드 알림 ─────────────────────────────────────────────────────

    def _notify(self, title, msg, color=0x00b0f4):
        if not self.webhook_url:
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
        except Exception:
            pass

    # ── 하락장 감지 ───────────────────────────────────────────────────────

    def _record_price(self, coin, price):
        """가격 기록 및 장기 MA 윈도우 초과 데이터 제거"""
        now = time.time()
        self.price_history[coin].append((now, price))
        cutoff = now - TREND_LONG_MIN * 60
        self.price_history[coin] = [
            (t, p) for t, p in self.price_history[coin] if t >= cutoff
        ]

    def _get_ma(self, coin, window_min):
        """최근 window_min 분 평균가 반환. 데이터 부족 시 None"""
        now    = time.time()
        cutoff = now - window_min * 60
        prices = [p for t, p in self.price_history.get(coin, []) if t >= cutoff]
        return sum(prices) / len(prices) if prices else None

    def _is_downtrend(self, coin, current_price):
        """
        단기 MA < 장기 MA × (1 + TREND_THRESHOLD/100) → 하락 추세
        데이터 부족 시 → 안전하게 False 반환
        """
        ma_short = self._get_ma(coin, TREND_SHORT_MIN)
        ma_long  = self._get_ma(coin, TREND_LONG_MIN)
        if ma_short is None or ma_long is None:
            return False
        gap_pct = (ma_short - ma_long) / ma_long * 100
        return gap_pct <= TREND_THRESHOLD

    # ── 유틸 ──────────────────────────────────────────────────────────────

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
            print(f'[경고] 로그 저장 실패: {e}')

    def _save_snapshot(self):
        """현재 총자산을 snapshot.json에 기록 (일별 손익 추이 추적용)"""
        SNAP_FILE = 'okx_upbit_snapshot.json'
        try:
            ob = self.okx.fetch_balance()
            ub = self.upbit.fetch_balance()
            usd_krw = self._get_usd_krw()

            okx_usdt = ob.get('USDT', {}).get('free', 0)
            ub_krw   = ub.get('KRW', {}).get('free', 0)
            coins = {}
            total = okx_usdt + ub_krw / usd_krw
            for c in COINS:
                try:
                    p_usdt = self.okx.fetch_ticker(f'{c}/USDT')['last']
                    p_krw  = self.upbit.fetch_ticker(f'{c}/KRW')['last']
                    oq = ob.get(c, {}).get('free', 0)
                    uq = ub.get(c, {}).get('free', 0)
                    total += oq * p_usdt + uq * p_krw / usd_krw
                    coins[c] = {'okx': round(oq, 4), 'upbit': round(uq, 4)}
                except Exception:
                    pass

            snap = {
                'time':       datetime.now().isoformat(),
                'usd_krw':    round(usd_krw, 1),
                'total_usdt': round(total, 2),
                'total_krw':  round(total * usd_krw),
                'okx_usdt':   round(okx_usdt, 2),
                'upbit_krw':  round(ub_krw),
                'coins':      coins,
            }

            try:
                with open(SNAP_FILE, 'r', encoding='utf-8') as f:
                    snaps = json.load(f)
            except Exception:
                snaps = []
            snaps.append(snap)
            with open(SNAP_FILE, 'w', encoding='utf-8') as f:
                json.dump(snaps, f, ensure_ascii=False, indent=2)
            print(f'[스냅샷] 총자산 ${total:.2f} ({total*usd_krw:,.0f}원) 기록', flush=True)
        except Exception as e:
            print(f'[스냅샷 실패] {e}', flush=True)

    def _get_usd_krw(self):
        if time.time() - self._usd_krw_updated_at > 60:
            try:
                self.usd_krw = self.upbit.fetch_ticker('USDT/KRW')['last']
                self._usd_krw_updated_at = time.time()
            except Exception:
                pass
        return self.usd_krw

    def _in_cooldown(self, coin):
        if coin not in self.cooldowns:
            return False
        return (datetime.now() - self.cooldowns[coin]).total_seconds() < COOLDOWN_SEC

    def _reset_daily_if_needed(self):
        today = date.today()
        if today != self.daily_reset_date:
            self.daily_trades = 0
            self.daily_reset_date = today

    # ── 스프레드 계산 ─────────────────────────────────────────────────────

    def get_spread(self, coin):
        """
        반환: (net_spread, okx_usdt, upbit_krw, usd_krw)
        net_spread 양수 → 업비트가 비쌈 (OKX매수/업비트매도)
        net_spread 음수 → OKX가 비쌈  (업비트매수/OKX매도)
        """
        usd_krw  = self._get_usd_krw()
        okx_usdt  = self.okx.fetch_ticker(f'{coin}/USDT')['last']
        upbit_krw = self.upbit.fetch_ticker(f'{coin}/KRW')['last']

        okx_krw    = okx_usdt * usd_krw
        raw_spread = (upbit_krw - okx_krw) / okx_krw * 100
        net_spread = raw_spread - TOTAL_FEE

        return net_spread, okx_usdt, upbit_krw, usd_krw

    # ── 잔고 기반 최대 거래 금액 계산 ────────────────────────────────────────

    def get_trade_amount(self, coin, direction, okx_usdt, upbit_krw, usd_krw):
        """
        가용 잔고 기준 최대 거래 금액(USDT) 계산.
        반환: (trade_usdt, msg)  trade_usdt=0 이면 거래 불가.
        """
        try:
            ob = self.okx.fetch_balance()
            ub = self.upbit.fetch_balance()

            usdt_free     = ob.get('USDT', {}).get('free', 0)
            coin_on_okx   = ob.get(coin,   {}).get('free', 0)
            krw_free      = ub.get('KRW',  {}).get('free', 0)
            coin_on_upbit = ub.get(coin,   {}).get('free', 0)

            if direction == 'BUY_OKX_SELL_UPBIT':
                # OKX USDT vs 업비트 코인 재고 중 작은 쪽
                okx_limit   = usdt_free          * TRADE_RATIO
                upbit_limit = coin_on_upbit * okx_usdt * TRADE_RATIO
                trade_usdt  = min(okx_limit, upbit_limit, MAX_TRADE_USDT)
                if usdt_free < MIN_TRADE_USDT:
                    return 0, f"OKX USDT 부족 ({usdt_free:.2f})"
                if coin_on_upbit * okx_usdt < MIN_TRADE_USDT:
                    return 0, f"업비트 {coin} 재고 부족 ({coin_on_upbit:.4f}개)"
            else:  # BUY_UPBIT_SELL_OKX
                # 업비트 KRW vs OKX 코인 재고 중 작은 쪽
                krw_limit  = krw_free / usd_krw  * TRADE_RATIO
                okx_limit  = coin_on_okx * okx_usdt * TRADE_RATIO
                trade_usdt = min(krw_limit, okx_limit, MAX_TRADE_USDT)
                if krw_free / usd_krw < MIN_TRADE_USDT:
                    return 0, f"업비트 KRW 부족 ({krw_free:,.0f}원)"
                if coin_on_okx * okx_usdt < MIN_TRADE_USDT:
                    return 0, f"OKX {coin} 재고 부족 ({coin_on_okx:.4f}개)"

            if trade_usdt < MIN_TRADE_USDT:
                return 0, f"거래 가능 금액 부족 (${trade_usdt:.2f})"

            return trade_usdt, "OK"
        except Exception as e:
            return 0, f"잔고 조회 실패: {e}"

    # ── 개별 주문 (스레드에서 실행) ────────────────────────────────────────

    def _buy_okx(self, coin, okx_usdt, trade_usdt, out):
        """OKX 시장가 매수: USDT → coin"""
        try:
            amount = trade_usdt / okx_usdt
            if PAPER_MODE:
                out['okx'] = {'status': 'paper', 'price': okx_usdt, 'amount': amount, 'cost_usdt': trade_usdt}
                return
            order = self.okx.create_market_buy_order(f'{coin}/USDT', amount)
            out['okx'] = {
                'status': 'ok',
                'order_id': order['id'],
                'price':    order.get('average') or okx_usdt,
                'amount':   order.get('filled') or amount,
                'cost_usdt': order.get('cost') or trade_usdt,
            }
        except Exception as e:
            out['okx'] = {'status': 'error', 'error': str(e)}

    def _sell_upbit(self, coin, coin_amount, upbit_krw, out):
        """업비트 시장가 매도: coin → KRW"""
        try:
            estimated_krw = coin_amount * upbit_krw
            if estimated_krw < 5000:
                out['upbit'] = {'status': 'error', 'error': f'최소 주문 금액 미달 ({estimated_krw:.0f}원 < 5,000원)'}
                return
            if PAPER_MODE:
                out['upbit'] = {'status': 'paper', 'price': upbit_krw, 'amount': coin_amount, 'proceeds_krw': estimated_krw}
                return
            order = self.upbit.create_market_sell_order(f'{coin}/KRW', coin_amount)
            out['upbit'] = {
                'status': 'ok',
                'order_id': order['id'],
                'price':    order.get('average') or upbit_krw,
                'amount':   order.get('filled') or coin_amount,
                'proceeds_krw': order.get('cost') or upbit_krw * coin_amount,
            }
        except Exception as e:
            out['upbit'] = {'status': 'error', 'error': str(e)}

    def _buy_upbit(self, coin, krw_amount, upbit_krw, out):
        """업비트 시장가 매수: KRW → coin (krw_amount 기준)"""
        try:
            coin_amount = krw_amount / upbit_krw
            if PAPER_MODE:
                out['upbit'] = {'status': 'paper', 'price': upbit_krw, 'amount': coin_amount, 'cost_krw': krw_amount}
                return
            order = self.upbit.create_market_buy_order(f'{coin}/KRW', krw_amount)
            out['upbit'] = {
                'status': 'ok',
                'order_id': order['id'],
                'price':    order.get('average') or upbit_krw,
                'amount':   order.get('filled') or coin_amount,
                'cost_krw': krw_amount,
            }
        except Exception as e:
            out['upbit'] = {'status': 'error', 'error': str(e)}

    def _sell_okx(self, coin, coin_amount, okx_usdt, out):
        """OKX 시장가 매도: coin → USDT"""
        try:
            if PAPER_MODE:
                out['okx'] = {'status': 'paper', 'price': okx_usdt, 'amount': coin_amount, 'proceeds_usdt': okx_usdt * coin_amount}
                return
            order = self.okx.create_market_sell_order(f'{coin}/USDT', coin_amount)
            out['okx'] = {
                'status': 'ok',
                'order_id': order['id'],
                'price':    order.get('average') or okx_usdt,
                'amount':   order.get('filled') or coin_amount,
                'proceeds_usdt': order.get('cost') or okx_usdt * coin_amount,
            }
        except Exception as e:
            out['okx'] = {'status': 'error', 'error': str(e)}

    # ── OKX 재고 자동 보충 ────────────────────────────────────────────────

    def _restock_upbit_coin(self, coin, upbit_krw, okx_usdt, usd_krw, net_spread_pct):
        """
        김프 거래 후 업비트 코인 재고 부족 시 자동 매수
        - 10분 쿨다운: 무한루프 방지
        - 조건: 김프 ≥ MIN_NET_SPREAD_KIMP일 때만 허용
        """
        try:
            # 재보충 쿨다운 (10분) - 무한루프 방지
            last = self.restock_cooldowns.get(f'upbit_{coin}')
            if last and (datetime.now() - last).seconds < 600:
                return

            ub        = self.upbit.fetch_balance()
            coin_free = ub.get(coin, {}).get('free', 0)
            krw_free  = ub.get('KRW', {}).get('free', 0)

            coin_value_usdt = coin_free * okx_usdt
            if coin_value_usdt * TRADE_RATIO >= MIN_TRADE_USDT:
                return  # 재고 충분 (90% 적용 후 최소 거래금액 이상)

            # 업비트에서 매수 시 프리미엄 = 현재 김프 스프레드 (업비트가 그만큼 비쌈)
            # 김프가 최소 기준 이상이면 재보충 허용
            # (김프 환경에서 업비트 매수 프리미엄은 감수해야 할 비용)
            if abs(net_spread_pct) < MIN_NET_SPREAD_KIMP:
                msg = (f'**{coin}** 업비트 재고 부족\n'
                       f'김프 {net_spread_pct:.2f}% < 기준 {MIN_NET_SPREAD_KIMP}%\n'
                       f'→ 재보충 보류')
                print(f'[재고 보류] {msg}', flush=True)
                self._notify('⚠️ 업비트 재고 부족 - 보충 보류', msg, color=0xffa500)
                return

            buy_krw = min(RESTOCK_AMOUNT_USDT * usd_krw, krw_free * 0.9)
            if buy_krw < 5000:
                self._notify('⚠️ 업비트 재고 부족 - KRW 부족',
                             f'KRW {krw_free:,.0f}원 부족', color=0xff0000)
                return

            # 쿨다운 기록 (매수 전 기록해서 중복 실행 방지)
            self.restock_cooldowns[f'upbit_{coin}'] = datetime.now()

            if not PAPER_MODE:
                self.upbit.create_market_buy_order(f'{coin}/KRW', buy_krw)
                buy_price = upbit_krw
                buy_qty   = buy_krw / buy_price
                self._update_upbit_avg_cost(coin, buy_price, buy_qty)

            msg = (f'**{coin}** {buy_krw:,.0f}원 매수 (재고 보충)\n'
                   f'김프 {net_spread_pct:+.2f}% 활성 중 | 매수단가 {upbit_krw:,.0f}원{"(모의)" if PAPER_MODE else ""}')
            print(f'[업비트 재고 보충] {msg}', flush=True)
            self._notify('🔄 업비트 재고 자동 보충', msg, color=0x00b0f4)

        except Exception as e:
            print(f'[업비트 재고 보충 실패] {coin}: {e}', flush=True)

    def _sell_okx_inventory(self, coin, okx_usdt, net_spread_pct=0.0):
        """
        김프 거래 후 OKX 코인 재고 정리 (USDT 회수)
        - 10분 쿨다운: 무한루프 방지
        """
        try:
            last = self.restock_cooldowns.get(f'okx_{coin}')
            if last and (datetime.now() - last).seconds < 300:
                return

            ob        = self.okx.fetch_balance()
            coin_free = ob.get(coin, {}).get('free', 0)
            usdt_free = ob.get('USDT', {}).get('free', 0)

            # USDT 충분하면 굳이 팔 필요 없음
            if usdt_free >= RESTOCK_THRESHOLD_USDT:
                return

            if coin_free < 0.001:
                return

            avg_info = self.okx_avg_cost.get(coin)
            avg_cost = avg_info['avg'] if avg_info else None

            if avg_cost and okx_usdt < avg_cost:
                # 단가 이하 → 김프 수익이 손실 커버하는지 확인
                loss_pct   = (avg_cost - okx_usdt) / avg_cost * 100
                spread_pct = abs(net_spread_pct)
                if spread_pct <= loss_pct:
                    msg = (f'**{coin}** OKX 재고 정리 보류\n'
                           f'매도손실 {loss_pct:.2f}% > 김프수익 {spread_pct:.2f}%\n'
                           f'평균단가 ${avg_cost:.2f} > 현재가 ${okx_usdt:.2f}')
                    print(f'[OKX 매도 보류] {msg}', flush=True)
                    self._notify('⚠️ OKX 재고 정리 보류 - 단가 손실', msg, color=0xffa500)
                    return
                reason = f'김프수익 {spread_pct:.2f}% > 단가손실 {loss_pct:.2f}% → 매도 진행'
            else:
                reason = f'현재가 ${okx_usdt:.2f} ≥ 평균단가 ${avg_cost:.2f}' if avg_cost else '단가 미확인'

            self.restock_cooldowns[f'okx_{coin}'] = datetime.now()

            if not PAPER_MODE:
                self.okx.create_market_sell_order(f'{coin}/USDT', coin_free)
                if coin in self.okx_avg_cost:
                    del self.okx_avg_cost[coin]

            proceeds = coin_free * okx_usdt
            msg = (f'**{coin}** {coin_free:.4f}개 매도 → ${proceeds:.2f} 회수\n{reason}')
            print(f'[OKX 재고 정리] {msg}', flush=True)
            self._notify('🔄 OKX 재고 정리 (USDT 회수)', msg, color=0x00b0f4)

        except Exception as e:
            print(f'[OKX 재고 정리 실패] {coin}: {e}', flush=True)

    def _restock_okx(self, coin, okx_usdt):
        """역프 거래 후 OKX 코인 재고 부족 시 자동 매수
        USDT가 MIN_USDT_RESERVE 이상 남을 때만 실행
        """
        MIN_USDT_RESERVE = 10.0  # 이 이하면 재보충 안 함 (김프 거래 자금 보호)
        try:
            ob = self.okx.fetch_balance()
            coin_free       = ob.get(coin, {}).get('free', 0)
            coin_value_usdt = coin_free * okx_usdt
            usdt_free       = ob.get('USDT', {}).get('free', 0)

            if coin_value_usdt >= RESTOCK_THRESHOLD_USDT:
                return  # 재고 충분

            # USDT 최소 보유량 확인 - 김프 거래 자금 보호
            if usdt_free <= MIN_USDT_RESERVE:
                print(f'[재보충 건너뜀] OKX USDT ${usdt_free:.2f} ≤ 최소보유 ${MIN_USDT_RESERVE} → 건너뜀', flush=True)
                return

            # 목표치(RESTOCK_THRESHOLD_USDT)까지만 보충, MIN_USDT_RESERVE 초과분만 사용
            need_usdt = RESTOCK_THRESHOLD_USDT - coin_value_usdt
            available = usdt_free - MIN_USDT_RESERVE  # 최소보유 제외 사용 가능
            buy_usdt  = min(need_usdt, available * 0.9)

            if buy_usdt < 2:
                self._notify(
                    '⚠️ OKX 재고 부족 - USDT 부족',
                    f'**{coin}** 재고 ${coin_value_usdt:.2f} | OKX USDT ${usdt_free:.2f}',
                    color=0xff0000
                )
                return

            if not PAPER_MODE:
                self.okx.create_market_buy_order(f'{coin}/USDT', buy_usdt / okx_usdt)

            msg = (f'**{coin}** 재고 ${coin_value_usdt:.2f} → '
                   f'${buy_usdt:.2f} 보충 (목표 ${RESTOCK_THRESHOLD_USDT}){"(모의)" if PAPER_MODE else ""}')
            print(f'[재보충] {msg}', flush=True)
            self._notify('🔄 OKX 재고 자동 보충', msg, color=0x00b0f4)

        except Exception as e:
            print(f'[재보충 실패] {coin}: {e}', flush=True)

    # ── 총 계좌 가치 스냅샷 ───────────────────────────────────────────────────

    def _total_value_usdt(self):
        """OKX + 업비트 전체 자산을 USDT로 환산"""
        try:
            ob = self.okx.fetch_balance()
            ub = self.upbit.fetch_balance()
            usd_krw = self._get_usd_krw()

            total = ob.get('USDT', {}).get('free', 0)
            for coin in COINS:
                try:
                    price_usdt = self.okx.fetch_ticker(f'{coin}/USDT')['last']
                    price_krw  = self.upbit.fetch_ticker(f'{coin}/KRW')['last']
                    total += ob.get(coin, {}).get('free', 0) * price_usdt
                    total += ub.get(coin, {}).get('free', 0) * price_krw / usd_krw
                except Exception:
                    pass
            total += ub.get('KRW', {}).get('free', 0) / usd_krw
            return total
        except Exception:
            return 0.0

    # ── OKX 평균 매입단가 추적 (김프 거래 기준) ──────────────────────────────

    def _update_okx_avg_cost(self, coin, price_usdt, qty):
        """김프 거래 시 OKX 코인 매수 단가 가중평균 업데이트"""
        if not qty or not price_usdt:
            return
        if coin not in self.okx_avg_cost:
            self.okx_avg_cost[coin] = {'avg': price_usdt, 'qty': qty, 'total': price_usdt * qty}
        else:
            old = self.okx_avg_cost[coin]
            nq  = old['qty'] + qty
            self.okx_avg_cost[coin] = {
                'avg':   (old['total'] + price_usdt * qty) / nq,
                'qty':   nq,
                'total': old['total'] + price_usdt * qty
            }

    # ── 업비트 평균 매입단가 추적 ─────────────────────────────────────────────

    def _update_upbit_avg_cost(self, coin, price_krw, qty):
        """역프 거래 시 업비트 DOGE 매수 단가 가중평균 업데이트"""
        if not qty or not price_krw:
            return
        if coin not in self.upbit_avg_cost:
            self.upbit_avg_cost[coin] = {'avg': price_krw, 'qty': qty}
        else:
            old = self.upbit_avg_cost[coin]
            new_qty = old['qty'] + qty
            new_avg = (old['avg'] * old['qty'] + price_krw * qty) / new_qty
            self.upbit_avg_cost[coin] = {'avg': new_avg, 'qty': new_qty}

    # ── 업비트 KRW 보충 (매입단가 이상일 때만 매도) ───────────────────────────

    def _restock_upbit_krw(self, coin, upbit_krw, usd_krw, net_spread_pct=0.0):
        """KRW 부족 시 업비트 코인 매도
        조건 1: 현재가 > 평균단가  → 무조건 매도
        조건 2: 현재가 ≤ 평균단가 → 거래 수익 > 단가 손실 시에만 매도
        """
        try:
            ub        = self.upbit.fetch_balance()
            krw_free  = ub.get('KRW',  {}).get('free', 0)
            coin_free = ub.get(coin,   {}).get('free', 0)
            krw_needed = RESTOCK_AMOUNT_USDT * usd_krw

            if krw_free >= krw_needed:
                return

            avg_info = self.upbit_avg_cost.get(coin)
            avg_cost = avg_info['avg'] if avg_info else None

            if avg_cost and upbit_krw < avg_cost:
                # 단가 이하 → 거래 수익이 매도 손실을 커버하는지 확인
                cost_loss_pct = (avg_cost - upbit_krw) / avg_cost * 100
                abs_spread    = abs(net_spread_pct)
                if abs_spread <= cost_loss_pct:
                    msg = (f'**{coin}** 현재가 {upbit_krw:,.0f}원 < 평균단가 {avg_cost:,.0f}원\n'
                           f'단가손실 {cost_loss_pct:.2f}% > 거래수익 {abs_spread:.2f}% → 보충 보류')
                    print(f'[KRW 보충 보류] {msg}', flush=True)
                    self._notify('⚠️ 업비트 KRW 부족 - 보충 보류', msg, color=0xffa500)
                    return
                reason = f'거래수익 {abs_spread:.2f}% > 단가손실 {cost_loss_pct:.2f}% → 보충 진행'
            else:
                reason = f'현재가 {upbit_krw:,.0f}원 ≥ 평균단가 {avg_cost:,.0f}원' if avg_cost else '평균단가 미확인'

            sell_krw   = krw_needed - krw_free
            sell_coins = sell_krw / upbit_krw

            if coin_free < sell_coins or sell_krw < 5000:
                self._notify('⚠️ 업비트 KRW 부족 - 재고 부족',
                             f'KRW {krw_free:,.0f}원 | {coin} {coin_free:.2f}개', color=0xff0000)
                return

            if not PAPER_MODE:
                self.upbit.create_market_sell_order(f'{coin}/KRW', sell_coins)

            # 단가 이하 매도 손실 계산 및 누적수익 차감
            loss_usdt = 0.0
            if avg_cost and upbit_krw < avg_cost:
                loss_krw  = (avg_cost - upbit_krw) * sell_coins
                loss_usdt = loss_krw / usd_krw
                with self.lock:
                    self.total_profit_usdt -= loss_usdt
                    self.total_restock_loss += loss_usdt
                # 로그에 기록
                record = {
                    'time': datetime.now().isoformat(),
                    'type': 'KRW_RESTOCK',
                    'coin': coin,
                    'sell_qty': sell_coins,
                    'sell_price': upbit_krw,
                    'avg_cost': avg_cost,
                    'restock_loss_usdt': round(loss_usdt, 4),
                    'paper': PAPER_MODE,
                }
                with self.lock:
                    self.trades.append(record)
                    self._save_trades()

            msg = (f'**{coin}** {sell_coins:.2f}개 매도 → 약 {sell_krw:,.0f}원 확보\n'
                   f'{reason}'
                   + (f'\n단가 손실: -${loss_usdt:.4f} → 누적수익 반영' if loss_usdt else ''))
            print(f'[KRW 보충] {msg}', flush=True)
            self._notify('🔄 업비트 KRW 자동 보충', msg, color=0x00b0f4)

        except Exception as e:
            print(f'[KRW 보충 실패] {coin}: {e}', flush=True)

    # ── 롤백 (한쪽 실패 시 성공한 쪽 역방향 복구) ───────────────────────────

    def _rollback(self, coin, direction, out, okx_ok, upbit_ok, coin_amount, krw_amount, okx_usdt, upbit_krw):
        result = {'attempted': True}
        try:
            if direction == 'BUY_OKX_SELL_UPBIT':
                if okx_ok and not upbit_ok:
                    # OKX 매수 성공 + 업비트 매도 실패 → OKX 다시 매도
                    qty = out['okx'].get('amount') or coin_amount
                    self.okx.create_market_sell_order(f'{coin}/USDT', qty)
                    result['action'] = f'OKX 매도 복구 {qty:.6f} {coin}'
                elif not okx_ok and upbit_ok:
                    # OKX 매수 실패 + 업비트 매도 성공 → 업비트 다시 매수
                    krw = out['upbit'].get('proceeds_krw') or (coin_amount * upbit_krw)
                    self.upbit.create_market_buy_order(f'{coin}/KRW', krw)
                    result['action'] = f'업비트 매수 복구 {krw:,.0f}원'
            else:  # BUY_UPBIT_SELL_OKX
                if upbit_ok and not okx_ok:
                    # 업비트 매수 성공 + OKX 매도 실패 → 업비트 다시 매도
                    qty = out['upbit'].get('amount') or coin_amount
                    self.upbit.create_market_sell_order(f'{coin}/KRW', qty)
                    result['action'] = f'업비트 매도 복구 {qty:.6f} {coin}'
                elif not upbit_ok and okx_ok:
                    # 업비트 매수 실패 + OKX 매도 성공 → OKX 다시 매수
                    usdt = out['okx'].get('proceeds_usdt') or TRADE_AMOUNT_USDT
                    self.okx.create_market_buy_order(f'{coin}/USDT', usdt / okx_usdt)
                    result['action'] = f'OKX 매수 복구 ${usdt:.2f}'
            result['status'] = 'ok'
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
            print(f'[긴급] 복구 주문 실패 - 수동 확인 필요: {e}', flush=True)
        return result

    # ── 동시 주문 실행 ────────────────────────────────────────────────────

    def execute_trade(self, coin, direction, net_spread, okx_usdt, upbit_krw, usd_krw, trade_usdt):
        coin_amount = trade_usdt / okx_usdt
        krw_amount  = trade_usdt * usd_krw
        out = {}

        # 거래 전 총 계좌 가치 스냅샷
        value_before = self._total_value_usdt()

        if direction == 'BUY_OKX_SELL_UPBIT':
            t1 = threading.Thread(target=self._buy_okx,    args=(coin, okx_usdt, trade_usdt, out))
            t2 = threading.Thread(target=self._sell_upbit, args=(coin, coin_amount, upbit_krw, out))
        else:
            t1 = threading.Thread(target=self._buy_upbit, args=(coin, krw_amount, upbit_krw, out))
            t2 = threading.Thread(target=self._sell_okx,  args=(coin, coin_amount, okx_usdt, out))

        t1.start(); t2.start()
        t1.join();  t2.join()

        okx_ok   = out.get('okx',   {}).get('status') in ('ok', 'paper')
        upbit_ok = out.get('upbit', {}).get('status') in ('ok', 'paper')
        success  = okx_ok and upbit_ok

        # 한쪽 실패 시 역방향 복구 (실거래 모드에서만)
        rollback = None
        if not success and not PAPER_MODE and (okx_ok or upbit_ok):
            print(f'[경고] 한쪽 주문 실패 - 복구 시도 중...', flush=True)
            rollback = self._rollback(coin, direction, out, okx_ok, upbit_ok,
                                      coin_amount, krw_amount, okx_usdt, upbit_krw)
            print(f'[복구] {rollback.get("action", "없음")} → {rollback.get("status")}', flush=True)
            rb_status = rollback.get('status')
            rb_color  = 0xffa500 if rb_status == 'ok' else 0xff0000
            self._notify(
                '⚠️ 한쪽 주문 실패 - 롤백',
                f'**코인**: {coin}\n'
                f'**OKX**: {"성공" if okx_ok else "실패"}  |  **업비트**: {"성공" if upbit_ok else "실패"}\n'
                f'**롤백**: {rollback.get("action","없음")} → {rb_status}\n'
                f'**롤백 오류**: {rollback.get("error","")}',
                color=rb_color
            )

        # 수익 계산
        value_after   = self._total_value_usdt()
        trade_profit  = value_after - value_before   # 거래 직전/직후 잔고 변화 (거래수익)
        spread_profit = trade_usdt * abs(net_spread) / 100  # 참고용 스프레드 수익
        estimated_profit = trade_profit
        avg_cost_used = self.upbit_avg_cost.get(coin, {}).get('avg') if direction == 'BUY_OKX_SELL_UPBIT' else None

        record = {
            'time':                  datetime.now().isoformat(),
            'coin':                  coin,
            'direction':             direction,
            'net_spread_pct':        round(net_spread, 4),
            'okx_price_usdt':        okx_usdt,
            'upbit_price_krw':       upbit_krw,
            'usd_krw':               usd_krw,
            'trade_usdt':            round(trade_usdt, 4),
            'avg_cost_krw':          round(avg_cost_used, 2) if avg_cost_used else None,
            'spread_profit_usdt':    round(spread_profit, 4),
            'estimated_profit_usdt': round(real_profit, 4),
            'paper':                 PAPER_MODE,
            'success':               success,
            'okx_result':            out.get('okx', {}),
            'upbit_result':          out.get('upbit', {}),
            'rollback':              rollback,
        }

        with self.lock:
            self.trades.append(record)
            if success:
                self.daily_trades      += 1
                self.total_profit_usdt += estimated_profit
            self._save_trades()

        # 역프 성공 시: 평균단가 업데이트 + OKX 보충 + KRW 보충(단가조건)
        if success and direction == 'BUY_UPBIT_SELL_OKX':
            qty = out.get('upbit', {}).get('amount') or (krw_amount / upbit_krw)
            self._update_upbit_avg_cost(coin, upbit_krw, qty)
            threading.Thread(
                target=self._restock_okx, args=(coin, okx_usdt), daemon=True
            ).start()
            threading.Thread(
                target=self._restock_upbit_krw, args=(coin, upbit_krw, usd_krw, net_spread), daemon=True
            ).start()

        # 김프 성공 시: OKX 단가 업데이트 + 업비트 재고 보충 + OKX 재고 정리
        if success and direction == 'BUY_OKX_SELL_UPBIT':
            qty = out.get('okx', {}).get('amount') or coin_amount
            self._update_okx_avg_cost(coin, okx_usdt, qty)
            threading.Thread(
                target=self._restock_upbit_coin, args=(coin, upbit_krw, okx_usdt, usd_krw, net_spread), daemon=True
            ).start()
            threading.Thread(
                target=self._sell_okx_inventory, args=(coin, okx_usdt, net_spread), daemon=True
            ).start()

        # 거래 결과 알림
        dir_str = 'OKX매수→업비트매도' if direction == 'BUY_OKX_SELL_UPBIT' else '업비트매수→OKX매도'
        if success:
            self._notify(
                '✅ 거래 성공',
                f'**코인**: {coin}  |  **방향**: {dir_str}\n'
                f'**스프레드**: {net_spread:+.3f}%  |  **거래금액**: ${trade_usdt:.2f}\n'
                f'**예상수익**: ${estimated_profit:.4f}  |  **누적수익**: ${self.total_profit_usdt:.4f}\n'
                f'**OKX**: ${okx_usdt:.4f}  |  **업비트**: {upbit_krw:,.0f}원',
                color=0x00ff00
            )
        elif not rollback:
            self._notify(
                '❌ 거래 실패',
                f'**코인**: {coin}  |  **방향**: {dir_str}\n'
                f'**OKX 결과**: {out.get("okx",{}).get("status")}\n'
                f'**업비트 결과**: {out.get("upbit",{}).get("status")}',
                color=0xff0000
            )

        return record

    # ── 메인 루프 ─────────────────────────────────────────────────────────

    def run(self):
        mode = "모의거래(PAPER)" if PAPER_MODE else "⚠️  실거래(LIVE)"
        print("=" * 70, flush=True)
        print(f"  OKX-업비트 차익거래 봇  [{mode}]", flush=True)
        print("=" * 70, flush=True)
        print(f"  코인       : {', '.join(COINS)}", flush=True)
        print(f"  거래 금액  : 가용 잔고 {int(TRADE_RATIO*100)}% (최소 ${MIN_TRADE_USDT} / 최대 ${MAX_TRADE_USDT})", flush=True)
        print(f"  김프 기준  : {MIN_NET_SPREAD_KIMP}%  |  역프 기준: {MIN_NET_SPREAD_Rkimp}%", flush=True)
        print(f"  쿨다운     : {COOLDOWN_SEC}초  |  일일 한도: {MAX_DAILY_TRADES}회", flush=True)
        print("=" * 70, flush=True)

        if not PAPER_MODE:
            print("\n실거래 모드 - 5초 후 시작 (Ctrl+C 취소)", flush=True)
            for i in range(5, 0, -1):
                print(f"  {i}...", flush=True)
                time.sleep(1)

        print("\n모니터링 시작 (Ctrl+C 종료)\n", flush=True)
        self._notify(
            '🚀 봇 시작',
            f'**모드**: {"모의거래" if PAPER_MODE else "실거래"}\n'
            f'**코인**: {", ".join(COINS)}\n'
            f'**김프 기준**: {MIN_NET_SPREAD_KIMP}%  |  **역프 기준**: {MIN_NET_SPREAD_Rkimp}%  |  **최대 거래**: ${MAX_TRADE_USDT}',
            color=0x0099ff
        )

        iteration = 0
        self._last_snapshot_at = 0
        self._save_snapshot()  # 시작 시점 스냅샷
        while True:
            try:
                iteration += 1
                self._reset_daily_if_needed()
                now = datetime.now().strftime('%H:%M:%S')

                # 1시간마다 자산 스냅샷 기록
                if time.time() - self._last_snapshot_at >= 3600:
                    self._save_snapshot()
                    self._last_snapshot_at = time.time()

                spread_lines = []

                for coin in COINS:
                    try:
                        net_spread, okx_usdt, upbit_krw, usd_krw = self.get_spread(coin)

                        # 가격 히스토리 기록
                        self._record_price(coin, upbit_krw)

                        direction = 'BUY_OKX_SELL_UPBIT' if net_spread >= 0 else 'BUY_UPBIT_SELL_OKX'
                        dir_str   = 'OKX매수→업비트매도' if net_spread >= 0 else '업비트매수→OKX매도'
                        threshold = MIN_NET_SPREAD_KIMP if net_spread >= 0 else MIN_NET_SPREAD_Rkimp
                        signal    = '🟢' if abs(net_spread) >= threshold else '🔴'

                        line = (
                            f"  {signal} {coin:<5} | {net_spread:+.3f}% | "
                            f"OKX ${okx_usdt:<10.4f} | 업비트 {upbit_krw:>8,.0f}원 | {dir_str}"
                        )

                        # 실행 가능 여부 확인
                        if abs(net_spread) < threshold:
                            spread_lines.append(line)
                            continue

                        # 역프 + 하락장 → 거래 중단
                        if direction == 'BUY_UPBIT_SELL_OKX' and self._is_downtrend(coin, upbit_krw):
                            ma_s   = self._get_ma(coin, TREND_SHORT_MIN)
                            ma_l   = self._get_ma(coin, TREND_LONG_MIN)
                            gap    = (ma_s - ma_l) / ma_l * 100 if ma_s and ma_l else 0
                            spread_lines.append(line + f'  [하락장 차단 MA{TREND_SHORT_MIN}/{TREND_LONG_MIN} {gap:.2f}%]')
                            alert_key = f'{coin}_downtrend'
                            if alert_key not in self._low_inventory_alerted:
                                self._low_inventory_alerted.add(alert_key)
                                self._notify(
                                    f'⛔ {coin} 하락장 감지 - 역프 거래 중단',
                                    f'**단기MA({TREND_SHORT_MIN}분)**: {ma_s:,.1f}원\n'
                                    f'**장기MA({TREND_LONG_MIN}분)**: {ma_l:,.1f}원\n'
                                    f'**괴리**: {gap:.2f}% (기준 {TREND_THRESHOLD}%)\n'
                                    f'역프 거래 중단 (단기MA > 장기MA 회복 시 재개)',
                                    color=0xff0000
                                )
                            continue
                        else:
                            self._low_inventory_alerted.discard(f'{coin}_downtrend')

                        if self._in_cooldown(coin):
                            spread_lines.append(line + '  [쿨다운]')
                            continue

                        if self.daily_trades >= MAX_DAILY_TRADES:
                            spread_lines.append(line + '  [일일 한도 초과]')
                            continue

                        trade_usdt, msg = self.get_trade_amount(coin, direction, okx_usdt, upbit_krw, usd_krw)
                        if trade_usdt == 0:
                            spread_lines.append(line + f'  [거래 불가: {msg}]')
                            alert_key = f'{coin}_{direction}'
                            if alert_key not in self._low_inventory_alerted:
                                self._low_inventory_alerted.add(alert_key)
                                if direction == 'BUY_UPBIT_SELL_OKX' and 'OKX' in msg:
                                    # 역프: OKX 코인 부족 → 자동 매수 보충
                                    threading.Thread(
                                        target=self._restock_okx, args=(coin, okx_usdt), daemon=True
                                    ).start()
                                elif direction == 'BUY_UPBIT_SELL_OKX' and 'KRW' in msg:
                                    # 역프: KRW 부족 → 거래수익이 매도손실 커버 시 자동 보충
                                    threading.Thread(
                                        target=self._restock_upbit_krw, args=(coin, upbit_krw, usd_krw, net_spread), daemon=True
                                    ).start()
                                else:
                                    # 김프: 업비트 코인 부족 → 단가 조건 확인 후 자동 보충
                                    threading.Thread(
                                        target=self._restock_upbit_coin,
                                        args=(coin, upbit_krw, okx_usdt, usd_krw, net_spread),
                                        daemon=True
                                    ).start()
                            continue
                        else:
                            self._low_inventory_alerted.discard(f'{coin}_{direction}')

                        spread_lines.append(line + f'  → 실행! (${trade_usdt:.2f})')

                        result = self.execute_trade(coin, direction, net_spread, okx_usdt, upbit_krw, usd_krw, trade_usdt)
                        self.cooldowns[coin] = datetime.now()

                        status = '성공' if result['success'] else '실패'
                        print(f"\n[{now}] {status} | {coin} | {dir_str}", flush=True)
                        print(f"  스프레드: {net_spread:+.3f}% | 거래금액: ${trade_usdt:.2f} | OKX: ${okx_usdt:.4f} | 업비트: {upbit_krw:,.0f}원", flush=True)
                        print(f"  실제수익: ${result['estimated_profit_usdt']:.4f} USDT "
                              f"(스프레드: ${result['spread_profit_usdt']:.4f})"
                              f" | 누적: ${self.total_profit_usdt:.4f}", flush=True)
                        if not result['success']:
                            print(f"  OKX 결과   : {result['okx_result']}", flush=True)
                            print(f"  업비트 결과: {result['upbit_result']}", flush=True)
                        print(flush=True)

                    except Exception as e:
                        spread_lines.append(f"  ⚠️  {coin:<5} | 오류: {e}")

                # 5회마다 대시보드 출력
                if iteration % 5 == 1:
                    current_value = self._total_value_usdt()
                    total_pnl     = current_value - self.value_at_start   # 전체 변화
                    trade_pnl     = self.total_profit_usdt                 # 거래 수익만
                    price_pnl     = total_pnl - trade_pnl                  # 가격 변동
                    # 잔고 조회
                    try:
                        ob = self.okx.fetch_balance()
                        ub = self.upbit.fetch_balance()
                        okx_usdt  = ob.get('USDT',{}).get('free',0)
                        ub_krw    = ub.get('KRW', {}).get('free',0)
                        bal_lines = []
                        for c in COINS:
                            oq = ob.get(c,{}).get('free',0)
                            uq = ub.get(c,{}).get('free',0)
                            if oq > 0.0001 or uq > 0.0001:
                                bal_lines.append(f"{c} OKX:{oq:.2f} 업비:{uq:.2f}")
                        bal_str = '  '.join(bal_lines)
                    except Exception:
                        okx_usdt = ub_krw = 0
                        bal_str  = ''

                    print(f"[{now}] 환율: {self.usd_krw:,.0f}  | "
                          f"거래: {self.daily_trades}회  | "
                          f"거래수익: ${trade_pnl:+.4f}  |  "
                          f"가격변동: ${price_pnl:+.4f}  |  "
                          f"합계: ${total_pnl:+.4f} ({total_pnl*self.usd_krw:+,.0f}원)",
                          flush=True)
                    print(f"  [잔고] OKX USDT:${okx_usdt:.2f}  업비트 KRW:{ub_krw:,.0f}원  {bal_str}",
                          flush=True)
                    for line in spread_lines:
                        print(line, flush=True)
                    print(flush=True)

                time.sleep(CHECK_INTERVAL)

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 루프 오류: {e}", flush=True)
                time.sleep(5)

        # 종료 요약
        success_trades = [t for t in self.trades if t.get('success')]
        total_profit   = sum(t.get('estimated_profit_usdt', 0) for t in success_trades)

        print("\n" + "=" * 70)
        print("  종료 요약")
        print("=" * 70)
        print(f"  성공 거래  : {len(success_trades)}회")
        print(f"  누적 수익  : ${total_profit:.4f} USDT")
        print(f"  로그 파일  : {LOG_FILE}")
        print("=" * 70)

        self._notify(
            '🛑 봇 종료',
            f'**성공 거래**: {len(success_trades)}회\n'
            f'**누적 수익**: ${total_profit:.4f} USDT',
            color=0x888888
        )


if __name__ == '__main__':
    bot = ArbitrageBot()
    bot.run()
