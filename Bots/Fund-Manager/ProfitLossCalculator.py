# Profit loss calculator

# External-Imports
import sys
import time

sys.path.append()

# Internal-Imports
import ExchangeAPI
import Helpers
import PrintLibrary

# CLASS: TransactionProcessor
# DESCRIPTION:
#   Container for suite of functions that process the transactions across various exchanges.
class TransactionProcesser(Object):

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

        chronological_tx = []
        ticker = 0
        for exchange in exchanges:

            # TODO: fix input syntax
            transactions = ExchangeAPI.getTransactionHistory(exchange)
            processed_transactions = self.processTransactions(exchange, transactions)
            chronological_tx[ticker] = (exchange, processed_transactions)
            ticker += 1
        if order_by == 'exchanges':
            # Sort by alphabetical exchange
            sorted_exchanges = SortingLibrary.sortAlphabetically(chronological_tx)

            sorted_tx = []
            ticker = 0
            for exchange in sorted_exchanges:
                sorted_tx[ticker] = exchange[1]
                ticker += 1

            PrintLibrary.displayVariables(sorted_tx)
            return sorted_tx
        
        elif order_by == 'time':
            # Same thing but time
            return 0

        else:
            # TODO: Error handle
            return -1

        # FUNCTION: storeTxCSV
        # INPUT: transactions - [(txdata1, ...), ...]
        # OUTPUT: N/A
        # DESCRIPTION:
        #    Takes sorted list of transactinos (chronologically) and stores them in the appropiate
        #     database. Store each transaction individually. If using a single transaction, it
        #     must be contained in a list until a better solution is devised.
        def storeTxs(transactions):
            pass

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
