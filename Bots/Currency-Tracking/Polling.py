''' 
                                          Polling.py
Description goes here


Notes:
    -Need individual database functions
    -Modify evaluate pairing to store each point in time
    -Call less frequently

'''



#                                           Imports

import sys
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Crypto-API/Exchange_APIs')
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Crypto-API/Main')
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Database-RD')
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Arbitrage')

# External Imports
from copy import deepcopy
import math 
import time
import threading

# Internal Imports
import API
from API import ExchangeAPI
import Helpers
from DatabaseLibrary import DatabaseLibrary
from DatabaseManager import ArbitrageDatabase

# CLASS: Polling
class Polling(object):

    class_exchanges = ('bittrex', 'binance')
    class_pairing_list = ['BTC-KMD', 'BTC-OMG', 'BTC-BAT', 'BTC-LTC', 'BTC-XMR', 'BTC-DASH', 'BTC-NAV', 'BTC-XRP', 'BTC-ETH',
                            'BTC-XLM', 'BTC-XVG', 'BTC-PIVX', 'BTC-STEEM', 'BTC-LSK', 'BTC-WAVES', 'BTC-ETC', 'BTC-STRAT',
                            'BTC-XZC', 'BTC-NEO', 'BTC-ZEC', 'BTC-ARK', 'BTC-WINGS', 'BTC-RLC', 'BTC-LUN', 'BTC-BNT', 'BTC-SNT',
                            'BTC-MCO', 'BTC-FUN', 'BTC-STORJ', 'BTC-ADX', 'BTC-QTUM', 'BTC-DNT', 'BTC-ADA', 'BTC-MANA', 'BTC-SALT', 
                            'BTC-RCN', 'BTC-VIB', 'BTC-POWR', 'BTC-BTG', 'BTC-ENG']

    class_assets = ['BTC', 'ARK', 'KMD', 'LTC', 'DASH', 'XMR', 'NAV', 'XRP', 'ETH', 'XLM', 'XVG', 'PIVX', 'STEEM',' LSK',' WAVES',
                    'ETC', 'STRAT','XZC','NEO','ZEC','WINGS','RLC','LUN','BAT','BNT','SNT','MCO','FUN','STORJ','ADX','OMG','QTUM','DNT',
                    'ADA','MANA','SALT','RCN','VIB','POWR','BTG','ENG']

    def __init__(self, clean=True):

        # Grab arguments and update global variables
        exchanges = exchanges = LowLiquidityArbitrage.class_exchanges # tuple
        pairing_list = LowLiquidityArbitrage.class_pairing_list       # list
        assets = LowLiquidityArbitrage.class_assets

    def Polling(self):
        exchanges = LowLiquidityArbitrage.class_exchanges             # tuple
        pairing_list = LowLiquidityArbitrage.class_pairing_list       # list
        ticker = 0
        while 1:

            # 1. Record polling information

            # Grab data on each pairing in pairing list using coinmarketcap,
            #  then store data for each in database.

            # price, volume, ...

            # - Check runtime on above for purpose of sleeps

            # 2. Record 'attempted' arbitrage information
            if ticker == 5:
                ticker = 0
                for pairing in pairing_list:
                    print("Polling Loop # ", ticker, " : ", pairing)
                    time.sleep(2)

                    base, quote = pairing.split("-")

                    order_list = [] 
                    thread_list = [] 
                    thread_count = 0
                    for ex in exchanges:
                        order_list.append( (ex, [], []) )
                        t = threading.Thread(target=self.getOrders,args=(ex, pairing, order_list[thread_count][1], order_list[thread_count][2]))
                        thread_count += 1
                        thread_list.append(t)
                        t.start()
                    [t.join() for t in thread_list]
                    bidask_one = self.evaluatePairing(order_list, pairing, 0)
                    bidask_two = self.evaluatePairing(order_list, pairing, 1)

                    # 1. Decide which one is better to look at
                    # 2. Store evaluation result

            ticker += 1


    def getOrders(self, exchange, pairing, ask_list, bid_list):
        time.sleep(1)

        dict1 = ExchangeAPI.getOrderbook(exchange, pairing)
        if dict1["success"]:
            bids = dict1["bids"]
            asks = dict1["asks"]
            bids_length = len(bids)
            asks_length = len(asks)
            for bid in bids:
                price = float(bid[0])
                quantity = float(bid[1])
                bid_total = price * quantity
                bid_l = [price, quantity, exchange, bid_total]
                bid_list.append(bid_l)
            for ask in asks:
                price = float(ask[0])
                quantity = float(ask[1])
                ask_total = price * quantity
                ask_l = [price, quantity, exchange, ask_total]
                ask_list.append(ask_l)

            ask_list.sort(key=lambda x: x[0], reverse=False)
            bid_list.sort(key=lambda x: x[0], reverse=True) # descending

        return -1


    def evaluatePairing(self, order_list, pairing, buy_num):
        base, quote = pairing.split("-")
        ask_num = int(not(buy_num))
        buy_exchange = order_list[buy_num][0]
        buy_asks = order_list[buy_num][1]
        buy_rate = buy_asks[0][0]
        sell_exchange = order_list[ask_num][0]
        sell_bids = order_list[ask_num][2]
        sell_rate = sell_bids[0][0]

        pr = Helpers.calculatePR(sell_rate, buy_rate)

        breakeven_price = buy_asks[0][0]

        bid_range = list(sell_bids)
        ask_range = list(buy_asks)
        
        for bid in sell_bids:
            if bid[0] > breakeven_price:
                bid_range.append(bid)

        bid_len = len(bid_range)
        ask_len = len(ask_range)

        quantity = 0
        buy_price = 0
        total_sale = 0
        ask_i = 0
        bid_i = 0
        residue = (0, 0) # price and quantity residue 
        avg_price_buy = 0
        avg_price_sell = 0
        bid_fee = Helpers.getFee(buy_exchange)
        ask_fee = Helpers.getFee(sell_exchange)

        sell_price_limit = 9999999
        buy_price_limit = -1

        while 1:
            if ask_i >= ask_len or bid_i >= bid_len:
                break

            ask_p = ask_range[ask_i][0]
            bid_p = bid_range[bid_i][0]
            ask_q = ask_range[ask_i][1]
            bid_q = bid_range[bid_i][1]

            if (ask_p + (ask_p * ask_fee)) >= (bid_p - (bid_p * bid_fee)):
                break

            sell_price_limit = bid_p
            buy_price_limit = ask_p

            work_quant = min(ask_q, bid_q)
            next_quantity = quantity + work_quant
            p = work_quant * ask_p
            next_price = buy_price + p

            sale_quant = work_quant * bid_p
            next_total_sale = total_sale + sale_quant

            curr_funds_base = balance_BTC - buy_price
            sell_quant_possible = balance_ALT - quantity
            buy_quant_possible = curr_funds_base / ask_p
            limit_quant = min(work_quant, buy_quant_possible, sell_quant_possible)
            if limit_quant != work_quant:
                p = limit_quant * ask_p
                buy_price += p
                quantity += limit_quant
                sale_quant = limit_quant * bid_p
                total_sale += sale_quant
                sell_price_limit =  bid_p
                buy_price_limit = ask_p
                break
            else:
                buy_price = next_price
                quantity = next_quantity
                total_sale = next_total_sale
                if ask_q >= bid_q:
                    bid_i += 1
                if bid_q >= ask_q:
                    ask_i += 1

        storePolling()
        return 0

    def storePolling():
        pass

    def storeMarketData():
        pass

    def storePollingFailures():
        pass

if __name__ == "__main__":
    Polling().Arbitrage()