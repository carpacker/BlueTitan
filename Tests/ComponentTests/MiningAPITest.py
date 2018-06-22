# External-Imports
import time
import sys
sys.path.append("U:/Directory/Projects/BlueTitan/Components/Libraries")
sys.path.append("U:/Directory/Projects/BlueTitan/Components/Crypto-API/Mining-APIs")

# Internal-Imports
import Ethermine
import Siamining
from PrintLibrary import PrintLibrary

# TESTERS: ethermine
# DESCRIPTION:
#   Tests each ethermine call individually and prints the results. Each result has a header for
#    what function is being tested.
def ethermineTests():
    PrintLibrary.header("Ethermine Tests")
    PrintLibrary.displayDictionary(Ethermine.getPoolStats(), "getPoolStats")
    time.sleep(5)
    PrintLibrary.displayDictionary(Ethermine.getNetworkStats(), "getNetworkStats")
    time.sleep(5)
    PrintLibrary.displayDictionary(Ethermine.getHashrates(), "getHashrates")
    time.sleep(5)
    PrintLibrary.displayDictionary(Ethermine.getMinerHistory(), "getMinerHistory")
    time.sleep(5)
    PrintLibrary.displayDictionary(Ethermine.getMinerPayouts(), "getMinerPayouts")
    time.sleep(5)
    PrintLibrary.displayDictionary(Ethermine.getMinerRounds(), "getMinerRounds")
    time.sleep(5)
    PrintLibrary.displayDictionary(Ethermine.getMinerStatistics(), "getMinerStatistics")
    time.sleep(5)
    PrintLibrary.displayDictionary(Ethermine.getWorkStatisticsAll(), "getWorkStatisticsAll")
    time.sleep(5)
    PrintLibrary.displayDictionary(Ethermine.getWorkerHistory(), "getWorkerHistory")
    time.sleep(5)
    PrintLibrary.displayDictionary(Ethermine.getWorkerStatistics(), "getWorkerStatistics")
    time.sleep(5)
    PrintLibrary.displayDictionary(Ethermine.getWorkerMonitor(), "getWorkerMonitor")

# TESTERS: siamining
# DESCRIPTION:
#   Tests each ethermine call individually and prints the results. Each result has a header for
#    what function is being tested.
def siaminingTests():
    pass

# TESTERS: generic
# DESCRIPTION:
#   Tests the generic API for mining. It makes a call to each supported site in order to verify
#    that each generic function works.
def genericTests():
	pass

if __name__ == '__main__':
	ethermineTests()
    siaminingTests()
    genericTests()