const pnlData = {
  "updated_at": "2026-07-29 17:01:04",
  "usd_krw": 1457.52,
  "total_asset_krw": 430766,
  "daily_pnl_krw": -8289,
  "daily_yield_pct": -1.888,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 454267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -23501,
    "seed_yield_pct": -5.173,
    "days_since_seed": 10,
    "avg_daily_yield_pct": -0.517
  },
  "reconciliation": {
    "since": "2026-07-25",
    "combined_realized_usd": -1.45,
    "combined_actual_delta_usd": -9.14,
    "drift_usd": -7.69,
    "drift_pct": -2.601,
    "status": "OK",
    "note": "drift = 실제총자산 증감(마크투마켓 포함) - 원장상 실현손익합계. 헷지 정상이면 작아야 함."
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
      "total_krw": 430766
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
      "total_asset_krw": 430766,
      "main_pnl_krw": 13444,
      "twin_pnl_krw": -21733,
      "total_pnl_krw": -8289,
      "main_pnl_pct": 3.959,
      "twin_pnl_pct": -21.846,
      "total_pnl_pct": -1.888,
      "target_met": false
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 414054,
      "balance_krw": 7645,
      "balance_usdt": 280.77,
      "cum_pnl_krw": 13444,
      "cum_pnl_pct": 3.959,
      "cum_pnl_since": "2026-07-28",
      "twr_pct": -0.001,
      "twr_events": 3,
      "twr_since": "2026-07-25",
      "total_pnl_usd_record": 199.7,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": 13444,
      "daily_pnl_pct": 3.959,
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
      "asset_krw": 16713,
      "xrp_bithumb": 1.1015,
      "xrp_okx": 5.3,
      "xrp_target": 3.2008,
      "hedge_upnl_usd": 0.0124,
      "cum_pnl_krw": -21733,
      "cum_pnl_pct": -21.846,
      "cum_pnl_since": "2026-07-28",
      "twr_pct": -1.1082,
      "twr_events": 96,
      "twr_since": "2026-07-25",
      "session_pnl_usd_record": 1.9353,
      "today_pnl_usd_record": 0.3505,
      "daily_pnl_krw": -21733,
      "daily_pnl_pct": -21.846,
      "daily_target_met": false,
      "today_trades": 6,
      "recent_trades": [
        {
          "time": "2026-07-29T10:55:59.868351",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.722,
          "pnl_usd": 0.0341
        },
        {
          "time": "2026-07-29T10:53:16.397339",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 0.769,
          "pnl_usd": 0.0624
        },
        {
          "time": "2026-07-29T09:37:42.722730",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 1.279,
          "pnl_usd": 0.0421
        },
        {
          "time": "2026-07-29T09:37:08.617472",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 1.324,
          "pnl_usd": 0.0818
        },
        {
          "time": "2026-07-29T00:53:26.614257",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 1.042,
          "pnl_usd": 0.0625
        },
        {
          "time": "2026-07-29T00:52:51.830773",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 1.117,
          "pnl_usd": 0.0676
        },
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
        }
      ]
    }
  }
};