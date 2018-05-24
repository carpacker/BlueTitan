# External-Imports
import sys
sys.path.append("U:/Directory/Projects/BlueTitan/Components/Libraries")
sys.path.append("U:/Directory/Projects/BlueTitan/Components/Crypto-API/Mining-APIs")

# Internal-Imports
import Ethermine
from PrintLibrary import PrintLibrary

# TESTERS: ethermine
# DESCRIPTION:
#	Tests each ethermine call individually and prints the results. Each result has a header for
#	 what function is being tested.
def ethermineTests():
	PrintLibrary.displayDictionary(Ethermine.getPoolStats(), "getPoolStats")
	time.sleep(5)
	print(Ethermine.getNetworkStats())
	time.sleep(5)
	print(Ethermine.getHashrates())
	time.sleep(5)
	print(Ethermine.getMinerHistory())
	time.sleep(5)
	print(Ethermine.getMinerPayouts())
	time.sleep(5)
	print(Ethermine.getMinerRounds())
	time.sleep(5)
	print(Ethermine.getMinerStatistics())
	time.sleep(5)
	print(Ethermine.getWorkStatisticsAll())
	time.sleep(5)
	print(Ethermine.getWorkerHistory())
	time.sleep(5)
	print(Ethermine.getWorkerStatistics())
	time.sleep(5)
	print(Ethermine.getWorkerMonitor())

# Tests for Siamining
def siaminingTests():
	pass

# Tests for generic implementation
def genericTests():
	pass


if __name__ == '__main__':
	ethermineTests()