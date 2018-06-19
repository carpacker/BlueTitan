# Profit loss calculator

# External-Imports
import sys
import time

sys.path.append('U:/Directory/Projects/BlueTitan/Components/Crypto-API/Exchange-APIs')
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Libraries')

# Internal-Imports
import ExchangeAPI
import Helpers
import PrintLibrary

# CLASS: TransactionProcessor
# DESCRIPTION:
#   Container for suite of functions that process the transactions across various exchanges.
class TransactionProcesser(Object):

    # FUNCTION: main
    # INPUT: exchanges - [string, ...]
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Top level function for converting a list of buys and sells into a FIFO
    #    profit loss generator
    def main(self, exchanges):
        # 1. Build the transaction CSV in chronological order
        chronological_txs = self.buildTxCSV(exchanges, "time")
        
        # 2. Determine which outputs AREN'T sells through deposit addresses
        adjusted_fifo_txs = self.processTransactions(exchanges, chronological_txs)
        
        # 3. Calculate FIFO profit loss
        profit_loss_list = self.calculateFIFOprofit(adjusted_fifo_txs)

        # 4. Build final CSV of all records
        self.buildFinalCSV(adjust_fifo_txs, profit_loss_list)
        
    # FUNCTION: buildTxCSV
    # INPUT: exchanges - [string, ...]
    #        order_by  - 'time' or 'exchange'
    # OUTPUT: list
    # DESCRIPTION:
    #   Takes a list of exchanges and builds a list of tuples containing transaction
    #    history. Each entry is a transaction. order_by input is used to determine
    #    what order to hold the transactions, if exchange is chosen, then there
    #    is a inner-order by time within exchange. Exchanges are ordered alphabetically.
    def buildTxCSV(self, exchanges, order_by):

        # First build deposits/withdrawals, don't sort them
        chronological_tx = []
        ticker = 0
        for exchange in exchanges:

            # Retrieves both deposit and withdrawals from both exchanges, deposits are stored first.
            transactions = ExchangeAPI.getDepositWithdrawals(exchange,
                                                             "as_is", "both")
            chronological_tx.append((exchange, transactions))

        # Next build Coinbase sells/buys
        coinbase_tx = Coinbase.listTransactions()
        chronological_tx.append(coinbase_tx)

        # Return sorted input/output
        if order_by == 'exchanges':
            
            # Sort by alphabetical exchange
            sorted_exchanges = SortingLibrary.sortAlphabetically(chronological_tx)

            # Next sort each exchange entry chronologically
            ticker = 0
            for value in sorted_exchanges:
                sorted_exchanges[ticker] = somethingSort(sorted_exchanges[ticker])
                ticker += 1

            print(sorted_exchanges)
            return sorted_exchanges
            
        elif order_by == 'time':
            chronological_tx = somethingSort(chronological_tx)
            print(chronological_tx)
            return chronological_tx
        
        else:
            # TODO: Error handle
            print("Error, not supported :order_by: input")
            return -1

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
            exchange_addresses = buildAddrDictionary(exchanges)
            # 2. Iterate through transactions
            for transaction in transactions:
                exchange = ""
                type_trans = ""
                # Check for withdrawals on Coinbase
                if type_trans == "withrawal" and exchange == "coinbase":
                    to_address = ""

        # FUNCTION: buildAddrDictionary
        # DESCRIPTION:
        #    Returns a dictionary with addresses as key to an exchange
        def buildAddrDictionary(exchanges):
            pass
        
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
            # 1. Build any derivative data
            # 2. Create and write the actual CSV file
            
        # FUNCTION: buildExchangeAddresses
        # INPUT: exchanges - [string, ...]
        #        assets    - [string, ...]
        # OUTPUT: nested dictionary
        # DESCRIPTION:
        #    Takes an input of exchanges an assets, creates entry in database to keep track of
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

# CLASS: ProfitCalculator
# DESCRIPTION:
#    Functions used to calculate the profit/loss of transactions using a csv input.
class ProfitCalculator(Object):

    def calculateProfits():
        pass

    def matchBuySell():
        pass

    def buildTxList():
        pass


if __name__ == "__main__":
    TransactionProcessor.main(['Poloniex'])
