# ArbitrageLibrary.py
# Carson Packer
# DESCRIPTION:
#    Library of functions used in the arbitrage system. Each function is pertinent to arbitrage
#     in some specific awy. This includes applications to market and limit arbitrage.

# External-Imports
import time 
import sys

# WINDOWS main-desktop, LINUX main-server
sys.path.append('U:/Directory/Projects/Work/BlueTitan/Components/Database-Manager')
sys.path.append('U:/Directory/Projects/Work/BlueTitan/Components/Libraries')
sys.path.append('U:/Directory/Projects/Work/BlueTitan/Components/Crypto-API/Exchange-APIs')

# WINDOWS laptop
# sys.path.append()

# Internal-Imports
from API import ExchangeAPI
import Helpers
from GeneralizedDatabase import GenDatabaseLibrary
from PrintLibrary import PrintLibrary

# CLASS: ArbitrageLibrary
# DESCRIPTION:
#   Set of functions that primarily [or are exclusively written] for the Arbitrage component of the
#    program.
####################################### FUNCTION LIST ##############################################
# * - assessProfitRatio         : Used to determine the profitability of a given profit ratio      #
# * - checkMinOrder             : Checks to ensure the minimum order size is reached for trades    #
#                                  on two exchanges, for arbitrage.                                # 
# * - decideOrder               : TO BE REWORKED                                                   #
# * - determineOrderSize        : Provides the order, or bet, size for a given trade               #
# * - evaluatePairing           : One of the main functions for market arbitrage, evaluates        #
#                                  whether there is profitable arbitrage available for a given     #
#                                  pairing.                                                        #
# * - handleIncompleteArbitrage : Executes when there is an incomplete arbitrage event.            #
####################################################################################################
class ArbitrageLibrary(object):

    # FUNCTION: getAggregateWFees
    # INPUT: pairing      - string
    #        exchange_one - string
    #        exchange_two - string
    #        quantity     - float
    # OUTPUT: float
    # DESCRIPTION: 
    #   Retrieves the withdrawal fees for a specified pairing and factors in the effective
    #    'per trade' withdrawal fee.
    def getAggregateWFees(quote, exchange_one, exchange_two, quantity):

        # Rework this
        fee_one_orig = DatabaseLibrary.getWithdrawalFee(quote, exchange_one, "BTC")
        fee_two_orig = DatabaseLibrary.getWithdrawalFee("BTC", exchange_two, "BTC")
        total_balance = DatabaseLibrary.getBalanceTotal("BTC")
        pairing = Helpers.pairingStr(quote)
        fae = DatabaseLibrary.getFAEProportion(quote, exchange_one)
        alloc_prop = total_balance * fae
        print(alloc_prop, "Allocated value in BTC")
        btc_value = Helpers.btcValue(quote, quantity, exchange_one)
        size = btc_value / alloc_prop
        fee_one = fee_one_orig * (size / 2)
        fee_two = fee_two_orig * (size / 2)
        fees = fee_one + fee_two
        print(fees, fee_one, fee_two, size, btc_value)
        return fees 

    # FUNCTION: checkMinOrder
    # INPUT: pairing      - string
    #        exchange_one - string
    #        exchange_two - string
    #        quantity     - float
    #        rate         - float
    # OUTPUT: quantity [float]
    # DESCRIPTION:
    #   Checks to ensure that order parameters fit minimum order size for each respective exchange.
    def checkMinOrder(pairing, exchange_one, exchange_two, quantity, rate):
        order_size = quantity * rate
        notional_dict_one = ExchangeAPI.getInfoPairing(exchange_one, pairing)
        notional_dict_two = ExchangeAPI.getInfoPairing(exchange_two, pairing)
        notional_one = notional_dict_one["min_trade_size"]
        notional_two = notional_dict_two["min_trade_size"]
        notional = min(notional_one, notional_two)

        # order size is too small, return 0
        if order_size < notional:
            PrintLibrary.displayVariable(order_size, "Order is below theshold for one of the exchanges")
            return 0

        # If order size is ok, perform step size conversion
        else:
            step_size = max(notional_dict_one["step_size"], notional_dict_two["step_size"])
            qty_trim = order_size % step_size
            quantity = quantity - qty_trim
            
        return quantity

    # FUNCTION: decideOrder
    # INPUT: buy_exchange  - string
    #        sell_exchange - string
    # OUTPUT: bool
    # DESCRIPTION:
    #   Decides which exchange to attempt to arbitrage on first.
    def decideOrder(buy_exchange, sell_exchange):
        temp_dict = {'binance': 3, 'bittrex': 2, 'cryptopia': 1}
        return temp_dict[sell_exchange] < temp_dict[buy_exchange]

    # FUNCTION: determineOrderSizeo
    # INPUT: profit_ratio - float
    #        quantity     - float
    # OUTPUT: quantity [float]
    # DESCRIPTION:
    #   Determines the order size for an arbitrage trade based on profit ratio. Implicit check on
    #    whether or not to perform arbitrage.
    def determineOrderSize(profit_ratio, quantity, price):

        # Case 1: Profit ratio is in huge range [?]
        if profit_ratio > 1.25:
            final_quantity = quantity * .25
        # Case 2: Profit ratio is within the regular range [?]
        elif profit_ratio > .65:
            adjusted_quant = quantity * .1
            btc_value = adjusted_quantity * price

            # Check to make sure the BTC value of the trade is more than a specified minimum
            if btc_value > .01:
                # why would this work
                #final_quantity = .01 / price
                final_quantity = quantity * .1
            else:
                final_quantity = 0
            PrintLibrary.displayKeyVariables((("Final_quantity", final_quantity),
                                                ("BTC value", btc_value),
                                                ("Original quantity", quantity),
                                                ("Profit_ratio", profit_ratio)), "Final Order Size")
            
        # Case 3: Profit ratio is not profitable
        else: 
            final_quantity = 0

        return final_quantity

    # FUNCTION: evaluatePairing
    # INPUT: order_list - [(bids, asks), ...], (TODO)
    #        pairing    - string
    #        buy_num    - ???
    # OUTPUT: Tuple
    # DESCRIPTION:
    #   Top level function for evaluating whether a pairing has profitable arbitrage available.
    def evaluatePairing(order_list, pairing, buy_num):

        # Error check incase of api issue, to be replaced in future.
        if order_list[buy_num][1] == None:
            PrintLibrary.message("Part of order_list in evaluatePairing turned up null, breaking")
            return (0)

        # VARIABLE SET UP
        base, quote = pairing.split("-")
        ask_num = int(not(buy_num))

        buy_exchange = order_list[buy_num][0]
        buy_asks = order_list[buy_num][1] # BIG BREAK POINT 
        buy_rate = buy_asks[0][0]
        buy_quantity = buy_asks[0][1]
        breakeven_price = buy_asks[0][0]

        sell_exchange = order_list[ask_num][0]
        sell_bids = order_list[ask_num][2]
        sell_rate = sell_bids[0][0]
        sell_quantity = sell_bids[0][1]

        bid_range = list(sell_bids)
        ask_range = list(buy_asks)
        bid_fee = Helpers.getFee(buy_exchange)
        ask_fee = Helpers.getFee(sell_exchange)

        profit_ratio = Helpers.calculatePR(sell_rate, buy_rate)     
        balance_ALT = DatabaseLibrary.getBalance(quote, sell_exchange)
        balance_BTC = DatabaseLibrary.getBalance(base, buy_exchange)
  
        for bid in sell_bids:
            if bid[0] > breakeven_price:
                bid_range.append(bid)

        bid_len = len(bid_range)
        ask_len = len(ask_range)

        #  INITIALIZATIONS FOR MAIN LOOP 
        quantity = 0
        buy_price = 0
        total_sale = 0
        ask_i = 0
        bid_i = 0
        avg_price_buy = 0
        avg_price_sell = 0
        
        # Initialize as booleans
        sell_price_limit = 99999999999999
        buy_price_limit = -1
        
        #  INITIAL PRINTS [debugging]
        temp_tuple = (('Sell Exchange', sell_exchange),
                    ('Profit Ratio ', str(profit_ratio)),
                    ('ALT Balance  ', balance_ALT),
                    ('BTC Balance  ', balance_BTC),
                    ("Sell rate", sell_rate),
                    ("Buy rate", buy_rate),
                    ("Sell quantity", sell_quantity),
                    ("Buy quantity", buy_quantity))

        PrintLibrary.displayKeyVariables(temp_tuple, "EvaluatePairing")

        # 2: MAIN EVALUATE LOOP
        while 1:

            # BREAK CONDITION: We have reached the end 
            if ask_i >= ask_len or bid_i >= bid_len:
                break

            ask_p = ask_range[ask_i][0]
            bid_p = bid_range[bid_i][0]
            ask_q = ask_range[ask_i][1]
            bid_q = bid_range[bid_i][1]

            profit_ratio_e = Helpers.calculatePR(bid_p, ask_p)
            PrintLibrary.displayVariable(profit_ratio_e, "evaluatePairing profit")
            PrintLibrary.displayVariables((ask_p, bid_p))

            # This might neeed to be reworked
            if (ask_p + (ask_p * ask_fee)) >= (bid_p - (bid_p * bid_fee)):

                if profit_ratio_e < 0.3:
                    print("breaking")
                    break

                if quantity == 0:
                    attempted_quantity = 0
                    attempted_quantity_btc = 0
                break

            # Current quantity to work with is MINIMUM of bid/ask pairing
            working_quantity = min(ask_q, bid_q)

            # Set up the potential next quantity (?)
            next_quantity = quantity + working_quantity
            working_btc_value = working_quantity * ask_p
            next_price = buy_price + working_btc_value

            sell_btc_v = working_quantity * bid_p
            next_total_sale = total_sale + sell_btc_v

            curr_funds_base = balance_BTC - buy_price
            sell_quant_possible = balance_ALT - quantity
            buy_quant_possible = curr_funds_base / ask_p
            limit_quantity = min(working_quantity, buy_quant_possible, sell_quant_possible)

            # Case 1: We have LESS than what is available
            if limit_quantity != working_quantity:
                PrintLibrary.displayVariable(limit_quantity, "Balance was too low on one")
                working_btc_value = limit_quantity * ask_p
                buy_price += working_btc_value
                quantity += limit_quantity
                sell_btc_v = limit_quantity * bid_p
                total_sale += sell_btc_v
                sell_price_limit =  bid_p
                buy_price_limit = ask_p
                break

            # Case 2: We have MORE than what is available
            else:
                buy_price = next_price
                quantity = next_quantity
                total_sale = next_total_sale

                if ask_q >= bid_q:
                    bid_i += 1
                if bid_q >= ask_q:
                    ask_i += 1

        # 3: PROCESS EVALUATION

        # NO-ARBITRAGE CASE
        if quantity == 0:        
            return (0, sell_exchange, sell_rate, buy_exchange, buy_rate, 0, profit_ratio, True)

        # ARBITRAGE CASE
        else:

            # Fees & profit
            sell_fee_btc = total_sale * bid_fee
            buy_fee_btc = buy_price * ask_fee
            total_fee = sell_fee_btc + buy_fee_btc
            profit  = (total_sale - buy_price) - total_fee
            profit_ratio = Helpers.calculatePR(total_sale, buy_price)

            withdrawal_fee = ArbitrageLibrary.getAggregateWFees(quote, buy_exchange, sell_exchange, quantity)
            all_fees = withdrawal_fee + total_fee
            profit = (total_sale - buy_price) - all_fees
            print(profit, "new profit")
            PrintLibrary.displayKeyVariables((("Withdrawal fee", withdrawal_fee),
                                                ("total_fee", total_fee),
                                                 ("profit", profit),
                                                ("profit_ratio", profit_ratio)))
            # CASE: Profit does not outperform withdrawal fee
            if profit <= (2 * withdrawal_fee):
                return (0, sell_exchange, sell_rate, buy_exchange, buy_rate, 0, profit_ratio, True)

            # Betsize the trade based on parameters
            arbitrage_quantity = ArbitrageLibrary.determineOrderSize(profit_ratio, quantity, buy_price_limit)
            arbitrage_quantity = ArbitrageLibrary.checkMinOrder(pairing, sell_exchange, buy_exchange, arbitrage_quantity, buy_price_limit)

            # Trim the quantity for exchange standardization
            qty_trim = arbitrage_quantity % 0.01
            arbitrage_quantity = arbitrage_quantity - qty_trim

            btc_value = arbitrage_quantity * buy_price_limit

            PrintLibrary.displayKeyVariables((("Quantity(sized)", arbitrage_quantity),
                                                ("BTC value", btc_value),
                                                ("Profit Ratio", profit_ratio),
                                                ("Profit", profit),
                                                ("Price", buy_price_limit)))

        if arbitrage_quantity == 0:
            return_bool = True
        else: 
            return_bool = False
        # Needs to OUTPUT :
        return (arbitrage_quantity, sell_exchange, sell_price_limit, buy_exchange, buy_price_limit, profit, profit_ratio, return_bool)

    # FUNCTION: handle_incomplete_arbitrage
    # INPUT: sell_dict     - TODO
    #        sell_exchange - string
    #        buy_dict      - TODO
    #        buy_exchange  - string
    #        order_type    - TODO
    #        pairing       - string
    # OUTPUT: dictionary
    # DESCRIPTION:
    #   Wrapper function to call buy/sell-limitAbs when an Arbitrage is left incomplete. It simply 
    #    sells or buys the currency o nthe same exchange, and takes a loss if it needs.
    def handleIncompleteArbitrage(sell_dict, sell_exchange, buy_dict, buy_exchange, order_type, pairing):

        if order_type == 'Buy':
            ret_dict = ExchangeAPI.buyLimitAbs(buy_exchange, pairing, buy_dict["quantity"], buy_dict["rate"])
        if order_type == 'Sell':
            ret_dict = ExchangeAPI.sellLimitAbs(sell_exchange, pairing, sell_dict["quantity"], sell_dict["rate"])

        # TODO: record difference between prices
        # TODO: error checking
        return ret_dict

# CLASS: LimitArbitrage
# DESCRIPTION:
#    Container object for limit arbitrage calls.
class LimitArbitrage():

    def checkLimitTrades():
        pass

    def createTrade():
        pass
    
    def getOpenLimits():
        pass
    
    def handleLimitTrades():
        pass

    def removeLimitTrades():
        pass
