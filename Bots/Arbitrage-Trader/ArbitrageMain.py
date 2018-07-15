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
sys.path.append('U:/Directory/Projects/Work/BlueTitan/Components/Database-Manager')
sys.path.append('U:/Directory/Projects/Work/BlueTitan/Components/Libraries')
sys.path.append('U:/Directory/Projects/Work/BlueTitan/Components/Crypto-API/Exchange-APIs')

# WINDOWS laptop
#sys.path.append('C:/Directory/Projects/Work/BlueTitan/Components/DatabaseManager')
#sys.path.append('C:/Directory/Projects/Work/BlueTitan/Components/Libraries')
#sys.path.append('C:/Directory/Projects/Work/BlueTitan/Components/Crypto-API/Exchange-APIs')

# LINUX main-server
#sys.path.append('U:/Directory/Projects/Work/BlueTitan/Components/Database-Manager')
#sys.path.append('U:/Directory/Projects/Work/BlueTitan/Components/Libraries')
#sys.path.append('U:/Directory/Projects/Work/BlueTitan/Components/Crypto-API/Exchange-APIs')# sys.path.append()

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
    cl_exchanges = []
    cl_pairings = []
    cl_assets = []
    cl_balance_dict = {}
    consecutive_fails = 0
    ticker = 0
    
    # INITIALIZATION
    # INPUT: Clean - Used to designate whether to clean databases on initialization. Defaults to True.
    # DESCRIPTION:
    #   Performs necessary tasks to begin Arbitrage. Grabs input variables
    def __init__(self, exchanges, m_pairings, l_pairings, assets):
        
		# Initialize local variables
		cl_exchanges = exchanges
		cl_market_pairings = m_pairings
        cl_limit_pairings = l_pairings
		cl_assets = assets
        cl_balance_dict = GenDatabaseLibrary.getAllBalances("ArbitrageDatabase", exchanges)
        PrintLibrary.displayDictionary("Initialized balances", cl_balance_dict)

    # FUNCTION: Arbitrage [Top Level]
    # DESCRIPTION:
    #   Main function for arbitrage that acts as the top level.
    def Arbitrage(self):

        # Local Variable initialization
        exchanges = self.cl_exchanges
        market_pairings = self.cl_market_pairings
        limit_pairings = self.cl_limit_pairings
        assets =  self.cl_assets
    
        header_string = "MAIN ARBITRAGE LOOP: Iteration " + str(self.ticker) + " at " + Helpers.convertFromUnix(Helpers.createTimestamp())
        PrintLibrary.header(header_string)

        PrintLibrary.header("Limit Arbitrage Loop")
        for pairing in limit_pairings:
            pass
            # 1. Check existing limit arbitrage
            # 2. Handle existing limit arbitrage
            # 3. Create new limit arbitrage

        PrintLibrary.header("Market Arbitrage Loop")
        for pairing in market_pairings:
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


            # IF the evaluate pairing failed [no profitable arbitrage] --> Store failed arbitrage for each case
            if bidask_one[7] == True:
                total_btc  = Helpers.baseAsset(bidask_one[0], bidask_one[4])
                failed_tuple = (pairing, bidask_one[0], total_btc, bidask_one[3], bidask_one[1], bidask_one[4], bidask_one[2],
                            bidask_one[6], bidask_one[5], "N/A", 1, consecutive_fails)
                GenDatabaseLibrary.storeEntry("ArbitrageFailureMetrics", failed_tuple)
            if bidask_two[7] == True:
                total_btc  = Helpers.baseAsset(bidask_two[0], bidask_two[4])
                failed_tuple = (pairing, bidask_two[0], total_btc, bidask_two[3], bidask_two[1], bidask_two[4], bidask_two[2],
                            bidask_two[6], bidask_two[5], "N/A", 1, consecutive_fails)
                GenDatabaseLibrary.storeEntry("ArbitrageFailureMetrics", failed_tuple)

            # Choose most profitable evaluated pairing
            # * - (arbitrage_quantity, sell_exchange, sell_price_limit, buy_exchange, buy_price_limit, profit, profit_ratio)
            order_tuple = max([bidask_one, bidask_two], key=lambda x:x[5])
            
            PrintLibrary.displayVariables(order_tuple, "BID/ASK pairing")

            # * - 'Profit' Boolean Conditional
            if order_tuple[7] == True:
                self.consecutive_fails += 1
                header_string = "FAILURE(" + str(consecutive_fails) + "): Not Profitable Arbitrage"
                PrintLibrary.displayVariable(header_string)
                continue

            # (arbitrage_quantity, sell_exchange, sell_price_limit, buy_exchange, buy_price_limit,pairing, exchange_one_quote, 
            #   exchange_one_base, exchange_two_quote, exchange_two_base)
            input_tuple = order_tuple[:-3] + (pairing,)
            return_balances = self.marketArbitrage(input_tuple)

            # TempTODO, create more robust stage detection
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

        self.ticker+=1


    # FUNCTION: marketArbitrage
    # INPUT: TODO
    # OUTPUT:  TODO
    # DESCRIPTION:
    #     Main function for executing market-based arbitrage.
    def marketArbitrage(input_tuple):
        PrintLibrary.header("Market Arbitrage")
        PrintLibrary.delimiter()
        
        # Initialize Variables
        quantity, sell_exchange, sell_price, buy_exchange, buy_price, pairing  = input_tuple
        base, quote = pairing.split("-")

        # Update balances from database
        sell_balance_quote = GenDatabaseLibrary.getItem("ArbitrageDatabase", quote, sell_exchange)
        sell_balance_base = GenDatabaseLibrary.getItem("ArbitrageDatabase", base, sell_exchange)
        buy_balance_base = GenDatabaseLibrary.getItem("ArbitrageDatabase", base, buy_exchange)
        buy_balance_quote = GenDatabaseLibrary.getItem("ArbitrageDatabase", quote, buy_exchange)

        # Convert price & quantity to appropiate standard such that each exchange
        #  will accept the parameter.
        buy_price = TradingLibrary.convertMinPrice(buy_exchange, buy_price, pairing)
        sell_price = TradingLibrary.convertMinPrice(sell_exchange, sell_price, pairing)
        quantity_buy = TradingLibrary.convertMinQuantity(buy_exchange, quantity, pairing)
        quantity_sell = TradingLibrary.convertMinQuantity(sell_exchange, quantity, pairing)

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
