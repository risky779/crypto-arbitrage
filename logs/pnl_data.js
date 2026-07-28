const pnlData = {
  "updated_at": "2026-07-28 18:16:03",
  "usd_krw": 1467.33,
  "total_asset_krw": 441835,
  "daily_pnl_krw": -1682,
  "daily_yield_pct": -0.379,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 454267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -12432,
    "seed_yield_pct": -2.737,
    "days_since_seed": 9,
    "avg_daily_yield_pct": -0.304
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
      "total_krw": 441835
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
      "total_asset_krw": 441835,
      "main_pnl_krw": 7493,
      "twin_pnl_krw": -9174,
      "total_pnl_krw": -1682,
      "main_pnl_pct": 2.95,
      "twin_pnl_pct": -4.84,
      "total_pnl_pct": -0.379,
      "target_met": false
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 270647,
      "balance_krw": 27687,
      "balance_usdt": 166.85,
      "cum_pnl_krw": 0,
      "cum_pnl_pct": 0.0,
      "cum_pnl_since": "2026-07-28",
      "total_pnl_usd_record": 199.7,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": 7493,
      "daily_pnl_pct": 2.95,
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
      "asset_krw": 171188,
      "xrp_bithumb": 74.6792,
      "xrp_okx": 5.2246,
      "xrp_target": 39.7094,
      "hedge_upnl_usd": 2.8457,
      "cum_pnl_krw": 0,
      "cum_pnl_pct": 0.0,
      "cum_pnl_since": "2026-07-28",
      "session_pnl_usd_record": 1.2684,
      "today_pnl_usd_record": 0.7369,
      "daily_pnl_krw": -9174,
      "daily_pnl_pct": -4.84,
      "daily_target_met": false,
      "today_trades": 35,
      "recent_trades": [
        {
          "time": "2026-07-28T18:06:48.329236",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.795,
          "pnl_usd": 0.0455
        },
        {
          "time": "2026-07-28T18:06:12.072075",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.822,
          "pnl_usd": 0.0473
        },
        {
          "time": "2026-07-28T16:38:57.578551",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.833,
          "pnl_usd": 0.0481
        },
        {
          "time": "2026-07-28T16:38:23.093770",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.758,
          "pnl_usd": 0.0429
        },
        {
          "time": "2026-07-28T16:37:48.614620",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.748,
          "pnl_usd": 0.0422
        },
        {
          "time": "2026-07-28T16:37:14.178721",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.805,
          "pnl_usd": 0.0462
        },
        {
          "time": "2026-07-28T16:36:39.195840",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.759,
          "pnl_usd": 0.043
        },
        {
          "time": "2026-07-28T16:35:56.300624",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.807,
          "pnl_usd": 0.0463
        },
        {
          "time": "2026-07-28T16:35:21.699253",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.816,
          "pnl_usd": 0.0469
        },
        {
          "time": "2026-07-28T10:03:52.730785",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.513,
          "pnl_usd": 0.026
        }
      ]
    }
  }
};