
'''
#                                        Helpers 

This script contains a set of classes that contain helper runctions for specific components 
of the systems. There is also a suite of functions outside of any class definition that are 
general purpose functions, used in many places because of their general application. 

'''

#                                       Imports

import sys

# WINDOWS
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Crypto-API/Exchange-APIs/')

# LINUX
# sys.path.append()

# External-Imports
import time
from datetime import datetime
from collections import defaultdict

# Internal-Imports
from API import ExchangeAPI
from DatabaseManager import ArbitrageDatabase

#                                    General Helpers

# * btcValue            - Convert an asset to BTC value
# * calculatePR         - Calculate the profit ratio given two prices
# * calculateProfit     - Calculate profit given prices and quantity
# * convertFromUnix     - Timestamp converter
# * convertToUnix       - Timestamp converter
# * createUuid          - Used to create a unique identifier for the internal uuid system
# * determinePrecision  - Used to navigate excvhange's requirements on precission
# * quoteAsset          - Quote asset converter [btc as input value w/ asset]
# * reversePairings     - Reverse a list of pairings (made by selim)
# * usdValue            - Output USD value of some quantity of asset

# FUNCTION: btcValue
# INPUT: quantity - float
#        asset    - string
#        exchange - string (OPTIONAL)
# OUTPUT: float
# DESCRIPTION:
#   Returns the BTC value of a specific asset. If an exchange is given, the price used to find
#    this value is taken fro mthe provided exchange, otherwise coinmarketcap is used.
def btcValue(asset, quantity, exchange=None):
    if asset == "BTC":
        return quantity
    else:
        if exchange:
            pairing = pairingStr(asset)
            price = ExchangeAPI.getPrice(exchange, pairing)
            value = float(price) * quantity
            return value

        else: 
            pairing = pairingStr(asset)
            price = ExchangeAPI.getPrice("coinmarketcap", pairing)
            value = float(price) * quantity
            return value

# FUNCTION: calculateOrderFee
# INPUT: exchange  - string
#        btc_value - float
# OUTPUT: float
# DESCRIPTION:
#   Calculates the fee for a specific order, in terms of BTC.
def calculateOrderFee(exchange, btc_value):
    rate = getFee(exchange)
    value = btc_value * rate
    print("calculateOrderFee", value, rate, btc_value)
    return value

# FUNCTION: calculateProfitRatio
# INPUT: sell_price - float
#        buy_price  - float
# OUTPUT: float
# DESCRIPTION:
#  Calculate the profit ratio of a trade event.
def calculatePR(sell_price, buy_price):
    return 100 * (sell_price - buy_price) / sell_price

# FUNCTION: calculateProfit
# INPUT: sell_price - float
#        buy_price  - float
#        quantity   - float
# OUTPUT: float
# DESCRIPTION:
#  Calculate the raw profit of a trade event.
def calculateProfit(sell_price, buy_price, quantity):
    profit_off = sell_price - buy_price
    profit = quantity * profit_off
    return profit

# FUNCTION: createTimestamp
# INPUT: N/A
# OUTPUT: float
#   Creates a Unix-based timestamp.
def createTimestamp():
    value = int(time.time() * 1000)
    return value

# FUNCTION: convertToUnix
# INPUT: timestamp - string
# OUTPUT: integer
# DESCRIPTION:
#   Converts Unix-based timestamp to string-date format [YYYY-MM-DD HH:MM:SS].
def convertToUnix(timestamp):
    timestamp_unix = time.mktime(datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").timetuple())
    return timestamp_unix

# FUNCTION: convertFromUnix
# INPUT: timestamp - int
# OUTPUT: string
# DESCRIPTION: 
#   Converts given string-date formatted timestamp to a Unix-based timestamp.
def convertFromUnix(timestamp):
    time_temp = timestamp / 1000
    timestamp = datetime.fromtimestamp(time_temp)
    timestamp_formatted = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return timestamp_formatted

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

# FUNCTION: getFee
# INPUT: exchange - string
# OUTPUT: float
# DESCRIPTION:
#   Used to output fee for passed in exchange.
def getFee(exchange):
    if exchange == 'bittrex':
        fee = .0025
    elif exchange == 'binance':
        fee = .0005
    elif exchange == 'cryptopia':
        fee = .002
    elif exchange == 'poloniex':
        fee = 0
    elif exchange == 'kucoin':
        fee = 0
    elif exchange == 'hitbtc':
        fee = 0
    else:
        print("ERROR: " + str(exchange) + " NOT SUPPORTED")
        return -1
    return fee

# 'stupid' function used for convenience in BalancingLibrary for now. [5/4/18]
def inverseExchange(exchange):
    if exchange == "binance":
        return "bittrex"
    if exchange == "bittrex":
        return "binance"

# FUNCTION: quoteAsset
# INPUT:  quantity - float
#         price    - float
# OUTPUT: float
# DESCRIPTION:
#   Converts base asset value to quote asset value
#  * - TODO Figure out where this is called and replace it with quoteValue
def quoteAsset(quantity, price):
    return quantity / price

# FUNCTION: quoteAssetStr
# INPUT: pairing - string
# OUTPUT: string
# DESCRIPTION:
#   Simple wrapper function used to output the quote asset in a pairing.
def quoteAssetStr(pairing):
    return pairing[4:7]

# FUNCTION: quoteValue
# INPUT: quantity - float
#        asset    - string
#        exchange - string
# OUTPUT: float
# DESCRIPTION:
#   Returns the quote value of a specified input quantity that is given in terms of BTC. If an exchange
#    is given, the price used to find this value is taken from the provided exchange, otherwise 
#    coinmarketcap is used.
def quoteValue(asset, quantity, exchange=None):
    if quantity == 0:
        return 0
    if asset == "BTC":
        return quantity
    else:
        if exchange:
            pairing = pairingStr(asset)
            price = ExchangeAPI.getPrice(exchange, pairing)
            value = quantity / float(price)
            return value

        else: 
            pairing = pairingStr(asset)
            price = ExchangeAPI.getPrice("coinmarketcap", pairing)
            value = quantity / float(price)
            return value

# FUNCTION: pairingStr
# INPUT: quote - string
# OUTPUT: string
# DESCRIPTION: 
#   Simple wrapper used to create a pairing string. Used to make code cleaner, more readable.
def pairingStr(quote):
    if quote == "BTC":
        return "USDT-BTC"
    else: 
        return "BTC-" + quote


# FUNCTION: removeItemsByIndex
# INPUT: list_items - list to have items altered
#        list_index - list of indexes
# OUTPUT: altered list
# DESCRIPTION:
#   Helper to adaptively remove items from a list using a number of indexes sorted in ascending order.
def removeItemsByIndex(list_items, list_index):
    ticker = 0
    for value in list_index:
        list_items.pop(value - ticker)
        ticker+=1

    return list_items

# FUNCTION: reversePairings
# INPUT: pairings - list of strings "A-B"
# OUTPUT: same as input, but "B-A"
# DESCRIPTION:
#   Reverses pairing order quote<->base 
def reversePairings(pairing_list):
    return ["%s-%s" % (v[0],v[1]) for v in [z.split("-") for z in pairing_list] ]

# FUNCTION: splitList
# INPUT: listy - list to split
#        parts - int
# OUTPUT: [[L1], [L2], [Ln], [Ln+1], ...] where n >= 0 
# DESCRIPTION:
#   Splits a list into multiple lists in the intuitive ordering. Returns a list of lists.
def splitList(listy, parts):
    length = len(listy)
    return [listy[i * length // parts: (i+1) * length // parts]
                for i in range(parts)]

# FUNCTION: sumFAE
# INPUT: fae_list - [(asset, exchange, value), ...]
# OUTPUT: float
# DESCRIPTION:
#   Finds the Bitcoin value of each fae in the input list of length >= 0. It then sums these values 
#    and returns the sum of the list in terms of Bitcoin.
def sumFAE(fae_list):
    tally = 0
    for value in fae_list:
        btc_value = btcValue(value[0], value[2], value[1])
        tally += btc_value
    return tally

# FUNCTION: usdValue
# INPUT: quantity - float
#        asset    - string
#        price    - float (OPTIONAL) in USD
# OUTPUT: float
# DESCRIPTION:
#   Returns the USD value of a specific asset. If no price is given, it calls binance's
#    getPrice function and calculates the usd value.
def usdValue(asset, quantity, exchange=None,):
    if exchange:        
        pairing = pairingStr(asset)
        usd_price = ExchangeAPI.getPriceUSD(exchange, pairing)
        usd_value = quantity * float(usd_price)
    else:
        pairing = pairingStr(asset)
        usd_price = ExchangeAPI.getPriceUSD("coinmarketcap", pairing)
        usd_value = quantity * float(usd_price)
    return usd_value