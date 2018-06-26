# BalancingTests.py
# Carson Packer
# DESCRIPTION:

# External-Imports
import sys
import time

# WINDOWS main-desktop
sys.path.append()

# WINDOWS laptop
# sys.path.append()

# LINUX main-server
# sys.path.append()

# Test-Imports
from PrintLibrary import PrintLibrary
from BalancingLibrary import BalancingLibrary

# TESTERS: Base functions
# DESCRIPTION:
#    Tests for functions that are considered low-level or base units for top-level.
def baseTesters():
    PrintLibrary.header("Base Functions")
    
    PrintLibrary.headerTwo("Transfer Quote")
    PrintLibrary.headerTwo("Transfer Base")

# TESTERS: Main functinos
# DESCRIPTION:
#    Tests for top-level functions.
def mainTesters():
    PrintLibrary.header("Main Tester")
        
        
if __name__ == '__main__':
    baseTesters()
    mainTesters()
