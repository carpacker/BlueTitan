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

# CLASS: GenDatabaseLibrary
# DESCRIPTION:
#   Library of generic functions for interacting with any database (and tables). Takes databases
#    (and tables, if required) as inputs.
class GenDatabaseLibrary(object):
    database_paths = {}

    # Lets try this for now, not sure if I totally agree with the underlying structure.
    def initializeDatabasePaths(name_paths):
        for value in name_paths:
            GenDatabaseLibrary.database_paths[value[0]] = value[1]
            
    # FUNCTION: buildInitTuple
    # INPUT: table_name    - string
    #        database_name - string
    # OUTPUT: tuple
    # DESCRIPTION:
    #    Creates an initiliazer tuple based on a given table and name. It provides a generic
    #     initializer value for eachd data type
    #  TEXT - ""
    #  REAL - 0
    #  REST - TODO
    def buildInitTuple(table_name, database_name):

        # Below isn't written yet... instead of getcolumns, it should be getcolumn names or something
        num_columns = GenDatabaseLibraries.getColumns()
        
        init_list = []
        for x in range (0, num_columns):
            # Below hasn't been written
            type_col = GenDatabaseLibrary.getColumnType(x, table_name, database_name)
            if type_col == "STRING":
                init_list.append("")
            elif type_col == "REAL":
                init_list.append(0)
            else:
                pass

        PrintLibrary.displayVariables(init_list)
        return init_list

    # FUNCTION: createTable
    # INPUT: table_name    - string
    #        database_name - string
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Generic function for creating a table in a database.
    # NOTE: Not useful yet.
    def createTable(database_name, table_name, columns=""):
        pass

    # FUNCTION: deleteTable
    # INPUT: cursor     - *
    #        table_name - string
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Deletes a table given a cursor for a databse and the table's name.
    def deleteTable(cursor, table_name):
        sql_s = 'DROP TABLE %s' % table_name
        cursor.execute(sql_s)

    # FUNCTION: cleanDatabase
    # INPUT: tables     - [string, ...]
    #        exceptions - [string, ...] 
    # OUTPUT: list of tables cleaned in database
    # DESCRIPTION
    #   Used to clean a database's tables minus exceptions.
    def cleanDatabase(database_name, tables, exceptions=[""]):
        database_path = database_paths[database_name]
        connection, cursor = connect(database_path)

        # Use regular expression to find difference of two lists
        list_clean = list(set(tables).difference(set(exceptions)))
        for table in list_clean:
            try:
                deleteTable(cursor, table, database_name)
            except sqlite3.OperationalError:
                pass
            database.createTable(cursor, table, database_name)
        disconnect(connection)
        return list_clean
                             
    # HELPER: buildStringStore
    # INPUT: cursor     - *
    #        table_name - string
    # OUTPUT: string
    # DESCRIPTION:
    #    Builds SQL string to store an entry. 
    def buildStringStore(cursor, table_name, columns="all"):
        
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
    def storeEntry(database_name, table_name, data):
        
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
    def storeEntries(database_name, table_name, data):

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
    def getEntryString(table_name, data):
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

    def updateEntryString():
        pass
    
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

    def getItemString():
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

    def updateItemString():
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
        pass
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

    def deleteEntryString():
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
