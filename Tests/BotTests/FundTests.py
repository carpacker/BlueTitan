# CoinCatTests.py
#  BlueTitan Trading System
#  Carson Packer
#  Paq ltd.
# DESCRIPTION:
#    Testing suite for individual and combined calls for the coin categorizer system.

# External Imports
import osmnnw
import sys
import time

# Relative path for imports
sys.path.append(os.path.realpath('../../Components/Crypto-API/Exchange-APIs/'))
sys.path.append(os.path.realpath('../../Components/Libraries'))
sys.path.append(os.path.realpath('../../Components/Database-Manager'))

# Internal Imports
from API import ExchangeAPI
import Helpers
from GeneralizedDatabase import GenDatabaseLibrary
from PrintLibrary import PrintLibrary

# TESTER: AssetMetricsTests
def AssetMetricsTests():
    pass

# TESTER: MetricsTests
#   Used to fill up database with initial values to do some stress testing without running
#    the main program.
def MetricsTests():
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
