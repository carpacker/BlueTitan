import json
import requests

# NOTES: 
# - Endpoints update every five minutes
# - Limit requests to no more than 10 per minute
# TODO DICTIONARY FORMAT RETURNS
# TODO add derivatives like getPrice


# FUNCTION: getTicker
# INPUT: start (optional) - int
#		 limit (optional) - int
# OUTPUT: dictionary
# DESCRIPTION:
#	Get ticker data of all assets
def getTicker(start=None, limit=None):
	req = requests.request('GET', 'https://api.coinmarketcap.com/v1/ticker/').json()
	return req

# FUNCTION: getTicker
# INPUT: start (optional) - int
#		 limit (optional) - int
# OUTPUT: dictionary
# DESCRIPTION:
#	Get ticker data for a specific asset
def getTickerId(asset):
	asset_id = convertId(asset)
	url = 'https://api.coinmarketcap.com/v1/ticker/' + asset_id
	json_var = requests.request('GET', url).json()
	# * -TODO RETURN DICTIONARY STUFF HERE
	return json_var[0]

# FUNCTION: getPriceBTC
# INPUT: start (optional) - int
#		 limit (optional) - int
# OUTPUT: dictionary
# DESCRIPTION:
#	Get ticker data for a specific asset
def getPriceBTC(asset):
	asset_id = convertId(asset)
	url = 'https://api.coinmarketcap.com/v1/ticker/' + asset_id
	json_var = requests.request('GET', url).json()
	# TODO RETURN DICTIONARY STUFF HERE
	return json_var[0]["price_btc"]

# FUNCTION: getPriceUSD
# INPUT: start (optional) - int
#		 limit (optional) - int
# OUTPUT: dictionary
# DESCRIPTION:
#	Get ticker data for a specific asset
def getPriceUSD(asset):
	asset_id = convertId(asset)
	url = 'https://api.coinmarketcap.com/v1/ticker/' + asset_id
	json_var = requests.request('GET', url).json()
	# TODO RETURN DICTIONARY STUFF HERE
	return json_var[0]["price_usd"]

# FUNCTION: getGlobal
# INPUT: N/A
# OUTPUT: dictionary
# DESCRIPTION:
#	Returns global data from coinmarketcap
def getGlobal():
	req = requests.request('GET', 'https://api.coinmarketcap.com/v1/global/').json()
	return req

# FUNCTION: convertId()
# INPUT: asset - string
# OUTPUT: asset string in coinamrketcap form
# DESCRIPTION:
# 	TODO
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
