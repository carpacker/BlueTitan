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
base_url = "https://poloniex.com/"

######################################## PUBLIC CALLS ##############################################
####################################################################################################
# getTicker       : Returns ticker information for all assets, if provided single asset            #
#                    then it returns the ticker information for just that asset.                   # 
# getVolume       : Returns 24hr volume for all assets on exchange, if provied single asset        #
#                    then it returns the 24hr volume for just that asset.                          # 
# getOrderbook    :
# getTradeHistory :
# getChartData    :
# getCurrencies   :
# getLoanOrders   :
####################################################################################################

# URL for all public calls
public_url = base_url + "public?command="

# FUNCTION: getTicker
# INPUT: asset - (OPTIONAL) string
# OUTPUT: Dictionary
# DESCRIPTION:
#    Returns ticker for all markets, optional input to just receive on currency.
def getTicker(asset=""):
    url = public_url + "returnTicker"
    PrintLibrary.displayVariable(url)
    
    json_var = requests.request('GET', url).json()
    # Check to make sure no error

    # JSON standardization
    ret_dict = {}
    for pairing in json_var:
        print(json_var[pairing])
        standardized_pairing = standardizePairing(pairing)
        nested_dict = {}
        nested_dict["last_price"] = information["last"]
        # and so on...

        ret_dict[standardized_pairing] = nested_dict

    PrintLibrary.displayDictionary(ret_dict)
    return ret_dict


# FUNCTION: getVolume
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#    Returns 24hr volume for all markets, optional input to just receive one currency.
def getVolume(asset=""):
    url = public_url + "return24hVolume"
    PrintLibrary.displayVariable(url)
    
    json_var = requests.request('GET', url).json()
    print(json_var)
    # Check to make sure no error

    # JSON standardization
    ret_dict = {}
    for pairing,information in json_var:
        pass
    
    PrintLibrary.displayDictionary(ret_dict)
    return ret_dict

######################################## MARKET CALLS ##############################################
#################################################################################################### 

# FUNCTION: getOrderbook
# INPUT: pairing - string
# OUTPUT: Dictionary
# DESCRIPTION:
#   Retrieves the orderbook for a given pairing. Output dictionary contains list of asks and bids,
#    ordered ascending and descending respectively.
def getOrderbook(pairing):
    url = public_url + "returnOrderBook"
    PrintLibrary.displayVariable(url)
    
    json_var = requests.request('GET', url).json()
    
    # Check to make sure no error

    # JSON standardization
    ret_dict = {}
    for pairing,information in json_var:
        pass
    
    PrintLibrary.displayDictionary(ret_dict)
    return ret_dict 

# FUNCTION: getTradeHistory
# INPUT: pairing - string
#        start   - int
#        end     - int
# OUTPUT: [(trade, ...), ...]
# DESCRIPTION:
#    Returns the past 200 trades for a given market, or up to 50,000 trades between range specific
#     in unix timpestamps by stat and end.
def getMarketHistory(pairing, start=0, end=0):
    url = public_url + "returnMarketHistory"
    PrintLibrary.displayVariable(url)
    
    json_var = requests.request('GET', url).json() 
    # Check to make sure no error

    # JSON standardization
    ret_dict = {}
    for pairing,information in json_var:
        pass
    
    PrintLibrary.displayDictionary(ret_dict)
    return ret_dict

# FUNCTION: getChartData
# INPUT: pairing - string
#        period  - seconds (VALID: 300, 900, 1800, 7200, 1440, 86400)
#        start   - int
#        end     - int
# OUTPUT: dictionary
# DESCRIPTION:
#    Returns candlestick chart data for a given market pairing.
def getChartData(pairing, period, start=0, end=0):
    url = public_url + "returnChartData"
    PrintLibrary.displayVariable(url)
    
    json_var = requests.request('GET', url).json()

    # Check to make sure no error

    # JSON standardization
    ret_dict = {}
    for pairing,information in json_var:
        pass
    
    PrintLibrary.displayDictionary(ret_dict)
    return ret_dict

# FUNCTION: getCurrencies
# INPUT: N/A
# OUTPUT: dictionary
# DESCRIPTION:
#    Returns information about [all] assets.
def getCurrencies():
    url = public_url + "returnCurrencies"
    PrintLibrary.displayVariable(url)
    
    json_var = requests.request('GET', url).json()
    
    # Check to make sure no error

    # JSON standardization
    ret_dict = {}
    for pairing,information in json_var:
        pass
    
    PrintLibrary.displayDictionary(ret_dict)
    return ret_dict

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
    url = public_url + "returnLoanOrders"
    PrintLibrary.displayVariable(url)
    
    json_var = requests.request('GET', url).json()

    # Check to make sure no error

    # JSON standardization
    ret_dict = {}
    for pairing,information in json_var:
        pass
    
    PrintLibrary.displayDictionary(ret_dict)
    return ret_dict

######################################## ORDER CALLS ###############################################
####################################################################################################

# FUNCTION: getOrderTrades
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getOrderTrades():
    pass

# FUNCTION: getOrder
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getOrder():
    pass

# FUNCTION: getOpenOrders
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getOpenOrders():
    pass

# FUNCTION: moveOrder
# INPUT:
# OUTPUT:
# DESCRIPTION:
def moveOrder():
    pass

# FUNCTION: cancelOrder
# INPUT:
# OUTPUT:
# DESCRIPTION:
def cancelOrder():
    pass

# FUNCTION: getTradeHistory
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getTradeHistory():
    pass

# FUNCTION: postBuy
# INPUT:
# OUTPUT:
# DESCRIPTION:
def postBuy():
    pass

# FUNCTION: buyLimit
# INPUT:
# OUTPUT:
# DESCRIPTION:
def buyLimit():
    pass

# FUNCTION: postSell
# INPUT:
# OUTPUT:
# DESCRIPTION:
def postSell():
    pass

# FUNCTION: sellLimit
# INPUT:
# OUTPUT:
# DESCRIPTION:
def sellLimit():
    pass

####################################### ACCOUNT CALLS ############################################## 
####################################################################################################

trading_url = base_url + "tradingApi?command="

# FUNCTION: getFeeInfo
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getFeeInfo():
    pass

# FUNCTION: getBalance
# INPUT: asset - string
# OUTPUT: Dictionary
# DESCRIPTION:
#    Returns the balance for a specific asset.
# NOTE: Calls returnBalances
# NOTE: Implement list of assets in the future
def getBalance():
    pass

# FUNCTION: getBalances
# INPUT: N/A 
# OUTPUT: Dictionary
# DESCRIPTION:
#    Retrieves balance for each asset on your account.
def getBalances():
    url = trading_url + "returnBalances"
    PrintLibrary.displayVariable(url)
    
    json_var = requests.request('GET', url).json()
    # Check to make sure no error

    # JSON standardization
    ret_dict = {}
    for pairing,information in json_var:
        pass
    
    PrintLibrary.displayDictionary(ret_dict)
    return ret_dict

# FUNCTION: getAvailableAccountBalances
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getAvailableAccountBalances():
    pass

# FUNCTION: getCompeleteBalances
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getCompleteBalances():
    url = trading_url + "returnCompleteBalances"
    PrintLibrary.displayVariable(url)
    
    json_var = requests.request('GET', url).json()
    
    # Check to make sure no error

    # JSON standardization
    ret_dict = {}
    for pairing,information in json_var:
        pass
    
    PrintLibrary.displayDictionary(ret_dict)
    return ret_dict

# FUNCTION: getDepositAddresses
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getDepositAddresses():
    # Check to make sure no error

    # JSON standardization
    ret_dict = {}
    for pairing,information in json_var:
        pass
    
    PrintLibrary.displayDictionary(ret_dict)
    return ret_dict

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
def getDepositAddress():
    url = trading_url + "returnCompleteBalances"
    PrintLibrary.displayVariable(url)
    
    json_var = requests.request('GET', url).json()
    
    # Check to make sure no error

    # JSON standardization
    ret_dict = {}
    for pairing,information in json_var:
        pass
    
    PrintLibrary.displayDictionary(ret_dict)
    return ret_dict

# FUNCTION:
# INPUT:
# OUTPUT: Dictionary
# DESCRIPTION:
def generateNewAddress():
    url = trading_url + "returnCompleteBalances"
    PrintLibrary.displayVariable(url)
    
    json_var = requests.request('GET', url).json()
    
    # Check to make sure no error

    # JSON standardization
    ret_dict = {}
    for pairing,information in json_var:
        pass
    
    PrintLibrary.displayDictionary(ret_dict)
    return ret_dict

# FUNCTION: getDepositsWithdrawals
# INPUT: start - int
#        end   - int
# OUTPUT: Dictionary
# DESCRIPTION:
#    Returns the deposits and withdrawals of the account, including all associated information.
#     Start and end optional parameters are used to defin a range.
def getDepositWithdrawals(start="", end=""):
    url = trading_url + "getDepositWithdrawals"
    PrintLibrary.displayVariable(url)
    
    json_var = encryptRequest(True, 'POST', url, start=start, end=end)
    # Check to make sure no error

    # JSON standardization
    ret_dict = {}
    deposits = json_var["desposits"]

    withdrawals = json_var["withdrawals"]
    
    for value in json_var:
        print(json_var[pairing])
        
        nested_dict = {}
        nested_dict["last_price"] = information["last"]
        # and so on...

        ret_dict[standardized_pairing] = nested_dict

    PrintLibrary.displayDictionary(ret_dict)
        
    
    PrintLibrary.displayDictionary(ret_dict)
    return ret_dict

# FUNCTION: getWithdrawals
# INPUT: 
# OUTPUT: Dictionary
# DESCRIPTION:
#
# NOTE: calls getDepositWithdrawals
def getWithdrawals(start=0, end=0):
    pass

# FUNCTION: getDeposits
# INPUT: start - int (unix timestamp)
#        end   - int (unix timestamp)
# OUTPUT: Dictionary
# DESCRIPTION:
#    Retrieves deposit history for all assets, optional input of time period (start, end).
# NOTE: calls getDepositWithdrawals
def getDeposits(start=0, end=0):
    # TODO
    pass

# FUNCTION: getDepositsAsset
# INPUT:
# OUTPUT: Dictionary
# DESCRIPTION:
#
# NOTE: calls getDeposits
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

# FUNCTION: standardizePairing
# INPUT: pairing - string
# OUTPUT: string
# DESCRIPTION:
#    Standardizes pairing format from Poloniex's to generic format.

def standardizePAiring():
    pass

# FUNCTION: unscramblePairing
# INPUT: pairing - string
# OUTPUT: string
# DESCRIPTION
#    Converts generic-formatted pairing to Poloniex's format.
def unscramblePairing():
    pass
