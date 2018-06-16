# External-Imports
import hashlib
import hmac
import json
import time
import requests
import sys

# Windows path
sys.path.append('U:/Directory/Projects/BlueTitan/Bots/Arbitrage/Libraries')

# Linux path
# sys.path.append()

# Internal-Imports
from PrintLibrary import PrintLibrary

# Secret Keys
from secret_keys import poloniex_private_key, poloniex_public_key 

# Endpoint URLs
base_url = ""

######################################## PUBLIC CALLS ##############################################
#################################################################################################### 

# FUNCTION: getTicker
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#    Returns ticker for all markets, optional input to just receive on currency.
def getTicker():
    pass

# FUNCTION: getVolume
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#    Returns 24hr volume for all markets, optional input to just receive one currency.
def getVolume():
    pass
    
######################################## MARKET CALLS ##############################################
#################################################################################################### 

# FUNCTION: getOrderbook
# INPUT: pairing - string
# OUTPUT: Dictionary
# DESCRIPTION:
#   Retrieves the orderbook for a given pairing. Output dictionary contains list of asks and bids,
#    ordered ascending and descending respectively.
def getOrderbook():
    pass

# FUNCTION: getTradeHistory
# INPUT: pairing - string
#        start   - int
#        end     - int
# OUTPUT: [(trade, ...), ...]
# DESCRIPTION:
#    Returns the past 200 trades for a given market, or up to 50,000 trades between range specific
#     in unix timpestamps by stat and end.
def getMarketHistory():
    pass

# FUNCTION: getChartData
# INPUT: pairing - string
#        period  - seconds (VALID: 300, 900, 1800, 7200, 1440, 86400)
#        start   - int
#        end     - int
# OUTPUT: dictionary
# DESCRIPTION:
#    Returns candlestick chart data for a given market pairing.
def getChartData():
    pass

# FUNCTION: getCurrencies
# INPUT: N/A
# OUTPUT: dictionary
# DESCRIPTION:
#    Returns information about [all] assets.
def getCurrencies():
    pass

# FUNCTION: getCurrency
# INPUT: asset - string
# OUTPUT: dictionary
# DESCRIPTION:
#    Returns information about an asset, calls getCurrencies.
def getCurrency():
    pass

# FUNCTION: getLoanOrders
# INPUT: asset - string
# OUTPUT: N/A
# DESCRIPTION:
#    TODO
def getLoanOrders():
    pass


######################################## ORDER CALLS ###############################################
####################################################################################################

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getOrderTrades():
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getOrder():
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getOpenOrders():
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def moveOrder():
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def cancelOrder():
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getTradeHistory():
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def postBuy():
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def buyLimit():
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def postSell():
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def sellLimit():
    pass

####################################### ACCOUNT CALLS ############################################## 
####################################################################################################

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getFeeInfo():
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getBalance():
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getBalances():
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getAvailableAccountBalances():
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getCompleteBalances():
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getDepositAddresses():
    # TODO
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getDepositAddress():
    # TODO
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def generateNewAddress():
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getDepositWithdrawals():
    # TODO
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getWithdrawals():
    # TODO
    pass

# FUNCTION: getDeposits
# INPUT: start - int (unix timestamp)
#        end   - int (unix timestamp)
# OUTPUT: Dictionary
# DESCRIPTION:
#    Retrieves deposit history for all assets, optional input of time period (start, end).
def getDeposits(start=0, end=0):
    # TODO
    pass

def getDepositsAsset():
    pass

# FUNCTION: withdraw
# INPUT: exchange - string
#        asset    - string
#        quantity - float
# OUTPUT: Dictionary
# DESCRIPTION:
#    Performs a withdraw call to a specified address.
def withdraw():
    pass

########################################## HELPERS #################################################
####################################################################################################
