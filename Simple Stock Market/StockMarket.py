from collections import OrderedDict
import CustomExceptions

class StockMarket:

    def __init__(self):

        self.stock_symbol = None
        self.type = None
        self.last_dividend = None
        self.fixed_dividend = None
        self.par_value = None
        self.dividend_yield = None

    def set_stock_symbol(self, data):
        self.stock_symbol = data.upper()

    def set_type(self, data):
        self.type = data.upper()

    def set_last_dividend(self, data):
        self.last_dividend = data

    def set_fixed_dividend(self, data):
        self.fixed_dividend = data

    def set_par_value(self, data):
        self.par_value = data

    def get_stock_symbol(self):
        return self.stock_symbol

    def get_type(self):
        return self.type

    def get_last_dividend(self):
        return self.last_dividend

    def get_fixed_dividend(self):
        return self.fixed_dividend

    def get_par_value(self):
        return self.par_value

    def calculate_dividend_yield(self, price):
        try:
            if self.get_type() == 'COMMON':
                self.dividend_yield = self.get_last_dividend() / price
            elif self.get_type() == 'PREFERRED':
                if self.get_fixed_dividend is not None:
                    self.dividend_yield = ((float(
                        self.get_fixed_dividend().strip('%')) / 100) * self.get_par_value()) / price
                else:
                    raise CustomExceptions.FixedDividendNotDefined('Fixed dividend should be defined for the '
                                                                   'preferred stocks')
            else:
                raise CustomExceptions.NoFormulaPresentForNewType('Stock type other than Common or Preferred is not '
                                                                  'handled here')
        except Exception as e:
            print(e)

    def calculate_pe_ratio(self, price):
        return self.dividend_yield / price

    def get_stocks(self):
        return OrderedDict({
            'StockSymbol': self.get_stock_symbol(),
            'Type':self.get_type(),
            'LastDividend': self.get_last_dividend(),
            'FixedDividend': self.get_fixed_dividend(),
            'ParValue': self.get_par_value()
        })