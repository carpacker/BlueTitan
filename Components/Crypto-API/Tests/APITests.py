# External-Imports
import time
import sys
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Crypto-API/Exchange_APIs')
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Crypto-API/Main')

# Internal-Imports
from PrintLibrary import PrintLibrary
from API import ExchangeAPI
import Bittrex
import Binance
import CoinMarketCap
import Cryptopia
import Gdax
import Kucoin
import Poloniex

###################################################################################################
# Each function contains a series of tests for the respective exchange. There is also a test for  #
#  the generic calls to each exchange. This testing suite is a bit long and parts may be commented#
#  out for convenience. For instance, it may not make sense to test sells or buys over and over   #
###################################################################################################

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

# TESTERS: CoinMarketCap
def CoinMarketCapTesters():
    PrintLibrary.header("CoinMarketCap Tests")

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

# TESTERS: Generic
def GenericTesters():
    PrintLibrary.header("Generic Tests")
    

if __name__ == "__main__": 
    BinanceTesters()
    BittrexTesters()
    CoinMarketCapTesters()
    CryptopiaTesters()
    GdaxTesters()
    KucoinTesters()
    PoloniexTesters()
    GenericTesters()
