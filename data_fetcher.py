import yfinance as yf
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def to_yf_ticker(symbol: str) -> str:
    """Convert NSE symbol to yfinance format."""
    if not symbol.endswith('.NS') and not symbol.endswith('.BO'):
        return symbol + '.NS'
    return symbol


def get_daily_data(symbol: str, days: int = 120) -> pd.DataFrame:
    ticker = to_yf_ticker(symbol)
    try:
        df = yf.download(ticker, period=f'{days}d', interval='1d',
                         auto_adjust=True, progress=False)
        if df.empty:
            logger.warning(f'No data returned for {ticker}')
            return pd.DataFrame()

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0].lower() for col in df.columns]
        else:
            df.columns = [c.lower() for c in df.columns]

        df.index = pd.to_datetime(df.index)
        df = df.dropna()
        logger.info(f'Fetched {len(df)} candles for {symbol}')
        return df

    except Exception as e:
        logger.error(f'Data fetch error for {symbol}: {e}')
        return pd.DataFrame()


def get_current_price(symbol: str) -> float:
    ticker = to_yf_ticker(symbol)
    try:
        data = yf.download(ticker, period='2d', interval='1d',
                           auto_adjust=True, progress=False)
        if data.empty:
            return 0.0
        if isinstance(data.columns, pd.MultiIndex):
            return float(data['Close'].iloc[-1].values[0])
        return float(data['Close'].iloc[-1])
    except Exception as e:
        logger.error(f'Price fetch error for {symbol}: {e}')
        return 0.0
