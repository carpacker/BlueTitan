import sys

# External-Imports
import time
import numpy

# Internal-Imports
from API import ExchangeAPI
from TradeLibrary import TradeLibrary
import Helpers

# MedianMain.py
# DESCRIPTION:
# 	This script provides the top level functionality for the median-trading bot component. The purpose of this program is to 
#	 automatically trade around the median point of a price for a given asset over given intervals. 

# FUNCTION: createTrade
# INPUT: pairing 	- string
#		 exchange 	- string
#		 period     - int (terms of MINUTES)
#		 median 	- float
#		 volatility - float
#		 balances   - dictionary
# OUTPUT:
# DESCRIPTION:
#	One of the main functions used to create a 'trade' for median trading. A trade generally comprises of two 
#	 orders that are intended to be filled in on period of time, if possible.
def createTrade(pairing, exchange, period, median, volatility, balances):

	if period == 1:

		# 1. Set buy, sell price
		buy_price = calculateBuyPrice(median, period, volatility)
		sell_price = calculateSellPrice(median, period, volatility)
		PrintLibrary.displayVariables(median, period, volatility, buy_price, sell_price)

		# 2. Set betsize
		betsize = calculateBetsize(pairing, exchange, volatility, balances, period)
		PrintLibrary.displayVariables(betsize)

		# 3. Set orders
		buy_order = ExchangeAPI.buyLimit(exchange, pairing, betsize, buy_price)
		sell_order = ExchangeAPI.sellLimit(exchange, pairing, betsize, sell_price)
		print("Buy Order", buy_order)
		print("Sell Order", sell_order)


		# For now, this will do
		median_trade = {"buy" : buy_order,
						"sell" : sell_order}

		# 4. Set expiration, uuid				
		median_trade["expiration"] = setExpiraton()
		median_trade["uuid"] = Helpers.createUUID()

		print(median_trade)
		# For now, instead of using global list (unsure of how to do so properly), perform through 
		#	database
		DatabaseLibrary.storeInitMedianT(median_trade)

		return median_trade

# FUNCTION: calculateBuyPrice
# INPUT: median - float
#		 scale  - int
# OUTPUT: float
# DESCRIPTION: 
#	Outputs a 'buy price' based on a given median price and the intended scale. Scale will be some integer
#	 which determines how wide of a swing there will be from median price
def calculateBuyPrice(median, scale):
	# For now, use IF statements based on scale
	if scale == 1:
		pass
	elif scale == 2:
		pass
	elif scale == 3:
		pass
	elif scale == 4:
		pass
	elif scale ==5:
		pass
	else:
		return -1

# FUNCTION: calculateSellPrice
# INPUT: median - float
#		 scale  - int
# OUTPUT: float
# DESCRIPTION:
#	Outputs a 'sell price' based on a given median price and the intended scale. Scale will be some integer
#	 which determines how wide of a swing there will be from median price
def calculateSellPrice(median, scale):
	# For now, use IF statements based on scale
	if scale == 1:
		pass
	elif scale == 2:
		pass
	elif scale == 3:
		pass
	elif scale == 4:
		pass
	elif scale == 5:
		pass
	else:
		return -1
	
# FUNCTION: calculateBetsize
# INPUT: quantity	  - float
#		 profit_ratio - float (OPTIONAL) [DEFAULT=.25]
# OUTPUT: float
# DESCRIPTION:
#	Used to set a specific size for a trade. Note that quantity is the TOTAL value available in terms of BTC. 
#	 The value must be converted back to asset ouside of the trade
def calculateBetsize(quantity, profit_ratio=.25):

	# Scaled sizing based on profit ratio
	if profit_ratio <= .1:
		betsize = quantity * .01
	elif profit_ratio <= .25:
		betsize = quantity * .02
	elif profit_ratio <= .5:
		betsize = quantity * .04
	elif profit_ratio <= 1:
		betsize = quantity * .08
	elif profit_ratio <= 2:
		betsize = quantity * .1

	# - Check minimum order size (will require porting ArbitrageLibrary to TradeLibrary)
	return betsize

# FUNCTION: setExpiration
# INPUT: period - int
#		 scale  - int
# OUTPUT: int
# DESCRIPTION:
# 	Sets the expiration date for a given (newly created) trade.
def setExpiration(period, scale):

	# Expiration is in terms of MINUTES
	if period == 1:
		expiration = 5 * scale
		return expiration
	elif period == 2:
		expiration = 30 * scale
		return expiration
	elif period == 3:
		expiration = 120 * scale
		return expiration
	else:
		print("not a valid period")
		return -1

	return trade

# FUNCTION: checkExpiration
# DESCRIPTION:
#	Used to check the expiration on a trade
def checkExpiration(trade):
	expiration = trade["expiration"]
	date_bool = expiration > time.time()
	# Check if date is past current date [TODO]
	return date_bool

# FUNCTION: handleExpiredTrade
# DESCRIPTION:
# 	Main function for handling an expired trade
def handleExpiredTrade():
	pass

# TOP LEVEL: medianTrading
# 	This is the main loop for the median trading algorithm
def medianTrading(pairing):
	
	# Initialization
	long_period = 3
	medium_period = 2
	short_period = 1
	trade_list = []

	# Initialize Database stuff (balances, metrics) --> TODO

	while 1:
		# --------------------------------- Check fills ---------------------------------
		# 1. Check if trades with no fills have seen one or two fills
		for median_trade in trade_list:
			
			# result = ExchangeAPI.getOrder(exchange, order_id)
			# expiration = checkExpiration(median_trade)

			# Case One: the order hasn't filled
			if result[0] == 0:
				if expiration == True:
					cancelOrders(median_trade)
				continue

			# Case Two: Both orders have filled (success)
			if result[0] == 2:
				# DONE: calculate profits and store results
				derivative_tuple = calculateDerivatives(result)
				storeTrade(result, derivative_tuple)

			# Case Three: One order has filled (handle second part of trade)
			if result[0] == 1:
				pass
				# Maybe try to arbitrage... (?)
				# Assess the original pair order
				# Assess the volatility and direction in the current period
				# Update the matchup order 

			# ALL DONE CHECKING NO ORDERS

		# --------------------------------- Create Orders ---------------------------------
		# A. Long period median orders
		median = setMedian(long_period)
		volatility = setVolatility(long_period)
		trade_list.append(createOrders(period, median, volatility, balances)) 
		# POTENTIALLY STORE ATTEMPT IN DATABASE 

		# B. Medium period median orders
		median = setMedian(medium_period)
		volatility = setVolatility(medium_period)
		trade_list.append(createOrders(medium_period, median, volatility, balances))

		# C. Short period median orders		
		median = setMedian(short_period)
		volatility = setVolatility(short_period)
		trade_list.append(createOrders(short_period, median, volatility, balances))

# FUNCTION: cancelExpired
# INPUT: 
# OUTPUT:
# DESCRIPTION:
# 	Cancels an expired trade using uuid
def cancelExpired(uuid):
	# Either use built in uuid to reference the actual uuid for an exchange, or do the exchange shit in higher level
	# Probably use uuid to find actual uuid to cancel, don't call exchangeAPI directly yet.
	pass

#									SUPPORTING / DATA FUNCTIONS
# FUNCTION: setMedian
# INPUT: period  - int (hours)
#		 pairing - string
# OUTPUT: float
# DESCRIPTION:
#	Evaluate a pairing over the past period of time and output an estimated median
def setMedian(pairing, period):
	# 1. Check moving averages for periods (???)
	# TODO, figure out what exactly to do here
	pass

# FUNCTION: calculateMovingAverage
# INPUT: period - float (hours)
# OUTPUT: float
# DESCRIPTION:
#	Given an input set of data, returns the moving average
def calculateMA1(data, period):
	cumulative_sum, moving_aves = [0], []

	for i, x in enumerate(data, 1):
	    cumulative_sum.append(cumulative_sum[i-1] + x)
	    if i>=period:
	        moving_ave = (cumulative_sum[i] - cumulative_sum[i-period])/period
	        moving_aves.append(moving_ave)

	return moving_aves

def calculateMA2(data, period):
	cumulative_sum = numpy.cumsum(numpy.insert(data, 0, 0))
	return (cumulative_sum[period:] - cumulative_sum[:-period]) / float(period)


if __name__ == '__main__':
	print(calculateMA2([5.5, 5.67, 5.54, 5.44, 5.3, 5.22], 6))