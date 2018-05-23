# Price Detection script

# FUNCTION: checkProfitability
def checkProfitability(asset, period):
	pass

# FUNCTION: rankProfitability
def rankProfitability(assets, period):
	max_val = 0
	max_asset = ""
	for asset in assets:
		profit_period = checkProfitability(asset, period)
		if profit_period > max_val:
			max_val = profit_period
			max_asset = asset

	result_tuple = (max_asset, max_val)
	return result_tuple