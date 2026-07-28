const pnlData = {
  "updated_at": "2026-07-28 12:16:04",
  "usd_krw": 1467.33,
  "total_asset_krw": 448454,
  "daily_pnl_krw": 4937,
  "daily_yield_pct": 1.113,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 454267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -5813,
    "seed_yield_pct": -1.28,
    "days_since_seed": 9,
    "avg_daily_yield_pct": -0.142
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
      "total_krw": 448454
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
      "main_pnl_krw": 1374,
      "twin_pnl_krw": -849,
      "total_pnl_krw": 525,
      "main_pnl_pct": 0.542,
      "twin_pnl_pct": -0.448,
      "total_pnl_pct": 0.119,
      "target_met": false
    },
    {
      "date": "2026-07-28",
      "total_asset_krw": 448454,
      "main_pnl_krw": 4134,
      "twin_pnl_krw": 803,
      "total_pnl_krw": 4937,
      "main_pnl_pct": 1.623,
      "twin_pnl_pct": 0.426,
      "total_pnl_pct": 1.113,
      "target_met": true
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 258859,
      "balance_krw": 153448,
      "balance_usdt": 72.7,
      "cum_pnl_krw": 0,
      "cum_pnl_pct": 0.0,
      "cum_pnl_since": "2026-07-28",
      "total_pnl_usd_record": 199.7,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": 4134,
      "daily_pnl_pct": 1.623,
      "daily_target_met": true,
      "today_trades": 0,
      "pending_transfers": 0,
      "restart_count": 1,
      "recent_trades": [
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
        },
        {
          "time": "2026-07-21T12:15:21.061851",
          "coin": "XLM",
          "profit_usd": 0.1017
        },
        {
          "time": "2026-07-21T12:13:57.797230",
          "coin": "SUI",
          "profit_usd": 0.2075
        },
        {
          "time": "2026-07-21T12:13:48.422577",
          "coin": "XLM",
          "profit_usd": 0.1742
        },
        {
          "time": "2026-07-21T12:12:57.415926",
          "coin": "XLM",
          "profit_usd": 0.1662
        },
        {
          "time": "2026-07-21T12:12:55.750222",
          "coin": "SUI",
          "profit_usd": 0.1867
        },
        {
          "time": "2026-07-12T09:20:23.298676",
          "coin": "NEAR",
          "profit_usd": 0.7816
        }
      ]
    },
    "twin_bot": {
      "label": "쌍둥이봇 · 양쪽재고 로컬거래",
      "running": true,
      "asset_krw": 189595,
      "xrp_bithumb": 82.6376,
      "xrp_okx": 3.5134,
      "xrp_target": 42.8543,
      "hedge_upnl_usd": 6.882,
      "cum_pnl_krw": 0,
      "cum_pnl_pct": 0.0,
      "cum_pnl_since": "2026-07-28",
      "session_pnl_usd_record": 0.86,
      "today_pnl_usd_record": 0.3285,
      "daily_pnl_krw": 803,
      "daily_pnl_pct": 0.426,
      "daily_target_met": false,
      "today_trades": 26,
      "recent_trades": [
        {
          "time": "2026-07-28T10:03:52.730785",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.513,
          "pnl_usd": 0.026
        },
        {
          "time": "2026-07-28T10:03:18.275330",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.568,
          "pnl_usd": 0.0298
        },
        {
          "time": "2026-07-28T10:02:43.871252",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.494,
          "pnl_usd": 0.0247
        },
        {
          "time": "2026-07-28T10:02:09.291763",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.465,
          "pnl_usd": 0.0227
        },
        {
          "time": "2026-07-28T10:01:35.071504",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.51,
          "pnl_usd": 0.0258
        },
        {
          "time": "2026-07-28T10:01:00.709504",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.464,
          "pnl_usd": 0.0226
        },
        {
          "time": "2026-07-28T10:00:26.241870",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.473,
          "pnl_usd": 0.0232
        },
        {
          "time": "2026-07-28T09:59:51.958286",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.502,
          "pnl_usd": 0.0252
        },
        {
          "time": "2026-07-28T09:59:17.565201",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.455,
          "pnl_usd": 0.0219
        },
        {
          "time": "2026-07-28T09:58:43.428071",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.457,
          "pnl_usd": 0.0221
        }
      ]
    }
  }
};