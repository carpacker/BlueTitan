# External-Imports
import sys
import os
import sqlite3
import time

# Windows Main Desktop
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Libraries')

# Windows Laptop
# sys.path.append('C:/C-Directory/Projects/BlueTitan/Components/Libraries')
# sys.path.append('C:/C-Directory/Projects/BlueTitan/Components/Crypto-API/Exchange-APIs')
# sys.path.append('C:/C-Directory/Projects/BlueTitan/Bots/Arbitrage/Libraries')

# Internal-Imports
from PrintLibrary import PrintLibrary
import Helpers
# import ArbitrageDatabaseLib

############################## HELPERS ###########################

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
    # Use letter at beginning to designate what type of thing it is 
    return 0

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

# ----------------------------- GLOBAL DATABASE DICTIONARIES --------------------------------------
# DATABASES:
#   arbitrage        -
#   asset-metrics  	 -
#   exchange-records -
#   historical-data	 -
#   metrics          -
#   mining-records   -
# DESCRIPTION:
#   In order to initialize our databases with ease, base information about each (number of columns,
#    typing and names) are stored in a dictionary which is accessed by the database library.

trades_info = {'initialize' : 0}

arbitrage_tables = {'trades' : trades_info}
assetMetrics_tables = {'asset_metrics' : asset_metrics_info}
exchangeRecords_tables = {}
historicalData_tables = {}
metrics_tables = {'metrics' : metrics_info2444  }
miningRecords_tables = {}

databases = {'arbitrage' : arbitrage_tables,	
            'asset_metrics' : assetMetrics_tables,
            'exchange_records' : exchangeRecords_tables,
            'historical_data' : historicalData_tables,
            'metrics' : metrics_tables,
            'mining_records' : miningRecords_tables
            }

database_paths = {"ArbitrageDatabase" : os.path.join(os.path.dirname(__file__), 'arbitrageDB.sqlite3'),
                    "MetricsDatabase" : os.path.join(os.path.dirname(__file__), 'arbitrageDB.sqlite3')}

tableNamesUuid = {}
databaseNamesUuid = {}

# CLASS: GenDatabaseLibrary
# DESCRIPTION:
#   Library of generic functions for interacting with any database (and tables). Takes databases
#    (and tables, if required) as inputs.
class GenDatabaseLibrary(object):

    # FUNCTION: createTable
    # INPUT: 
    # OUTPUT:
    # DESCRIPTION:
    #   Generic function for creating a table in a database.
    def createTable():
        # Check for tables that are already set
        pass
        # Otherwise, fill in with input parameters.

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
        # IF no input parameters [assume it is handled in createTable]
        if columns == "":
            for table in tables:
                database.createTable(cursor, table)

        # OTHERWISE, create tables using input parameters
        else:
            pass

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
    def initializeDatabase(database_name):
        # 1. Connect to database based on name
        database = tbd[database_name]
        connect, cursor = database.connect()
        # 2. Create tables (???)
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
    def getEntry(data_uuid, table_name=None, database_name=None):
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
            table_name = tableNamesUuid[uuid[0]]
            database_name = databaseNamesUuid[uuid[1]]

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
    # INPUT: 
    # OUTPUT: 
    # DESCRIPTION:
    #   Effectively replaces an entry with new values. It doesn't necessitate that every value is updated, but it
    #    will check to update each item.
    def updateEntry(data_uuid, input, table_name, database_name):
        pass

    # FUNCTION: updateEntries
    # INPUT: 
    # OUTPUT: 
    # DESCRIPTION:
    #   
    def updateEntries(data_uuid, input, table_name, database_name):
        pass

    # FUNCTION: getItem
    # INPUT:
    # OUTPUT:
    # DESCRIPTION:
    #   
    def getItem(data_uuid, column, table_name, database_name):
        pass

    # FUNCTION: getItems
    # INPUT: 
    # OUTPUT: 
    # DESCRIPTION:
    #   
    def getItems(data_uuid, column, table_name, database_name):
        pass

    # FUNCTION: replaceItem
    # INPUT: 
    # OUTPUT: 
    # DESCRIPTION:
    #   
    def updateItem(data_uuid, input, column, table_name, database_name):
        pass

    # FUNCTION: replaceItems
    # INPUT: 
    # OUTPUT: 
    # DESCRIPTION:
    #   
    def updateItems(data_uuid, input, columns, table_name, database_name):
        pass

    # FUNCTION: getColumn
    # INPUT: table_name    - string
    #        database_name - string
    # KWARGS: limit  - int,  [how many entries to return]
    #         period - tuple (start_time, end_time), in UNIX timestamp
    # OUTPUT: list
    # DESCRIPTION:
    #   Retrieves an entire column from a table in a datbase. kwargs limit and period can
    #    be used to restrict the number of values to return.
    # WARNING: heavy load on time, very slow
    def getColumn(table_name, database_name, **kwargs):
        pass

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


    # FUNCTION: getColumn
    # INPUT:
    # OUTPUT:
    # DESCRIPTION:
    #   
    # WARNING: heavy load on time, very slow
    def getColumns():
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