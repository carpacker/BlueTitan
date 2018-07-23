# ArbitrageTests.py
# Carson Packer
# DESCRIPTION:
#    Tests involving the arbitrage-trader bot subsystem. This testin gsuite goes through individual
#     testers by library, then performs a runtime test of the actual system in isolation.

# External-Imports
import sys
import time

# WINDOWS main-desktop, LINUX main-server
sys.path.append('U:/Directory/Projects/Work/BlueTitan/Components/Libraries')

# WINDOWS laptop
# sys.path.append()

# Internal Imports
from PrintLibrary import PrintLibrary
from ArbitrageLibrary import ArbitrageLibrary
from BalancingLibrary import BalancingLibrary
from ArbitrageTrader import 0

# TESTER: arbitrageUnitTests
# DESCRIPTION:
#   Tests for functions in the ArbitrageLibrary.py file
def arbitrageUnitTests():
    PrintLibrary.header("Arbitrage Unit Tests")
    ArbitrageLibrary.getAggregateWFees()
    ArbitrageLibrary.checkMinOrder()
    ArbitrageLibrary.convertMinPrice()
    ArbitrageLibrary.convertMinQuantity()
    ArbitrageLibrary.decideOrder()

# TESTER: balancingUnitTests
# DESCRIPTION:
#   Individual tests for balancing related functions, pulls from the BalancingLibraory.py file
def balancingTests():
    PrintLibrary.header("Balancing Unit Tests")

# TESTER: databaseTests
# DESCRIPTION:
#    Tests for specific database functions pertinent to arbitrage.
def databaseTests():
    pass

# TESTERS: Main function
# DESCRIPTION:
#    Performs a test run of arbitrage trading. More to come
def mainTesters():
    PrintLibrary.header("Main Tester")

if __name__ == '__main__':
    ArbitrageUnitTests()
    BalancingUnitTests()
