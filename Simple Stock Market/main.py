from datetime import datetime

import pandas as pd

import CustomExceptions
import StockMarket
import Trade
import TradingOutputs

if __name__ == "__main__":
    try:
        # Setting up of data given in the assignment
        stock_data = {
            "Stock Symbol": ['TEA', 'POP', 'ALE', 'GIN', 'JOE'],
            "Type": ['Common', 'Common', 'Common', 'Preferred', 'Common'],
            "Last Dividend": [0, 8, 23, 8, 13],
            "Fixed Dividend": [None, None, None, '2%', None],
            "Par Value": [100, 100, 60, 100, 250]
        }

        stock_data_df = pd.DataFrame(stock_data)

        mystock_list = []  # this will have all of the stocks objects class as list.
        object_count = 0  # No of stock class objects. Initializing to 0.

        # Iterating over stock data dataframe. Creating stock objects and adding to object lists.

        # Below loop will dynamically setup stock class objects and add data present in the stock_data_df dataframe
        # to stocks class.

        for index, rows in stock_data_df.iterrows():
            print('Adding a new stock in Market for:', rows['Stock Symbol'])
            my_stocks = StockMarket.StockMarket()
            mystock_list.append(my_stocks)

            mystock_list[object_count].set_stock_symbol(rows['Stock Symbol'])
            mystock_list[object_count].set_type(rows['Type'])
            mystock_list[object_count].set_last_dividend(rows['Last Dividend'])
            mystock_list[object_count].set_fixed_dividend(rows['Fixed Dividend'])
            mystock_list[object_count].set_par_value(rows['Par Value'])

            object_count += 1

        stock_data = pd.DataFrame.from_records([my_stock.get_stocks() for my_stock in mystock_list])
        print('Stock Market data')
        print(stock_data)

        # Stocks are created with above steps.

        # Testing Inputs -
        # For a given stock, i. Given any price as input, calculate the dividend yield and PE ratio

        stock_symbol = 'GIN'  # Input stock name here
        stock_price = 100  # Input stock price here

        stock_object = None  # Stock object which is used to check the given stock is in the stock market or not.

        for stock in mystock_list:
            if stock.get_stock_symbol() == stock_symbol.upper():
                stock_object = stock

        if stock_object is None:
            raise CustomExceptions.NoStockFound(
                '{} stock is not present in the stock market. Please use valid stock symbol'.format(stock_symbol))

        # Calculating dividend yield.
        stock_object.calculate_dividend_yield(stock_price)
        print('Dividend yield for {} is {}'.format(stock_object.get_stock_symbol(), stock_object.dividend_yield))

        pe = stock_object.calculate_pe_ratio(stock_price)
        print('P/E Ratio for {} is {}'.format(stock_object.get_stock_symbol(), pe))

        # Setting up of trading data.
        trade_data = {
            "Stocks": [mystock_list[0], mystock_list[1], mystock_list[0], mystock_list[2], mystock_list[3],
                       mystock_list[4], mystock_list[4], mystock_list[4]],
            "Quantity": [1, 10, 2, 5, 80, 7, 2, 10],
            "BS Indicator": ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
            "Trade Price": [100, 1000, 150, 299, 478, 3874, 4000, 4100],
            "Trade Time": [datetime.now(), '2019-09-18 00:01:10.790865', datetime.now(), datetime.now(), datetime.now(),
                           datetime.now(), datetime.now(), datetime.now()]
        }

        trade_data_df = pd.DataFrame(trade_data)

        mytrade_list = []  # this will have all of the trade objects class as list.
        object_count = 0  # No of trade class objects. Initializing to 0.

        # Iterating over trade data dataframe. Creating trade objects and adding to object lists.

        # Below loop will dynamically setup trade class objects and add data present in the trade_data_df dataframe to stocks class.

        for index, rows in trade_data_df.iterrows():
            my_trade = Trade.Trade(rows['Stocks'])
            mytrade_list.append(my_trade)

            mytrade_list[object_count].set_quantity(rows['Quantity'])
            mytrade_list[object_count].set_bs_indicator(rows['BS Indicator'])
            mytrade_list[object_count].set_trade_price(rows['Trade Price'])
            mytrade_list[object_count].set_trade_time(rows['Trade Time'])

            object_count += 1

        all_stock_trades = TradingOutputs.TradingOutputs()
        all_stock_trades.record_trades(mytrade_list)
        print('Trades Recorded:\n', all_stock_trades.trade_df)

        stocks_traded = list(all_stock_trades.trade_df['StockSymbol'].unique())
        print('Stocks Traded:', stocks_traded)

        all_stock_trades.calculate_stocks_vwsp(stocks_traded)
        print('Calculate Volume wighted stock price for last 5 minutes')
        print('VWSP', all_stock_trades.vwsp_dict)

        # GBCE All share index
        asi = all_stock_trades.calculate_all_share_index()
        print('GBCE All Share Index: ', asi)

    except Exception as e:
        print(e)
