const pnlData = {
  "updated_at": "2026-08-01 03:31:03",
  "usd_krw": 1429.51,
  "total_asset_krw": 421613,
  "daily_pnl_krw": 78278,
  "daily_yield_pct": 22.799,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 454267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -32654,
    "seed_yield_pct": -7.188,
    "days_since_seed": 13,
    "avg_daily_yield_pct": -0.553
  },
  "reconciliation": {
    "since": "2026-07-25",
    "combined_realized_usd": -3.05,
    "combined_actual_delta_usd": -9.76,
    "drift_usd": -6.71,
    "drift_pct": -2.273,
    "status": "OK",
    "note": "drift = 실제총자산 증감(마크투마켓 포함) - 원장상 실현손익합계. 헷지 정상이면 작아야 함."
  },
  "bot_reconciliation": {
    "twin_bot": {
      "displayed_asset_krw": 245125,
      "twr_implied_asset_krw": 184908,
      "drift_krw": 60217,
      "drift_pct": 24.57,
      "status": "WARNING"
    },
    "main_bot": {
      "displayed_asset_krw": 176488,
      "twr_implied_asset_krw": 246290,
      "drift_krw": -69802,
      "drift_pct": -39.55,
      "status": "WARNING"
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
      "total_krw": 343335
    },
    {
      "date": "2026-08-01",
      "total_krw": 421613
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
      "total_asset_krw": 343335,
      "main_pnl_krw": 3700,
      "twin_pnl_krw": -83672,
      "total_pnl_krw": -79971,
      "main_pnl_pct": 1.46,
      "twin_pnl_pct": -49.253,
      "total_pnl_pct": -18.892,
      "target_met": false
    },
    {
      "date": "2026-08-01",
      "total_asset_krw": 421613,
      "main_pnl_krw": -80636,
      "twin_pnl_krw": 158915,
      "total_pnl_krw": 78278,
      "main_pnl_pct": -31.361,
      "twin_pnl_pct": 184.334,
      "total_pnl_pct": 22.799,
      "target_met": true
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 176488,
      "balance_krw": 176076,
      "balance_usdt": 2.27,
      "cum_pnl_krw": -77457,
      "cum_pnl_pct": -30.501,
      "cum_pnl_since": "2026-07-28",
      "twr_pct": -0.7893,
      "twr_events": 10,
      "twr_since": "2026-07-25",
      "total_pnl_usd_record": 201.07,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": -80636,
      "daily_pnl_pct": -31.361,
      "daily_target_met": false,
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
      "asset_krw": 245125,
      "xrp_bithumb": 78.7844,
      "xrp_okx": 39.8433,
      "xrp_target": 33.2887,
      "hedge_upnl_usd": 1.0309,
      "cum_pnl_krw": 60016,
      "cum_pnl_pct": 32.422,
      "cum_pnl_since": "2026-07-28",
      "twr_pct": -1.2819,
      "twr_events": 125,
      "twr_since": "2026-07-25",
      "session_pnl_usd_record": 2.5738,
      "today_pnl_usd_record": 0.0118,
      "daily_pnl_krw": 158915,
      "daily_pnl_pct": 184.334,
      "daily_target_met": true,
      "today_trades": 1,
      "recent_trades": [
        {
          "time": "2026-08-01T03:19:34.345623",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.308,
          "pnl_usd": 0.0118
        },
        {
          "time": "2026-07-31T23:14:04.345784",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.43,
          "pnl_usd": 0.0204
        },
        {
          "time": "2026-07-31T23:13:30.481784",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.392,
          "pnl_usd": 0.0177
        },
        {
          "time": "2026-07-31T23:12:56.636507",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.29,
          "pnl_usd": 0.0105
        },
        {
          "time": "2026-07-31T23:12:23.237336",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.411,
          "pnl_usd": 0.0191
        },
        {
          "time": "2026-07-31T23:11:49.686910",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.403,
          "pnl_usd": 0.0185
        },
        {
          "time": "2026-07-31T23:11:16.167103",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.422,
          "pnl_usd": 0.0198
        },
        {
          "time": "2026-07-31T23:10:42.067136",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.367,
          "pnl_usd": 0.0159
        },
        {
          "time": "2026-07-31T23:10:08.481809",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.45,
          "pnl_usd": 0.0218
        },
        {
          "time": "2026-07-31T23:09:35.093531",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.451,
          "pnl_usd": 0.0218
        }
      ]
    }
  }
};