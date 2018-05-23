#  bittrexAPI.py

import sys
sys.path.append('C:/C-directory/Projects/Work-i/Bots/Arbitrage')

# External-Imports
import requests
import hmac
import hashlib
import time

# Key Imports
#from secret_keys import bittrex_public_key, bittrex_private_key
from secret_keyz import bittrex_public_key, bittrex_private_key

def createTimestamp():
    return str(int(time.time() * 1000))

# ---------------------------------------- MARKET CALLS ----------------------------------------
# * - getCurrencies   :
# * - getInfoPairing  :
# * - getInfoPairings :
# * - getMarkets      :
# * - getMarketHistory:

# FUNCTION: getCurrencies
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#   Retrieves list of currenciey pairings currently being traded on the exchanges and 
#    pertinent information.
def getCurrencies():
    json_var2 = requests.request('GET', 'https://bittrex.com/api/v1.1/public/getcurrencies').json()

    # JSON STANDARDIZATION
    if json_var2["success"] == True:

        json_var = json_var2["result"]
        ret_dict2 = {}
        for currency in json_var:
            transaction_fee = currency["TxFee"]
            is_active = currency["IsActive"]
            coin_type = currency["CoinType"]
            base_address = currency["BaseAddress"]
            currency_long = currency["CurrencyLong"]
            min_confirmation = currency["MinConfirmation"]
            nested_dict = {
                "transaction_fee" : transaction_fee,
                "is_active" : is_active,
                "min_confirmation" : min_confirmation,
                "base_address" : base_address
            }
            currency_value = currency["Currency"]
            ret_dict2[currency_value] = nested_dict

        ret_dict = {
        "success" : True,
        "currencies" : ret_dict2
        }
    else:
        ret_dict ={
        "success" : False
        }

    return ret_dict    

# FUNCTION: getInfoPairing
# INPUT: pairing - string
# OUTPUT: dictionary of information
# DESCRIPTION:
#   Wrapper function to retrieve information on a single pairing using getMarkets() call.
def getInfoPairing(pairing):
    json_var = getMarkets()
    if json_var["success"] == True:
        for dictionary in json_var["result"]:
            if dictionary["MarketName"] == pairing:
                MinTradeSize = dictionary["MinTradeSize"]
                ret_dict = {
                "success" : True,
                "pairing" : pairing,
                "min_trade_size" : MinTradeSize,
                "min_price" : .0000001,
                "min_quantity" : .0000001,
                "step_size" : 0.00000001
                }
    else:
        ret_dict ={
        "success" : False
        }

    return ret_dict

# FUNCTION: getInfoPairings
def getInfoPairings(pairings):
    json_var = getMarkets()
    pair_list = {}
    ret_dict = {}
    if json_var["success"] == True:
        for pairing in pairings:
            pair_list[pairing] = pairing
        for dictionary in json_var["result"]:
            if dictionary["MarketName"] in pair_list.keys():
                pairing = dictionary["MarketName"]
                MinTradeSize = dictionary["MinTradeSize"]
                inner_dict = {
                "success" : True,
                "pairing" : pairing,
                "min_trade_size" : MinTradeSize
                }
                ret_dict[pairing] = inner_dict
    else:
        ret_dict ={
        "success" : False
        }
        return ret_dict

    ret_dict["success"] = True
    return ret_dict

# FUNCTION: getMarkets
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRITION:
#   Returns the active markets for Bittrex.
# * Not dictionary standardized
def getMarkets():
    req = requests.request('GET', 'https://bittrex.com/api/v1.1/public/getmarkets').json()
    return req

# FUNCTION: getMarketHistory
# INPUT: pairing - string
# OUTPUT: dictionary
# DESCRIPTION:
#   Outputs dictionary with relevant parameters for recent market history
def getMarketHistory(pairing):
    url = 'https://bittrex.com/api/v1.1/public/getmarkethistory?market' + str(pairing)
    req = requests.request('GET', url).json()
    return req

# FUNCTION: getMarketSummary
# INPUT: pairing - string
# OUTPUT: Dictionary
# DESCRIPTION:
#   TODO
# * Not dictionary standardized
def getMarketSummary(pairing):
    url = 'https://bittrex.com/api/v1.1/public/getmarketsummary?market=' + str(pairing)
    req = requests.request('GET', url).json()
    return req 

# FUNCTION: getMarketSummaries
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#   TODO
# * Not dictionary standardized
def getMarketSummaries():
    req = requests.request('GET', 'https://bittrex.com/api/v1.1/public/getmarketsummaries').json()
    return req 

# FUNCTION: getOrderbook
# INPUT: pairing - string
#        order_type - string
# OUTPUT: Dictionary
# DESCRIPTION:
#   TODO
def getOrderbook(pairing, order_type):
    # order type is required: bids, asks or both 
    url = 'https://bittrex.com/api/v1.1/public/getorderbook?market=' + str(pairing) + '&type=' + str(order_type)
    json_var = requests.request('GET', url).json()
    if json_var["success"] == False:
        print(json_var)
        return -1
    # JSON STANDARDIZATION
    if json_var["success"] == True:
        json_var2 = json_var["result"]
        bids = json_var2["buy"]
        asks = json_var2["sell"]
        dict_bids = []
        dict_asks = []
        if bids == None:
            ret_dict ={
            "success" : False
            }        
            return ret_dict  
        for bid in bids:
            dict_bids.append((bid["Rate"], bid["Quantity"]))
        for ask in asks:
            dict_asks.append((ask["Rate"], ask["Quantity"]))

        ret_dict = {
        "success" : True,
        "bids" : dict_bids,
        "asks" : dict_asks
        }
    else:

        ret_dict ={
        "success" : False
        }

    return ret_dict

# WRAPPER: getOrderbookBoth
#   Wrapper function to get the orderbook for both sides of a pairing.
def getOrderbookBoth(pairing):
    return getOrderbook(pairing, "both")

# FUNCTION: getTicker
# INPUT: pairing - string
# OUTPUT: Dictionary
#   Returns the ticker information for a specified market pairing.
# * Not dictionary standardized
def getTicker(pairing):
    url = 'https://bittrex.com/api/v1.1/public/getticker?market=' + str(pairing)
    req = requests.request('GET', url).json()
    if req["message"] == "INVALID_MARKET":
        return 0
    else:
        return req["result"]["Last"]

def getPriceUSD(pairing):
    if pairing != "USDT-BTC":
        price_symb = getTicker(pairing)
    else:
        price_symb = 1
    price_btc = getTicker("USDT-BTC")
    price_usd = price_btc * price_symb
    return price_usd
# ---------------------------------------- ORDER CALLS ----------------------------------------
# /market/%

# FUNCTION: buyLimit
# INPUT: pairing  - string
#        quantity - float
#        rate     - float
# OUTPUT: dictionary
# DESCRIPTION
#   Places a limit buy order for a given pairing at a given rate for a given quantity.
def buyLimit(pairing, quantity, rate):

    # Check if its a minimum order
    input_s = float(quantity) * float(rate)
    if input_s < .0005:
        ret_dict = {
        "success": False,
        "btc_value" : input_s,
        "error" : "micro_order"
        } 
        return ret_dict

    # 1. Perform the operation, buyLimit
    nonce = createTimestamp()
    url = "https://bittrex.com/api/v1.1/market/buylimit?apikey=%s&nonce=%s&market=%s&quantity=%s&rate=%s" % (bittrex_public_key, nonce, pairing, quantity, rate)
    buy_json_var = encrypt(url).json()

    # 2. If it was successful, grab the order for the sake of the return dictionary
    if buy_json_var["success"] == True:
        json_var = getOrder(pairing, buy_json_var["result"]["uuid"])
    else:
        if "message" in buy_json_var:
            error = buy_json_var["message"]
        else:
            error = "failed_request"
        return_dict ={
            "success" : False,
            "pairing" : pairing,
            "quantity" : quantity,
            "rate" : rate,
            "error" : error,
            "function" : "buyLimit"
        }
        return return_dict

    # JSON STANDARDIZATION    
    if json_var["success"] == True:
        order_id = json_var["order_id"]
        original_quantity = json_var["original_quantity"]
        filled_quantity = original_quantity - json_var["remaining_quantity"]
        filled = (json_var["status"] == "is_open")
        base, quote = pairing.split("-")
        btc_value = filled_quantity * rate

        return_dict = {
            "success" : True,
            "order_id" : order_id,
            "filled" : filled,
            "original_quantity" : original_quantity,
            "filled_quantity" : filled_quantity,
            "btc_value" : btc_value,
            "usd_value" : 0,
            "pairing" : pairing,
            "asset" : quote,
            "type" : "limit",
            "rate" : rate,
            "filled_rate": json_var["rate"],
            "side" : "buy",
            "error" : "",
            "exchange" : "bittrex"
        }

    else:
        if "message" in json_var:
            error = json_var["message"]
        else:
            error = "failed_request"
        return_dict ={
            "success" : False,
            "pairing" : pairing,
            "quantity" : quantity,
            "rate" : rate,
            "error" : error
        }

    return return_dict

# FUNCTION: sellLimit
# INPUT: pairing  - string
#        quantity - float
#        rate     - float
# OUTPUT: dictionary
# DESCRIPTION
#   Places a limit sell order for a given pairing at a given rate for a given quantity.
def sellLimit(pairing, quantity, rate):

    # Check if its a minimum order
    input_s = float(quantity) * float(rate)
    if input_s < .0005:
        ret_dict = {
        "success": False,
        "btc_value" : input_s,
        "error" : "micro_order"
        } 
        return ret_dict

    # 1. Perform the operation, buyLimit
    nonce = str(int(time.time() * 1000))
    url = "https://bittrex.com/api/v1.1/market/selllimit?apikey=%s&nonce=%s&market=%s&quantity=%s&rate=%s" % (bittrex_public_key, nonce, pairing, quantity, rate)
    sell_json_var = encrypt(url).json()

    # 2. If it was successful, grab the order for the sake of the return dictionary
    if sell_json_var["success"] == True:
        json_var = getOrder(pairing, sell_json_var["result"]["uuid"])
    else:
        if "message" in sell_json_var:
            error = sell_json_var["message"]
        else:
            error = "failed_request"
        return_dict ={
            "success" : False,
            "pairing" : pairing,
            "quantity" : quantity,
            "rate" : rate,
            "error" : error,
            "function" : "sellLimit : 1",
            "exchange" : "bittrex"
        }
        return return_dict

    # JSON STANDARDIZATION    
    if json_var["success"] == True:
        order_id = json_var["order_id"]
        original_quantity = json_var["original_quantity"]
        filled_quantity = original_quantity - json_var["remaining_quantity"]
        filled = (json_var["status"] == "is_open")
        print(json_var["status"])
        base, quote = pairing.split("-")
        quantity_btc = filled_quantity * rate
        return_dict = {
            "success" : True,
            "order_id" : order_id,
            "filled" : filled,
            "original_quantity" : original_quantity,
            "filled_quantity" : filled_quantity,
            "btc_value" : quantity_btc,
            "usd_value" : 0,
            "pairing" : pairing,
            "asset" : quote,
            "type" : "limit",
            "filled_rate" : json_var["rate"],
            "rate" : rate,
            "side" : "sell",
            "error" : "",
            "exchange" : "bittrex"
        }

    else:
        if "message" in json_var:
            error = json_var["message"]
        else:
            error = "failed_request"
        return_dict ={
        "success" : False,
        "pairing" : pairing,
        "quantity" : quantity,
        "rate" : rate,
        "error" : error,
        "exchange" : "bittrex",
        "function" : "sellLimit: getOrder"
        }
    return return_dict

# FUNCTION: cancelOrder
# INPUT: uuid    - string
#        pairing - string
# OUTPUT: dictionary
# DESCRIPTION:
#   Cancels an order given the UUID. Pairing isn't required, but is left as parameter for
#    the purpose of generic calls.
def cancelOrder(uuid, pairing=""):
    nonce = createTimestamp()
    url = "https://bittrex.com/api/v1.1/market/cancel?apikey=%s&nonce=%s&uuid=%s" % (bittrex_public_key, nonce, uuid)
    json_var = encrypt(url).json()
    print("CANCEL ORDER FOR BITTREX", json_var)
    if "message" in json_var:
        if json_var["message"] == "ORDER_NOT_OPEN":
            message = "order_closed"
        else: 
            message = ""
    else:
        message = ""
    # JSON STANDARDIZATION
    if json_var["success"] == True:
        ret_dict = {
        "success" : True,
        "order_id" : uuid,
        "pairing" : pairing,
        "timestamp" : nonce,
        "error" : message
        }
    else:
        ret_dict = {
        "success" : False,
        "order_id" : uuid,
        "pairing" : pairing,
        "timestamp" : nonce,
        "error" : message
        }

    return ret_dict

# FUNCTION: getOpenOrders
def getOpenOrders(market=None):
    nonce = str(int(time.time() * 1000))
    url = "https://bittrex.com/api/v1.1/market/getopenorders?apikey=%s&nonce=%s&" % (bittrex_public_key, nonce)
    if market:
        open_orders_string= "&market=%s" % (market)
    url += open_orders_string
    req = encrypt(url).json()
    return req

# FUNCTION: getOrder
def getOrder(pairing, uuid):
    nonce = str(int(time.time() * 1000))
    url = "https://bittrex.com/api/v1.1/account/getorder?apikey=%s&nonce=%s&uuid=%s" % (bittrex_public_key, nonce, uuid)
    json_var = encrypt(url).json()

    print(json_var)
    # JSON STANDARDIZATION
    if json_var["success"] == True:
        json_var2 = json_var["result"]
        original_quantity = json_var2["Quantity"]
        remaining = json_var2["QuantityRemaining"]
        price_per = json_var2["PricePerUnit"] if json_var2["PricePerUnit"] != None else 0
        total_price = json_var2["Price"]
        executed_quantity = original_quantity - remaining
        quantity_btc = executed_quantity * price_per
        if json_var2["Type"] == "LIMIT_BUY":
            side = "Buy"
        elif json_var2["Type"] == "LIMIT_SELL":
            side = "Sell"
        status = json_var2["IsOpen"]

        incomplete_var = True if executed_quantity != original_quantity else False

        base, quote = pairing.split("-")
        
        ret_dict = {
        "success" : True,
        "order_id" : uuid,
        "original_quantity" : original_quantity,
        "filled_quantity" : executed_quantity,
        "remaining_quantity" : remaining,
        "side" : side,
        "btc_value" : quantity_btc,
        "status" : status,
        "incomplete" : incomplete_var,
        "rate" : price_per,
        "notional" : total_price,
        "asset" : quote
        }
    else:
        if "message" in json_var:
            message = json_var["message"]
        else:
            message = ""
        ret_dict ={
        "success" : False,
        "order_id" : uuid,
        "pairing" : pairing,
        "exchange" : "bittrex",
        "error" : message
        }

    return ret_dict

# Input: market - Optional
#   A string literal for the market (ie. BTC-LTC). No input returns the order history for all markets.
def getOrderHistory(market=None):
    nonce = str(int(time.time() * 1000))
    url = "https://bittrex.com/api/v1.1/account/getorderhistory?apikey=%s&nonce=%s" % (bittrex_public_key, nonce)
    if market:
            market_string = "&market=%s" % (market)
    url += market_string
    req = encrypt(url).json()
    return req

# ---------------------------------------- ACCOUNT CALLS ----------------------------------------
# /account/%

# FUNCTION: getBalance
def getBalance(currency):
    nonce = str(int(time.time() * 1000))
    url = "https://bittrex.com/api/v1.1/account/getbalance?apikey=%s&nonce=%s&currency=%s" % (bittrex_public_key, nonce, currency)
    json_var = encrypt(url).json()

    # JSON STANDARDIZATION
    if json_var["success"] == True:
        json_var2 = json_var["result"]
        currency = json_var2["Currency"]
        total_balance = json_var2["Balance"]
        available_balance = json_var2["Available"]
        pending_balance = json_var2["Pending"]
        address = json_var2["CryptoAddress"]
        #requested = json_var2["Requested"]
        #uuid = json_var2["Uuid"]

        ret_dict = {
        "success" : True,
        "currency" : currency,
        "total_balance" : total_balance,
        "available_balance" : available_balance,
        "pending_balance" : pending_balance,
        "address" : address
        }
    else:
        ret_dict ={
        "success" : False
        }

    return ret_dict

# FUNCTION: getBalances
def getBalances():
    nonce = str(int(time.time() * 1000))
    url = "https://bittrex.com/api/v1.1/account/getBalances?apikey=%s&nonce=%s" % (bittrex_public_key, nonce)
    json_var = encrypt(url).json()

    # JSON STANDARDIZATION
    if json_var["success"] == True:
        json_var2 = json_var["result"]
        ret_dict2 = {}
        for bal in json_var2:
            currency = bal["Currency"]
            total_balance = bal["Balance"]
            available_balance = bal["Available"]
            pending_balance = bal["Pending"]
            address = bal["CryptoAddress"]
            #requested = json_var2["Requested"]
            #uuid = json_var2["Uuid"]
            nested_dict = {
            "total_balance" : total_balance,
            "available_balance" : available_balance,
            "pending_balance" : pending_balance,
            "address" : address
            }
            ret_dict2[currency] = nested_dict
        ret_dict = {
        "success" : True,
        "balances" : ret_dict2
        }
    else:
        ret_dict ={
        "success" : False
        }

    return ret_dict

# FUNCTION: getDepositAddress
# INPUT: currency - string
# OUTPUT: dictionary
# DESCRIPTION:
#   Retrieves the deposit address for a given asset.
def getDepositAddress(currency):
    nonce = createTimestamp()
    url = "https://bittrex.com/api/v1.1/account/getdepositaddress?apikey=%s&nonce=%s&currency=%s" % (bittrex_public_key, nonce, currency)  
    json_var = encrypt(url).json()

    # JSON STANDARDIZATION
    if json_var["success"] == True:
        json_var2 = json_var["result"]
        currency = json_var2["Currency"]
        outlier_dict = checkOutliers(currency)
        if outlier_dict != -1:
            ret_dict = {
            "success" : True,
            "currency" : currency,
            "address" : outlier_dict[0],
            "withdrawal_tag" : outlier_dict[1]
            }
            return ret_dict
        else: 
            address = json_var2["Address"]
            ret_dict = {
            "success" : True,
            "currency" : currency,
            "address" : address,
            "withdrawal_tag" : None
            }
    else:
        ret_dict ={
        "success" : False
        }

    return ret_dict

# FUNCTION: checkDeposit
# INPUT: asset      - string
#        quantity   - float
#        start_time - int [unix]
# OUTPUT: boolean
# DESCRIPTION:
#   Looks for a deposit of the given quantity in the given asset, returns a boolean
#    indicating whether or not it exists. 
def checkDeposit(asset, quantity, start_time):
    deposit_history = getDepositHistoryAsset(asset)
    for value in deposit_history:
        if value["amount"] == quantity and value["asset"] == asset:
            return True
    return False

# FUNCTION: getDeposit
# INPUT: asset    - string
#        quantity - float
# OUTPUT: dictionary
# DESCRIPTION:
#   Retrieves a single deposit for a given asset. Returns False if the deposit isn't found.
# * TODO - check to make sure there are no 'duplicates' based on quantity.
def getDeposit(asset, quantity):
    deposit_history = getDepositHistoryAsset(asset)
    for value in deposit_history:
        if value["amount"] == quantity and value["asset"] == asset:
            return value
    return False

# FUNCTION: getDepositHistory
# INPUT: currency - string
#        quantity - float [TODO]
# OUTPUT: dictionary
# DESCRIPTION:
#   Retrieves the deposit history for all assets.
# * TODO - add quantity/start time
# * TODO - dictionary/list thing 
def getDepositHistory(currency=None):
    nonce = createTimestamp()
    url = "https://bittrex.com/api/v1.1/account/getdeposithistory?apikey=%s&nonce=%s" % (bittrex_public_key, nonce)
    if currency:
            currency_string_deposit= "&currency=%s" % (currency)
    url += currency_string_deposit
    req = encrypt(url).json()

    # JSON STANDARDIZATION
    if json_var["success"] == True:
        json_var2 = json_var["result"]
        ret_list = []
        for value in json_var:
            tx_id = json_var2["TxId"]
            # pending = json_var2["PendingPayment"]
            confirmations = value["Confirmations"]
            # authorized = json_var["Authorized"]
            # open_date = json_var2["Opened"]
            address = json_var2["CryptoAddress"]
            amount = json_var2["Amount"]
            asset = json_var2["Currency"]
            # TODO - standardize open date

            nested_dict = {            
            "tx_id" : tx_id,
            "confirmations" : confirmations,
            # "authorized" : authorized,
            # "opened" : open_date,
            "address" : address,
            "amount" : amount
            }
            ret_list.append(nested_dict)

    else:
        ret_list = [False]

    return ret_list

# FUNCTION: getDepositHistoryAsset
# INPUT: asset - string
# OUTPUT: dictionary
# DESCRIPTION:
#   Retrieves the deposit history for a single asset.
# * TODO - add quantity/start time
def getDepositHistoryAsset(asset):
    nonce = createTimestamp()
    url = "https://bittrex.com/api/v1.1/account/getdeposithistory?apikey=%s&nonce=%s" % (bittrex_public_key, nonce)
    currency_string_deposit= "&currency=%s" % (asset)
    url += currency_string_deposit
    json_var = encrypt(url).json()

    # JSON STANDARDIZATION
    if json_var["success"] == True:
        json_var2 = json_var["result"]
        ret_list = []
        for value in json_var2:
            tx_id = value["TxId"]
            confirmations = value["Confirmations"]
            # authorized = json_var["Authorized"]
            # open_date = value["Opened"]
            address = value["CryptoAddress"]
            amount = value["Amount"]
            # TODO - standardize open date

            nested_dict = {"success" : True,
            "tx_id" : tx_id,
            "confirmations" : confirmations,
            # "authorized" : authorized,
            # "opened" : open_date,
            "address" : address,
            "amount" : amount,
            "asset" : asset
            }
            ret_list.append(nested_dict)
    else:
        ret_list = [False]
        
    return ret_list

# FUNCTION: getWithdrawalHistory
# INPUT:
# OUTPUT: dictionary
# DESCRIPTION:
#   TODO, No input returns the withdrawal history for all currencies
def getWithdrawalHistory(currency=None):
    nonce = str(int(time.time() * 1000))
    url = "https://bittrex.com/api/v1.1/account/getwithdrawalhistory?apikey=%s&nonce=%s" % (bittrex_public_key, nonce)
    if currency:
            currency_string_withdrawal = "&currency=%s" % (currency)
            url += currency_string_withdrawal
            req = encrypt(url).json()
    return req

# Input: paymentid - Optional
def withdraw(currency, quantity, address, paymentid=""):
    nonce = str(int(time.time() * 1000))
    url = "https://bittrex.com/api/v1.1/account/withdraw?apikey=%s&nonce=%s&currency=%s&quantity=%s&address=%s" % (bittrex_public_key, nonce, currency, quantity, address)
    if paymentid != "":
        url = url + "&paymentid=" + str(paymentid)
        print(url)
    json_var = encrypt(url).json()

    print(json_var)
    if json_var["success"] == True:
        timestamp = time.time() # TODO FIX
        json_var2 = json_var["result"]
        withdrawal_id = json_var2["uuid"]
        ret_dict = {
        "success" : True,
        "id" : withdrawal_id,
        "exchange" : "bittrex",
        "amount" : amount,
        "asset" : asset,
        "address" : address,
        "time" : timestamp,
        "paymentid" : paymentid
        }
    else:
        ret_dict ={
        "success" : False,
        "message" : json_var["message"]
        }
    print(ret_dict)
    return ret_dict

# ---------------------------------------- HELPERS ----------------------------------------

# SHA512 ENCRYPTION FOR ACCOUNT REQUESTS
def encrypt(url):
    sign = hmac.new(bittrex_private_key.encode(), url.encode(), 'sha512')
    header_digest = sign.hexdigest()
    header_dic = {'apisign':header_digest}
    req = requests.get(url, headers=header_dic)
    return req

def returnExchangeInfo():
    pass

# FUNCTION: standardizePairing
def standardizePairing(pairing):
    return pairing

def checkOutliers(currency):
    if currency == "XRP":
        address = "rPVMhWBsfF9iMXYj3aAzJVkPDTFNSyWdKy"
        tag = "1137916251"
    elif currency == "XMR":
        address = "463tWEBn5XZJSxLU6uLQnQ2iY9xuNcDbjLSjkn3XAXHCbLrTTErJrBWYgHJQyrCwkNgYvyV3z8zctJLPCZy24jvb3NiTcTJ"
        tag = "0040df39509b4a4588cb8abf841e0c58c28966c02e4e4f0abe687f9d4da16581"
    else:
        return -1

    return (address, tag)