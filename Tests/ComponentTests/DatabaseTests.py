# External-Imports
import sys
import os
import sqlite3
import time

# Relative path for imports
sys.path.append(os.path.realpath('../../Components/Crypto-API/Exchange-APIs/'))
sys.path.append(os.path.realpath('../../Components/Libraries'))
sys.path.append(os.path.realpath('../../Components/Database-Manager'))

# Internal-Imports
from PrintLibrary import PrintLibrary
import Helpers
import GeneralizedDatabase
from GeneralizedDatabase import GenDatabaseLibrary

# Path for test database
path = os.path.join(os.path.realpath('../../Resources/Databases'), 'TestDatabase.sqlite3')

# FUNCTION: initializeTestDatabase
# INPUT: N/A
# OUTPUT: N/A
# DESCRIPTION:
#   Creates test database to be used for testing GeneralizedDatabase calls. If necessary,
#    may be expanded to test other parts of the program
def initializeTestDatabase():
    PrintLibrary.header("Initializing Test Database")

    # Testing initialization of paths
    TestGenDatabaseLibrary = GenDatabaseLibrary({"TestDatabase" : path})
    PrintLibrary.displayDictionary(TestGenDatabaseLibrary.database_paths)
    print(TestGenDatabaseLibrary.database_paths)

    connection, cursor = GeneralizedDatabase.connect(path)
    
    TestGenDatabaseLibrary.createTable(path, "RandomTable", [("Column1", "real", "NOT NULL")])
    TestGenDatabaseLibrary.deleteTable(path, "RandomTable")
    TestGenDatabaseLibrary.createTable(path, "RandomTable", [("Column1", "real", "NOT NULL")])
    TestGenDatabaseLibrary.initializeTable(path, "RandomTable")

    PrintLibrary.header("Test Database Initialized")
    

# TESTERS: base functions
# DESCRIPTION:
#   All testers for helper functions exclusively used within the GeneralizedDatabase.py file.
def baseTesters():
    PrintLibrary.header("Base Calls")
    PrintLibrary.delimiter()
    PrintLibrary.header("Functions without database dependencies")

    #PrintLibrary.header("UUID tests")
    #PrintLibrary.displayVariable(GeneralizedDatabase.createUuid("ArbitrageTrades", "ArbitrageDatabase"))
    #PrintLibrary.displayVariable(GeneralizedDatabase.createUuid("Metrics", "MetricsDatabase"))
    #PrintLibrary.displayVariable(GeneralizedDatabase.createUuid("AssetMetrics", "AssetMetricsDatabase"))

    PrintLibrary.header("Connect, checkTableNameExists, generalQuery, commitWrite, disconnect flow tests")
    connect, cursor = GeneralizedDatabase.connect()
    print(GeneralizedDatabase.checkTableNameExists(path, "Testing"))
    GenDatabaseLibrary.createTable(path, "Testing", [("Column1", "real", "NOT NULL")])
    print(GeneralizedDatabase.checkTableNameExists(path, "Testing"))
    #GeneralizedDatabase.generalQuery()
    #GeneralizedDatabase.commitWrite()
    GeneralizedDatabase.disconnect(connect)
    PrintLibrary.header("BASE function tests are FINISHED")
    PrintLibrary.delimiter()

# TESTERS: main functions
# DESCRIPTION:
#   Testers for each main generic function.
def mainTesters():
    PrintLibrary.header("Main functions")
    PrintLibrary.header("storeEntry")
    
    TestGenDatabaseLibrary = GenDatabaseLibrary({"TestDatabase" : path})
    
    TestGenDatabaseLibrary.storeEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.storeEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.storeEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.storeEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.storeEntry(path, "EntryTests", 0)

    PrintLibrary.delimiter()
    PrintLibrary.header("storeEntries")
    TestGenDatabaseLibrary.storeEntries(path, "EntryTests", [])
    TestGenDatabaseLibrary.storeEntries(path, "EntryTests", ())
    TestGenDatabaseLibrary.storeEntries(path, "EntryTests", [])
    TestGenDatabaseLibrary.storeEntries(path, "EntryTests", [])
    TestGenDatabaseLibrary.storeEntries(path, "EntryTests", [])

    PrintLibrary.delimiter()
    PrintLibrary.header("getEntry")
    TestGenDatabaseLibrary.getEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntry(path, "EntryTests", 0)

    PrintLibrary.delimiter()
    PrintLibrary.header("getEntries")
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)

    PrintLibrary.delimiter()
    PrintLibrary.header("getLastEntry")
    TestGenDatabaseLibrary.getLastEntry(path, "EntryTests")

    PrintLibrary.delimiter()
    PrintLibrary.header("getColumn")
    TestGenDatabaseLibrary.getColumn(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getColumn(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getColumn(path, "EntryTests", 0)

    PrintLibrary.delimiter()
    PrintLibrary.header("getColumns")
    TestGenDatabaseLibrary.getColumns(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getColumns(path, "ColumnTests", 0)

    PrintLibrary.delimiter()
    PrintLibrary.header("getColumnType")
    TestGenDatabaseLibrary.getColumnType(path, "ColumnTests", 0)
    TestGenDatabaseLibrary.getColumnType(path, "ColumnTests", 0)
    TestGenDatabaseLibrary.getColumnType(path, "ColumnTests", 0)
    TestGenDatabaseLibrary.getColumnType(path, "ColumnTests", 0)
    TestGenDatabaseLibrary.getColumnType(path, "ColumnTests", 0)

    PrintLibrary.delimiter()
    PrintLibrary.header("getColumnTypes")
    TestGenDatabaseLibrary.getColumnTypes(path, "ColumnTests", 0)
    TestGenDatabaseLibrary.getColumnTypes(path, "ColumnTests", 0)
    TestGenDatabaseLibrary.getColumnTypes(path, "ColumnTests", 0)
    TestGenDatabaseLibrary.getColumnTypes(path, "ColumnTests", 0)

    PrintLibrary.delimiter()
    PrintLibrary.header("getColumnName")
    TestGenDatabaseLibrary.getColumnName(path, "ColumnTests", 0)
    TestGenDatabaseLibrary.getColumnName(path, "ColumnTests", 0)
    TestGenDatabaseLibrary.getColumnName(path, "ColumnTests", 0)
    TestGenDatabaseLibrary.getColumnName(path, "ColumnTests", 0)

    PrintLibrary.delimiter()
    PrintLibrary.header("getColumnNames")
    GenDatabaseLibrary.getColumnNames()

    PrintLibrary.delimiter()
    PrintLibrary.header("getItem")
    GenDatabaseLibrary.getItem()
    GenDatabaseLibrary.getItem()
    GenDatabaseLibrary.getItem()
    GenDatabaseLibrary.getItem()
    GenDatabaseLibrary.getItem()
    GenDatabaseLibrary.getItem()
    
    PrintLibrary.delimiter()
    PrintLibrary.header("getItems")
    GenDatabaseLibrary.getItems()
    GenDatabaseLibrary.getItems()
    GenDatabaseLibrary.getItems()
    GenDatabaseLibrary.getItems()
    GenDatabaseLibrary.getItems()
    GenDatabaseLibrary.getItems()
    GenDatabaseLibrary.getItems()
    GenDatabaseLibrary.getItems()

    PrintLibrary.delimiter()
    PrintLibrary.header("updateEntry")
    GenDatabaseLibrary.updateEntry()
    GenDatabaseLibrary.updateEntry()
    GenDatabaseLibrary.updateEntry()
    GenDatabaseLibrary.updateEntry()
    GenDatabaseLibrary.getEntry()
    GenDatabaseLibrary.getEntry()
    GenDatabaseLibrary.getEntry()
    GenDatabaseLibrary.getEntry()

    PrintLibrary.delimiter()
    PrintLibrary.header("updateEntries")
    GenDatabaseLibrary.updateEntries()
    GenDatabaseLibrary.updateEntries()
    GenDatabaseLibrary.updateEntries()
    GenDatabaseLibrary.updateEntries()
    GenDatabaseLibrary.updateEntries()
    GenDatabaseLibrary.updateEntries()
    GenDatabaseLibrary.getEntries()
    GenDatabaseLibrary.getEntries()
    GenDatabaseLibrary.getEntries()
    GenDatabaseLibrary.getEntries()
    GenDatabaseLibrary.getEntries()
    GenDatabaseLibrary.getEntries()
    
    PrintLibrary.delimiter()
    PrintLibrary.header("updateitem")
    GenDatabaseLibrary.updateItem()
    GenDatabaseLibrary.updateItem()
    GenDatabaseLibrary.updateItem()
    GenDatabaseLibrary.updateItem()

    PrintLibrary.delimiter()
    PrintLibrary.header("updateItems")
    GenDatabaseLibrary.updateItems()
    GenDatabaseLibrary.updateItems()
    
    PrintLibrary.delimiter()
    PrintLibrary.header("deleteEntry")
    GenDatabaseLibrary.deleteEntry()
    
    PrintLibrary.delimiter()
    PrintLibrary.header("deleteEntries")
    GenDatabaseLibrary.deleteEntries()

if __name__ == "__main__":
    initializeTestDatabase()
    baseTesters()
    mainTesters()
