const pnlData = {
  "updated_at": "2026-07-29 00:46:03",
  "usd_krw": 1467.33,
  "total_asset_krw": 438209,
  "daily_pnl_krw": -846,
  "daily_yield_pct": -0.193,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 454267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -16058,
    "seed_yield_pct": -3.535,
    "days_since_seed": 10,
    "avg_daily_yield_pct": -0.353
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
      "total_krw": 438209
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
      "main_pnl_krw": 24567,
      "twin_pnl_krw": -29028,
      "total_pnl_krw": -4461,
      "main_pnl_pct": 9.674,
      "twin_pnl_pct": -15.312,
      "total_pnl_pct": -1.006,
      "target_met": false
    },
    {
      "date": "2026-07-29",
      "total_asset_krw": 438209,
      "main_pnl_krw": -1134,
      "twin_pnl_krw": 288,
      "total_pnl_krw": -846,
      "main_pnl_pct": -0.334,
      "twin_pnl_pct": 0.289,
      "total_pnl_pct": -0.193,
      "target_met": false
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 338440,
      "balance_krw": 8127,
      "balance_usdt": 226.7,
      "cum_pnl_krw": -1134,
      "cum_pnl_pct": -0.334,
      "cum_pnl_since": "2026-07-28",
      "total_pnl_usd_record": 199.7,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": -1134,
      "daily_pnl_pct": -0.334,
      "daily_target_met": false,
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
      "asset_krw": 99769,
      "xrp_bithumb": 29.5386,
      "xrp_okx": 16.316,
      "xrp_target": 22.9297,
      "hedge_upnl_usd": 1.2085,
      "cum_pnl_krw": 288,
      "cum_pnl_pct": 0.289,
      "cum_pnl_since": "2026-07-28",
      "session_pnl_usd_record": 1.5848,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": 288,
      "daily_pnl_pct": 0.289,
      "daily_target_met": false,
      "today_trades": 0,
      "recent_trades": [
        {
          "time": "2026-07-28T23:33:38.907673",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.891,
          "pnl_usd": 0.0521
        },
        {
          "time": "2026-07-28T22:54:17.325136",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.844,
          "pnl_usd": 0.0448
        },
        {
          "time": "2026-07-28T22:53:43.052004",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.75,
          "pnl_usd": 0.0424
        },
        {
          "time": "2026-07-28T22:53:08.385250",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.742,
          "pnl_usd": 0.0418
        },
        {
          "time": "2026-07-28T22:52:33.929432",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.781,
          "pnl_usd": 0.0445
        },
        {
          "time": "2026-07-28T19:34:25.788252",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.814,
          "pnl_usd": 0.0468
        },
        {
          "time": "2026-07-28T19:33:51.281617",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.774,
          "pnl_usd": 0.044
        },
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
        }
      ]
    }
  }
};