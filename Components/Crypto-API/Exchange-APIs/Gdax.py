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
from secret_keys import gdax_private_key, gdax_public_key 

# Endpoint URLs
base_url = "https://api.gdax.com"
web_socket = "wss://ws-feed.gdax.com"
fix_url = "tcp+ssl://fix.gdax.com:4198"


######################################## PUBLIC CALLS ##############################################
# * - getTime : retrieves server time                                                              #
#################################################################################################### 
# FUNCTION: getTime
# INPUT: N/A
# OUTPUT: float
# DESCRIPTION:
#   Retrieves server time.
def getTime():
    pass

######################################## MARKET CALLS ##############################################
#################################################################################################### 
def getProducts():
    pass

# FUNCTION: getOrderbook
# INPUT: pairing - string
# OUTPUT: Dictionary
# DESCRIPTION:
#   Retrieves the orderbook for a given pairing. Output dictionary contains list of asks and bids,
#    ordered ascending and descending respectively.
# NOTE: NOT paginated, websocket recommended for up to date information
def getOrderbook():
    pass

def getProductsTicker():
    pass

def getProductsTrades():
    pass

# Historic rates
def getProductsCandles():
    pass

def getProducts24hrStats():
    pass

def getCurrencies():
    pass


######################################## ORDER CALLS ###############################################
####################################################################################################

def postOrder():
    pass

def cancelOrder():
    pass

def cancelAll():
    pass

def getAllOrders():
    pass

def getOpenOrders():
    pass

def getClosedOrders():
    pass

def getOrder():
    pass

def getFills():
    pass

####################################### ACCOUNT CALLS ############################################## 
####################################################################################################


def getAccounts():
    pass

def getAccount():
    pass

def getAccountsLedger():
    pass

def getAccountsHolds():
    pass

def postDepositsPayment():
    pass

def postDepositsCoinbase():
    pass

def postWithdrawalCoinbase():
    pass

def postWithdrawalPayment():
    pass

def postWithdrawalCrypto():
    pass

def getPaymentMethods():
    pass

def getCoinbaseAccounts():
    pass

def postReports():
    pass

def getReports():
    pass

def getTrailingVolume():
    pass
########################################## HELPERS #################################################
####################################################################################################



