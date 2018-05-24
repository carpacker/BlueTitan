# 1. write Store & test...
# 2. Replace store functions in each and test individually
# 3. write get/select & test
# 4. Replace get/select in each and test individually
# 5. SelectfromPeriod/table
# 6. Initializes


INITIALIZE FUNCTIONS



Possibly deprecate these comments
# CLASS: DatabaseLibrary
# DESCRIPTION:
#   Used to contain database calls. Acts as object for convinient references. Tables currently in use 
#    for the database include: ArbitradeTrades, AccountBalances, BalancingHistory, DepositAddresses, 
#    Metrics, FailureMetrics, AssetMetrics, AssetFailureMetrics.
class DatabaseLibrary(object):


----------------------------------------------------

# Work these into ONE function:
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

# Stores to replace
#    
# FUNCTION: insertBalance
def insertBalance(cursor, exchange, asset, amount, btc_value, usd_value, table_name=ACCOUNT_BALANCES_NAME):
    sql_s = "INSERT INTO %s(Exchange,Asset,Amount,Btc_value,Usd_value) VALUES (?,?,?,?,?)" % table_name
    cursor.execute(sql_s,(exchange,asset,amount,btc_value,usd_value))

# FUNCTION: insertFAE
def insertFAE(cursor, asset, exchange, proportion_as, proportion_ex, table_name=FAE_NAME):
    sql_s = "INSERT INTO %s(Exchange,Asset,Proportion_as,Proportion_ex) VALUES (?,?,?,?)" % table_name
    cursor.execute(sql_s,(exchange, asset, proportion_as, proportion_ex))
# FUNCTION: insertAssetInformation
def insertAssetInformation(cursor, asset, exchange, address, withdrawal_tag, withdrawal_fee, usd_fee, table_name=ASSET_INFO_NAME):
    sql_s = "INSERT INTO %s VALUES (?,?,?,?,?,?)" % table_name
    cursor.execute(sql_s,(asset, exchange, address, withdrawal_tag, withdrawal_fee, usd_fee))

# FUNCTION: insertDepositAddress
def insertDepositAddress(cursor, asset, exchange, address, table_name=ASSET_INFO_NAME):
    sql_s = "INSERT INTO %s VALUES (?,?,?)" % table_name
    cursor.execute(sql_s,(asset,exchange,address))

    # TODO, ADD UUID
def insertTransfer(cursor, time_stamp, transfer_time, buy_exchange, asset, amount, sell_exchange, base_t_asset,
                    base_btc_value, total_btc, fee_btc, buy_withdraw_id, sell_withdraw_id):
    sql_s = "INSERT INTO %s (Time_stamp, Transfer_time, Buy_exchange, Asset, Amount, Sell_exchange, Base_t_asset, Base_btc_value, Total_btc, Fee_btc, Buy_withdraw_id, Sell_withdraw_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)" % table_name
    cursor.execute(sql_s,(time_stamp, transfer_time, buy_exchange, asset, amount, sell_exchange, base_t_asset,
                    base_btc_value, total_btc, fee_btc, buy_withdraw_id, sell_withdraw_id))


# F: Insertion
#       [failure_values]
def insertMAFailure(cursor, Time_stamp, uuid, Symbol, Total_quantity, Total_btc, Buy_exchange, Sell_exchange, Avg_buy_rate, Avg_sell_rate,
                    Profit_ratio, Profit, Failed_exchange, Stage, Consecutive_fails, table_name="FailureTrades"):
    sql_s = "INSERT INTO %s(Time_stamp,Uuid,Symbol,Total_quantity,Total_btc,Buy_exchange,Sell_exchange,Avg_buy_rate,Avg_sell_rate,Profit_ratio,Profit,Failed_exchange,Stage,Consecutive_fails) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)" % table_name
    cursor.execute(sql_s,(Time_stamp,uuid,Symbol,Total_quantity,Total_btc,Buy_exchange,Sell_exchange,Avg_buy_rate,Avg_sell_rate,Profit_ratio,Profit,Failed_exchange,Stage,Consecutive_fails))

def insertLAFailure():
    pass

# F: Insertion
#       [trade_values]
def insertTrade(cursor, Time_stamp, uuid, Symbol, Total_quantity, Total_btc, Executed_quantity, Buy_exchange, Sell_exchange, Avg_buy_rate, Avg_sell_rate, Profit_ratio, Profit, table_name="ArbitrageTrades"):
    sql_s = "INSERT INTO %s(Time_stamp,Uuid,Symbol,Total_quantity,Total_btc,Executed_quantity,Buy_exchange,Sell_exchange,Avg_buy_rate,Avg_sell_rate,Profit_ratio,Profit) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)" % table_name
    PrintLibrary.displayKeyVariables((("uuid", uuid),
                                        ("Symbol", Symbol),
                                        ("Total Quantity", Total_quantity),
                                        ("BTC Value", Total_btc)))
    cursor.execute(sql_s,(Time_stamp,uuid,Symbol,Total_quantity,Total_btc,Executed_quantity,Buy_exchange,Sell_exchange,Avg_buy_rate,Avg_sell_rate,Profit_ratio, Profit))

# storeError
# F: Insertion
def insertError(cursor, timestamp, uuid, message, typeOf, stage, table_name=ERROR_TABLE_NAME):
    sql_s = "INSERT INTO %s VALUES (?,?,?,?,?)" % table_name
    cursor.execute(sql_s,(timestamp,uuid,message,typeOf,stage))
    # FUNCTION: storeError
    def storeError(error_values):
        connect, cursor = ArbitrageDatabase.connect()
        timestamp = Helpers.createTimestamp()
        uuid = createUuid()
        table_name = ArbitrageDatabase.ERROR_TABLE_NAME
        table_names = listTables(cursor)
        checkTableNameExists(cursor, table_name, table_names)
        ArbitrageDatabase.insertError(cursor, timestamp, uuid, *error_values, table_name)
        disconnect(connect)
        print("insertError", error_values, uuid)
    # Probably want to differentiate balancing operations and transfers between exchanges
    def storeBalancingOperation():

# FUNCTON: storeBalance
# INPUT: exchange   - string
#        asset      - string
#        quantity     - float
#        btc_value  - float (OPTIONAL)
#        usd_value  - float (OPTIONAL)
# OUTPUT: N/A
# DESCRIPTION:
#   Called in order to store the balance of a specific asset in the appropiate
#    database for account balances. If btc and usd value for the quantity aren't
#    provided, then the function calculates it to be stored.
def storeBalance(exchange, asset, quantity, btc_value, usd_value):
    connect, cursor = ArbitrageDatabase.connect()
    table_name = ArbitrageDatabase.ACCOUNT_BALANCES_NAME
    table_names = listTables(cursor)
    checkTableNameExists(cursor, table_name, table_names)
    ArbitrageDatabase.insertBalance(cursor, exchange, asset, quantity, btc_value, usd_value, table_name)
    disconnect(connect)

# FUNCTION: storeLimitArbitrage
# INPUT: TBD
# OUTPUT: N/A
# DESCRIPTION:
#   Wrapper to store data on a limit arbitrage trade.
def storeLimitArbitrage():
    connect, cursor = ArbitrageDatabase.connect()
    timestamp = Helpers.createTimestamp()
    uuid = createUuid("limit_arbitrage")
    table_name = ArbitrageDatabase.TRADE_TABLE_NAME
    checkTableNameExists(cursor, table_name, ArbitrageDatabase)
    ArbitrageDatabase.insertTrade(cursor, timestamp, uuid, *input_tuple)
    disconnect(connect)

# FUNCTION: storeMarketArbitrage
# INPUT: input_tuple -  symbol, total_quantity, filled_quantity, 
#                       buy_exchange, sell_exchange, avg_buy_rate,
#                       avg_sell_rate, profit_percent, profit
# OUTPUT: N/A
# DESCRIPTION:
#   Wrapper to store data on a market arbitrage trade.
def storeMarketArbitrage(input_tuple):
    connect, cursor = ArbitrageDatabase.connect()
    timestamp = Helpers.createTimestamp()
    uuid = createUuid("market_arbitrage")
    table_name = ArbitrageDatabase.TRADE_TABLE_NAME
    checkTableNameExists(cursor, table_name, ArbitrageDatabase)
    ArbitrageDatabase.insertTrade(cursor, timestamp, uuid, *input_tuple)
    disconnect(connect)

# FUNCTION: storeTransfer
# INPUT: withdraw_list - TODO
# OUTPUT: N/A
# DESCRIPTION:
#   TODO
def storeTransfer(withdraw_list):
connect, cursor = ArbitrageDatabase.connect()
timestamp = Helpers.createTimestamp()
table_name = ArbitrageDatabase.BALANCING_HISTORY_NAME
table_names = listTables(cursor)
checkTableNameExists(cursor, table_name, table_names)
ArbitrageDatabase.insertTransfer(cursor, timestamp, *withdraw_list, table_name)
disconnect(connect)
# FUNCTION: storeFAE
# INPUT:  asset      - string
#         exchange   - string
#         proportion - float 
# OUTPUT: N/A
# DESCRIPTION:
#   Stores a representative FAE balance entry.
def storeFAE(asset, exchange, proportion_as, proportion_ex):
    connect, cursor = ArbitrageDatabase.connect()
    table_name = ArbitrageDatabase.FAE_NAME
    table_names = listTables(cursor)
    checkTableNameExists(cursor, table_name, table_names)
    # Change this to UPDATE if it already exists
    ArbitrageDatabase.insertFAE(cursor, asset, exchange, proportion_as, proportion_ex)
    disconnect(connect)   

    # FUNCTION: storeFailedMArbitrage
    # INPUT: input_tuple - TODO
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Process input tuple containing data on a failed market arbitrage trade, store values in database.
    def storeFailedMArbitrage(input_tuple):      
        connect, cursor = ArbitrageDatabase.connect()
        timestamp = Helpers.createTimestamp()
        uuid = createUuid("market_arbitrage_f")
        table_name = ArbitrageDatabase.MFAILURETRADES_TABLE_NAME      
        checkTableNameExists(cursor, table_name, ArbitrageDatabase)
        ArbitrageDatabase.insertMAFailure(cursor, timestamp, uuid, *input_tuple)
        disconnect(connect)

    # FUNCTION: storeFailedLArbitrage
    # INPUT: input_tuple - TODO
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Process input tuple containing data on a failed limit arbitrage trade, store values in database.
    def storeFailedLArbitrage(input_tuple):      
        connect, cursor = ArbitrageDatabase.connect()
        timestamp = Helpers.createTimestamp()
        uuid = createUuid("limit_arbitrage_f")
        table_name = ArbitrageDatabase.LFAILURETRADES_TABLE_NAME      
        checkTableNameExists(cursor, table_name, ArbitrageDatabase)
        ArbitrageDatabase.insertLAFailure(cursor, timestamp, uuid, *input_tuple)
        disconnect(connect)
# Gets to replace by UUID
# 
# getError

    # FUNCTION: createTables
    # INPUT: tables - [string, ...]
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Used to iterate over a list of table names and declare the tables in the database
    def createTables(cursor, tables):
        for table in tables:
            ArbitrageDatabase.createTable(cursor, table)

    # FUNCTION: connect
    # INPUT: path - location of file
    # OUTPUT: None
    # DESCRIPTION:
    #   Wrapper function used to easily connect to the desired database 
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'arbitrageDB.sqlite3')
    def connect(path=DEFAULT_PATH):
        try:
            connection = sqlite3.connect(path)
            cursor = connection.cursor()
            return connection,cursor
        except Error as e:
            print(e)
        return None



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

    # FUNCTION: updateBalance
    # INPUT: exchange - string
    #        asset    - string
    #        amount   - float
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Updates the balance of a given exchange/asset pairing in the database.
    def updateBalance(exchange, asset, amount):
        connect, cursor = ArbitrageDatabase.connect()
        table_name = ArbitrageDatabase.ACCOUNT_BALANCES_NAME
        table_names = listTables(cursor)
        checkTableNameExists(cursor, table_name, table_names)
        ArbitrageDatabase.updateBalance(cursor, exchange, asset, amount, table_name)
        disconnect(connect)

    # FUNCTION: updateFAEProportion
    # INPUT: asset      - string
    #        exchange   - string
    #        proportion - string
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Updates the proportion value of an exchange-asset pairing of the FAE.
    def updateFAEProportion(asset, exchange, proportion):
        connect, cursor = ArbitrageDatabase.connect()
        table_name = ArbitrageDatabase.FAE_NAME
        table_names = listTables(cursor)
        checkTableNameExists(cursor, table_name, table_names)
        ArbitrageDatabase.updateFAEProportion(cursor, asset, exchange, proportion)
        disconnect(connect)   

    # FUNCTION: updateDepositAddress
    # INPUT:
    # OUTPUT:
    # DESCRIPTION:
    #   
    def updateDepositAddress(asset, exchange, address):
        connect, cursor = ArbitrageDatabase.connect()
        table_name = ArbitrageDatabase.ASSET_INFO_NAME
        table_names = listTables(cursor)
        checkTableNameExists(cursor, table_name, table_names)
        success_dict = ArbitrageDatabase.updateDepositAddress(cursor, asset, exchange, address)
        disconnect(connect)

    # FUNCTION: updateWithdrawalFee
    # INPUT: 
    # OUTPUT:
    # DESCRIPTION:
    #   
    def updateWithdrawalFee(asset, exchange, withdrawal_fee):
        connect, cursor = ArbitrageDatabase.connect()
        table_name = ArbitrageDatabase.ASSET_INFO_NAME
        table_names = listTables(cursor)
        checkTableNameExists(cursor, table_name, table_names)
        sucess_dict = ArbitrageDatabase.updateWithdrawalFee(cursor, asset, exchange, withdrawal_fee)
        disconnect(connect)

    # FUNCTION: updateWithdrawalTag
    # INPUT: 
    # OUTPUT:
    # DESCRIPTION:
    #   
    def updatewithdrawalTag(asset, exchange, tag):
        connect, cursor = ArbitrageDatabase.connect()
        table_name = ArbitrageDatabase.ASSET_INFO_NAME
        table_names = listTables(cursor)
        checkTableNameExists(cursor, table_name, table_names)
        sucess_dict = ArbitrageDatabase.updateWithdrawalTag(cursor, asset, exchange, withdrawal_tag)
        disconnect(connect)

# FUNCTION: deleteFAE
# INPUT:
# OUTPUT:
# DESCRIPTION:
#   TODO - Don't need delete functions for time being
def deleteFAEentry():
    connect, cursor = ArbitrageDatabase.connect()
    disconnect(connect)   

def deleteFAEentries(pairing, exchanges):
    pass

# FUNCTION: deleteBalance
# INPUT: exchange - string
#        asset    - string
# DESCRIPTION:
#   Removes a balance entry from the database
def deleteBalance(exchange, asset):
    connect, cursor = ArbitrageDatabase.connect()
    success_dict = ArbitrageDatabase.deleteBalance(cursor, exchange, asset)
    disconnect(connect)
    return success_dict

# F: Deletion
#       [trade_values_1, trade_values_2, ... CUTOFF]
#       *restricted by period of time
def deleteFailuresTimeframe(cursor, days, table_name=TRADE_TABLE_NAME):
    one_day = 60*60*24 # seconds
    time = int(time.time() * 1000)
    cutoff = time - (one_day*days)
    sql_s = 'DELETE FROM %s WHERE Time < %s' % cutoff
    cursor.execute(sql_s)
    
# F: Deletion
#       [trade_values_1, trade_values_2, ... CUTOFF]
#       *restricted by period of time
def deleteTradesTimeframe(cursor,days,table_name=TRADE_TABLE_NAME):
    one_day = 60*60*24 # seconds
    time = int(time.time() * 1000)
    cutoff = time - (one_day*days)
    sql_s = 'DELETE FROM %s WHERE Time_stamp < %s' % cutoff
    cursor.execute(sql_s)


# FORM THESE INTO MORE UNIQUE FUNCTIONS
def getAssets(cursor, exchange, table_name=ACCOUNT_BALANCES_NAME):
    sql_s = "SELECT DISTINCT Asset FROM %s WHERE Exchange= ? " % table_name
    cursor.execute(sql_s,(exchange,))
    currencies = cursor.fetchall()
    final_curr = []
    for curr in currencies:
        final_curr.append(curr[0])
    return final_curr


# F: Retrieval
#       [failure_values]
def getFailure(cursor, id_val, table_name=FAILURETRADES_TABLE_NAME):
    sql_s = "SELECT FROM %s WHERE id = ?" % table_name
    cursor.execute(sql_s,(id_var,))
    cols = cursor.fetchall()
    print(cols)
    return cols

# F: Retrieval 
#       [trade_values_1, trade_values_2, ... CUTOFF]
#       *restricted by period of time
def getFailureTimeframe(cursor, days, table_name=FAILURETRADES_TABLE_NAME):
    one_day = 60*60*24 # seconds
    time = int(time.time() * 1000)
    cutoff = time - (one_day*days)
    sql_s = 'SELECT FROM %s WHERE Time < %s' % cutoff
    cursor.execute(sql_s)
    cols = cursor.fetchall()
    print(cols)
    return cols

def getTransfer(cursor, id_value, table_name=BALANCING_HISTORY_NAME):
    sql_s = "SELECT FROM %s WHERE id = ?" % table_name
    cursor.execute(sql_s,(id_val,))
    cols = cursor.fetchall()
    return cols[0]

# FUNCTION: getTransfers
# DESCRIPTION:
#   Gets a list of transfers after a specified date.
def getTransfers(cursor, Time_stamp, table_name=BALANCING_HISTORY_NAME):
    sql_s = "SELECT FROM %s WHERE Time_stamp > ?" % table_name
    cursor.execute(sql_s,(Time_stamp,))
    cols = cursor.fetchall() # list of tuples 
    return cols

# FUNCTION: getDepositAddress
def getDepositAddress(cursor, asset, exchange, table_name=ASSET_INFO_NAME):
    sql_s = "SELECT * FROM %s WHERE Exchange = ? AND Asset = ?" % table_name
    cursor.execute(sql_s,(exchange,asset,))
    cols = cursor.fetchall()
    PrintLibrary.displayVariables(cols, "Deposit Addresses?")
    return cols[0][2]

# FUNCTION: getWithdrawalFee
def getWithdrawalFee(cursor, asset, exchange, table_name=ASSET_INFO_NAME):
    sql_s = "SELECT * FROM %s WHERE Exchange = ? AND Asset = ?" % table_name
    cursor.execute(sql_s,(exchange,asset,))
    cols = cursor.fetchall()
    return cols[0][4]

# FUNCTION: getWithdrawalTag
def getWithdrawalTag(cursor, asset, exchange, table_name=ASSET_INFO_NAME):
    sql_s = "SELECT * FROM %s WHERE Exchange = ? AND Asset = ?" % table_name
    cursor.execute(sql_s,(exchange,asset,))
    cols = cursor.fetchall()
    return cols[0][3]

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

# From printlibrary, possibly deprecating
# FUNCTION: displayKeyVariables
# INPUT: dict  - dictionary
#        header - string (OPTIONAL)
# OUTPUT: N/A
# DESCRIPTION:
#   Takes a dictionary and prints each key/value pairing of the dictionary.
def displayKeyVariables(dict, header=""):
    if header != "":
        print("|- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -|")
        print(" * " + str(header))
        print("  ___________")
    else :
        print("|- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -|")
    for key,value in dict:
        print("  " + str(key) + " - " + str(value))  
# To be deprecated
METRICS_TABLE_NAME = "Metrics"
METRICSFAILURES_TABLE_NAME = "FailureMetrics"
METRICSASSET_TABLE_NAME = "AssetMetrics"
METRICSFAILURESASSET_TABLE_NAME = "AssetFailureMetrics"
POLLING_TABLE_NAME = "RuntimePolling"