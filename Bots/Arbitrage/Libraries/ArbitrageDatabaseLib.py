import sys
sys.path.append('C:/C-directory/Projects/Work-i/Components/Crypto-API/Exchange_APIs')
sys.path.append('C:/C-directory/Projects/Work-i/Components/Crypto-API/Main')
sys.path.append('C:/C-directory/Projects/Work-i/Components/Database-Manager')
sys.path.append('C:/C-directory/Projects/Work-i/Bots/Arbitrage/')
sys.path.append('C:/C-directory/Projects/Work-i/Bots/Arbitrage/Information_accounting')
sys.path.append('C:/C-directory/Projects/Work-i/Bots/Arbitrage/Libraries')
sys.path.append('C:/C-directory/Projects/Work-i/Bots/Arbitrage/Scripts')

# External-Imports
from collections import defaultdict
import time
import sqlite3

# Internal-Imports
import Helpers
from API import ExchangeAPI
from FeeScraper import FeeScraper
import Arbitrage

# FUNCTION: create_table
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

# FUNCTION: initializeTrades
# INPUT: N/A
# OUTPUT: TODO
# DESCRIPTION:
#   Creates trade database if it doesn't already exist, places a filler trade to signify a new session.
def initializeTrades():
    connect, cursor = ArbitrageDatabase.connect()
    timestamp = Helpers.createTimestamp()
    table_name = ArbitrageDatabase.TRADE_TABLE_NAME
    init_tuple = (timestamp, "", 0, 0, 0, "", "", 0, 0, 0, 0)
    checkTableNameExists(cursor, table_name, ArbitrageDatabase)
    ArbitrageDatabase.insertTrade(cursor, "ArbitrageTrades", timestamp, init_tuple)
    disconnect(connect)

# FUNCTION: initializeFailureTrades
# INPUT: N/A
# OUTPUT: N/A
# DESCRIPTION:
#   Creates failure-trades database if it doesn't already exist, places a filler trade to
#    signify a new session.
def initializeFailureTrades():
    connect, cursor = ArbitrageDatabase.connect()
    timestamp = Helpers.createTimestamp()
    uuid = createSessionNum()
    # Market Arbitrage
    table_name = ArbitrageDatabase.MFAILURETRADES_TABLE_NAME
    checkTableNameExists(cursor, table_name, ArbitrageDatabase)
    init_tuple = ("", 0, 0, "", "", 0, 0, 0, 0, "", "", 0)
    ArbitrageDatabase.insertMFailure(cursor, timestamp, uuid, *init_tuple)
    disconnect(connect)

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
    connect, cursor = ArbitrageDatabase.connect()
    table_name = ArbitrageDatabase.FAE_NAME
    table_names = listTables(cursor)
    checkTableNameExists(cursor, table_name, table_names)
    for fae in fae_list:
        DatabaseLibrary.storeFAE(fae[0], fae[1], fae[2], fae[3])
    disconnect(connect)   

# FUNCTION: initializeTransferHistory
# INPUT: N/A
# OUTPUT: N/A
def initializeTransferHistory():
    connect, cursor = ArbitrageDatabase.connect()
    timestamp = Helpers.createTimestamp()
    table_name = ArbitrageDatabase.BALANCING_HISTORY_NAME
    table_names = listTables(cursor)
    # Add session number to init tuple
    init_tuple = (0, 0, 0, "", "", "", 0, 0, 0)
    checkTableNameExists(cursor, table_name, table_names)
    ArbitrageDatabase.insertTransfer(cursor, timestamp, *init_tuple, table_name)
    disconnect(connect)

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

# TODO
def initializeErrors():
    connect, cursor = ArbitrageDatabase.connect()
    timestamp = Helpers.createTimestamp()
    # Error values: error (text), code(text), type(text)
    input_tuple = ("N/A", "", "initialization")
    table_name = ArbitrageDatabase.ERROR_TABLE_NAME
    table_names = listTables(cursor)
    checkTableNameExists(cursor, table_name, table_names)
    createTable(cursor, table_name, timestamp, *input_tuple)
    disconnect(connect)

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

# FUNCTION: GetAllBalances
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

# CLASS: ArbitrageDatabase
class ArbitrageDatabase(object):

    #                                       Tables
    #  
    #   ArbitrageTrades : [Time_stamp, Uuid, Symbol, Total_quantity, Total_btc, Executed_qauntity
    #                       Buy_exchange, Sell_exchange, Avg_buy_rate, Avg_sell_rate, Profit_ratio,
    #                       Profit]
    #       Each entry is a single MarketArbitrage trade
    TRADE_TABLE_NAME = "ArbitrageTrades"
    
    #   MFailureTrades : []
    #   LFailureTrades : []
    #       Table of failed trades, to be used by other processing systems
    MFAILURETRADES_TABLE_NAME = "MFailureTrades"
    LFAILURESTRADES_TABLE_NAME = "LFailureTrades"

    #   AccountBalances : []
    #       Balances for each asset & exchange
    ACCOUNT_BALANCES_NAME = "AccountBalances"

    #   IntendedFAE : []
    #       TODO
    FAE_NAME = "IntendedFAE"

    #  BalancingHistory : []
    #       todo
    BALANCING_HISTORY_NAME = "BalancingHistory"

    #   AssetInformation : []
    #       Provides information for a specific asset on a specific exchange
    ASSET_INFO_NAME = "AssetInformation"

    #   Errors : []
    #       Database of errors that have occured during the arbitrage process
    ERROR_TABLE_NAME = "Errors"

    # To be deprecated
    METRICS_TABLE_NAME = "Metrics"
    METRICSFAILURES_TABLE_NAME = "FailureMetrics"
    METRICSASSET_TABLE_NAME = "AssetMetrics"
    METRICSFAILURESASSET_TABLE_NAME = "AssetFailureMetrics"
    POLLING_TABLE_NAME = "RuntimePolling"

    table_names = ["ArbitrageTrades", "FailureTrades", "AccountBalances", "IntendedFAE", "BalancingHistory",
                    "AssetInformation"]




    # --------------------------------------- TRADE FUNCTIONS ---------------------------------------
    # F: Insertion
    #       [trade_values]
    def insertTrade(cursor, Time_stamp, uuid, Symbol, Total_quantity, Total_btc, Executed_quantity, Buy_exchange, Sell_exchange, Avg_buy_rate, Avg_sell_rate, Profit_ratio, Profit, table_name="ArbitrageTrades"):
        sql_s = "INSERT INTO %s(Time_stamp,Uuid,Symbol,Total_quantity,Total_btc,Executed_quantity,Buy_exchange,Sell_exchange,Avg_buy_rate,Avg_sell_rate,Profit_ratio,Profit) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)" % table_name
        PrintLibrary.displayKeyVariables((("uuid", uuid),
                                            ("Symbol", Symbol),
                                            ("Total Quantity", Total_quantity),
                                            ("BTC Value", Total_btc)))
        cursor.execute(sql_s,(Time_stamp,uuid,Symbol,Total_quantity,Total_btc,Executed_quantity,Buy_exchange,Sell_exchange,Avg_buy_rate,Avg_sell_rate,Profit_ratio, Profit))


    # F: Deletion
    #       [trade_values_1, trade_values_2, ... CUTOFF]
    #       *restricted by period of time
    def deleteTradesTimeframe(cursor,days,table_name=TRADE_TABLE_NAME):
        one_day = 60*60*24 # seconds
        time = int(time.time() * 1000)
        cutoff = time - (one_day*days)
        sql_s = 'DELETE FROM %s WHERE Time_stamp < %s' % cutoff
        cursor.execute(sql_s)

    # F: Insertion
    #       [failure_values]
    def insertMAFailure(cursor, Time_stamp, uuid, Symbol, Total_quantity, Total_btc, Buy_exchange, Sell_exchange, Avg_buy_rate, Avg_sell_rate,
                        Profit_ratio, Profit, Failed_exchange, Stage, Consecutive_fails, table_name="FailureTrades"):
        sql_s = "INSERT INTO %s(Time_stamp,Uuid,Symbol,Total_quantity,Total_btc,Buy_exchange,Sell_exchange,Avg_buy_rate,Avg_sell_rate,Profit_ratio,Profit,Failed_exchange,Stage,Consecutive_fails) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)" % table_name
        cursor.execute(sql_s,(Time_stamp,uuid,Symbol,Total_quantity,Total_btc,Buy_exchange,Sell_exchange,Avg_buy_rate,Avg_sell_rate,Profit_ratio,Profit,Failed_exchange,Stage,Consecutive_fails))
    
    def insertLAFailure():
        pass

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

    # F: Deletion
    #       [trade_values_1, trade_values_2, ... CUTOFF]
    #       *restricted by period of time
    def deleteFailuresTimeframe(cursor, days, table_name=TRADE_TABLE_NAME):
        one_day = 60*60*24 # seconds
        time = int(time.time() * 1000)
        cutoff = time - (one_day*days)
        sql_s = 'DELETE FROM %s WHERE Time < %s' % cutoff
        cursor.execute(sql_s)

    # ---------------------------------- TRANSFER ---------------------------------
    # FUNCTION: insertTransfer
    # DESCRIPTION:
    #   Insert a balancing transfer into its database

    # TODO, ADD UUID
    def insertTransfer(cursor, time_stamp, transfer_time, buy_exchange, asset, amount, sell_exchange, base_t_asset,
                        base_btc_value, total_btc, fee_btc, buy_withdraw_id, sell_withdraw_id):
        sql_s = "INSERT INTO %s (Time_stamp, Transfer_time, Buy_exchange, Asset, Amount, Sell_exchange, Base_t_asset, Base_btc_value, Total_btc, Fee_btc, Buy_withdraw_id, Sell_withdraw_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)" % table_name
        cursor.execute(sql_s,(time_stamp, transfer_time, buy_exchange, asset, amount, sell_exchange, base_t_asset,
                        base_btc_value, total_btc, fee_btc, buy_withdraw_id, sell_withdraw_id))

    # FUNCTION: getTransfer
    # DESCRIPTION:
    #   Get a specific transfer using an id as the reference key.

    # TODO, FIX THIS
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

    # ------------------------- ASSET INFORMATION -------------------------

    # FUNCTION: insertAssetInformation
    def insertAssetInformation(cursor, asset, exchange, address, withdrawal_tag, withdrawal_fee, usd_fee, table_name=ASSET_INFO_NAME):
        sql_s = "INSERT INTO %s VALUES (?,?,?,?,?,?)" % table_name
        cursor.execute(sql_s,(asset, exchange, address, withdrawal_tag, withdrawal_fee, usd_fee))

    # FUNCTION: insertDepositAddress
    def insertDepositAddress(cursor, asset, exchange, address, table_name=ASSET_INFO_NAME):
        sql_s = "INSERT INTO %s VALUES (?,?,?)" % table_name
        cursor.execute(sql_s,(asset,exchange,address))

    # FUNCTION: updateDepositAddress
    def updateDepositAddress(cursor, asset, exchange, address, table_name=ASSET_INFO_NAME):
        sql_s = "UPDATE %s SET Address = ? WHERE Exchange = ? AND Asset = ?" % table_name
        cursor.execute(sql_s,(address,exchange,asset))

    # FUNCTION: getDepositAddress
    def getDepositAddress(cursor, asset, exchange, table_name=ASSET_INFO_NAME):
        sql_s = "SELECT * FROM %s WHERE Exchange = ? AND Asset = ?" % table_name
        cursor.execute(sql_s,(exchange,asset,))
        cols = cursor.fetchall()
        PrintLibrary.displayVariables(cols, "Deposit Addresses?")
        return cols[0][2]

    # FUNCTION: updateWithdrawalFee
    def updateWithdrawalFee(cursor, asset, exchange, fee, table_name=ASSET_INFO_NAME):
        sql_s = "UPDATE %s SET Withdrawal_fee = ? WHERE Exchange = ? AND Asset = ?" % table_name
        cursor.execute(sql_s, (fee,exchange,asset))

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

    # FUNCTION: updateWithdrawalTag
    def updateWithdrawalTag(cursor, asset, exchange, table_name=ASSET_INFO_NAME):
        sql_s = "UPDATE %s SET Withdrawal_tag = ? WHERE Exchange = ? AND Asset = ?" % table_name
        cursor.execute(sql_s, (fee,exchange,asset))

    # ------------------------- BALANCE HELPER FUNCTIONS ---------------------------

    # FUNCTION: insertBalance
    def insertBalance(cursor, exchange, asset, amount, btc_value, usd_value, table_name=ACCOUNT_BALANCES_NAME):
        sql_s = "INSERT INTO %s(Exchange,Asset,Amount,Btc_value,Usd_value) VALUES (?,?,?,?,?)" % table_name
        cursor.execute(sql_s,(exchange,asset,amount,btc_value,usd_value))

    # FUNCTION: updateBalance
    def updateBalance(cursor, exchange, asset, amount, btc_value, usd_value, table_name=ACCOUNT_BALANCES_NAME):
        sql_s = "UPDATE %s SET Amount = ?, Btc_value = ?, Usd_value = ? WHERE Exchange = ? AND Asset = ?" % table_name
        cursor.execute(sql_s, (amount,exchange,asset,btc_value,usd_value))

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

    # FUNCTION: insertFAE
    def insertFAE(cursor, asset, exchange, proportion_as, proportion_ex, table_name=FAE_NAME):
        sql_s = "INSERT INTO %s(Exchange,Asset,Proportion_as,Proportion_ex) VALUES (?,?,?,?)" % table_name
        cursor.execute(sql_s,(exchange, asset, proportion_as, proportion_ex))

    # FUNCTION: updateFAEProportions
    # Do both of the below
    def updateFAEProportions():
        pass

    # FUNCTION: updateFAEExchangeProportion
    def updateFAEExchangeProportion(cursor, asset, exchange, proportion, table_name=FAE_NAME):
        sql_s = "UPDATE %s SET Proportion_ex = ? WHERE Exchange = ? AND Asset = ?" % table_name
        cursor.execute(sql_s, (proportion, exchange, asset))

    # FUNCTION: updateFAEAccountProportion
    def updateFAEAccountProportion(cursor, asset, exchange, proportion, table_name=FAE_NAME):
        sql_s = "UPDATE %s SET Proportion_as = ? WHERE Exchange = ? AND Asset = ?" % table_name
        cursor.execute(sql_s, (proportion, exchange, asset))

