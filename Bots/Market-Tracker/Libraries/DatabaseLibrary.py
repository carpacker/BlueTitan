# DatbaseLibrary.py (MARKET TRACKER)
# Carson Packer
# DESCRIPTION:
#    Specialized library of database calls for the performance tracking system.

# External-Imports
import sys

# WINDOWS main-desktop
sys.path.append('U:/Directory/Projects/BlueTitan/Components/DatabaseManager')

# WINDOWS laptop
# sys.path.append()

# LINUX main-server
# sys.path.append()

# Internal Imports
import Helpers
from GeneralizedDatabase import GenDatabaseLibrary
from PrintLibrary import PrintLibrary

# CLASS: HistoricalDatabase
# DESCRIPTION:
#    TODO
class HistoricalDatabase():
    path = 0
    table_names = []
