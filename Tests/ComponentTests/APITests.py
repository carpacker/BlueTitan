# APITests.py
# Carson Packer
# BlueTitan Testing System
# DESCRIPTION:
# Each function contains a series of tests for the respective exchange. There is also a test for  
#  the generic calls to each exchange. This testing suite is a bit long and parts may be commented
#  out for convenience. For instance, it may not make sense to test sells or buys over and over.

# External-Imports
import time
import sys
sys.path.append('U:/Directory/Projects/WorkBlueTitan/Components/Crypto-API/Exchange-APIs')
sys.path.append('U:/Directory/Projects/Work/BlueTitan/Components/Crypto-API/Main')
sys.path.append("U:/Directory/Projects/Work/BlueTitan/Components/Crypto-API/Mining-APIs")
sys.path.append('U:/Directory/Projects/Work/BlueTitan/Components/Libraries')

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

# EXCHANGE TESTS
class ExchangeTesters(object):

    def main():
        pass

    def
# TESTERS: Binance
def BinanceTesters():
    PrintLibrary.header("Binance Tests")
    PrintLibrary.delimiter()
    PrintLibrary.header("Public calls")
    
    # Standardize the below two
    Binance.checkServertime()
    Binance.getCurrencies()
    # Figure out what to do with this guy (getCurrencies uses it)
    Binance.getExchangeInfo()
    
    # Test (2 right, 1 wrong)
    Binance.getInfoPairing("BTC-ETH")
    Binance.getInfoPairing("BTC-FUN")
    Binance.getInfoPairing("BTC-SMT")

    Binance.getInfoPairings()
    Binance.getInfoPairings()
    Binance.getInfoPairings()

    Binance.testConnectivity()
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

if __name__ == "__main__": 
    # BinanceTesters()
    # BittrexTesters()
    # CoinMarketCapTesters()
    # CryptopiaTesters()
    # GdaxTesters()
    # KucoinTesters()
    PoloniexTesters()
    CoinbaseTesters()
    # GenericTesters()
