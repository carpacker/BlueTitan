import sys
import urllib.request as request
import requests
import json

# Internal-Imports
from PrintLibrary import PrintLibrary

exchanges = ["binance"]
# Flow: get this thing to grab the fees, print test to check, then store in database
#		Once that is finished, in ArbitrageLibrary test through the incorporated fees. Potentially change some numbers around.
#  Need to figure out how best to actually retrieve the values off the website
# Script will grab fees, calculate USD value and store them in assetinformation database

# FUNCTION: getFee
# simple for now...
class FeeScraper(object):

	# FUNCTION: getFee
	# simple for now...
	def getFee(exchange, asset):
            fee = FeeScraper.grabFeesPage(exchange, asset)
	    PrintLibrary.displayVariable(fee, "fee")
	    return fee

	# FUNCTION: processFeeDict
	# INPUT: list_i - [dictionary1, ..., dictionaryN]
	# OUTPUT: input list as dictionary
	# DESCRIPTION
	#	Convert's binance's list format for transaction fees into a more easily accessible dictionary format.
	def processFeeDict(list_i):
	    return_dict = {}
	    for value in list_i:
       		return_dict[value['assetCode']] = value['transactionFee']
	    return return_dict

	# FUNCTION: grabFeesPage
	# INPUT: exchange - strig
	# OUTPUT: TODO
	# DESCRIPTION:
	#	Grabs the HTML fees page for a given exchange (Currently only necessary for binance)
	def grabFeesPage(exchange, asset):
       	if exchange == 'binance':
	    url = "https://www.binance.com/assetWithdraw/getAllAsset.html"
	    html = requests.get(url)
	    json = html.json()
	    print(len(json))
	    if len(json) == 0:
		raise Exception("Page failed to load")
	    fee_dict = FeeScraper.processFeeDict(json)
	    fee = fee_dict[asset]
	    else:
		raise Exception("Not a Supported Exchange")

	    return fee



if __name__ == '__main__':
	FeeScraper.grabFeesPage('binance', 'ETH')
