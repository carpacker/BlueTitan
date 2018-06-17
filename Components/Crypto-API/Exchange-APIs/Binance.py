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
from secret_keys import binance_private_key, binance_public_key

# Endpoint URLs
V1_URL = "https://api.binance.com/api/v1/"
V3_URL = "https://api.binance.com/api/v3/"
WAPI_URL = "https://api.binance.com/wapi/v3/"

######################################## PUBLIC CALLS ############################################## 
# * - checkServerTime   : Returns the server's recorded current time                               #
# * - getCurrencies     : Retrieves a list of currencies being actively traded on Binance          #
# * - getExchangeInfo   : Retrieves general information on the exchange and its pairings           # 
# * - getInfoPairing    : Retrieves information for a specific pairing                             #
# * - getInfoPairings   : Retrieves information for a list of pairings                             #
# * - testConnectivity  : Checks the connection to Binance                                         #
####################################################################################################

# FUNCTION: checkServerTime
# INPUT: N/A
# OUTPUT: JSON
# DESCRIPTION:
#   Ping server for time [unix timestamp].
def checkServerTime():
    json_var = requests.request('GET', 'https://api.binance.com/api/v1/time').json()

    # Print library to get return dictionary
    PrintLibrary.displayDictionary(json_var)

    if "code" in json_var:
        return {"success" : False,
                "message" : json_var["msg"]}
    ret_dict = {}

    return json_var

# FUNCTION: getCurrencies
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#   Returns information on currencies traded on Binance.
def getCurrencies():
    json_var = getExchangeInfo()
    ret_dict = {}

    if "code" in json_var:
        return {"success" : False,
                "message" : json_var["msg"]}

    symb_list = json_var["symbols"]
    for symb_json in symb_list:
        currency = symb_json["symbol"]
        is_active = (symb_json["status"] == "Trading")

        # Check what else is there to put in the nested dictionary
        PrintLibrary.displayDictionary(symb_json)

        nested_dict = {
        "is_active" : is_active
        }
        asset_dict[currency] = nested_dict
    
    ret_dict = {
        "success" : True,
        "currencies" : asset_dict
    }
    return ret_dict

# FUNCTION: getExchangeInfo
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#   Returns the up-to-date information on the exchange and its trading pairs.
def getExchangeInfo():
    req = requests.request('GET', 'https://api.binance.com/api/v1/exchangeInfo').json()
    return req

# FUNCTION: getInfoPairing
# INPUT: pairing - string
# OUTPUT: Dictionary
# DESCRIPTION:
#   Retrieves relevant information for a single pairing on the exchange. This includes
#    items like minimum quantity, maximum quantity, minimum price, and so on.
def getInfoPairing(pairing):
    json_var = getExchangeInfo()["symbols"]

    if "code" in json_var:
        return {
        "success" : False,
        "message" : json_var["msg"]}

    for dictionary in json_var:
        if dictionary["symbol"] == pairing:

            pairing_s = standardizePairing(pairing)
            filters = dictionary["filters"]
            MinTradeSize = float(filters[2]["minNotional"])
            minQty = float(filters[1]["minQty"])
            maxQty = float(filters[1]["maxQty"])
            maxPrice = float(filters[0]["maxPrice"])
            minPrice = float(filters[0]["minPrice"])
            stepSize= float(filters[1]["stepSize"])

            ret_dict = {
                "success" : True,
                "pairing" : pairing_s,
                "min_trade_size" : MinTradeSize,
                "max_quantity" : maxQty,
                "min_quantity" : minQty,
                "max_price" : maxPrice,
                "min_price" : minPrice,
                "step_size" : stepSize
            }

    return ret_dict

# FUNCTION: getInfoPAirings
# INPUT: pairings - [string, ...]
# OUTPUT: Dictionary
# DESCRIPTION:
#   Retrieves relevant information for a list of pairings on the exchange. This includes
#    items like minimum quantity, maximum quantity, minimum price, and so on.
def getInfoPairings(pairings):
    ret_dict = {}
    json_var = getExchangeInfo()["symbols"]
    if "code" in json_var:
        return {
        "success" : False,
        "message" : json_var["msg"]}

    # Build the pairing list for the given exchange. 
    # NOTE: In the future there is probably a better way to do this,
    #        but I'm not sure. This might be the best way to do it.
    #        For the time being, this will be the way to unscramble
    #        pairings.
    pair_list = {}
    for pairing in pairings:
        pair = unscramble(pairing)
        pair_list[pair] = pairing

    for dictionary in json_var:
        if dictionary["symbol"] in pair_list.keys():

            filters = dictionary["filters"]
            MinTradeSize = float(filters[2]["minNotional"])
            minQty = float(filters[1]["minQty"])
            maxQty = float(filters[1]["maxQty"])
            maxPrice = float(filters[0]["maxPrice"])
            minPrice = float(filters[0]["minPrice"])
            inner_pair = pair_list[dictionary["symbol"]]

            nested_dict = {
                "pairing" : inner_pair,
                "min_trade_size" : MinTradeSize,
                "max_quantity" : maxQty,
                "min_quantity" : minQty,
                "max_price" : maxPrice,
                "min_price" : minPrice
            }
            ret_dict[inner_pair] = nested_dict

    ret_dict["success"] = True
    return ret_dict

# FUNCTION: testConnectivity
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#   Ping server for response time.
def testConnectivity():
    json_var = requests.request('GET', 'https://api.binance.com/api/v1/ping').json()

    # Print library to get return dictionary
    PrintLibrary.displayDictionary(json_var)

    if "code" in json_var:
        return {"success" : False,
                "message" : json_var["msg"]}
    ret_dict = {}
    return json_var

######################################## MARKET CALLS ############################################## 
# * - get24hr             : Retrieves 24hr ticker 
# * - getAggTrades        :
# * - getBookTicker       :
# * - getCandlestick      :
# * - getHistoricalTrades :
# * - getOrderbook        :
# * - getPrice            :
# * - getPriceUSD         :
# * - getPriceBTC         :
# * - getTrades           :
################################################################################################### 

# FUNCTION: get24hr
# INPUT: (optional) symbol - string
# OUTPUT: JSON
# DESCRIPTION:
#  Get 24hr ticker price change statistics.
# ** No input returns tickers for all symbols in array
def get24hr(symbol):
    url = V1_URL + 'ticker/24hr'
    json_var = encryptRequest(False, 'GET', url, symbol=symbol)

    return json_var

# FUNCTION: getAggTrades
# INPUT: symbol
# OPTIONALS:  fromId, startTime, endTime, limit
# OUTPUT: JSON
# DESCRIPTION:
#  TODO better description
def getAggTrades(symbol, **kwargs):
    url =  V1_URL + 'aggTrades'
    return encryptRequest(False, 'GET', url, symbol=symbol, **kwargs)

# FUNCTION: getBookTicker 
# INPUT: symbol - string
#             symbol - [string, string, ...]
# OUTPUT: JSON
# DESCRIPTION:
#   Best price & associated quantity on the order book for a symbol or list of symbols
def getBookTicker(symbol=None):
    url = V3_URL + 'ticker/bookTicker'
    return encryptRequest(False,'GET', url, symbol)

# FUNCTION: getCandlestick
# INPUT: symbol - string
#             interval - TODO
#             limit = 500
# OPTIONALS:  startTime, endTime 
# OUTPUT: Dictionary
# DESCRIPTION:
#  Get candlestick data
# ** If startTime and endTime are not sent, the most recent klines are returned.
def getCandlestick(symbol, interval, limit=500,**kwargs):
    url = V1_URL + 'klines'
    return encryptRequest(False, 'GET', url, symbol=symbol, interval=interval, limit=limit,**kwargs)

# FUNCTION: getHistoricalTrades
# INPUT: symbol - string
#             limit = 500
# OUTPUT: Dictionary
# DESCRIPTION:
#  Get older trades
# TODO
# TradeId to fetch from. Default gets most recent trades.
# to use tradeId, include fromId=.... in function args when called 
def getHistoricalTrades(symbol, limit=500, **kwargs):
    url =  V1_URL + 'historicalTrades'
    return encryptRequest(False,'GET',url,symbol=symbol, limit=limit,**kwargs)

# FUNCTION: getOrderbook
# INPUT: symbol(pairing) - string
#             limit - int
# OUTPUT: Dictionary
# DESCRIPTION:
#   Get bid/ask book
def getOrderbook(symbol, limit=10):
    url =  V1_URL + 'depth'
    json_var = encryptRequest(False, 'GET', url, symbol=symbol, limit=limit)
    if "msg" in json_var:
        dict_error = {
        "success": False
        }
        return dict_error
    json_bids = json_var["bids"]

    dict_bids = []
    for bid in json_bids:
        dict_bids.append( (bid[0],bid[1]) )
    json_asks = json_var["asks"]

    dict_asks = []
    for ask in json_asks:
        dict_asks.append( (ask[0],ask[1]) )

    ret_dict = {
        "success" : True,
        "bids" : dict_bids,
        "asks" : dict_asks
    }

    return ret_dict

# FUNCTION: getPrice
# INPUT: (optional) symbol - string
# OUTPUT: JSON
# DESCRIPTION:            
#  Get latest price for a market pairing
# ** NOT SUPPORTED: url = If the symbol is not sent, prices for all symbols will be returned in an array.
def getPrice(symbol=None):
    url = V3_URL + 'ticker/price'
    json_var = encryptRequest(False, 'GET', url, symbol=symbol)
    if "msg" in json_var:
        price = 0
    # TODO clean up the below
    else: 
        price = json_var["price"]
    ret_dict = {"price":price}
    return float(price)

def getPriceUSD(symbol):
    if symbol != "BTCUSDT":
        price_symb = getPrice(symbol)
    else:
        price_symb = 1
    price_btc = getPrice('BTCUSDT')
    price_usd = price_symb * price_btc
    return price_usd

# FUNCTION: getTrades
# INPUT: symbol(pairing) - string
#            limit - int
# OUTPUT: JSON
# DESCRIPTION:
# Get recent trades
def getTrades(symbol, limit=500):
    url =  V1_URL + 'trades'
    return encryptRequest(False, 'GET', url, symbol=symbol, limit=limit)

######################################## ORDER CALLS ############################################## 
# * - cancelOrder :
# * - queryOrder  :
# * - postOrder   :
# * - testOrder   : tests an given order, does not actually execute the order.
#   ORDER DERIVATIVES
# * - buyLimit    :
# * - sellLimit   :
# * - stopLoss    :
# * - stopLossLim :
################################################################################################### 

# FUNCTION: cancelOrder
# INPUT: symbol - string
# OPTIONALS: orderId, origClientOrderId, newClientOrderId, recvWindow
# OUTPUT: Dictionary
# DESCRIPTION:
#   Cancel an open trade. Requires both symbol and the order id.
def cancelOrder(order_id, symbol):
    url = V3_URL + 'order'

    # Check if id is orderId or clientId by length
    if len(order_id) > 8:
        ret_json = encryptRequest(True, 'DELETE', url, symbol=symbol, origClientOrderId=order_id)
    else:
        ret_json = encryptRequest(True, 'DELETE', url, symbol=symbol, orderId=order_id)
    
    success = not ("code" in ret_json)
    if 'msg' in ret_json:
        if ret_json["msg"] == "UNKOWN_ORDER":
            message = "order_closed"
        else:
            message = ret_json["msg"]
    else:
        message = ""
    ret_dict = {
    "success" : success,
    "order_id" : order_id,
    "error" : message
    }

    return ret_dict

# FUNCTION: queryOrder
# INPUT:  symbol - string
# OPTIONALS: orderId, origClientOrderId, recvWindow
# OUTPUT: Dictionary
# DESCRIPTION:
#   Check an order's status. Uses one of the orderIds to access the order.
def queryOrder(symbol, clientOrderId, **kwargs):
    url = V3_URL + 'order'
    ret_json = encryptRequest(True, 'GET', url, symbol=symbol, origClientOrderId=clientOrderId, **kwargs)
    if "code" in ret_json:
        return {"success" : False,
                "message" : json_var["msg"]}
    side = ret_json["side"]
    original_quantity_s = ret_json["origQty"]
    original_quantity = float(original_quantity_s)
    executed_quantity_s = ret_json["executedQty"]
    executed_quantity = float(executed_quantity_s)
    price_s = ret_json["price"]
    price = float(price_s)
    status = ret_json["status"]
    remaining = original_quantity - executed_quantity
    incomplete = True if remaining > 0 else False
    ret_dict = {
        "success" : True,
        "side" : side,
        "original_quantity" : original_quantity,
        "executed_quantity" : executed_quantity,
        "remaining_quantity" : remaining,
        "incomplete" : incomplete,
        "rate" : price, 
        "status" : status
    }

    return ret_dict

# FUNCTION: postOrder
# INPUT: symbol   - string
#        side     - string
#        typeE    - string
#        quantity - float
# OPTIONALS: timeInForce, price, newClientOrderId, stopPrice, icebergQty, newOrderRespType, recvWindow
# OUTPUT: Dictionary
# DESCRIPTION:
#  Post an order (buy or sell limit or stop loss)
# ** ADDITIONAL MANDATORY PARAMETERS NEEDED BASED ON REQUEST TYPE
def postOrder(symbol, side, typeE, quantity, timeInForce='GTC', **kwargs):
    url = V3_URL + 'order'

    json_ret = encryptRequest(True, 'POST', url, symbol=symbol, side=side, type=typeE, 
                                quantity=quantity, timeInForce=timeInForce, **kwargs)
    if "code" in json_ret:
        print("JSON_RET", json_ret)
        return {"success": False,
                "message" : json_ret["code"]}

    client_id = json_ret["clientOrderId"]
    filled = (json_ret["status"] == "FILLED")
    original_quantity = float(json_ret["origQty"])
    executed_quantity = float(json_ret["executedQty"])
    quote = quoteSymbol(symbol)

    ret_dict = {
    "success" : True,
    "order_id" : client_id,
    "filled" : filled,
    "original_quantity" : original_quantity,
    "filled_quantity" : executed_quantity,
    "btc_value" : 0,
    "usd_value" : 0,
    "exchange" : "binance",
    "asset" : quote,
    "pairing" : symbol
    }

    return ret_dict

# FUNCTION: testOrder
# INPUT: symbol - string
#        side - string
#        typeE - string
#        quantity - double
# OPTIONALS: timeInForce, price, newClientOrderId, stopPrice, icebergQty, newOrderRespType, recvWindow
# OUTPUT: JSON
# DESCRIPTION:
#  Test an order, to ensure that it would process as desired
# ** ADDITIONAL MANDATORY PARAMETERS NEEDED BASED ON REQUEST TYPE
def testOrder(symbol, side, typeE, quantity, **kwargs):
    url = V3_URL + 'order/test'
    return encryptRequest(True, 'POST', url, symbol=symbol, side=side, type=typeE, quantity=quantity, **kwargs)

# WRAPPER: buyLimit
# INPUT: symbol   - string
#        quantity - float
#        rate     - float
# OUTPUT: dictionary
# DESCRIPTION:
#   Wrapper for postOrder call in order to make a sell limit order
def buyLimit(symbol, quantity, rate):
    quantity = BinanceErrors.handleOrderReq(symbol, quantity, rate)
    rate = BinanceErrors.convertMinPrice(rate, symbol)
    if quantity == 0:
        return {"success" : False,
                    "filled_quantity" : 0,
                    "rate" : rate,
                    "symbol" : symbol,
                    "error" : "min_notional",
                    "exchange" : "binance",
                    "side" : "buy",
                    "btc_value" : 0}
    # print("symbol/quantity/rate before buy limit BINANCE: ", symbol, quantity, rate)
    return_dict = postOrder(symbol, "BUY", "LIMIT", quantity, price=rate)
    return_dict["rate"] = rate
    return_dict["type"] = "limit"
    return_dict["side"] = "buy"
    btc_value = float(return_dict["filled_quantity"]) * float(rate)
    return_dict["btc_value"] = btc_value
    return return_dict

# WRAPPER: sellLimit
# INPUT: symbol   - string
#        quantity - float
#        rate     - float
# OUTPUT: dictionary
# DESCRIPTION: 
#   Wrapper for postOrder call in order to make a sell limit order.
def sellLimit(symbol, quantity, rate):
    quantity = BinanceErrors.handleOrderReq(symbol, quantity, rate)
    rate = BinanceErrors.convertMinPrice(rate, symbol)
    if quantity == 0:
        return {"success" : False,
                    "filled_quantity" : 0,
                    "rate" : rate,
                    "symbol" : symbol,
                    "error" : "min_notional",
                    "exchange" : "binance",
                    "side" : "sell",
                    "btc_value" : 0}
    # print("Quantity before sell limit BINANCE: ", quantity)
    return_dict = postOrder(symbol, "SELL", "LIMIT", quantity, price=rate)
    return_dict["rate"] = rate
    return_dict["type"] = "limit"
    return_dict["side"] = "sell"
    btc_value = float(return_dict["filled_quantity"]) * float(rate)
    return_dict["btc_value"] = btc_value
    return return_dict

# WRAPPER: stopLoss
# INPUT: type_trade - string ['sell' or 'buy']
#        symbol     - string
#        quantity   - float
#        stop_rate  - float
# OUTPUT: Dictionary
# DESCRIPTION:
#   Perform a stop-loss trade. 
def stopLoss(type_trade, symbol, quantity, stop_rate):
    pass

# WRAPPER: stopLossLimit
# INPUT: type_trade - string ['sell' or 'buy']
#        symbol     - string
#        quantity   - float
#        stop_rate  - float
#        limit_rate - float
# OUTPUT: Dictionary
# DESCRIPTION:
#   Perform a stop-loss limit trade.
def stopLossLimit(type_trade, symbol, quantity, stop_rate, limit_rate):
    pass

####################################### ACCOUNT CALLS ############################################# 
# * - getAllOrders  :
# * - getBalance    :
# * - getBalances   :
# * - getMyTrades   :
# * - getOpenOrders :
################################################################################################### 

# FUNCTION: getAllOrders
# INPUT: symbol - string
# OPTIONALS: origClientOrderId(TODO), orderId, limit, recvWindow,
# OUTPUT: dictionary
# DESCRIPTION:
#   Return all orders (closed and open)
def getAllOrders(symbol, **kwargs):
    url = V3_URL + 'allOrders'
    return encryptRequest(True, 'GET', url,symbol=symbol,**kwargs)

# FUNCTION: getAccount
# INPUT: asset - string
# OUTPUT: dictionary
# DESCRIPTION:
#   Return's the account information
def getBalance(asset):
    url = V3_URL + 'account'
    json_var = encryptRequest(True, 'GET', url)

    if "code" in json_var:
        return {"success" : False,
                "message" : json_var["msg"]}

    balance_list = json_var["balances"]
    for bal in balance_list:
        if bal["asset"] == asset:
            total = float(bal["free"])+float(bal["locked"])
            free = float(bal["free"])
            locked = float(bal["locked"])

            ret_dict = {
                "success" : True,
                "currency" : asset,
                "total_balance" : total,
                "available_balance" : free,
                "locked_balance" : locked
            }
            return ret_dict

    ret_dict = {
    "success" : False
    }

    return ret_dict

# FUNCTION: getBalances
# INPUT: N/A
# OUTPUT: dictionary
# DESCRIPTION:
#   Retrieves the balances for the entire account.
def getBalances():
    url = V3_URL + 'account'
    json_var = encryptRequest(True, 'GET', url)
    if "code" in json_var:
        return {"success" : False,
                "message" : json_var["msg"]}

    balance_list = json_var["balances"]
    ret_dict = {}
    for bal in balance_list:
        asset = bal["asset"]
        total = float(bal["free"]) + float(bal["locked"])
        free = float(bal["free"])
        locked = float(bal["locked"])

        nested_dict = {
        "total_balance" : total,
        "available_balance" : free,
        "locked_balance" : locked
        }
        ret_dict[asset] = nested_dict
    
    ret_dict2 = {
    "success" : True,
    "balances" : ret_dict
    }

    return ret_dict2

# FUNCTION: getMyTrades
# INPUT: symbol - string
# OPTIONALS:  limit, fromId, recvWindow, 
# OUTPUT: JSON
# DESCRIPTION:
#  Return account trade list
def getMyTrades(symbol, **kwargs):
    url = V3_URL + 'myTrades'
    return encryptRequest(True, 'GET', url, symbol=symbol, **kwargs)

# FUNCTION: getOpenOrders
# INPUT: N/A
# OPTIONALS: symbol, recvWindow
# OUTPUT: JSON
# DESCRIPTION:
#  Return all open orders
# ** CAREFUL WHEN USING THIS WITH NO SYMBOLS
# * When all symbols are returned, the number of requests counted against the rate limiter is equal 
#   to the number of symbols currently trading on the exchange.
def getOpenOrders(**kwargs):
    url = V3_URL + 'openOrders'
    return encryptRequest(True, 'GET', url, **kwargs)


######################################### WAPI CALLS ############################################## 
# * - getAccountStatus          :
# * - getDepositAddress         :
# * - checkDeposit              :
# * - getDeposit                :
# * - getDepositHistory         :
# * - getDepositHistoryAsset    :
# * - getWithdrawal             :
# * - getWithdrawalHistory      :
# * - getWithdrawalHistoryAsset :
# * - withdraw                  :
################################################################################################### 

# FUNCTION: getAccountStatus
# INPUT: N/A
# OPTIONALS: recvWindow
# OUTPUT: JSON
# DESCRIPTION:
#  Get the status of account
def getAccountStatus(**kwargs):
    url = WAPI_URL + 'accountStatus.html'
    return encryptRequest(False, 'GET', url, **kwargs)

# FUNCTION: getDepositAddress
# INPUT: asset - string
# OPTIONALS: recvWindow
# OUTPUT: JSON
# DESCRIPTION:
#  Get the deposit address for a currency. 
def getDepositAddress(asset, **kwargs):
    url = WAPI_URL + 'depositAddress.html'
    json_var = encryptRequest(True, 'GET', url, asset=asset, **kwargs)
    print(json_var)

    # JSON STANDARDIZATION
    if json_var["success"] == True:
        ret_dict = {
        "success" : True,
        "currency" : asset,
        "address" : json_var["address"],
        "withdrawal_tag" : json_var["addressTag"]
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
def getDepositHistory(**kwargs):
    url = WAPI_URL + 'depositHistory.html'
    json_var = encryptRequest(True, 'GET', url, **kwargs)
    
    # TODO: fix
    if 'msg' in json_var:
        return -1

    json_var2 = json_var["depositList"]
    ret_list = []
    for value in json_var:
        tx_id = value["txId"]
        open_date = value["insertTime"]
        asset = value["asset"]
        address = value["address"]
        status = value["status"]
        amount = value["amount"]

        nested_dict = {
        "tx_id" : tx_id,
        "opened" : open_date,
        "address" : address,
        "amount" : amount
        }

        ret_list.append(nested_dict)

    return ret_list

# FUNCTION: getDepositHistory
# INPUT: currency - string
#        quantity - float [TODO]
# OUTPUT: dictionary
# DESCRIPTION:
#   Retrieves the deposit history for all assets.
# * TODO - add quantity/start time
# * TODO - dictionary/list thing 
def getDepositHistoryAsset(asset):
    url = WAPI_URL + 'depositHistory.html'    
    json_var = encryptRequest(True, 'GET', url, asset=asset)
    
    # TODO: fix
    if 'msg' in json_var:
        return -1

    json_var2 = json_var["depositList"]
    ret_list = []
    for value in json_var2:
        tx_id = value["txId"]
        open_date = value["insertTime"]
        asset = value["asset"]
        address = value["address"]
        status = value["status"]
        amount = value["amount"]

        nested_dict = {
        "tx_id" : tx_id,
        "opened" : open_date,
        "address" : address,
        "amount" : amount,
        "asset" : asset
        }

        ret_list.append(nested_dict)

    return ret_list

# FUNCTION: getWithdrawHistory
# INPUT: N/A
# OPTIONALS: asset, status, startTime, endTime, recvWindow
# OUTPUT: JSON
# DESCRIPTION:
#  Return JSON object of account's withdrawal history
def getWithdrawalHistory(**kwargs):
    url = WAPI_URL + 'withdrawHistory.html'
    json_var = encryptRequest(True, 'GET', url, **kwargs)

    # TODO: fix
    if 'msg' in json_var:
        return -1    

    json_var2 = json_var["withdrawList"]

# FUNCTION: withdraw
# INPUT:     asset   - string
#            address - string
#            amount  - double
# OPTIONALS: addressTag - string
#            name, recvWindow
# OUTPUT: Dictionary
# DESCRIPTION:
#  Submit a withdraw request
def withdraw(asset, amount, address, addressTag="", **kwargs):
    url = WAPI_URL + 'withdraw.html'
    # TODO, re-add addressTag
    json_var = encryptRequest(True, 'POST', url, asset=asset, address=address, amount=amount, name="bittrex", addressTag=addressTag, **kwargs)
    print(json_var["success"])
    
    if 'msg' in json_var:
        print(json_var["msg"])

    if "code" in json_var:
        print(json_var["code"])
        print("JSONREST", json_var)
        return {"success" : False,
                "message" : json_var["msg"]}

    timestamp = time.time() 
    withdrawal_id = json_var["id"]
    ret_dict = {
        "success" : True,
        "id" : withdrawal_id,
        "exchange" : "binance",
        "amount" : amount,
        "asset" : asset,
        "address" : address,
        "time" : timestamp,
        "paymentid" : addressTag
    }

    return ret_dict


########################################## HELPERS ################################################
# * - encryptRequest     : Encryption method.                                                     #
# * - quoteSymbol        : Return quote symbol specifically in Binance's format.                  # 
# * - standardizePairing : Convert pairing from Binance format to standard format.                # 
# * - unscramblePairing  : Convert pairing from standard format to Binance format                 #
###################################################################################################

# FUNCTION: encryptRequest
# INPUT: signature - boolean
#        method    - 'POST' or 'GET'
#        end       - url (string)
#        * - Query vars passed in as list of params (a=1,b=2,c=3)
# OUTPUT: Encrypted url used for HTTPS request
# DESCRIPTION:
#   Encrypts an API request to Binance.
def encryptRequest(signature, method, end, **query_vars):
    header = {'X-MBX-APIKEY':binance_public_key}
    queryString = "&".join(['%s=%s' % (key,value) for (key,value) in query_vars.items()])
    if signature:
        if "recvWindow" not in query_vars and "timestamp" not in query_vars:
            extra = "&recvWindow=5000&timestamp=" + str(int(time.time()*1000))
        elif "timestamp" not in query_vars:
            extra = "&timestamp=" + str(int(time.time()*1000))
        elif "recvWindow" not in query_vars:
            extra = "&recvWindow=5000"
        queryString += extra
        sig = hmac.new(binance_private_key.encode(),queryString.encode(),'sha256')
        signature = sig.hexdigest()
        sigstring = "&signature=%s" % (signature)
        url = end + "?" + queryString + sigstring
    else:
        url = end + "?" + queryString

    req = requests.request(method,url,headers=header).json()
    return req

# FUNCTION: quoteSymbol
# INPUT: pairing - string ("ETHBTC" format)
# OUTPUT: string
# DESCRIPTION:
#   Returns just the qutoe symbol from an input pairing. Standardizes it first in the current case.
#    This function will get reworked in the future.
def quoteSymbol(pairing):
    pairing = standardizePairing(pairing)
    base, quote = pairing.split("-")
    return quote

# FUNCTION: standardizePairing
# INPUT: pairing - string
# OUTPUT: string
# DESCRIPTION:
#   Takes a pairing that is in the base binance format ("ETHBTC") and standardizes it to the
#    generic format ("BTC-ETH").
def standardizePairing(pairing):
    length = len(pairing)
    if length == 6:
        return pairing[3:6] + "-" + pairing[0:3]
    elif length == 7:
        return pairing[3:7] + "-" + pairing[0:3]
    elif length == 8:
        return pairing[3:8] + "-" + pairing[0:3]
    elif length == 9:
        return pairing[3:6] + "-" + pairing[0:3]
    else:
        print("Error in pairing length: ", pairing)

# FUNCTION: unscramblePairing
# INPUT: pairing - string
# OUTPUT: string
# DESCRIPTION:
#   Takes a pairing that is standarized to the generic format ("BTC-ETH") and converts it
#    to Binanace's input format ("ETHBTC").
def unscramblePairing(pairing):
    base, quote = pairing.split("-")
    return quote + base


######################################### WEB SOCKET ##############################################
# * - startUsrStrm     :
# * - keepaliveUsrStrm : 
# * - closeUsrStrm     :
###################################################################################################
# Work in Progress

def startUsrStrm():
    url = V1_URL + 'userDataStream'
    return encryptRequest(False, 'POST', url)

def keepaliveUsrStrm():
    url = V1_URL + 'userDataStream'
    return encryptRequest(False, 'PUT', url)

def closeUsrStream(listenKey):
    url = V1_URL + 'userDataStream'
    return encryptRequest(False, 'DELETE', url, listenKey=listenKey)


# CLASS: BinanceErrors
# DESCRIPTION:
#   Library of functions pertaining to handling errors produced by Binance.

# Error Codes:
# Code 0000: TODO
class BinanceErrors():

    def handleOrderReq(symbol, quantity, rate):
        # 0.  Check predictable symbol issues
        # TODO

        # 1.  Check Min order
        quantity = BinanceErrors.checkMinOrder(symbol, quantity, rate)
        return quantity
        # 1.1 Check max order
        # TODO

        # 2.  Check lot size

    # FUNCTION: checkMin[imum]Order
    # INPUT: pairing      - string
    #        exchange_one - string
    #        exchange_two - string
    #        quantity     - float
    #        rate         - float
    # OUTPUT: quantity [float]
    # DESCRIPTION:
    #   Checks to ensure that order parameters fit minimum order size for Binance.
    def checkMinOrder(pairing, quantity, rate):
        order_size = quantity * rate
        notional_dict = getInfoPairing(pairing)
        notional = notional_dict["min_trade_size"]
        if order_size < notional:
            print(" - Binance: ORDER IS BELOW THRESHOLD: " + str(order_size))
            return 0
        else:
            # Perform Lotsize conversion
            step_size = notional_dict["step_size"]
            qty_trim = quantity % step_size
            quantity = quantity - qty_trim
        return quantity

    # FUNCTION: convertMinPrice
    # INPUT: price    - float
    #        pairing  - string
    # OUTPUT: price [float]
    # DESCRIPTION:
    #   Converts a given price to the minimum price for a pairing.
    def convertMinPrice(price, pairing): 
        trim_value = getInfoPairing(pairing)
        precision = BinanceErrors.determinePrecision(trim_value["min_price"])
        temp_string = "{:." + str(precision) + "f}"
        price = temp_string.format(price)
        return price

    # FUNCTION: determinePrecision
    # INPUT: value - float
    # OUTPUT: integer
    # DESCRIPTION:
    #   Assesses the precision of the input value.
    def determinePrecision(value):
        if value == 1.0:
            return 0
        if value == 0.1:
            return 1
        if value == 0.01:
            return 2
        if value == 0.001:
            return 3
        if value == 0.0001:
            return 4
        if value == 0.00001:
            return 5
        if value == 0.000001:
            return 6
        if value == 0.0000001:
            return 7
        if value == 0.00000001:
            return 8
        else:
            return 0
