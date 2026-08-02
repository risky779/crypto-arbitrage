const pnlData = {
  "updated_at": "2026-08-02 11:46:55",
  "usd_krw": 1438.2,
  "total_asset_krw": 420565,
  "daily_pnl_krw": -776,
  "daily_yield_pct": -0.184,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 454267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -33702,
    "seed_yield_pct": -7.419,
    "days_since_seed": 14,
    "avg_daily_yield_pct": -0.53
  },
  "reconciliation": {
    "since": "2026-07-25",
    "combined_realized_usd": -2.91,
    "combined_actual_delta_usd": -12.27,
    "drift_usd": -9.36,
    "drift_pct": -3.201,
    "status": "WARNING",
    "note": "drift = 실제총자산 증감(마크투마켓 포함) - 원장상 실현손익합계. 헷지 정상이면 작아야 함."
  },
  "bot_reconciliation": {
    "twin_bot": {
      "displayed_asset_krw": 195029,
      "twr_implied_asset_krw": 186240,
      "drift_krw": 8789,
      "drift_pct": 4.51,
      "status": "OK"
    },
    "main_bot": {
      "displayed_asset_krw": 225536,
      "twr_implied_asset_krw": 247786,
      "drift_krw": -22251,
      "drift_pct": -9.87,
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
      "total_krw": 421341
    },
    {
      "date": "2026-08-02",
      "total_krw": 420565
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
      "main_pnl_krw": 0,
      "twin_pnl_krw": -79971,
      "total_pnl_krw": -79971,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -47.075,
      "total_pnl_pct": -18.892,
      "target_met": false
    },
    {
      "date": "2026-08-01",
      "total_asset_krw": 421341,
      "main_pnl_krw": -26938,
      "twin_pnl_krw": 104945,
      "total_pnl_krw": 78007,
      "main_pnl_pct": -10.63,
      "twin_pnl_pct": 116.721,
      "total_pnl_pct": 22.72,
      "target_met": true
    },
    {
      "date": "2026-08-02",
      "total_asset_krw": 420565,
      "main_pnl_krw": -951,
      "twin_pnl_krw": 174,
      "total_pnl_krw": -776,
      "main_pnl_pct": -0.42,
      "twin_pnl_pct": 0.089,
      "total_pnl_pct": -0.184,
      "target_met": false
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 225536,
      "balance_krw": 226871,
      "balance_usdt": 60.78,
      "cum_pnl_krw": -1971,
      "cum_pnl_pct": -0.7893,
      "cum_pnl_since": "2026-07-25",
      "twr_pct": -0.7893,
      "twr_events": 10,
      "twr_since": "2026-07-25",
      "total_pnl_usd_record": 201.07,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": null,
      "daily_pnl_pct": null,
      "daily_target_met": null,
      "today_trades": 0,
      "pending_transfers": 0,
      "restart_count": 1,
      "recent_trades": [
        {
          "time": "2026-07-30T13:40:04.468295",
          "coin": "XLM",
          "profit_usd": 0.1462,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.1462
        },
        {
          "time": "2026-07-30T12:36:11.883013",
          "coin": "XLM",
          "profit_usd": 0.2262,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.2262
        },
        {
          "time": "2026-07-30T12:32:05.414682",
          "coin": "XLM",
          "profit_usd": 0.2487,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.2487
        },
        {
          "time": "2026-07-30T10:40:46.587146",
          "coin": "XLM",
          "profit_usd": 0.2465,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.2465
        },
        {
          "time": "2026-07-30T10:38:01.608762",
          "coin": "SUI",
          "profit_usd": 0.2568,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.2568
        },
        {
          "time": "2026-07-30T10:29:02.763836",
          "coin": "XLM",
          "profit_usd": 0.2467,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.2467
        },
        {
          "time": "2026-07-21T18:54:59.276261",
          "coin": "SUI",
          "profit_usd": 0.0752,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.0752
        },
        {
          "time": "2026-07-21T18:48:53.380076",
          "coin": "SUI",
          "profit_usd": 0.1924,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.1924
        },
        {
          "time": "2026-07-21T18:48:32.870122",
          "coin": "XLM",
          "profit_usd": 0.1446,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.1446
        },
        {
          "time": "2026-07-21T12:32:51.447574",
          "coin": "SUI",
          "profit_usd": 0.1793,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.1793
        }
      ]
    },
    "twin_bot": {
      "label": "쌍둥이봇 · 양쪽재고 로컬거래",
      "running": true,
      "asset_krw": 195029,
      "xrp_bithumb": 19.0705,
      "xrp_okx": 32.3606,
      "xrp_target": 25.7189,
      "hedge_upnl_usd": 0.1371,
      "cum_pnl_krw": -2207,
      "cum_pnl_pct": -1.1713,
      "cum_pnl_since": "2026-07-25",
      "twr_pct": -1.1713,
      "twr_events": 165,
      "twr_since": "2026-07-25",
      "session_pnl_usd_record": 3.0457,
      "today_pnl_usd_record": 0.063,
      "daily_pnl_krw": null,
      "daily_pnl_pct": null,
      "daily_target_met": null,
      "today_trades": 6,
      "recent_trades": [
        {
          "time": "2026-08-02T05:40:35.277603",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.281,
          "pnl_usd": 0.0099,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.0099
        },
        {
          "time": "2026-08-02T04:33:57.982132",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.283,
          "pnl_usd": 0.0089,
          "allocated_cost_usd": 0.00042,
          "net_pnl_usd": 0.00848
        },
        {
          "time": "2026-08-02T04:16:53.947221",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.282,
          "pnl_usd": 0.01,
          "allocated_cost_usd": 0.00042,
          "net_pnl_usd": 0.00958
        },
        {
          "time": "2026-08-02T03:55:02.189878",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.321,
          "pnl_usd": 0.0127,
          "allocated_cost_usd": 0.00042,
          "net_pnl_usd": 0.01228
        },
        {
          "time": "2026-08-02T03:54:28.630684",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.302,
          "pnl_usd": 0.0113,
          "allocated_cost_usd": 0.00042,
          "net_pnl_usd": 0.01088
        },
        {
          "time": "2026-08-02T03:51:15.261351",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.285,
          "pnl_usd": 0.0102,
          "allocated_cost_usd": 0.00042,
          "net_pnl_usd": 0.00978
        },
        {
          "time": "2026-08-01T19:18:22.130583",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.307,
          "pnl_usd": 0.0116,
          "allocated_cost_usd": 0.00042,
          "net_pnl_usd": 0.01118
        },
        {
          "time": "2026-08-01T15:15:40.120434",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.345,
          "pnl_usd": 0.0131,
          "allocated_cost_usd": 0.00223,
          "net_pnl_usd": 0.01087
        },
        {
          "time": "2026-08-01T15:11:21.497459",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.307,
          "pnl_usd": 0.0117,
          "allocated_cost_usd": 0.00223,
          "net_pnl_usd": 0.00947
        },
        {
          "time": "2026-08-01T15:10:47.680199",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.307,
          "pnl_usd": 0.0117,
          "allocated_cost_usd": 0.00223,
          "net_pnl_usd": 0.00947
        }
      ]
    }
  }
};