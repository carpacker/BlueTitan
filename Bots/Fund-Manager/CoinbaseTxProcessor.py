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
    adjusted_fifo_txs = processTransactions(exchanges, chronological_txs)

    # 3. Calculate FIFO profit loss
    profit_loss_list = calculateFIFOprofit(adjusted_fifo_txs)
    print(profit_loss_list)
    
    # 4. Build final CSV of all record
    buildFinalCSV(adjusted_fifo_txs, profit_loss_list)

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
                print(transaction)
                transaction[1] = "Sell"

        elif type_trans == "Receive":
            pass

        # ERROR CASE: TODO
        else:
            print(type_trans)
            return 'error'

    return transactions

# FUNCTION: calculateFIFOprofit
# INPUT: transactions - [transaction1, ...]
# OUTPUT: Dictionary
# DESCRIPTION:
#    Given a list of chronologically sorted transactions, calculates the profit loss up
#     until the last transaction.
# NOTE: maybe do it by asset?
def calculateFIFOprofit(transactions):
    inputs = []
    outputs = []
    exchange_in = []
    exchange_out = []
    
    # Places BUYs and SELLs into their own lists.
    for row in transactions:
        if row[1] == 'Buy':
            inputs.append(row)
        elif row[1] == 'Sell':
            outputs.append(row)
        elif row[1] == 'Transfer':
            print(row)
            outputs.append(row)
            exchange_in.append(row[5])
        elif row[1] == 'Receive':
            print(row)
            inputs.append(row)
            exchange_out.append(row[5])
    exchange_profit = sum(exchange_out) - sum(exchange_in)
    
    print(exchange_profit)
    
    # 2. While there are outputs still left to be acted over, calculate
    #     profit loss using FIFO methodology.
    running_profit = 0
    running_loss = 0
    ctr_flag = 1
    
    ticker = 0
    while len(outputs) > 0:
        print("Iteration #", ticker)
        
        # Control flag determines what elements to pop:
        if ctr_flag == 1:
            current_output = outputs[ticker]
            current_input = inputs[ticker]

        elif ctr_flag == 0:
            current_output = outputs[ticker]

        print("CURRENT PROFIT:", running_profit)
        
        # CASE: Sell is larger - work through buys
        curr_value = float(current_output[5])
        print("Current inputs, outputs", current_input, current_output)
        
        ticker_t = 0
        while curr_value >= current_input[5]:
            # Multiply asset by price, subtract asset from running
            orig_value = float(current_input[quantity]) * float(current_input[price])
            sell_value = float(current_input[quantity]) * float(current_output[price])
            running_profit += profit_loss
            current_output[4]  = float(current_output[quantity]) - float(current_input[quantity])
            curr_value = float(current_output[totalvalue]) - sell_value
            current_input = inputs.pop()
            time.sleep(1)
        
        # CASE: Buy is larger, continue loop

        # Multiple asset by price, subtract asset from running
        orig_value = float(current_output[quantity]) * float(current_input[price])
        sell_value = float(current_output[quantity]) * float(current_output[price])
        running_profit += profit_loss
        current_input[4]  = float(current_input[quantity]) - float(current_output[quantity])
        running_profit += profit_loss
        
        # Pop new input
        ctr_flag = 0
        ticker+=1
        time.sleep(3)


    final_profit = running_profit + exchange_profit
    return running_profit

def buildFinalCSV():
    pass
    # 1. Build any derivative data
    # 2. Create and write the actual CSV file
