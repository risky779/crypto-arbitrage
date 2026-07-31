const pnlData = {
  "updated_at": "2026-07-31 23:01:03",
  "usd_krw": 1429.51,
  "total_asset_krw": 421349,
  "daily_pnl_krw": -1957,
  "daily_yield_pct": -0.462,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 454267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -32918,
    "seed_yield_pct": -7.246,
    "days_since_seed": 12,
    "avg_daily_yield_pct": -0.604
  },
  "reconciliation": {
    "since": "2026-07-25",
    "combined_realized_usd": -3.3,
    "combined_actual_delta_usd": -9.94,
    "drift_usd": -6.64,
    "drift_pct": -2.254,
    "status": "OK",
    "note": "drift = 실제총자산 증감(마크투마켓 포함) - 원장상 실현손익합계. 헷지 정상이면 작아야 함."
  },
  "bot_reconciliation": {
    "twin_bot": {
      "displayed_asset_krw": 165290,
      "twr_implied_asset_krw": 184557,
      "drift_krw": -19268,
      "drift_pct": -11.66,
      "status": "WARNING"
    },
    "main_bot": {
      "displayed_asset_krw": 256059,
      "twr_implied_asset_krw": 246290,
      "drift_krw": 9769,
      "drift_pct": 3.82,
      "status": "OK"
    },
    "note": "drift = 표시자산(shift보정) - TWR내포자산(그 봇 자체 거래+이체비용만). 크면 cum_capital_shift_krw가 못 잡은 미기록 자본이동 의심."
  },
  "asset_trend": [
    {
      "date": "2026-07-25",
      "total_krw": 446968
    },
    {
      "date": "2026-07-26",
      "total_krw": 442992
    },
    {
      "date": "2026-07-27",
      "total_krw": 443517
    },
    {
      "date": "2026-07-28",
      "total_krw": 439056
    },
    {
      "date": "2026-07-29",
      "total_krw": 431012
    },
    {
      "date": "2026-07-30",
      "total_krw": 423306
    },
    {
      "date": "2026-07-31",
      "total_krw": 421349
    }
  ],
  "daily_history": [
    {
      "date": "2026-07-25",
      "total_asset_krw": 446968,
      "main_pnl_krw": null,
      "twin_pnl_krw": null,
      "total_pnl_krw": null,
      "main_pnl_pct": null,
      "twin_pnl_pct": null,
      "total_pnl_pct": null,
      "target_met": null
    },
    {
      "date": "2026-07-26",
      "total_asset_krw": 442992,
      "main_pnl_krw": -1412,
      "twin_pnl_krw": -2565,
      "total_pnl_krw": -3976,
      "main_pnl_pct": -0.554,
      "twin_pnl_pct": -1.334,
      "total_pnl_pct": -0.89,
      "target_met": false
    },
    {
      "date": "2026-07-27",
      "total_asset_krw": 443517,
      "main_pnl_krw": 594,
      "twin_pnl_krw": -69,
      "total_pnl_krw": 525,
      "main_pnl_pct": 0.235,
      "twin_pnl_pct": -0.037,
      "total_pnl_pct": 0.119,
      "target_met": false
    },
    {
      "date": "2026-07-28",
      "total_asset_krw": 439056,
      "main_pnl_krw": 0,
      "twin_pnl_krw": -4463,
      "total_pnl_krw": -4461,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -2.354,
      "total_pnl_pct": -1.006,
      "target_met": false
    },
    {
      "date": "2026-07-29",
      "total_asset_krw": 431012,
      "main_pnl_krw": 0,
      "twin_pnl_krw": -8042,
      "total_pnl_krw": -8044,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -4.345,
      "total_pnl_pct": -1.832,
      "target_met": false
    },
    {
      "date": "2026-07-30",
      "total_asset_krw": 423306,
      "main_pnl_krw": -521,
      "twin_pnl_krw": -7185,
      "total_pnl_krw": -7706,
      "main_pnl_pct": -0.205,
      "twin_pnl_pct": -4.058,
      "total_pnl_pct": -1.788,
      "target_met": false
    },
    {
      "date": "2026-07-31",
      "total_asset_krw": 421349,
      "main_pnl_krw": 2635,
      "twin_pnl_krw": -4592,
      "total_pnl_krw": -1957,
      "main_pnl_pct": 1.04,
      "twin_pnl_pct": -2.703,
      "total_pnl_pct": -0.462,
      "target_met": false
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 256059,
      "balance_krw": 25513,
      "balance_usdt": 107.29,
      "cum_pnl_krw": 2114,
      "cum_pnl_pct": 0.832,
      "cum_pnl_since": "2026-07-28",
      "twr_pct": -0.7893,
      "twr_events": 10,
      "twr_since": "2026-07-25",
      "total_pnl_usd_record": 201.07,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": 2635,
      "daily_pnl_pct": 1.04,
      "daily_target_met": true,
      "today_trades": 0,
      "pending_transfers": 0,
      "restart_count": 1,
      "recent_trades": [
        {
          "time": "2026-07-30T13:40:04.468295",
          "coin": "XLM",
          "profit_usd": 0.1462
        },
        {
          "time": "2026-07-30T12:36:11.883013",
          "coin": "XLM",
          "profit_usd": 0.2262
        },
        {
          "time": "2026-07-30T12:32:05.414682",
          "coin": "XLM",
          "profit_usd": 0.2487
        },
        {
          "time": "2026-07-30T10:40:46.587146",
          "coin": "XLM",
          "profit_usd": 0.2465
        },
        {
          "time": "2026-07-30T10:38:01.608762",
          "coin": "SUI",
          "profit_usd": 0.2568
        },
        {
          "time": "2026-07-30T10:29:02.763836",
          "coin": "XLM",
          "profit_usd": 0.2467
        },
        {
          "time": "2026-07-21T18:54:59.276261",
          "coin": "SUI",
          "profit_usd": 0.0752
        },
        {
          "time": "2026-07-21T18:48:53.380076",
          "coin": "SUI",
          "profit_usd": 0.1924
        },
        {
          "time": "2026-07-21T18:48:32.870122",
          "coin": "XLM",
          "profit_usd": 0.1446
        },
        {
          "time": "2026-07-21T12:32:51.447574",
          "coin": "SUI",
          "profit_usd": 0.1793
        }
      ]
    },
    "twin_bot": {
      "label": "쌍둥이봇 · 양쪽재고 로컬거래",
      "running": true,
      "asset_krw": 165290,
      "xrp_bithumb": 99.4996,
      "xrp_okx": 19.2475,
      "xrp_target": 59.3848,
      "hedge_upnl_usd": 1.0427,
      "cum_pnl_krw": -19819,
      "cum_pnl_pct": -10.707,
      "cum_pnl_since": "2026-07-28",
      "twr_pct": -1.4691,
      "twr_events": 109,
      "twr_since": "2026-07-25",
      "session_pnl_usd_record": 2.3179,
      "today_pnl_usd_record": 0.0216,
      "daily_pnl_krw": -4592,
      "daily_pnl_pct": -2.703,
      "daily_target_met": false,
      "today_trades": 2,
      "recent_trades": [
        {
          "time": "2026-07-31T23:00:53.411861",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.299,
          "pnl_usd": 0.0111
        },
        {
          "time": "2026-07-31T22:54:59.836967",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.289,
          "pnl_usd": 0.0105
        },
        {
          "time": "2026-07-30T13:45:08.980545",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 1.685,
          "pnl_usd": 0.1063
        },
        {
          "time": "2026-07-30T13:44:34.635278",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 1.609,
          "pnl_usd": 0.1012
        },
        {
          "time": "2026-07-30T13:33:33.888024",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 1.618,
          "pnl_usd": 0.1018
        },
        {
          "time": "2026-07-29T18:22:07.355856",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 1.644,
          "pnl_usd": 0.0516
        },
        {
          "time": "2026-07-29T10:55:59.868351",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.722,
          "pnl_usd": 0.0341
        },
        {
          "time": "2026-07-29T10:53:16.397339",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.769,
          "pnl_usd": 0.0624
        },
        {
          "time": "2026-07-29T09:37:42.722730",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 1.279,
          "pnl_usd": 0.0421
        },
        {
          "time": "2026-07-29T09:37:08.617472",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 1.324,
          "pnl_usd": 0.0818
        }
      ]
    }
  }
};