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
