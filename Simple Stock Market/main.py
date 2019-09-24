"""
Author - Jaideep Singh

Problem Description - 

Super simple stock market
 
1. The Global Beverage Corporation Exchange is a new stock market trading in drinks companies.
    a. Your company is building the OOPS system to run that trading
    b. You have been assigned to build part of the core object model for a limited phase 1

2. Provide the complete source code that will:
    a. For a given stock,
        i. Given any price input, calculate the dividend yield.
       ii. Given any price input, calculate the P/E Ratio.
      iii. Record trade, with timestamp, quantity, buy or sell indicator and price.
       iv. Calculate Volume Weighted Stock Price based on trades in past 5 minutes.
    
    b. Calculate the GBCE All Share Index using the geometric mena of the Volume Weighted Stock Price for all stocks.

Formulas to be used as part of this problem:

1. Dividend Yield - The dividend yeild is the ratio of a company's annual dividend compared to its share price. While high dividend yields are attractive, they may come at the cost of growth potential. Every dollar a company is paying in dividends to its shareholders is a dollar that company is not re-investing to grow and generate capital gains. Shareholders can earn high returns if the value of their stock increases while they hold it.
    a. Common - Last Dividend / Price
    b. Preferred - (Fixed Dividend * Par Value) / Price
    
2. P/E Ratio - Price / Dividend
    The P/E Ratio measures the relationship between a company's stock price and its earnings per share of stock issued.
    
3. Geometric Mean - nth root of product of "Volume weighted stock price".

4. Volume weighted stock price - (summation(traded price * quantity))/summation(quantity)

Dataset attribute descriptions based on my knowledge

    a. Stock symbol - TIcker. A stock symbol is a unique series of letter assigned to a security for trading purposes. NYSE or AMEX have 3 characters or less. NASDAQ has 4-5 characters
    
    b. Type - Stock type(Common, preferred) - The main difference is that preferred stock usually do not give shareholders voting rights, while common stock does. With preferred shares, investors are usually garanted a fixed dividend.
    
    c. Last Dividend - Annual dividend per share.
    
    d. Fixed Dividend - For preferred stocks only.
    
    e. Par value - Par can refer to bonds, preferred stocks, common stocks or currencies, with different meanings depending on the context. Par most commonly refers to bonds, in which case it means the face value, or value at which bond will be redeemed at maturity.

Asumptions : The stock symbol is unique in dataset. One stock symbol will have only one row in the given dataset.

"""

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
