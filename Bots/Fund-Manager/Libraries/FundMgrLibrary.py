# External Imports
import sys
import time

# Windows Main Desktop
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Crypto-API/Exchange_APIs')
sys.path.append('U:/Directory/Projects/BlueTitan/Components/DatabaseManager')

# Linux Main Server

# Internal Imports
from API import ExchangeAPI
import Helpers
from GeneralizedDatabase import GenDatabaseLibrary
from PrintLibrary import PrintLibrary

# CLASS: PTrackingLibrary
# FUNCTION LIST: [calculateMetrics, averageValue, calculateChange, sumBalances, sumProfit, sumVolume]
# DESCRIPTION:
#   Function library for the profit tracking components. More comprehensive description to come.
class MetricsCalculator(object):

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
        # TODO: change inputs here
        previous_tuple_metric = GeneralizedDatabase.getLastEntry(MetricsDatabase, "Metrics")
        previous_tuple_failure_metric = GeneralizedDatabase.getLastEntry(MetricsDatabase, "FailureMetrics")
        period = float(previous_tuple_metric[0])

        PrintLibrary.displayVariables(previous_tuple_metric, "Previous Metrics")
        PrintLibrary.displayVariables(previous_tuple_failure_metric, "Previous failureMetrics")

        # 2. Calculate derivative variables current period vs previous period
        balance_list = []
        for balance_a in balances:
            # TODO: Figure out these
            something = balance_a[0]
            something1 = balance_a[1]
            # TODO: change getBalance inputs
            previous_balance = GeneralizedDatabase.getBalance(balance_a[1], balance_a[0])
            balance = balance_a[2]
            btc_balance = balance_a[3]
            final_balance = balance_a[2]
            if final_balance != 0:
                delta_balance = PTrackingLibrary.calculateChange(previous_balance, final_balance)
            else:
                delta_balance = 0

            balance_tuple = (balance_a[0], balance_a[1], final_balance, delta_balance)
            balance_list.append(balance_tuple)
        
        PrintLibrary.displayVariables(balance_list, "Balances")

        # Get dictionary of lists --> profit_t["BTC"] --> [profit1, profit2, ...]

        # TODO: make this a bit more efficient, perhaps selectColumns
        columns = ["Profit", "Profit_ratio", "Total_btc"]
        columns_mining = [""]
        arbitrage_columns = GeneralizedDatabase.selectColumns("ArbitrageTrades", columns, period)
        failure_columns = GeneralizedDatabase.selectColumns("FailureTrades", columns, period)

        quantity_t = float(len(profit_t))
        quantity_f = float(len(profit_ratio_f))

        # FOR WHEN I GET AROUND TO THIS
        #     each asset should probably have its own table in the assetmetric database. Each call would then
        #      be indexing into the table with the asset name as the identifier. This portion should mimic
        #      the general
        # 3. Calculate individual asset metrics
        for asset in supportedassets:

            # Replacing getAssetMEtrics
            asset_tuple = GeneralizedDatabase.getEntry(asset)

            # Below needs correct inputs and needs to pull the asset metrics properly, need to work out how to implement this.
            pr = Helpers.averageValue()
            profit = Helpers.sumValues()
            volume = Helpers.sumValues()
            utilization = Helpers.calculateChange()
            quantity = float(len(profit_ratio_t[asset]))

            pr_delta = Helpers.calculateChange(asset_tuple[0], pr)
            profit_delta = Helpers.calculateChange(asset_tuple[1], profit)
            volume_delta = Helpers.calculateChange(asset_tuple[2], volume)
            utilization_delta = Helpers.calculateChange(asset_tuple[3], utilization)
            quantity_delta = Helpers.calculateChange(asset_tuple[4], quantity)

            # Failure database 
            volume_failures = sumVolume(volume_f[asset])
            utilization_failures = calculateUtilizaton(volume_failures, balances[asset])
            quantity_failures = float(len(volume_f[asset]))
            success_rate = quantity / quantity_failures 

            quantity_failures_delta = calculateChange(asset_tuple[5], quantity_failures)
            utilization_failures_delta = calculateChange(asset_tuple[6], utilization_failures)
            volume_failures_delta = calculateChange(asset_tuple[7], volume_failures)
            success_rate_delta = calculateChange(asset_tuple[8], success_rate)

            # Store metricAsset entry
            GenDatabaseLibrary.storeEntry()

        # 4. Calculate global asset metrics
        initial_balance = previous_tuple_metric[3]
        final_balance = PTrackingLibrary.sumBalances(balances)

        agg_pr = PTrackingLibrary.averageValue(profit_ratio_t)
        agg_profit = PTrackingLibrary.(profit_t)
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

class Liquidator(object):

    # FUNCTION: assessProfitPeriod
    # INPUT: TBD
    # OUTPUT: TBD
    # DESCRIPTION:
    #   Looks at the account balances for a period of time and determines how much
    #    profit there was. 
    def assessProfitPeriod():
        pass

    # FUNCTION: liquidateProfit
    # INPUT: ratio - int
    # OUTPUT:
    # DESCRIPTION:
    #   Attempts to liquidate given profit for a period of time
    def liquidateProfit(ratio):
        pass
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

