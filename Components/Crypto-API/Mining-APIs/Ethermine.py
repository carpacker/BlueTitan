# ETHERMINE API
# URL: https://api.ethermine.org/docs/#api-Pool
# RATE LIMIT: Only need to check every ~2 minutes maximum

# External Imports
import requests
import time

# Internal Imports
from PrintLibrary import PrintLibrary

#                                        GLOBAL 
# *  getPoolstats  -
# *  getBlockStats -

# FUNCTION: getPoolstats
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#	Returns statistics for the pool (top miners, mined blocks, price and other general info)
def getPoolStats():
    json_var = requests. request('GET', 'https://api.ethermine.org/poolStats').json()
    print(json_var)
    if json_var["status"] == 'OK':
        json_var2 = json_var["data"]

        # miner (string), hashRate(float)
        top_miners = json_var2["topMiners"]
        # number (BLOCK number), miner (string), time(int)
        mined_blocks = json_var2["minedBlocks"]
        # hashrate(number), miners(int), workers(int)
        pool_stats = json_var2["poolStats"]
        # usd(number), btc(number)
        price = json_var2["price"]

        red_dict = {
        "success" : True,
        "api" : 'ethermine',
        "top_miners" : top_miners,
        "mined_blocks" : mined_blocks,
        "pool_stats" : pool_stats,
        "price" : price
        }
    else:
        ret_dict ={
        "success" : False,
        "api" : 'ethermine'
        }

    return json_var

# FUNCTION: getBlockStats
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#	Get statistics for the current block
def getBlockStats():
    json_var = requests.request('GET', 'https://api.ethermine.org/blocks/history').json()

    if json_var["status"] == "OK":
        json_var2 = json_var["data"]
        time = json_var2["time"]
        block_count = json_var2["nbrBlocks"]
        difficulty = json_var2["difficulty"]

        red_dict = {
        "success" : True,
        "api" : 'ethermine',
        "time" : time,
        "block_count" : block_count,
        "difficulty" : difficulty
        }
    else:
        ret_dict ={
        "success" : False,
        "api" : 'ethermine'
        }

    return ret_dict   

# FUNCTION: getNetworkStats 
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#	Returns statistics for the network
def getNetworkStats():
    json_var = requests.request('GET', 'https://api.ethermine.org/networkStats').json()
    print(json_var)
    if json_var["status"] == "OK":
        json_var2 = json_var["data"]
        time = json_var2["time"]
        block_time = json_var2["blockTime"]
        difficulty = json_var2["difficulty"]
        hashrate = json_var2["hashrate"]
        usd = json_var2["usd"]
        btc = json_var2["btc"]

        ret_dict = {
        "success" : True,
        "api" : 'ethermine',
        "time" : time,
        "block_time" : block_time,
        "hashrate" : hashrate,
        "usd" : usd,
        "btc" : btc
        }
    else:
        ret_dict ={
        "success" : False,
        "api" : 'ethermine'
        }

    return ret_dict   

# FUNCTION: getHashrates
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#	Returns hash rate of your miners
def getHashrates():
    json_var = requests.request('GET', 'https://api.ethermine.org/servers/history').json()
    print(json_var)
    if json_var["status"] == "OK":
        json_var2 = json_var["data"]
        time = json_var2["time"]
        hashrate = json_var2["hashrate"]
        server = json_var2["server"]

        ret_dict = {
        "success" : True,
        "api" : 'ethermine',
        "time" : time,
        "hashrate" : hashrate,
        "serfer" : server
        }
    else:
        ret_dict ={
        "success" : False,
        "api" : 'ethermine'
        }

    return ret_dict   

# ---------------------------------------- MINER ----------------------------------------
# FUNCTION: getMinerHistory
# INPUT: miner - string
# OUTPUT: Dictionary
# DESCRIPTION:
#	
def getMinerHistory(miner):
	url = 'https://api.ethermine.org/miner/' + miner + '/history'
    json_var = requests.request('GET', url).json()
    print(json_var)
    if json_var["status"] == "OK":
        json_var2 = json_var["data"]
        time = Helpers.createTimestamp()
        reported_hashrate = json_var2["reportedHashrate"]
        average_hashrate = json_var2["averageHashrate"]
        current_hashrate = json_var2["currentHashrate"]
        valid_shares = json_var2["validShares"]
        invalid_shares = json_var2["invalidShares"] 
        stale_shares = json_var2["staleShares"]
        active_workers = json_var2["activeWorkers"]

        ret_dict = {
        "success" : True,
        "time" : time,
        "api" : 'ethermine',
        "miner" : miner,
        "reported_hashrate" : reported_hashrate,
        "average_hashrate" : average_hashrate,
        "current_hashrate" : current_hashrate,
        "valid_shares" = valid_shares,
        "invalid_shares" = invalid_shares,
        "stale_shares" = stale_shares,
        "active_workers" = active_workers
        }
    else:
        ret_dict ={
        "success" : False,
        "api" : 'ethermine'
        }

    return ret_dict   


# FUNCTION: getMinerPayouts
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#	Returns list of payouts from Ethermine
def getMinerPayouts(miner):
	url = 'https://api.ethermine.org/miner/' + miner + '/payouts'
    json_var = requests.request('GET', url).json()
    print(json_var)
    if json_var["status"] == "OK":
        json_var2 = json_var["data"]
        time = Helpers.createTimestamp()
        paid_on = json_var2["paidOn"]
        start = json_var2["start"]
        end = json_var2["end"]
        amount = json_var2["amount"]
        tx_hash = json_var2["txHash"]

        ret_dict = {
        "success" : True,
        "api" : 'ethermine',
        "time" : time,
        "miner" : miner,
        "paid_on" : paid_on,
        "start" : start,
        "end" : end,
        "amount" : amount,
        "tx_hash" : tx_hash
        }
    else:
        ret_dict ={
        "success" : False,
        "api" : 'ethermine'
        }

    return ret_dict   


# FUNCTION: getMinerRounds
# INPUT: miner - string
# OUTPUT: Dictionary
# DESCRIPTION:
#    TODO
def getMinerRounds(miner):
    url = 'https://api.ethermine.org/miner/' + miner + '/rounds'
    json_var = requests.request('GET', url).json()
    print(json_var)
    if json_var["status"] == "OK":
        json_var2 = json_var["data"]
        time = Helpers.createTimestamp()
        block = json_var2["block"]
        amount = json_var2["amount"]
        ret_dict = {
        "success" : True,
        "api" : "ethermine",
        "miner" : miner,
        "time" : time,
        "block" : block,
        "amount" : amount
        }
    else:
        ret_dict ={
        "success" : False,
        "api" : 'ethermine'
        }

    return ret_dict   

# FUNCTION: getMinerSettings
# INPUT: miner - string
# OUTPUT: Dictionary
# DESCRIPTION:
#	Returns the current settings for the address
def getMinerSettings(miner):
    url = 'https://api.ethermine.org/miner/' + miner + '/settings'
    json_var = requests.request('GET', url).json()
    print(json_var)
    if json_var["status"] == "OK":
        json_var2 = json_var["data"]
        time = Helpers.createTimestamp()
        email = json_var2["email"]
        monitor = json_var2["monitor"]
        min_payout = json_var2["minPayout"]
        ip = json_var2["ip"]

        ret_dict = {
        "success" : True,
        "api" : "ethermine",
        "miner" : miner,
        "time" : time,
        "email" : email,
        "monitor" : monitor,
        "min_payout" : min_payout,
        "ip" : ip
        }
    else:
        ret_dict ={
        "success" : False,
        "api" : 'ethermine'
        }

    return ret_dict  

# FUNCTION: getMinerStatistics
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#	
def getMinerStatistics():
    json_var = requests.request('GET', 'https://api.ethermine.org/networkStats').json()
    print(json_var)
    if json_var["status"] == "OK":
        json_var2 = json_var["data"]
        time = json_var2["time"]

        ret_dict = {
        "success" : True,
        "time" : time,
        "api" : "ethermine",
        "miner" : miner,
        
        }
    else:
        ret_dict ={
        "success" : False,
        "api" : 'ethermine'
        }

    return ret_dict   

# ---------------------------------------- Worker ----------------------------------------
# FUNCTION: getWorkStatisticsAll
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#	
def getWorkStatisticsAll():
    json_var = requests.request('GET', 'https://api.ethermine.org/networkStats').json()
    print(json_var)
    if json_var["status"] == "OK":
        json_var2 = json_var["data"]
        time = json_var2["time"]

        ret_dict = {
        "success" : True,
        "time" : time
        }
    else:
        ret_dict ={
        "success" : False,
        "api" : 'ethermine'
        }

    return ret_dict   

# FUNCTION: getWorkerHistory
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#
def getWorkerHistory():
    json_var = requests.request('GET', 'https://api.ethermine.org/networkStats').json()
    print(json_var)
    if json_var["status"] == "OK":
        json_var2 = json_var["data"]
        time = json_var2["time"]

        ret_dict = {
        "success" : True,
        "time" : time
        }
    else:
        ret_dict ={
        "success" : False,
        "api" : 'ethermine'
        }

    return ret_dict   

# FUNCTION: getWorkStatistics
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#
def getWorkerStatistics():
    json_var = requests.request('GET', 'https://api.ethermine.org/networkStats').json()
    print(json_var)
    if json_var["status"] == "OK":
        json_var2 = json_var["data"]
        time = json_var2["time"]

        ret_dict = {
        "success" : True,
        "time" : time
        }
    else:
        ret_dict ={
        "success" : False,
        "api" : 'ethermine'
        }

    return ret_dict   

# FUNCTION: getWorkerMonitor
# INPUT: N/A
# OUTPUT: Dictionary
# DESCRIPTION:
#
def getWorkerMonitor():
    json_var = requests.request('GET', 'https://api.ethermine.org/networkStats').json()
    print(json_var)
    if json_var["status"] == "OK":
        json_var2 = json_var["data"]
        time = json_var2["time"]

        ret_dict = {
        "success" : True,
        "time" : time
        }
    else:
        ret_dict ={
        "success" : False,
        "api" : 'ethermine'
        }

    return ret_dict   