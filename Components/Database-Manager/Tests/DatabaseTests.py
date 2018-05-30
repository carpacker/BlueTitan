# External-Imports
import sys
import os
import sqlite3
import time

# Windows Main Desktop
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Libraries')
sys.path.append('U:/Directory/Projects/BlueTitan/Bots/Arbitrage/Librarise')
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Database-Manager')

# Windows Laptop
# sys.path.append('C:/C-Directory/Projects/BlueTitan/Components/Libraries')
# sys.path.append('C:/C-Directory/Projects/BlueTitan/Components/Crypto-API/Exchange-APIs')
# sys.path.append('C:/C-Directory/Projects/BlueTitan/Bots/Arbitrage/Libraries')

# Internal-Imports
from PrintLibrary import PrintLibrary
import Helpers
import ArbitrageDatabaseLib
from GeneralizedDataase import GenDatabaseLibrary

# FUNCTION: initializeTestDatabase
# INPUT: N/A
# OUTPUT: N/A
# DESCRIPTION:
#   Creates a test database to be used for testing GeneralizedDatabase calls. If necessary,
#    may be expanded to test other parts of the program
def initializeTestDatabase():
    pass
    
# TESTERS: base functions
# DESCRIPTION:
#   All testers for helper functions exclusively used within the GeneralizedDatabase.py file
def baseTesters():
    PrintLibrary.header("Base Calls")
    #                    Base Function Calls
    # GenDatabaseLibrary.listColumns()
    # GenDatabaseLibrary.selectFromTable()
    pass

# TESTERS: main functions
# DESCRIPTION:
#   Testers for eac
def mainTesters():
    PrintLibrary.header("Main functions")
    PrintLibrary.header("storeEntry, storeEntries")
    GenDatabaseLibrary.storeEntry(("", "", 0, 0), "IntendedFAE", "ArbitrageDatabase")
    GenDatabaseLibrary.storeEntries([("first", "second", 1, 1), ("third", "fourth", 1, 1)], "IntendedFAE", "ArbitrageDatabase")
    # GenDatabaseLibrary.storeEntry() . do test database here
    GenDatabaseLibrary.storeEntries([("fifth", "sixth", 1, 2), ("seventh", "eighth", 3, 4), "IntendedFAE", "ArbitrageDatabase"])

    PrintLibrary.header("getEntry, getEntries, getLastEntry")
    GenDatabaseLibrary.getEntry("aa1", "ArbitrageTrades", "ArbitrageDatabase")
    GenDatabaseLibrary.getEntry("mm1", "Metrics", "MetricsDatabase")
    GenDatabaseLibrary.getEntry("aa2", "ArbitrageTrades", "ArbitrageDatabase")

    GenDatabaseLibrary.getEntries()
    GenDatabaseLibrary.getEntries()
    GenDatabaseLibrary.getEntries()

    GenDatabaseLibrary.getLastEntry()

    PrintLibrary.header("getColumn,getColumns")
    GenDatabaseLibrary.getColumn()

    # getItem, getItems
    GenDatabaseLibrary.getItem()
    GenDatabaseLibrary.getItem()

    GenDatabaseLibrary.getItems()
    GenDatabaseLibrary.getItems()

    # updateEntry, updateEntries
    
    # updateItem, updateItems

    # deleteEntry, deleteEntries
    GenDatabaseLibrary.deleteEntry()
    GenDatabaseLibrary.deleteEntries()

if __name__ == "__main__":
