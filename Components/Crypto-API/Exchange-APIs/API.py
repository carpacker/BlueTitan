# API.py
# Carson Packer
# DESCRIPTION:
#    Generic wrapper API implementation of cryptocurrency exchanges.

# External-Imports
import time

# Internal-Imports
import Bittrex
import Binance
import Cryptopia 
import Coinbase
import CoinMarketCap
import Gdax
import Kucoin
import Poloniex
from PrintLibrary import PrintLibrary


############################### Global Function Dictionaries ######################################
#   Each exchange has a dictionary of functions. There is a key for each generic call and it 
#    coincides with a function within the exchange's file.

binance =  {'getCurrencies' : Binance.getCurrencies,
            'getInfoPairing' : Binance.getInfoPairing,
            'getInfoPairings': Binance.getInfoPairings,
            'getPrice' : Binance.getPrice,
            'getOrderbook' : Binance.getOrderbook,
            'buyLimit' : Binance.buyLimit,
            'sellLimit' : Binance.sellLimit,
            'stopLoss' : Binance.stopLoss,
            'stopLossLimit' : Binance.stopLossLimit,
            'getOrder' : Binance.queryOrder,
            'cancelOrder' : Binance.cancelOrder,
            'getOpenOrders' : Binance.getOpenOrders,
            'getAllOrders' : Binance.getAllOrders,
            'getMyTrades' : Binance.getMyTrades,
            'checkDeposit' : Binance.checkDeposit,
            'getDeposit' : Binance.getDeposit,
            'getDepositHistory' : Binance.getDepositHistory,
            'getDepositHistoryAsset' : Binance.getDepositHistoryAsset,
            'getWithdrawalHistory' : Binance.getWithdrawalHistory,
            'getDepositAddress' : Binance.getDepositAddress,
            'getBalance' : Binance.getBalance,
            'getBalances' : Binance.getBalances,
            'withdraw' : Binance.withdraw,
            'getTrades' : Binance.getTrades,
            'getHistoricalTrades' : Binance.getHistoricalTrades,
            'getAggTrades' : Binance.getAggTrades,
            'getCandlestick' : Binance.getCandlestick,
            'get24hr' : Binance.get24hr,
            'getBookTicker' : Binance.getBookTicker,
            'getPriceUSD' : Binance.getPriceUSD,
           }

bittrex = { 'getCurrencies' : Bittrex.getCurrencies,
            'getInfoPairing' : Bittrex.getInfoPairing,
            'getInfoPairings' : Bittrex.getInfoPairings,
            'getMarkets' : Bittrex.getMarkets,
            'getPrice' : Bittrex.getTicker,
            'getOrderbook' : Bittrex.getOrderbookBoth,
            'getRecentHistory' : Bittrex.getMarketHistory,
            'buyLimit' : Bittrex.buyLimit,
            'sellLimit' : Bittrex.sellLimit,
            'getOrder' : Bittrex.getOrder,
            'cancelOrder' : Bittrex.cancelOrder,
            'getOpenOrders' : Bittrex.getOpenOrders,
            'getOrderHistory' : Bittrex.getOrderHistory,
            'getBalance' : Bittrex.getBalance,
            'getBalances' : Bittrex.getBalances,
            'getDepositAddress' : Bittrex.getDepositAddress,
            'getWithdrawalHistory' : Bittrex.getWithdrawalHistory,
            'checkDeposit' : Bittrex.checkDeposit,
            'getDeposit' : Bittrex.getDeposit,
            'getDepositHistory' : Bittrex.getDepositHistory,
            'getDepositHistoryAsset' : Bittrex.getDepositHistoryAsset,
            'withdraw' : Bittrex.withdraw,
            'getPriceUSD' : Bittrex.getPriceUSD,
            }

coinbase = {'getDepositWithdrawals' : Coinbase.getDepositWithdrawals}

coinmarketcap = {'getPrice' : CoinMarketCap.getPriceBTC,
                    'getPriceUSD' : CoinMarketCap.getPriceUSD}

cryptopia = {'getCurrencies' : Cryptopia.getCurrencies,
            'getTradePairs' : Cryptopia.getTradePairs,
            'getMarkets' : Cryptopia.getMarkets,
            'getMarket' : Cryptopia.getMarket,
            'getMarketHistory' : Cryptopia.getMarketHistory,
            'getOrderbook' : Cryptopia.getMarketOrders,
            'getMarketOrderGroups' : Cryptopia.getMarketOrderGroups,
            'getBalance' : Cryptopia.getBalance,
            'getDepositAddress' : Cryptopia.getDepositAddress,
            'getOpenOrders' : Cryptopia.getOpenOrders,
            'getTradeHistory' : Cryptopia.getTradeHistory,
            'getTransactions' : Cryptopia.getTransactions,
            'getDepositHistory' : Cryptopia.getDepositHistory,
            'getWithdrawalHistory' : Cryptopia.getWithdrawalHistory,
            'submitTrade' : Cryptopia.submitTrade,
            'buyLimit' : Cryptopia.buyLimit,
            'sellLimit' : Cryptopia.sellLimit,
            'cancelOrder' : Cryptopia.cancelTrade,
            'getOrder' : Cryptopia.getOrder,
            'withdraw' : Cryptopia.submitWithdraw,
            'getBalances' : Cryptopia.getBalances
             }

gdax = {}

hitbtc = {}

kucoin = {}

poloniex = {}

exchanges = {'binance' : binance,
             'bittrex' : bittrex,
             'coinmarketcap' : coinmarketcap,
             'cryptopia' : cryptopia,
             'gdax' : gdax,
             'kucoin' : kucoin,
             'poloniex' : poloniex
             } 

# CLASS: ExchangeAPI
# DESCRIPTION:
#   Container for all calls to the generic exchange API. Most functions are top level wrappers that
#    index into a given dictionary in order to access the desired function from the desired
#    exchange's specific implementation. In some cases, other actions need to be performed. The
#    only other thing each function does besides that is verify that the exchange is supported
#    for the given function.
class ExchangeAPI():

    ##################################### MARKET CALLS #############################################

    # FUNCTION: getCurrencies
    # INPUT: exchange - string
    # OUTPUT: dictionary
    # DESCRIPTION:
    #   Generic function call for getCurrencies. Outputs a list of currencies
    #    for each exchanges and relevant information for the currencies.
    def getCurrencies(exchange):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getCurrencies']
        result_dict = curr_func()
        return result_dict

    # FUNCTION: getInfoPairing
    # INPUT: exchange - string
    #        pairing  - string
    # OUTPUT: Dictionary
    # DESCRIPTION:
    #   Returns the relevant information for a given pairing on a given exchange.
    def getInfoPairing(exchange, pairing):
        supportedexchanges = ['binance', 'bittrex']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        pairing_u = unscramblePairing(exchange, pairing)
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getInfoPairing']
        result_dict = curr_func(pairing_u)
        return result_dict

    # FUNCTION: getInfoPairings
    # INPUT: exchange - string
    #        pairings - [string, ...]
    # OUTPUT: Dictionary
    # DESCRIPTION:
    #   Generic function call to get the relevant information for a list of pairings on a given
    #    exchange. 
    def getInfoPairings(exchange, pairings):
        supportedexchanges = ['binance', 'bittrex']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getInfoPairings']
        result_dict = curr_func(pairings)
        return result_dict

    # FUNCTION: getMarkets
    # INPUT: exchange - string
    # OUTPUT: Dictionary
    # DESCRIPTION:
    #   Outputs a list of currently traded markets. Each element is a dictionary containing
    #    relevant information.
    def getMarkets():
        supportedexchanges = ['binance', 'bittrex']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getMarkets']
        result_dict = curr_func()
        return result_dict

    # FUNCTION: getPrice
    # INPUT: exchange - string
    #        pairing  - string
    # OUTPUT: float
    #   Generic function call for getPrice. Outputs the last price for a given
    #    market pairing. Return is in terms of bitcoin.
    def getPrice(exchange, pairing):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia', 'coinmarketcap', 'poloniex']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getPrice']
        pairing_u = unscramblePairing(exchange, pairing)
        result_dict = curr_func(pairing_u)
        return result_dict

    # FUNCTION: getPriceBTC
    # INPUT: exchange - string
    #        pairing  - string
    # OUTPUT: float
    #   Generic function call for getPrice. Outputs the last price for a given
    #    market pairing in terms of BTC.
    def getPriceBTC(exchange, pairing):
        supportedexchanges = ['coinmarketcap', 'binance', 'bittrex']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getPriceBTC']
        pairing_u = unscramblePairing(exchange, pairing)
        result_dict = curr_func(pairing_u)
        return result_dict

    # FUNCTION: getPriceUSD
    # INPUT: exchange - string
    #        pairing  - string
    # OUTPUT: float
    #   Generic function call for getPrice. Outputs the last price for a given
    #    market pairing in terms of USD. 
    def getPriceUSD(exchange, pairing):
        supportedexchanges = ['coinmarketcap']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getPriceUSD']
        pairing_u = unscramblePairing(exchange, pairing)
        result_dict = curr_func(pairing_u)
        return result_dict

    # FUNCTION: getOrderbook
    # INPUT: exchange - string
    #        pairing  - string
    # OUTPUT: dictionary
    #   Generic function call for getOrderbook. Outputs a list of tuples which
    #    consist of a price and quantity for an ask or a bid.
    def getOrderbook(exchange, pairing):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        curr_ex = exchanges[exchange]
        pairing_u = unscramblePairing(exchange, pairing)
        curr_func = curr_ex['getOrderbook']
        result_dict = curr_func(pairing_u)
        return result_dict

    # FUNCTION: getRecentTrades
    # INPUT: exchange - string
    #        pairing  - string
    #        limit    - int 
    # OUTPUT: dictionary
    # DESCRIPTION:
    #   Generic function call that outputs a list of the most recent trades for
    #    a given market symbol.
    def getRecentTrades(exchange, pairing):
        supportedexchanges = ['binance', 'bittrex']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        curr_ex = exchanges[exchange]
        pairing_u = unscramblePairing(exchange, pairing)
        curr_func = curr_ex['getRecentTrades']
        result_json = curr_func(pairing_u)
        return result_json

    #################################### ACCOUNT CALLS ############################################

    # FUNCTION: getBalance
    # INPUT: exchange - string
    #        asset    - string
    # OUTPUT: Dictionary
    # DESCRIPTION: 
    #   Generic function call for getBalance. Returns the balance for
    #    specific asset on an exchange.
    def getBalance(exchange, asset):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getBalance']
        result_dict = curr_func(asset)
        return result_dict

    # FUNCTION: getBalances
    # INPUT: exchange - string
    # OUTPUT: Dictionary
    # DESCRIPTION: 
    #   Generic function call for getBalances. Returns the balances of all
    #    assets on a specific exchange.
    def getBalances(exchange):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getBalances']
        result_dict = curr_func()
        return result_dict

    # FUNCTION: checkDeposit
    # INPUT: exchange   - string
    #        assets     - string
    #        quantity   - float
    #        start_time - int
    # OUTPUT: dictionary
    # DESCRIPTION:
    #   Used to check if a deposit has arrived by looking through the deposit history
    #    and finding a match given input parameters. This function is nearly identical
    #    to getDeposit, with the exception of it returning True instead of the deposit.
    #    A difference is that it has a start_time parameter for efficiency purposes.
    def checkDeposit(exchange, asset, quantity, start_time=0):
        supportedexchanges = ['binance', 'bittrex']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['checkDeposit']
        result_dict = curr_func(asset, quantity, start_time)
        return result_dict

    # FUNCTION: getDeposit
    # INPUT: exchange   - string
    #        assets     - string
    #        quantity   - float
    # OUTPUT: Dictionary
    # DESCRIPTION:
    #   Retrieve a single deposit given input parameters to detect it. Returns False if
    #    the deposit could not be found.
    def getDeposit(exchange, asset, quantity):
        supportedexchanges = ['binance', 'bittrex']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getDeposit']
        result_dict = curr_func(asset, quantity)
        return result_dict

    # FUNCTION: getDepositAddress
    # INPUT: exchange - string
    #        asset    - string
    # OUTPUT: dictionary
    # DESCRIPTION:
    #   Generic function call for getDepositAddress. Returns a dictionary which
    #    contains the deposit address of the queried asset.
    def getDepositAddress(exchange, asset):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getDepositAddress']
        result_json = curr_func(asset)
        return result_json

    # FUNCTION: getDepositHistory
    # INPUT: exchange - string
    #        period   - TODO
    #        max      - TODO [Maximum number of deposits to return]
    # OUTPUT: dictionary
    # DESCRIPTION: 
    #   Generic function call for getDepositHistory. Retrieves the withdrawal
    #    history of either a single currency or all currencies for a given period 
    #    of time.
    def getDepositHistory(exchange):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        symbol_u = unscramblePairing(exchange, symbol)
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getDepositHistory']
        result_dict = curr_func()
        return result_dict

    # FUNCTION: getDepositHistoryAsset
    # INPUT: exchange   - string
    #        assets     - string
    #        start_time - int
    #        max        - TODO [Maximum number of deposits to return]
    # OUTPUT: dictionary
    # DESCRIPTION:
    #   Returns the deposit history from a given exchange for a given asset.
    def getDepositHistoryAsset(exchange, asset, start_time):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getDepositHistoryAsset']
        result_dict = curr_func(asset)
        return result_dict

    # FUNCTION: getTradeHistory
    # INPUT: exchange - string
    #        quantity - int [OPTIONAL] (number of trades to return) 
    # OUTPUT: dictionary
    # DESCRIPTION
    #   Returns the trade history for an account on the given exchange for all 
    #    assets.
    def getTradeHistory(exchange, quantity=100):
        pass

    # FUNCTION: getTradeHistoryAsset
    # INPUT: exchange - string
    #        asset    - string
    #        quantity - int [OPTIONAL] (number of trades to return) 
    # OUTPUT: dictionary
    # DESCRIPTION:
    #   Returns the trade history for an account on the given exchange for
    #    a given asset.
    def getTradeHistoryAsset(exchange, asset, quantity=100):
        pass

    # FUNCTION: getWithdraw
    # INPUT: TODO
    # OUTPUT: TODO
    # DESCRIPTION:
    #   retrieves a withdraw record from a given exchange.
    def getWithdraw():
        pass

    # FUNCTION: getWithdrawalHistory
    # INPUT: exchange - string
    #        asset    - string
    #        period   - TODO
    # OUTPUT: dictionary
    # DESCRIPTION: 
    #   Generic function call for getWithdrawalHistory. Retrieves the withdrawal
    #    history of either a single currency or all currencies for a given period 
    #    of time.
    def getWithdrawalHistory():
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        symbol_u = unscramblePairing(exchange, symbol)
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getWithdrawalHistory']
        # Inputs: pairing, quantity, rate [kwarg1, kwarg2, ..., kwargN]
        result_dict = curr_func(symbol_u)
        return result_dict

    def getWithdrawalHistoryAsset():
        pass

    # FUNCTION: withdraw
    # INPUT: exchange - string
    #        asset    - string
    #        address  - string
    # OUTPUT: dictionary
    # DESCRIPTION: 
    #   Generic function call for withdraw. Submits a withdraw request to
    #    an exchange, which then sends said currency to the passed in address.
    #    Returns a dictionary with information to track a withdraw.
    def withdraw(exchange, asset, quantity, address, tag=""):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['withdraw']
        result_json = curr_func(asset, quantity, address, tag)
        return result_json

    ##################################### ORDER CALLS #############################################
    # FUNCTION: buyLimit
    # INPUT: TODO
    # OUTPUT: dictionary
    # DESCRIPTION:
    #   Generic wrapper for a buy-limit call. TODO, describe what buy limit is
    def buyLimit(exchange, symbol, quantity, rate):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        symbol_u = unscramblePairing(exchange, symbol)
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['buyLimit']
        result_dict = curr_func(symbol_u, quantity, rate)
        return result_dict

    # FUNCTION: sellLimit
    # INPUTS: exchange(string), symbol(string), quantity(float), rate(float)
    def sellLimit(exchange, symbol, quantity, rate):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        symbol_u = unscramblePairing(exchange, symbol) 
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['sellLimit']
        # Inputs: symbol, quantity, rate [kwarg1, kwarg2, ..., kwargN] 
        result_dict = curr_func(symbol_u, quantity, rate)
        return result_dict

    # TODO NOT IMPLEMENTED
    def stopLoss(exchange, symbol, quantity, rate):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        symbol_u = unscramblePairing(exchange, symbol)
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['stopLoss']
        # Inputs: order_id [kwarg1, kwarg2, ..., kwargN] 
        result_dict = curr_func(symbol_u, side, quantity, rate)
        return result_dict

    # TODO NOT IMPLEMENTED
    def stopLossLimit(exchange, side, symbol, quantity, rate_one, rate_two):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        symbol_u_u = unscramblePairing(exchange, symbol)
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['stopLossLimit']
        # Inputs: order_id [kwarg1, kwarg2, ..., kwargN] 
        result_dict = curr_func(symbol_u, side, quantity, rate_one, rate_two)
        return result_dict

    def getOrder(exchange, order_id, pairing):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        pairing_u = unscramblePairing(exchange, pairing)
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getOrder']
        # Inputs: order_id [kwarg1, kwarg2, ..., kwargN] 
        result_dict = curr_func(pairing_u, order_id)
        return result_dict

    # TODO NOT IMPLEMENTED
    def getOpenOrders(exchange, symbol):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        symbol_u = unscramblePairing(exchange, symbol)
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getOpenOrders']
        # Inputs: order_id [kwarg1, kwarg2, ..., kwargN] 
        result_dict = curr_func(symbol_u)
        return result_dict

    # TODO NOT IMPLEMENTED
    def getClosedOrders(exchange, symbol):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        symbol_u = unscramblePairing(exchange, symbol)
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getClosedOrders']
        # Inputs: order_id [kwarg1, kwarg2, ..., kwargN] 
        result_dict = curr_func(pairing_u, order_id)
        return result_dict

    # FUNCTION: getAllOrdersPairing
    # INPUT: exchange - string
    #        symbol   - string
    # OUTPUT: dictionary
    # DESCRIPTION:
    #   Returns all orders on a given exchange (open and closed) for a given pairing.
    # TODO NOT IMPLEMENTED
    def getAllOrdersPairing(exchange, symbol):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        symbol_u = unscramblePairing(exchange, symbol)
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getAllOrders']
        result_dict = curr_func(symbol_u)
        return result_dict

    # FUNCTION: getAllOrdersExchange
    # INPUT: exchange - string
    # OUTPUT: dictionary
    # DESCRIPTION:
    #   Returns all orders (open and closed, for each pairing) for a given exchange.
    # TODO NOT IMPLEMENTED
    def getAllOrders(exchange):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        symbol_u = unscramblePairing(exchange, symbol)
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getAllOrders']
        result_dict = curr_func(symbol_u)
        return result_dict

    # FUNCTION: getAllOrders
    # INPUT: N/A
    # OUTPUT: dictionary
    # DESCRIPTION:
    #   Returns all orders (open and closed, for each pairing) for all supportedexchanges.
    # TODO NOT IMPLEMENTED
    def getAllOrders():
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        symbol_u = unscramblePairing(exchange, symbol)
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['getAllOrders']
        result_dict = curr_func(symbol_u)
        return result_dict

   # FUNCTION: cancelOrder
   # INPUT: exchange - string
   #        order_id - string
   #        symbol   - string
   # OUTPUT: dictionary
   # DESCRIPTION:
   #    Cancels an open order on a given exchange using the order id. Symbol is not required for 
   #     all exchanges, but for the purpose of standardization it is a required parameter.
    def cancelOrder(exchange, order_id, symbol):
        supportedexchanges = ['binance', 'bittrex', 'cryptopia']
        if verifySupported(exchange, supportedexchanges) == False:
            return -1
        symbol_u = unscramblePairing(exchange, symbol)
        curr_ex = exchanges[exchange]
        curr_func = curr_ex['cancelOrder']
        result_dict = curr_func(order_id, symbol_u)
        return result_dict

    # FUNCTION: buyLimitAbs
    # INPUT: exchange - string
    #        symbol   - string
    #        quantity - float
    #        rate     - float
    #        distance - float
    # OUTPUT:
    # DESCRIPTION:
    #   Same as buyLimit, but ensures that the entire original quantity is filled.
    def buyLimitAbs(exchange, symbol, quantity, rate, distance):
        symbol = unscramblePairing(exchange, symbol)
        buy_dict = ensureOriginalQuant(exchange, symbol, quantity, rate, "buyLimit", distance)
        return buy_dict

    # FUNCTION: sellLimitAbs
    # INPUT: exchange - string
    
    # Future make these one function
    def sellLimitAbs(exchange, symbol, quantity, rate, distance):
        symbol = unscramblePairing(exchange, symbol)
        sell_dict = ensureOriginalQuant(exchange, symbol, quantity, rate, "sellLimit", -distance)
        return sell_dict

# HELPER: ensureOriginalQuant
# INPUT: exchange     - string
#        symbol       - string
#        quantity     - float
#        func_name    - string
#        distance     - int
#        alloted_time - int [default 60] in terms of SECONDS or string ['MAX']
# OUTPUT: dictionary
# DESCRIPTION:
#   Ensures that an order function performs an operation over a given quantity. Let's say one wants to buy 1 Ethereum to
#    perform an operation. If you perform a buy and sell and it doesn't fill, you now don't have the 1 Ethereum that was 
#    required for your operation, prompting an error. This function performs the error handling necessary to make sure
#    that an order is filled or partially filled. There are inputs that allow for flexibility in said error handling.

# * - TODO, currently only works for buyLimit, sellLimit. Need to adapt func arguments 
#           to  make it work for functions that require new parameters
def ensureOriginalQuant(exchange, symbol, quantity, rate, func_name, distance, allotted_time=60):

    curr_ex = exchanges[exchange]
    func = exchanges[exchange][func_name]
    cancel_func = exchanges[exchange]["cancelOrder"]

    # TEMPORARY FIX
    symbol_stand = standardizePairing(exchange, symbol)


    # FUNCTION: averageWeight
    # DESCRIPTION:
    # * TODO - Move this to helpers
    def averageWeight(prices, weights):
        if sum(weights) != 0:
            return sum(x * y  for x, y in zip(prices, weights)) / sum(weights)
        else:
            return 0

    # FUNCTION: adaptPrice
    # INPUT: price    - float
    #        distance - float
    #        percent  - float
    # OUTPUT: float
    # DESCRIPTION:
    #   Returns a new price adapted to the given distance from the original.
    # * TODO - add an example
    def adaptPrice(price, distance, percent):
        distance = distance * percent
        price = price * (distance / 100) + price
        return price

    # FUNCTION: retryUnsuccessfulOrder
    # INPUT: func     - function
    #        symbol   - string
    #        quantity - float
    #        rate     - float
    # OUTPUT: order dictionary
    # DESCRIPTION:
    #   Retry the order if unsuccessful. In a normal scenario, it should only happen once or twice, when the site is down for a bit, 
    #    this would handle that case. If the site goes down for more than ~30seconds, it will be handled later.
    def retryUnsuccessfulOrder(func, symbol, quantity, rate):
        return_dict = func(symbol, quantity, rate)

        ticker = 0
        while return_dict["success"] == False:
            if return_dict["error"] == "micro_order" or return_dict["error"] == "min_notional":
                return return_dict
            time.sleep(1)
            PrintLibrary.displayDictionary(return_dict, str(ticker))
            return_dict = func(symbol, quantity, rate)

            # After ~30 seconds of unsuccessful orders, return denoting some error with exchange or connection.
            if ticker == 30:
                # Error message might be edited for a future component, this is a good placeholder
                error_message = "NoConnection-ExchangeDown"
                return_dict = {"error" : error_message}
                return return_dict

        # If we were able to break out with a successful order, fill the error slot with no error [""]
        return_dict["error"] = ""
        return return_dict

    # FUNCTION: retryUnfilledOrder
    # INPUT: exchange           - string
    #        symbol             - string
    #        remaining_quantity - float
    #        return_dict        - dictionary
    #        func_name          - name of the order function [currently only supports 'buyLimit' and 'sellLimit']
    # OUTPUT: order dictionary
    # DESCRIPTION:
    #   Attempts to fill either a partially filled or unfilled order again. This includes cancelling the old order.
    def retryUnfilledOrder(exchange, symbol, remaining_quantity, rate, return_dict, func_name):
        func = exchanges[exchange][func_name]
        get_func = exchanges[exchange]["getOrder"]
        cancel_dict = cancel_func(return_dict["order_id"], symbol)
        if cancel_dict["error"] == "order_closed":
            return_dict = get_func(symbol,cancel_dict["order_id"])
            print("Error order closed", return_dict)
            return return_dict

        order_dict = get_func(symbol, cancel_dict["order_id"])
        print("RetryUnfilled: Order check: ", order_dict)
        if order_dict["remaining_quantity"] != remaining_quantity:
            print("Remaining Quantity Original:", remaining_quantity)
            remaining_quantity = order_dict["remaining_quantity"]
            print(" - REMAINING DONT MATCH UP", remaining_quantity)
            return_dict = retryUnsuccessfulOrder(func, symbol, remaining_quantity, rate)
            return return_dict

        time.sleep(2)
        return_dict = retryUnsuccessfulOrder(func, symbol, remaining_quantity, rate)
        print("RetryUnfilled, finished: ", return_dict)
        return return_dict

    # 1. Vet initial price against real time price
    # Potentially change curr_ex to a string
    price_symbol = ExchangeAPI.getPrice(exchange, symbol_stand)

    # Possibly use a helper here instead
    distance_rate = abs(((rate - price_symbol) / rate))

    # If the change is greater than ~10% [currently arbitrary]
    if distance_rate > .1:
        # return an error dict
        error_message = "PriceDifferenceTooHigh"
        return_dict = {"error" : error_message}
        return return_dict

    # 2. Attempt initial order, if successful move on
    return_dict = retryUnsuccessfulOrder(func, symbol, quantity, rate)
    if return_dict["error"] != "":
        if return_dict["error"] == "micro_order":
            return return_dict
        return return_dict

    # 3. Attempt to fill original quantity at original price. `
    # TODO - Future, add an efficiency check if its 0 too many times
    # TODO - Future, consider adding failure tracking
    ticker = 0
    original_quantity = quantity
    filled_quantity = return_dict["filled_quantity"]
    print("SYMBOL BEFORE FILL LOOP", symbnol)
    while filled_quantity < (original_quantity * .98):
        price = []
        #   1. Try again a few times, until 25% of alotted time
        if ticker < (allotted_time * .25):
            # Attempt unfilled order here
            remaining_quantity = original_quantity - filled_quantity
            print("before", remaining_quantity)
            notional_dict = ExchangeAPI.getInfoPairing(exchange, symbol)
            step_size = notional_dict["step_size"]
            qty_trim = remaining_quantity % step_size
            remaining_quantity = remaining_quantity - qty_trim
            print("after", remaining_quantity)
            return_dict = retryUnfilledOrder(exchange, symbol, remaining_quantity, rate, return_dict, func_name)
            newly_filled = return_dict["filled_quantity"] 
            filled_quantity = filled_quantity + newly_filled
            PrintLibrary.displayVariables((original_quantity, newly_filled, filled_quantity))
            ticker+=1
        else:
            break

    prices = []
    weights = []
    print(return_dict)
    while filled_quantity < (original_quantity * .98):

        percent = ticker / allotted_time
        rate_adapt = adaptPrice(rate, distance, percent)

        remaining_quantity = original_quantity - filled_quantity
        return_dict = retryUnfilledOrder(exchange, symbol, remaining_quantity, rate_adapt, return_dict, func_name)
        newly_filled = return_dict["filled_quantity"] 
        filled_quantity = filled_quantity + newly_filled
        PrintLibrary.displayVariables((original_quantity, newly_filled, filled_quantity))

        weight = newly_filled / original_quantity
        weights.append(weight)
        prices.append(rate_adapt)

        ticker += 1

        #  3. When we run out of time, build return dictionary
        if ticker == allotted_time:
            average_rate = averageWeight(prices, weights)
            return_dict["filled_quantity"] = filled_quantity
            return_dict["average_rate"] = average_rate
            return_dict["distance_rate"] = adapt_rate
            return_dict["original_rate"] = rate
            return return_dict

    return return_dict

# FUNCTION: standardizePairing
# INPUT: exchange - string
#        pairing  - string
# OUTPUT: string
# DESCRIPTION:
#   Standardizes a pairing to the required format per given exchange.
def standardizePairing(exchange, pairing):
    if exchange == 'binance':
        # TODO: make this more robust
        formatted_pairing = pairing[3:7] + "-" + pairing[0:3]
        return formatted_pairing
    elif exchange == 'bittrex':
        return pairing
    else:
        print("ERROR :: standardizePairing :: exchange not supported")
        return -1

# FUNCTION: unscramblePairing
# INPUT: pairing - string
# OUTPUT: pairing formatted properly for genericAPI pass in
# DEFINITIONs#  Takes any input string of standard format and converts it to appropiate exchange's format
#   BASE ASSET dash QUOTE ASSET' --> 'BTC-LTC' 
def unscramblePairing(exchange, pairing):
    base,quote = pairing.split("-")
    if exchange == 'binance':
        formatted_pairing = quote + base
        return formatted_pairing
    elif exchange == 'bittrex':
        return pairing
    elif exchange == 'cryptopia':
        formatted_pairing = quote + '_' + base
        return formatted_pairing
    elif exchange == 'coinmarketcap':
        formatted_pairing = quote
        return formatted_pairing
    elif exchange == 'poloniex':
        return -1
    elif exchange == 'kucoin':
        return -1
    elif exchange == 'hitbtc':
        return -1
    elif exchange == 'gdax':
        return -1
    else:
        print("ERROR :: unscramblePairing :: exchange not supported")
        return -1

# FUNCTION: verifySupported
# INPUT: exchange           - string
#        supportedexchanges - [string, ...]
# OUTPUT: boolean
# DESCRIPTION:
#   Used to verify whether an exchange is in the list of supported exchanges. Runtime is O(n) where n
#    is the length of supportedexchanges. Since supportedexchanges should be pretty small, this is neglible
#    for now. In the future, a more runtime friendly check may be required.
def verifySupported(exchange, supportedexchanges):
    for s_exchange in supportedexchanges:
        if s_exchange == exchange:
            return True

    print("ERROR :: exchange not supported")
    return False
