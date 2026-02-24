import pandas as pd
import numpy as np
import logging
import config

logger = logging.getLogger(__name__)


def get_signal(df):
    if len(df) < 60:
        return {'signal': 'NONE'}

    df = df.copy()

    delta = df['close'].diff()
    gain  = delta.clip(lower=0).ewm(span=14, adjust=False).mean()
    loss  = (-delta.clip(upper=0)).ewm(span=14, adjust=False).mean()
    rs    = gain / loss.replace(0, np.nan)
    df['rsi'] = 100 - (100 / (1 + rs))

    ema12          = df['close'].ewm(span=12, adjust=False).mean()
    ema26          = df['close'].ewm(span=26, adjust=False).mean()
    df['macd']     = ema12 - ema26
    df['macd_sig'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['macd_hist']= df['macd'] - df['macd_sig']

    df['sma50']   = df['close'].rolling(50).mean()
    df['vol_avg'] = df['volume'].rolling(20).mean()

    last  = df.iloc[-1]
    prev  = df.iloc[-2]
    entry = round(float(last['close']), 2)

    if prev['macd_hist'] > 0 and last['macd_hist'] < 0:
        return {'signal': 'EXIT', 'entry': entry}

    uptrend      = last['close'] > last['sma50']
    rsi_recovery = prev['rsi'] < 40 and last['rsi'] > prev['rsi']
    macd_cross   = prev['macd_hist'] < 0 and last['macd_hist'] > 0
    vol_ok       = last['volume'] > 1.2 * last['vol_avg']

    if uptrend and rsi_recovery and macd_cross and vol_ok:
        sl     = round(entry * (1 - config.SWING_SL_PCT), 2)
        target = round(entry + 2 * (entry - sl), 2)
        return {
            'signal':    'BUY',
            'entry':     entry,
            'stop_loss': sl,
            'target':    target,
            'hold_days': 7
        }

    return {'signal': 'NONE'}
