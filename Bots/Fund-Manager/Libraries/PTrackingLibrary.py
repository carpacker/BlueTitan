import sys

# SYS imports for PERSONAL DESKTOP
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Crypto-API/Exchange_APIs')
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Database-RD')

# SYS imports for MAIN ARBITRAGE SERVER
# 

# External Imports
import time

# Internal Imports
from PrintLibrary import PrintLibrary
from API import ExchangeAPI
import Helpers

from GeneralizedDatabase import GenDatabaseLibrary, SQLoperations

# CLASS: PTrackerHelpers
# FUNCTION LIST: [calculateMetrics, averageValue, calculateChange, sumBalances, sumProfit, sumVolume]
# DESCRIPTION:
#   Function library for the profit tracking components. More comprehensive description to come.
class PTrackingLibrary(object):

    # FUNCTION: calculateMetrics
    # INPUTS: period             - int
    #         balances           - TODO
    #         supportedexchanges - [string]
    #         supportedassets    - [string]
    # OUTPUT: integer (representing sucess or not)
    # DESCRIPTION:
    #   Calculates metric based on time period, grabs values from successful trades and from
    #    unsuccessful trades and then stores them in a new database.
    def calculateMetrics(balances, supportedexchanges, supportedassets):

        # 1. Retrieve the last entry
        previous_tuple_metric = DatabaseLibraryBase.getLastEntry(MetricsDatabase, "Metrics")
        previous_tuple_failure_metric = DatabaseLibraryBase.getLastEntry(MetricsDatabase, "FailureMetrics")
        period = float(previous_tuple_metric[0])
        PrintLibrary.displayVariables(previous_tuple_metric, "Previous Metrics")
        PrintLibrary.displayVariables(previous_tuple_failure_metric, "Previous failureMetrics")

        # 2. Calculate derivative variables current period vs previous period
        balance_list = []
        for balance_a in balances:
            previous_balance = DatabaseLibrary.getBalance(balance_a[1], balance_a[0])
            balance = balance_a[2]
            btc_balance = balance_a[3]
            final_balance = balance_a[2]
            if final_balance != 0:
                delta_balance = PTrackingLibrary.calculateChange(previous_balance, final_balance)
            else:
                delta_balance = 0

            # TUPLE OF (ASSET, EXCHANGE, BALANCE, CHANGE IN BALANCE)
            balance_tuple = (balance_a[0], balance_a[1], final_balance, delta_balance)
            balance_list.append(balance_tuple)
        
        PrintLibrary.displayVariables(balance_list, "Balances")
        connect, cursor = ArbitrageDatabase.connect()

        # Get dictionary of lists --> profit_t["BTC"] --> [profit1, profit2, ...]
        profit_t = DatabaseManager.selectColumn(cursor, "ArbitrageTrades", "Profit", period)
        profit_ratio_t = DatabaseManager.selectColumn(cursor, "ArbitrageTrades", "Profit_ratio", period)
        quantity_t = float(len(profit_t))
        volume_t = DatabaseManager.selectColumn(cursor, "ArbitrageTrades", "Total_btc", period)

        profit_f = DatabaseManager.selectColumn(cursor, "FailureTrades", "Profit", period)
        profit_ratio_f = DatabaseManager.selectColumn(cursor, "FailureTrades", "Profit_ratio", period)
        quantity_f = float(len(profit_ratio_f))
        volume_f = DatabaseManager.selectColumn(cursor, "FailureTrades", "Total_btc", period)

        # 3. Calculate individual asset metrics
        # for asset in supportedassets:
        #   FOR WHEN I GET AROUND TO THIS
        #       each asset should probably have its own table in the assetmetric database. Each call would then
        #        be indexing into the table with the asset name as the identifier. This portion should mimic
        #        the general
        #   asset_tuple = DatabaseLibrary.getAssetMetrics(asset, period)
        #   print(asset_tuple)

        #   print(profit_ratio_t)

        #   # SOME NOTES: 
        #   # Was currently working on doing asset metrics separately
        #   # Below needs correct inputs and needs to pull the asset metrics properly, need to work out how to implement this.
        #   # Once this is finished and works , I will implement the framework for mining databases
        #   # This will also need a USD value column thing-a-ma-jig 
        #   pr = Helpers.averagePR()
        #   profit = Helpers.sumProfit()
        #   volume = Helpers.sumVolume()
        #   utilization = Helpers.calculateUtilizaton()
        #   quantity = float(len(profit_ratio_t[asset]))

        #   pr_delta = DatabaseLibrary.calculateChange(asset_tuple[0], pr)
        #   profit_delta = DatabaseLibrary.calculateChange(asset_tuple[1], profit)
        #   volume_delta = DatabaseLibrary.calculateChange(asset_tuple[2], volume)
        #   utilization_delta = DatabaseLibrary.calculateChange(asset_tuple[3], utilization)
        #   quantity_delta = DatabaseLibrary.calculateChange(asset_tuple[4], quantity)

        #   # Failure database 
        #   volume_failures = sumVolume(volume_f[asset])
        #   utilization_failures = calculateUtilizaton(volume_failures, balances[asset])
        #   quantity_failures = float(len(volume_f[asset]))
        #   success_rate = quantity / quantity_failures 

        #   quantity_failures_delta = calculateChange(asset_tuple[5], quantity_failures)
        #   utilization_failures_delta = calculateChange(asset_tuple[6], utilization_failures)
        #   volume_failures_delta = calculateChange(asset_tuple[7], volume_failures)
        #   success_rate_delta = calculateChange(asset_tuple[8], success_rate)

        #   # Store metrics for specific asset in its database
        #   # Helpers.storeMetricsAsset()

        # 4. Calculate global asset metrics
        initial_balance = previous_tuple_metric[3]
        final_balance = PTrackingLibrary.sumBalances(balances)

        agg_pr = PTrackingLibrary.averageValue(profit_ratio_t)
        agg_profit = PTrackingLibrary.sumProfit(profit_t)
        agg_volume = PTrackingLibrary.sumProfit(volume_t)
        agg_utilization = PTrackingLibrary.calculateChange(final_balance, agg_volume)
        agg_quantity = quantity_t

        agg_volume_delta = PTrackingLibrary.calculateChange(previous_tuple_metric[5], agg_volume)
        agg_pr_delta = PTrackingLibrary.calculateChange(previous_tuple_metric[7], agg_pr)
        agg_profit_delta = PTrackingLibrary.calculateChange(previous_tuple_metric[9], agg_profit)
        agg_utilization_delta = PTrackingLibrary.calculateChange(previous_tuple_metric[11], agg_utilization)
        agg_quantity_delta = PTrackingLibrary.calculateChange(previous_tuple_metric[14], quantity_t)

        agg_pr_failures = PTrackingLibrary.averageValue(profit_ratio_f)
        agg_volume_failures = PTrackingLibrary.sumProfit(volume_f)
        agg_utilization_failures = PTrackingLibrary.calculateChange(final_balance, agg_volume_failures)
        agg_quantity_failures = quantity_f
        agg_success_rate = PTrackingLibrary.calculateChange(agg_quantity_failures, agg_quantity)

        quantity_s1 = 0
        quantity_s2 = 0
        agg_pr_failures_delta = PTrackingLibrary.calculateChange(previous_tuple_metric[10], agg_pr_failures)
        agg_quantity_failures_delta = PTrackingLibrary.calculateChange(previous_tuple_failure_metric[9], agg_quantity_failures)
        agg_utilization_failures_delta = PTrackingLibrary.calculateChange(previous_tuple_failure_metric[7], agg_utilization_failures)
        agg_volume_failures_delta = PTrackingLibrary.calculateChange(previous_tuple_failure_metric[3], agg_volume_failures)
        agg_success_rate_delta = PTrackingLibrary.calculateChange(previous_tuple_failure_metric[13], agg_success_rate)

        # TODO FIX SUPPORTED ASSETS STUFF
        success_values = ("", initial_balance, final_balance, agg_volume, agg_volume_delta, agg_pr, agg_pr_delta,
                            agg_profit, agg_profit_delta, agg_utilization, agg_utilization_delta, agg_quantity,
                            agg_quantity_delta)

        failure_values = ("", agg_volume_failures, agg_volume_failures_delta, agg_pr_failures, agg_pr_failures_delta,
                            agg_utilization_failures, agg_utilization_failures_delta, agg_quantity_failures, agg_quantity_failures_delta,
                            quantity_s1, quantity_s2, agg_success_rate, agg_success_rate_delta)


        Plist = (("Period", period), ("Sucess Rate", agg_success_rate), ("Profit", agg_profit), ("Profit Ratio", agg_pr),
                    ("Utilization", agg_utilization), ("Quantity Trades", agg_quantity))
        PrintLibrary.displayKeyVariables(Plist)

        # Store values
        DatabaseLibrary.storeMetric(success_values)
        DatabaseLibrary.storeFailureMetric(failure_values)

        DatabaseLibraryBase.disconnect(connect)
        return -1

    # FUNCTION: averageValue
    # INPUT: values - [float or number-as-string]
    # OUTPUT: float
    # DESCRIPTION:
    #   Takes an input list of values and averages them
    def averageValue(values):
        if values != []:
            average = 0
            for value in values:
                average += float(value[0])
            return_value = average / float(len(values))
            return return_value
        else:
            return 0

    # FUNCTION: calculateChange
    # INPUT: value_one - float
    #        value_two - float
    # OUTPUT: float
    #   TODO (Not sure what to do this with, its a bit too simple)
    def calculateChange(value_one, value_two):
        if value_one != 0:
            value = (value_two / value_one)
            return value
        else: 
            return value_two

    # FUNCTION: liquidateProfits
    # DESCRIPTION:
    #   Function that checks the profit margin for the day and sets aside a portion to be sold into USDT that 
    #    represents a 'cash out'
    def liquidateProfits():
        pass
        # 1. Access the profits for the day
        # 2. Determine the 'degree' of liquidation
        # 3. Liquidate the profits
        # 4. Store the results
        #   ^ -- need a new database for this

    # FUNCTION: retrieveAccountBalances
    # INPUTS: supportedexchanges - list of strings
    # OUTPUT: list of balances by exchange (alphabetical ordering)
    # DESCRIPTION:
    #   Creates a list that consists of the balances for each exchange we are using.
    def retrieveAccountBalances(supportedexchanges, supportedassets):
        balance_dict = {}
        for exchange in supportedexchanges:
            balance_dict[exchange] = ExchangeAPI.getBalances(exchange)

        ret_list = []
        for asset in supportedassets:
            for exchange in supportedexchanges:
                balance = balance_dict[exchange]["balances"][asset]["available_balance"]
                if asset != "BTC":
                    pairing = "BTC-" + asset 
                    price = ExchangeAPI.getPrice(exchange, pairing)
                    btc_balance = Helpers.btcValue(asset, balance, exchange)
                else: 
                    btc_balance = balance

                tuple_s = (asset, exchange, balance, btc_balance)
                ret_list.append(tuple_s)
                time.sleep(1)

        return ret_list # (ASSET, EXCHANGE, BALANCE)

    # FUNCTION: sumBalances
    # INPUT: balances - tuple (asset, exchange, value, BTCvalue)
    # OUTPUT: float
    # DESCRIPTION:
    #   Sums the value of assets in terms of BTC and outputs the final value
    # * - TODO - make this more robust... currently a bit simple and mostly a wrapper
    def sumBalances(balances):
        total = 0
        for balance in balances:
            total += balance[3]
        return total

    # FUNCTION: sumProfit
    # INPUT: profits - TODO
    # OUTPUT: TODO
    # DESCRIPTION:
    #   TODO
    # * - TODO, Input tuple already a list of profits from a period...
    # * - TODO, probably make this more robust...
    def sumProfit(profits):
        sum_profit = 0
        for value in profits:
            sum_profit += float(value[0])
        return sum_profit

    # FUNCTION: sumVolume
    # INPUT: initial_balances - float
    #        final_balances   - [float]
    # OUTPUT: volume[float]
    #   Sums up volume traded for period
    # * - TODO - This isn't right
    def sumVolume(initial_balance, final_balances):
        final_balance = sum(final_balances)
        volume = final_balance - initial_balance
        return volume

    # TESTER: testRun
    #   Used to fill up database with initial values to do some stress testing without running
    #    the main program.
    def testRun():
        pairing = "BTC-BAT"
        buy_exchange = 'binance'
        sell_exchange = 'bittrex'
        quantity = randint(0, 30)
        print(pairing[4:7])
        quantity_btc = Helpers.btcValue(quantity, pairing[4:7])
        buy_rate = ExchangeAPI.getPrice(buy_exchange, pairing)
        sell_rate = ExchangeAPI.getPrice(sell_exchange, pairing)
        profit = Helpers.calculateProfit(sell_rate, buy_rate, quantity)
        profit_ratio = Helpers.calculatePR(sell_rate, buy_rate)
        trade_one = (pairing, quantity, quantity_btc, quantity, buy_exchange, sell_exchange, buy_rate, sell_rate, profit_ratio, profit)

        pairing = "BTC-BAT"
        buy_exchange = 'binance'
        sell_exchange = 'bittrex'
        quantity = randint(0, 30)
        print(pairing[4:7])
        quantity_btc = Helpers.btcValue(quantity, pairing[4:7])
        buy_rate = ExchangeAPI.getPrice(buy_exchange, pairing)
        sell_rate = ExchangeAPI.getPrice(sell_exchange, pairing)
        profit = Helpers.calculateProfit(sell_rate, buy_rate, quantity)
        profit_ratio = Helpers.calculatePR(sell_rate, buy_rate)
        trade_two = (pairing, quantity, quantity_btc, quantity, buy_exchange, sell_exchange, buy_rate, sell_rate, profit_ratio, profit)

        # Fails
        pairing = "BTC-BAT"
        buy_exchange = 'binance'
        sell_exchange = 'bittrex'
        failed_exchange = 'binance'
        quantity = randint(0, 30)
        print(pairing[4:7])
        quantity_btc = Helpers.btcValue(quantity, pairing[4:7])
        buy_rate = ExchangeAPI.getPrice(buy_exchange, pairing)
        sell_rate = ExchangeAPI.getPrice(sell_exchange, pairing)
        profit = Helpers.calculateProfit(sell_rate, buy_rate, quantity)
        profit_ratio = Helpers.calculatePR(sell_rate, buy_rate)
        print("PR", profit_ratio)
        print("PROFIT", profit)
        fail_one = (pairing, quantity, quantity_btc, buy_exchange, sell_exchange, buy_rate, sell_rate, profit_ratio, profit, failed_exchange, 0, 0)

        fail_two = (pairing, quantity, quantity_btc, buy_exchange, sell_exchange, buy_rate, sell_rate, profit_ratio, profit, failed_exchange, 0, 0)
        fail_three = (pairing, quantity, quantity_btc, buy_exchange, sell_exchange, buy_rate, sell_rate, profit_ratio, profit, failed_exchange, 0, 0)
        fail_four = (pairing, quantity, quantity_btc, buy_exchange, sell_exchange, buy_rate, sell_rate, profit_ratio, profit, failed_exchange, 0, 0)

        DatabaseLibrary.storeArbitrage(trade_one)
        DatabaseLibrary.storeArbitrage(trade_two)

        DatabaseLibrary.storeFailedArbitrage(fail_one)
        DatabaseLibrary.storeFailedArbitrage(fail_two)
        DatabaseLibrary.storeFailedArbitrage(fail_three)
        DatabaseLibrary.storeFailedArbitrage(fail_four)

    # FOR TESTING PURPOSES
    def initializeMetrics():
        metric_one = ("BTC-BAT", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        failure_metric_one = ("BTC-BAT", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        DatabaseLibrary.storeMetric(metric_one)
        DatabaseLibrary.storeFailureMetric(failure_metric_one)  