const pnlData = {
  "updated_at": "2026-07-26 20:31:04",
  "usd_krw": 1462.79,
  "total_asset_krw": 444105,
  "daily_pnl_krw": -2863,
  "daily_yield_pct": -0.641,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 454267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -10162,
    "seed_yield_pct": -2.237,
    "days_since_seed": 7,
    "avg_daily_yield_pct": -0.32
  },
  "asset_trend": [
    {
      "date": "2026-07-25",
      "total_krw": 446968
    },
    {
      "date": "2026-07-26",
      "total_krw": 444105
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
      "total_asset_krw": 444105,
      "main_pnl_krw": -1735,
      "twin_pnl_krw": -1128,
      "total_pnl_krw": -2863,
      "main_pnl_pct": -0.681,
      "twin_pnl_pct": -0.587,
      "total_pnl_pct": -0.641,
      "target_met": false
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 253028,
      "balance_krw": 1162,
      "balance_usdt": 172.18,
      "cum_pnl_krw": -1735,
      "cum_pnl_pct": -0.681,
      "cum_pnl_since": "2026-07-25",
      "total_pnl_usd_record": 199.7,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": -1735,
      "daily_pnl_pct": -0.681,
      "daily_target_met": false,
      "today_trades": 0,
      "pending_transfers": 0,
      "restart_count": 6,
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
      "asset_krw": 191078,
      "xrp_bithumb": 74.9893,
      "xrp_okx": 11.7379,
      "xrp_target": 43.8692,
      "hedge_upnl_usd": 3.2558,
      "cum_pnl_krw": -1128,
      "cum_pnl_pct": -0.587,
      "cum_pnl_since": "2026-07-25",
      "session_pnl_usd_record": 0.4956,
      "today_pnl_usd_record": 0.0947,
      "daily_pnl_krw": -1128,
      "daily_pnl_pct": -0.587,
      "daily_target_met": false,
      "today_trades": 18,
      "recent_trades": [
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
        },
        {
          "time": "2026-07-26T17:57:54.508081",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.226,
          "pnl_usd": 0.006
        },
        {
          "time": "2026-07-26T17:55:43.587335",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.199,
          "pnl_usd": 0.0041
        },
        {
          "time": "2026-07-26T17:54:05.327577",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.199,
          "pnl_usd": 0.0041
        },
        {
          "time": "2026-07-26T17:53:31.166539",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.199,
          "pnl_usd": 0.0041
        },
        {
          "time": "2026-07-26T17:51:21.018128",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.216,
          "pnl_usd": 0.0053
        },
        {
          "time": "2026-07-26T17:50:14.637333",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.207,
          "pnl_usd": 0.0047
        },
        {
          "time": "2026-07-26T17:49:40.660687",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.225,
          "pnl_usd": 0.0059
        }
      ]
    }
  }
};