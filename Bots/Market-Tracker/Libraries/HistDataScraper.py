import sys
sys.append("")

# External-Imports
import time
import urllib.request as request
import requests
import json

# Internal-Imports
from DatabaseLibrary import DatabaseLibrary


# 					Historical Data Scraper
#
# 	Designed to build historical database for currencies

# FUNCTION: scapeCurrency
# INPUT: currency - string
#		 period   - int [months]
# OUTPUT: N/A
# DESCRIPTION:
#	Pulls and stores data for a single currency for a given period on coinmarketcap.com
#	 and stores it in the historical-data-db.
def scrapeCurrency(currency, period):
	pass

# FUNCTION: scapeCurrencies
# INPUT: currencies - [string, ...]
#		 period   	- int [months]
# OUTPUT: N/A
# DESCRIPTION:
#	Pulls and stores data for a list of currencies for a given period on coinmarketcap.com
#	 and stores it in the historical-data-db.
def scrapeCurrencies(currencies, period):
	pass

