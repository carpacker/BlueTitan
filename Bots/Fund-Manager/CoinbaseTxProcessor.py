# CoinbaseTxProcessor.py
# Carson Packer
# DESCRIPTION:
#    Specifically designed to process 2017's Coinbase transactions in order to distinguish profit
#     loss for taxes.

# External-Imports
import sys
import time
import os
import csv

sys.path.append('U:/Directory/Projects/Work/BlueTitan/Components/Crypto-API/Exchange-APIs')
sys.path.append('U:/Directory/Projects/Work/BlueTitan/Components/Libraries')

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
    adjusted_fifo_txs = processTransactions(exchanges, chronological_txs)

    # 3. Calculate FIFO profit loss
    profit_loss_list = calculateFIFOprofit(adjusted_fifo_txs, ["ETH", "LTC", "BTC"])
    print(profit_loss_list)
    
    # 4. Build final CSV of all record
    buildFinalCSV("finalCSV.csv", adjusted_fifo_txs, profit_loss_list)

# FUNCTION: processTransactions
# INPUT: transactions - list
# OUTPUT: same list with entries edited
# DESCRIPTION:
#    Iterates through chronological list of transactions. Detects when certain withdrawals
#     are sent to addresses of another exchange, denoting that it is not a proper sell
#     but instead a transfer. Marks any transfer that goes to a random address as a sell
#     and any transfer to another exchange as a transfer.
def processTransactions(exchanges, transactions):

    # 1. Retrieve exchange addresses from supported exchanges
    exchange_addresses = Helpers.buildAddrDictionary(exchanges, ["ETH", "LTC", "BTC"])
    
    # 2. Iterate through transactions
    for transaction in transactions:
        type_trans = transaction[1]
        # For each type of transaction

        # WITHDRAWAL: Check the address against exchange addresses
        if type_trans == "Send":
            to_address = transaction[6]
            try:
                test = exchange_addresses[to_address]
                transaction[1] = "Transfer"
                
            except KeyError:
                transaction[1] = "Sell"

    return transactions

# FUNCTION: calculateFIFOprofit
# INPUT: transactions - [transaction1, ...]
# OUTPUT: Dictionary
# DESCRIPTION:
#    Given a list of chronologically sorted transactions, calculates the profit loss up
#     until the last transaction. Provides a variety of dynamic functionalities. It
#     returns the total profit, total loss and then provides the P/L by asset. It deals
#     with Transfers by waiting for a receive, and summing  the profit from the time
#     anything left to when it came back.
def calculateFIFOprofit(transactions, assets):
    exchange_in = []
    exchange_out = []
	
    inputs = []
    outputs = []

    profit_loss = 0
    # Places BUYs and SELLs into their own lists.
    for row in transactions:

        if row[1] == 'Buy':
            inputs.append(float(row[5]))
        elif row[1] == 'Sell':
            outputs.append(float(row[5]))
        elif row[1] == 'Transfer':
            print("TRANSFERS", row)
            outputs.append(float(row[5]))
            exchange_in.append(float(row[5]))
        elif row[1] == 'Receive':
            print(row)
            inputs.append(float(row[5]))
            exchange_out.append(float(row[5]))

    input_volume = Helpers.sumValues(inputs)
    sell_volume = Helpers.sumValues(outputs)
    return_exchange = Helpers.sumValues(exchange_out)
    off_exchange = Helpers.sumValues(exchange_in)
    
    print(input_volume, sell_volume)
    profit =  return_exchange - off_exchange + sell_volume - input_volume
    return profit

# FUNCTION: buildFinalCSV
# INPUT: filename         - string
#        adjusted_txs     -
#        profit_loss_list -
# OUTPUT: N/A
# DESCRIPTION
def buildFinalCSV(csv_name, adjusted_txs, profit):
    
    script_dir = os.path.dirname('U:/Directory/Projects/Work/BlueTitan/')
    full_path = os.path.join(script_dir, 'resources/CSV/' + csv_name)
    with open(full_path, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['DATE', 'TRANSACTION TYPE', 'ASSET', 'QUANTITY', 'PRICE', 'VALUE', 'ADDRESS[TO/FROM]'])
        writer.writerow(['-', 'PROFIT', 'ALL', '-', '-', profit, ''])
        time.sleep(10)
        for row in adjusted_txs:
            writer.writerow(row)

    csv_file.close()
    
	# 1. Write in final values at top
	# 1.5. Delimiter
	# 2. Add in adjusted transactions line by line
    pass
