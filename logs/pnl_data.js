const pnlData = {
  "updated_at": "2026-08-05 17:31:04",
  "usd_krw": 1428.89,
  "total_asset_krw": 437838,
  "daily_pnl_krw": 172,
  "daily_yield_pct": 0.039,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 474267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -36429,
    "seed_yield_pct": -7.681,
    "days_since_seed": 17,
    "avg_daily_yield_pct": -0.452
  },
  "reconciliation": {
    "since": "2026-07-25",
    "combined_realized_usd": -2.6,
    "combined_actual_delta_usd": 1.73,
    "drift_usd": 4.32,
    "drift_pct": 1.411,
    "status": "OK",
    "note": "drift = 실제총자산 증감(마크투마켓 포함) - 원장상 실현손익합계. 헷지 정상이면 작아야 함."
  },
  "unallocated": {
    "krw": -5421,
    "pct": -1.24,
    "status": "OK",
    "note": "총자산(실측) - (메인봇+쌍둥이봇 TWR기준 자산). 봇별 원장이 실제잔고와 못 맞춘 부분 — 크면 TWR 원장에 미기록 이벤트 의심."
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
      "total_krw": 419351
    },
    {
      "date": "2026-08-03",
      "total_krw": 440343
    },
    {
      "date": "2026-08-04",
      "total_krw": 437623
    },
    {
      "date": "2026-08-05",
      "total_krw": 437838
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
      "main_pnl_krw": -3,
      "twin_pnl_krw": -1698,
      "total_pnl_krw": -1701,
      "main_pnl_pct": -0.001,
      "twin_pnl_pct": -0.883,
      "total_pnl_pct": -0.381,
      "target_met": false
    },
    {
      "date": "2026-07-27",
      "total_asset_krw": 443517,
      "main_pnl_krw": 0,
      "twin_pnl_krw": 0,
      "total_pnl_krw": 0,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": 0.0,
      "total_pnl_pct": 0.0,
      "target_met": false
    },
    {
      "date": "2026-07-28",
      "total_asset_krw": 439056,
      "main_pnl_krw": 0,
      "twin_pnl_krw": -284,
      "total_pnl_krw": -284,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -0.15,
      "total_pnl_pct": -0.064,
      "target_met": false
    },
    {
      "date": "2026-07-29",
      "total_asset_krw": 431012,
      "main_pnl_krw": 0,
      "twin_pnl_krw": -114,
      "total_pnl_krw": -114,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -0.062,
      "total_pnl_pct": -0.026,
      "target_met": false
    },
    {
      "date": "2026-07-30",
      "total_asset_krw": 423306,
      "main_pnl_krw": -1956,
      "twin_pnl_krw": -765,
      "total_pnl_krw": -2721,
      "main_pnl_pct": -0.77,
      "twin_pnl_pct": -0.432,
      "total_pnl_pct": -0.631,
      "target_met": false
    },
    {
      "date": "2026-07-31",
      "total_asset_krw": 343335,
      "main_pnl_krw": 0,
      "twin_pnl_krw": 380,
      "total_pnl_krw": 380,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": 0.224,
      "total_pnl_pct": 0.09,
      "target_met": false
    },
    {
      "date": "2026-08-01",
      "total_asset_krw": 421341,
      "main_pnl_krw": 0,
      "twin_pnl_krw": 134,
      "total_pnl_krw": 134,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": 0.149,
      "total_pnl_pct": 0.039,
      "target_met": false
    },
    {
      "date": "2026-08-02",
      "total_asset_krw": 419351,
      "main_pnl_krw": 0,
      "twin_pnl_krw": 183,
      "total_pnl_krw": 183,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": 0.094,
      "total_pnl_pct": 0.043,
      "target_met": false
    },
    {
      "date": "2026-08-03",
      "total_asset_krw": 440343,
      "main_pnl_krw": 0,
      "twin_pnl_krw": 0,
      "total_pnl_krw": 0,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": 0.0,
      "total_pnl_pct": 0.0,
      "target_met": false
    },
    {
      "date": "2026-08-04",
      "total_asset_krw": 437623,
      "main_pnl_krw": 0,
      "twin_pnl_krw": 163,
      "total_pnl_krw": 163,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": 0.06,
      "total_pnl_pct": 0.037,
      "target_met": false
    },
    {
      "date": "2026-08-05",
      "total_asset_krw": 437838,
      "main_pnl_krw": 0,
      "twin_pnl_krw": 172,
      "total_pnl_krw": 172,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": 0.064,
      "total_pnl_pct": 0.039,
      "target_met": false
    }
  ],
  "realized_pnl_history": [
    {
      "date": "2026-07-25",
      "main_cum_krw": 0,
      "twin_cum_krw": 79,
      "total_cum_krw": 79
    },
    {
      "date": "2026-07-26",
      "main_cum_krw": -3,
      "twin_cum_krw": -1619,
      "total_cum_krw": -1622
    },
    {
      "date": "2026-07-27",
      "main_cum_krw": -3,
      "twin_cum_krw": -1619,
      "total_cum_krw": -1622
    },
    {
      "date": "2026-07-28",
      "main_cum_krw": -3,
      "twin_cum_krw": -1903,
      "total_cum_krw": -1906
    },
    {
      "date": "2026-07-29",
      "main_cum_krw": -3,
      "twin_cum_krw": -2017,
      "total_cum_krw": -2020
    },
    {
      "date": "2026-07-30",
      "main_cum_krw": -1959,
      "twin_cum_krw": -2782,
      "total_cum_krw": -4741
    },
    {
      "date": "2026-07-31",
      "main_cum_krw": -1959,
      "twin_cum_krw": -2402,
      "total_cum_krw": -4361
    },
    {
      "date": "2026-08-01",
      "main_cum_krw": -1959,
      "twin_cum_krw": -2268,
      "total_cum_krw": -4227
    },
    {
      "date": "2026-08-02",
      "main_cum_krw": -1959,
      "twin_cum_krw": -2085,
      "total_cum_krw": -4044
    },
    {
      "date": "2026-08-03",
      "main_cum_krw": -1959,
      "twin_cum_krw": -2085,
      "total_cum_krw": -4044
    },
    {
      "date": "2026-08-04",
      "main_cum_krw": -1959,
      "twin_cum_krw": -1922,
      "total_cum_krw": -3881
    },
    {
      "date": "2026-08-05",
      "main_cum_krw": -1959,
      "twin_cum_krw": -1750,
      "total_cum_krw": -3709
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 102238,
      "balance_krw": 5391,
      "balance_usdt": 35.73,
      "cum_pnl_krw": -1959,
      "cum_pnl_pct": -0.7893,
      "cum_pnl_since": "2026-07-25",
      "twr_pct": -0.7893,
      "twr_events": 12,
      "twr_since": "2026-07-25",
      "total_pnl_usd_record": 201.07,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": 0,
      "daily_pnl_pct": 0.0,
      "daily_target_met": false,
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
      "asset_krw": 341021,
      "xrp_bithumb": 21.309,
      "xrp_okx": 165.6616,
      "xrp_target": 93.4853,
      "hedge_upnl_usd": 0.9912,
      "cum_pnl_krw": -1750,
      "cum_pnl_pct": -1.0081,
      "cum_pnl_since": "2026-07-25",
      "twr_pct": -1.0081,
      "twr_events": 218,
      "twr_since": "2026-07-25",
      "session_pnl_usd_record": 3.9589,
      "today_pnl_usd_record": 0.3294,
      "daily_pnl_krw": 172,
      "daily_pnl_pct": 0.064,
      "daily_target_met": false,
      "today_trades": 12,
      "recent_trades": [
        {
          "time": "2026-08-05T17:11:18.051061",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.493,
          "pnl_usd": 0.0246,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.0246
        },
        {
          "time": "2026-08-05T16:32:27.115023",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.504,
          "pnl_usd": 0.0253,
          "allocated_cost_usd": 0.00019,
          "net_pnl_usd": 0.02511
        },
        {
          "time": "2026-08-05T15:53:52.243628",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.54,
          "pnl_usd": 0.0278,
          "allocated_cost_usd": 0.00038,
          "net_pnl_usd": 0.02742
        },
        {
          "time": "2026-08-05T15:23:52.053921",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.549,
          "pnl_usd": 0.0285,
          "allocated_cost_usd": 0.00171,
          "net_pnl_usd": 0.02679
        },
        {
          "time": "2026-08-05T10:56:55.213326",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.669,
          "pnl_usd": 0.0368,
          "allocated_cost_usd": 0.00311,
          "net_pnl_usd": 0.03369
        },
        {
          "time": "2026-08-05T09:01:09.631682",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.521,
          "pnl_usd": 0.0265,
          "allocated_cost_usd": 0.00458,
          "net_pnl_usd": 0.02192
        },
        {
          "time": "2026-08-05T06:57:54.557656",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.595,
          "pnl_usd": 0.0217,
          "allocated_cost_usd": 0.00458,
          "net_pnl_usd": 0.01712
        },
        {
          "time": "2026-08-05T06:57:20.398063",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.576,
          "pnl_usd": 0.0303,
          "allocated_cost_usd": 0.00458,
          "net_pnl_usd": 0.02572
        },
        {
          "time": "2026-08-05T06:46:04.575782",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.529,
          "pnl_usd": 0.0271,
          "allocated_cost_usd": 0.00519,
          "net_pnl_usd": 0.02191
        },
        {
          "time": "2026-08-05T02:47:01.864096",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.548,
          "pnl_usd": 0.0202,
          "allocated_cost_usd": 0.00766,
          "net_pnl_usd": 0.01254
        }
      ]
    }
  }
};