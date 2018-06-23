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
    buildFinalCSV(adjust_fifo_txs, profit_loss_list)


    
# FUNCTION: buildAddrDictionary
# INPUT: exchanges - [string, ...]
# OUTPUT: Dictionary
# DESCRIPTION:
#    Returns a dictionary with addresses as key to an exchange.
# NOTE: only grabs addresses for ETH, BTC, LTC                
def buildAddrDictionary(exchanges, assets):
    # Address Dict
    addr_dict = {}
    for exchange in exchanges:
        addresses = []
        for asset in assets:
            address = ExchangeAPI.getDepositAddress(exchange, asset)
            addr_dict[address['asset']] = (asset, exchange)

    return addr_dict

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
    exchange_addresses = buildAddrDictionary(exchanges, ["ETH", "LTC", "BTC"])
    print("hm", exchange_addresses)
    # 2. Iterate through transactions
    for transaction in transactions:
        type_trans = transaction[1]
        # For each type of transaction

        # WITHDRAWAL: Check the address against exchange addresses
        if type_trans == "Send":
            to_address = transaction[6]
            try:
                test = exchange_addresses[to_address]
                transaction[6] = "Transfer"
                print(transaction)
            except KeyError:
                pass
        # RECEIVE: Mark as transfer, possibly ignore
        elif type_trans == "Receive":
            pass
        elif type_trans == "Buy":
            pass
        elif type_trans == "Sell":
            pass
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
# NOTE: keep track of final value?
def calculateFIFOprofit(transactions):
    inputs = []
    outputs = []

    for row in transactions:
        if row[1] == 'buy':
            inputs.append(row)
        elif row[1] == 'sell':
            outputs.append(row) 

    # 2. While there are outputs still left to be acted over, calculate
    #     profit loss using FIFO methodology.
    running_profit = 0
    running_loss = 0

    total_in = 0
    total_out = 0

    ctr_flag = 2

    while len(outputs) > 0:

        # Control flag determines what elements to pop:
        # 2 - both
        # 1 - inputs
        # 0 - outputs
        if ctr_flag == 2:
            current_output = outputs.pop()
            current_input = inputs.pop()

        elif ctr_flag == 1:
            current_input = inputs.pop()

        elif ctr_flag == 0:
            current_output = outputs.pop()

        print("---- ITERATION " + str(len(outputs)) + "----")
        print("OUT:", outputs)
        print("IN:", inputs)
        print("CURRENT PROFIT:", running_profit)

        # CASE: Sell is larger - work through buys
        curr_value = float(current_output[2])
        print(current_input, current_output)
        while curr_value > float(current_input[2]):
            # Calculate the profit FILO
            orig_value = float(current_input[4]) * float(current_input[5])
            sell_value = float(current_input[4]) * float(current_output[5])
            profit_loss = sell_value - orig_value

            # Add to running profit, adjust current output's value for next iteration
            running_profit += profit_loss
            current_output[4] = float(current_output[4]) - float(current_input[4])
            curr_value = float(current_output[2]) - sell_value
            print(orig_value,sell_value,profit_loss,running_profit,curr_value)

            # Set control flag to pop input
            current_input = inputs.pop()
            time.sleep(3)

        # CASE: Buy is larger, continue loop 
        orig_value = float(current_output[4]) * float(current_input[5])
        sell_value = float(current_output[4]) * float(current_output[5])
        profit_loss = sell_value - orig_value

        # Add to running profit, adjust current output's value for next iteration
        running_profit += profit_loss
        current_input[4] = float(current_input[4]) - float(current_output[4])
        print(orig_value,sell_value,profit_loss,running_profit)

        # Pop new input
        ctr_flag = 0
        time.sleep(3)           

def buildFinalCSV():
    pass
    # 1. Build any derivative data
    # 2. Create and write the actual CSV file

# FUNCTION: buildExchangeAddresses
# INPUT: exchanges - [string, ...]
#        assets    - [string, ...]
# OUTPUT: nested dictionary
# DESCRIPTION:
#    Takes an input of exchanges and assets, creates entry in database to keep track of
#     wallet addresses, where static addresses are possible.
# NOTE: This function may not be necessary, some other functino does this job perhaps
def buildExchangeAddresses(exchanges, assets):
    pass

# FUNCTION: storeTxCSV
# INPUT: transactions - [(txdata1, ...), ...]
# OUTPUT: N/A
# DESCRIPTION:
#    Takes sorted list of transactinos (chronologically) and stores them in the appropiate
#     database. Store each transaction individually. If using a single transaction, it
#     must be contained in a list until a better solution is devised.
def storeTxs(transactions):
    pass
