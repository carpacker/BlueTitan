# cryptopiaAPI.py
# WORK IN PROGRESS, CURRENTLY DEPRECATED DUE TO ERRORS ON CRYPTOPIA'S SIDE

import json
import requests
import hmac
import time
import hashlib
import base64
from requests.compat import quote_plus

from secret_keys import cryptopia_public_key, cryptopia_private_key

# PUBLIC
def getCurrencies():
    json_var = requests.request('GET', 'https://www.cryptopia.co.nz/api/GetCurrencies').json()

    # JSON STANDARDIZATION
    if json_var["Success"] == True:
        json_var2 = json_var["Data"]
        ret_dict2 = {}
        for currency in json_var2:
            #currency_long = json_var["CurrencyLong"]
            #min_confirmation = json_var["MinConfirmation"]
            transaction_fee = currency["WithdrawFee"]
            is_active = currency["ListingStatus"]
            #coin_type = json_var["CoinType"]
            #base_address = json_var["BaseAddress"]
            nested_dict = {
            "transaction_fee" : transaction_fee,
            "is_active" : is_active
            }
            currency_value = currency["Symbol"]
            ret_dict2[currency_value] = nested_dict
        ret_dict = {
        "success" : True,
        "balances" : ret_dict2
        }
    else:
        ret_dict ={
        "Success" : False
        }

    return ret_dict    

def getTradePairs():
    req = requests.request('GET', 'https://www.cryptopia.co.nz/api/GetTradePairs').json()
    return req

def getMarkets(*args):
    # optional arguments for getMarkets is baseMarket and hours
    # if both are used as parameters, first argument must be baseMarket
    # default market is all, and default is 24
    url = 'https://www.cryptopia.co.nz/api/GetMarkets'
    if args:
        for arg in args:
            url += '/' + arg

    req = requests.request('GET', url).json()
    return req

def getMarket(market_name, hours=None):
    # market_name parameter is required
    # hours parameter is optional, defaults to 24 hours
    url = 'https://www.cryptopia.co.nz/api/GetMarket/' + market_name
    if hours:
        url += '/' + hours
    req = requests.request('GET', url).json()
    return req

def getMarketHistory(market_name, hours=None):
    # market_name parameter is required
    # hours parameter is optional, defaults to 24 hours
    url = 'https://www.cryptopia.co.nz/api/GetMarketHistory/' + market_name
    if hours:
        url += '/' + hours
    req = requests.request('GET', url).json()
    return req

def getMarketOrders(market_name, order_count=None):
    # market_name parameter is required
    # order_count parameter is optional, defaults to 100
    url = 'https://www.cryptopia.co.nz/api/GetMarketOrders/' + market_name
    if order_count:
        url += '/' + order_count
    json_var = requests.request('GET', url).json()
    # JSON STANDARDIZATION
    if json_var["Success"] == True:
        json_var2 = json_var["Data"]
        bids = json_var2["Buy"]
        asks = json_var2["Sell"]
        dict_bids = []
        dict_asks = []
        for bid in bids:
            dict_bids.append((bid["Price"], bid["Volume"]))
        for ask in asks:
            dict_asks.append((ask["Price"], ask["Volume"]))

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

def getMarketOrderGroups(*args, order_count=None):
    # market_name parameter is required, input many markets
    # order_count parameter is optional, defaults to 100
    url = 'https://www.cryptopia.co.nz/api/GetMarketOrderGroups/'
    if args:
        for arg in args:
            url += arg + '-'
    if order_count:
        url += '/' + order_count
    req = requests.request('GET', url).json()
    return req

# PRIVATE

def getBalance(currency=None):
    # Returns all balances by default, or returns balance for a single currency
    # if currency is specified
    url = 'https://www.cryptopia.co.nz/Api/GetBalance'
    data = {'Currency': currency}
    req = headerSetup(url=url, post_data=data)
    json_var = req.json()
    # JSON STANDARDIZATION
    if json_var["Success"] == True:
        json_var2 = json_var["Data"][0]
        currency = json_var2["Symbol"]
        total_balance = json_var2["Total"]
        available_balance = json_var2["Available"]
        pending_balance = json_var2["PendingWithdraw"]
        address = json_var2["Address"]

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

def getBalances():
    url = 'https://www.cryptopia.co.nz/Api/GetBalance'
    data = {'Currency' : ''}
    req = headerSetup(url=url, post_data=data)
    json_var = req.json()

    # JSON STANDARDIZATION
    if json_var["Success"] == True:
        json_var3 = json_var["Data"]
        ret_dict2 = {}
        for json_var2 in json_var3:
            currency = json_var2["Symbol"]
            total_balance = json_var2["Total"]
            available_balance = json_var2["Available"]
            pending_balance = json_var2["PendingWithdraw"]
            address = json_var2["Address"]

            nested_dict = {
            "currency" : currency,
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

def getDepositAddress(currency):
    url = 'https://www.cryptopia.co.nz/Api/GetDepositAddress'
    data = {'Currency': currency}
    req = headerSetup(url=url, post_data=data)
    response = req.json()
    return response

    # JSON STANDARDIZATION
    if json_var["Success"] == True:
        json_var2 = json_var["Data"]
        currency = json_var2["Currency"]
        address = json_var2["Address"]

        ret_dict = {
        "success" : True,
        "currency" : currency,
        "address" : address
        }
    else:
        ret_dict ={
        "success" : False
        }

    return ret_dict

def getOpenOrders(market, count=100):
    url = 'https://www.cryptopia.co.nz/Api/GetOpenOrders'
    data = {'Market': market, 'Count': count}
    req = headerSetup(url=url, post_data=data)
    response = req.json()
    return response

def getTradeHistory(market, count=100, tradePairId=None):
    url = 'https://www.cryptopia.co.nz/Api/GetTradeHistory'
    data = {'Market': market, 'TradePairId' : tradePairId, 'Count': count}
    req = headerSetup(url=url, post_data=data)
    response = req.json()
    return response

def getTransactions(trantype, count):
    url = 'https://www.cryptopia.co.nz/Api/GetTransactions'
    data = {'Type': trantype, 'Count': count}
    req = headerSetup(url=url, post_data=data)
    response = req.json()
    return response

def getDepositHistory():
    pass

def getWithdrawalHistory():
    pass

def submitTrade(market, trantype, amount, rate):
    url = 'https://www.cryptopia.co.nz/Api/SubmitTrade'
    data = {'Market': market, 'Type': trantype, 'Rate': rate, 'Amount': amount}
    req = headerSetup(url=url, post_data=data)
    json_var = req.json()
    # JSON STANDARDIZATION
    if json_var["Success"] == True:
        json_var2 = json_var["Data"]
        order_id = json_var2["OrderId"]
        filled_orders = json_var2["FilledOrders"]

        ret_dict = {
        "success" : True,
        "order_id" : order_id
        }
    else:
        ret_dict ={
        "success" : False
        }

    return ret_dict


def buyLimit(market, amount, rate):
    if amount * rate < .0005:
        ret_dict = {
        "success": False
        }
        return ret_dict

    ret_dict = submitTrade(market, "Buy", amount, rate)
    return ret_dict

def sellLimit(market, amount, rate):
    if amount * rate < .0005:
        ret_dict = {
        "success": False
        }
        return ret_dict

    ret = submitTrade(market, "Sell", amount, rate)
    return ret

def cancelTrade(typeE, orderId=None, tradePairId=None):
    url = 'https://www.cryptopia.co.nz/Api/CancelTrade'
    data = {'Type': typeE, 'OrderId': orderId, 'TradePairId': tradePairId}
    req = headerSetup(url=url, post_data=data)
    response = req.json()
    return response

    # JSON STANDARDIZATION
    if json_var["Success"] == True:
        ret_dict = {
        "success" : True
        }
    else:
        ret_dict = {
        "success" : False
        }

    return ret_dict

# WRAPPER: getOrder
def getOrder(order_id, market):
    json = getOpenOrders(market)
    data_list = json["Data"]  
    ret_dict = {}
    for element in data_list:
        if element["OrderId"] == order_id:
            original_quantity = element["Amount"]
            remaining = element["Remaining"]
            executed_quantity = original_quantity - remaining
            side = element["Type"]
            status = "isOpen"

            ret_dict = {
            "success" : True,
            "side" : side,
            "original_quantity" : original_quantity,
            "executed_quantity" : executed_quantity,
            "remaining_quantity" : remaining,
            "status" : status,
            "incomplete" : True
            }
            return ret_dict

    ret_dict = {
    "success" : False, 
    "incomplete" : False
    }
    return ret_dict

def submitWithdraw(currency, address, paymentId, amount):
    url = 'https://www.cryptopia.co.nz/Api/SubmitWithdraw'
    data = {'Currency': currency, 'Address': address, 'PaymentId': paymentId, 'Amount': amount}
    req = headerSetup(url=url, post_data=data)
    response = req.json()

    # JSON STANDARDIZATION
    if json_var["Success"] == True:
        order_id = json_var["Data"]
        ret_dict = {
        "success" : True,
        "order_id" : order_id
        }
    else:
        ret_dict ={
        "success" : False
        }

    return ret_dict

def returnExchangeInfo():
    pass

def headerSetup(url, post_data):
    nonce = str(int(time.time()))
    json_data = json.dumps(post_data).encode('utf-8')
    md5 = hashlib.md5()
    md5.update(json_data)
    rcb64 = base64.b64encode(md5.digest()).decode('utf-8')
    signature = cryptopia_public_key + "POST" + quote_plus(url).lower() + nonce + rcb64
    hmacsig = base64.b64encode(hmac.new(base64.b64decode(cryptopia_private_key),
                                                        signature.encode('utf-8'),
                                                        hashlib.sha256).digest())
    header_value = "amx " + cryptopia_public_key + ":" + hmacsig.decode('utf-8') + ":" + nonce
    headers = { 'Authorization': header_value, 'Content-Type': 'application/json; charset=utf-8' }
    req = requests.post(url, data=json_data, headers=headers)
    return req