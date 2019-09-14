'''
Author - Jaideep Singh

Problem: Super simple stock market

Requirements: 
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

Asumptions : The stock symbol is unique in dataset.

'''

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys

python_version = float('{}.{}'.format(sys.version_info[0],sys.version_info[1]))

if python_version < 3.7:
	#Ordered dict is only required to be enabled for python 3.6 and below.
	#for python 3.7 and above, dictionary remembers the position of the keys as inserted
	print('Python version is: ',python_version)
	from collections import OrderedDict
	
class stock_market():
	
	def __init__(self, stock_market_data):

		self.stock_market_df = pd.DataFrame(stock_market_data)		
		self.stock_market_df['Stock Symbol'] = self.stock_market_df['Stock Symbol'].str.upper()
		self.stock_market_df['Type'] = self.stock_market_df['Type'].str.upper()
		
		print('Current Dataset to be used: ')
		print(self.stock_market_df.head())
		
		self.trade_df= pd.DataFrame(columns=['Stock Symbol', 'Timestamp', 'Quantity', 'bsIndicator','Trade Price'])
		self.vwsp_list= []
	
	def dividend_yield(self, stock_symbol, price):
	
		try:
		
			'''		
			self.stock_market_df['Stock Price']=np.where(self.stock_market_df['Stock Symbol']=='TEA', price, None)
			#stock_market_df['Stock Price']=[price if x == stock_symbol else None for x in stock_market_df['Stock Symbol']]
			
			self.stock_market_df['Dividend Yield']=np.where(self.stock_market_df['Stock Symbol']==stock_symbol, np.where(self.stock_market_df['Type']=='Common', self.stock_market_df['Last Dividend'] / self.stock_market_df['Stock Price'], ((float(self.stock_market_df['Fixed Dividend'].strip('%'))/100) * self.stock_market_df['Par Value']) / price), None)
			
			print(self.stock_market_df)
			
			#stock_market_df['Dividend Yield']=[(stock_market_df['Last Dividend'] / price) if (x == stock_symbol & stock_market_df['Last Dividend']=='Common')else None for x in stock_market_df['Stock Symbol']]
			
			'''
			
			stock_symobol_df = self.stock_market_df[self.stock_market_df['Stock Symbol'] == stock_symbol]
			
			if stock_symobol_df.empty:
				raise StockSymbolNotPresent
			
			stock_symobol_type = list(stock_symobol_df['Type'])[0]
			stock_symobol_ldiv = list(stock_symobol_df['Last Dividend'])[0]
			stock_symobol_fdiv = list(stock_symobol_df['Fixed Dividend'])[0]
			stock_symobol_pv = list(stock_symobol_df['Par Value'])[0]
			
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
			#logging.FATAL('Stock Type other than Common or Preferred is not handled here.')
			print('Stock Type other than Common or Preferred is not handled here.')
		except StockSymbolNotPresent:
			print('Stock Symbol is not present in the data.')
			
	def pe_ratio(self, stock_symbol, price):
		return self.dividend_yield(stock_symbol, price) / price
	
	def RecordTrade(self, stock_symbol, quantity, bs, price, tradetime=None):
		
		if tradetime is None:
			start_time = datetime.now()
		else:
			start_time = tradetime
			
		stock_market_trade={}
		stock_market_trade['Stock Symbol'] = stock_symbol
		stock_market_trade['Timestamp'] = start_time
		stock_market_trade['Quantity'] = quantity
		stock_market_trade['bsIndicator']=bs
		stock_market_trade['Trade Price'] = price
		
		#print(stock_market_trade)
		
		self.trade_df = self.trade_df.append(stock_market_trade, ignore_index=True)
		
		#print(self.trade_df)
		
		return self.trade_df
	
	def vwstocks(self, stock_symbols):
		
		stock_symbols = list(stock_symbols)
		
		end_time = datetime.now()
			
		start_time = end_time - timedelta(minutes=5)
			
		for stock_symbol in stock_symbols:
			
			trade_df_5mins = pd.DataFrame()
			
			trade_df_5mins = self.trade_df[self.trade_df['Stock Symbol']==stock_symbol]
			
			trade_df_5mins['Timestamp'] = pd.to_datetime(trade_df_5mins['Timestamp'])
			trade_df_5mins.set_index('Timestamp', inplace=True)
			
			#print('Start Time: ',start_time)
			#print('End Time: ', end_time)
			
			trade_df_5mins = trade_df_5mins[start_time:end_time]
			
			#print(trade_df_5mins)
			
			trade_df_5mins['TradePrice * Quantity'] = trade_df_5mins['Trade Price'] * trade_df_5mins['Quantity']
			
			#print(trade_df_5mins)
			
			vwsp = trade_df_5mins['TradePrice * Quantity'].sum() / trade_df_5mins['Quantity'].sum()
			
			#print('vwsp for {}: '.format(stock_symbol),vwsp)
			
			self.vwsp_list.append(vwsp)
		
		#print(self.vwsp_list)
		
		return self.vwsp_list
	
	def AllShareIndex(self):
		cnt = len(self.vwsp_list)
		vwsp_prod = np.prod(self.vwsp_list)
		asi = np.power(vwsp_prod, (1/cnt))
		return asi

class CustomExceptions(Exception):
	pass

class FixedDividendNotDefined(CustomExceptions):
	pass
	
class NoFormulaPresentForNewType(CustomExceptions):
	pass

class StockSymbolNotPresent(CustomExceptions):
	pass

#Setting up of data given in the assignment
stock_market_data = {"Stock Symbol":['TEA', 'POP','ALE', 'GIN', 'JOE'], "Type":['Common', 'Common', 'Common', 'Preferred', 'Common'], "Last Dividend":[0, 8, 23, 8, 13], "Fixed Dividend":[None, None, None, '2%', None], "Par Value":[100, 100, 60, 100, 250]}

if python_version < 3.7:
	stock_market_data = OrderedDict(stock_market_data)

stock_symbol = 'TEA'
trade_price = 100

# Calling stock market class
sm = stock_market(stock_market_data)

# Calculating dividend yield.
dy = sm.dividend_yield(stock_symbol, trade_price)
print('Dividend Yield of {}: '.format(stock_symbol),dy)

# Calculating P/E Ratio.
pe = sm.pe_ratio(stock_symbol, trade_price)
print('P/E Ratio of {}: '.format(stock_symbol),pe)

# Recordin trades for various stocks.
rt = sm.RecordTrade('TEA', 1, 'S', 100, '2019-09-14 17:33:10.790865')
rt = sm.RecordTrade('TEA', 1, 'S', 101)
rt = sm.RecordTrade('TEA', 1, 'S', 90)
rt = sm.RecordTrade('TEA', 1, 'S', 110)

rt = sm.RecordTrade('POP', 1, 'S', 10, '2019-09-14 17:33:10.790865')
rt = sm.RecordTrade('POP', 1, 'S', 5)
rt = sm.RecordTrade('POP', 1, 'S', 6)
rt = sm.RecordTrade('POP', 1, 'S', 11)

rt = sm.RecordTrade('ALE', 1, 'S', 3000, '2019-09-14 17:33:10.790865')
rt = sm.RecordTrade('ALE', 1, 'S', 2999)
rt = sm.RecordTrade('ALE', 1, 'S', 3100)
rt = sm.RecordTrade('ALE', 1, 'S', 2980)

print('Trades done:\n',rt)

#Calculating volume weighted stock price of trading
vw = sm.vwstocks(rt['Stock Symbol'].unique())
print('Volume Weighted Stock Price: ', vw)

#GBCE All share index
asi = sm.AllShareIndex()
print('GBCE All Share Index: ', asi)