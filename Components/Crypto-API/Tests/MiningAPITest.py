# MiningAPI tests
import sys
sys.append()

import Ethermine

# Tests for Ethermine
def ethermineTests():
	print(Ethermine.getPoolStats())
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