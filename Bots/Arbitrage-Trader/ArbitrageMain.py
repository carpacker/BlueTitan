# ArbitrageMain.py
# Carson Packer
# DESCRIPTION:
#    Top level file for arbitrage, automatically handles and executes arbitrage trading.

# External-Imports
from copy import deepcopy
import math 
import schedule
import sys
import threading
import time

# WINDOWS main-desktop
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Database-Manager')
# Rest of these

# WINDOWS laptop
# sys.path.append()

# LINUX main-server
# sys.path.append()

# Internal-Imports
from API import ExchangeAPI
from ArbitrageLibrary import ArbitrageLibrary
from BalancingLibrary import BalancingLibrary
from GeneralizedDatabase import GenDatabaseLibrary
import Helpers
from PrintLibrary import PrintLibrary

# CLASS: [B]lue[T]itanArbitrage
# DESCRIPTION:
#    Container arbitrage for the low-liquidity arbitrage component. This is the main loop for
#     arbitrage and can be considered the top-level. Manages all arbitrage events and activities,
#     which includes both market and limit arbitrage.
class BTArbitrage(object):

    # Class Variables [Exchanges, Pairings, Assets, Balances]
    cl_exchanges = ['bittrex', 'binance']
    cl_pairings = ['BTC-KMD', 'BTC-ADA', 'BTC-ARK', 'BTC-XVG']
    cl_assets = ['BTC', 'ARK', 'KMD', 'XVG', 'ADA']
    cl_balance_dict = {}

    # INITIALIZATION
    # INPUT: Clean - Used to designate whether to clean databases on initialization. Defaults to True.
    # DESCRIPTION:
    #   Performs necessary tasks to begin Arbitrage. Grabs input variables
    def __init__(self, clean=True, exchanges, pairings, assets):
		# Initialize local variables
		cl_exchanges = exchanges
		cl_pairings = pairings
		cl_assets = assets

		# Grab balance dict
        cl_balance_dict = DatabaseLibrary.getAllBalances(exchanges)
        PrintLibrary.displayDictionary("Initialized balances", cl_balance_dict)
		
    # FUNCTION: Arbitrage [Top Level]
    # DESCRIPTION:
    #   Main function for arbitrage that acts as the top level.
    def Arbitrage(self):

        # Local Variable initialization
        exchanges = LowLiquidityArbitrage.cl_exchanges
        pairings = LowLiquidityArbitrage.cl_pairings 
        assets = LowLiquidityArbitrage.cl_assets
        ticker = 0
        consecutive_fails = 0

        # Scheduled Events
        #

        # Main arbitrage loop -
		#  1. checks for events
		#  2. market arbitrage actions
		#  3. limit arbitrage actions
        while 1:
            header_string = "MAIN ARBITRAGE LOOP: Iteration " + str(ticker) + " at " + Helpers.convertFromUnix(Helpers.createTimestamp())
            PrintLibrary.header(header_string)
            
            # Check schedule for events waiting to be run
            schedule.run_pending()

			# Market Arbitrage
            for pairing in pairings:
                time.sleep(2) # For rate limits

                # Variable setup
                base, quote = pairing.split("-")
                order_list = [] 
                thread_list = [] 
                thread_count = 0
                
                header_string = "Current Arbitrage Pairing : " + quote
                PrintLibrary.header2(header_string)

                # FOR each EXCHANGE --> call getOrders [for the given pairing]
                for ex in exchanges:
                    order_list.append( (ex, [], []) )
                    t = threading.Thread(target=ArbitrageLibrary.getOrders, args=(ex, pairing, order_list[thread_count][1], order_list[thread_count][2]))
                    thread_count += 1
                    thread_list.append(t)
                    t.start()
                [t.join() for t in thread_list]

                # Evaluate pairings for each bid-ask pairing -- [B1>A2 & B2>A1]
                bidask_one = ArbitrageLibrary.evaluatePairing(order_list, pairing, 0)
                bidask_two = ArbitrageLibrary.evaluatePairing(order_list, pairing, 1)


                # TODO: storeFailedArbitrage Prints
                # IF the evaluate pairing failed [no profitable arbitrage] --> Store failed arbitrage for each case
                if bidask_one[7] == True:
                    total_btc  = ArbitrageLibrary.baseAsset(bidask_one[0], bidask_one[4])
                    failed_tuple = (pairing, bidask_one[0], total_btc, bidask_one[3], bidask_one[1], bidask_one[4], bidask_one[2],
                                bidask_one[6], bidask_one[5], "N/A", 1, consecutive_fails)
                    DatabaseLibrary.storeFailedMArbitrage(failed_tuple)
                if bidask_two[7] == True:
                    total_btc  = ArbitrageLibrary.baseAsset(bidask_two[0], bidask_two[4])
                    failed_tuple = (pairing, bidask_two[0], total_btc, bidask_two[3], bidask_two[1], bidask_two[4], bidask_two[2],
                                bidask_two[6], bidask_two[5], "N/A", 1, consecutive_fails)
                    DatabaseLibrary.storeFailedMArbitrage(failed_tuple)

                # Choose most profitable evaluated pairing
                # * - (arbitrage_quantity, sell_exchange, sell_price_limit, buy_exchange, buy_price_limit, profit, profit_ratio)
                order_tuple = max([bidask_one, bidask_two], key=lambda x:x[5])

                PrintLibrary.displayVariables(order_tuple, "BIDASK pairing")

                # * - 'Profit' Boolean Conditional
                if order_tuple[7] == True:
                    consecutive_fails += 1
                    header_string = "FAILURE(" + str(consecutive_fails) + "): Not Profitable Arbitrage"
                    PrintLibrary.displayVariable(header_string, "Top Level")
                    continue

                # (arbitrage_quantity, sell_exchange, sell_price_limit, buy_exchange, buy_price_limit,pairing, exchange_one_quote, 
                #   exchange_one_base, exchange_two_quote, exchange_two_base)
                input_tuple = order_tuple[:-3] + (pairing,)
                return_balances = self.executeArbitrage(input_tuple)

                # Temporary work around -- TODO, create more robust stage detection
                if return_balances == 2 or return_balances == 3:
                    failed_tuple = (pairing, order_tuple[0], total_btc, order_tuple[3], order_tuple[1], order_tuple[4], order_tuple[2],
                                    order_tuple[6], order_tuple[5], "N/A", return_balances, consecutive_fails)
                    DatabaseLibrary.storeFailedArbitrage(failed_tuple)
                else:              
                    # Reset consecutive_fails variable
                    consecutive_fails = 0
                    PrintLibrary.displayVariables(return_balances, "Execute Arbitrage Output")
                    time.sleep(5)
                    BalancingLibrary.balanceFAE(quote, return_balances)

                time.sleep(1)

            # Global Actions
            # TODO

            ticker+=1


    # FUNCTION: executeArbitrage
    # INPUT: TODO
    # OUTPUT:  TODO
    # DESCRIPTION:
    #     Main function for executing market-based arbitrage
    def executeArbitrage(input_tuple):
        PrintLibrary.header("Execute Arbitrage")
        PrintLibrary.delimiter()
        # Initialize Variables
        quantity, sell_exchange, sell_price, buy_exchange, buy_price, pairing  = input_tuple
        base, quote = pairing.split("-")

        # Update balances from database
        sell_balance_quote = DatabaseLibrary.getBalance(quote, sell_exchange)
        sell_balance_base = DatabaseLibrary.getBalance(base, sell_exchange)
        buy_balance_base = DatabaseLibrary.getBalance(base, buy_exchange)
        buy_balance_quote = DatabaseLibrary.getBalance(quote, buy_exchange)

        # Convert price & quantity to appropiate standard such that each exchange
        #  will accept the parameter.
        buy_price = ArbitrageLibrary.convertMinPrice(buy_exchange, buy_price, pairing)
        sell_price = ArbitrageLibrary.convertMinPrice(sell_exchange, sell_price, pairing)
        quantity_buy = ArbitrageLibrary.convertMinQuantity(buy_exchange, quantity, pairing)
        quantity_sell = ArbitrageLibrary.convertMinQuantity(sell_exchange, quantity, pairing)

        result = ArbitrageLibrary.decideOrder(buy_exchange, sell_exchange)
        PrintLibrary.displayVariables([sell_balance_quote, sell_balance_base, buy_balance_quote], "Sell quote/base, buy quote/base going into arbitrage")
        if result == True:
            sell_id_one = ExchangeAPI.sellLimit(sell_exchange, pairing, quantity_sell, sell_price)
            if sell_id_one["success"] != True:
                print(' ERROR [executeArbitrage, order ONE sell_order_failed]')
                return 2
            time.sleep(2)
            print("sell_id_one", sell_id_one)
            order_dict_sell1 = ExchangeAPI.getOrder(sell_exchange, sell_id_one["order_id"], pairing)
            print("order sell 1", order_dict_sell1)
            # CASE: None of value has been executed :: cancel and exit
            if order_dict_sell1["incomplete"] == True:
                print("INCOMPLETE ARBITRAGE")
                ExchangeAPI.cancelOrder(sell_exchange, sell_id_one["order_id"], pairing)
                if order_dict_sell1["executed_quantity"] == 0:
                    print("Execution FAILED: Returning")
                    return 2
                if order_dict_sell1["success"] == True:
                    #checkMinimumOrder
                    quantity = float(order_dict_sell1['executed_quantity'])
                    quantity = ArbitrageLibrary.convertMinQuantity(buy_exchange, quantity, pairing)
            else:
                quantity = quantity_sell

            print("FIRST ORDER SUCCESS SELL")
            print("QUANTITY = " + str(quantity))
            print("INCOMPLETE = " + str(order_dict_sell1["incomplete"]))
        else:
            buy_id_one = ExchangeAPI.buyLimit(buy_exchange, pairing, quantity_buy, buy_price)
            print(buy_id_one)
            if buy_id_one["success"] != True:
                print(' ERROR [executeArbitrage, order ONE : buy_order_failed ]')
                return 2
            time.sleep(3)
            order_dict_buy1 = ExchangeAPI.getOrder(buy_exchange, buy_id_one["order_id"], pairing)
            print("order buy 1 ", order_dict_buy1)
            # CASE: None of value has been executed :: cancel and exit
            if order_dict_buy1["incomplete"] == True:
                ExchangeAPI.cancelOrder(buy_exchange, buy_id_one["order_id"], pairing)
                if order_dict_buy1["executed_quantity"] == 0:
                    print("Execution FAILED: Returning")
                    return 2
                if order_dict_buy1["success"] == True:
                    #checkMinimumOrder
                    quantity = float(order_dict_buy1['executed_quantity'])
                    quantity = ArbitrageLibrary.convertMinQuantity(sell_exchange, quantity, pairing)
            else: 
                quantity = quantity_sell

            print("FIRST ORDER SUCCESS BUY")
            print("QUANTITY = " + str(quantity))
            print("INCOMPLETE = " + str(order_dict_buy1["incomplete"]))

        # Fix notional, lot size
        stage = PrintLibrary.stageHeader("Second Order", stage)
        if result == True:
            sell_dict = order_dict_sell1
            print("buyprice: ", buy_price)
            buy_id_two = ExchangeAPI.buyLimit(buy_exchange, pairing, quantity, buy_price)
            print(buy_id_two)
            if buy_id_two["success"] != True:
                print(' ERROR [executeArbitrage, order TWO : buy_order_failed]')
                order_dict_buy2 = {}
                order_dict_buy2["quantity"] = quantity
                order_dict_buy2["rate"] = buy_price
                incomplete_arbitrage_dict = ArbitrageLibrary.handleIncompleteArbitrage(sell_dict, sell_exchange, order_dict_buy2, buy_exchange, 'Buy', pairing)
                return 3

            order_dict_buy2 = ExchangeAPI.getOrder(buy_exchange, buy_id_two["order_id"], pairing)
            executed_quantity = float(order_dict_buy2["executed_quantity"])
            buy_dict = order_dict_buy2

            print("SECOND ORDER SUCCESS (SELL FIRST):")
            print("QUANTITY = " + str(executed_quantity))
            print("BUY_DICT = ", buy_dict)
        else:
            buy_dict = order_dict_buy1
            print("sellPrice: ", sell_price)
            sell_id_two = ExchangeAPI.sellLimit(sell_exchange, pairing, quantity, sell_price)
            print(sell_id_two)
            if sell_id_two["success"] != True:
                print(' ERROR [executeArbitrage, order TWO : sell_order_failed]')
                order_dict_sell2 = {}
                order_dict_sell2["quantity"] = quantity
                order_dict_sell2["rate"] = buy_price
                incomplete_arbitrage_dict = ArbitrageLibrary.handleIncompleteArbitrage(order_dict_sell2, sell_exchange, buy_dict, buy_exchange, 'Sell', pairing)
                return 3


            order_dict_sell2 = ExchangeAPI.getOrder(sell_exchange, sell_id_two["order_id"], pairing)
            executed_quantity = float(order_dict_sell2["executed_quantity"])
            sell_dict = order_dict_sell2

            print("SECOND ORDER SUCCESS (BUY FIRST):")
            print("QUANTITY = " + str(executed_quantity))
            print("SELL_DICT = ", sell_dict)

        sell_price = float(sell_dict["rate"])
        buy_price = float(buy_dict["rate"])
        print(sell_price, "sellPrice")
        print(buy_price, "buyPrice")

        stage = PrintLibrary.stageHeader("Calculate Profits", stage)
        pr = Helpers.calculatePR(sell_price, buy_price)
        profit = Helpers.calculateProfit(sell_price, buy_price, executed_quantity)

        stage = PrintLibrary.stageHeader("Update Account Balances", stage)
        quant_float = float(executed_quantity)
        total_btc_sell = ArbitrageLibrary.baseAsset(quant_float, sell_price)
        total_btc_buy = ArbitrageLibrary.baseAsset(quant_float, buy_price)
        total_btc  =  total_btc_sell + total_btc_buy

        sell_balance_base += total_btc_sell
        sell_balance_quote -= quant_float
        buy_balance_base -= total_btc_buy
        buy_balance_quote += quant_float

        DatabaseLibrary.updateBalance(sell_exchange, base, sell_balance_base)
        DatabaseLibrary.updateBalance(sell_exchange, quote, sell_balance_quote)
        DatabaseLibrary.updateBalance(buy_exchange, base, buy_balance_base)
        DatabaseLibrary.updateBalance(buy_exchange, quote, buy_balance_quote)

        init_quantity = input_tuple[0]
        packed_info = pairing, init_quantity, total_btc, executed_quantity, buy_exchange, sell_exchange, buy_price, sell_price, pr, profit
        print(packed_info)
        DatabaseLibrary.storeArbitrage(packed_info)

        result = (pairing, sell_exchange, buy_exchange, sell_balance_base, sell_balance_quote, buy_balance_base, buy_balance_quote)
            
        print(result)
        return result

if __name__ == '__main__':
    LowLiquidityArbitrage().Arbitrage()
