# External-Imports
import sys
import os
import sqlite3
import time
import uuid

# Internal-Imports
from PrintLibrary import PrintLibrary
import Helpers

##################################### HELPERS ######################################################
# * checkTableNameExists -
# * commitWrite          -
# * connect              -
# * createUUID           -
# * disconnect           -
# * generalQuery         -
####################################################################################################
# FUNCTION: checkTableNameExists
# INPUT: table_name - string
# OUTPUT: N/A
#   Wrapper function to ensure that the table exists before performing an operation.
# TODO: TRY/CATCH block in case database doesn't have default table or something like that.
def checkTableNameExists(database_path, table_name):
    table_names = GenDatabaseLibrary.listTables(database_path)
    if table_name not in table_names:
        return False

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
    print("booga", path)
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        return connection,cursor
    except Error as e:
        print(e)
    return None

#
def listColumns(cursor, table_name):
    sql_s = "PRAGMA table_info('%s')" % table_name
    cols_list = []
    cursor.execute(sql_s)
    col_tups = cursor.fetchall()
    for tup in col_tups:
        cols_list.append(tup[1])
    return cols_list

# HELPER: buildStringStore
# INPUT: cursor     - *
#        table_name - string
#        columns    - TODO
# OUTPUT: string
# DESCRIPTION:
#    Builds SQL string to store an entry. 
def buildStringStore(cursor, table_name, columns="all"):
    
    # 1. List columns
    columns = listColumns(cursor, table_name)
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
 
# FUNCTION: createUuid
# INPUT: table_name    - string
#        database_name - string
# OUTPUT: int
# DESCRIPTION:
#   Creates a unique identifier for a given trade, metric, transfer, etc.
def createUuid(table_name, database_name):

    # Prototype, inefficient system to create unique identifiers. Future will need
    #  a better solution, as this makes too many database calls in a row.
    table_identifiers = GenDatabaseLibrary.getItem(runtime_path, "table_identifiers")
    database_identifiers = GenDatabaseLibrary.getItem(runtime_path, "database_identifiers")
    uuid_counter = GenDatabaseLibrarye.getItem(runtime_path, "last_uuid", "globals")
    
    identifier = table_identifier + database_identifier + str(uuid_counter)
    print(identifier)
    return identifier

# FUNCTION: disconnect
# INPUT: connect - *
# OUTPUT: N/A
# DESCRIPTION:
#   Wrapper for disconnecting from a database
def disconnect(connection):
    connection.commit()
    connection.close()

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

    # INITIALIZATION:
    #    GenDatabaseLibrary must be instantiated as instance with an input of the used database
    #     paths. This allows the class to remain truly generic as it caters to the input given
    #     by another script. The downside is that the object must be passed around.
    def __init__(self, paths):
        for path in paths:
            self.database_paths[path] = paths[path]
            
    # INPUT: database_name - string
    #        table_name    - string
    # OUTPUT: tuple
    # DESCRIPTION:
    #    Creates an initiliazer tuple based on a given table and name. It provides a generic
    #     initializer value for eachd data type
    #  TEXT - ""
    #  REAL - 0
    #  REST - TODO
    def buildInitTuple(database_name, table_name):

        # Below isn't written yet... instead of getcolumns, it should be getcolumn names or
        #  something
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
    def createTable(self, database_path, table_name, columns):
        connection, cursor = connect(database_path)

        # Check if table name exists already
        table_names = GenDatabaseLibrary.listTables(database_path)
        exists = table_name in table_names
        if exists:
            disconnect(connection)
        else: 
            sql_s = """
               CREATE TABLE %s (
               id integer PRIMARY KEY""" % table_name

            for col_tuple in columns:
                print(col_tuple)
                added_s = ",%s %s %s" % col_tuple
                sql_s += added_s
                sql_s += ")"

            PrintLibrary.displayVariable(sql_s)
            cursor.execute(sql_s)
            disconnect(connection)

    # FUNCTION: initializeTable
    # INPUT: database_name - string
    #        table_name    - string
    # OUTPUT: N/A
    # DESCRIPTION:
    #    Generic table initializer, looks through columns in table and fills it with default values
    #     based on the type of data stored there.
    def initializeTable(self, database_path, table_name):
        pass
    
    # FUNCTION: deleteTable
    # INPUT: database_name - string
    #        table_name    - string
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Deletes a table given a cursor for a databse and the table's name.
    def deleteTable(self, database_path, table_name):
        connection, cursor = connect(database_path)
        # TODO: Add better check
        sql_s = 'DROP TABLE %s' % table_name
        cursor.execute(sql_s)
        disconnect(connection)

    # FUNCTION: cleanDatabase
    # INPUT: tables     - [string, ...]
    #        exceptions - [string, ...] 
    # OUTPUT: list of tables cleaned in database
    # DESCRIPTION
    #   Used to clean a database's tables minus exceptions.
    def cleanDatabase(self, database_path, tables, exceptions=[""]):
        connection, cursor = connect(database_path)

        # Use regular expression to find difference of two lists
        list_clean = list(set(tables).difference(set(exceptions)))
        for table in list_clean:
            try:
                GenDatabaseLibrary.deleteTable(cursor, table)
            except sqlite3.OperationalError:
                pass
            database.createTable(cursor, table)
            disconnect(connection)
        return list_clean
    


    # FUNCTION: storeEntry
    # INPUT: database_path -
    #        table_name    -
    #        data          - tuple, (item, ...)
    # OUTPUT: N/A
    # DESCRIPTION:
    #    Generic function for storing an entry into a table in a database.
    def storeEntry(self, database_path, table_name, data):
        
        # Set database, initializes variables, check table exists

        #timestamp = int(time.time() * 1000)
        #uuid = createUuid(table_name, database_name)

        connection, cursor = connect(database_path) 
        checkTableNameExists(cursor, database_name, table_name)

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
    def storeEntries(self, database_path, table_name, data):

        # Set database, initializes variables, check table exists
        connection, cursor = connect(database_path)
        checkTableNameExists(cursor, table_name, database_name)

        # For each tuple in data, build SQL execution string, execute and then disconnect
        for value in data:
            sql_s = GenDatabaseLibrary.buildStringStore(cursor, table_name)
            PrintLibrary.displayVariable(sql_s, "SQL string")
            PrintLibrary.displayVariable(value, "Value")
            cursor.execute(sql_s,value)
            
        disconnect(connection)

    # FUNCTION: getEntry
    # INPUT: database_name - string
    #        table_name    - string
    #        data_uuid     - list or string
    # OUTPUT: (V1, ..., Vn) where n is number of columns
    # DESCRIPTION:
    #   Accesses a table in a database and pulls a row from the database. There
    #    are two options to access the entry. The first is by a unique identifier
    #    (uuid). The second is by a list of variables/values, and the function
    #    attempts to find the entry using these as a key.
    def getEntry(database_path, table_name, data_uuid):

        # Set database, initializes variables, check table exists
        print(type(data_uuid))
        if data_uuid == 'list':
            timestamp = int(time.time() * 1000)
            uuid = createUuid(table_name, database_name)
            connection, cursor = connect(database_path)
            checkTableNameExists(cursor, table_name, database_name)
        elif data_uuid == 'string':
            timestamp = int(time.time() * 1000)
            uuid = createUuid(table_name, database_name)
            connection, cursor = connect(database_path)
            checkTableNameExists(cursor, table_name, database_name)
            data_uuid = [data_uuid]
        else:
            # TODO, better error handling
            return 'error'
        sql_s = GenDatabaseLibrary.getEntryString(table_name, data_uuid)
        PrintLibrary.displayVariable(sql_s, "execution string")
        
        cursor.execute(sql_s, data_uuid)

    # FUNCTION: getEntryString
    # INPUT: table_name - string
    #        data       - list
    # OUTPUT: string
    # DESCRIPTION:
    #   Builds selection string.
    def getEntryString(table_name, data):
        sql_s ="SELECT * FROM %s WHERE" % table_name
        for value in data:
            sql_s += "%s = ? AND " % value
            sql_s = sql_s[:-4]
        return sql_s
    
    # FUNCTION: getEntries
    # INPUT: database_name - string
    #        table_name    - string
    #        data_uuids    - list or string
    #        period        - (OPTIONAL) int [DEFAULT=0]
    #        limit         - (OPTIONAL) int [DEFAULT=-1]
    #        order_by      - (OPTIONAL) string [DEFAULT=""]
    # OUTPUT: [(*entry), ...]
    # DESCRIPTION:
    #   Retrieves multiple entries. Various different methods are possible to
    #    determine what entries to return. 
    def getEntries(database_path, table_name, data_uuids, period=0, limit=-1, order_by=""):
        connection, cursor = connect(database_path)
        
        cursor.execute(sql_s)
        result = cursor.fetchall()
        disconnect(connection)
        return result

    # FUNCTION: getEntriesString
    # INPUT: table_name - string
    #        data       - list
    #        period     - int (unix timestamp, beginning)
    #        limit      - int
    #        order_by   - string
    # OUTPUT: string
    # DESCRIPTION:
    #   Builds selection string.
    def getEntriesString(table_name, data, period, limit, order_by):

        # Initial select
        sql_s ="SELECT * FROM %s WHERE" % table_name
        for value in data:
            sql_s += "%s = ? AND " % value
            # Add period
            sql_s += "Time_stamp > %s" % (period)
            # Add limit
        if limit > -1:
            sql_s += " LIMIT %S" % limit
            # Add ordering
        if order_by is not "":
            sql_s += " ORDER BY %s" % order_by

        PrintLibrary.displayVariable(sql_s, "execution string")
        return sql_s
    
    # FUNCTION: selectDistinct
    def selectDistinct():
        pass

    # FUNCTION: getLastEntry
    # INPUT: database_name - string
    #        table_name    - string
    # OUTPUT: desired entry
    # DESCRIPTION:
    #   Retrieves the last entry in a database. Uses timestamp instead of internal
    #    id, assumes ascending order based on timestamp.
    def getLastEntry(database_path, table_name):
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
    def updateEntry(database_path, data_uuid, input_val, table_name):
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
    def updateEntries(database_path, data_uuid, input_val, table_name, database_name):
        pass

    def getItemString():
        pass
    
    # FUNCTION: getItem
    # INPUT: database_path -
    #        table_name    - string
    #        data_uuid     - [data1, ...]
    #        column        - string
    # OUTPUT: Varies
    # DESCRIPTION: 
    #   Retrieves a single item from an entry in the input database and table.
    def getItem(database_path, table_name, data_uuid, column):
        pass

    # FUNCTION: getItems
    # INPUT: database_path - *
    #        table_name    - string
    #        data_uuid     - [data1, ...]
    #        columns       - string
    # OUTPUT: list of tuples [(data1, ...) ...] 
    # DESCRIPTION:
    #   Retrieves multiple items from an entry, designated by the column names.
    def getItems(database_path, table_name, data_uuid, columns):
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


    def updateItemString():
        pass
    
    # FUNCTION: updateItem
    # INPUT:  database_path - *
    #         table_name    - string
    #         data_uuid     - [data1, ...]
    #         input_val     - varies
    #         column        - string
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Updates an item using UUID or data as a reference to access the entry.
    def updateItem(database_path, table_name, data_uuid, input_val, column):
        pass

    # FUNCTION: updateItems
    # INPUT:  database_path - *
    #         table_name    - string
    #         data_uuid     - [data1, ...]
    #         input_val     - varies
    #         columns       - [string, ...]
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Updates multiple items (column values in an entry) using UUID or data as a reference
    #    to access the entry.
    def updateItems(database_path, table_name, data_uuid, input_val, columns):
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
    def getColumn(database_path, table_name):
        pass
    # 1. Check if attempting use period
    # 2. Check the quantity of entries to grab
    # 3. If neither, grab all
        
    # FUNCTION: getColumns
    # INPUT: table_name    - string
    #        database_name - string
    #        columns       - [string, ...]
    # KWARGS:
    # OUTPUT:
    # DESCRIPTION:
    #   Performs multiple getColumn() calls in order to retrieve multiple columns.
    # WARNING: heavy load on time, very slow
    def getColumns(database_path, table_name):
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
    def deleteEntry(database_path, table_name, data_uuid):
        pass

    # FUNCTION: deleteEntries
    # INPUT: type_v  - 'QUANT', 'MINUTES', 'HOURS'
    #        minutes - int
    # OUTPUT: boolean
    # DESCRIPTION:
    #    Delete entries either by minutes from start point or number of entries from start point.
    # TODO: error handling
    def deleteEntries(database_path, table_name, type_v, value, start=0):
	    # Connect to database here
        sql_s = 'DELETE FROM %s WHERE Time < %s' % cutoff
        if type_v == 'QUANT':
            sql_s = ''
            cursor.execute(sql_s)
            return True
        # One day in seconds, hours in seconds  
        one_day = 60*60*24        
        time = Helpers.getTimestamp()
        cutoff = time - (one_day)
        sql_s = 'DELETE FROM %s WHERE Time < %s' % cutoff
        cursor.execute(sql_s)

    # FUNCTION: listColumns
    # INPUT: database_path - *
    #        table_name    - string
    # OUTPUT: list of strings
    # DESCRIPTION:
    #   Returns a list of the names of each column in a given table.
    #  * - Wrapper over generic list columns
    def listColumns(database_path, table_name):
        connection, cursor = connect(database_path)
        
        sql_s = "PRAGMA table_info('%s')" % table_name
        cols_list = []
        cursor.execute(sql_s)
        col_tups = cursor.fetchall()
        for tup in col_tups:
            cols_list.append(tup[1])
        disconnect(connection)
        return cols_list

    # FUNCTION: listTables
    # INPUT: database_path - *
    # OUTPUT: table_list which is a representation of all the tables.
    # DESCRIPTION:
    #   Lists the tables in a database.
    def listTables(database_path):
        connection, cursor = connect(database_path)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        table_list = []
        fetched = cursor.fetchall()
        for tup in fetched:
            table_list.append(tup[0])
        disconnect(connection)
        return table_list
