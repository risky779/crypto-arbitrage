const pnlData = {
  "updated_at": "2026-08-01 01:46:04",
  "usd_krw": 1429.51,
  "total_asset_krw": 343436,
  "daily_pnl_krw": 101,
  "daily_yield_pct": 0.029,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 454267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -110831,
    "seed_yield_pct": -24.398,
    "days_since_seed": 13,
    "avg_daily_yield_pct": -1.877
  },
  "reconciliation": {
    "since": "2026-07-25",
    "combined_realized_usd": -3.05,
    "combined_actual_delta_usd": -64.44,
    "drift_usd": -61.39,
    "drift_pct": -25.554,
    "status": "WARNING",
    "note": "drift = 실제총자산 증감(마크투마켓 포함) - 원장상 실현손익합계. 헷지 정상이면 작아야 함."
  },
  "bot_reconciliation": {
    "twin_bot": {
      "displayed_asset_krw": 86210,
      "twr_implied_asset_krw": 184906,
      "drift_krw": -98697,
      "drift_pct": -114.48,
      "status": "WARNING"
    },
    "main_bot": {
      "displayed_asset_krw": 257226,
      "twr_implied_asset_krw": 246290,
      "drift_krw": 10936,
      "drift_pct": 4.25,
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
      "total_krw": 343335
    },
    {
      "date": "2026-08-01",
      "total_krw": 343436
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
      "total_asset_krw": 343436,
      "main_pnl_krw": 101,
      "twin_pnl_krw": 0,
      "total_pnl_krw": 101,
      "main_pnl_pct": 0.039,
      "twin_pnl_pct": -0.001,
      "total_pnl_pct": 0.029,
      "target_met": false
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 257226,
      "balance_krw": 166042,
      "balance_usdt": 10.05,
      "cum_pnl_krw": 3281,
      "cum_pnl_pct": 1.292,
      "cum_pnl_since": "2026-07-28",
      "twr_pct": -0.7893,
      "twr_events": 10,
      "twr_since": "2026-07-25",
      "total_pnl_usd_record": 201.07,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": 101,
      "daily_pnl_pct": 0.039,
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
      "asset_krw": 86210,
      "xrp_bithumb": 7.2603,
      "xrp_okx": 59.3271,
      "xrp_target": 59.3848,
      "hedge_upnl_usd": 1.6091,
      "cum_pnl_krw": -98899,
      "cum_pnl_pct": -53.427,
      "cum_pnl_since": "2026-07-28",
      "twr_pct": -1.2828,
      "twr_events": 123,
      "twr_since": "2026-07-25",
      "session_pnl_usd_record": 2.562,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": 0,
      "daily_pnl_pct": -0.001,
      "daily_target_met": false,
      "today_trades": 0,
      "recent_trades": [
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
        },
        {
          "time": "2026-07-31T23:09:01.697520",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.459,
          "pnl_usd": 0.0225
        }
      ]
    }
  }
};