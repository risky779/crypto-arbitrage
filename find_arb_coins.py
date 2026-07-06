#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OKX-업비트 공통 코인 스프레드 스캐너
- 양 거래소에 동시 상장된 전체 코인 대상
- 스프레드 기준 내림차순 정렬
- 결과를 콘솔 + JSON으로 저장
"""

import ccxt, sys, io, time, json, concurrent.futures
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ========== 설정 ==========
TARGET_SPREAD = 5.0     # 이 이상이면 강조 표시
OKX_FEE   = 0.10       # OKX 수수료 %
UPBIT_FEE = 0.05       # 업비트 수수료 %
TOTAL_FEE = OKX_FEE + UPBIT_FEE
RESULT_FILE = 'arb_scan_result.json'
MAX_WORKERS = 5         # 동시 조회 스레드 수 (rate limit 고려)
# ==========================

okx   = ccxt.okx({'enableRateLimit': True, 'rateLimit': 200})
upbit = ccxt.upbit({'enableRateLimit': True, 'rateLimit': 200})


def get_usd_krw():
    try:
        return upbit.fetch_ticker('USDT/KRW')['last']
    except Exception:
        return 1380


def find_common_coins():
    """OKX(USDT 마켓) ∩ 업비트(KRW 마켓) 공통 코인 반환"""
    print("마켓 정보 로딩 중...")
    okx.load_markets()
    upbit.load_markets()

    okx_coins   = {s.split('/')[0] for s in okx.markets   if s.endswith('/USDT')}
    upbit_coins = {s.split('/')[0] for s in upbit.markets if s.endswith('/KRW')}

    common = sorted(okx_coins & upbit_coins)
    print(f"OKX USDT 마켓: {len(okx_coins)}개  |  업비트 KRW 마켓: {len(upbit_coins)}개  |  공통: {len(common)}개\n")
    return common


def fetch_spread(coin, usd_krw):
    """단일 코인 스프레드 계산. 오류 시 None 반환"""
    try:
        okx_ticker   = okx.fetch_ticker(f'{coin}/USDT')
        upbit_ticker = upbit.fetch_ticker(f'{coin}/KRW')

        okx_usdt  = okx_ticker['last']
        upbit_krw = upbit_ticker['last']

        if not okx_usdt or not upbit_krw:
            return None

        okx_krw    = okx_usdt * usd_krw
        raw_spread = (upbit_krw - okx_krw) / okx_krw * 100
        net_spread = raw_spread - TOTAL_FEE

        # 업비트 24h 거래량(KRW) - 유동성 지표
        upbit_vol_krw = (upbit_ticker.get('quoteVolume') or 0)

        return {
            'coin':        coin,
            'okx_usdt':    okx_usdt,
            'upbit_krw':   upbit_krw,
            'okx_krw':     round(okx_krw, 4),
            'raw_spread':  round(raw_spread, 4),
            'net_spread':  round(net_spread, 4),
            'direction':   'OKX매수→업비트매도' if raw_spread > 0 else '업비트매수→OKX매도',
            'upbit_vol_krw': round(upbit_vol_krw),
        }
    except Exception:
        return None


def main():
    print("=" * 70)
    print("  OKX-업비트 스프레드 스캐너")
    print("=" * 70)

    usd_krw = get_usd_krw()
    print(f"환율: 1 USDT = {usd_krw:,.0f} KRW\n")

    common_coins = find_common_coins()
    total = len(common_coins)
    results = []
    errors  = 0

    print(f"총 {total}개 코인 스프레드 조회 중...\n")
    start = time.time()

    # 병렬 조회 (rate limit 고려해 MAX_WORKERS 제한)
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_spread, coin, usd_krw): coin for coin in common_coins}
        done = 0
        for future in concurrent.futures.as_completed(futures):
            done += 1
            result = future.result()
            if result:
                results.append(result)
            else:
                errors += 1
            # 진행률 표시
            print(f"\r  조회 중... {done}/{total} (오류: {errors})", end='', flush=True)

    elapsed = time.time() - start
    print(f"\r  완료: {len(results)}개 성공, {errors}개 실패  ({elapsed:.1f}초)\n")

    # 절댓값 스프레드 기준 정렬
    results.sort(key=lambda x: abs(x['net_spread']), reverse=True)

    # ── 출력 ──────────────────────────────────────────────────────────────
    print("=" * 90)
    print(f"  {'순위':>4}  {'코인':<7} {'순수익':>8}  {'원시스프레드':>10}  {'방향':<18}  {'업비트거래량(억원)':>16}")
    print("=" * 90)

    highlight = []
    for i, r in enumerate(results, 1):
        vol_100m = r['upbit_vol_krw'] / 1e8  # 억원 단위
        marker = '★' if abs(r['net_spread']) >= TARGET_SPREAD else ' '

        print(
            f"  {marker}{i:>3}  {r['coin']:<7} {r['net_spread']:>+7.3f}%  "
            f"{r['raw_spread']:>+9.3f}%  {r['direction']:<18}  {vol_100m:>12.1f}억"
        )

        if abs(r['net_spread']) >= TARGET_SPREAD:
            highlight.append(r)

    print("=" * 90)
    print(f"  ★ = 순수익 {TARGET_SPREAD}% 이상  |  수수료 {TOTAL_FEE}% 차감 기준\n")

    # ── 핵심 결과 요약 ─────────────────────────────────────────────────────
    if highlight:
        print(f"{'='*70}")
        print(f"  순수익 {TARGET_SPREAD}% 이상 코인 ({len(highlight)}개) — 차익거래 우선 대상")
        print(f"{'='*70}")
        for r in highlight:
            print(f"  {r['coin']:<6}  순수익 {r['net_spread']:>+.3f}%  |  {r['direction']}")
            print(f"         OKX: ${r['okx_usdt']:.6f}  |  업비트: {r['upbit_krw']:,.4f}원")
            vol_100m = r['upbit_vol_krw'] / 1e8
            print(f"         업비트 24h 거래량: {vol_100m:.1f}억원")
            print()
    else:
        print(f"  현재 순수익 {TARGET_SPREAD}% 이상 코인 없음")
        print(f"  상위 5개:")
        for r in results[:5]:
            print(f"    {r['coin']:<6}  {r['net_spread']:>+.3f}%  |  {r['direction']}")

    # ── JSON 저장 ──────────────────────────────────────────────────────────
    output = {
        'scanned_at': datetime.now().isoformat(),
        'usd_krw':    usd_krw,
        'total_fee_pct': TOTAL_FEE,
        'total_coins': len(results),
        'results':    results,
        'highlight_over_5pct': highlight,
    }
    with open(RESULT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n결과 저장: {RESULT_FILE}")
    print(f"스캔 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


if __name__ == '__main__':
    main()
