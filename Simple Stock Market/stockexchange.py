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

# Importing required libraries.

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys

pythonversion = float('{}.{}'.format(sys.version_info[0],sys.version_info[1]))

if pythonversion < 3.7:
	#Ordered dict is only required to be enabled for python 3.6 and below.
	#for python 3.7 and above, dictionary remembers the position of the keys as inserted
	print('Python version is: ',pythonversion)
	from collections import OrderedDict

# StockMarket class declaration
	
class StockMarket():
	
	def __init__(self, stock_market_data):

		self.stock_market_df = pd.DataFrame(stock_market_data)		
		self.stock_market_df['Stock Symbol'] = self.stock_market_df['Stock Symbol'].str.upper()
		self.stock_market_df['Type'] = self.stock_market_df['Type'].str.upper()
		
		print('Current Dataset to be used: ')
		print(self.stock_market_df.head())
		
		self.trade_df = pd.DataFrame(columns=['Stock Symbol', 'Timestamp', 'Quantity', 'BSIndicator','Trade Price'])
		self.vwsp_dict = {}
	
	def dividend_yield(self, stock_symbol, price):
	
		try:
			# Single stock data
			stock_symobol_df = self.stock_market_df[self.stock_market_df['Stock Symbol'] == stock_symbol]
			
			if stock_symobol_df.empty:
				raise StockSymbolNotPresent
			
			stock_symobol_type = list(stock_symobol_df['Type'])[0]				# Holds stock type
			stock_symobol_ldiv = list(stock_symobol_df['Last Dividend'])[0]		# Holds last dividend value
			stock_symobol_fdiv = list(stock_symobol_df['Fixed Dividend'])[0]	# Holds fixed dividend value
			stock_symobol_pv = list(stock_symobol_df['Par Value'])[0]			# Holds Par value of the stock.
			
			if stock_symobol_type == 'COMMON':
				return stock_symobol_ldiv / price
				
			elif (stock_symobol_type == 'PREFERRED'):
			
				if stock_symobol_fdiv is not None:
					return ((float(stock_symobol_fdiv.strip('%'))/100) * stock_symobol_pv) / price
				else:
					raise FixedDividendNotDefined
			else:
				raise NoFormulaPresentForNewType
		
		except FixedDividendNotDefined:
			print('Fixed dividend is not defined for the preferred stocks')
		except NoFormulaPresentForNewType:
			print('Stock Type other than Common or Preferred is not handled here.')
		except StockSymbolNotPresent:
			print('Stock Symbol is not present in the data.')
			
	def pe_ratio(self, stock_symbol, price):
		return self.dividend_yield(stock_symbol, price) / price
	
	def RecordTrade(self, stock_symbol, quantity, bs, trade_price, trade_time=None):
		
		if trade_time is None:
			trade_time = datetime.now()
			
		stock_market_trade={}
		stock_market_trade['Stock Symbol'] = stock_symbol
		stock_market_trade['Timestamp'] = trade_time
		stock_market_trade['Quantity'] = quantity
		stock_market_trade['BSIndicator']=bs
		stock_market_trade['Trade Price'] = trade_price
		
		self.trade_df = self.trade_df.append(stock_market_trade, ignore_index=True)
	
	def stocks_vwsp(self, stock_symbols):
		
		try:
			end_time = datetime.now()
				
			start_time = end_time - timedelta(minutes=5)
				
			for stock_symbol in stock_symbols:
				
				trade_df_5mins = self.trade_df[self.trade_df['Stock Symbol']==stock_symbol].copy()
				
				trade_df_5mins['Timestamp'] = pd.to_datetime(trade_df_5mins['Timestamp'])
				
				trade_df_5mins.set_index('Timestamp', inplace=True)
				
				trade_df_5mins = trade_df_5mins[start_time:end_time]
				
				trade_df_5mins['TradePrice * Quantity'] = trade_df_5mins['Trade Price'] * trade_df_5mins['Quantity']
				
				vwsp = trade_df_5mins['TradePrice * Quantity'].sum() / trade_df_5mins['Quantity'].sum()
				
				self.vwsp_dict[stock_symbol] = vwsp
				
		except Exception as e:
			
			print(sys.exc_info())
			
	def AllShareIndex(self):
	
		noofstocks = len(self.vwsp_dict)
		if noofstocks == 0:
			asi = 0
		
		else:
			asi = np.power(np.prod(list(self.vwsp_dict.values())), (1/noofstocks))
		
		return asi

class CustomExceptions(Exception):
	pass

class FixedDividendNotDefined(CustomExceptions):
	pass
	
class NoFormulaPresentForNewType(CustomExceptions):
	pass

class StockSymbolNotPresent(CustomExceptions):
	pass
	
if __name__ == "__main__":
	
	#Setting up of data given in the assignment
	stock_market_data = {"Stock Symbol":['TEA', 'POP','ALE', 'GIN', 'JOE'], "Type":['Common', 'Common', 'Common', 'Preferred', 'Common'], "Last Dividend":[0, 8, 23, 8, 13], "Fixed Dividend":[None, None, None, '2%', None], "Par Value":[100, 100, 60, 100, 250]}

	# if python version is less than 3.7, then ordered dict is used to make sure the input data set in correct order.
	if pythonversion < 3.7:
		stock_market_data = OrderedDict(stock_market_data)

	# for testing
	stock_symbol = 'TEA'
	stock_price = 100

	# Calling stock market class
	sm = StockMarket(stock_market_data)

	# Calculating dividend yield.
	dy = sm.dividend_yield(stock_symbol, stock_price)
	print('Dividend Yield of {}: '.format(stock_symbol),dy)

	# Calculating P/E Ratio.
	pe = sm.pe_ratio(stock_symbol, stock_price)
	print('P/E Ratio of {}: '.format(stock_symbol),pe)

	# Recording trades for various stocks.
	# Send trade data as sm.RecordTrade(stock symbol, quantity, buy sell indicator, trade price, trade time)
	# Trade time will be taken as current time, if not sent.

	sm.RecordTrade('TEA', 1, 'B', 100, '2019-09-14 17:33:10.790865')
	sm.RecordTrade('TEA', 1, 'B', 101)
	sm.RecordTrade('TEA', 1, 'B', 90)
	sm.RecordTrade('TEA', 1, 'B', 110)

	sm.RecordTrade('POP', 1, 'B', 10, '2019-09-14 17:33:10.790865')
	sm.RecordTrade('POP', 1, 'B', 5)
	sm.RecordTrade('POP', 1, 'B', 6)
	sm.RecordTrade('POP', 1, 'B', 11)

	sm.RecordTrade('ALE', 1, 'B', 3000, '2019-09-14 17:33:10.790865')
	sm.RecordTrade('ALE', 1, 'B', 2999)
	sm.RecordTrade('ALE', 1, 'B', 3100)
	sm.RecordTrade('ALE', 1, 'B', 2980)

	print('Trades done:\n',sm.trade_df)

	#Calculating volume weighted stock price of trading
	sm.stocks_vwsp(sm.trade_df['Stock Symbol'].unique())
	print('Volume Weighted Stock Price: ', sm.vwsp_dict)

	#GBCE All share index
	asi = sm.AllShareIndex()
	print('GBCE All Share Index: ', asi)