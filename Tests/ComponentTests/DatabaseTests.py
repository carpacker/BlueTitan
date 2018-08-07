# DatabaseTests.py
#  BlueTitan Trading System
#  Testing Suite for Database-Manager component
#  Carson Packer
# DESCRIPTION:
#    Performs individual and combined test for the GeneralizedDatabase library. Also includes
#     auxillary tests for specialized database calls.

# External-Imports
import os
import sqlite3
import sys
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
    TestGenDatabaseLibrary.getColumnNames(path, "ColumnTests", 0)

    PrintLibrary.delimiter()
    PrintLibrary.header("getItem")
    TestGenDatabaseLibrary.getItem(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItem(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItem(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItem(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItem(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItem(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItem(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItem(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItem(path, "ItemTests", 0))
    
    PrintLibrary.delimiter()
    PrintLibrary.header("getItems")
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0))
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0))

    PrintLibrary.delimiter()
    PrintLibrary.header("updateEntry")
    TestGenDatabaseLibrary.updateEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntry(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntry(path, "EntryTests", 0)


    PrintLibrary.delimiter()
    PrintLibrary.header("updateEntries")
    TestGenDatabaseLibrary.updateEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.updateEntries(path, "EntryTests", 0)
    TestGenDatabaseLibrary.getEntries(path, "EntryTests", 0)

    PrintLibrary.delimiter()
    PrintLibrary.header("updateItem, getItem")
    TestGenDatabaseLibrary.updateItem(path, "ItemTests", 0)
    TestGenDatabaseLibrary.getItem(path, "ItemTests", 0)
    TestGenDatabaseLibrary.updateItem(path, "ItemTests", 0)
    TestGenDatabaseLibrary.getItem(path, "ItemTests", 0)
    TestGenDatabaseLibrary.updateItem(path, "ItemTests", 0)
    TestGenDatabaseLibrary.getItem(path, "ItemTests", 0)
    TestGenDatabaseLibrary.updateItem(path, "ItemTests", 0)
    TestGenDatabaseLibrary.getItem(path, "ItemTests", 0)
    TestGenDatabaseLibrary.updateItem(path, "ItemTests", 0)
    TestGenDatabaseLibrary.getItem(path, "ItemTests", 0)
    TestGenDatabaseLibrary.updateItem(path, "ItemTests", 0)
    TestGenDatabaseLibrary.getItem(path, "ItemTests", 0)
    TestGenDatabaseLibrary.updateItem(path, "ItemTests", 0)
    TestGenDatabaseLibrary.getItem(path, "ItemTests", 0)
    TestGenDatabaseLibrary.updateItem(path, "ItemTests", 0)
    TestGenDatabaseLibrary.getItem(path, "ItemTests", 0)
    
    PrintLibrary.delimiter()
    PrintLibrary.header("updateItems")
    TestGenDatabaseLibrary.updateItems(path, "ItemTests", 0)
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0)
    TestGenDatabaseLibrary.updateItems(path, "ItemTests", 0)
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0)
    TestGenDatabaseLibrary.updateItems(path, "ItemTests", 0)
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0)
    TestGenDatabaseLibrary.updateItems(path, "ItemTests", 0)
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0)
    TestGenDatabaseLibrary.updateItems(path, "ItemTests", 0)
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0)
    TestGenDatabaseLibrary.updateItems(path, "ItemTests", 0)
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0)
    TestGenDatabaseLibrary.updateItems(path, "ItemTests", 0)
    TestGenDatabaseLibrary.getItems(path, "ItemTests", 0)
    
    PrintLibrary.delimiter()
    PrintLibrary.header("deleteEntry")
    TestGenDatabaseLibrary.deleteEntry(path, "EntryTests", 0)
    
    PrintLibrary.delimiter()
    PrintLibrary.header("deleteEntries")
    TestGenDatabaseLibrary.deleteEntries(path, "EntryTests", 0)

if __name__ == "__main__":
    initializeTestDatabase()
    baseTesters()
    mainTesters()
