import sys
# SYS imports for PERSONAL DESKTOP
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Crypto-API/Main')
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Arbitrage/Information_accounting')
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Database-RD')
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Arbitrage')

# SYS imports for MAIN ARBITRAGE SERVER
# TODO

# Internal-Imports
import API
from API import ExchangeAPI
from DatabaseManager import ArbitrageDatabase
import Helpers
from Helpers import DatabaseHelpers
from AccountBalancing import AccountBalancing
from ProfitTracker import ProfitTracker

# TODO 
# 	Organize these testers in some coherent way for each file...
#  The point of this testing suite is to provide unit tests for specific components of the project
#   and to provide a general space to test different aspects piece by pieces. At some point this
#   file will contain a tester for each individual function that can be viably tested for the purpose
#   of proving the validity of said function.

def currentTests():
	pass

if __name__ == '__main__':
	currentTests()