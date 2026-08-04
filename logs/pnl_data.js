const pnlData = {
  "updated_at": "2026-08-05 01:46:03",
  "usd_krw": 1429.59,
  "total_asset_krw": 437721,
  "daily_pnl_krw": 0,
  "daily_yield_pct": 0.0,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 474267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -36546,
    "seed_yield_pct": -7.706,
    "days_since_seed": 17,
    "avg_daily_yield_pct": -0.453
  },
  "reconciliation": {
    "since": "2026-07-25",
    "combined_realized_usd": -2.72,
    "combined_actual_delta_usd": 1.5,
    "drift_usd": 4.21,
    "drift_pct": 1.376,
    "status": "OK",
    "note": "drift = 실제총자산 증감(마크투마켓 포함) - 원장상 실현손익합계. 헷지 정상이면 작아야 함."
  },
  "unallocated": {
    "krw": -5364,
    "pct": -1.23,
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
      "total_krw": 437721
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
      "twin_pnl_krw": -1699,
      "total_pnl_krw": -1702,
      "main_pnl_pct": -0.001,
      "twin_pnl_pct": -0.884,
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
      "main_pnl_krw": -1957,
      "twin_pnl_krw": -765,
      "total_pnl_krw": -2722,
      "main_pnl_pct": -0.771,
      "twin_pnl_pct": -0.432,
      "total_pnl_pct": -0.632,
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
      "total_asset_krw": 437721,
      "main_pnl_krw": 0,
      "twin_pnl_krw": 0,
      "total_pnl_krw": 0,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": 0.0,
      "total_pnl_pct": 0.0,
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
      "twin_cum_krw": -1620,
      "total_cum_krw": -1623
    },
    {
      "date": "2026-07-27",
      "main_cum_krw": -3,
      "twin_cum_krw": -1620,
      "total_cum_krw": -1623
    },
    {
      "date": "2026-07-28",
      "main_cum_krw": -3,
      "twin_cum_krw": -1904,
      "total_cum_krw": -1907
    },
    {
      "date": "2026-07-29",
      "main_cum_krw": -3,
      "twin_cum_krw": -2018,
      "total_cum_krw": -2021
    },
    {
      "date": "2026-07-30",
      "main_cum_krw": -1960,
      "twin_cum_krw": -2783,
      "total_cum_krw": -4743
    },
    {
      "date": "2026-07-31",
      "main_cum_krw": -1960,
      "twin_cum_krw": -2403,
      "total_cum_krw": -4363
    },
    {
      "date": "2026-08-01",
      "main_cum_krw": -1960,
      "twin_cum_krw": -2269,
      "total_cum_krw": -4229
    },
    {
      "date": "2026-08-02",
      "main_cum_krw": -1960,
      "twin_cum_krw": -2086,
      "total_cum_krw": -4046
    },
    {
      "date": "2026-08-03",
      "main_cum_krw": -1960,
      "twin_cum_krw": -2086,
      "total_cum_krw": -4046
    },
    {
      "date": "2026-08-04",
      "main_cum_krw": -1960,
      "twin_cum_krw": -1923,
      "total_cum_krw": -3883
    },
    {
      "date": "2026-08-05",
      "main_cum_krw": -1960,
      "twin_cum_krw": -1923,
      "total_cum_krw": -3883
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 173642,
      "balance_krw": 37730,
      "balance_usdt": 228.48,
      "cum_pnl_krw": -1960,
      "cum_pnl_pct": -0.7893,
      "cum_pnl_since": "2026-07-25",
      "twr_pct": -0.7893,
      "twr_events": 11,
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
      "asset_krw": 269443,
      "xrp_bithumb": 34.2955,
      "xrp_okx": 1.3984,
      "xrp_target": 17.8515,
      "hedge_upnl_usd": 0.0575,
      "cum_pnl_krw": -1923,
      "cum_pnl_pct": -1.07,
      "cum_pnl_since": "2026-07-25",
      "twr_pct": -1.07,
      "twr_events": 197,
      "twr_since": "2026-07-25",
      "session_pnl_usd_record": 3.6294,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": 0,
      "daily_pnl_pct": 0.0,
      "daily_target_met": false,
      "today_trades": 0,
      "recent_trades": [
        {
          "time": "2026-08-04T22:58:48.272995",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.455,
          "pnl_usd": 0.022,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.022
        },
        {
          "time": "2026-08-04T22:58:14.332812",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.493,
          "pnl_usd": 0.0246,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.0246
        },
        {
          "time": "2026-08-04T22:46:55.812682",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.539,
          "pnl_usd": 0.0278,
          "allocated_cost_usd": 0.00082,
          "net_pnl_usd": 0.02698
        },
        {
          "time": "2026-08-04T22:46:21.641095",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.548,
          "pnl_usd": 0.0284,
          "allocated_cost_usd": 0.00082,
          "net_pnl_usd": 0.02758
        },
        {
          "time": "2026-08-04T22:45:47.627573",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.557,
          "pnl_usd": 0.029,
          "allocated_cost_usd": 0.00082,
          "net_pnl_usd": 0.02818
        },
        {
          "time": "2026-08-04T16:43:57.852658",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.379,
          "pnl_usd": 0.0167,
          "allocated_cost_usd": 0.00727,
          "net_pnl_usd": 0.00943
        },
        {
          "time": "2026-08-04T16:43:23.815557",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.445,
          "pnl_usd": 0.0212,
          "allocated_cost_usd": 0.00727,
          "net_pnl_usd": 0.01393
        },
        {
          "time": "2026-08-04T16:32:04.026656",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.473,
          "pnl_usd": 0.0232,
          "allocated_cost_usd": 0.00844,
          "net_pnl_usd": 0.01476
        },
        {
          "time": "2026-08-04T16:31:29.895690",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.417,
          "pnl_usd": 0.0193,
          "allocated_cost_usd": 0.00844,
          "net_pnl_usd": 0.01086
        },
        {
          "time": "2026-08-04T16:30:55.749863",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.501,
          "pnl_usd": 0.0252,
          "allocated_cost_usd": 0.00844,
          "net_pnl_usd": 0.01676
        }
      ]
    }
  }
};