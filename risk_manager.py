import logging
import config

logger = logging.getLogger(__name__)


class RiskManager:
    def __init__(self):
        self.daily_pnl    = 0.0
        self.positions    = {}
        self.orders_today = 0

    def can_enter(self, symbol: str) -> tuple:
        if self.daily_pnl <= -config.MAX_DAILY_LOSS:
            return False, f'Daily loss limit ₹{config.MAX_DAILY_LOSS:.0f} reached'
        if symbol in self.positions:
            return False, f'Already holding {symbol}'
        if len(self.positions) >= config.MAX_POSITIONS:
            return False, f'Max {config.MAX_POSITIONS} positions open'
        return True, 'OK'

    def calc_qty(self, entry: float, stop_loss: float) -> int:
        risk_per_share = abs(entry - stop_loss)
        if risk_per_share < 0.01:
            return 0
        qty = int(config.RISK_PER_TRADE / risk_per_share)
        return max(1, qty)

    def open_position(self, symbol, entry, qty, sl, target):
        self.positions[symbol] = {
            'entry': entry, 'qty': qty,
            'sl': sl, 'target': target
        }
        self.orders_today += 1
        logger.info(f'Position opened: {symbol} {qty}@{entry} SL={sl} TGT={target}')

    def close_position(self, symbol, exit_price) -> float:
        if symbol not in self.positions:
            return 0.0
        pos = self.positions.pop(symbol)
        pnl = (exit_price - pos['entry']) * pos['qty']
        self.daily_pnl += pnl
        logger.info(f'Closed: {symbol} PnL=₹{pnl:.2f} | Day=₹{self.daily_pnl:.2f}')
        return pnl

    def reset_daily(self):
        self.daily_pnl    = 0.0
        self.orders_today = 0
        logger.info('Daily counters reset')
