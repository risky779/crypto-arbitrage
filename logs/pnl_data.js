const pnlData = {
  "updated_at": "2026-07-27 23:46:04",
  "usd_krw": 1459.6,
  "total_asset_krw": 443517,
  "daily_pnl_krw": 525,
  "daily_yield_pct": 0.119,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 454267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -10750,
    "seed_yield_pct": -2.367,
    "days_since_seed": 8,
    "avg_daily_yield_pct": -0.296
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
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 254725,
      "balance_krw": 92108,
      "balance_usdt": 111.41,
      "cum_pnl_krw": -38,
      "cum_pnl_pct": -0.015,
      "cum_pnl_since": "2026-07-25",
      "total_pnl_usd_record": 199.7,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": 1374,
      "daily_pnl_pct": 0.542,
      "daily_target_met": false,
      "today_trades": 0,
      "pending_transfers": 0,
      "restart_count": 2,
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
      "asset_krw": 188792,
      "xrp_bithumb": 81.1739,
      "xrp_okx": 5.1148,
      "xrp_target": 43.8692,
      "hedge_upnl_usd": 4.3536,
      "cum_pnl_krw": -3413,
      "cum_pnl_pct": -1.776,
      "cum_pnl_since": "2026-07-25",
      "session_pnl_usd_record": 0.5313,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": -849,
      "daily_pnl_pct": -0.448,
      "daily_target_met": false,
      "today_trades": 0,
      "recent_trades": [
        {
          "time": "2026-07-26T22:56:36.162975",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.196,
          "pnl_usd": 0.0039
        },
        {
          "time": "2026-07-26T22:53:52.115424",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.205,
          "pnl_usd": 0.0046
        },
        {
          "time": "2026-07-26T22:53:17.929545",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.205,
          "pnl_usd": 0.0046
        },
        {
          "time": "2026-07-26T22:52:43.518580",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.205,
          "pnl_usd": 0.0046
        },
        {
          "time": "2026-07-26T22:50:00.142732",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.242,
          "pnl_usd": 0.0071
        },
        {
          "time": "2026-07-26T22:49:25.578732",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.242,
          "pnl_usd": 0.0071
        },
        {
          "time": "2026-07-26T22:39:42.176396",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.195,
          "pnl_usd": 0.0038
        },
        {
          "time": "2026-07-26T18:00:41.404129",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.217,
          "pnl_usd": 0.0054
        },
        {
          "time": "2026-07-26T18:00:07.141280",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.217,
          "pnl_usd": 0.0054
        },
        {
          "time": "2026-07-26T17:58:28.652041",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.217,
          "pnl_usd": 0.0054
        }
      ]
    }
  }
};