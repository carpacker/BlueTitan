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
# getOrderbook    : Retrieves the orderbook for a given pairing                                    #
# getTradeHistory : Retrieves the most recent trades on the market for a given pairing             #
# getChartData    : Retrieves candlestick data for a given pairing                                 #
# getCurrencies   : Returns a list of currencies and associated information                        #
# getLoanOrders   : Retrieves available loan orders                                                #
####################################################################################################

# URL for all public calls
public_url = base_url + "public?command="

# FUNCTION: getTicker
# INPUT: pairing - (OPTIONAL) string
# OUTPUT: Dictionary
# DESCRIPTION:
#    Returns ticker for all markets, optional input to just receive one market.
def getTicker(pairing=""):
    url = public_url + "returnTicker"
    PrintLibrary.displayVariable(url)
    
    json_var = requests.request('GET', url).json()

    # Check to make sure no error
    # TODO

    # JSON standardization
    ret_dict = {}
    
    # If pairing is provided 
    if pairing != "":
        print(json_var[pairing])
        standardized_pairing = standardizePairing(pairing)
        # build ret_dict
        
        return ret_dict

    for pairing in json_var:
        print(json_var[pairing])
        json_var2 = json_var[pairing]
        standardized_pairing = standardizePairing(pairing)
        nested_dict = {}
        nested_dict["last_price"] = json_var2["last"]
        # and so on...

        ret_dict[standardized_pairing] = nested_dict

    PrintLibrary.displayDictionary(ret_dict)
    return ret_dict

# FUNCTION: getVolume
# INPUT: pairing - string
# OUTPUT: Dictionary
# DESCRIPTION:
#    Returns 24hr volume for all markets, optional input to just receive one currency.
def getVolume(pairing=""):
    url = public_url + "return24hVolume"
    PrintLibrary.displayVariable(url)
    
    json_var = requests.request('GET', url).json()
    print(json_var)

    # Check to make sure no error
    # TODO
    
    # JSON standardization
    ret_dict = {}
    
    # If pairing is provided 
    if pairing != "":
        print(json_var[pairing])
        standardized_pairing = standardizePairing(pairing)
        # build ret_dict
        
        return ret_dict

    for pairing in json_var:
        print(json_var[pairing])
        standardized_pairing = standardizePairing(pairing)
        nested_dict = {}
        # Build nested_dict

        ret_dict[standardized_pairing] = nested_dict
    
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
    
    json_var = encryptRequest(False, 0) 

    # Check to make sure no error
    # TODO

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
    
    json_var = encryptRequest(False, 0)
    
    # Check to make sure no error
    # TODO
    
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
    
    json_var = encryptRequest(False, 0)
    
    # Check to make sure no error
    # TODO
    
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
    
    json_var = encryptRequest(False, 0)
    
    # Check to make sure no error
    # TODO

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
    for pairing in json_var:
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
# INPUT: assets - [string, ...]
# OUTPUT: Dictionary
# DESCRIPTION:
#    Retrieves a list of deposit addresses from a list of currencies, returns
#     a dictionary of currency to deposit address.
def getDepositAddresses():
    # Check to make sure no error

    # JSON standardization
    ret_dict = {}
    for pairing,information in json_var:
        pass
    
    PrintLibrary.displayDictionary(ret_dict)
    return ret_dict

# FUNCTION: getDepositAddress
# INPUT: asset - string
# OUTPUT: Dictionary
# DESCRIPTION:
# 
def getDepositAddress():
    url = trading_url + "returnDepositAddress"
    PrintLibrary.displayVariable(url)
    
    json_var = requests.request('GET', url).json()
    
    # Check to make sure no error

    # JSON standardization
    ret_dict = {}
    for pairing,information in json_var:
        pass
    
    PrintLibrary.displayDictionary(ret_dict)
    return ret_dict

# FUNCTION: generateNewAddress
# INPUT: asset - string
# OUTPUT: Dictionary
# DESCRIPTION:
#    Generates a new address for a given asset
def generateNewAddress():
    url = trading_url + "generateNewAddress"
    PrintLibrary.displayVariable(url)
    
    json_var = requests.request('GET', url).json()
    
    # Check to make sure no error

    # JSON standardization
    ret_dict = {}
    for pairing,information in json_var:
        passb
    
    PrintLibrary.displayDictionary(ret_dict)
    return ret_dict

# FUNCTION: getDepositsWithdrawals
# INPUT: start - int
#        end   - int
# OUTPUT: Dictionary
# DESCRIPTION:
#    Returns the deposits and withdrawals of the account, including all associated information.
#     Start and end optional parameters are used to defin a range.
def getDepositWithdrawals(order_by, start="", end="", asset=""):
    url = trading_url + "getDepositWithdrawals"
    PrintLibrary.displayVariable(url)
    
    json_var = encryptRequest(True, 'POST', url, start=start, end=end)

    # * Check to make sure no error
    # TODO
    
    # * Standardization
    deposit_list = []
    deposits = json_var["deposits"]
    for deposit in deposits:
        deposit_dict = {}
        deposit_dict[''] = deposit['']
        # and so on...
        deposit_list.append(deposit_dict)

    withdrawal_list = []
    withdrawals = json_var["withdrawals"]
    for withdrawal in withdrawals:
        withdrawal_dict = {}
        withdrawal_dict[''] = withdrawal['']
        # and so on...
        withdrawal_list.append(withdrawal_dict)
        

    deposit_withdrawals = (deposit_list, withdrawal_list)
    
    PrintLibrary.displayVariables(deposit_list)
    PrintLibrary.displayVariables(withdrawal_list)
    
    return json_var

# FUNCTION: getWithdrawals
# INPUT:  start - int [unix timestamp]
#         end   - int [unix timestamp]
#         asset - string
# OUTPUT: Dictionary
# DESCRIPTION:
#    Retrieves list of withdrawals. Specifically a wrapper over getDepositWithdrawals. Asset is an
#     optional parameter used to return only withdrawals of a specific asset.
# NOTE: calls getDepositWithdrawals
def getWithdrawals(order_by, start=0, end=0, asset=""):
    dep_wit = getDepositWithdrawals(order_by, start, end, asset)
    # Filter Withdrawals out
    withdrawals = dep_wit[0]
    return withdrawals

# FUNCTION: getDeposits
# INPUT: start - int (unix timestamp)
#        end   - int (unix timestamp)
# OUTPUT: Dictionary
# DESCRIPTION:
#    Retrieves deposit history for all assets, optional input of time period (start, end).
# NOTE: calls getDepositWithdrawals
def getDeposits(order_by, start=0, end=0, asset=""):
    dep_wit = getDepositWithdrawals(order_by, start, end, asset)
    # Filter Deposits out
    deposits = dep_wit[1]
    return deposits

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

# FUNCTION: encryptRequest
# INPUT: signature - boolean
#        method    - 'POST' or 'GET'
#        end       - url (string)
#        * - Query vars passed in as list of params (a=1,b=2,c=3)
# OUTPUT: Encrypted url used for HTTPS request
# DESCRIPTION:
#   Encrypts an API request to Binance.
def encryptRequest(signature, method, base_url, **query_vars):

    # Add queries and header
    header = { 'X-MBX-APIKEY' : poloniex_public_key}
    queryString = "&".join(['%s=%s' % (key,value) for (key,value) in query_vars.items()])
    if "timestamp" not in query_vars:
        extra = "&timestamp=" + str(int(time.time()*1000))
    queryString += extra

    # Sign the transaction
    sig = hmac.new(poloniex_private_key.encode(),queryString.encode(),'sha256')
    signature = sig.hexdigest()
    sigstring = "&signature=%s" % (signature)
    
    url = base_url + "?" + queryString + sigstring
    print(url)
    
    req = requests.request(method, url, headers=header).json()
    return req

# FUNCTION: standardizePairing
# INPUT: pairing - string
# OUTPUT: string
# DESCRIPTION:
#    Standardizes pairing format from Poloniex's to generic format.
def standardizePairing(pairing):
    if "_" in pairing:
        base, quote = pairing.split("_")
        s_pairing = base + "-" + quote
        return s_pairing
    else:
        # TODO; fix this
        print(pairing)

# FUNCTION: unscramblePairing
# INPUT: pairing - string
# OUTPUT: string
# DESCRIPTION
#    Converts generic-formatted pairing to Poloniex's format.
def unscramblePairing(pairing):
    base, quote = pairing.split("-")
    s_pairing = base + "_" + quote
    return s_pairing
