const pnlData = {
  "updated_at": "2026-07-25 19:11:04",
  "usd_krw": 1462.59,
  "total_asset_krw": 447642,
  "daily_pnl_krw": null,
  "daily_yield_pct": null,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 454267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -6625,
    "seed_yield_pct": -1.458,
    "days_since_seed": 6,
    "avg_daily_yield_pct": -0.243
  },
  "asset_trend": [
    {
      "date": "2026-07-25",
      "total_krw": 447642
    }
  ],
  "daily_history": [
    {
      "date": "2026-07-25",
      "total_asset_krw": 447642,
      "main_pnl_krw": null,
      "twin_pnl_krw": null,
      "total_pnl_krw": null
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 255566,
      "balance_krw": 78330,
      "balance_usdt": 121.18,
      "cum_pnl_krw": 0,
      "cum_pnl_since": "2026-07-25",
      "total_pnl_usd_record": 199.7,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": null,
      "today_trades": 0,
      "pending_transfers": 0,
      "restart_count": 13,
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
      "asset_krw": 192076,
      "xrp_bithumb": 43.8404,
      "xrp_okx": 43.8305,
      "xrp_target": 43.8692,
      "hedge_upnl_usd": 4.2476,
      "cum_pnl_krw": 0,
      "cum_pnl_since": "2026-07-25",
      "session_pnl_usd_record": 0.3763,
      "today_pnl_usd_record": 0.0308,
      "daily_pnl_krw": null,
      "today_trades": 4,
      "recent_trades": [
        {
          "time": "2026-07-25T18:07:11.277680",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.2,
          "pnl_usd": 0.0042
        },
        {
          "time": "2026-07-25T11:00:51.112797",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.202,
          "pnl_usd": 0.0093
        },
        {
          "time": "2026-07-25T10:53:49.495093",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.193,
          "pnl_usd": 0.008
        },
        {
          "time": "2026-07-25T10:50:02.242822",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.202,
          "pnl_usd": 0.0093
        },
        {
          "time": "2026-07-23T12:34:15.686353",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 1.501,
          "pnl_usd": 0.1329
        },
        {
          "time": "2026-07-23T12:33:42.696969",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 1.579,
          "pnl_usd": 0.2125
        }
      ]
    }
  }
};