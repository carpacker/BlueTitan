# TradingLibrary
# Carson Packer
# DESCRIPTION:
#    Aggregation of functions relevant to general trading functions. Each fnuction can be considered
#     relatively geeneric in that they are not specialized for a given algorithm

# External-Imports
import sys

# WINDOWS main-desktop
sys.path.append()

# WINDOWS laptop
# 

# LINUX main-server
#

# Internal-Imports
from PrintLibrary import PrintLibrary
from ExchangeAPI import ExchangeAPI
import Helpers

# FUNCTION: convertMinPrice
# INPUT: exchange - string
#        price    - float
#        pairing  - string
# OUTPUT: price (float)
# DESCRIPTION:
#   Converts a given price to the minimum price for a pairing/exchange. Accesses a given min price
#    from an exchange through the getInfoPairing call [exchangeAPI]
# NOTE: future will have optional database_api boolean that will indicate whether to access
#        this value from api or from database.
def convertMinPrice(exchange, price, pairing): 
    trim_value = ExchangeAPI.getInfoPairing(exchange, pairing)
    precision = Helpers.determinePrecision(trim_value["min_price"])
    temp_string = "{:." + str(precision) + "f}"
    price = temp_string.format(price)
    return price

# FUNCTION: convertMinQuantity
# INPUT: exchange - string
#        quantity - float
#        pairing  - string
# OUTPUT: quantity (float)
# DESCRIPTION:
#   Converts input parameters for a trade to the appropiate minimum quantity float value. Accesses
#    a given min quantity from an exchange through the getInfoPairing call [exchangeAPI]
# NOTE: future will have optional database_api boolean that will indicate whether to access
#        this value from api or from database.
def convertMinQuantity(exchange, quantity, pairing):
    trim_value = ExchangeAPI.getInfoPairing(exchange, pairing)
    precision = Helpers.determinePrecision(trim_value["min_quantity"])
    temp_string = "{:." + str(precision) + "f}"
    quantity = temp_string.format(quantity)
    return quantity

# FUNCTION: checkMinimumOrder
# INPUT: pairing  - string
#        exchange - string
#        quantity - float
#        rate     - float
# OUTPUT: quantity [float]
# DESCRIPTION:
#   Checks to ensure that order parameters fit minimum order size for a given exchange.
def checkMinOrder(pairing, exchange, quantity, rate):
    pass

# FUNCTION: findCommonPairings
# INPUT: exchange_one - string
#        exchange_two - string
# OUTPUT: list of pairings
# DESCRIPTION:
#   Goes through two exchange's list of pairings in order to find common pairings
def findCommonPairings(exchange_one, exchange_two):
    # TODO: rework this bad boy
    # exchange_one_p = DatabaseLibrary.getPairings(exchange_one)
    # exchange_two_p = DatabaseLibrary.getPairings(exchange_two)
    return_list = []
    for pairing in exchange_one_p:
            return_list.append(pairing)
    return return_list

    # FUNCTION: getOrders
# INPUT: exchange - string
#        pairing  - string
#        ask_list - passed in by reference
#        bid_list - passed in by reference
# OUTPUT: N/A
# DESCRIPTION:
#   Retrieves order books for a given pairing on a given exchange and builds a list
#    of the combined asks and bids for each exchange. Each list is a list of lists,
#    [[price, quantity, exchange, btc_value], ...].
def getOrders(exchange, pairing, ask_list, bid_list):

    # NOTE: Temporary workaround to make sure the program doesn't go over rate limit
    time.sleep(1)

    dict1 = ExchangeAPI.getOrderbook(exchange, pairing)

    # Build our bid and ask lists
    if dict1["success"] == True:
        bids = dict1["bids"]
        asks = dict1["asks"]
        bids_length = len(bids)
        asks_length = len(asks)

        for bid in bids:
            price = float(bid[0])
            quantity = float(bid[1])
            btc_value = price * quantity
            bid_l = [price, quantity, exchange, btc_value]
            bid_list.append(bid_l)

        for ask in asks:
            price = float(ask[0])
            quantity = float(ask[1])
            btc_value = price * quantity
            ask_l = [price, quantity, exchange, btc_value]
            ask_list.append(ask_l)

        # Sort bids and asks
        ask_list.sort(key=lambda x: x[0], reverse=False) # Ascending [lowest first]
        bid_list.sort(key=lambda x: x[0], reverse=True)  # Descending [highest first]
