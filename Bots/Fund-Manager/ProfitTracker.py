import sys
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Arbitrage/Libraries')

# External-Import 
import time
from random import randint

# Internal-Import
from PTrackingLibrary import PTrackingLibrary
from PrintLibrary import PrintLibrary

# CLASS: ProfitTracker
# DESCRIPTION:
#	Top level object for profit tracking component. More comprehensive description to come.
class ProfitTracker(object):

	# INITIALIZATION: 
	# 	* - TODO, figure out the initialize parameters
    def __init__(self, clean=True):
    	PrintLibrary.displayMessage("ProfitTracker Initialized")

    # FUNCTION: runHourly
    # INPUT: exchanges	- [string]
    #		 assets     - [string]
    #		 balances  	- TODO
    # OUTPUT: N/A
    # DESCRIPTION:
    #	Top level function for profit tracking on the hour
    def runHourly(exchanges, assets):
        balances = PTrackingLibrary.retrieveAccountBalances(exchanges, assets)
        hourly_metrics = PTrackingLibrary.calculateMetrics(balances, exchanges, assets)
        print(hourly_metrics)

	# FUNCTION: runDaily
	# INPUT: exchanges  - [string]
	#		 assets		- [string]
	#		 balances	- TODO
	# OUTPUT: N/A
	# DESCRIPTION:
	#	Top level function for profit tracking on the daily
    def runDaily(exchanges, assets, balances):
        daily_metrics = PTrackingLibrary.calculateMetrics(balances, print_b, exchanges, assets)
        print(daily_metrics)