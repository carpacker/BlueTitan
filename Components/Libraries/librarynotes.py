# 1. write Store & test...
# 2. Replace store functions in each and test individually
# 3. write get/select & test
# 4. Replace get/select in each and test individually
# 5. SelectfromPeriod/table
# 6. Initializes


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

# EACH needs
# STORE/INSERT
# GET1, GET*, GET*by time
# DELETE1, DELETE*, DELETE*by time
# 

# Stores to replace
#
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