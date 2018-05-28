# External-Imports
import json
import requests
import sys

# Windows path
sys.path.append('U:/Directory/Projects/BlueTitan/Bots/Arbitrage/Libraries')

# Linux path
# sys.path.append()

# Internal-Imports
from PrintLibrary import PrintLibrary

base_url = 'https://api.coinmarketcap.com/v1/ticker/'

######################################## COINMARKETCAP #############################################
#   BASE CALLS
# * - getGlobal   :  
# * - getTicker   :
# * - getTickerId :

#   DERIVATIVE CALLS
# * - getPriceBTC :
# * - getPriceUSD :

######################################### BASE CALLS ##############################################
# FUNCTION: getGlobal
# INPUT: N/A
# OUTPUT: dictionary
# DESCRIPTION:
#   Returns global data from coinmarketcap.
def getGlobal():
    json_var = requests.request('GET', 'https://api.coinmarketcap.com/v1/global/').json()
    # TODO: json standardization stuff here
    return json_var

# FUNCTION: getTicker
# INPUT: start (optional) - int
#        limit (optional) - int
# OUTPUT: Dictionary
# DESCRIPTION:
#   Get ticker data of all assets
def getTicker(start=None, limit=None):
    json_var = requests.request('GET', base_url).json()
    # TODO: json standardization stuff here
    return json_var

# FUNCTION: getTicker
# INPUT: asset            - string
#        start (optional) - int
#        limit (optional) - int
# OUTPUT: dictionary
# DESCRIPTION:
#   Get ticker data for a specific asset
def getTickerId(asset, start=None, limit=None):
    asset_id = convertId(asset)
    url = base_url + asset_id
    json_var = requests.request('GET', url).json()
    # * -TODO RETURN DICTIONARY STUFF HERE
    return json_var[0]

######################################## DERIVATIVES #############################################

# FUNCTION: getPriceBTC
# INPUT: start (optional) - int
#        limit (optional) - int
# OUTPUT: dictionary
# DESCRIPTION:
#	Get ticker data for a specific asset
def getPriceBTC(asset):
    asset_id = convertId(asset)
    url = base_url + asset_id
    json_var = requests.request('GET', url).json()
    # TODO RETURN DICTIONARY STUFF HERE
    return json_var[0]["price_btc"]

# FUNCTION: getPriceUSD
# INPUT: start (optional) - int
#        limit (optional) - int
# OUTPUT: dictionary
# DESCRIPTION:
#   Get ticker data for a specific asset
def getPriceUSD(asset):
    asset_id = convertId(asset)
    url = base_url + asset_id
    json_var = requests.request('GET', url).json()
    # TODO RETURN DICTIONARY STUFF HERE
    return json_var[0]["price_usd"]


######################################### HELPERS ###############################################

# FUNCTION: convertId()
# INPUT: asset - string
# OUTPUT: asset string in coinamrketcap form
# DESCRIPTION:
# 	Converts an input asset identifier to the long-form, which is required as an input to
#	 coinmarketcap.
def convertId(asset):
    id_dict = {"BTC" : "bitcoin", 
                "ETH" : "ethereum",
                "KMD" : "komodo",
                "ADA" : "cardano",
                "XMR" : "monero",
                "XRP" : "ripple",
                "XVG" : "verge",
                "USDT" : "tether",
                "OMG" : "omisego",
                "BAT" : "basic-attention-token",
                "ARK" : "ark"}
    return id_dict[asset]


# NOTES: 
# - Endpoints update every five minutes
# - Limit requests to no more than 10 per minute
