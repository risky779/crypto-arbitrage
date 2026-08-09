const pnlData = {
  "updated_at": "2026-08-09 20:31:04",
  "usd_krw": 1412.2,
  "total_asset_krw": 429315,
  "daily_pnl_krw": -417,
  "daily_yield_pct": -0.097,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 474267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -44952,
    "seed_yield_pct": -9.478,
    "days_since_seed": 21,
    "avg_daily_yield_pct": -0.451
  },
  "reconciliation": {
    "since": "2026-07-25",
    "combined_realized_usd": -6.97,
    "combined_actual_delta_usd": -0.69,
    "drift_usd": 6.28,
    "drift_pct": 2.066,
    "status": "OK",
    "note": "drift = 실제총자산 증감(마크투마켓 포함) - 원장상 실현손익합계. 헷지 정상이면 작아야 함."
  },
  "unallocated": {
    "krw": -7814,
    "pct": -1.82,
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
      "total_krw": 434954
    },
    {
      "date": "2026-08-06",
      "total_krw": 432261
    },
    {
      "date": "2026-08-07",
      "total_krw": 431930
    },
    {
      "date": "2026-08-08",
      "total_krw": 429044
    },
    {
      "date": "2026-08-09",
      "total_krw": 429315
    }
  ],
  "daily_history": [
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
      "twin_pnl_krw": -280,
      "total_pnl_krw": -280,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -0.148,
      "total_pnl_pct": -0.063,
      "target_met": false
    },
    {
      "date": "2026-07-29",
      "total_asset_krw": 431012,
      "main_pnl_krw": 0,
      "twin_pnl_krw": -113,
      "total_pnl_krw": -113,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -0.061,
      "total_pnl_pct": -0.026,
      "target_met": false
    },
    {
      "date": "2026-07-30",
      "total_asset_krw": 423306,
      "main_pnl_krw": -1933,
      "twin_pnl_krw": -756,
      "total_pnl_krw": -2689,
      "main_pnl_pct": -0.761,
      "twin_pnl_pct": -0.427,
      "total_pnl_pct": -0.624,
      "target_met": false
    },
    {
      "date": "2026-07-31",
      "total_asset_krw": 343335,
      "main_pnl_krw": 0,
      "twin_pnl_krw": 375,
      "total_pnl_krw": 375,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": 0.221,
      "total_pnl_pct": 0.089,
      "target_met": false
    },
    {
      "date": "2026-08-01",
      "total_asset_krw": 421341,
      "main_pnl_krw": 0,
      "twin_pnl_krw": 133,
      "total_pnl_krw": 133,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": 0.148,
      "total_pnl_pct": 0.039,
      "target_met": false
    },
    {
      "date": "2026-08-02",
      "total_asset_krw": 419351,
      "main_pnl_krw": 0,
      "twin_pnl_krw": 180,
      "total_pnl_krw": 180,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": 0.092,
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
      "twin_pnl_krw": 161,
      "total_pnl_krw": 161,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": 0.06,
      "total_pnl_pct": 0.036,
      "target_met": false
    },
    {
      "date": "2026-08-05",
      "total_asset_krw": 434954,
      "main_pnl_krw": 0,
      "twin_pnl_krw": -659,
      "total_pnl_krw": -659,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -0.245,
      "total_pnl_pct": -0.149,
      "target_met": false
    },
    {
      "date": "2026-08-06",
      "total_asset_krw": 432261,
      "main_pnl_krw": 0,
      "twin_pnl_krw": -1519,
      "total_pnl_krw": -1519,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -0.447,
      "total_pnl_pct": -0.343,
      "target_met": false
    },
    {
      "date": "2026-08-07",
      "total_asset_krw": 431930,
      "main_pnl_krw": 0,
      "twin_pnl_krw": -2,
      "total_pnl_krw": -2,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -0.001,
      "total_pnl_pct": -0.0,
      "target_met": false
    },
    {
      "date": "2026-08-08",
      "total_asset_krw": 429044,
      "main_pnl_krw": 0,
      "twin_pnl_krw": -3407,
      "total_pnl_krw": -3407,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -1.008,
      "total_pnl_pct": -0.773,
      "target_met": false
    },
    {
      "date": "2026-08-09",
      "total_asset_krw": 429315,
      "main_pnl_krw": 0,
      "twin_pnl_krw": -416,
      "total_pnl_krw": -416,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -0.125,
      "total_pnl_pct": -0.095,
      "target_met": false
    }
  ],
  "realized_pnl_history": [
    {
      "date": "2026-07-25",
      "main_cum_krw": 0,
      "twin_cum_krw": 78,
      "total_cum_krw": 78
    },
    {
      "date": "2026-07-26",
      "main_cum_krw": -3,
      "twin_cum_krw": -1600,
      "total_cum_krw": -1603
    },
    {
      "date": "2026-07-27",
      "main_cum_krw": -3,
      "twin_cum_krw": -1600,
      "total_cum_krw": -1603
    },
    {
      "date": "2026-07-28",
      "main_cum_krw": -3,
      "twin_cum_krw": -1880,
      "total_cum_krw": -1883
    },
    {
      "date": "2026-07-29",
      "main_cum_krw": -3,
      "twin_cum_krw": -1993,
      "total_cum_krw": -1996
    },
    {
      "date": "2026-07-30",
      "main_cum_krw": -1936,
      "twin_cum_krw": -2749,
      "total_cum_krw": -4685
    },
    {
      "date": "2026-07-31",
      "main_cum_krw": -1936,
      "twin_cum_krw": -2374,
      "total_cum_krw": -4310
    },
    {
      "date": "2026-08-01",
      "main_cum_krw": -1936,
      "twin_cum_krw": -2241,
      "total_cum_krw": -4177
    },
    {
      "date": "2026-08-02",
      "main_cum_krw": -1936,
      "twin_cum_krw": -2061,
      "total_cum_krw": -3997
    },
    {
      "date": "2026-08-03",
      "main_cum_krw": -1936,
      "twin_cum_krw": -2061,
      "total_cum_krw": -3997
    },
    {
      "date": "2026-08-04",
      "main_cum_krw": -1936,
      "twin_cum_krw": -1900,
      "total_cum_krw": -3836
    },
    {
      "date": "2026-08-05",
      "main_cum_krw": -1936,
      "twin_cum_krw": -2559,
      "total_cum_krw": -4495
    },
    {
      "date": "2026-08-06",
      "main_cum_krw": -1936,
      "twin_cum_krw": -4078,
      "total_cum_krw": -6014
    },
    {
      "date": "2026-08-07",
      "main_cum_krw": -1936,
      "twin_cum_krw": -4080,
      "total_cum_krw": -6016
    },
    {
      "date": "2026-08-08",
      "main_cum_krw": -1936,
      "twin_cum_krw": -7487,
      "total_cum_krw": -9423
    },
    {
      "date": "2026-08-09",
      "main_cum_krw": -1936,
      "twin_cum_krw": -7903,
      "total_cum_krw": -9839
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 104020,
      "balance_krw": 2677,
      "balance_usdt": 252.44,
      "cum_pnl_krw": -1936,
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
      "running": false,
      "asset_krw": 333109,
      "xrp_bithumb": 0.0,
      "xrp_okx": 0.0,
      "xrp_target": 0.0,
      "hedge_upnl_usd": 0.9884,
      "cum_pnl_krw": -7903,
      "cum_pnl_pct": -2.8482,
      "cum_pnl_since": "2026-07-25",
      "twr_pct": -2.8482,
      "twr_events": 355,
      "twr_since": "2026-07-25",
      "session_pnl_usd_record": 6.3358,
      "today_pnl_usd_record": 0.2458,
      "daily_pnl_krw": -417,
      "daily_pnl_pct": -0.125,
      "daily_target_met": false,
      "today_trades": 3,
      "recent_trades": [
        {
          "time": "2026-08-09T18:40:27.206149",
          "coin": "ZRO",
          "sell_side": "OKX",
          "gap_pct": 2.017,
          "pnl_usd": 0.1109,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.1109
        },
        {
          "time": "2026-08-09T14:43:41.727055",
          "coin": "ZRO",
          "sell_side": "OKX",
          "gap_pct": 1.553,
          "pnl_usd": 0.0795,
          "allocated_cost_usd": 0.00575,
          "net_pnl_usd": 0.07375
        },
        {
          "time": "2026-08-09T10:02:48.742977",
          "coin": "ZRO",
          "sell_side": "OKX",
          "gap_pct": 1.201,
          "pnl_usd": 0.0554,
          "allocated_cost_usd": 0.0099,
          "net_pnl_usd": 0.0455
        },
        {
          "time": "2026-08-08T23:35:02.399310",
          "coin": "ZRO",
          "sell_side": "OKX",
          "gap_pct": 1.071,
          "pnl_usd": 0.0332,
          "allocated_cost_usd": 0.01763,
          "net_pnl_usd": 0.01557
        },
        {
          "time": "2026-08-08T23:33:21.960954",
          "coin": "RE",
          "sell_side": "OKX",
          "gap_pct": 1.125,
          "pnl_usd": 0.0358,
          "allocated_cost_usd": 0.01975,
          "net_pnl_usd": 0.01605
        },
        {
          "time": "2026-08-08T23:23:12.301068",
          "coin": "RE",
          "sell_side": "OKX",
          "gap_pct": 1.342,
          "pnl_usd": 0.0465,
          "allocated_cost_usd": 0.0216,
          "net_pnl_usd": 0.0249
        },
        {
          "time": "2026-08-08T23:04:58.242914",
          "coin": "ZRO",
          "sell_side": "OKX",
          "gap_pct": 1.317,
          "pnl_usd": 0.0452,
          "allocated_cost_usd": 0.03305,
          "net_pnl_usd": 0.01215
        },
        {
          "time": "2026-08-08T23:04:54.425970",
          "coin": "ZRO",
          "sell_side": "OKX",
          "gap_pct": 1.317,
          "pnl_usd": 0.0452,
          "allocated_cost_usd": 0.03305,
          "net_pnl_usd": 0.01215
        },
        {
          "time": "2026-08-08T23:04:52.035142",
          "coin": "ZRO",
          "sell_side": "OKX",
          "gap_pct": 1.317,
          "pnl_usd": 0.0452,
          "allocated_cost_usd": 0.03305,
          "net_pnl_usd": 0.01215
        },
        {
          "time": "2026-08-08T22:59:11.642965",
          "coin": "RE",
          "sell_side": "OKX",
          "gap_pct": 1.356,
          "pnl_usd": 0.0471,
          "allocated_cost_usd": 0.05961,
          "net_pnl_usd": -0.01251
        }
      ]
    }
  }
};