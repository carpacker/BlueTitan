import sys
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Crypto-API/Exchange_APIs')
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Crypto-API/Main')
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Database-RD')
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Arbitrage')

from Helpers import DatabaseHelpers
from API import ExchangeAPI
import time

class AccountBalancing(object):

	# FUNCTION: to be used to flatten accounts in times of transition
	def ethBalance():
		pass
		
	# Currently looking to fix the main passthrough
	def account_balancing(self, input_tuple):  
		# Store input_tuple in local variables
		pairing, sell_exchange, buy_exchange, sell_balance_base, sell_balance_quote, buy_balance_base, buy_balance_quote = input_tuple
		allocated_quantity = sell_balance_base + buy_balance_base + Helpers.btcValue(sell_balance_quote) + Helpers.btcValue(buy_balance_quote)
		print("Sell balances [base quote], buy balances [base quote]", sell_balance_base, sell_balance_quote, buy_balance_base, buy_balance_quote)
		print("Allocated Quantity", allocated_quantity)

		# Variable represents the quote/base bias for an exchange
		equilibrium_proportion = 0.8
		current_proportion = Helpers.assessProportion(sell_balance_base, sell_balance_quote, buy_balance_base, buy_balance_quote, equilibrium_proportion)
		proportion_rate = current_proportion / equilibrium_proportion

		print("current_proportion, equilibrium_proportion, proportion_rate: ", current_proportion, equilibrium_proportion, proportion_rate)
		if proportion_rate < 0.25:
			# Send BITCOIN from SELL ex to BUY ex
			quantity_base_sb = (equilibrium_proportion * allocated_quantity) - buy_balance_base
			print ("Quantity Base: ", quantity_base)
			# Send QUOTE from BUY ex to SELL ex
			quantity_quote_bs = (equilibrium_proportion * allocated_quantity) - sell_balance_quote
			print("Quantity Quote: ", quantity_quote)

			# Record keeping
			quantity_quote_sb = 0
			quantity_base_bs = 0

		self.balanceAccounts(pairing, quantity_base, quantity_quote, sell_exchange, buy_exchange)

		intended_result = (buy_exchange, buy_exchange, sell_balance_base, sell_balance_quote, buy_balance_base, buy_balance_quote)
		return result

	def initializeBalances(asset_list, exchange_list):
		pass
		# Basically, given a list of
		# [{asset : {current_balance : 0, goal_balance : 0}}...]

		# for each exchange: 
		# part one: determine important coins (BTC, ETH)
		# part two: sell coins that are above current balance (btc exempt pretty much)
		# part three: use BTC to buy up to buy coins
		# part four: optimization, incase its not perfect
		# part five: cancel/rebuy if orders didnt fill (do 2X before returning error)
		# part six: return filled balances, unfilled balances in concise list

	# FUNCTION: balanceAccounts
	# INPUTS: pairing - string
	#		  quantity_base - float
	#		  quantity_quote - float
	#		  sell_exchange - string
	#		  buy_exchange  - string
	# OUTPUT: list of withdrawal information
	# DESCRIPTION:
	#	TODO
	def balanceAccounts(self, pairing, quantity_base, quantity_quote, sell_exchange, buy_exchange):

		# Transfer quote, base, store results
		withdraw_two = transferBase(base_asset, quantity_base, sell_exchange, buy_exchange)
		withdraw_one = transferQuote(quote_asset, quantity_quote, buy_exchange, sell_exchange)
		print("Withdraw tuple: ", withdraw_one, withdraw_two)

		# Store withdraw FEEs, CURRENCY, EXCHANGES as a message to be based on later
		# * Start a timer thing to track how long a transactoin takes
		withdraw_list = [withdraw_quote, withdraw_base]

		# STORE RESULTS IN DATABASE (finished parameter to be updated)
		DatabaseHelpers.storeTransfer(withdraw_list)
		return withdraw_list

	# FUNCTION: transferQuote
	# INPUT: asset 		 	- string
	#        quantity 		- string
	#        from_exchange 	- string
	#        to_exchange	- string
	# OUTPUT: dictionary
	# DESCRIPTION:
	#	Function used to transfer quote asset from exchange to exchange and store
	#	 relevant information in order to pass on to listener
	def transferQuote(asset, quantity, from_exchange, to_exchange):
		print(asset)
		print(quantity)
		withdraw_dict = AccountBalancing.withdraw(from_exchange, to_exchange, asset, quantity)
		return withdraw_dict

	# FUNCTION: transferBase
	# INPUT: base_asset - string
	#		 quantity   - float
	#		 from_exchange - string
	#		 to_exchange - string
	# OUTPUT: tuple containing withdraw information
	# DESCRIPTION:
	#	Function used to transfer quote asset from exchange to exchange and store
	#	 relevant information in order to pass on to listener
	def transferBase(base_asset, quantity, from_exchange, to_exchange):
		xfer_asset_tuple = AccountBalancing.decideXferAsset(base_asset, quantity, from_exchange, to_exchange)
		buy_info = AccountBalancing.buyXferAsset(from_exchange, xfer_asset_tuple)
		print(xfer_asset_tuple)

		# Simple error handling for time being
		ticker = 0
		while buy_info == -1:
			ticker += 1
			print("BUY WAS NOT SUCCESSFUL:: TRYING AGAIN IN 10 SECONDS")
			time.sleep(10)
			buy_info = AccountBalancing.buyXferAsset(from_exchange, xfer_asset_tuple)
			if ticker == 10:
				print ("ERROR :: BUYING NOT SUCCESSFUL AFTER 10 ATTEMPT")
				return -1

		print(buy_info)
		time.sleep(60)
		withdraw_dict = AccountBalancing.withdraw(from_exchange, to_exchange, buy_info[0], buy_info[0])
		return withdraw_dict

	# FUNCTION: buyXferAsset
	# INPUT:  from_exchange - string
	#         xfer_asset_tuple - tuple
	# OUTPUT: dictionary containing buy information
	# DESCRIPTION:
	#	Function used to buy the designated transfer asset
	def buyXferAsset(from_exchange, xfer_asset_tuple):
		# Grab the price
		asset = xfer_asset_tuple[0]    # <---  LTC 
		buy_rate = xfer_asset_tuple[1] # <---  buying price
		quantity = xfer_asset_tuple[3] # <---  buys (buying quantity)

		print("Buy XFER asset")
		return -1
		# buy_dict = ExchangeAPI.buyLimit(from_exchange, asset, quantity, buy_rate)
		if buy_dict["success"] == False:
			# Need to do error handling 
			return -1

		return buy_dict

	# FUNCTION: decideXferAsset
	# INPUT: base_asset
	#		 quantity
	#		 from_exchange
	#		 to_exchange
	# OUTPUT: tuple of:
	#(transfer_asset, exchange_one_prices, exchange_two_prices, buys, sells)
	# DESCRIPTION:
	#	Decide which transfer asset to use
	'''
	This function determines what the best transfer asset is to use
	it also checks through bids and asks lists on each exchange, and finds
	the quantities and prices at which to buy and sell the transfer asset

	The function will return a transfer asset as a string
	as well as a list for each exchange, containing the quantity and price pairs
	for the buys and the sells that can be done
	The function will also return how much can actually be bought, and how much can be sold
	'''
	def decideXferAsset(base_asset, quantity, from_exchange, to_exchange):
		transfer_asset = 'XRP'
		exchange_one_prices = []
		exchange_two_prices = []
		place = 0
		quantBuy = quantity
		quantSell = quantity
		buys = quantity
		sells = quantity

		# asset pair will be in BASE-TRAN format
		assetPair = base_asset + '-' + transfer_asset
		# Check the ask price of transfer assets on one exchange
		XferJson1 = ExchangeAPI.getOrderbook(from_exchange, assetPair)
		lenAsks = len(XferJson1['asks'])

		while place < lenAsks:
			exchange_one_price = float(XferJson1['asks'][place][0])
			exchange_one_quantity = float(XferJson1['asks'][place][1])
			print(quantBuy)
			print(exchange_one_quantity)
			if quantBuy <= exchange_one_quantity:
				addTuple = (exchange_one_price, quantBuy)
				exchange_one_prices.append(addTuple)
				quantBuy = 0
			else:
				addTuple = (exchange_one_price, exchange_one_quantity)
				exchange_one_prices.append(addTuple)
				quantBuy -= exchange_one_quantity

			if quantBuy <= 0:
				break

			place += 1

		# REVISIT
		if place >= lenAsks:
			quantSell = quantity - quantBuy
			buys = quantSell

		XferJson2 = ExchangeAPI.getOrderbook(to_exchange, assetPair)
		lenBids = len(XferJson1['bids'])
		place = 0

		# Check the buy pricea of transfer assets on another exchange
		while place < lenBids:
			exchange_two_price = float(XferJson2['bids'][place][0])
			exchange_two_quantity = float(XferJson2['bids'][place][1])
			if quantSell <= exchange_two_quantity:
				addTuple = (exchange_two_price, quantSell)
				exchange_two_prices.append(addTuple)
				quantSell = 0
			else:
				addTuple = (exchange_two_price, exchange_two_quantity)
				exchange_two_prices.append(addTuple)
				quantSell -= exchange_two_quantity
			if quantSell <= 0:
				break
			place += 1

		# REVISIT
		if place >= lenBids:
			sells = buys - quantSell

		retTuple = (transfer_asset, exchange_one_prices, exchange_two_prices, buys, sells)
		print("decideXfer", retTuple)
		return retTuple


	# FUNCTION: Withdraw
	#	Wrapper, calls API withdraw, checks withdrawal tag shit
	def withdraw(from_exchange, to_exchange, asset, quantity):
		tag_assets = ["XMR", "XRP"]
		# 2. if withdrawal tag, get withdrawal tag
		# 3. Withdraw, return output
		address = DatabaseHelpers.getDepositAddress(asset, to_exchange)
		print(address)
		for tag_asset in tag_assets:
			if tag_asset == asset:
				tag = DatabaseHelpers.getWithdrawalTag(asset, to_exchange)
				print(tag)
				time.sleep(30)
				withdraw_info = ExchangeAPI.withdraw(from_exchange, asset, quantity, address, tag)
				return withdraw_info

		print("no tag for", asset)
		time.sleep(30)
		withdraw_info = ExchangeAPI.withdraw(from_exchange, quantity, asset, address)
		return withdraw_info
