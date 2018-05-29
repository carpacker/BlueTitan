# External-Imports
import time 
import sys

# Windows
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Database-Manager')
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Libraries')
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Crypto-API/Exchange-APIs')

# Linux
# sys.path.append()

# Internal-Imports
from API import ExchangeAPI
import Helpers
from GeneralizedDatabase import GenDatabaseLibrary
from PrintLibrary import PrintLibrary

# CLASS: ArbitrageLibrary
# FUNCTION LIST: [assessProfitRatio, checkMinimumOrderm checkPairingExchanges, convertMinPrice, 
#                  convertMinQuantity, decideOrder, determineOrderSize, evalutePairing, 
#                  findCommonPairings, getOrders, handleIncompleteArbitrage]
# DESCRIPTION:
#   Set of functions that primarily [or are exclusively written] for the Arbitrage component of the program.
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

        # Down here somewhere usdt error
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
        # PrintLibrary.displayKeyVariables((("Fees", fees),
        #                                     ("Fee_one_orig", fee_one_orig),
        #                                     ("Fee_one", fee_one),
        #                                     ("Fee_two_orig", fee_two_orig),
        #                                     ("Fee_two", fee_two),
        #                                     ("Balance BTC_buy", balance_BTC_one),
        #                                     ("Balance BTC_sell", balance_BTC_two)
        #                                     ("Balance BTC", balance_BTC),
        #                                     ("Quantity BTC", quantity_BTC),
        #                                     ("Quantity", quantity)))
        # if balance_BTC != 0:
        return fees 

    # FUNCTION: assessProfitRatio
    # INPUT: profit_ratio -float
    # OUTPUT: boolean
    # DESCRIPTION: 
    #   Used to assess whether the profit ratio is suitable in runtime to execute arbitrage.
    def assessProfitRatio(profit_ratio, pairing):
        # 1. Estimate minimum profit ratio
        # 1. Look at current profits to date 
        if profit_ratio > .5:
            return True
        return False

    # FUNCTION: checkMinimumOrder
    # INPUT: pairing      - string
    #        exchange_one - string
    #        exchange_two - string
    #        quantity     - float
    #        rate         - float
    # OUTPUT: quantity [float]
    # DESCRIPTION:
    #   Checks to ensure that order parameters fit minimum order size for each respective exchange
    def checkMinOrder(pairing, exchange_one, exchange_two, quantity, rate):
        # * TODO - Possible deal with both directions later
        order_size = quantity * rate
        notional_dict_one = ExchangeAPI.getInfoPairing(exchange_one, pairing)
        notional_dict_two = ExchangeAPI.getInfoPairing(exchange_two, pairing)
        notional_one = notional_dict_one["min_trade_size"]
        notional_two = notional_dict_two["min_trade_size"]
        notional = min(notional_one, notional_two)
        print("NOTIONAL: ", notional)
        print("ORDER SIZE: ", order_size)
        if order_size < notional:
            print("ORDER IS BELOW THRESHOLD: " + str(order_size))
            return 0
        else:
            # Perform Lotsize conversion
            step_size = max(notional_dict_one["step_size"], notional_dict_two["step_size"])
            qty_trim = order_size % step_size
            quantity = quantity - qty_trim
            PrintLibrary.displayKeyVariables((("Step size", step_size),
                                                ("Trim quantity", qty_trim),
                                                ("quantity", quantity)))
        return quantity

    # FUNCTION: convertMinPrice
    # INPUT: exchange - string
    #        price    - float
    #        pairing  - string
    # OUTPUT: price(float)
    # DESCRIPTION:
    # Converts a given price to the minimum price for a pairing/exchange.
    def convertMinPrice(exchange, price, pairing): 
        trim_value = ExchangeAPI.getInfoPairing(exchange, pairing)
        precision = Helpers.determinePrecision(trim_value["min_price"])
        temp_string = "{:." + str(precision) + "f}"
        price = temp_string.format(price)
        return price

    # FUNCTION: convertMinQuantity
    # INPUT: exchange - string
    #        quantity - float
    #        pairing  - string
    # OUTPUT: quantity (float)
    # DESCRIPTION:
    #   Converts input parameters for a trade to the appropiate minimum quantity float value
    def convertMinQuantity(exchange, quantity, pairing):
        trim_value = ExchangeAPI.getInfoPairing(exchange, pairing)
        precision = Helpers.determinePrecision(trim_value["min_quantity"])
        temp_string = "{:." + str(precision) + "f}"
        quantity = temp_string.format(quantity)
        return quantity

    # FUNCTION: decideOrder
    # INPUT: buy_exchange  - string
    #        sell_exchange - string
    # OUTPUT: bool
    # DESCRIPTION:
    #   Decides which exchange to attempt to arbitrage on first
    def decideOrder(buy_exchange, sell_exchange):
        # returns True if sell first, meaning sell is low liq
        temp_dict = {'binance': 3, 'bittrex': 2, 'cryptopia': 1}
        # binance > bittrex > cryptopia 
        return temp_dict[sell_exchange] < temp_dict[buy_exchange]

    # FUNCTION: determineOrderSizeo
    # INPUT: profit_ratio - float
    #        quantity     - float
    # OUTPUT: quantity [float]
    # DESCRIPTION:
    #   Determines the order size for an arbitrage trade based on profit ratio
    def determineOrderSize(profit_ratio, quantity, price):

        # Case 1: Profit ratios is huge
        if profit_ratio > 1.25:
            # Use 25% of allocated portfolio (large sizing)
            final_quantity = quantity * .25

        # Case 2: Profit ratio is within the regular range (.3 to 1.25); attempt a very specific order_size
        elif profit_ratio > .65:
            btc_value = quantity * price
            if btc_value > .01:
                final_quantity = .01 / price
            else:
                final_quantity = 0
            PrintLibrary.displayKeyVariables((("Final_quantity", final_quantity),
                                                ("BTC value", btc_value),
                                                ("Original quantity", quantity),
                                                ("Profit_ratio", profit_ratio)))
            
        # Case 3: Profit ratio is not profitable
        else: 
            final_quantity = 0

        return final_quantity

    # FUNCTION: evaluatePairing
    # INPUT: order_list - TODO
    #        pairing    - TODO
    #        buy_num    - TODO
    # OUTPUT: TODO
    # DESCRIPTION:
    #   TODO
    def evaluatePairing(order_list, pairing, buy_num):

        # ERROR CHECK
        if order_list[buy_num][1] == None:
            print("ERROR IN EVALUATE PAIRING: BREAKING")
            return (0)

        # 1: VARIABLE SET UP
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

        # Temporary workaround for 0 quantity error [3/21/18]
        if arbitrage_quantity == 0:
            return_bool = True
        else: 
            return_bool = False
        # Needs to OUTPUT :
        return (arbitrage_quantity, sell_exchange, sell_price_limit, buy_exchange, buy_price_limit, profit, profit_ratio, return_bool)

    # FUNCTION: findCommonPairings
    # INPUT: exchange_one - string
    #        exchange_two - string
    # OUTPUT: list of pairings
    # DESCRIPTION:
    #   Goes through two exchange's list of pairings in order to find common pairings
    def findCommonPairings(exchange_one, exchange_two):
        exchange_one_p = DatabaseLibrary.getPairings(exchange_one)
        exchange_two_p = DatabaseLibrary.getPairings(exchange_two)
        return_list = []
        for pairing in exchange_one_p:
                return_list.append(pairing)
        return return_list

    # FUNCTION: getOrders
    # INPUT: exchange - string
    #        pairing  - string
    #        ask_list - passed in by reference
    #        bid_list - passed in by reference
    # OUTPUT: TODO
    # DESCRIPTION:
    #   Retrieves order books for a given pairing on a given exchange and builds a list
    #    of the combined asks and bids for each exchange. Each list is a list of lists,
    #    [[price, quantity, exchange, btc_value], ...].
    def getOrders(exchange, pairing, ask_list, bid_list):

        # Temporary workaround to make sure the program doesn't go over rate limit
        time.sleep(1)

        dict1 = ExchangeAPI.getOrderbook(exchange, pairing)
        if dict1["success"] == True:
            bids = dict1["bids"]
            asks = dict1["asks"]
            bids_length = len(bids)
            asks_length = len(asks)

            for bid in bids:
                price = float(bid[0])
                quantity = float(bid[1])
                btc_value = price * quantity
                bid_l = [price, quantity, exchange, btc_value]
                bid_list.append(bid_l)

            for ask in asks:
                price = float(ask[0])
                quantity = float(ask[1])
                btc_value = price * quantity
                ask_l = [price, quantity, exchange, btc_value]
                ask_list.append(ask_l)

            ask_list.sort(key=lambda x: x[0], reverse=False) # Ascending [lowest first]
            bid_list.sort(key=lambda x: x[0], reverse=True)  # Descending [highest first]

        return -1

    # FUNCTION: handle_incomplete_arbitrage
    # INPUT: sell_dict     - TODO
    #        sell_exchange - string
    #        buy_dict      - TODO
    #        buy_exchange  - string
    #        order_type    - TODO
    #        pairing       - string
    # OUTPUT: dictionary
    # DESCRIPTION:
    #   Hack solution to handle incomplete arbitrage for the time being
    # * - TODO, come back to this and devise a more comprehensive solution
    def handleIncompleteArbitrage(sell_dict, sell_exchange, buy_dict, buy_exchange, order_type, pairing):

        # ATTEMPT AGAIN IN 10S
        time.sleep(10)
        if order_type == 'Buy':
            ret_dict = ExchangeAPI.buyLimit(buy_exchange, pairing, buy_dict["quantity"], buy_dict["rate"])
        if order_type == 'Sell':
            ret_dict = ExchangeAPI.sellLimit(sell_exchange, pairing, sell_dict["quantity"], sell_dict["rate"])

        if ret_dict['success'] == 'True':
            ret_dict["incomplete_arbitrage"] = False
            return ret_dict

        # IF UNSUCCESSFUL: PLACE LIMIT ORDER ON ORIGINAL EXCHANGE
        if order_type == 'Buy':
            ret_dict = ExchangeAPI.buyLimit(buy_exchange, pairing, buy_dict["quantity"], buy_dict["rate"])
            ret_dict["incomplete_arbitrage"] = True
            return ret_dict
        if order_type == 'Sell':
            ret_dict = ExchangeAPI.sellLimit(sell_exchange, pairing, sell_dict["quantity"], sell_dict["rate"])
            ret_dict["incomplete_arbitrage"] = True
            return ret_dict


# CLASS: LimitArbitrage
# DESCRIPTION:
#   Container for all functions related to performing limit based arbitrage
class LimitArbitrage(object):
    def main():
        pass
