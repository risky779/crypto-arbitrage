const pnlData = {
  "updated_at": "2026-08-04 15:46:03",
  "usd_krw": 1429.59,
  "total_asset_krw": 438917,
  "daily_pnl_krw": 127,
  "daily_yield_pct": 0.029,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 474267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -35350,
    "seed_yield_pct": -7.454,
    "days_since_seed": 16,
    "avg_daily_yield_pct": -0.466
  },
  "reconciliation": {
    "since": "2026-07-25",
    "combined_realized_usd": -2.74,
    "combined_actual_delta_usd": 2.33,
    "drift_usd": 5.07,
    "drift_pct": 1.653,
    "status": "OK",
    "note": "drift = 실제총자산 증감(마크투마켓 포함) - 원장상 실현손익합계. 헷지 정상이면 작아야 함."
  },
  "unallocated": {
    "krw": -4131,
    "pct": -0.94,
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
      "total_krw": 438917
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
      "total_asset_krw": 438917,
      "main_pnl_krw": 0,
      "twin_pnl_krw": 126,
      "total_pnl_krw": 126,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": 0.047,
      "total_pnl_pct": 0.028,
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
      "twin_cum_krw": -1960,
      "total_cum_krw": -3920
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 173642,
      "balance_krw": 57174,
      "balance_usdt": 120.71,
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
      "asset_krw": 269406,
      "xrp_bithumb": 97.0937,
      "xrp_okx": 4.9468,
      "xrp_target": 51.0256,
      "hedge_upnl_usd": 0.3261,
      "cum_pnl_krw": -1960,
      "cum_pnl_pct": -1.0836,
      "cum_pnl_since": "2026-07-25",
      "twr_pct": -1.0836,
      "twr_events": 181,
      "twr_since": "2026-07-25",
      "session_pnl_usd_record": 3.3462,
      "today_pnl_usd_record": 0.2252,
      "daily_pnl_krw": 127,
      "daily_pnl_pct": 0.047,
      "daily_target_met": false,
      "today_trades": 7,
      "recent_trades": [
        {
          "time": "2026-08-04T10:12:02.814098",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.578,
          "pnl_usd": 0.0305,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.0305
        },
        {
          "time": "2026-08-04T10:11:28.784298",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.597,
          "pnl_usd": 0.0318,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.0318
        },
        {
          "time": "2026-08-04T10:10:54.477717",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.578,
          "pnl_usd": 0.0305,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.0305
        },
        {
          "time": "2026-08-04T10:10:20.810862",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.55,
          "pnl_usd": 0.0285,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.0285
        },
        {
          "time": "2026-08-04T10:09:46.644670",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.654,
          "pnl_usd": 0.0357,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.0357
        },
        {
          "time": "2026-08-04T10:09:12.846202",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.663,
          "pnl_usd": 0.0364,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.0364
        },
        {
          "time": "2026-08-04T10:08:39.128090",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.597,
          "pnl_usd": 0.0318,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.0318
        },
        {
          "time": "2026-08-02T14:53:00.679415",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.285,
          "pnl_usd": 0.0101,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.0101
        },
        {
          "time": "2026-08-02T14:48:10.973376",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.303,
          "pnl_usd": 0.0114,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.0114
        },
        {
          "time": "2026-08-02T14:43:53.986688",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.312,
          "pnl_usd": 0.012,
          "allocated_cost_usd": 0.0,
          "net_pnl_usd": 0.012
        }
      ]
    }
  }
};