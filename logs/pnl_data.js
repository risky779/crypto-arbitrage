const pnlData = {
  "updated_at": "2026-07-28 08:31:04",
  "usd_krw": 1459.6,
  "total_asset_krw": 446085,
  "daily_pnl_krw": 2568,
  "daily_yield_pct": 0.579,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 454267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -8182,
    "seed_yield_pct": -1.801,
    "days_since_seed": 9,
    "avg_daily_yield_pct": -0.2
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
      "total_krw": 446085
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
      "total_asset_krw": 446085,
      "main_pnl_krw": 3600,
      "twin_pnl_krw": -1031,
      "total_pnl_krw": 2568,
      "main_pnl_pct": 1.413,
      "twin_pnl_pct": -0.546,
      "total_pnl_pct": 0.579,
      "target_met": false
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 258325,
      "balance_krw": 235243,
      "balance_usdt": 15.81,
      "cum_pnl_krw": 3562,
      "cum_pnl_pct": 1.398,
      "cum_pnl_since": "2026-07-25",
      "total_pnl_usd_record": 199.7,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": 3600,
      "daily_pnl_pct": 1.413,
      "daily_target_met": true,
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
      "asset_krw": 187760,
      "xrp_bithumb": 29.7198,
      "xrp_okx": 56.4657,
      "xrp_target": 42.8543,
      "hedge_upnl_usd": 6.1596,
      "cum_pnl_krw": -4445,
      "cum_pnl_pct": -2.313,
      "cum_pnl_since": "2026-07-25",
      "session_pnl_usd_record": 0.6088,
      "today_pnl_usd_record": 0.0773,
      "daily_pnl_krw": -1031,
      "daily_pnl_pct": -0.546,
      "daily_target_met": false,
      "today_trades": 14,
      "recent_trades": [
        {
          "time": "2026-07-28T08:29:56.224779",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.242,
          "pnl_usd": 0.0071
        },
        {
          "time": "2026-07-28T08:29:21.786780",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.223,
          "pnl_usd": 0.0058
        },
        {
          "time": "2026-07-28T08:25:34.734627",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.232,
          "pnl_usd": 0.0065
        },
        {
          "time": "2026-07-28T08:25:00.965735",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.242,
          "pnl_usd": 0.0071
        },
        {
          "time": "2026-07-28T08:16:57.383231",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.237,
          "pnl_usd": 0.0068
        },
        {
          "time": "2026-07-28T08:16:23.644573",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.19,
          "pnl_usd": 0.0035
        },
        {
          "time": "2026-07-28T08:15:49.532987",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.198,
          "pnl_usd": 0.0041
        },
        {
          "time": "2026-07-28T08:09:22.196839",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.245,
          "pnl_usd": 0.0074
        },
        {
          "time": "2026-07-28T08:08:48.328812",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.218,
          "pnl_usd": 0.0055
        },
        {
          "time": "2026-07-28T08:08:14.576728",
          "coin": "XRP",
          "sell_side": "BITHUMB",
          "gap_pct": -0.206,
          "pnl_usd": 0.0046
        }
      ]
    }
  }
};