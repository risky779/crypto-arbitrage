const pnlData = {
  "updated_at": "2026-08-05 22:16:04",
  "usd_krw": 1428.89,
  "total_asset_krw": 435108,
  "daily_pnl_krw": -666,
  "daily_yield_pct": -0.153,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 474267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -39159,
    "seed_yield_pct": -8.257,
    "days_since_seed": 17,
    "avg_daily_yield_pct": -0.486
  },
  "reconciliation": {
    "since": "2026-07-25",
    "combined_realized_usd": -3.18,
    "combined_actual_delta_usd": -0.18,
    "drift_usd": 3.0,
    "drift_pct": 0.985,
    "status": "OK",
    "note": "drift = 실제총자산 증감(마크투마켓 포함) - 원장상 실현손익합계. 헷지 정상이면 작아야 함."
  },
  "unallocated": {
    "krw": -7312,
    "pct": -1.68,
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
      "total_krw": 435108
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
      "total_asset_krw": 435108,
      "main_pnl_krw": 0,
      "twin_pnl_krw": -667,
      "total_pnl_krw": -667,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -0.248,
      "total_pnl_pct": -0.151,
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
      "twin_cum_krw": -2589,
      "total_cum_krw": -4548
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 102238,
      "balance_krw": 16496,
      "balance_usdt": 214.25,
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
      "asset_krw": 340182,
      "xrp_bithumb": 54.2163,
      "xrp_okx": 1.021,
      "xrp_target": 27.6278,
      "hedge_upnl_usd": 0.2866,
      "cum_pnl_krw": -2589,
      "cum_pnl_pct": -1.2551,
      "cum_pnl_since": "2026-07-25",
      "twr_pct": -1.2551,
      "twr_events": 242,
      "twr_since": "2026-07-25",
      "session_pnl_usd_record": 4.3479,
      "today_pnl_usd_record": 0.7185,
      "daily_pnl_krw": -666,
      "daily_pnl_pct": -0.247,
      "daily_target_met": false,
      "today_trades": 31,
      "recent_trades": [
        {
          "time": "2026-08-05T21:03:45.449671",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.515,
          "pnl_usd": 0.0261,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.0261
        },
        {
          "time": "2026-08-05T21:03:22.854512",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.505,
          "pnl_usd": 0.0254,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.0254
        },
        {
          "time": "2026-08-05T21:02:27.528743",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.534,
          "pnl_usd": 0.0274,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.0274
        },
        {
          "time": "2026-08-05T21:00:21.430104",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.543,
          "pnl_usd": 0.0281,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.0281
        },
        {
          "time": "2026-08-05T20:57:43.782330",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.543,
          "pnl_usd": 0.02,
          "allocated_cost_usd": 0.00261,
          "net_pnl_usd": 0.01739
        },
        {
          "time": "2026-08-05T20:57:00.580352",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.525,
          "pnl_usd": 0.0268,
          "allocated_cost_usd": 0.00261,
          "net_pnl_usd": 0.02419
        },
        {
          "time": "2026-08-05T20:56:01.001648",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.534,
          "pnl_usd": 0.0274,
          "allocated_cost_usd": 0.00261,
          "net_pnl_usd": 0.02479
        },
        {
          "time": "2026-08-05T20:55:44.367544",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.525,
          "pnl_usd": 0.0268,
          "allocated_cost_usd": 0.00261,
          "net_pnl_usd": 0.02419
        },
        {
          "time": "2026-08-05T20:23:53.381990",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.287,
          "pnl_usd": 0.0103,
          "allocated_cost_usd": 0.01328,
          "net_pnl_usd": -0.00298
        },
        {
          "time": "2026-08-05T20:23:37.809357",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.287,
          "pnl_usd": 0.0103,
          "allocated_cost_usd": 0.01328,
          "net_pnl_usd": -0.00298
        }
      ]
    }
  }
};