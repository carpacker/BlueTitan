import sys
sys.path.append('U:/Directory/Projects/BlueTitan/Bots/Fund-Manager')

# External-Import 
import time
from random import randint

# Internal-Import
from PrintLibrary import PrintLibrary

# CLASS: ProfitTracker
# DESCRIPTION:
#   Top level object for profit tracking component. More comprehensive description to come.
class ProfitTracker(object):

    # INITIALIZATION: 
    #  * - TODO, figure out the initialize parameters
    def __init__(self, clean=True):
    	PrintLibrary.displayMessage("ProfitTracker Initialized")

