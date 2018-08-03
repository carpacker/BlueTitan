# FrontendTest.py
#  BlueTitan Trading System
#  Testing Suite for Front End Component
#  Carson Packer
# DESCRIPTION:
#    Tester file for frontend. Builds a screen which allows one to cycle through test widgets,
#     one must input a test widget to the tester class.

# External-Imports
import os
import sys
import time

# Relative path for imports
sys.path.append(os.path.realpath('../../Components/Front-End/'))
sys.path.append(os.path.realpath('../../Components/Libraries'))
sys.path.append(os.path.realpath('../../Components/Database-Manager'))

# Internal-Imports
from PrintLibrary import PrintLibrary
import Helpers
import TradingApp
import CentralApp
import MarketTrkApp

# Run each app, test  for a time, add buttons to switch to next app, or have own toolbar or something

if __name__ == "__main__":
    # TODO: Run the front end
    
