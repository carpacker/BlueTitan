# Polling.py
# Carson Packer
# DESCRIPTION:
#   Top-level script which builds database of information related to cryptocurrencies over time.
#    This includes price, volume, etc. Additionally, it will be able to perform algorithms in
#    between in order to test the effectiveness of an algorithm simultaneously.

# External-Imports
from copy import deepcopy
import math
import sys
import threading
import time

# WINDOWS main-desktop
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Crypto-API/Exchange-APIs')
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Database-manager')
sys.path.append('U:/Directory/Projects/BlueTitan/Bots/Market-Tracker/Libraries')

# WINDOWS laptop
# sys.path.append()

# LINUX main-server
# sys.path.append()

# Internal-Imports
from API import ExchangeAPI
import Helpers
import DatabaseLibrary
from GeneralizedDatabase import GenDatabaseLibrary

# Polling version of algorithms
import ArbitragePolling
import CurrencyPolling

# CLASS: Polling
# DESCRIPTION:
#    TODO
class Polling(object):
    pass

if __name__ == "__main__":
    Polling().Arbitrage()
