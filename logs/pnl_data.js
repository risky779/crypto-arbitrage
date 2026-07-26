const pnlData = {
  "updated_at": "2026-07-26 15:46:03",
  "usd_krw": 1462.79,
  "total_asset_krw": 445758,
  "daily_pnl_krw": -1211,
  "daily_yield_pct": -0.271,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 454267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -8509,
    "seed_yield_pct": -1.873,
    "days_since_seed": 7,
    "avg_daily_yield_pct": -0.268
  },
  "asset_trend": [
    {
      "date": "2026-07-25",
      "total_krw": 446968
    },
    {
      "date": "2026-07-26",
      "total_krw": 445758
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
      "total_asset_krw": 445758,
      "main_pnl_krw": -1413,
      "twin_pnl_krw": 203,
      "total_pnl_krw": -1211,
      "main_pnl_pct": -0.555,
      "twin_pnl_pct": 0.105,
      "total_pnl_pct": -0.271,
      "target_met": false
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 253350,
      "balance_krw": 164707,
      "balance_usdt": 60.6,
      "cum_pnl_krw": -1413,
      "cum_pnl_pct": -0.555,
      "cum_pnl_since": "2026-07-25",
      "total_pnl_usd_record": 199.7,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": -1413,
      "daily_pnl_pct": -0.555,
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
      "asset_krw": 192408,
      "xrp_bithumb": 30.5819,
      "xrp_okx": 57.0277,
      "xrp_target": 43.8692,
      "hedge_upnl_usd": 3.4124,
      "cum_pnl_krw": 203,
      "cum_pnl_pct": 0.105,
      "cum_pnl_since": "2026-07-25",
      "session_pnl_usd_record": 0.4142,
      "today_pnl_usd_record": 0.0135,
      "daily_pnl_krw": 203,
      "daily_pnl_pct": 0.105,
      "daily_target_met": false,
      "today_trades": 2,
      "recent_trades": [
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
        },
        {
          "time": "2026-07-25T19:53:05.128742",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.2,
          "pnl_usd": 0.0042
        },
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
        }
      ]
    }
  }
};