import sys
sys.path.append('C:/C-directory/Projects/Work-i/Components/Crypto-API/Exchange_APIs')
sys.path.append('C:/C-directory/Projects/Work-i/Components/Crypto-API/Main')
sys.path.append('C:/C-directory/Projects/Work-i/Components/Database-Manager')
sys.path.append('C:/C-directory/Projects/Work-i/Bots/Arbitrage/Information_accounting')
sys.path.append('C:/C-directory/Projects/Work-i/Bots/Arbitrage/Libraries')
sys.path.append('C:/C-directory/Projects/Work-i/Bots/Arbitrage/Scripts')

# External-Imports
import time

# Internal-Imports
from DatabaseLibrary import DatabaseLibrary
from API import ExchangeAPI
import Helpers
from PrintLibrary import PrintLibrary

# FUNCTION: sortAlphabetically 
# INPUT: fae - list [asset, exchange, ...]
# OUTPUT: sorted list
# DESCRIPTION:
#	Performs a nested alphabetical sorted (inside first, then outside). Intended purpose is to sort by [asset, exchange] 
#	 alphabetically, it sorts by exchange first then by asset.
def sortAlphabetically(fae):
	def getKey(item):
		return item[0]
	def getKey2(item):
		return item[1]

	return sorted(sorted(fae, key=getKey), key=getKey2)

# FUNCTION: convertAssetDict
# INPUT: balances - dictionary
# OUTPUT: dictionary
# DESCRIPTION:
#	Converts a balances exchange-key dictionary to a dictionary with ASSET as outer key instead. In general, flips the 
#	 dictionary (future will re-name function).
# TODO - move to helpers, rename invert nested dict
def convertAssetDict(balances):
	asset_dict = {}
	for exchange in balances:
		for asset in balances[exchange]:
			asset_dict[asset] = {}

	return asset_dict

# CLASS: BalancingLibrary
# FUNCTION LIST: [balanceAccounts, balancePairing]
# DESCRIPTION:
#   Library of functions that represents the set of primary operations used in the account 
# 	 balancing component.
class BalancingLibrary(object):

	# FUNCTION: balanceAccounts
	# INPUT:  asset            - string
	#		  changed_balances - TBD
	# OUTPUT: withdraw information
	# DESCRIPTION:
	#	Performs a balance over a specifical fae pairing if the proper requirements are met.
	def balanceFAE(arbitrage_tuple):
		asset = arbitrage_tuple[0] 
		exchange = arbitrage_tuple[1]

		# Turn changed_balances into FAE
		# * TODO

		# Retrieve the intended_fae for the given asset/exchanges
		intended_fae = BalancingLibrary.retrieveIntendedFAE(asset, exchange)

		# Make sure balancing would be profitable
		balance_bool = BalancingLibrary.checkProfitability(asset, current_fae, intended_fae)

		# Check if any balances have returned
		if balance_bool:

			withdraw_info = BalancingLibrary.balancePairing(pairing, quantity_base, quantity_quote, sell_exchange, buy_exchange)

			# withdraw_info contains information that is used to later to determine when a 
			#  transfer is being tracked and so on.
			return withdraw_info
		else:
			# Don't balance, return nothing
			return 0

	# FUNCTION: balancePairing
	# INPUTS: pairing 		 - string
	#		  quantity_base  - float
	#		  quantity_quote - float
	#		  sell_exchange  - string
	#		  buy_exchange   - string


	# OUTPUT: list of withdrawal information
	# DESCRIPTION:
	#	Top level function involved in balancing the accounts after arbitrage.
	def balancePairing(pairing, quantity_base, quantity_quote, sell_exchange, buy_exchange):

		# Transfer quote, base, store results
		buy_withdraw = BalancingLibrary.transferQuote(quote_asset, quantity_quote, buy_exchange, sell_exchange)
		sell_withdraw = BalancingLibrary.transferBase(base_asset, quantity_base, sell_exchange, buy_exchange)
		print("Withdraw tuple: ", buy_withdraw, sell_withdraw)

		# Create withdraw list --> [timestamp, transfertime, buy_exchange, asset, amount,
		#							sell_exchange, base_t_asset, base_btc_value, total_btc,
		#							fee_btc, buy_withdraw_id, sell_withdraw_id] 
		withdraw_list = BalancingLibrary.buildWithdrawList(buy_withdraw, sell_withdraw)
		PrintLibrary.displayVariables(withdraw_list)

		DatabaseLibrary.storeTransferP1(withdraw_list)

		return withdraw_list

	# FUNCTION: balancePairings
	# INPUT: fae_list - [(asset, exchange, change in quantity[absolute terms]), ...]
	# OUTPUT: TODO
	# DESCRIPTION:
	#	Used to balance multiple pairings in one go, mainly to be used in initialize balances. The purpose is 
	#	 to reduce loss of profits through withdrawal fees by combining transfers of the base asset.
	def balancePairings(fae_list):
		print("Balancepairings Start // INPUT: ", fae_list)

		# 1. Sell assets that are overflowing
		temp_dict = {}
		ticker = 0
		remove_list = []
		for value in fae_list:
			asset = value[0]
			exchange = value[1]
			quantity_delta = value[2]

			# If the FAE is NEGATIVE (SURPLUS) and it is NOT bitcoin
			if quantity_delta < 0 and asset != "BTC":

				
				quantity = -quantity_delta
				pairing = Helpers.pairingStr(asset)
				rate = ExchangeAPI.getPrice(exchange, pairing)
				distance = 4

				print("A. [SELLING SURPLUS] Pairing, Quantity, Rate", pairing, quantity, rate)
				sell_dict = ExchangeAPI.sellLimitAbs(exchange, pairing, quantity, rate, distance)

				# If there was no error -> add to available btc
				if sell_dict["error"] == "":
					btc_value = sell_dict["btc_value"]
					print(" - BTC value AFTER trade", btc_value)
					try:
						temp_dict[exchange] = temp_dict[exchange] + btc_value
					except KeyError:
						temp_dict[exchange] = 0 + btc_value
				remove_list.append(ticker)
			elif asset == "BTC":
				remove_list.append(ticker)
				try:
					temp_dict[exchange] = temp_dict[exchange] + quantity_delta
				except KeyError:
					temp_dict[exchange] = 0 + quantity_delta				
			ticker += 1

		print("FIRST LOOP FINISHED | temp_dict: ", temp_dict)

		# Remove the items that we just sold
		fae_list = Helpers.removeItemsByIndex(fae_list, remove_list)		

		print("NEW fae_list with NEGATIVE values accounted for: ", fae_list)

		# Now, aggregate the AVAILABLE BTC for each exchange, and attempt to buy whatever needs to be bought until
		#	available < cost OR one has run out of items to buy. Remove these elements from the list.

		# Sort the fae_list so that it can be split into a Bittrex list and a Binance list.
		sorted_fae = sortAlphabetically(fae_list)
		lists_ex = Helpers.splitList(sorted_fae, 2)

		print("EXCHANGE lists as INPUTS to buy assets", lists_ex)

		# Loop that uses available BTC to buy assets until it runs out. One list will run out of items and the other
		#  will run out of BTC

		remainder_list = []
		for listy in lists_ex:
			exchange = listy[0][1]
			available_btc = temp_dict[exchange]
			ticker = 0
			remove_list = []
			print("0. AVAILABLE BTC on exchange", available_btc, listy[1][1])
			for fae in listy:
				asset = fae[0]
				quantity_delta = fae[2]

				cost = Helpers.btcValue(asset, quantity_delta, exchange)
				print("1. COST", cost)

				if available_btc >= cost:

					# Attempt to buy
					pairing = Helpers.pairingStr(asset)
					rate = ExchangeAPI.getPrice(exchange, pairing)
					quantity = cost / rate
					distance = 5

					print("2. RATE, PAIRING, QUANTITY", rate, pairing, quantity)

					buy_dict = ExchangeAPI.buyLimitAbs(exchange, pairing, quantity, rate, distance)
					available_btc = available_btc - buy_dict["btc_value"]

					# Record success
					remove_list.append(ticker)
					print("3. SUCCESSFUL BUY ", buy_dict["btc_value"], available_btc)
					print("-----------------------------------------")

				elif available_btc < cost:
					remove_list.append(ticker)
				else:
					# Rough cost up
					print("1. COST, AVAILABLE - before alteration: ", cost, available_btc)
					actual_cost = available_btc * .95
					print("2. AFTER alteration", actual_cost)

					# Buy whatever you can
					pairing = Helpers.pairingStr(asset)
					rate = ExchangeAPI.getPrice(exchange, pairing)
					quantity = cost / rate
					distance = 5

					print("3. RATE, PAIRING, QUANTITY", rate, pairing, quantity)	
					buy_dict = ExchangeAPI.buyLimitAbs(exchange, pairing, quantity, rate, distance)

					remove_list.append(ticker)
					# Record what is left to buy
					remainder_val = (cost - actual_cost) / rate
					remainder = (asset, exchange, remainder_val)
					print("4. Remainder tuple: ", remainder)

					# Remove successful buys
					print("Index list and fae list before removal: ", remove_list, listy)
					print("-----------------------------------------")					
					ticker = 0
					listy = Helpers.removeItemsByIndex(listy, remove_list)
					
					# Re-insert remainder after removing used items
					listy.insert(0, remainder)
					print("AFTER re-insertion", listy)
					break 
				ticker += 1

				# If we reached the end and still have BTC left over
				if ticker == len(listy):
					leftover_list = Helpers.removeItemsByIndex(listy, remove_list)
					print(available_btc, "leftover BTC")
					remainder = ("BTC", exchange, available_btc)
					remainder_list.append(remainder)
			print("Update available", temp_dict, available_btc, exchange)
			temp_dict[exchange] = available_btc

		# This should now be (probably) one empty list with remainder of some BTC value and one
		#  list with nothing left over and more things to buy
		print("ADAPTED list after buying assets with excess BTC", lists_ex)

		# Now we have all thats left to buy, and the excess BTC. Send BTC from the exchange that ran out of items to buy 
		#	(or ran out of BTC...?) to the other exchange. Other exchange then waits.

		# This is weird and/or doesn't work, might need to withdraw before something
		
		# 1. Detect which exchange still has excess
		sum_one = Helpers.sumFAE(lists_ex[0])
		sum_two = Helpers.sumFAE(lists_ex[1])
		print(lists_ex[0], sum_one, "SUM")
		print(lists_ex[1], sum_two, "SUM")

		print(temp_dict)

		# 2. Set variables to withdraw
		if sum_one == sum_two:
			for key in temp_dict:
				if temp_dict[key] < 0:
					print("negative value", temp_dict[key], key)
					exchange_to = Helpers.inverseExchange(key)
					exchange_from = key
					quantity_withdraw = -temp_dict[key]
				else:
					quantity_withdraw = 0
					exchange_from = ""
					exchange_to = ""
		else:
			# Case : There is more left to buy on one exchange
			if sum_one > sum_two:
				leftover_list = lists_ex[0][0][1]
				exchange_to = lists_ex[0][0][1]
				exchange_from = lists_ex[1][0][1]
				quantity_withdraw = sum_one * .98

			# Case : There is more left to buy on the other exchange
			else:
				leftover_list = lists_ex[1][0][1]
				exchange_to = lists_ex[1][0][1]
				exchange_from = lists_ex[0][0][1]
				quantity_withdraw = sum_two * .98

		print("ADJUST BTC_VALUE: ", quantity_withdraw)

		asset = "BTC"

		# 3. Withdraw to exchange
		print("WITHDRAWING quantity from EX1 to EX2", exchange_from, exchange_to, quantity_withdraw)
		print("withdraw portion")
		print(ExchangeAPI.getBalance(exchange_from, asset))

		withdraw_info = BalancingLibrary.withdraw(asset, quantity_withdraw, exchange_from, exchange_to)

		# Polling loop until funds have arrived
		funds_bool = BalancingLibrary.detectFundsArrived(withdraw_info, 60)

		# Funds have arrived! Do whatevers necessary to buy the rest. Account for errors.
		if funds_bool == True:
			# Continue to buy on the exchange that needed more
			print("LEFTOVER LIST", leftover_list)
			for value in leftover_list:
				asset = value[0]
				exchange = value[1]
				quantity = value[2]		
				pairing = Helpers.pairingStr(asset)
				rate = ExchangeAPI.getPrice(exchange, pairing)
				distance = 5

				print("BUYING LEFTOVER: RATE, PAIRING, QUANTITY", rate, pairing, quantity)
				buy_dict = ExchangeAPI.buyLimitAbs(exchange, pairing, quantity, rate, distance)
			
		# More than the alotted time has passed (for now, sixty minutes)
		else:
			raise Exception("ERROR: TRANSACTION OVER ALOTTED TIME")

		return -1

	# FUNCTION:	buildCurrentFAE
	# INPUT: balances     - dictionary
	#		 intended_fae - list
	# OUTPUT: [fae, ...]
	# DESCRIPTION:
	#	Builds a 'current FAE' list to be used in a comparison against the intended fae list. The idea is to create a list,	 based on 
	#	 the current balances, that can be compared against the intended FAE in order to initialize the balances.
	def buildCurrentFAE(balances, intended_fae):
		current_fae = []
		total_value_usd = balances["ALL"]["total_value_usd"]
		total_value_btc = balances["ALL"]["total_value_btc"]
		print("TOTAL BTC available: ", total_value_btc)
		if 'ALL' in balances: del balances['ALL']


		# Loop determines how much BTC and ASSET should be attributed to each
		#  currency. Need to test values that aren't flat
		intend_fae = []
		for value in intended_fae:
			total_attrib_btc = value[2] * total_value_btc
			btc_total = total_attrib_btc * value[3] / 2
			asset_total = total_attrib_btc * value[3] / 2
			intend_fae.append((value[0], value[1], btc_total, asset_total))		
		return intend_fae

	# WRAPPER: buildWithdrawList
	# INPUT: buy_withdraw  - dictionary
	#		 sell_withdraw - dictionary
	# OUTPUT: list
	# DESCRIPTION:
	#	Builds the necessary withdraw list to then be stored in the database from input withdraw dictionaries
	def buildWithdrawList(buy_withdraw, sell_withdraw):
		timestamp = Helpers.createTimestamp()

		# TODO - figure out transfer time
		transfer_time = 0

		# For now, use variables for readability, in the future, will just reference directly.
		#	compiler might deal with this inefficiency though.
		buy_exchange = buy_withdraw["exchange"]
		asset = buy_withdraw["asset"]
		amount = buy_withdraw["amount"]
		quote_btc_value = Helpers.btcValue(asset, amount)

		sell_exchange = sell_withdraw["exchange"]
		base_t_asset = sell_withdraw["asset"]
		base_btc_value = Helpers.btcValue(base_t_asset, sell_withdraw["amount"])

		# TODO - Either self-generated or we use theirs [maybe both, who knows]
		buy_withdraw_id = 0
		sell_withdraw_id = 0

		total_btc = quote_btc_value + base_btc_value

		fee_btc = BalancingLibrary.calculateFees(buy_withdraw, sell_withdraw)
		withdraw_list = [timestamp, transfer_time, buy_exchange, asset, amount, sell_exchange,
							base_t_asset, base_btc_value, total_btc, fee_btc, buy_withdraw_id, 
							sell_withdraw_id]

		return withdraw_list

	# FUNCTION: calculateFees
	# INPUT: buy_withdraw  - return dictionary from the first withdraw
	#		 sell_withdraw - return dictoinary from the second withdraw
	# OUTPUT: float
	# DESCRIPTION:
	#	Uses the withdraw information to obtain the aggregate fees for a balancing action and returns them.
	#	 The aggregate fees amount to the withdrawal fee for each transaction and the order fee (if appplicable)
	#	 for the 'sell' portion of a transaction [see transferBase].
	def calculateFees(buy_withdraw, sell_withdraw):
		sell_exchange = sell_withdraw["exchange"]
		buy_exchange = buy_withdraw["exchange"]

		transfer_asset = sell_exchange["asset"]
		quote_asset = buy_exchange["asset"]

		fee_one = DatabaseLibrary.getWithdrawalFee(sell_exchange, transfer_asset)
		fee_two = DatabaseLibrary.getWithdrawalFee(buy_exchange, quote_asset)
		fee_three = Helpers.calculateOrderFee(sell_exchange, sell_withdraw["btc_value"])

		fee = fee_one + fee_two + fee_three
		print(fee, "|", fee_one, "|", fee_two, "|", fee_three)
		return fee

	# FUNCTION: checkProfitability
	# INPUT:
	# OUTPUT: bool
	# DESCRIPTION:
	#	Function used to check whether or not its okay to balance the accounts yet. There must be a minimum
	#	 profit that must be reached before a balancing action's fees can be properly offset, this function
	#	 checks if the accounts have reached that threshold.
	def checkProfitability():
		pass

	# FUNCTION: compareFAE
	# INPUT: current_fae  - list
	#		 intended_fae - list
	# OUTPUT: balance_list - [(fae, fae_complement), ...] <--- verify this is how it would work
	#			This is a list of fae pairings that have been deemed worthy enough to be balanced.
	# DESCRIPTION:
	# 	Assess's whether an fae pairing is ready to be balanced. This is decided by the distance
	# 	 between the intended and current proportion in relation to the aggregate withdrawal fee.
	def compareFAE(balances, current_fae):
		balance_list = []

		if 'ALL' in balances: del balances['ALL']
		print("COMPAREFAE begin, BALANCES: ", balances)
		PrintLibrary.delimiter()

		temp_dict = {}
		for value in current_fae:
			asset = value[0]
			exchange = value[1]
			quantity = value[2]

			# Convert the BTC value of ASSET quantity to actual
			intended = Helpers.quoteValue(asset, quantity, exchange)

			# Get the ASSET quantity 
			current = balances[exchange][asset][0]

			# If its less, denote that we need to buy INTENDED -CURRENT, if its more [negative], sell
			quant = intended - current

			# BTC is handled in a special case, since it is the base asset
			# if asset == "BTC":
				# quant = current

			balance_list.append((asset, exchange, quant))
			
			print("buy or sell", asset, exchange, quant) 

			try:
				temp_dict[exchange] = temp_dict[exchange] + value[3]
			except KeyError:
				temp_dict[exchange] = 0 + value[3]

		for key in temp_dict:
			PrintLibrary.delimiter()
			diff = temp_dict[key] - balances[key]["BTC"][0]
			print("CURRENT Balance: ", key, balances[key]["BTC"])
			print("INTENDED change in bitcoin", diff)
			balance_list.append(("BTC", key, diff))

		return balance_list


	# FUNCTION: deleteFAEPairing
	# INPUT: pairing - string
	# OUTPUT: values to be balanced
	# DESCRIPTION:
	#	Removes an FAE pairing from the database, signifying that it is being removed from circulation.
	def deleteFAEPairing(pairing):
		balance_list = []

		# 1. Check exchanges pairing is on
		# TODO: below function
		# exchanges - [exchange_one, ...]
		exchanges = DatabaseLibrary.getExchangesFAE(pairing)

		# 3. Delete from FAE database
		DatabaseLibrary.deleteFAEentries(pairing, exchanges)

		# 4. Grab Accountbalances of pairing/exchange
		# TODO: inputs work properly?
		balance_list = DatabaseLibrary.getBalances(pairing, exchanges)

		# 5. Return [(balance_one_tuple), (balance_two_tuple)]
		return balance_list

	# FUNCTION: initializeFAE
	# INPUT: assets 		- [string, ...]
	#		 exchanges 		- [string, ...]
	#	 	 intended_fae	- [(asset, exchange, proportion), ...]
	# OUTPUT: N/A
	# DESCRIPTION:
	# 	Function run at call time (once) to set up the initial account balances.
	def initializeFAE(assets, exchanges, balances):
		# 1. Create intendedFAE
		intended_fae = BalancingLibrary.initializeFAEProportions(assets, exchanges, balances, True)
		print("1 - INTENDEDFAE after INITIALIZING proportions", intended_fae)
		PrintLibrary.delimiter()
		current_fae = BalancingLibrary.buildCurrentFAE(balances, intended_fae)
		print("2 - CURRENT FAE after building: ", current_fae)
		PrintLibrary.delimiter()

		# balance_list - []
		# 	This is a list of tuples representing the FAEs that passed the 'to be balanced' check
		balance_list = BalancingLibrary.compareFAE(balances, current_fae)
		print("3 - FAEs AFTER balance check: ", balance_list)

		if balance_list == []:
			print("4 - Nothing to balance for this iteration")
			return 0
		else:
			result = BalancingLibrary.balancePairings(balance_list)
			print("4 - BALANCE PAIRING RESULTS", result)
			return result

	# FUNCTION: initializeFAEProportions
	# INPUT: assets    - [string, ...]
	#		 exchanges - [string, ...]
	# OUTPUT: N/A
	# DESCRIPTION:
	# 	Create our arbitrary proportions (Currently 50%), update database. 
	# * TODO - better description
	def initializeFAEProportions(assets, exchanges, balances, return_init_proportions=False):

		# This should be BTC, the first element of the assets list.
		# * - TODO, make more robust jusssttt incase
		assets.pop(0)
		return_list = []

		# Initialize our intendedFAE proportion IF its in balances and not in the given assets.
		for key in balances:
			for keyv in balances[key]:
				if keyv not in assets:
					if keyv != "BNB" and keyv != 'total_value_btc' and keyv != 'total_value_usd' and keyv != 'ALL' and keyv != "BTC":
						DatabaseLibrary.storeFAE(keyv, key, 0, .5)
						return_list.append((keyv, key, 0, .5))

		print("RETURN", return_list)
		# # Add currencies to exclusively be removed, since it is not one of our assets
		# for key in balances:
		# 	for keyv in balances[key]:

		# For each asset, exchange pairing --> store initial FAE entry
		num_assets = len(assets)
		equal_prop = 1 / num_assets
		if return_init_proportions:
			for asset in assets:
				for exchange in exchanges:
					fae = (asset, exchange, equal_prop, .5)
					DatabaseLibrary.storeFAE(asset, exchange, equal_prop, .5)
					return_list.append(fae)
			return return_list
		else:
			for asset in assets:
				for exchange in exchanges:
					fae = (asset, exchange, .5, equal_prop)
					DatabaseLibrary.storeFAE(asset, exchange, equal_prop, .5)
			return []


	# FUNCTION: retrieveIntendedFAE
	# INPUT: asset 	  - string [optional]
	#		 exchange - string [optional]
	# OUTPUT: varying
	# DESCRIPTION:
	#	Flexible function used to retrieve either a single IntendedFAE entry for an asset and exchange,
	#	 or multiple FAE entries for all assets and exchanges or for a given asset, or a given exchange.
	# * - Designate that you're looking for all assets on exchange by passing in "ALL" as the parameter
	#	   for asset.!s
	def retrieveIntendedFAE(asset, exchange=None):
		pass

	# --------------------------------- BALANCE PAIRING FUNCTIONS ---------------------------------s
	# FUNCTION: buyTransferAsset
	# INPUT:  from_exchange - string
	#         transfer_tuple - tuple
	# OUTPUT: dictionary containing buy information
	# DESCRIPTION:
	#	Function used to buy the designated asset to transfer between exchanges.
	def buyTransferAsset(from_exchange, transfer_tuple):

		asset = transfer_tuple[0]
		buy_rate = transfer_tuple[1]
		quantity = transfer_tuple[3]

		buy_dict = ExchangeAPI.buyLimitAbs(from_exchange, asset, quantity, buy_rate)
		
		print("buyTransferAsset")
		PrintLibrary.displayVariables(transfer_tuple)
		PrintLibrary.displayDictionary(buy_dict)

		return buy_dict

	# FUNCTION: decideTransferAsset
	# INPUT: base_asset		- string
	#		 quantity 		- float
	#		 from_exchange 	- string
	#		 to_exchange 	- string
	# OUTPUT: (transfer_asset, exchange_one_prices, exchange_two_prices, buys, sells)
	# DESCRIPTION:
	#	This function determines what the best transfer asset is to use. it also checks 
	#	 through bids and asks lists on each exchange, and finds the quantities and 
	#	 prices at which to buy and sell the transfer asset.
	def decideTransferAsset(base_asset, quantity, from_exchange, to_exchange):

		# REHAUL
		# * - Review logic, test through
		# * - IS it best to place it off orderbook? or do something else to get a gauge. Regular last price might work fine
		# * - Add a way to look through asset information for currencies with lowest withdrawal fee. In future, short
		#	 transaction times will be useful as well.
		# * - NEed to maek sure gap between two exchanges isn't too large as well
		# * - Finally, starting to track the 'losses' from transfering and selling

		# 1. Check out of the given transfer assets (LTC, XRP, BTC, ...) which incurs 
		#		the least costs.
		transfer_asset = 'XRP'
		exchange_one_prices = []
		exchange_two_prices = []
		place = 0
		quantBuy = quantity
		quantSell = quantity
		buys = quantity
		sells = quantity

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

	# FUNCTION: detectFundsArrived
	# INPUT: withdraw_info - dictionary
	#		 max_time 	   - int (in minutes)
	# OUTPUT: boolean
	# DESCRIPTION:
	#	Function called when attempting to determine when funds from a transfer have arrived, and then what to do
	#	 if so. In some instances, the program may require further actions once the funds have arrived, in most
	#	 instances it is simply to acknowledge funds are no longer locked up.
	def detectFundsArrived(withdraw_info, max_time):
		sent_funds = withdraw_info["amount"]
		asset = withdraw_info["asset"]
		exchange = withdraw_info["to_exchange"]
		initial_time = Helpers.createTimestamp()
		
		print("Fund loop [exchange waiting, quantity, asset] ", exchange, sent_funds, asset)

		ticker = 0
		while ticker < max_time:
			succeed_bool = ExchangeAPI.checkDeposit(exchange, asset, sent_funds, initial_time)
			print("Deposit arrived:", succeed_bool)
			if succeed_bool:
				return True
			time.sleep(60)
			ticker += 1

		return False

	# FUNCTION: sellTransferAsset
	# INPUT:
	# OUTPUT:
	# DESCRIPTION:
	#	Final leg for the 'transfer base' series of actions. This function handles selling a transfer asset that is
	#	 used in place of BTC.
	def sellTransferAsset():
		pass

	# FUNCTION: transferQuote
	# INPUT: asset 		 	- string
	#        quantity 		- string
	#        from_exchange 	- string
	#        to_exchange	- string
	# OUTPUT: dictionary
	# DESCRIPTION:
	#	Function used to transfer quote asset from exchange to exchange and store
	#	 relevant information in order to pass on to listener.
	def transferQuote(asset, quantity, from_exchange, to_exchange):
		withdraw_dict = AccountBalancing.withdraw(from_exchange, to_exchange, asset, quantity)
		return withdraw_dict

	# FUNCTION: transferBase
	# INPUT: asset  	   - string [BASE ASSET, NON-DESCRIPTIVE NAME FOR NAMESPACE OPTIMIZATION]
	#		 quantity      - float
	#		 from_exchange - string
	#		 to_exchange   - string
	# OUTPUT: tuple containing withdraw information
	# DESCRIPTION:
	#	Function used to transfer quote asset from exchange to exchange and store
	#	 relevant information in order to pass on to listener.
	def transferBase(asset, quantity, from_exchange, to_exchange):
		# (asset,)
		transfer_asset_tup = AccountBalancing.decideTransferAsset(base_asset, quantity, from_exchange, to_exchange)

		# Possibly add another profitability check here
		buy_info = AccountBalancing.buyTransferAsset(from_exchange, transfer_asset_tup)
		# In the future, error handling might include trying again in a few minutes if it isn't usccessful

		# IF the buy was successful
		if buy_info["something"] == True:
			# Withdraw using buy info
			print(buy_info, "About to WITHDRAW")
			time.sleep(10)

			# TODO, vet the buy_info parameters
			withdraw_dict = AccountBalancing.withdraw(transfer_asset_tup[0], buy_info["quantity"], from_exchange, to_exchange)
			return withdraw_dict
		else:
			# If it wasn't, do some error handling
			pass

	# FUNCTION: withdraw
	# INPUT: asset 			- string
	#		 quantity 		- float
	#		 from_exchange  - string
	#		 to_exchange 	- string
	# OUTPUT: dictionary of information pertaining to the withdrawal
	# DESCRIPTION: 
	#	
	def withdraw(asset, quantity, from_exchange, to_exchange):
		tag_assets = ["XMR", "XRP"]

		# Check min order here
		address = DatabaseLibrary.getDepositAddress(asset, to_exchange)
		print("to address", address)
		for tag_asset in tag_assets:
			if tag_asset == asset:
				tag = DatabaseLibrary.getWithdrawalTag(asset, to_exchange)
				print(tag)
				time.sleep(30)
				withdraw_info = ExchangeAPI.withdraw(from_exchange, asset, quantity, address, tag)
				withdraw_info["to_exchange"] = to_exchange
				return withdraw_info

		print("no tag for", asset)
		withdraw_dict = ExchangeAPI.withdraw(from_exchange, asset, quantity, address)
		withdraw_dict["to_exchange"] = to_exchange
		return withdraw_dict

	# --------------------------------- FOR THE FUTURE ---------------------------------
	# FUNCTION: convertToETH
	# INPUT: size - int [1 to 100 are valid inputs]
	# OUTPUT: TODO
	# DESCRIPTION:
	# 	Converts a portion [or the entirety] of the portfolio to Ethereum. The purpose
	#	 would be to hold the account over in times of turmoil or transition.
	def convertToETH(size):
		# 1. Take the current balances
		# 2. Sell everything that isn't ETH in each exchange
		# 3. Buy ETH
		pass

	# FUNCTION: createFAEProportions
	# DESCRIPTION:
	#	To be called intermittently, used to created 'intended_fae' object for each period of time where
	#	 base balances are getting updated during runtime.
	# For now, doesn't need to work
	def createFAEProportions(heuristic_message):
		pass

	def removeDust():
		pass

	def buyBNB():
		pass

if __name__ == '__main__':
	# 1. Test transfering base, quote individually
	value  = BalancingLibrary.transferQuote("KMD", 10, "binance", "bittrex")
	print(value)
	value = BalancingLibrary.transferBase("BTC", .005, "bittrex", "binance")
	print(value)

	# 2. Test a 'balance account' action [both together, with a storeTransfer]
	value = BalancingLibrary.balancePairing("BTC-KMD", .005, 10, "binance", "bittrex")
	print(value)