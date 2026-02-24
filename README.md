🤖 Stocks Buyer — Zerodha Algo Trading Bot
An automated swing trading bot for Indian stock markets (NSE) built with Python.
Scans 80 Nifty 50 + Midcap stocks daily using RSI + MACD strategy and places CNC delivery orders via Zerodha's free Kite Personal API.

⚡ Tech Stack
ComponentToolCostMarket DatayfinanceFREEOrder ExecutionKite Personal APIFREENotificationsTwilio WhatsAppFREECloud ServerAzure VM (Standard_B1s)~₹600/month
Total running cost: ₹600/month only!

📈 Strategy
Swing trading on daily candles — holds positions for 3-7 days (CNC delivery).
Entry conditions (ALL must be true):

Price above 50-day SMA (uptrend filter)
RSI(14) was below 40, now recovering (oversold bounce)
MACD histogram crossed from negative to positive (momentum confirmation)
Volume above 1.2x 20-day average (participation confirmation)

Exit conditions:

Stop Loss hit (4% below entry)
Target hit (8% above entry — 1:2 risk:reward)
MACD histogram turns negative (momentum fading)


📁 File Structure
kitebot/
├── bot.py              # Main runner — schedules everything
├── auto_login.py       # Zerodha login via TOTP
├── data_fetcher.py     # Downloads daily OHLCV from yfinance
├── strategy_swing.py   # RSI + MACD signal logic
├── risk_manager.py     # Position sizing, daily loss limits
├── order_engine.py     # Places CNC orders via Kite API
├── notifier.py         # WhatsApp alerts via Twilio
├── news_filter.py      # Gemini AI news filter (optional)
├── backtest.py         # Backtests strategy on 2 years data
└── logs/               # Daily log files

⏰ Daily Schedule (IST)
TimeAction08:50 AMReset daily P&L counters09:20 AMCheck exits (SL/target hit)09:25 AMScan batch 1 (first 40 symbols)09:40 AMScan batch 2 (next 40 symbols)03:35 PMEOD WhatsApp report

📊 Symbols Scanned (80 total)
Nifty 50 (all 50): HDFCBANK, ICICIBANK, KOTAKBANK, SBIN, AXISBANK, BAJFINANCE, BAJAJFINSV, SHRIRAMFIN, HDFCLIFE, SBILIFE, TCS, INFY, WIPRO, HCLTECH, TECHM, LTIM, RELIANCE, ONGC, BPCL, POWERGRID, NTPC, TATAPOWER, MARUTI, TATAMOTORS, M&M, EICHERMOT, BAJAJ-AUTO, HEROMOTOCO, HINDUNILVR, ITC, NESTLEIND, BRITANNIA, SUNPHARMA, DRREDDY, CIPLA, DIVISLAB, APOLLOHOSP, TATASTEEL, HINDALCO, JSWSTEEL, GRASIM, ULTRACEMCO, ADANIENT, ADANIPORTS, LT, TITAN, ASIANPAINT, COALINDIA, INDUSINDBK, ZOMATO
Nifty Midcap 150 — Quality picks (30): PERSISTENT, MPHASIS, COFORGE, FEDERALBNK, IDFCFIRSTB, BANDHANBNK, AUROPHARMA, TORNTPHARM, ALKEM, CUMMINSIND, BHEL, SIEMENS, INDHOTEL, IRCTC, PIIND, UPL, CHAMBLFERT, SAIL, NMDC, NATIONALUM, MUTHOOTFIN, CHOLAFIN, MAXHEALTH, LALPATHLAB, ASTRAL, POLYCAB, TRENT, VEDL, GLAND, OBEROIRLTY

🚀 Setup
Prerequisites

Zerodha account with Kite Personal API (free) — developers.kite.trade
Twilio account for WhatsApp alerts — twilio.com
Azure VM (Standard_B1s, Ubuntu 22.04, South India region)

Installation
bashgit clone https://github.com/Kanupriya-Johari/Stocks-buyer.git
cd Stocks-buyer
python3 -m venv venv
source venv/bin/activate
pip install kiteconnect yfinance pandas numpy twilio python-dotenv pyotp requests pytz schedule google-genai
Configuration
Create a .env file (never commit this!):
KITE_API_KEY=your_api_key
KITE_API_SECRET=your_api_secret
KITE_USER_ID=your_user_id
KITE_PASSWORD=your_password
KITE_TOTP_SECRET=your_totp_secret
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_FROM=whatsapp:+14155238886
TWILIO_TO=whatsapp:+91XXXXXXXXXX
PAPER_TRADING=true
MAX_DAILY_LOSS_INR=1500
RISK_PER_TRADE_INR=300
MAX_OPEN_POSITIONS=3
SWING_SL_PERCENT=4.0
SWING_SYMBOLS=RELIANCE,INFY,TCS,...
Running
bash# Get daily token first (every market day before 9 AM)
python3 get_token.py

# Start bot in screen
screen -S kitebot
python3 bot.py
# Ctrl+A then D to detach

⚠️ Disclaimer
This bot is for educational purposes. Algorithmic trading carries significant financial risk. Always paper trade for at least 2-3 weeks before going live. Never trade money you cannot afford to lose. You are solely responsible for all trading decisions.

📱 WhatsApp Alerts
The bot sends WhatsApp alerts for:

Bot startup
Every BUY order placed
Every SELL order (SL hit / target hit / signal exit)
Daily EOD report (P&L, open positions, order count)


Built with ❤️ | Paper trade first, always!
