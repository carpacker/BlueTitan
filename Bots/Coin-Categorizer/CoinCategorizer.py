# CoinCategorizer.py
# Carson Packer
# DESCRIPTION:
#    Top level function

# External-Imports
import sys
import csv

# WINDOWS main-desktop, LINUX main-server
sys.path.append("U:/Directory/Projects/Work/BlueTitan/Components/Libraries")
sys.path.append("U:/Directory/Projects/Work/BlueTitan/Components/
sys.path.append("U:/Directory/Projects/Work/BlueTitan/Components/
# Internal-Import
from API import ExchangeAPI
import Helpers

# CLASS: CoinCategorizer
# DESCRIPTION:
#    Suite of functions relevant to cateogrizing and purchasing unknown cryptocurrencies.
def CoinCategorizer(Object):

    # FUNCTION: main
    # INPUT: assets - list of supported assets
    # OUTPUT: N/A
    # DESCRIPTION: 
    #   Top level function for the coin categorizer.
    def main(file_name):
        # 1. Parsse the CSV for the values we will be working with
        coin_info = CoinCategorizer.parseCSV(file_name)
        balances = getBalances(asset)
        coin_list = rankCoins()
        distribution_values = allocateFunds(coin_list, balances)

    # FUNCTION: buildAssetList
    # INPUT: coin_info - [(data, ...), ...]
    # OUTPUT: list
    # DESCRIPTION:
    #    Runs through our coin info list taking each asset and adding it to asset list.
    def buildAssetList(coin_info):
        pass
    
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
    # OUTPUT: int
    # DESCRIPTION:
    #   Takes an input coin tuple and assigns an aggregate score based on its values.
    def assignValue(coin_tuple):

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

    # FUNCTION: buyCoin
    def buyCoin():
        pass
