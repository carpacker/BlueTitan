# External-Imports
import sys
import os
import sqlite3
import time

sys.path.append('U:/Directory/Projects/BlueTitan/Components/Libraries')

# Internal-Imports
from PrintLibrary import PrintLibrary
import Helpers
import ArbitrageDatabaseLib

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

trades_info = {'initialize' : ''}

arbitrage_tables = {'trades' : trades_info}
assetMetrics_tables = {}
exchangeRecords_tables = {}
historicalData_tables = {}
metrics_tables = {}
miningRecords_tables = {}

databases = {'arbitrage' : arbitrage_tables,	
            'asset_metrics' : assetMetrics_tables,
            'exchange_records' : exchangeRecords_tables,
            'historical_data' : historicalData_tables,
            'metrics' : metrics_tables,
            'mining_records' : miningRecords_tables
            }

database_paths = {"ArbitrageDatabase" : os.path.join(os.path.dirname(__file__), 'arbitrageDB.sqlite3')}

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

    # FUNCTION: storeEntry
    # INPUT: data          - tuple
    #        database_name - string
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Generic function for storing an entry into a table in a database.
    def storeEntry(data, table_name, database_name):
        # 1. Set database, initializes variables, check table exists
        database_path = database_paths[database_name]
        timestamp = Helpers.createTimestamp()
        uuid = createUuid(table_name, database_name)
        checkTableNameExists(cursor, table_name, database)
        connect, cursor = database.connect(database_path)

        # 1. List columns
        columns = SQLoperations.listColumns(cursor, table_name)
        num_columns = len(column)

        PrintLibrary.displayVariables(column_names, "Columns for table")

        # 2. Build string based on column names and number of columns

        # (?, ...) where number of elements is equal to number of columns.
        sql_q = "("
        for value in range(0, num_columns):
            sql_q += "?,"
        sql_q -= ","
        sql_q += ")"

        sql_s = "INSERT INTO %s (" % table_name
        for column in columns:
            sql_s += column + ","
        sql_s -= ","
        sql_s += ") VALUES " + sql_q

        PrintLibrary.displayVariable(sql_s, "SQL string")
        cursor.execute(sql_s)
        disconnect(connect)

    # FUNCTION: storeEntries
    # INPUT: data - [(data, ...), ...]
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Generic function for storing multiple entries into a table in a database.
    def storeEntries():
        # TODO
        #  Similar to above but only one connect
        pass

    # FUNCTION: retrieveEntry
    # INPUT: TBD
    # OUTPUT: (V1, ..., Vn) where n is number of columns
    # DESCRIPTION:
    #	Accesses a table in a database and pulls a row from the database.
    # TODO - retrieving variables within row
    # TODO - various methods to retrieve an entry
    def getEntry():
        pass

    def getEntries():
        pass

    # FUNCTION: getLastEntry
    # INPUT: cursor     - *
    #        table_name - string
    # OUTPUT: desired entry
    # DESCRIPTION:
    #   Retrieves the last entry in a database. Uses timestamp instead of internal
    #    id, assumes ascending order based on timestamp.
    def getLastEntry(cursor, table_name):
        sql_s = "SELECT * FROM %s ORDER BY Time_stamp DESC LIMIT 1" % table_name
        cursor.execute(sql_s,)
        entry = cursor.fetchall()
        return entry[0]

    def getItem():
        pass

    # Special parameters
    def getItems():
        pass

    def getColumn():
        pass

    # NOTE: If database is provided, just go into database, other than that just infer database based on uuid
    # 
    def deleteEntry(uuid, database=None):
        pass

    # 
    def deleteEntries(uuid, database=None):
        pass

    #
    def deleteEntriesPeriod(period, database=None):
        pass

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

# If called independently, these are the tests.
if __name__ == "__main__":
    GenDatabaseLibrary.storeEntry(("", "", 0, 0), "IntendedFAE", "ArbitrageDatabase")