    balances_info = {"name" : "AccountBalances"}
    fae_info = {"name" : "IntendedFAE"}
    trades_info = {"name" : "ArbitrageTrades",
               "initialize" : 0}
    lfailure_info = {"name" : "LFailureTrades"}
    mfailure_info = {"name" : "MFailureTrades"}
    balancing_info = {"name" : "BalancingHistory"}
    asset_info = {"name" : "AssetInformation"}
    arb_errors_info = {"name" : "Errors"}

# 	selectDistinct
    def getCurrenciesAmounts(cursor, exchange, table_name=ACCOUNT_BALANCES_NAME):
        sql_s = "SELECT DISTINCT Asset, Amount, Btc_value, Usd_value FROM %s WHERE Exchange= ? " % table_name
        cursor.execute(sql_s,(exchange,))
        currencies = cursor.fetchall()
        return currencies

    def getExchanges(cursor, table_name=ACCOUNT_BALANCES_NAME):
        sql_s = "SELECT DISTINCT Exchange FROM %s" % table_name
        cursor.execute(sql_s)
        exchanges = cursor.fetchall()
        final_ex = []
        for ex in exchanges:
            final_ex.append(ex[0])
        return final_ex

    # ------------------------- MISC HELPER FUNCTIONS ----------------------------
    def getAssets(cursor, exchange, table_name=ACCOUNT_BALANCES_NAME):
        sql_s = "SELECT DISTINCT Asset FROM %s WHERE Exchange= ? " % table_name
        cursor.execute(sql_s,(exchange,))
        currencies = cursor.fetchall()
        final_curr = []
        for curr in currencies:
            final_curr.append(curr[0])
        return final_curr
    # FUNCTION: getFAEProportion
    # TODO... add second one or fleexible
    def getFAEProportion(cursor, asset, exchange, table_name=FAE_NAME):
        sql_s = "SELECT Proportion_as FROM %s WHERE Exchange = ? AND Asset = ?" % table_name
        cursor.execute(sql_s, (exchange, asset,))
        row = cursor.fetchall()
        return row[0][0]
        pass

    # F: Retrieval 
    #       [trade_values]
    def getTrade(cursor, id_value, table_name=TRADE_TABLE_NAME):
        sql_s = "SELECT FROM %s WHERE id = ?" % table_name
        cursor.execute(sql_s,(id_var,))
        cols = cursor.fetchall()
        return cols

    # F: Retrieval 
    #       [trade_values_1, trade_values_2, ... CUTOFF]
    #       *restricted by period of time
    # TODO - FIX THESE TWO TIME FRAMES
    def getTradesTimeframe(cursor, days, table_name=TRADE_TABLE_NAME):
        one_day = 60*60*24 # seconds
        time = int(time.time() * 1000)
        cutoff = time - (one_day*days)
        sql_s = 'SELECT FROM %s WHERE Time_stamp < %s' % cutoff
        cursor.execute(sql_s)
        cols = cursor.fetchall()
        return cols

    # FUNCTION: getFAEProportion
    # INPUT:
    # OUTPUT:
    # DESCRIPTION:
    #   Retrieves the proportion of exchange-asset pairing of the FAE.
    def getFAEProportion(asset, exchange):
        connect, cursor = ArbitrageDatabase.connect()
        table_name = ArbitrageDatabase.FAE_NAME
        table_names = listTables(cursor)
        checkTableNameExists(cursor, table_name, table_names)
        fae = ArbitrageDatabase.getFAEProportion(cursor, asset, exchange)
        disconnect(connect)   
        return fae

    # FUNCTION: retrieveTrade
    # INPUT: uuid - Unique Identifier
    # OUTPUT: trade object
    # DESCRIPTION:
    #   Retrieves a specific trade based on unique identifier.
    def retrieveTrade(uuid):
        connect, cursor = ArbitrageDatabase.connect()
        timestamp = Helpers.createTimestamp()
        table_name = ArbitrageDatabase.TRADE_TABLE_NAME
        checkTableNameExists(cursor, table_name, ArbitrageDatabase)
        trade = ArbitrageDatabase.getTrade(cursor, uuid, table_name)
        return trade

    def getBalancingOperation():
        pass


    # WRAPPER: getTransfersExchange
    # INPUT: exchange - string
    #        period   - TODO [OPTIONAL]
    # OUTPUT: [transfer1, ...]
    # DESCRIPTION:
    #   Returns all transfers that involved a specific exchange. Can input 
    #    a range of time to retrieve transfers from a specific exchange for a 
    #    given time period.
    def getTransfersExchange(exchange, period=""):
        pass

    # WRAPPER: getTransfersPairing
    # INPUT: pairing - string
    #        period  - TODO [OPTIONAL]
    # OUTPUT: [transfer1, ...]
    # DESCRIPTION:
    #   Returns all transfers that involved a specific pairing. Can input
    #    a range of time to retrieve transfers from a specific pairing for a
    #    given period of time.
    def getTransfersPairing(pairing, period=""):
        pass
    pass
    # FUNCTION: getDepositAddress
    # INPUT:
    # OUTPUT:
    # DESCRIPTION:
    #   
    def getDepositAddress(asset, exchange):
        connect, cursor = ArbitrageDatabase.connect()
        table_name = ArbitrageDatabase.ASSET_INFO_NAME
        table_names = listTables(cursor)
        checkTableNameExists(cursor, table_name, table_names)
        depositaddress = ArbitrageDatabase.getDepositAddress(cursor, asset, exchange)
        disconnect(connect)
        return depositaddress

    # FUNCTION: getWithdrawalTag
    # INPUT: 
    # OUTPUT: 
    # DESCRIPTION:
    #   
    def getWithdrawalTag(asset, exchange):
        connect, cursor = ArbitrageDatabase.connect()
        table_name = ArbitrageDatabase.ASSET_INFO_NAME
        table_names = listTables(cursor)        
        checkTableNameExists(cursor, table_name, table_names)
        tag = ArbitrageDatabase.getWithdrawalTag(cursor, asset, exchange)
        disconnect(connect)
        return tag

# EACH needs
# STORE/INSERT
# GET1, GET*, GET*by time
# DELETE1, DELETE*, DELETE*by time
#

# UPDATE VALUE BASED ON INPUTS
    # FUNCTION: updateFAEProportions
    # Do both of the below
    # FUNCTION: updateDepositAddress
    def updateDepositAddress(cursor, asset, exchange, address, table_name=ASSET_INFO_NAME):
        sql_s = "UPDATE %s SET Address = ? WHERE Exchange = ? AND Asset = ?" % table_name
        cursor.execute(sql_s,(address,exchange,asset))

    def updateFAEProportions():
        pass
    # FUNCTION: updateBalance
    def updateBalance(cursor, exchange, asset, amount, btc_value, usd_value, table_name=ACCOUNT_BALANCES_NAME):
        sql_s = "UPDATE %s SET Amount = ?, Btc_value = ?, Usd_value = ? WHERE Exchange = ? AND Asset = ?" % table_name
        cursor.execute(sql_s, (amount,exchange,asset,btc_value,usd_value))

    # FUNCTION: updateWithdrawalTag
    def updateWithdrawalTag(cursor, asset, exchange, table_name=ASSET_INFO_NAME):
        sql_s = "UPDATE %s SET Withdrawal_tag = ? WHERE Exchange = ? AND Asset = ?" % table_name
        cursor.execute(sql_s, (fee,exchange,asset))

    # FUNCTION: updateWithdrawalFee
    def updateWithdrawalFee(cursor, asset, exchange, fee, table_name=ASSET_INFO_NAME):
        sql_s = "UPDATE %s SET Withdrawal_fee = ? WHERE Exchange = ? AND Asset = ?" % table_name
        cursor.execute(sql_s, (fee,exchange,asset))
    # FUNCTION: updateFAEExchangeProportion
    def updateFAEExchangeProportion(cursor, asset, exchange, proportion, table_name=FAE_NAME):
        sql_s = "UPDATE %s SET Proportion_ex = ? WHERE Exchange = ? AND Asset = ?" % table_name
        cursor.execute(sql_s, (proportion, exchange, asset))

    # FUNCTION: updateFAEAccountProportion
    def updateFAEAccountProportion(cursor, asset, exchange, proportion, table_name=FAE_NAME):
        sql_s = "UPDATE %s SET Proportion_as = ? WHERE Exchange = ? AND Asset = ?" % table_name
        cursor.execute(sql_s, (proportion, exchange, asset))

# FORM THESE INTO MORE UNIQUE FUNCTIONS
def getAssets(cursor, exchange, table_name=ACCOUNT_BALANCES_NAME):
    sql_s = "SELECT DISTINCT Asset FROM %s WHERE Exchange= ? " % table_name
    cursor.execute(sql_s,(exchange,))
    currencies = cursor.fetchall()
    final_curr = []
    for curr in currencies:
        final_curr.append(curr[0])
    return final_curr

def getExchanges(cursor, table_name=ACCOUNT_BALANCES_NAME):
    sql_s = "SELECT DISTINCT Exchange FROM %s" % table_name
    cursor.execute(sql_s)
    exchanges = cursor.fetchall()
    final_ex = []
    for ex in exchanges:
        final_ex.append(ex[0])
    return final_ex

# TODO: rework this into balances
def getCurrenciesAmounts(cursor, exchange, table_name=ACCOUNT_BALANCES_NAME):
    sql_s = "SELECT DISTINCT Asset, Amount, Btc_value, Usd_value FROM %s WHERE Exchange= ? " % table_name
    cursor.execute(sql_s,(exchange,))
    currencies = cursor.fetchall()
    return currencies

# FUNCTION: getBalanceAll
def getBalanceAll(cursor, asset, exchange, table_name=ACCOUNT_BALANCES_NAME):
    sql_s = "SELECT Amount, Btc_value, Usd_value FROM %s WHERE Exchange = ? AND Asset = ?" % table_name
    cursor.execute(sql_s, (exchange, asset,))
    balance_rows = cursor.fetchall()
    row = balance_rows[0][0] if len(balance_rows) else 0
    return row # this should be amount

# FUNCTION: getBalanceAsset
#   Retrieves specifically the asset denominated quantity
def getBalanceAsset(cursor, asset, exchange, table_name=ACCOUNT_BALANCES_NAME):
    sql_s = "SELECT Amount FROM %s WHERE Exchange = ? AND Asset = ?" % table_name
    cursor.execute(sql_s, (exchange, asset,))
    balance_rows = cursor.fetchall()
    row = balance_rows[0][0] if len(balance_rows) else 0
    return row # this should be amount

# FUNCTION: getBalanceBTCVal
#   Retrieves the btc value of the quantity available of given asset
def getBalanceBTCVal(cursor, asset, exchange, table_name=ACCOUNT_BALANCES_NAME):
    sql_s = "SELECT Btc_value FROM %s WHERE Exchange = ? AND Asset = ?" % table_name
    cursor.execute(sql_s, (exchange, asset,))
    balance_rows = cursor.fetchall()
    row = balance_rows[0][0] if len(balance_rows) else 0
    return row # this should be amount

# FUNCTION: getBalanceUSDVal
#   Retrieves the btc value of the quantity available of given asset
def getBalanceUSDVal(cursor, asset, exchange, table_name=ACCOUNT_BALANCES_NAME):
    sql_s = "SELECT Usd_value FROM %s WHERE Exchange = ? AND Asset = ?" % table_name
    cursor.execute(sql_s, (exchange, asset,))
    balance_rows = cursor.fetchall()
    row = balance_rows[0][0] if len(balance_rows) else 0
    return row # this should be amount


    # ---------------------------------------- METRICS DATABASE ---------------------------------------

    # FUNCTION: initializeMetrics
    # INPUT: N/A
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Initializes the metrics table in the appropiate database.
    def initializeMetrics():
        table_name = MetricsDatabase.METRICS_TABLE_NAME
        connect, cursor = MetricsDatabase.connect()
        timestamp = Helpers.createTimestamp()
        uuid = createUuid()
        init_tuple = ("", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        checkTableNameExists(cursor, table_name, table_names)
        MetricsDatabase.insertMetric(cursor, timestamp, uuid, *init_tuple, table_name)
        disconnect(connect)

    # FUNCTION: initializeFailureMetrics
    # INPUT: N/A
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Initializes the failure metrics table in the appropiate database.
    def initializeFailureMetrics():
        table_name = MetricsDatabase.METRICSFAILURES_TABLE_NAME
        connect, cursor = MetricsDatabase.connect()
        timestamp = Helpers.createTimestamp()
        uuid = createUuid()
        init_tuple = ("", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        checkTableNameExists(cursor, table_name, MetricsDatabase)
        MetricsDatabase.insertFailureMetric(cursor, timestamp, uuid, *init_tuple, table_name)
        disconnect(connect)

    # --------------------------------------- ASSET METRICS  ---------------------------------------

    # FUNCTION: initializeAssetMetrics
    # INPUT: N/A
    # OUTPUT: N/A
    # DESCRIPTION:
    #   
    def initializeAssetMetrics():
        table_name = AssetMetricsDatabase.ASSETMETRICS_TABLE_NAME
        connect, cursor = AssetMetricsDatabase.connect()
        timestamp = Helpers.createTimestamp()
        uuid = createUuid()
        table_names = listTables(cursor)
        # Add session number to init tuple
        init_tuple = ("", "", "", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        checkTableNameExists(cursor, table_name, table_names)
        AssetMetricsDatabase.insertAssetMetric(cursor, timestamp, uuid, *init_tuple, table_name)
        disconnect(connect)

    # FUNCTION: initializeAssetMetricsFailure
    # INPUT: N/A
    # OUTPUT: N/A
    # DESCRIPTION:
    #   
    def initializeAssetMetricsFailure():
        table_name = AssetMetricsDatabase.ASSETMETRICSFAILURES_TABLE_NAME
        connect, cursor = AssetMetricsDatabase.connect()
        timestamp = Helpers.createTimestamp()
        uuid = createUuid()
        table_names = listTables(cursor)
        # Add session number to tuple, dont need in init probably
        init_tuple = ("", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        checkTableNameExists(cursor, table_name, table_names)
        AssetMetricsDatabase.insertAssetMetricFailure(cursor, timestamp, uuid, *init_tuple, table_name)
        disconnect(connect)
