# ArbitrageTests.py
#  BlueTitan Trading System
#  Carson Packer
#  Paq Ltd.
# DESCRIPTION:
#    Tests involving the arbitrage-trader bot subsystem. This testin gsuite goes through individual
#     testers by library, then performs a runtime test of the actual system in isolation.

# External-Imports
import sys
import time

# Relative Imports

# Internal Imports
from PrintLibrary import PrintLibrary
from ArbitrageLibrary import ArbitrageLibrary
from BalancingLibrary import BalancingLibrary
from ArbitrageTrader import BTArbitrage

# TESTER: arbitrageUnitTests
# DESCRIPTION:
#   Tests for functions in the ArbitrageLibrary.py file.
def ArbitrageTests():
    PrintLibrary.header("Arbitrage Unit Tests")
    PrintLibrary.delimiter()

    PrintLibrary.header("checkMinOrder")
    PrintLibrary.displayDictionary(ArbitrageLibrary.checkMinOrder())
    PrintLibrary.displayDictionary(ArbitrageLibrary.checkMinOrder())
    PrintLibrary.displayDictionary(ArbitrageLibrary.checkMinOrder())
    PrintLibrary.displayDictionary(ArbitrageLibrary.checkMinOrder())
    PrintLibrary.displayDictionary(ArbitrageLibrary.checkMinOrder())
    PrintLibrary.delimiter()
    
    PrintLibrary.displayDictionary(ArbitrageLibrary.convertMinPrice())
    PrintLibrary.displayDictionary(ArbitrageLibrary.convertMinQuantity())
    PrintLibrary.displayDictionary(ArbitrageLibrary.decideOrder())

# TESTER: balancingUnitTests
# DESCRIPTION:
#   Individual tests for balancing related functions, pulls from the BalancingLibraory.py file
def BalancingTests():
    PrintLibrary.header("Balancing Unit Tests")

# TESTER: databaseTests
# DESCRIPTION:
#    Tests for specific database functions pertinent to arbitrage.
def DatabaseTests():
    pass

# TESTERS: Main function
# DESCRIPTION:
#    Performs a test run of arbitrage trading. Tests both execute and limit arbitrage.
def mainTest():
    PrintLibrary.header("Main Tester")

if __name__ == '__main__':
    ArbitrageTests()
    BalancingTests()
    DatabaseTests()
    # mainTest()
