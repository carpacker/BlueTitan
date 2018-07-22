# External-Imports
import sys
import os
import sqlite3
import time

# Windows Main Desktop
sys.path.append('U:/Directory/Projects/BlueTitan/Libraries')
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Database-Manager')

# Windows Laptop
# sys.path.append('C:/C-Directory/Projects/BlueTitan/Components/Libraries')
# sys.path.append('C:/C-Directory/Projects/BlueTitan/Components/Crypto-API/Exchange-APIs')
# sys.path.append('C:/C-Directory/Projects/BlueTitan/Bots/Arbitrage/Libraries')

# Internal-Imports
from PrintLibrary import PrintLibrary
import Helpers
import GeneralizedDatabase
from GeneralizedDatabase import GenDatabaseLibrary

# FUNCTION: initializeTestDatabase
# INPUT: N/A
# OUTPUT: N/A
# DESCRIPTION:
#   Creates test database to be used for testing GeneralizedDatabase calls. If necessary,
#    may be expanded to test other parts of the program
def initializeTestDatabase():
    PrintLibrary.header("Initializing Test Database")
    
    path = os.path.join(os.path.dirname(__file__), 'TestDatabase.sqlite3')
    connection, cursor = GeneralizedDatabase.connect(path)
    
    GenDatabaseLibrary.deleteTable(path, "RandomTable")
    GenDatabaseLibrary.createTable(path, "RandomTable", [("Column1", "real", "NOT NULL")])
    GenDatabaseLibrary.initializeTable(path, "RandomTable")

    PrintLibrary.header("Test Database Initialized")
    

# TESTERS: base functions
# DESCRIPTION:
#   All testers for helper functions exclusively used within the GeneralizedDatabase.py file.
def baseTesters():
    PrintLibrary.header("Base Calls")
    PrintLibrary.delimiter()
    PrintLibrary.header("Functions without database dependencies")

    PrintLibrary.header("UUID tets")
    PrintLibrary.displayVariable(GeneralizedDatabase.createUuid("ArbitrageTrades", "ArbitrageDatabase"))
    PrintLibrary.displayVariable(GeneralizedDatabase.createUuid("Metrics", "MetricsDatabase"))
    PrintLibrary.displayVariable(GeneralizedDatabase.createUuid("AssetMetrics", "AssetMetricsDatabase"))

    PrintLibrary.header("Connect, checkTableNameExists, generalQuery, commitWrite, disconnect flow tests")
    connect, cursor = GeneralizedDatabase.connect()
    GeneralizedDatabase.checkTableNameExists()
    GeneralizedDatabase.generalQuery()
    GeneralizedDatabase.commitWrite()
    GeneralizedDatabase.disconnect(connect)
    PrintLibrary.header("BASE function tests are FINISHED")
    PrintLibrary.delimiter()

# TESTERS: main functions
# DESCRIPTION:
#   Testers for each main generic function.
def mainTesters():
    PrintLibrary.header("Main functions")
    PrintLibrary.header("storeEntry")
    GenDatabaseLibrary.storeEntry("TestDatabase", "", 0)
    GenDatabaseLibrary.storeEntry("TestDatabase", "", 0)
    GenDatabaseLibrary.storeEntry("TestDatabase", "", 0)
    GenDatabaseLibrary.storeEntry("TestDatabase", "", 0)
    GenDatabaseLibrary.storeEntry("TestDatabase", "", 0)

    PrintLibrary.delimiter()
    PrintLibrary.header("storeEntries")
    GenDatabaseLibrary.storeEntries("TestDatabase", "", [])
    GenDatabaseLibrary.storeEntries("TestDatabase", "", ())
    GenDatabaseLibrary.storeEntries("TestDatabase", "", [])
    GenDatabaseLibrary.storeEntries("TestDatabase", "", [])
    GenDatabaseLibrary.storeEntries("TestDatabase", "", [])

    PrintLibrary.delimiter()
    PrintLibrary.header("getEntry")
    GenDatabaseLibrary.getEntry("aa1", "ArbitrageTrades", "ArbitrageDatabase")
    GenDatabaseLibrary.getEntry("mm1", "Metrics", "MetricsDatabase")
    GenDatabaseLibrary.getEntry("aa2", "ArbitrageTrades", "ArbitrageDatabase")
    GenDatabaseLibrary.getEntry("aa2", "ArbitrageTrades", "ArbitrageDatabase")
    GenDatabaseLibrary.getEntry("aa2", "ArbitrageTrades", "ArbitrageDatabase")
    GenDatabaseLibrary.getEntry("aa2", "ArbitrageTrades", "ArbitrageDatabase")
    GenDatabaseLibrary.getEntry("aa2", "ArbitrageTrades", "ArbitrageDatabase")
    GenDatabaseLibrary.getEntry("aa2", "ArbitrageTrades", "ArbitrageDatabase")

    PrintLibrary.delimiter()
    PrintLibrary.header("getEntries")
    GenDatabaseLibrary.getEntries()
    GenDatabaseLibrary.getEntries()
    GenDatabaseLibrary.getEntries()
    GenDatabaseLibrary.getEntries()
    GenatabaseeLibrary.getEntries()
    GenDatabaseLibrary.getEntries()
    GenDatabaseLibrary.getEntries()
    GenatabaseeLibrary.getEntries()

    PrintLibrary.delimiter()
    PrintLibrary.header("getLastEntry")
    GenDatabaseLibrary.getLastEntry()

    PrintLibrary.delimiter()
    PrintLibrary.header("getColumn")
    GenDatabaseLibrary.getColumn()
    GenDatabaseLibrary.getColumn()
    GenDatabaseLibrary.getColumn()

    PrintLibrary.delimiter()
    PrintLibrary.header("getColumns")
    GenDatabaseLibrary.getColumns()
    GenDatabaseLibrary.getColumns()
    GenDatabaseLibrary.getColumns()
    GenDatabaseLibrary.getColumns()
    GenDatabaseLibrary.getColumns()

    PrintLibrary.delimiter()
    GenDatabaseLibrary.header("getColumnType")
    GenDatabaseLibrary.getColumnType()
    GenDatabaseLibrary.getColumnType()
    GenDatabaseLibrary.getColumnType()

    PrintLibrary.delimiter()
    GenDatabaseLibrary.header("getColumnTypes")
    GenDatabaseLibrary.getColumnTypes()

    PrintLibrary.delimiter()
    GenDatabaseLibrary.header("getColumnName")
    GenDatabaseLibrary.getColumnName()
    GenDatabaseLibrary.getColumnName()
    GenDatabaseLibrary.getColumnName()

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
