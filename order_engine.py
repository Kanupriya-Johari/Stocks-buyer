from kiteconnect import KiteConnect
import config, logging, notifier
import data_fetcher

logger = logging.getLogger(__name__)


class OrderEngine:
    def __init__(self, kite: KiteConnect, risk_mgr):
        self.kite = kite
        self.rm   = risk_mgr

    def place_buy_order(self, symbol: str, qty: int, entry_price: float,
                        sl: float, target: float) -> str:

        if config.PAPER_TRADING:
            order_id = f'PAPER-{symbol}-BUY-{qty}'
            logger.info(f'[PAPER] {order_id} @{entry_price}')
        else:
            try:
                order_id = self.kite.place_order(
                    variety=self.kite.VARIETY_REGULAR,
                    exchange=config.EXCHANGE,
                    tradingsymbol=symbol,
                    transaction_type=self.kite.TRANSACTION_TYPE_BUY,
                    quantity=qty,
                    product=self.kite.PRODUCT_CNC,
                    order_type=self.kite.ORDER_TYPE_LIMIT,
                    price=entry_price,
                    validity=self.kite.VALIDITY_DAY
                )
                logger.info(f'[LIVE BUY] {symbol} qty={qty} @{entry_price} id={order_id}')
            except Exception as e:
                logger.error(f'Order failed for {symbol}: {e}')
                notifier.send(f'ORDER FAILED\nSymbol: {symbol}\nError: {e}')
                return ''

        notifier.send(
            f'BUY ORDER PLACED\n'
            f'Symbol: {symbol}\n'
            f'Qty: {qty}\n'
            f'Entry: Rs{entry_price}\n'
            f'Stop Loss: Rs{sl}\n'
            f'Target: Rs{target}\n'
            f'Type: CNC (Delivery)\n'
            f'ID: {order_id}'
        )
        self.rm.open_position(symbol, entry_price, qty, sl, target)
        return order_id

    def place_sell_order(self, symbol: str, qty: int, reason: str = 'Signal') -> str:
        if config.PAPER_TRADING:
            order_id = f'PAPER-{symbol}-SELL-{qty}'
            logger.info(f'[PAPER SELL] {order_id} reason={reason}')
        else:
            try:
                order_id = self.kite.place_order(
                    variety=self.kite.VARIETY_REGULAR,
                    exchange=config.EXCHANGE,
                    tradingsymbol=symbol,
                    transaction_type=self.kite.TRANSACTION_TYPE_SELL,
                    quantity=qty,
                    product=self.kite.PRODUCT_CNC,
                    order_type=self.kite.ORDER_TYPE_MARKET,
                    validity=self.kite.VALIDITY_DAY
                )
                logger.info(f'[LIVE SELL] {symbol} qty={qty} id={order_id}')
            except Exception as e:
                logger.error(f'Sell failed for {symbol}: {e}')
                notifier.send(f'SELL FAILED - CHECK KITE NOW\nSymbol: {symbol}\nError: {e}')
                return ''

        exit_price = data_fetcher.get_current_price(symbol)
        pnl = self.rm.close_position(symbol, exit_price)
        notifier.send(
            f'SELL ORDER PLACED\n'
            f'Symbol: {symbol}\n'
            f'Qty: {qty}\n'
            f'Approx Exit: Rs{exit_price}\n'
            f'Reason: {reason}\n'
            f'Trade PnL: Rs{pnl:.2f}\n'
            f'Day PnL: Rs{self.rm.daily_pnl:.2f}'
        )
        return order_id

    def check_exits(self):
        for symbol, pos in list(self.rm.positions.items()):
            price = data_fetcher.get_current_price(symbol)
            if price <= 0:
                continue
            if price <= pos['sl']:
                logger.info(f'SL HIT: {symbol} @ Rs{price}')
                self.place_sell_order(symbol, pos['qty'], 'STOP LOSS HIT')
            elif price >= pos['target']:
                logger.info(f'TARGET HIT: {symbol} @ Rs{price}')
                self.place_sell_order(symbol, pos['qty'], 'TARGET HIT')
