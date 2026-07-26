const pnlData = {
  "updated_at": "2026-07-26 16:01:03",
  "usd_krw": 1462.79,
  "total_asset_krw": 445582,
  "daily_pnl_krw": -1386,
  "daily_yield_pct": -0.31,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 454267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -8685,
    "seed_yield_pct": -1.912,
    "days_since_seed": 7,
    "avg_daily_yield_pct": -0.273
  },
  "asset_trend": [
    {
      "date": "2026-07-25",
      "total_krw": 446968
    },
    {
      "date": "2026-07-26",
      "total_krw": 445582
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
      "total_asset_krw": 445582,
      "main_pnl_krw": -1630,
      "twin_pnl_krw": 243,
      "total_pnl_krw": -1386,
      "main_pnl_pct": -0.64,
      "twin_pnl_pct": 0.127,
      "total_pnl_pct": -0.31,
      "target_met": false
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 253133,
      "balance_krw": 134043,
      "balance_usdt": 81.41,
      "cum_pnl_krw": -1630,
      "cum_pnl_pct": -0.64,
      "cum_pnl_since": "2026-07-25",
      "total_pnl_usd_record": 199.7,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": -1630,
      "daily_pnl_pct": -0.64,
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
      "asset_krw": 192449,
      "xrp_bithumb": 49.6559,
      "xrp_okx": 37.9415,
      "xrp_target": 43.8692,
      "hedge_upnl_usd": 3.2906,
      "cum_pnl_krw": 243,
      "cum_pnl_pct": 0.127,
      "cum_pnl_since": "2026-07-25",
      "session_pnl_usd_record": 0.4301,
      "today_pnl_usd_record": 0.0294,
      "daily_pnl_krw": 243,
      "daily_pnl_pct": 0.127,
      "daily_target_met": false,
      "today_trades": 5,
      "recent_trades": [
        {
          "time": "2026-07-26T16:00:44.642263",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.21,
          "pnl_usd": 0.0049
        },
        {
          "time": "2026-07-26T16:00:10.468755",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.237,
          "pnl_usd": 0.0068
        },
        {
          "time": "2026-07-26T15:58:31.958628",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.2,
          "pnl_usd": 0.0042
        },
        {
          "time": "2026-07-26T11:06:08.486593",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.227,
          "pnl_usd": 0.0061
        },
        {
          "time": "2026-07-26T11:05:34.513069",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.245,
          "pnl_usd": 0.0074
        },
        {
          "time": "2026-07-25T23:04:39.226604",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.198,
          "pnl_usd": 0.0041
        },
        {
          "time": "2026-07-25T23:00:52.191153",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.198,
          "pnl_usd": 0.0041
        },
        {
          "time": "2026-07-25T22:59:12.652165",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.198,
          "pnl_usd": 0.0041
        },
        {
          "time": "2026-07-25T22:19:28.501585",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.198,
          "pnl_usd": 0.0041
        },
        {
          "time": "2026-07-25T22:18:52.611286",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.198,
          "pnl_usd": 0.0041
        }
      ]
    }
  }
};