# Notes for functions from deprecated.

# getAssets : select distinct asset where exchange = ?
# getExchanges : select distinct exchange

# getBalanceUSDVal,BTCVal,Asset[amount],All :: use exchange, asset
# getWithdrawaltag,depositAddress :: use asset, exchange
# Updates are the same

# FUNCTION: initializeMetrics
init_tuple = (timestamp, uuid, "", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
# FUNCTION: initializeFailureMetrics
init_tuple = (timestamp, uuid"", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
# FUNCTION: initializeAssetMetrics
init_tuple = (timestamp, uuid, "", "", "", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
# FUNCTION: initializeAssetMetricsFailure
init_tuple = (timestamp, uuid, "", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

def initializeTrades():
init_tuple = (timestamp, "", 0, 0, 0, "", "", 0, 0, 0, 0)

# FUNCTION: initializeFailureTrades
init_tuple = ("", 0, 0, "", "", 0, 0, 0, 0, "", "", 0)


def initializeTransferHistory():
    init_tuple = (0, 0, 0, "", "", "", 0, 0, 0)

def initializeErrors():
    input_tuple = ("N/A", "", "initialization")
