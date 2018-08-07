# CoinCatTests.py
#  BlueTitan Trading System
#  Carson Packer
#  Paq ltd.
# DESCRIPTION:
#    Testing suite for individual and combined calls for the coin categorizer system.

# External-Imports
import os
import sys
import time

# Relative path for imports
sys.path.append(os.path.realpath('../../Components/Crypto-API/Exchange-APIs/'))
sys.path.append(os.path.realpath('../../Components/Crypto-API/Mining-APIs/'))
sys.path.append(os.path.realpath('../../Components/Libraries'))
sys.path.append(os.path.realpath('../../Components/Database-Manager'))

# Internal-Imports
from PrintLibrary import PrintLibrary
