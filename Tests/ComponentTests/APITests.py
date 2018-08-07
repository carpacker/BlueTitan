# APITests.py
#  Carson Packer
#  BlueTitan Trading System
#  Testing Suite for API
# DESCRIPTION:
#    Each function contains a series of tests for the respective exchange. There is also a test for  
#     the generic calls to each exchange. This testing suite is a bit long and parts may be
#     commented out for convenience. For instance, it may not make sense to test sells or buys over
#     and over.

# External-Imports
import os
import sys
import time

# Relative path for imports
sys.path.append(os.path.realpath('../../Components/Crypto-API/Exchange-APIs/'))
sys.path.append(os.path.realpath('../../Components/Crypto-API/Mining-APIs/'))
sys.path.append(os.path.realpath('../../Components/Libraries'))
sys.path.append(os.path.realpath('../../Components/Database-Manager'))

# Internal-Imports
from PrintLibrary import PrintLibrary

# Exchanges
from API import ExchangeAPI
import Bittrex
import Binance
import Coinbase
import CoinMarketCap
import Cryptopia
import Gdax
import Kucoin
import Poloniex

# Mining
from API import MiningAPI
import Ethermine
import Siamining

# Exchange Tests
# DESCRIPTION:
#    Tests exchange calls.
class ExchangeTesters(object):

    # MAIN
    # DESCRIPTION:
    #    Calls each suite of exchange testers and then the generic testers.
    def main():
        BinanceTesters()
        BittrexTesters()
        CoinMarketCapTesters()
        CryptopiaTesters()
        GdaxTesters()
        KucoinTesters()
        PoloniexTesters()
        CoinbaseTesters()
        GenericTesters()
        
    # TESTERS: Binance
    def BinanceTesters():
        PrintLibrary.header("Binance Tests")
        PrintLibrary.delimiter()
        PrintLibrary.header("Public calls")

        PrintLibrary.delimiter()
        PrintLibrary.header("checkServerTime")
        PrintLibrary.displayDictionary(Binance.checkServertime())
        PrintLibrary.delimiter()

        PrintLibrary.header("getCurrencies")
        PrintLibrary.displayDictionary(Binance.getCurrencies())
        PrintLibrary.delimiter()

        PrintLibrary.header("getExchangeInfo")
        Binance.getExchangeInfo()
        PrintLibrary.delimiter()

        PrintLibrary.header("getInfoPairing, getInfoPairings")
        # Test (2 right, 1 wrong)
        PrintLibrary.displayDictionary(Binance.getInfoPairing("BTC-ETH"))
        PrintLibrary.displayDictionary(Binance.getInfoPairing("BTC-FUN"))
        PrintLibrary.displayDictionary(Binance.getInfoPairing("BTC-SMT"))
        
        PrintLibrary.displayDictionary(Binance.getInfoPairings())
        PrintLibrary.displayDictionary(Binance.getInfoPairings())
        PrintLibrary.displayDictionary(Binance.getInfoPairings())
        PrintLibrary.delimiter()

        PrintLibrary.header("testConnectivity")
        PrintLibrary.displayDictionary(Binance.testConnectivity())
        PrintLibrary.header("Market Calls")
        
        PrintLibrary.header("Order Calls")
        
    # TESTERS: Bittrex
    def BittrexTesters():
        PrintLibrary.header("Bittrex Tests")

    # TESTERS: Coinbase
    def CoinbaseTesters():
        PrintLibrary.header("Coinbase Tests")
        PrintLibrary.displayDictionary(Coinbase.getTime())
        PrintLibrary.displayDictionary(Coinbase.getAccounts())
        PrintLibrary.displayDictionary(Coinbase.listTransactions())
    
    # TESTERS: CoinMarketCap
    def CoinMarketCapTesters():
        PrintLibrary.header("CoinMarketCap Tests")

        # Base calls
        CoinMarketCap.getGlobal()
        time.sleep(60)
        CoinMarketCap.getTicker()
        time.sleep(60)
        CoinMarketCap.getTickerId("BTC")
        time.sleep(60)
        CoinMarketCap.getTickerId("ARK")

        # Base calls: Limit/Start tests

        # Derivative calls
        CoinMarketCap.getPriceUSD()
        time.sleep(60)
        CoinMarketCap.getPriceBTC()
        time.sleep(60)

    # TESTERS: Cryptopia
    # * DEPRECATED
    def CryptopiaTesters():
        pass

    # TESTERS: Gdax
    def GdaxTesters():
        PrintLibrary.header("Gdax Tests")

    # TESTERS: Kucoin
    def KucoinTesters():
        PrintLibrary.header("Kucoin Tests")

    # TESTERS: Poloniex
    def PoloniexTesters():
        PrintLibrary.header("Poloniex Tests")

        PrintLibrary.header("Public Calls")
        PrintLibrary.displayDictionary(Poloniex.getTicker())
        PrintLibrary.displayDictionary(Poloniex.getVolume())
        
        PrintLibrary.header("Accounts calls")
        PrintLibrary.displayDictionary(Poloniex.getDepositWithdrawals("as-is"))
                                   
    # TESTERS: Generic
    def GenericTesters():
        PrintLibrary.header("Generic Tests")


    # TESTERS: ethermine
    # DESCRIPTION:
    #   Tests each ethermine call individually and prints the results. Each result has a header for
    #    what function is being tested.
    def ethermineTests():
        PrintLibrary.header("Ethermine Tests")
        PrintLibrary.displayDictionary(Ethermine.getPoolStats(), "getPoolStats")
        time.sleep(5)
        PrintLibrary.displayDictionary(Ethermine.getNetworkStats(), "getNetworkStats")
        time.sleep(5)
        PrintLibrary.displayDictionary(Ethermine.getHashrates(), "getHashrates")
        time.sleep(5)
        PrintLibrary.displayDictionary(Ethermine.getMinerHistory(), "getMinerHistory")
        time.sleep(5)
        PrintLibrary.displayDictionary(Ethermine.getMinerPayouts(), "getMinerPayouts")
        time.sleep(5)
        PrintLibrary.displayDictionary(Ethermine.getMinerRounds(), "getMinerRounds")
        time.sleep(5)
        PrintLibrary.displayDictionary(Ethermine.getMinerStatistics(), "getMinerStatistics")
        time.sleep(5)
        PrintLibrary.displayDictionary(Ethermine.getWorkStatisticsAll(), "getWorkStatisticsAll")
        time.sleep(5)
        PrintLibrary.displayDictionary(Ethermine.getWorkerHistory(), "getWorkerHistory")
        time.sleep(5)
        PrintLibrary.displayDictionary(Ethermine.getWorkerStatistics(), "getWorkerStatistics")
        time.sleep(5)
        PrintLibrary.displayDictionary(Ethermine.getWorkerMonitor(), "getWorkerMonitor")

    # TESTERS: siamining
    # DESCRIPTION:
    #   Tests each ethermine call individually and prints the results. Each result has a header for
    #    what function is being tested.
    def siaminingTests():
        pass

    # TESTERS: generic
    # DESCRIPTION:
    #   Tests the generic API for mining. It makes a call to each supported site in order to verify
    #    that each generic function works.
    def genericTests():
	    pass

# MINING TESTS
class MiningTesters(object):

    # Call all the testers here
    def main():
        ethermineTests()
        siaminingTests()
        genericTests()

    # TESTERS: Generic implementation
    def genericTests():
        pass

    # TESTERS: Ethermine.com
    def ethermineTests():
        pass

    # TESTERS: Siamining.com
    def siaminingTests():
        pass
if __name__ == "__main__": 

