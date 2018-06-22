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
#   Top level object for profit tracking component. More comprehensive description to come.
class ProfitTracker(object):

    # INITIALIZATION: 
    #  * - TODO, figure out the initialize parameters
    def __init__(self, clean=True):
    	PrintLibrary.displayMessage("ProfitTracker Initialized")

