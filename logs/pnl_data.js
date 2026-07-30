const pnlData = {
  "updated_at": "2026-07-31 02:46:04",
  "usd_krw": 1448.99,
  "total_asset_krw": 422820,
  "daily_pnl_krw": -486,
  "daily_yield_pct": -0.115,
  "target_daily_yield_pct": 1.0,
  "seed": {
    "seed_krw": 454267,
    "seed_date": "2026-07-19",
    "seed_pnl_krw": -31447,
    "seed_yield_pct": -6.922,
    "days_since_seed": 12,
    "avg_daily_yield_pct": -0.577
  },
  "reconciliation": {
    "since": "2026-07-25",
    "combined_realized_usd": -2.98,
    "combined_actual_delta_usd": -12.89,
    "drift_usd": -9.9,
    "drift_pct": -3.394,
    "status": "WARNING",
    "note": "drift = 실제총자산 증감(마크투마켓 포함) - 원장상 실현손익합계. 헷지 정상이면 작아야 함."
  },
  "bot_reconciliation": {
    "twin_bot": {
      "displayed_asset_krw": 170073,
      "twr_implied_asset_krw": 187524,
      "drift_krw": -17451,
      "drift_pct": -10.26,
      "status": "WARNING"
    },
    "main_bot": {
      "displayed_asset_krw": 252747,
      "twr_implied_asset_krw": 249645,
      "drift_krw": 3102,
      "drift_pct": 1.23,
      "status": "OK"
    },
    "note": "drift = 표시자산(shift보정) - TWR내포자산(그 봇 자체 거래+이체비용만). 크면 cum_capital_shift_krw가 못 잡은 미기록 자본이동 의심."
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
      "total_krw": 431012
    },
    {
      "date": "2026-07-30",
      "total_krw": 423306
    },
    {
      "date": "2026-07-31",
      "total_krw": 422820
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
      "main_pnl_krw": 0,
      "twin_pnl_krw": -4463,
      "total_pnl_krw": -4461,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -2.354,
      "total_pnl_pct": -1.006,
      "target_met": false
    },
    {
      "date": "2026-07-29",
      "total_asset_krw": 431012,
      "main_pnl_krw": 0,
      "twin_pnl_krw": -8042,
      "total_pnl_krw": -8044,
      "main_pnl_pct": 0.0,
      "twin_pnl_pct": -4.345,
      "total_pnl_pct": -1.832,
      "target_met": false
    },
    {
      "date": "2026-07-30",
      "total_asset_krw": 423306,
      "main_pnl_krw": -521,
      "twin_pnl_krw": -7185,
      "total_pnl_krw": -7706,
      "main_pnl_pct": -0.205,
      "twin_pnl_pct": -4.058,
      "total_pnl_pct": -1.788,
      "target_met": false
    },
    {
      "date": "2026-07-31",
      "total_asset_krw": 422820,
      "main_pnl_krw": -677,
      "twin_pnl_krw": 191,
      "total_pnl_krw": -486,
      "main_pnl_pct": -0.267,
      "twin_pnl_pct": 0.113,
      "total_pnl_pct": -0.115,
      "target_met": false
    }
  ],
  "bots": {
    "main_bot": {
      "label": "메인봇 · 전송 아비트라지",
      "running": true,
      "asset_krw": 252747,
      "balance_krw": 5468,
      "balance_usdt": 117.41,
      "cum_pnl_krw": -1198,
      "cum_pnl_pct": -0.472,
      "cum_pnl_since": "2026-07-28",
      "twr_pct": -0.7893,
      "twr_events": 10,
      "twr_since": "2026-07-25",
      "total_pnl_usd_record": 201.07,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": -677,
      "daily_pnl_pct": -0.267,
      "daily_target_met": false,
      "today_trades": 0,
      "pending_transfers": 0,
      "restart_count": 1,
      "recent_trades": [
        {
          "time": "2026-07-30T13:40:04.468295",
          "coin": "XLM",
          "profit_usd": 0.1462
        },
        {
          "time": "2026-07-30T12:36:11.883013",
          "coin": "XLM",
          "profit_usd": 0.2262
        },
        {
          "time": "2026-07-30T12:32:05.414682",
          "coin": "XLM",
          "profit_usd": 0.2487
        },
        {
          "time": "2026-07-30T10:40:46.587146",
          "coin": "XLM",
          "profit_usd": 0.2465
        },
        {
          "time": "2026-07-30T10:38:01.608762",
          "coin": "SUI",
          "profit_usd": 0.2568
        },
        {
          "time": "2026-07-30T10:29:02.763836",
          "coin": "XLM",
          "profit_usd": 0.2467
        },
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
        }
      ]
    },
    "twin_bot": {
      "label": "쌍둥이봇 · 양쪽재고 로컬거래",
      "running": true,
      "asset_krw": 170073,
      "xrp_bithumb": 112.6273,
      "xrp_okx": 6.1329,
      "xrp_target": 59.3848,
      "hedge_upnl_usd": -1.8601,
      "cum_pnl_krw": -15035,
      "cum_pnl_pct": -8.122,
      "cum_pnl_since": "2026-07-28",
      "twr_pct": -1.2306,
      "twr_events": 105,
      "twr_since": "2026-07-25",
      "session_pnl_usd_record": 2.2963,
      "today_pnl_usd_record": 0,
      "daily_pnl_krw": 191,
      "daily_pnl_pct": 0.113,
      "daily_target_met": false,
      "today_trades": 0,
      "recent_trades": [
        {
          "time": "2026-07-30T13:45:08.980545",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 1.685,
          "pnl_usd": 0.1063
        },
        {
          "time": "2026-07-30T13:44:34.635278",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 1.609,
          "pnl_usd": 0.1012
        },
        {
          "time": "2026-07-30T13:33:33.888024",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 1.618,
          "pnl_usd": 0.1018
        },
        {
          "time": "2026-07-29T18:22:07.355856",
          "coin": "XRP",
          "sell_side": "OKX",
          "gap_pct": 1.644,
          "pnl_usd": 0.0516
        },
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
        }
      ]
    }
  }
};