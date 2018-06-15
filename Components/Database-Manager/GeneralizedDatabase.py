# External-Imports
import sys
import os
import sqlite3
import time
import uuid


# Windows Main Desktop
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Libraries')

# Windows Laptop
# sys.path.append('C:/C-Directory/Projects/BlueTitan/Components/Libraries')
# sys.path.append('C:/C-Directory/Projects/BlueTitan/Components/Crypto-API/Exchange-APIs')
# sys.path.append('C:/C-Directory/Projects/BlueTitan/Bots/Arbitrage/Libraries')

# Linux Desktop
# sys.path.append()

# Main Server
# sys.path.append()

# Internal-Imports
from PrintLibrary import PrintLibrary
import Helpers
# import ArbitrageDatabaseLib

'''                                       Helpers                                   
'''


# FUNCTION: checkTableNameExists
# INPUT: table_name - string
# OUTPUT: N/A
#   Wrapper function to ensure that the table exists before performing an operation.
def checkTableNameExists(cursor, table_name, database):
    table_names = GenDatabaseLibrary.listTables(cursor)
    if table_name not in table_names:
        database.createTable(cursor, table_name)

# FUNCTION: commitWrite
# INPUT: connect - SQL connection
# OUTPUT: N/A
# DESCRIPTION:
#   Wrapper function for committing a write.
def commitWrite(connect):
    connect.commit()

# FUNCTION: connect
# INPUT: path - location of file
# OUTPUT: None
# DESCRIPTION:
#   Wrapper function used to easily connect to the desired database.
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'MiscDatabase.sqlite3')
def connect(path=DEFAULT_PATH):
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        return connection,cursor
    except Error as e:
        print(e)
    return None

# FUNCTION: createUuid
# INPUT: table_name    - string
#        database_name - string
# OUTPUT: int
# DESCRIPTION:
#   Creates a unique identifier for a given trade, metric, transfer, etc.
def createUuid(table_name, database_name):

    # Prototype, inefficient system to create unique identifiers. Future will need
    #  a better solution, as this makes too many database calls in a row.
    table_identifiers = GeneralizedDatabase.getItem(table_name, "table_ientifiers",  "RuntimeDatabase")
    database_identifiers = GeneralizedDatabase.getItem(database_name, "database_identifiers", "RuntimeDatabase")
    uuid_counter = GeneralizedDatabase.getItem("last_uuid", "globals", "RuntimeDatabase")
    
    identifier = table_identifier + database_identifier + str(uuid_counter)
    print(identifier)
    return identifier

# FUNCTION: disconnect
# INPUT: connect - *
# OUTPUT: N/A
# DESCRIPTION:
#   Wrapper for disconnecting from a database
def disconnect(connect):
    connect.commit()
    connect.close()

# FUNCTION: generalQuery
# INPUT: cursor - *
#        query  - string
# OUTPUT: varying
# DESCRIPTION:
#   Performs a general query over a cursor. Input will be a string that represents an 
#    SQL operation.
def generalQuery(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()

'''
                                           Databases

 Algorithms

   arbitrage        - Contains all data pertinent to the 'arbitrage' suite of trading algorithms.
   moving-ave       - Contains all data pertinent to the 'moving-average' suite of trading
                       algorithms.


  Records & Currency Data

   exchange-records - Contains all data that can be classified as a record on an exchange. This
                       includes trades, withdrawals, deposits and transfers. Each exchange gets
                       three tables, one for withdrawals, one for deposits and one for trades.
                       Transfers will be implemented another time.
                       
   historical-data  - Contains a list of tables that contain historical-data for each currency
                       that is designated to be tracked. Each currency has its own table where
                       each entry contains data pertinent to a period in time.
   running-data     - The same as above, but instead data captured by our own program rather
                       than scraped from an external site.
   mining-records   - Contains data pertinent to mining, specifically records and performance.

 
  Metrics & Performance Data

   asset-metrics    - Metrics for each asset
   metrics          - Global metrics

'''

# CLASS: GenDatabaseLibrary
# DESCRIPTION:
#   Library of generic functions for interacting with any database (and tables). Takes databases
#    (and tables, if required) as inputs.
class GenDatabaseLibrary(object):

    # TBD: Global dictionary for UUID matchups, possibly not necessary
    tableNamesUUID = {}
    databaseNamesUUID = {}


    # FUNCTION: buildInitTuple
    # INPUT: table_name    - string
    #        database_name - string
    # OUTPUT: tuple
    # DESCRIPTION:
    #    Creates an initiliazer tuple based on a given table and name. It provides a generic
    #     initializer value for eachd data type
    #  TEXT - ""
    #  REAL - 0
    #  TODO TODO
    def buildInitTuple(table_name, database_name):

        init_list = []
        for x in range (0, num_columns):
            type_col = GenDatabaseLibrary.getColumnType(x, table_name, database_name)
            if type_col == "STRING":
                pass
            elif type_col == "REAL":
                pass
            else:
                pass

        # [0, "", ???]
        PrintLibrary.displayVariables(init_list)
        return init_list
    
    # DATABASE CONTAINER CLASSES
    # DESCRIPTION:
    #    Each database has its own container class which contains functions unique to that
    #     database.
    class ArbitrageDatabase():
        path = 0
        table_names = []
        
        # FUNCTION: createTable
        # INPUT: cursor       - *
        #        table_name   - string
        #        table_tuples - (column_name, column_type, 'NULL'||'NOT NULL')
        # OUTPUT: creates SQL table
        # DESCRIPTION:
        #   Creates a given table based on input. Can create a new table, if trying to create
        #    a specific table it checks for that table to create.
        def createTable(cursor, table_name, table_tuples=None):
            print("ArbitrageDatabase: Initializing Table as ", table_name)
            if table_name == "ArbitrageTrades":
                sql_s = """
                CREATE TABLE %s (
                    Time_stamp text NOT NULL,
                    Uuid text NOT NULL,
                    Symbol text NOT NULL,
                    Total_quantity real NOT NULL,
                    Total_btc real NOT NULL,
                    Executed_quantity real NOT NULL,
                    Buy_exchange text NOT NULL,
                    Sell_exchange text NOT NULL,
                    Avg_buy_rate real NOT NULL,
                    Avg_sell_rate real NOT NULL,
                    Profit_ratio real NOT NULL,
                    Profit real NOT NULL)
                """ % table_name
            elif table_name == "FailureTrades":
                sql_s = """
                CREATE TABLE %s (
                    Time_stamp text NOT NULL,
                    Uuid text NOT NULL,
                    Symbol text NOT NULL,
                    Total_quantity real NOT NULL,
                    Total_btc real NOT NULL,
                    Buy_exchange text NOT NULL,
                    Sell_exchange text NOT NULL,
                    Avg_buy_rate real NOT NULL,
                    Avg_sell_rate real NOT NULL,
                    Profit_ratio real NOT NULL,
                    Profit real NOT null,
                    Failed_exchange text NOT NULL,
                    Stage text NOT NULL,
                    Consecutive_fails integer NOT NULL)
                """ % table_name
            elif table_name == "AccountBalances":
                sql_s = """
                CREATE TABLE %s (
                    id integer PRIMARY KEY,
                    Exchange text NOT NULL,
                    Asset text NOT NULL,
                    Amount real NOT NULL,
                    Btc_value real NOT NULL,
                    Usd_value real NOT NULL)
                """ % table_name       
            elif table_name == "IntendedFAE":
                sql_s = """
                CREATE TABLE %s (
                    Exchange text NOT NULL,
                    Asset text NOT NULL,
                    Proportion_as real NOT NULL, 
                    Proportion_ex real NOT NULL)
                """ % table_name
            elif table_name == "BalancingHistory":
                sql_s = """
                CREATE TABLE %s (
                    Time_stamp integer NOT NULL,
                    Transfer_time integer NOT NULL,
                    Buy_exchange text NOT NULL,
                    Asset  text NOT NULL,
                    Amount  real NOT NULL, 
                    Sell_exchange text NOT NULL,
                    Base_t_asset text NOT NULL,
                    Base_btc_value real NOT NULL,
                    Total_btc real NOT NULL,
                    Fee_btc real NOT NULL,
                    Buy_withdraw_id text NOT NULL,
                    Sell_withdraw_id text NOT NULL)
                """ % table_name
            elif table_name == "AssetInformation":
                sql_s = """
                CREATE TABLE %s (
                    Asset text NOT NULL,
                    Exchange text NOT NULL,
                    Address text NOT NULL,
                    Tag text NOT NULL,
                    Fee real NOT NULL,
                    USDFee real NOT NULL)
                """ % table_name
            elif table_name == "Errors":
                sql_s = """
                CREATE TABLE %s (
                    id integer PRIMARY KEY,
                    Time_stamp text NOT NULL,
                    Error text NOT NULL,
                    Code text NOT NULL,
                    Type text NOT NULL)
                """ % table_name              
            else:
                if table_tuples is None:
                    table_tuples = []
                sql_s = """
                CREATE TABLE %s (
                    id integer PRIMARY KEY)""" % table_name
                for tup in table_tuples:
                    added_s = ",%s %s %s" % tup
                sql_s += added_s
            ArbitrageDatabase.table_names.append(table_name)
            cursor.execute(sql_s)

        # TODO:
        # Initialize each table in the database
        def initializeTables():
            pass
        
        # FUNCTION: initializeBalances
        # INPUT: exchanges - [string, ...] : (list of exchanges to initialize database with)
        # OUTPUT: 'same kind of dictionary that getDbBalances returns'
        # DESCRIPTION:
        #   Initializes the balances for each asset in the used exchanges. index into balance_dict 
        #    using the notation: dict[exchange][asset].
        def initializeBalances(exchanges):
            connect,cursor = ArbitrageDatabase.connect()
            balance_dict = {}
            total_value = 0
            total_btc = 0

            for exchange in exchanges:
                exchange_usd = 0
                exchange_btc = 0
                api_balances = ExchangeAPI.getBalances(exchange)
                if api_balances["success"]:
                    balance_dict[exchange] = defaultdict(int)
                    balances = api_balances["balances"]
                    for asset, values in balances.items():
                        quantity = values["total_balance"]

                        # 1. Calculate USD, BTC value
                        # Hack to work around USDT problem for now
                        if quantity > 0:
                            if asset == "USDT":
                                btc_value = 0
                                usd_value = 0
                            if asset == "BTC":
                                btc_value = quantity
                                usd_value = Helpers.usdValue(asset, quantity, exchange)
                            else: 
                                btc_value = Helpers.btcValue(asset, quantity, exchange)
                                usd_value = Helpers.usdValue(asset, quantity, exchange)

                            # 2. Filter out unattractive/not useful assets 
                            # Accounts for :
                            #   - Unlisted assets
                            #   - Micro-quantities
                            #   - Zero balances
                            if usd_value > 5:
                                total_value += usd_value
                                total_btc += btc_value
                                exchange_usd += usd_value
                                exchange_btc += btc_value

                                # 3. Store desirable results in database, append to return list
                                balance_dict[exchange][asset] = values["total_balance"]
                                DatabaseLibrary.storeBalance(exchange, asset, quantity, btc_value, usd_value)

                DatabaseLibrary.storeBalance(exchange, "ALL", "N/A", exchange_btc, exchange_usd)

            DatabaseLibrary.storeBalance("ALL", "ALL", "N/A", total_btc, total_value)
            balance_dict["ALL"] = defaultdict(int)
            balance_dict["ALL"]["total_value_usd"] = total_value
            balance_dict["ALL"]["total_value_btc"] = total_btc
            disconnect(connect)
            print(balance_dict)
            return balance_dict

        # FUNCTION: initializeFAE
        # INPUT: fae_list - [(asset, exchange, proportion), ...]
        # OUTPUT: N/A
        # DESCRIPTION:
        #   Purpose is to fill up fae table with our currently used asset/exchanges
        def initializeFAE(fae_list):
            for fae in fae_list:
                DatabaseLibrary.storeFAE(fae[0], fae[1], fae[2], fae[3])


        # FUNCTION: initializeAssetInfoes
        # INPUT: exchanges - list of exchanges used
        #        pairing   - list of pairings used
        # OUTPUT: list of (exchange, asset) where the request failedA
        # DESCRIPTION:
        #   Goes through a list of pairings & exchanges and fills up the depositaddress database
        #    Initializes the database with deposit addresses.
        def initializeAssetInfo(assets, exchanges):
            connect, cursor = ArbitrageDatabase.connect()
            errors = []
            table_name = ArbitrageDatabase.ASSET_INFO_NAME
            table_names = listTables(cursor)
            checkTableNameExists(cursor, table_name, table_names)
            print(assets)
            print(exchanges)

            for asset in assets:
                time.sleep(1)
                for exchange in exchanges:
                    # DICT1: deposit address, withdrawaltag(for some currencies only)
                    dict1 = ExchangeAPI.getDepositAddress(exchange, asset) 
                    if dict1["success"]:

                        address = dict1["address"]
                        if dict1["withdrawal_tag"] != None:
                            withdrawal_tag = dict1["withdrawal_tag"]
                        else: 
                            withdrawal_tag = ""

                        if exchange == "binance":
                            withdrawal_fee = FeeScraper.getFee(exchange, asset)
                            withdrawal_tag = dict1["withdrawal_tag"] 
                            usd_value = Helpers.usdValue(asset, withdrawal_fee)
                        else:
                            dict2 = ExchangeAPI.getCurrencies(exchange)
                            withdrawal_fee = dict2["currencies"][asset]["transaction_fee"]
                            withdrawal_tag = ""
                            usd_value = Helpers.usdValue(asset, withdrawal_fee)
                        ArbitrageDatabase.insertAssetInformation(cursor, asset, exchange, address, withdrawal_tag, withdrawal_fee, usd_value)
                    else:
                        errors.append((exchange,asset)) 
            disconnect(connect)
            return errors
        
        # FUNCTION: getPairings
        # INPUT: exchange - string
        # OUTPUT: list of strings [pairing_one, ...]
        # DESCRIPTION:
        #   Outputs list of traded pairings by the program on a given exchange 
        #    based on the database in use.
        # TODO - same function but API.
        def getPairings():
            pass

        # FUNCTION: getWithdrawalFee
        # INPUT: asset      - string
        #        exchange   - string
        #        type_value - TODO
        # OUTPUT: float
        # DESCRIPTION: 
        #   Grabs the withdrawal fee for a given asset on a given exchange from the
        #    asset information database.
        def getWithdrawalFee(asset, exchange, type_value = ""):
            connect, cursor = ArbitrageDatabase.connect()
            table_name = ArbitrageDatabase.ASSET_INFO_NAME
            table_names = listTables(cursor)
            checkTableNameExists(cursor, table_name, table_names)
            fee = ArbitrageDatabase.getWithdrawalFee(cursor, asset, exchange)
            if type_value == "BTC":     
                fee = Helpers.btcValue(asset, fee, exchange)
            disconnect(connect)
            return fee

        # FUNCTION: getBalance
        # INPUT: exchange - string
        #        asset    - string
        # OUTPUT: float
        # DESCRIPTION:
        #   Retrieves a balance for a given asset from the balance database.
        # *If it returns -1, its unavailable
        def getBalance(asset, exchange, type_value=""):
            connect, cursor = ArbitrageDatabase.connect()
            balance = ArbitrageDatabase.getBalanceAsset(cursor, asset, exchange)
            if type_value == "BTC":
                balance = ArbitrageDatabase.getBalanceBTCVal(cursor, asset, exchange)
            elif type_value == "USD":
                balance = ArbitrageDatabase.getBalanceUSDVal(cursor, asset, exchange)
            disconnect(connect)
            return balance  

        # FUNCTION: getBalances
        # * TODO flip assets and exchange for STOREBALANCE, UPDATEBALANCE, GETBALANCES
        def getBalances(exchange, assets, cursor=None):
            if cursor == None:
                connect, cursor = ArbitrageDatabase.connect()
                balance_dict = {}
                for asset in assets:
                    balance_dict[asset] = ArbitrageDatabase.getBalanceAll(cursor, asset, exchange)
                disconnect(connect)
                return balance_dict
            else:
                balance_dict = {}
                for asset in assets:
                    balance_dict[asset] = ArbitrageDatabase.getBalanceAll(cursor, asset, exchange)
                return balance_dict

        def getBalanceTotal(type_a): 
            connect, cursor = ArbitrageDatabase.connect()
            if type_a == "BTC":
                value = ArbitrageDatabase.getBalanceBTCVal(cursor, 'ALL', 'ALL')
            elif type_a == "USD":
                value = ArbitrageDatabase.getBalanceUSDVal(cursor, 'ALL', 'ALL')

            print("total", value)
            return value

        # FUNCTION: getAllBalances
        # INPUT: exchanges - [string, ...]
        # OUTPUT: dictionary of balances - {TODO}
        # DESCRIPTION:
        #   Retrieves all the balances from the exchanges, includes a total balance calculation
        def getAllBalances(exchanges):
            connect,cursor = ArbitrageDatabase.connect()
            # TODO, check database exists shit

            balance_dict = {}
            for exchange in exchanges:
                balance_dict[exchange] = defaultdict(lambda: (0,0,0))
                quantity_list = ArbitrageDatabase.getCurrenciesAmounts(cursor,exchange)
                for tup in quantity_list:
                    balance_dict[exchange][tup[0]] = (tup[1], tup[2], tup[3])

            # # Retrive values for totals
            total_value_usd = DatabaseLibrary.getBalance("ALL", "ALL", "USD")
            total_value_btc = DatabaseLibrary.getBalance("ALL", "ALL", "BTC")
            balance_dict["ALL"] = defaultdict(int)
            balance_dict["ALL"]["total_value_usd"] = total_value_usd
            balance_dict["ALL"]["total_value_btc"] = total_value_btc
            return balance_dict

    class AssetMetricsDatabase():
        path = os.path.join(os.path.dirname(__file__), 'AssetMetricsDB.sqlite3')

        def createTable(cursor, table_name, table_tuples=None):
            if table_name == "AssetMetrics":
                sql_s = """
                CREATE TABLE %s (                
                    Time_stamp text NOT NULL,
                    Uuid text NOT NULL,
                    Asset text NOT NULL,
                    Primary_sell_ex text NOT NULL,
                    Primary_buy_ex text NOT NULL,
                    Initial_balance real NOT NULL,
                    End_balance real NOT NULL,
                    Volume real NOT NULL,
                    Volume_delta real NOT NULL,
                    Profit_ratio real NOT NULL,
                    Profit_ratio_delta real NOT NULL,
                    Utilization real NOT NULL,
                    Utilization_delta real NOT NULL, 
                    Quantity_trades real NOT NULL,
                    Quantity_trades_delta real NOT NULL)
                """ % table_name        
            elif table_name == "AssetFailureMetrics":
                sql_s = """
                CREATE TABLE %s (                
                    Time_stamp text NOT NULL,
                    Uuid text NOT NULL,
                    Asset text NOT NULL,
                    Stage text NOT NULL,
                    Primary_sell_ex text NOT NULL,
                    Primary_buy_ex text NOT NULL,
                    Volume real NOT NULL,
                    Volume_delta real NOT NULL,
                    Profit_ratio real NOT NULL,
                    Profit_ratio_delta real NOT NULL,
                    Quantity_trades_f real NOT NULL,
                    Quantity_trades_f_delta real NOT NULL,
                    Avg_success_rate real NOT NULL,
                    Avg_success_rate_delta real NOT NULL)
                """ % table_name
            else:
                if table_tuples is None:
                    table_tuples = []
                sql_s = """
                CREATE TABLE %s (
                    id integer PRIMARY KEY)""" % table_name
                for tup in table_tuples:
                    added_s = ",%s %s %s" % tup
                sql_s += added_s
            ArbitrageDatabase.table_names.append(table_name)
            cursor.execute(sql_s)


    # CLASS: ExchangeRecords
    class ExchangeRecords():
        path = 0
        table_names = []

    # CLASS: HistoricalDatabase
    class HistoricalDatabase():
        path = 0
        table_names = []
        
    # CLASS: MADatabase
    class MADatabase():
        path = 0
        table_names = []

    # CLASS: MetricsDatabase
    class MetricsDatabase():
        
        def createTable(cursor, table_name, table_tuples=None):
            if table_name == "Metrics":
                sql_s = """
                CREATE TABLE %s (
                    Time_stamp text NOT NULL,
                    Uuid text NOT NULL,
                    Pairings text NOT NULL,
                    Initial_balance real NOT NULL,
                    End_balance real NOT NULL,
                    Volume real NOT NULL,
                    Volume_delta real NOT NULL,
                    Profit_ratio real NOT NULL,
                    Profit_ratio_delta real NOT NULL,
                    Profit real NOT NULL,
                    Profit_delta real NOT NULL,
                    Utilization real NOT NULL,
                    Utilization_delta real NOT NULL,
                    Quantity_trades real NOT NULL,
                    Quantity_trades_delta real NOT NULL)
                """ % table_name
            elif table_name == "FailureMetrics":
                sql_s = """
                CREATE TABLE %s (
                    Time_stamp text NOT NULL,
                    Uuid text NOT NULL,
                    Pairings text NOT NULL,
                    Volume real NOT NULL,
                    Volume_delta real NOT NULL,
                    Profit_ratio real NOT NULL,
                    Profit_ratio_delta real NOT NULL,
                    Utilization real NOT NULL,
                    Utilization_delta real NOT NULL, 
                    Quantity_trades_f real NOT NULL,
                    Quantity_trades_f_delta real NOT NULL,
                    Quantity_stage1 real NOT NULL,
                    Quantity_stage2 real NOT NULL,
                    Avg_success_rate real NOT NULL,
                    Avg_success_rate_delta real NOT NULL)
                """ % table_name   
            elif table_name == "ProfitMetrics":
                pass
            elif table_name == "LiquidationHistory":
                pass
            else:
                if table_tuples is None:
                    table_tuples = []
                sql_s = """
                CREATE TABLE %s (
                    id integer PRIMARY KEY)""" % table_name
                for tup in table_tuples:
                    added_s = ",%s %s %s" % tup
                sql_s += added_s
            ArbitrageDatabase.table_names.append(table_name)
            cursor.execute(sql_s)

        # FUNCTION: initializeTables
        def initializeTables(self):
            for table in self.table_names:
                pass
        
    # CLASS: MiningDatabase
    # createTable(), 
    class MiningDatabase(object):
        path = 0
        table_names = []

        # FUNCTION: createTable
        def createTable(cursor, table_name, table_tuples=None):
            if table_name == "MiningProfits":
                sql_s = """
                CREATE TABLE %s (
                    Time_stamp text NOT NULL,
                    Mining_pool text NOT NULL,
                    Primary text NOT NULL,
                    Mined_primary real NOT NULL,
                    Secondary text NOT NULL,
                    Mined_secondary real NOT NULL)
                """ % table_name    
            elif table_name == "MiningStatistics":
                sql_s = """
                CREATE TABLE %s (
                    Time_stamp text NOT NULL,
                    Eth_difficulty real NOT NULL,
                    Zec_difficulty real NOT NULL,
                    Sc_difficulty real NOT NULL,
                    Dcr_difficulty real NOT NULL)
                """ % table_name   
            elif table_name == "MiningMetrics":
                sql_s = """
                CREATE TABLE %s (
                    Time_stamp text NOT NULL,
                    Mining_pool text NOT NULL,
                    Primary text NOT NULL,
                    Mined_primary real NOT NULL,
                    Secondary text NOT NULL,
                    Mined_secondary real NOT NULL)
                """ % table_name               
            else:
                if table_tuples is None:
                    table_tuples = []
                sql_s = """
                CREATE TABLE %s (
                    id integer PRIMARY KEY)""" % table_name
                for tup in table_tuples:
                    added_s = ",%s %s %s" % tup
                sql_s += added_s
            ArbitrageDatabase.table_names.append(table_name)
            cursor.execute(sql_s)

        # FUNCTION: initializeTables
        def initializeTables():
            pass

    # CLASS: MiningDatabase
    class MiningDatabase():
        pass

    # CLASS: RunningDatabase
    class RunningDatabase():
        pass

    # CLASS: RuntimeDatabase
    class RuntimeDatabase():
        pass

    # CLASS VARIABLE: databases
    # DESCRIPTION:
    #    Dictionary to access the database object
    databases = {
        "ArbitrageDatabase" : GeneralizedDatabase.ArbitrageDatabase,
        "MetricsDatabase" : GeneralizedDatabase.MetricsDatabase,
        "AssetMetricsDatabase" : GeneralizedDatabase.AssetMetricsDatabase,
        "RuntimeDatabase" : GeneralizedDatabase.RuntimeDatabase,
        "HistoricalDatabase" : GeneralizedDatabase.HistoricalDatabase,
        "MiningDatabase" : GeneralizedDatabase.MiningDatabase,
        "ExchangeRecords" : GeneralizedDatabase.ExchRecordsDtabase,
        "RunningDatabase" : GeneralizedDatabase.RunningDatabase,
        "MADatabase" : GeneralizedDatabase.MADatabase
    }
    
    # FUNCTION: createTable
    # INPUT: table_name    - string
    #        database_name - string
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Generic function for creating a table in a database.
    def createTable(table_name, database_name, columns=""):
        database = databases[database_name]
        for table in tables:
            database.createTable(cursor, table)

    # FUNCTION: createTable
    # INPUT: cursor   - *
    #        tables   - [string, ...]
    #        database - Database
    #        columns  - TODO
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Generic function for creating multiple tables in a database. Iterates over 
    #    a list of table names and declare the tables in the database
    def createTables(cursor, tables, database, columns=""):
        for table in tables:
            database.createTable(cursor, table)

    # FUNCTION: deleteTable
    # INPUT: cursor     - *
    #        table_name - string
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Deletes a table given a cursor for a databse and the table's name
    def deleteTable(cursor, table_name):
        sql_s = 'DROP TABLE %s' % table_name
        cursor.execute(sql_s)

    # FUNCTION: initializeTables
    # INPUT: tables   - [string, ...]
    #        database - either string or database object (TODO)
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Executes the initialization of all tables in a given databases.
    def initializeDatabase(self, database_name):
        # 1. Connect to database based on name
        database = self.database_paths[database_name]
        connect, cursor = connect(database)
        
        # 3. Call initialize function using global dictionary
        database.initializeTables()
        disconnect(connect)

    # FUNCTION: initializeDatabases
    # INPUT: tables    - [string, ...]
    #        assets    - [string, ...]
    #        exchanges - [string, ...]
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Initializes all of the tables in each database in the system.
    def initializeDatabases(database_names):
        for database_name in databases_names:
            GenDatabaseLibrary.initializeDatabase(database_name)

    # FUNCTION: cleanDatabase
    # INPUT: tables     - [string, ...]
    #        exceptions - [string, ...] 
    # OUTPUT: list of tables cleaned in database
    # DESCRIPTION
    #   Used to clean a database's tables minus exceptions.
    def cleanDatabase(database_nameles, exceptions=[""]):
        connect, cursor = database.connect()

        # Use regular expression to find difference of two lists
        list_clean = list(set(tables).difference(set(exceptions)))
        for table in list_clean:
            try:
                deleteTable(cursor, table, database_name)
            except sqlite3.OperationalError:
                pass
            database.createTable(cursor, table, database_name)
        disconnect(connect)
    return list_clean
                             
    #
    def buildStringStore(cursor, table_name):
        # 1. List columns
        columns = GenDatabaseLibrary.listColumns(cursor, table_name)
        num_columns = len(columns)

        # 2. Build string based on column names and number of columns
        sql_q = "("
        for value in range(0, num_columns):
            sql_q += "?,"
        sql_q = sql_q[:-1]
        sql_q += ")"

        # 3. (?, ...) where number of elements is equal to number of columns.
        sql_s = "INSERT INTO %s(" % table_name
        for column in columns:
            sql_s += column + ","
        sql_s = sql_s[:-1]
        sql_s += ") VALUES " + sql_q
        return sql_s

    # FUNCTION: storeEntry
    # INPUT: data          - tuple, (item, ...)
    #        table_name    - string
    #        database_name - string
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Generic function for storing an entry into a table in a database.
    def storeEntry(data, table_name, database_name):
        # Set database, initializes variables, check table exists
        database_path = database_paths[database_name]
        timestamp = int(time.time() * 1000)
        uuid = createUuid(table_name, database_name)
        connection, cursor = connect(database_path)
        checkTableNameExists(cursor, table_name, database_name)
        # Build SQL execution string, execute and then disconnect
        sql_s = GenDatabaseLibrary.buildStringStore(cursor, table_name)
        PrintLibrary.displayVariable(sql_s, "SQL string")
        cursor.execute(sql_s,data)
        disconnect(connection)

    # FUNCTION: storeEntries
    # INPUT: data - list [(data, ...), ...]
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Generic function for storing multiple entries into a table in a database.
    def storeEntries(data, table_name, database_name):

        # Set database, initializes variables, check table exists
        database_path = database_paths[database_name]
        timestamp = int(time.time() * 1000)
        uuid = createUuid(table_name, database_name)
        connection, cursor = connect(database_path)
        checkTableNameExists(cursor, table_name, database_name)

        # For each tuple in data, build SQL execution string, execute and then disconnect
        for value in data:
            sql_s = GenDatabaseLibrary.buildStringStore(cursor, table_name)
            PrintLibrary.displayVariable(sql_s, "SQL string")
            print(value)
            cursor.execute(sql_s,value)
        disconnect(connection)

    # FUNCTION: retrieveEntry
    # INPUT: TBD
    # OUTPUT: (V1, ..., Vn) where n is number of columns
    # DESCRIPTION:
    #	Accesses a table in a database and pulls a row from the database. There
    #    are two options to access the entry. The first is by a unique identifier
    #    (uuid). The second is by a list of variables/values, and the function
    #    attempts to find the entry using these as a key.
    def getEntry(self, data_uuid, table_name=None, database_name=None):
        # Set database, initializes variables, check table exists
        print(type(data_uuid))
        if data_uuid == 'list':
            database_path = database_paths[database_name]
            timestamp = int(time.time() * 1000)
            uuid = createUuid(table_name, database_name)
            connection, cursor = connect(database_path)
            checkTableNameExists(cursor, table_name, database_name)
        elif data_uuid == 'string':
            # Grab table_name database_name based on uuid
            table_name = self.tableNamesUuid[uuid[0]]
            database_name = self.databaseNamesUuid[uuid[1]]
            database_path = database_paths[database_name]
            timestamp = int(time.time() * 1000)
            uuid = createUuid(table_name, database_name)
            connection, cursor = connect(database_path)
            checkTableNameExists(cursor, table_name, database_name)
            data_uuid = [data_uuid]
        else:
            # TODO, better error handling
            return 'error'
        sql_s = GenDatabaseLibrary.selectEntry(table_name, data_uuid)
        print(sql_s)
        cursor.execute(sql_s, data_uuid)

    # FUNCTION: getEntries
    # INPUT:
    # OUTPUT: [(*entry), ...]
    # DESCRIPTION:
    #   Retrieves multiple entries. Various different methods are possible to
    #    determine what entries to return. TODO
    def getEntries():
        
        if columns is not None:
            col_s = ",".join(columns)
            sql_s = "SELECT %s FROM %s" % (col_s, table_name)
            if limit > -1:
                sql_s += " LIMIT %s" % limit
            if order_by is not "":
                sql_s += " ORDER BY %s" % order_by
            cursor.execute(sql_s)
            result = cursor.fetchall()
            return result
        sql_s ="SELECT * FROM %s" % table_name
        if limit > -1:
                sql_s += " LIMIT %S" % limit
        if order_by is not "":
                sql_s += " ORDER BY %s" % order_by
        cursor.execute(sql_s)
        result = cursor.fetchall()
        return result
    # def selectFromTablePeriod(cursor, table_name, period, order_by, columns=None):
        print("TIMESTAMP BASE", period)
        if columns is not None:
            col_s = ",".join(columns)
            sql_s = "SELECT %s FROM %s WHERE Time_stamp > %s" % (col_s,table_name,period)
            print(sql_s, "SQL string")
            if order_by is not "":
                sql_s += " ORDER BY %s" % order_by
            cursor.execute(sql_s)
            result = cursor.fetchall()
            return result
        sql_s = "SELECT FROM %s WHERE Time_stamp > %s" % (col_s,table_name, period)
        if order_by is not "":
            sql_s += " ORDER BY %s" % order_by



    # FUNCTION: selectDistinct
    def selectDistinct():
        pass
    
    # FUNCTION: selectEntry
    # INPUT: table_name - string
    #        data       - list
    # OUTPUT: string
    # DESCRIPTION:
    #   Builds selection string.
    def selectEntry(table_name, data):
        sql_s = "SELECT * FROM %s WHERE " % table_name
        for value in data:
            sql_s += "%s = ? AND " % value
        sql_s = sql_s[:-4]
        return sql_s

    # FUNCTION: getLastEntry
    # INPUT: cursor     - *
    #        table_name - string
    # OUTPUT: desired entry
    # DESCRIPTION:
    #   Retrieves the last entry in a database. Uses timestamp instead of internal
    #    id, assumes ascending order based on timestamp.
    def getLastEntry(table_name, database_name):
        # Edit/fix this
        database_path = database_paths[database_name]
        timestamp = int(time.time() * 1000)
        uuid = createUuid(table_name, database_name)
        connection, cursor = connect(database_path)
        checkTableNameExists(cursor, table_name, database_name)
        sql_s = "SELECT * FROM %s ORDER BY Time_stamp DESC LIMIT 1" % table_name
        cursor.execute(sql_s,)
        entry = cursor.fetchall()
        return entry[0]

    # FUNCTION: updateEntry 
    # INPUT: data_uuid     - [] OR []
    #        input_val     - [value1, value2, ...]
    #        table_name    - string
    #        database_name - string
    # OUTPUT: TBD
    # DESCRIPTION:
    #   Effectively replaces an entry with new values. It doesn't necessitate that every value
    #    is updated, but it will check to update each item.
    def updateEntry(data_uuid, input_val, table_name, database_name):
        pass

    # FUNCTION: updateEntries
    # INPUT: data_uuid     - [] OR []
    #        input_val     - [value1, value2, ...]
    #        table_name    - string
    #        database_name - string
    # OUTPUT: TBD
    # DESCRIPTION:
    #   Replaces multiple entries with new values. Similar to update entry, but with lists
    #    as inputs.
    def updateEntries(data_uuid, input_val, table_name, database_name):
        pass

    # FUNCTION: getItem
    # INPUT:
    # OUTPUT:
    # DESCRIPTION:
    #   Retrieves a single item from a
    def getItem(data_uuid, column, table_name, database_name):
        pass

    # FUNCTION: getItems
    # INPUT: data_uuid -
    #
    # OUTPUT: tuple [data1, ...]
    # DESCRIPTION:
    #   Retrieves multiple items from an entry, designated by the column names.
    def getItems(data_uuid, columns, table_name, database_name):
        pass

    # FUNCTION: updateItem
    # INPUT: 
    # OUTPUT: 
    # DESCRIPTION:
    #   Updates an item using UUID or data as a reference to access the entry.
    def updateItem(data_uuid, input_val, column, table_name, database_name):
        pass

    # FUNCTION: updateItems
    # INPUT: 
    # OUTPUT: 
    # DESCRIPTION:
    #   Updates multiple items (column values in an entry) using UUID or data as a reference
    #    to access the entry.
    def updateItems(data_uuid, input_val, columns, table_name, database_name):
        pass

    # FUNCTION: getColumn
    # INPUT: table_name    - string
    #        database_name - string
    #        column        - string
    # KWARGS: limit  - int,  [how many entries to return]
    #         period - tuple (start_time, end_time), in UNIX timestamp
    # OUTPUT: list
    # DESCRIPTION:
    #   Retrieves an entire column from a table in a datbase. kwargs limit and period can
    #    be used to restrict the number of values to return.
    # WARNING: heavy load on time, very slow
    def getColumn(table_name, database_name, **kwargs):
        # 1. Check if attempting use period
        # 2. Check the quantity of entries to grab
        # 3. If neither, grab all
        
    # FUNCTION: getColumn
    # INPUT: table_name    - string
    #        database_name - string
    #        columns       - [string, ...]
    # KWARGS:
    # OUTPUT:
    # DESCRIPTION:
    #   Performs multiple getColumn() calls in order to retrieve multiple columns.
    # WARNING: heavy load on time, very slow
    def getColumns(table_name, database_name, **kwargs):
        pass

    # FUNCTION: deleteEntry
    # INPUT: data_uuid 
    #        table_name    - string
    #        database_name - string
    # OUTPUT: N/A
    # DESCRIPTION:
    #   TODO: will be similar to getEntry
    def deleteEntry(data_uuid, table_name=None, database_name=None):
        pass

    # FUNCTION: deleteEntries
    # INPUT: 
    # OUTPUT:
    # DESCRIPTION:
    #   TODO: will be similar to getEntries
    def deleteEntries():
        
        # Below is reference for time based
        one_day = 60*60*24 # seconds
        time = int(time.time() * 1000)
        cutoff = time - (one_day*days)
        sql_s = 'DELETE FROM %s WHERE Time < %s' % cutoff
        cursor.execute(sql_s)

    # FUNCTION: listColumns
    # INPUT: cursor     - *
    #        table_name - string
    # OUTPUT: list of strings
    # DESCRIPTION:
    #   Returns a list of the names of each column in a given table.
    def listColumns(cursor, table_name):
        sql_s = "PRAGMA table_info('%s')" % table_name
        cols_list = []
        cursor.execute(sql_s)
        col_tups = cursor.fetchall()
        for tup in col_tups:
            cols_list.append(tup[1])
        return cols_list

    # FUNCTION: listTables
    # INPUT: cursor
    # OUTPUT: table_list which is a representation of all the tables.
    # DESCRIPTION:
    #   Lists the tables in a database.
    def listTables(cursor):
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        table_list = []
        fetched = cursor.fetchall()
        for tup in fetched:
            table_list.append(tup[0])
        return table_list
