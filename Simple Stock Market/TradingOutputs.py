import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class TradingOutputs:

    def __init__(self):
        self.trade_df = pd.DataFrame()
        self.vwsp_dict = {}

    def record_trades(self, trade_data):
        self.trade_df = pd.DataFrame.from_records([trade.get_trades() for trade in trade_data])

    def calculate_stocks_vwsp(self, stock_symbols):
        try:
            end_time = datetime.now()

            start_time = end_time - timedelta(minutes=5)

            for stock_symbol in stock_symbols:
                trade_df_5mins = self.trade_df[self.trade_df.StockSymbol == stock_symbol].copy()

                trade_df_5mins.TradeTime = pd.to_datetime(trade_df_5mins.TradeTime)

                trade_df_5mins.set_index(trade_df_5mins.TradeTime, inplace=True)

                trade_df_5mins = trade_df_5mins[start_time:end_time]

                if trade_df_5mins.empty:
                    print('No last 5 mins trades found for {}'.format(stock_symbol))
                else:
                    trade_df_5mins['TradePrice * Quantity'] = trade_df_5mins.TradePrice * trade_df_5mins.Quantity

                    vwsp = trade_df_5mins['TradePrice * Quantity'].sum() / trade_df_5mins.Quantity.sum()

                    self.vwsp_dict[stock_symbol] = vwsp

        except Exception as e:

            print('Some Exception occured', e)

    def calculate_all_share_index(self):
        try:
            no_of_stocks = len(self.vwsp_dict)
            if no_of_stocks == 0:
                asi = 0

            else:
                asi = np.power(np.prod(list(self.vwsp_dict.values())), (1 / no_of_stocks))

            return asi
        except Exception as e:
            print(e)
