import sys
sys.path.append('C:/C-directory/Projects/Work-i/Components/Crypto-API/Exchange_APIs')
sys.path.append('C:/C-directory/Projects/Work-i/Components/Crypto-API/Main')

from API import ExchangeAPI
import Bittrex

if __name__ == "__main__": 
	# ExchangeAPI.sellLimit("binance", "BTC-KMD", 5, 0.000444)
	# ExchangeAPI.sellLimitAbs("bittrex", "BTC-KMD", 5, 0.00048, .5)
	print(ExchangeAPI.getDepositHistoryAsset("binance", "ETH", 0))
	print(ExchangeAPI.getDeposit("binance", "ETH", 2.0))
	print(ExchangeAPI.getDeposit("binance", "ETH", 1.1))
	print(ExchangeAPI.checkDeposit("binance", "ETH", 2.0, 0))

	# SellLimit/BuyLimit tests for Binanace

	# MIN ORDER / NOTIONAL
	print(ExchangeAPI.buyLimit('binance'))
	print(ExchangeAPI.sellLimit('binance'))

	# LOT SIZE
	print(ExchangeAPI.buyLimit('binance'))
	print(ExchangeAPI.sellLimit('binance'))
