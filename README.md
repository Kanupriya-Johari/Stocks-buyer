# 🤖 Stocks Buyer — Zerodha Algo Trading Bot

An automated swing trading bot for Indian stock markets (NSE).
Scans 80 Nifty 50 + Midcap stocks daily using RSI + MACD strategy.

## ⚡ Tech Stack
- Market Data: yfinance (FREE)
- Order Execution: Kite Personal API (FREE)
- Notifications: Twilio WhatsApp (FREE)
- Cloud Server: Azure VM (~₹600/month)

## 📈 Strategy
Swing trading on daily candles, 3-7 day hold, CNC delivery.
Entry: RSI oversold bounce + MACD histogram cross + above 50 SMA + volume confirmation
Exit: SL (4%) / Target (8%) / MACD exit signal

## ⏰ Daily Schedule (IST)
- 08:50 AM — Reset counters
- 09:20 AM — Exit checks
- 09:25 AM — Scan batch 1 (40 symbols)
- 09:40 AM — Scan batch 2 (40 symbols)
- 03:35 PM — EOD WhatsApp report

## ⚠️ Disclaimer
For educational purposes only. Always paper trade first. Never risk money you cannot afford to lose.
