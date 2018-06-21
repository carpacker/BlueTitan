# coinbase.py (API)
# Carson Packer
# DESCRIPTION:
#    Interface to coinbase's API.

# External Imports
import time
import hashlib
import hmac
import requests
import json

# Internal Imports
import PrintLibrary

from secret_keys import coinbase_public_key, coinbase_private_key
base_url = "https://api.coinbase.com/v2/"


######################################## USER CALLS ################################################ 
####################################################################################################

user_url = base_url + "users/"

def getTime():
    json_var = requests.request('get', base_url + 'time').json()
    print(time.time())
    return json_var

# FUNCTION: getUserID
# INPUT: user_id - string
# OUTPUT: dictionary
# DESCRIPTION:
#    Retrieves user information using id. Need id to access
def getUserID(user_id):
    url = user_url + user_id
    json_var = requests.request('GET', url).json()

    # TODO -] check error
    
    # Already in dictionary format because they love us.
    return json_var["data"]

# FUNCTION: getUser
# INPUT:
# OUTPUT:
# DESCRIPTION:
# 
def getUser():
    pass

# INPUT: userAuth
# OUTPUT:
# DESCRIPTION:
# 
def userAuth():
    pass

# INPUT:
# OUTPUT:
# DESCRIPTION:
#    Update user information,
def updateUser():
    pass
####################################### ACCOUNT CALLS ############################################## 
####################################################################################################
account_url = base_url + 'accounts'

# acccounts/:account_id
# Currency can be used instead of account_id
def getAccount():
    pass

# FUNCTION: getAccounts
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#    Lists current user's accounts to which auth method has access to.
def getAccounts():
    json_var = encryptRequest(True, 'GET', account_url)
    return json_var

# string, name, creates account
# POST
def createAccount():
    pass

# Promote account as primary account
# POST
# Accounts/:account_id/primary
def setActPrimary():
    pass

# PUT
# accounts/:account_uid
# Mostly update account name, name;string optional
def updateAccount(name=""):
    pass

# TODO
def deleteAccount():
    pass
# string name optional

########################################## ADDRESSES ###############################################
####################################################################################################

# get
# accounts/:account_id/addresses
# ADDRESSES one time use
def listAddresses():
    pass

# get
# accounts/:account_id/addresses/:address_id
# One time use
# coin addresses can be replaced in address_id
def showAddress():
    pass

#GET https://api.coinbase.com/v2/accounts/:account_id/addresses/:address_id/transaction
def listAddrTx():
    pass

# Name, string, optional label
# Post
# accounts/:account_id/addresses
def createAddress():
    pass

######################################## TRANSACTIONS ##############################################
####################################################################################################

# FUNCTION: listTransactions
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#    Wrapper function to call list transactions without an account id.
def listTransactions():
    account_id = getAccount()
    transactions = listTransactionsID(account_id)
    return transactions

# FUNCTION: listTransactionsID
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#    Returns a list of all transactions made on a given Coinbase account. This includes BUYS, SELLS,
#     TRANSFERS, DEPOSITS, WITHDRAWALS, etc.
# NOTE: Assumes one already has the account id through some manner.
def listTransactionsID(accountid):
    url = account_url + accountid + "/transactions"
    json_var = encryptRequest(True, 'GET', url)
    print(json_var)
    # OUTPUT STANDARDIZATION
    # TODO

    return ret_dict

# Show single transaction
# GET https://api.coinbase.com/v2/accounts/:account_id/transactions/:transaction_id
def showTransaction():
    pass

# FUNCTION: sendMoney
# INPUT: TBD
# OUTPUT: Dictionary
# DESCRIPTION:
#    Initiates a transfer to send money to another address or account.
def sendMoney():
    pass

# TODO
def internalTransfer():
    pass

# TODO
def requestMoney():
    pass

# ???
def completeRequest():
    pass

# TODO: cancels request
def cancelMoneyRq():
    pass


########################################## ORDERS ##################################################
####################################################################################################

# FUNCTION: buy
# INPUT: TBD
# OUTPUT: Dictionary
# DESCRIPTION:
#    Submits a general buy operation.
def buy():
    pass

# Possible list buys for currency
def listBuys():
    pass

def showBuy():
    pass

# TODO
def placeBuyOrder():
    pass

# TODO
def commitBuy():
    pass

def sell():
    pass

def listSells():
    pass

def showSell():
    pass

def placeSellOrder():
    pass

def commitSell():
    pass

########################################## DEPOSITS ################################################
######################################## WITHDRAWALS ###############################################
####################################################################################################
def deposit():
    pass

def listDeposits():
    pass

# FUNCTION:
# INPUT:
# OUTPUT:
# DESCRIPTION:
#  
def showDeposit():
    pass

def depositFunds():
    pass

def commitDeposit():
    pass

def withdraw():
    pass

def listWithdrawals():
    pass

def showWithdrawal():
    pass

def withdrawFunds():
    pass

def commitWithdrawal():
    pass

def getDepositWithdrawals():
    pass

# Data endpoints todo
# Payment methods todo

########################################## HELPERS #################################################
####################################################################################################

# FUNCTION: encryptRequest
# INPUT: signature - boolean
#        method    - string ['POST', 'GET', 'PUT', 'DELETE']
#        end       - string (url)
# OUTPUT: Encrypted url used for HTTPS request
def encryptRequest(signature, method, base_url, **query_vars):
    timestamp = str(int(time.time()))
    # Add queries and header
            
    queryString = "&".join(['%s=%s' % (key,value) for (key,value) in query_vars.items()])
    
    # Sign the transaction
    message = timestamp + method + '/v2/accounts' + queryString
    print(message)
    sig = hmac.new(coinbase_private_key.encode(),message.encode(),'sha256')
    signature = sig.hexdigest()
    
    header = { 'CB-ACCESS-KEY' : coinbase_public_key,
               'CB-ACCESS-SIGN' : signature,
               'CB-ACCESS-TIMESTAMP' : timestamp,
               'CB-VERSION' :'2018-06-21'}
               
    url = base_url + "" + queryString
    print(url)
    
    req = requests.request(method, url, headers=header).json()
    return req
