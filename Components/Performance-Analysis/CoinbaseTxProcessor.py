# CoinbaseTxProcessor.py
# Carson Packer
# DESCRIPTION:
#    Specifically designed to process 2017's Coinbase transactions in order to distinguish profit
#     loss for taxes.

# External-Imports
import sys
import time

sys.path.append('U:/Directory/Projects/BlueTitan/Components/Crypto-API/Exchange-APIs')
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Libraries')

# Internal-Imports
import Coinbase
from API import ExchangeAPI
import Helpers
from PrintLibrary import PrintLibrary

# FUNCTION: main
# INPUT: exchanges - [string, ...]
# OUTPUT: N/A
# DESCRIPTION:
#   Top level function for converting a list of buys and sells into a FIFO
#    profit loss generator
def main(exchanges):
    # 1. Read input Coinbase CSV
    chronological_txs = Helpers.readCSV('CB2017.csv')

    # 2. Classify what to do with each transaction
    adjusted_fifo_txs = ProfitLibrary.processTransactions(exchanges, ["BTC", "LTC", "ETH"], chronological_txs)

    # 3. Calculate FIFO profit loss
    profit_loss_list = ProfitLibrary.calculateFIFOprofit(adjusted_fifo_txs)
    print(profit_loss_list)
    
    # 4. Build final CSV of all record
    buildFinalCSV(adjusted_fifo_txs, profit_loss_list)

def buildFinalCSV():
    pass
    # 1. Build any derivative data
    # 2. Create and write the actual CSV file
