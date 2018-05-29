
import sys
# Temporary solution: append sys path in order to import from other folders
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Red-Dogs/2API/Exchange_APIs')
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Red-Dogs/2API/Main')
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Red-Dogs/3Database_Management')

import time
import json
import sqllite3
import threading
from copy import deepcopy
import math 
import DatabaseManager
import Helpers
import API


class LowLiquidityArbitrage():

	#FUNCTION: Arbitrage
	#INPUT: heuristic - dictionary
	#OUTPUT: tuple
	#DESCRIPTION:
	#	Main loop where arbitrage is run
	def Arbitrage(heuristic):
		DatabaseHelpers.cleanDb()


	    # index into this via dict[exchange][currency]
	    balance_dictionary = DatabaseHelpers.getDbBalances(exchanges_used)
	    while 1:
	    	# MAIN LIST LOOP
			for pairing in main_list:

				limit_result = checkLimitOrder()
				AccountBalancing.balanceAccounts(limit_result)

				# Store quote/base in advance in order to save processing time
	        	base, quote = pairing.split("-")
				# Retrieve list of exchanges (currently only will be looking at TWO)
				exchanges = Helpers.getSupported(pairing)
				order_list = [] 
				thread_list = [] 
				thread_count = 0

				# TODO COMMENT THIS
				# For each exchange, create a thread which calls get_order over our pairing
				for ex in exchanges:
					order_list.append( (ex, [], []) )
					t = threading.Thread(target=getOrders,args=(ex, quote, base, order_list[thread_count][1], order_list[thread_count][2]))
					thread_count += 1
					thread_list.append(t)
					t.start()
				[t.join() for t in thread_list]


				# TODO COMMENT THIS
                # order_tuple :: (quantity, sell_exchange, sell_price_limit, buy_exchange, buy_price_limit)
				# Evaluate pairing and store data
				order_tup = eval_func(order_list, base, quote)
                order_tup1 = evaluatePairing(order_list, base, quote, 0)
                order_tup2 = evaluatePairing(order_list, base, quote, 1)
                order_tup = max([order_tup1,order_tup2], key=lambda x:x[5])

                limit_info = limitArbitrage()
                
                # IF arbitrage's profit is less than zero continue to next pairing
                if order_tup[0] <= 0:
                    continue

                # TODO COMMENT THIS
                exchange_one_base = DatabaseHelpers.getBalance(exchanges[0], base)
                exchange_one_quote = DatabaseHelpers.getBalance(exchanges[0], quote)
                exchange_two_base = DatabaseHelpers.getBalance(exchanges[1], base)
                exchange_two_quote = DatabaseHelpers.getBalance(exchanges[1], quote)

                # TODO COMMENT THIS
                input_tuple = order_tuple[:-1] + (pairing, exchange_one_quote, exchange_one_base, exchange_two_quote, exchange_two_base)

                # TODO COMMENT THIS
                return_balances = marketArbitrage(input_tuple)

                # TODO COMMENT THIS
                AccountBalancing().balanceAccounts(return_balances)


		      	###### PART TWO: USE PREVIOUS DATA TO SET UP LIMIT BASED ORDERS #########
		      	# 
		      	# (ITERATION after first: check to see if limit orders have filled)
		      	#       if so, attempt market order, remove from list
		      	#        potentially double down on limit order if market is successful
		      	#        if not error handling
		      	#         initially it would just check 0 orders and say ok go on
		      	# call new function for each pairing that is attractive based on above data
		      	# open limit orders near highest bid lowest ask
		      	# wait for them to fill (set something in place to make sure they don't open
		      	#   a new one until they're filled)
		      	# probably keep a list of open orders
		      	#
		      	# more to come, probably start here
		      	##########################################################################

		      	############ PAIRING HEURISTIC / NEW LIST HERE ##########################
		      	# IF PAIRING IS ATTRACTIVE FOR SOME REASON
		      	# 	ADD TO SECONDARY LIST
		      	#########################################################################
	
		    ################################################################################
		    # SECONDARY LIST LOOP: USING COINS DESIGNATED TO BE ATTRACTIVE
		    # DO THESE COINS FOR ??? ITERATIONS
		    # for pairing in secondary_list
		    # 	same arbitrage loop
		    #   remove if out of quantity
		    #   after X iterations || not enough currencies (??)
		    #   remove certain currencies (update lists based on balances)
		    #   break and do a main loop
		    #
		    # NOTE: Account balances needs to inform (???) listener when the accounts are rebalanced for favourable currencies;
		    #             add them back into main to check for preference again
		    ###############################################################################

		    # Verify account balances remotely based on some ticker system, update all account balances (30 minutes?)


	# -------- INITIALIZE VARIABLES --------
	# Initialize list of supported exchanges
    exchanges = ('bittrex', 'binance')
	# Initialize list of supported pairings
    pairing_list = ['BTC-ARK', 'BTC-BAT', 'BTC-ZEC', 'BTC-NEO', 'BTC-LTC', 'BTC-KMD', 'BTC-OMG', 'BTC-QTUM',
                    'BTC-ADA', 'BTC-MANA', 'BTC-STRAT']
	# eval_func_dic['init_eval'] # calls evaluate_pairing
	eval_func_dic = {'init_eval' : evaluate_pairing}

	# Part 1: IDENTIFICATION
	# Input: List of supported exchanges, list of supported pairings
	# Functions: getOrders, evaluatePairing, identifyArbitrage
	# Description:

	# FUNCTION: getOrders
	# INPUT: exchange - string
	#		 quote    - double
	#		 base     - double
	#		 ask_list - tuple(price,quantity,exchange) [PASSED IN BY REFERENCE]
	#		 bid_list - tuple(price,quantity,exchange) [PASSED IN BY REFERENCE]
	# OUTPUT: TODO
	# DESCRIPTION:
	#	Grabs the order book for a given exchange and fills up the bids and asks in tuples
	#	 to be passed to evaluated pairing
	def getOrders(exchange, quote, base, ask_list, bid_list):

		# TODO COMMENT
        dict1 = API.getOrderbook(exchange, pairing)
        if dict1["success"]:
            bids = dict1["bids"]
            asks = dict1["asks"]
            bids_length = len(bids)
            asks_length = len(asks)
            for bid in bids:
                price = bid[0]
                quantity = bid[1]
                bid_total = price*quantity
                bid_l = [price,quantity,exchange,bid_total]
                bid_list.append(bid_l)
            for ask in asks:
                price = ask[0]
                quantity = ask[1]
                ask_total = price*quantity
                ask_l = [price,quantity,exchange,ask_total]
                ask_list.append(ask_l)

            ask_list.sort(key=lambda x: x[0],reverse=False)
            bid_list.sort(key=lambda x: x[0],reverse=True) # descending

        return -1

	# FUNCTION: evaluatePairing
	# INPUT: order_list - tuple (exchange_name, ask_list, bid_list)
	#		 base 		- string
	#		 quote 		- string
	# OUTPUT: tuple -- (final_quantity, sell_exchange, sell_price_limit, buy_exchange, buy_price_limit, profit))
	# DESCRIPTION:
	#	Evaluates the arbitrage opportunity of a given pairing between two exchanges
	def evaluatePairing(order_list, base, quote):

		# TODO COMMENT THIS
        sell_bids = order_list[ask_num][2]
		bid_range = list(sell_bids)
		breakeven_price = buys_asks[0][0]
		for bid in sell_bids:
			if bid[0] > breakeven_price:
				bid_range.append(bid)

		# TODO COMMENT THIS
        ask_num = int(not(buy_num))
        buy_exchange = order_list[buy_num][0]
        buy_asks = order_list[buy_num][1]
        buy_rate = buy_asks[0][0]
        sell_exchange = order_list[ask_num][0]
        sell_rate = sell_bids[0][0]
		ask_range = list(buy_asks)

		# TODO COMMENT THIS
		quantity = 0
		buy_price = 0 # money spent
		total_sale = 0 # total money made
		ask_i = 0
		bid_i = 0
		residue = (0,0) # price and quantity residue 
		avg_price_buy = 0
		avg_price_sell = 0
		bid_fee = .25/100
		ask_fee = .05/100
		bid_fee = Helpers.getFee(buy_exchange)
        ask_fee = Helpers.getFee(sell_exchange)
		bid_len = len(bid_range)
		ask_len = len(ask_range)

		# BTC available in the exchange you're buying in
        balance_ALT = DatabaseHelpers.getBalance(sell_exchange, quote)
		# altcoin available in the exchange you're selling in 
        balance_BTC = DatabaseHelpers.getBalance(buy_exchange, base)

        # TODO COMMENT THIS
		while 1:

			# TODO COMMENT THIS
			if ask_i >= ask_len or bid_i >= ask_i:
				break

        	# Grab ask price/bid price 
			ask_p = ask_range[ask_i][0]
			bid_p = bid_range[bid_i][0]

			# Check if price's are still good, fees factored in
        	if (ask_p + (ask_p * ask_fee)) >= (bid_p - (bid_p * bid_fee)):
            	break

            # Grab quantities
			ask_q = ask_range[ask_i][1]
			bid_q = bid_range[bid_i][1]

			# TODO COMMENT THIS
        	sell_price_limit = bid_p
        	buy_price_limit = ask_p

        	# TODO COMMENT THIS
            work_quant = min(ask_q,bid_q)
            next_quantity = quantity + work_quant
            p = work_quant * ask_p
            next_price = buy_price + p
            sale_quant = work_quant * bid_p
            next_total_sale = total_sale + sale_quant

            # TODO COMMENT THIS
            curr_funds_base = balance_BTC - buy_price
            sell_quant_possible = balance_ALT - quantity
            buy_quant_possible = curr_funds_base / ask_p
            limit_quant = min(work_quant,buy_quant_possible,sell_quant_possible)
            if limit_quant != work_quant:
                p = limit_quant * ask_p
                buy_price += p
                quantity += limit_quant
                sale_quant = limit_quant * bid_p
                total_sale += sale_quant
                sell_price_limit =  bid_p
                buy_price_limit = ask_p
                break
            else:
                buy_price = next_price
                quantity = next_quantity
                total_sale = next_total_sale
                if ask_q >= bid_q:
                    bid_i += 1
                if bid_q >= ask_q:
                    ask_i += 1

        profit_ratio = calculatePR()
        arbitrage_bool = Helpers.assessProfitRatio(profit_ratio)
        # Pass arbitrage_bool by reference
        arbitrage_quantity = determineOrderSize(profit_ratio, quantity, arbitrage_bool)
        arbitrage_bool = checkMinimumOrder(quantity, avg_price_buy, avg_price_sell, buy_exchange, sell_exchange)

        return (final_quantity, sell_exchange, sell_price_limit, buy_exchange, buy_price_limit, profit, arbitrage_bool)

	# Part 2: Executing Arbitrage
	# Inputs:
	# Functions: executeArbitrage
	# Description:	In this section, we take action over the identified potential arbitrage with input parameters from the first part.
	#				 The implementation must handle errors and return results to be stored in a database.

	# FUNCTION: executeArbitrage
	# INPUT: input_tuple - (pairing, quantity, sell_exchange, sell_price, buy_exchange, buy_price, quote_balance, base_balance)
	#	input_tuple:pairing - string
	#             	quantity - double [QUOTE ASSET VALUE]
	#             	sell_exchange - string
	#             	sell_price	  - double [price to sell at]
	#             	quote_balance - double
	#             	buy_exchange  - string
	#             	buy_price	  - double 
	#             	base_balance  - double
	# OUTPUT: new account balance OR original account balance with error flag
	def marketArbitrage(self, input_tuple):

		# Assign local variables from input tuple
        quantity, sell_exchange, sell_price, buy_exchange, buy_price, pairing, sell_balance_quote, sell_balance_base, buy_balance_quote, buy_balance_base = input_tuple

		# ORDER ONE: LOW-LIQUIDITY EXCHANGE
		#	BUY or SELL on the exchange with lower liquidity relative to the other one. This sets the benchmark
		#    price and quantity for the arbitrage. If the first order sells, error handling composes of breaking
		#	 from the arbitrage, effectively cancelling the arbitrage attempt.

		# TRUE designates SELL 
		# FALSE designates BUY
        result = Helpers.decideOrder(buy_exchange, sell_exchange)
        if result == True:
            sell_id_one = API.sellLimit(sell_exchange, pairing, quantity, sell_price)
            if sell_id_one["success"] != True:
                print(' ERROR [executeArbitrage, order ONE : sell_order_failed]')
                return -1 
            order_dict_sell1 = API.getOrder(sell_exchange, sell_id_one["order_id"], pairing)

            # CASE: None of value has been executed :: cancel and exit
            if order_dict_sell1["incomplete"] == True:
                API.cancelOrder(sell_exchange, sell_id_one["order_id"], pairing)
                if order_dict_sell1["success"] == True:
                    quantity = order_dict_sell1['executed_quantity']
                return -1
        else:
            buy_id_one = API.buyLimit(buy_exchange, pairing, quantity, buy_price)
            print(buy_id_one)
            if buy_id_one["success"] != True:
                print(' ERROR [executeArbitrage, order ONE : buy_order_failed ]')
                return -1 
            order_dict_buy1 = API.getOrder(buy_exchange, buy_id_one["order_id"], pairing)

            # CASE: None of value has been executed :: cancel and exit
            if order_dict_buy1["incomplete"] == 0:
                API.cancelOrder(buy_exchange, buy_id_one["order_id"], pairing)
                if order_dict_buy1["success"] == True:
                    quantity = order_dict_buy1['executed_quantity']
                return -1

		# ORDER TWO: HIGH-LIQUIDITY EXCHANGE
		#	Perform opposite side order depending on first order. Use first order's price as minimum break-even point.
		#    Second order requires more complex error handling
        if result == True:
            sell_dict = order_dict_sell1
            buy_id_two = API.buyLimit(buy_exchange, pairing, quantity, buy_price)
            order_dict_buy2 = API.getOrder(buy_exchange, buy_id_two["order_id"], pairing)
            if buy_id_two["success"] != True:
                print(' ERROR [executeArbitrage, order TWO : buy_order_failed]')
                adjust_min = Helpers.handleIncompleteArbitrage(order_dict_sell1, order_dict_buy2)
                return err_balance
            executed_quantity = order_dict_buy2["quantity"]
            buy_dict = order_dict_buy2
        else:
            buy_dict = order_dict_buy1
            sell_id_two = sellOrder(sell_exchange, pairing, quantity, sell_price)
            order_dict_sell2 = getOrder(sell_exchange, sell_id_two["order_id"], pairing)
            if sell_id_two["success"] != True:
                print(' ERROR [executeArbitrage, order TWO : sell_order_failed]')
                adjust_min = Helpers.handleIncompleteArbitrage(order_dict_sell2, order_dict_buy1)
                return err_balance
            executed_quantity = order_dict_sell2["quantity"]
            sell_dict = order_dict_sell2

		# SUCCESSFUL ARBITRAGE
		#	Move on to storing results of arbitrage and setting up inputs for account balancing
		sell_price = sell_dict["rate"]
		buy_price = buy_dict["rate"]

		# Calculate potential profit ratio
		pr = Helpers.calculatePR(sell_price, buy_price)
		profit = Helpers.calculateProfit(sell_price, buy_price, quantity)
        
		# Update account balances
 	    sell_balance_base += Helpers.baseAsset(quantity, sell_price)
  	    sell_balance_quote -= quantity
 	    buy_balance_base -= Helpers.baseAsset(quantity, buy_price)
   	    buy_balance_quote += quantity

		# Store in database
        DatabaseHelpers.storeArbitrage(input_tuple, sell_dict, buy_dict, pr, profit)

        result = (sell_exchange, buy_exchange, sell_balance_base, sell_balance_quote, buy_balance_base, buy_balance_quote)
        return result

    def limitArbitrage():
    	pass

    def checkLimit():
    	pass