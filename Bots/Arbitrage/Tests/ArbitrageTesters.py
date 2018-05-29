# External-Imports
import sys
import time

# Windows
sys.path.append('U:/Directory/Projects/BlueTitan/Bots/Arbitrage/Libraries')

# Linux
# sys.path.append()

# Internal-Imports
from ArbitrageLibrary import ArbitrageLibrary
from BalancingLibrary import BalancingLibrary
from PrintLibrary import PrintLibrary

#									 TESTING SUITE
#
# DESCRIPTION:
#  The point of this testing suite is to provide unit tests for specific components of the project
#   and to provide a general space to test different aspects piece by pieces. At some point this
#   file will contain a tester for each individual function that can be viably tested for the purpose
#   of proving the validity of said function.

# TESTER: ArbitrageUnitTests
# DESCRIPTION:
#   Tests for functions in the ArbitrageLibrary.py file
def ArbitrageUnitTests():
    PrintLibrary.header("Arbitrage Unit Tests")
    ArbitrageLibrary.getAggregateWFees()
    ArbitrageLibrary.checkMinOrder()
    ArbitrageLibrary.convertMinPrice()
    ArbitrageLibrary.convertMinQuantity()
    ArbitrageLibrary.decideOrder()


# TESTER: BalancingUnitTests
# DESCRIPTION:
#   Individual tests for balancing related functions, pulls from the BalancingLibraory.py file
def BalancingUnitTests():
    PrintLibrary.header("Balancing Unit Tests")

if __name__ == '__main__':
    ArbitrageUnitTests()
    BalancingUnitTests()