import sys

from API import ExchangeAPI

# Mass autobuy script
# Purpose:
#   Iterate through a list of cryptocurrencies with defined attributes, give them an aggregate
#   score based on these attributes, identify coins which are 'to be bought' and then go through
#   the API of whatever sites are necessary to buy them.


# CLASS: SpreadsheetParser
class SpreadsheetParser():

    spreadsheet_dict = {}

    def processCSV():
        currency_list = []

        # 1. Access the file
        # 2. for each line
        #   - Store values in temporary tuple
        #   - Append tuple to running list
        #   - Store tuple in database

        return currency_list

    # OUTPUT: DICTIONARY
    #     [Asset :  (PRICE, VOLUME, MARKETS, TIMELINE, SOCIAL_NEWS, WEBSITE,
    #                   SOURCE_CODE, PRICE_MOV, MINEABLE, WHITEPAPER)]  
    #     [ETH   :   (8, 10, 8, ...)] --> 8
    # LENGTH = (1 + NUMBER OF VARIABLES)

# CLASS: CoinRanker
class CoinRanker():

    # FUNCTION: rankCoins
    # INPUT: TODO
    # OUTPUT: [(asset, value), ...]
    # DESCRIPTION:
    #   Takes in an input dictionary from the CSV processing stage. Acts as top level
    #    function for inner logic.
    def rankCoins(coin_dictionary, supportedcoins):
        # List will become [(asset, value), (asset, value), ...]
        coin_list = []
        for coin in supportedcoins:
            tuple_f = coin_dictionary[coin]
            coin_value = assignValue(tuple_f)
            intemediary_tuple = (coin, coin_value)
            coin_list.append(intemediary_tuple)

        return coin_list

    # FUNCTION: assignValue
    # INPUT: tuple
    # DESCRIPTION:
    #   Takes an input coin tuple and assigns an aggregate score based on its values.
    def assignValue(coin_tuple):

        # Ticker system is used to aid in determining value
        ticker = 0
        for category in coin_tuple:
            # First check the special case
            # - Potentially assign to deviate list

            # Otherwise,
            #   Do something to figure out the betsize
            #    Average each value with a weight towards some values(maybe some categories count twice for weighting)

        # Value might be (betsize, #)
        # where betsize is [small, medium, large]
        #   and # is some score/rank from 1-10
        return value

    # FUNCTION: allocateFunds
    # INPUT: coin_list - list of each asset with ranking values
    #        balances  - dictionary of balance for each asset
    def allocateFunds(coin_list, balances):
        for coin in coin_list:
            # Find matching balance tuple with asset as key or something

        return something

    # FUNCTION: main
    # INPUT: assets - list of supported assets
    # OUTPUT: N/A
    # DESCRIPTION: 
    #   Top level function for the coin ranker.
    def main(assets):
        # Balances should probably be a dictionary
        balances = getBalances(asset)
        coin_list = rankCoins()
        distribution_values = allocateFunds(coin_list, balances)

# CLASS: CoinBuyer
class CoinBuyer():

    # INPUT:  dictionary of [grouping : [pairing : percentage_allocated]
    #         total value to be allocated
    # 1. Check exchanges pairing is on
    # 2. Allocate quantity based on input
    # 3. Buy from exchange with API written
    #   a. Return error if exchange API doesn't exist
    # 4. Validate buy went through
    # 5. Store result in database
    # 6. Move onto next coin


# TODO:
# - Minimum buy all coins (? $2, .0005 btc minimum)
# - Given list of coins, find all exchanges needed
# - Plan exchange APIs
# - First round buys all coins on exchanges that are already supported
# - Function that outputs BTC quantity required, function that transfers necessary funds to buy
#    all coins to appropiate exchanges
# - Logic functions should deal with percentage of total input

# ----------- COIN RANKER THEORY -----------
# PART ONE:
# Dictionary for each grouping:
# OUTER DICTIONARY: [grouping : grouping_dict]
# INNER DICTIONARY: [currency : aggregate_score]
# FOR EACH GROUPING:
#   Output aggregate score for a currency using logic functions
#   FUNCTION(TUPLE)
#       FUNCTION(PRICE) :: DO THIS TO SCORE
#       FUNCTION(VOLUME) :: DO THIS TO SCORE (+1)
#       RETURN AGGREGATE SCORE
#   Add [currency : aggregate_score] to current grouping_dict

# PART TWO:
# INPUT: grouping dictionary from previous part
# OUTER DICTIONARY: [grouping : value_dict]
# INNER DICTIONARY: [currency : percentage_allocated]
# FOR each grouping
#   allocate certain percentage of fund based on grouping type
#   allocate percentage of grouping_fund to each currency based on aggregate_score
# Return outer dictionary to coinbuyer