from collections import OrderedDict


class Trade:

    def __init__(self, stocks):
        self.stocks = stocks
        self.quantity = None
        self.bs_indicator = None
        self.trade_price = None
        self.trade_time = None

        print('Creating trade for', stocks.get_stock_symbol())

    def set_quantity(self, data):
        self.quantity = data

    def set_bs_indicator(self, data):
        self.bs_indicator = data

    def set_trade_price(self, data):
        self.trade_price = data

    def set_trade_time(self, data):
        self.trade_time = data

    def get_quantity(self):
        return self.quantity

    def get_bs_indicator(self):
        return self.bs_indicator

    def get_trade_price(self):
        return self.trade_price

    def get_trade_time(self):
        return self.trade_time

    def get_trades(self):
        return OrderedDict({
            'StockSymbol': self.stocks.get_stock_symbol(),
            'Quantity': self.get_quantity(),
            'BSIndicator': self.get_bs_indicator(),
            'TradePrice': self.get_trade_price(),
            'TradeTime': self.get_trade_time()
        })