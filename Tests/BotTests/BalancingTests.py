if __name__ == '__main__':
	# 1. Test transfering base, quote individually
	value  = BalancingLibrary.transferQuote("KMD", 10, "binance", "bittrex")
	print(value)
	value = BalancingLibrary.transferBase("BTC", .005, "bittrex", "binance")
	print(value)

	# 2. Test a 'balance account' action [both together, with a storeTransfer]
	value = BalancingLibrary.balancePairing("BTC-KMD", .005, 10, "binance", "bittrex")
	print(value)
