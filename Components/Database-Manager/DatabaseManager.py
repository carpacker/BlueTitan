'''
                                              Database Manager.py

Intention of script is to act as an independent library to access and manager our various databases. Any other scripts
in our program can call this library with all the necessary inputs and make changes to data. Compartamentalizing SQL
calls provides a layer of security between databases and those that intend to interact with said databases. Additionally,
this allows for us to scale our capabilities without needing to edit other parts of the program that have the initial
database management protocol hardcoded.

'''

#                                                  Imports

# External-Imports
import sys
sys.path.append('C:/Users/Carson/Desktop/Coding Projects/Bots/Arbitrage/Libraries')

import os
import sqlite3
import time

# Internal-Imports
from PrintLibrary import PrintLibrary

# Possibly looking to deprecate these general functions to outside DatabaseLibrary
# Possibly looking to deprecate this manager to move all database functions inside a DatabaseLibrary

#                                           SQL Operation Functions

# FUNCTION: commit_w
# INPUT: connect - SQL connection
# OUTPUT: N/A
# DESCRIPTION:
#   Wrapper function for commits
def commitWrite(connect):
    connect.commit()

# FUNCTION: connect
# INPUT: path - location of file
# OUTPUT: None
# DESCRIPTION:
#   Wrapper function used to easily connect to the desired database 
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'MiscDatabase.sqlite3')
def connect(path=DEFAULT_PATH):
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        return connection,cursor
    except Error as e:
        print(e)
    return None

# FUNCTION: deleteTable
# INPUT: cursor     - *
#        table_name - string
# OUTPUT: N/A
# DESCRIPTION:
#   Deletes a table given a cursor for a databse and the table's name
def deleteTable(cursor, table_name):
    sql_s = 'DROP TABLE %s' % table_name
    cursor.execute(sql_s)

# FUNCTION: disconnect
# INPUT: connect - *
# OUTPUT: N/A
# DESCRIPTION:
#   Wrapper for disconnecting from a database
def disconnect(connect):
    connect.commit()
    connect.close()

# FUNCTION: generalQuery
# INPUT: todo
# OUTPUT: varying
# DESCRIPTION:
#   Performs a generalized query over a cursor
def generalQuery(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()

# FUNCTION: listColumns
# INPUT: cursor     - *
#        table_name - string
# OUTPUT: list of strings
# DESCRIPTION:
#   Returns a list of the names of each column in a given table
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
# OUTPUT: table_list which is a representation of all the tables
# DESCRIPTION:
#   Lists the tables in a database.
def listTables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_list = []
    fetched = cursor.fetchall()
    for tup in fetched:
        table_list.append(tup[0])
    return table_list

# FUNCTION: selectColumn
# INPUT: cursor 
#        table_name   - string
#        column_name  - string
#        limit_period - int [will either be number of trades OR a unix timestamp designating the time to start from]
# OUTPUT: tuple
# DESCRIPTION:
#   Returns a tuple from a single column.
# * TODO [NotUrgent] - Make this more robust, for instance 50,000 is arbitrary
def selectColumn(cursor, table_name, column_name, limit_period=None):
    if limit_period < 50000:
        ret_tuple = selectFromTable(cursor, table_name, limit_period, "", [column_name])
    elif limit_period > 50001:
        print("select from period")
        ret_tuple = selectFromTablePeriod(cursor, table_name, limit_period, "", [column_name])
    else:
        ret_tuple = selectFromTable(cursor, table_name, -1, "", [column_name])
    return ret_tuple

# FUNCTION: selectFromTable
# INPUT: table_name - string
#        limit      - int
#        order_by   - string (column to order the list by)
#        columns    - [string, ...]
# OUTPUT: [tuple, ...]
# DESCRIPTION:
#   Returns list of tuples (each tuple represents a row)
# ** In order to return all data from a table, leave out parameter 'columns'
# ** Limit -1 returns all rows
# ** order_by is either "" or the name of a column  
def selectFromTable(cursor, table_name, limit, order_by, columns=None):
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

def selectFromTablePeriod(cursor, table_name, period, order_by, columns=None):
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

    print(sql_s)
    cursor.execute(sql_s)
    result = cursor.fetchall()
    return result

'''
                                           Databases

   ArbitrageDatabase    - Stores all information on arbitrage trading
   MetricsDatabase      - Stores all information on general metrics for the system (currently just arbitrage & profits)
   AssetMetricsDatabase - Stores information for each asset (separate table)
   PollingDatabase      - General table and table for each asset
   MiningDatabase       - Information on mining (results, network difficulty)
   MedianTraderDatabase - Stores all information on median trading

'''

# CLASS: ArbitrageDatabase
class ArbitrageDatabase(object):

    #                                       Tables
    #  
    #   ArbitrageTrades : [Time_stamp, Uuid, Symbol, Total_quantity, Total_btc, Executed_qauntity
    #                       Buy_exchange, Sell_exchange, Avg_buy_rate, Avg_sell_rate, Profit_ratio,
    #                       Profit]
    #       Each entry is a single MarketArbitrage trade
    TRADE_TABLE_NAME = "ArbitrageTrades"
    
    #   FailureTrades : []
    #       Table of failed trades, to be used by other processing systems
    FAILURETRADES_TABLE_NAME = "FailureTrades"

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

    # WRAPPERS: 

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


    # ------------------------------ INITIALIZATION OF TABLES ------------------------------------|
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

    # FUNCTION: createTables
    # INPUT: tables - [string, ...]
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Used to iterate over a list of table names and declare the tables in the database
    def createTables(cursor, tables):
        for table in tables:
            ArbitrageDatabase.createTable(cursor, table)

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
    def insertFailure(cursor, Time_stamp, uuid, Symbol, Total_quantity, Total_btc, Buy_exchange, Sell_exchange, Avg_buy_rate, Avg_sell_rate,
                        Profit_ratio, Profit, Failed_exchange, Stage, Consecutive_fails, table_name="FailureTrades"):
        sql_s = "INSERT INTO %s(Time_stamp,Uuid,Symbol,Total_quantity,Total_btc,Buy_exchange,Sell_exchange,Avg_buy_rate,Avg_sell_rate,Profit_ratio,Profit,Failed_exchange,Stage,Consecutive_fails) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)" % table_name
        cursor.execute(sql_s,(Time_stamp,uuid,Symbol,Total_quantity,Total_btc,Buy_exchange,Sell_exchange,Avg_buy_rate,Avg_sell_rate,Profit_ratio,Profit,Failed_exchange,Stage,Consecutive_fails))
    

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


    # FUNCTION: deleteFAE
    # TODO
    def deleteFAE(cursor, asset, exchange, proportion, table_name=FAE_NAME):
        pass

    # FUNCTION: getFAEProportion
    # TODO... add second one or fleexible
    def getFAEProportion(cursor, asset, exchange, table_name=FAE_NAME):
        sql_s = "SELECT Proportion_as FROM %s WHERE Exchange = ? AND Asset = ?" % table_name
        cursor.execute(sql_s, (exchange, asset,))
        row = cursor.fetchall()
        return row[0][0]



    # --------------------------------------- ERRORS -------------------------------------------
    # F: Insertion
    def insertError(cursor, timestamp, uuid, message, typeOf, stage, table_name=ERROR_TABLE_NAME):
        sql_s = "INSERT INTO %s VALUES (?,?,?,?,?)" % table_name
        cursor.execute(sql_s,(timestamp,uuid,message,typeOf,stage))

    # F: Retrieval
    def getError(cursor, uuid, table_name=ERROR_TABLE_NAME):
        sql_s = "SELECT FROM %s WHERE Uuid = ?" % table_name
        cursor.execute(sql_s,(uuid))

    # F: Retrieval : Multiple by period and/or uuids
    def getErrors():
        # TODO BUT NOT NECESSARY
        pass

    # F: Deletion : Currently not in use
    def deleteError(cursor, table_name=ERROR_TABLE_NAME):
        pass

    # ------------------------- MISC HELPER FUNCTIONS ----------------------------
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

    # FUNCTION: getLastEntry
    # INPUT: cursor     - *
    #        table_name - string
    # OUTPUT: desired entry
    # DESCRIPTION:
    #   Retrieves the last entry in a database.
    def getLastEntry(cursor, table_name):
        sql_s = "SELECT * FROM %s ORDER BY Time_stamp DESC LIMIT 1" % table_name
        cursor.execute(sql_s,)
        entry = cursor.fetchall()
        return entry[0]


# CLASS: MedianTraderDatabase
#   Library of functions used to interact with Median Trading data via SQL.
class MedianTraderDatabase(object):

    # FUNCTION: connect
    # INPUT: path - location of file
    # OUTPUT: None
    # DESCRIPTION:
    #   Wrapper function used to easily connect to the desired database 
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'MedianDB.sqlite3')
    def connect(path=DEFAULT_PATH):
        try:
            connection = sqlite3.connect(path)
            cursor = connection.cursor()
            return connection,cursor
        except Error as e:
            print(e)
        return None

    # FUNCTION: createTable
    # DESCRIPTION:
    #   Declaration of mining tables.

    # TODO-  fill out data typing
    def createTable():
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

    # FUNCTION: createTables
    # INPUT: tables - [string, ...]
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Used to iterate over a list of table names and declare the tables in the database
    def createTables(cursor, tables):
        for table in tables:
            ArbitrageDatabase.createTable(cursor, table)


class MiningDatabase(object):

    MINING_P_TABLE_NAME = "MiningProfits"
    MINING_S_table_NAME = "MiningStatistics"
    table_names = []

    # FUNCTION: connect
    # INPUT: path - location of file
    # OUTPUT: None
    # DESCRIPTION:
    #   Wrapper function used to easily connect to the desired database 
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'MiningDB.sqlite3')
    def connect(path=DEFAULT_PATH):
        try:
            connection = sqlite3.connect(path)
            cursor = connection.cursor()
            return connection,cursor
        except Error as e:
            print(e)
        return None


    # FUNCTION: createTable
    # DESCRIPTION:
    #   Declaration of mining tables.

    # TODO-  fill out data typing
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

    # FUNCTION: createTables
    # INPUT: tables - [string, ...]
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Used to iterate over a list of table names and declare the tables in the database
    def createTables(cursor, tables):
        for table in tables:
            ArbitrageDatabase.createTable(cursor, table)

    def insertProfit():
        pass

    def deleteProfit():
        pass

    def insertStatistic():
        pass

    def deleteStatistic():
        pass

    def insertMetric():
        pass

    def deleteMetric():
        pass


# CLASS: PollingDatabase
#   Library of functions used to interact with polling data via SQL.
class PollingDatabase(object):

    # FUNCTION: connect
    # INPUT: path - location of file
    # OUTPUT: None
    # DESCRIPTION:
    #   Wrapper function used to easily connect to the desired database 
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'PollingDB.sqlite3')
    def connect(path=DEFAULT_PATH):
        try:
            connection = sqlite3.connect(path)
            cursor = connection.cursor()
            return connection,cursor
        except Error as e:
            print(e)
        return None
    table_names = []

    # FUNCTION: createTable
    # DESCRIPTION:
    #   Declaration of mining tables.

    # TODO-  fill out data typing
    def createTable():
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

    # FUNCTION: createTables
    # INPUT: tables - [string, ...]
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Used to iterate over a list of table names and declare the tables in the database
    def createTables(cursor, tables):
        for table in tables:
            ArbitrageDatabase.createTable(cursor, table)



# CLASS: MetricsDatabase
#   Stores all information on general metrics
class MetricsDatabase(object):  

    # FUNCTION: connect
    # INPUT: path - location of file
    # OUTPUT: None
    # DESCRIPTION:
    #   Wrapper function used to easily connect to the desired database 
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'MetricsDB.sqlite3')
    def connect(path=DEFAULT_PATH):
        try:
            connection = sqlite3.connect(path)
            cursor = connection.cursor()
            return connection,cursor
        except Error as e:
            print(e)
        return None

    #                                       Tables
    #  
    #   Metrics : []
    #       todo
    METRICS_TABLE_NAME = "Metrics"

    #   FailureMetrics : []
    #       todo
    METRICSFAILURES_TABLE_NAME = "FailureMetrics"

    #   ProfitMetrics : []
    #       Will be table that specifically tracks profits
    PROFITS_TABLE_NAME = "ProfitMetrics"

    #   LiquidationHistory : []
    #       Tracks liquidation 
    LIQUIDATION_TABLE_NAME = "LiquidationHistory"

    table_names = []

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

    # ------------------------------- METRIC HELPER FUNCTIONS ----------------------------

    # F: Insertion
    def insertMetric(cursor, timestamp, uuid, pairings, initial_balance, end_balance, agg_volume, agg_volume_d, profit_ratio, profit_ratio_d, profit, profit_d, 
                        agg_utilization, agg_utilization_d, agg_quantity, agg_quantity_d, table_name="Metrics"):
        sql_s = "INSERT INTO %s VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)" % table_name
        cursor.execute(sql_s,(timestamp,uuid,pairings, initial_balance, end_balance, agg_volume, agg_volume_d, profit_ratio, profit_ratio_d, 
                                profit,profit_d, agg_utilization, agg_utilization_d, agg_quantity, agg_quantity_d))

    # F: Retrieval : Single by UUID
    def getMetric(cursor, metric_id, table_name="Metrics"):
        sql_s = "SELECT FROM %s WHERE Uuid = ?" % table_name
        cursor.execute(sql_s,(metric_id))
        m_row = cursor.fetchall()
        # Potentially convert to tuple
        return m_row

    # F: Retrieval : Multiple by period and/or UUIDs
    def getMetrics(cursor, period, metric_ids=None, table_name="Metrics"):
        # TODO BUT NOT NECESSARY
        pass

    # F: Deletion : Currently not in use
    def deleteMetric(cursor, timestamp, metric_id, table_name="Metrics"):
        # FINE FOR NOW
        pass

    # ** FAILURES

    # F: Insertion
    def insertFailureMetric(cursor, timestamp, uuid, pairings, profit_ratio, profit_ratio_d, profit, profit_d, agg_volume, agg_volume_d, 
                        agg_utilization, agg_utilization_d, agg_quantity, agg_quantity_d, avg_success_rate, avg_success_rate_d, table_name="FailureMetrics"):
        sql_s = "INSERT INTO %s VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)" % table_name
        cursor.execute(sql_s,(timestamp,uuid,pairings,profit_ratio,profit_ratio_d,profit,profit_d,agg_volume,agg_volume_d,agg_utilization,
                                agg_utilization_d,agg_quantity,agg_quantity_d,avg_success_rate,avg_success_rate_d))

    # F: Retrieval : Single by UUID
    def getMetricFailure(cursor, metric_id, table_name="MetricsFailures"):
        sql_s = "SELECT * FROM %s WHERE Uuid = ?" % table_name
        cursor.execute(sql_s,(metric_id))
        mf_row = cursor.fetchall()
        return mf_row

    # F: Retrieval : Multiple by period and/or UUIDs 
    def getMetricsFailure(cursor, period, metric_ids=None, table_name="MetricsFailures"):
        # This is potentially more copmlicated based on supportedassets
        # TODO BUT NOT NECESSARY
        pass

    # F: Deletion : Currently not in use
    def deleteMetricFailure(cursor, timestamp, metric_id, table_name="MetricsFailures"):
        # FINE FOR NOW
        pass



# Table will be quite big, as such, in the future this database will hold all the asset metric information
class AssetMetricsDatabase(object):
    # FUNCTION: connect
    # INPUT: path - location of file
    # OUTPUT: None
    # DESCRIPTION:
    #   Wrapper function used to easily connect to the desired database 
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'AssetMetricsDB.sqlite3')
    def connect(path=DEFAULT_PATH):
        try:
            connection = sqlite3.connect(path)
            cursor = connection.cursor()
            return connection,cursor
        except Error as e:
            print(e)
        return None

    #                                       Tables
    #  
    #   AssetMetrics : []
    #       TODO
    ASSETMETRICS_TABLE_NAME = "AssetMetrics"

    #   AssetFailureMetrics : []
    #       TODO
    ASSETMETRICSFAILURES_TABLE_NAME = "AssetFailureMetrics"
    table_names = []

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


    # ----------------------------- ASSET METRIC HELPER FUNCTIONS --------------------------    

    # F: Insertion
    def insertAssetMetric(cursor, timestamp, uuid, asset, primary_sell_ex, primary_buy_ex, initial_balance, end_balance,
                            volume, volume_d, profit_ratio, profit_ratio_d, utilization, utilization_d, quantity_trades,
                            quantity_trades_d, table_name="AssetMetrics"):
        sql_s = "INSERT INTO %s VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)" % table_name
        cursor.execute(sql_s,(timestamp, uuid, asset, primary_sell_ex, primary_buy_ex, initial_balance, end_balance,
                            volume, volume_d, profit_ratio, profit_ratio_d, utilization, utilization_d, quantity_trades,
                            quantity_trades_d))

    # F: Retrieval : Single by UUID
    def getAssetMetric(cursor, uuid, table_name="AssetMetrics"):
        sql_s = "SELECT * FROM %s WHERE Uuid = ?" % table_name
        cursor.execute(sql_s,(uuid,))
        ma_row = cursor.fetchall()
        print("DatabaseManager/getAssetMetric", ma_row)
        return ma_row

    # F: Retrieval : Multiple by period and/or UUIDs
    def getAssetMetrics(cursor, asset, period, uuids=None, table_name="AssetMetrics"):
        sql_s = "SELECT * FROM %s WHERE Asset = ?" % table_name
        cursor.execute(sql_s,(asset,))
        ma_row = cursor.fetchall()
        print("DatabaseManager/getAssetMetrics", ma_row)
        return ma_row

    # F: Deletion : Currently not in use
    def deleteAssetMetric(cursor, asset, id, table_name="AssetMetrics"):
        # FINE FOR NOW
        pass

    # ** FAILURES

    # F: Insertion
    def insertAssetMetricFailure(cursor, timestamp, uuid, asset, stage, primary_sell_ex, primary_buy_ex, volume, volume_d,
                                    profit_ratio, profit_ratio_d, quantity_trades, quantity_trades_d, avg_success_rate,
                                    avg_success_rate_d, table_name="AssetFailureMetrics"):
        sql_s = "INSERT INTO %s VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)" % table_name
        cursor.execute(sql_s,(timestamp, uuid, asset, stage, primary_sell_ex, primary_buy_ex, volume, volume_d,
                                    profit_ratio, profit_ratio_d, quantity_trades, quantity_trades_d, avg_success_rate,
                                    avg_success_rate_d))


    # F: Retrieval : Single by UUID
    def getAssetMetricFailure(cursor, uuid, table_name="AssetFailureMetrics"):
        sql_s = "SELECT * FROM %s WHERE Uuid = ?" % table_name
        cursor.execute(sql_s,(uuid,))
        maf_row = cursor.fetchall()
        print("DatabaseManager/getAssetMetricFailure")
        return maf_row

    # F: Retrieval : Multiple by period/UUIDs
    def getAssetFailureMetrics():
        # TODO BUT NOT NECESSARY
        pass

    # F: Deletion : Currently not in use
    def deleteAssetMetricFailure(cursor, asset, id,  table_name="AssetFailureMetrics"):
        pass

