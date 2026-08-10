const pnlData = {
  "updated_at": "2026-08-10 13:01:08",
  "usd_krw": 1409.64,
  "total_asset_krw": 356542,
  "daily_pnl_krw": 41,
  "daily_yield_pct": 0.012,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 474267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -117725,
    "seed_yield_pct": -24.823,
    "days_since_seed": 22,
    "avg_daily_yield_pct": -1.128
  },
  "reconciliation": {
    "since": "2026-07-25",
    "combined_realized_usd": -7.07,
    "combined_actual_delta_usd": -51.76,
    "drift_usd": -44.69,
    "drift_pct": -17.668,
    "status": "WARNING",
    "note": "drift = 실제총자산 증감(마크투마켓 포함) - 원장상 실현손익합계. 헷지 정상이면 작아야 함."
  },
  "unallocated": {
    "krw": -80458,
    "pct": -22.57,
    "status": "WARNING",
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
      "total_krw": 429770
    },
    {
      "date": "2026-08-10",
      "total_krw": 356542
    }
  ],
  "daily_history": [
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
      "twin_pnl_krw": -112,
      "total_pnl_krw": -112,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -0.061,
      "total_pnl_pct": -0.026,
      "target_met": false
    },
    {
      "date": "2026-07-30",
      "total_asset_krw": 423306,
      "main_pnl_krw": -1929,
      "twin_pnl_krw": -755,
      "total_pnl_krw": -2684,
      "main_pnl_pct": -0.76,
      "twin_pnl_pct": -0.426,
      "total_pnl_pct": -0.623,
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
      "twin_pnl_krw": 132,
      "total_pnl_krw": 132,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": 0.147,
      "total_pnl_pct": 0.038,
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
      "twin_pnl_krw": -658,
      "total_pnl_krw": -658,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -0.244,
      "total_pnl_pct": -0.149,
      "target_met": false
    },
    {
      "date": "2026-08-06",
      "total_asset_krw": 432261,
      "main_pnl_krw": 0,
      "twin_pnl_krw": -1516,
      "total_pnl_krw": -1516,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -0.446,
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
      "twin_pnl_krw": -3401,
      "total_pnl_krw": -3401,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -1.006,
      "total_pnl_pct": -0.771,
      "target_met": false
    },
    {
      "date": "2026-08-09",
      "total_asset_krw": 429770,
      "main_pnl_krw": 0,
      "twin_pnl_krw": -604,
      "total_pnl_krw": -604,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -0.181,
      "total_pnl_pct": -0.138,
      "target_met": false
    },
    {
      "date": "2026-08-10",
      "total_asset_krw": 356542,
      "main_pnl_krw": 0,
      "twin_pnl_krw": 41,
      "total_pnl_krw": 41,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": 0.012,
      "total_pnl_pct": 0.009,
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
      "twin_cum_krw": -1597,
      "total_cum_krw": -1600
    },
    {
      "date": "2026-07-27",
      "main_cum_krw": -3,
      "twin_cum_krw": -1597,
      "total_cum_krw": -1600
    },
    {
      "date": "2026-07-28",
      "main_cum_krw": -3,
      "twin_cum_krw": -1877,
      "total_cum_krw": -1880
    },
    {
      "date": "2026-07-29",
      "main_cum_krw": -3,
      "twin_cum_krw": -1989,
      "total_cum_krw": -1992
    },
    {
      "date": "2026-07-30",
      "main_cum_krw": -1932,
      "twin_cum_krw": -2744,
      "total_cum_krw": -4676
    },
    {
      "date": "2026-07-31",
      "main_cum_krw": -1932,
      "twin_cum_krw": -2369,
      "total_cum_krw": -4301
    },
    {
      "date": "2026-08-01",
      "main_cum_krw": -1932,
      "twin_cum_krw": -2237,
      "total_cum_krw": -4169
    },
    {
      "date": "2026-08-02",
      "main_cum_krw": -1932,
      "twin_cum_krw": -2057,
      "total_cum_krw": -3989
    },
    {
      "date": "2026-08-03",
      "main_cum_krw": -1932,
      "twin_cum_krw": -2057,
      "total_cum_krw": -3989
    },
    {
      "date": "2026-08-04",
      "main_cum_krw": -1932,
      "twin_cum_krw": -1896,
      "total_cum_krw": -3828
    },
    {
      "date": "2026-08-05",
      "main_cum_krw": -1932,
      "twin_cum_krw": -2554,
      "total_cum_krw": -4486
    },
    {
      "date": "2026-08-06",
      "main_cum_krw": -1932,
      "twin_cum_krw": -4070,
      "total_cum_krw": -6002
    },
    {
      "date": "2026-08-07",
      "main_cum_krw": -1932,
      "twin_cum_krw": -4072,
      "total_cum_krw": -6004
    },
    {
      "date": "2026-08-08",
      "main_cum_krw": -1932,
      "twin_cum_krw": -7473,
      "total_cum_krw": -9405
    },
    {
      "date": "2026-08-09",
      "main_cum_krw": -1932,
      "twin_cum_krw": -8077,
      "total_cum_krw": -10009
    },
    {
      "date": "2026-08-10",
      "main_cum_krw": -1932,
      "twin_cum_krw": -8036,
      "total_cum_krw": -9968
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 104293,
      "balance_krw": 703,
      "balance_usdt": 106.4,
      "cum_pnl_krw": -1932,
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
      "asset_krw": 332707,
      "xrp_bithumb": 0.0,
      "xrp_okx": 0.0,
      "xrp_target": 0.0,
      "hedge_upnl_usd": -0.0416,
      "cum_pnl_krw": -8036,
      "cum_pnl_pct": -2.8922,
      "cum_pnl_since": "2026-07-25",
      "twr_pct": -2.8922,
      "twr_events": 380,
      "twr_since": "2026-07-25",
      "session_pnl_usd_record": 7.0546,
      "today_pnl_usd_record": 0.6212,
      "daily_pnl_krw": 41,
      "daily_pnl_pct": 0.012,
      "daily_target_met": false,
      "today_trades": 10,
      "recent_trades": [
        {
          "time": "2026-08-10T11:14:09.464250",
          "coin": "ZRO",
          "sell_side": "OKX",
          "gap_pct": 1.239,
          "pnl_usd": 0.058,
          "allocated_cost_usd": 0.00016,
          "net_pnl_usd": 0.05784
        },
        {
          "time": "2026-08-10T11:14:06.823277",
          "coin": "ZRO",
          "sell_side": "OKX",
          "gap_pct": 1.239,
          "pnl_usd": 0.058,
          "allocated_cost_usd": 0.00016,
          "net_pnl_usd": 0.05784
        },
        {
          "time": "2026-08-10T11:13:18.298147",
          "coin": "RE",
          "sell_side": "OKX",
          "gap_pct": 1.24,
          "pnl_usd": 0.0557,
          "allocated_cost_usd": 0.00016,
          "net_pnl_usd": 0.05554
        },
        {
          "time": "2026-08-10T11:04:17.594061",
          "coin": "ZRO",
          "sell_side": "OKX",
          "gap_pct": 1.4,
          "pnl_usd": 0.069,
          "allocated_cost_usd": 0.02089,
          "net_pnl_usd": 0.04811
        },
        {
          "time": "2026-08-10T10:56:38.915994",
          "coin": "RE",
          "sell_side": "OKX",
          "gap_pct": 1.443,
          "pnl_usd": 0.0694,
          "allocated_cost_usd": 0.02874,
          "net_pnl_usd": 0.04066
        },
        {
          "time": "2026-08-10T10:43:19.452265",
          "coin": "RE",
          "sell_side": "OKX",
          "gap_pct": 1.309,
          "pnl_usd": 0.06,
          "allocated_cost_usd": 0.03713,
          "net_pnl_usd": 0.02287
        },
        {
          "time": "2026-08-10T10:39:30.613978",
          "coin": "ZRO",
          "sell_side": "OKX",
          "gap_pct": 1.279,
          "pnl_usd": 0.0608,
          "allocated_cost_usd": 0.03713,
          "net_pnl_usd": 0.02367
        },
        {
          "time": "2026-08-10T10:27:13.956439",
          "coin": "ZRO",
          "sell_side": "OKX",
          "gap_pct": 1.276,
          "pnl_usd": 0.0605,
          "allocated_cost_usd": 0.06012,
          "net_pnl_usd": 0.00038
        },
        {
          "time": "2026-08-10T10:26:34.600491",
          "coin": "RE",
          "sell_side": "OKX",
          "gap_pct": 1.298,
          "pnl_usd": 0.0599,
          "allocated_cost_usd": 0.06012,
          "net_pnl_usd": -0.00022
        },
        {
          "time": "2026-08-10T09:00:15.072850",
          "coin": "ZRO",
          "sell_side": "OKX",
          "gap_pct": 1.413,
          "pnl_usd": 0.0699,
          "allocated_cost_usd": 0.07428,
          "net_pnl_usd": -0.00438
        }
      ]
    }
  }
};