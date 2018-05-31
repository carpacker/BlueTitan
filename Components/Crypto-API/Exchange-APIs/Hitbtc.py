# External-Imports
import hashlib
import hmac
import json
import time
import requests
import sys

# Windows path
sys.path.append('U:/Directory/Projects/BlueTitan/Bots/Arbitrage/Libraries')

# Linux path
# sys.path.append()

# Internal-Imports
from PrintLibrary import PrintLibrary

# Secret Keys
from secret_keys import hitbtc_private_key, hitbtc_public_key 

# Endpoint URLs
base_url = ""

######################################## PUBLIC CALLS ##############################################
####################################################################################################

######################################## MARKET CALLS ##############################################
####################################################################################################

# FUNCTION: getOrderbook
# INPUT: pairing - string
# OUTPUT: Dictionary
# DESCRIPTION:
#   Retrieves the orderbook for a given pairing. Output dictionary contains list of asks and bids,
#    ordered ascending and descending respectively.
def getOrderbook():
    pass

######################################## ORDER CALLS ###############################################
####################################################################################################

####################################### ACCOUNT CALLS ############################################## 
####################################################################################################

########################################## HELPERS #################################################
####################################################################################################