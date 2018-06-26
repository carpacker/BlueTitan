# DatbaseLibrary.py (PERFORMANCE TRACKER)
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
from GeneralizedDatabase import GenData

# CLASS: ExchangeRecords
class ExchangeRecords():
    path = 0
    table_names = []
