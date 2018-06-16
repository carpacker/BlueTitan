# coinbase.py (API)
# Carson Packer
# DESCRIPTION:
#    Interface to coinbase's API.

# External Imports
import time
import md5
import hashlib

# Internal Imports
import PrintLibrary

base_url = "https://api.coinbase.com/v2/users/"

# User calls

def getUserID():
    # :user_id
    pass

def getUser():
    pass

def userAuth():
    pass

def updateUser():
    pass
####################################### ACCOUNT CALLS ############################################## 
####################################################################################################

# acccounts/:account_id
# Currency can be used instead of account_id
def getAccount():
    pass

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

# GET https://api.coinbase.com/v2/accounts/:account_id/transactions
# Possibly wrapper that only returns for one currency
def listTransactions():
    pass

# Show single transaction
# GET https://api.coinbase.com/v2/accounts/:account_id/transactions/:transaction_id
def showTransaction():
    pass

# TODO
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

# Data endpoints todo
# Payment methods todo

########################################## HELPERS #################################################
####################################################################################################
# TODO: auth method
