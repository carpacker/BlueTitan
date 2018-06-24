# DatabaseLibrary.py (Arbitrage)
# Carson Packer
# DESCRIPTION:
#    Arbitrage's database library

# External-Imports
import sys

# WINDOWS main-desktop
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Web-Scrapers')
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Crypto-API/Exchange-APIs')
sys.path.append('U:/Directory/Projects/BlueTitan/Components/Database-Manager')

# WINDOWS laptop

# LINUX main-server

# Internal-Imports
from GeneralizedDatabase import GenDatabaseLibrary
from API import ExchangeAPI
import FeeScraper

# Local Variables
path = os.path.join(os.path.dirname(__file__), 'ArbitrageDatabase.sqlite3')
table_names = []

# FUNCTION: createTable
# INPUT: cursor       - *
#        table_name   - string
#        table_tuples - (column_name, column_type, 'NULL'||'NOT NULL')
# OUTPUT: creates SQL table
# DESCRIPTION:
#   Creates a given table based on input. Can create a new table, if trying to create
#    a specific table it checks for that table to create.
def createTable(cursor, table_name, table_tuples=None):
    if table_name == "ArbitrageTrades":
        sql_s = """
        CREATE TABLE %s (
            Time_stamp text NOT NULL,
            Uuid text NOT NULL,
            Symbol text NOT NULL,
            Total_quantity real NOT NULL,
            Total_btc real NOT NULL,
            Executed_quantity real NOT NULL,
            Buy_exchange text NOT NULL,
            Sell_exchange text NOT NULL,
            Avg_buy_rate real NOT NULL,
            Avg_sell_rate real NOT NULL,
            Profit_ratio real NOT NULL,
            Profit real NOT NULL)
        """ % table_name
    elif table_name == "FailureTrades":
        sql_s = """
        CREATE TABLE %s (
            Time_stamp text NOT NULL,
            Uuid text NOT NULL,
            Symbol text NOT NULL,
            Total_quantity real NOT NULL,
            Total_btc real NOT NULL,
            Buy_exchange text NOT NULL,
            Sell_exchange text NOT NULL,
            Avg_buy_rate real NOT NULL,
            Avg_sell_rate real NOT NULL,
            Profit_ratio real NOT NULL,
            Profit real NOT null,
            Failed_exchange text NOT NULL,
            Stage text NOT NULL,
            Consecutive_fails integer NOT NULL)
        """ % table_name
    elif table_name == "AccountBalances":
        sql_s = """
        CREATE TABLE %s (
            id integer PRIMARY KEY,
            Exchange text NOT NULL,
            Asset text NOT NULL,
            Amount real NOT NULL,
            Btc_value real NOT NULL,
            Usd_value real NOT NULL)
        """ % table_name       
    elif table_name == "IntendedFAE":
        sql_s = """
        CREATE TABLE %s (
            Exchange text NOT NULL,
            Asset text NOT NULL,
            Proportion_as real NOT NULL, 
            Proportion_ex real NOT NULL)
        """ % table_name
    elif table_name == "BalancingHistory":
        sql_s = """
        CREATE TABLE %s (
            Time_stamp integer NOT NULL,
            Transfer_time integer NOT NULL,
            Buy_exchange text NOT NULL,
            Asset  text NOT NULL,
            Amount  real NOT NULL, 
            Sell_exchange text NOT NULL,
            Base_t_asset text NOT NULL,
            Base_btc_value real NOT NULL,
            Total_btc real NOT NULL,
            Fee_btc real NOT NULL,
            Buy_withdraw_id text NOT NULL,
            Sell_withdraw_id text NOT NULL)
        """ % table_name
    elif table_name == "AssetInformation":
        sql_s = """
        CREATE TABLE %s (
            Asset text NOT NULL,
            Exchange text NOT NULL,
            Address text NOT NULL,
            Tag text NOT NULL,
            Fee real NOT NULL,
            USDFee real NOT NULL)
        """ % table_name
    elif table_name == "Errors":
        sql_s = """
        CREATE TABLE %s (
            id integer PRIMARY KEY,
            Time_stamp text NOT NULL,
            Error text NOT NULL,
            Code text NOT NULL,
            Type text NOT NULL)
        """ % table_name              
    else:
        if table_tuples is None:
            table_tuples = []
        sql_s = """
        CREATE TABLE %s (
            id integer PRIMARY KEY)""" % table_name
        for col_tuple in columns:
            added_s = ",%s %s %s" % col_tuple
        sql_s += added_s
    cursor.execute(sql_s)

# FUNCTION: initializeTables
# INPUT: N/A
# OUTPUT: N/A
# DESCRIPTION:
#    Wrapper to initialize each table in the database.
# NOTE: What to do about FAE...
# NOTE: Future will probably move the two special initializes to separate information
#        database, making this initialize call into something that only needs to call
#        generic initializes.
def initializeTables(self, assets, exchanges):

    # Initialize special tables
    initializeBalances(exchanges)
    initializeAssetInfo(assets, exchanges)
    
    # Generic filler initialize
    for table in table_names:
        # Temp fix
        if table_name != "Balances" or table_name != "AssetInformation":
            GenDatabaseLibrary.initializeTable(table)

# FUNCTION: initializeBalances
# INPUT: exchanges - [string, ...] : (list of exchanges to initialize database with)
# OUTPUT: {exchange : {Asset : balances, ...}, ...}
# DESCRIPTION:
#   Initializes the balances for each asset in the used exchanges. index into balance_dict 
#    using the notation: dict[exchange][asset].
def initializeBalances(exchanges):
    balance_dict = {}
    total_value = 0
    total_btc = 0

    for exchange in exchanges:
        exchange_usd = 0
        exchange_btc = 0
        api_balances = ExchangeAPI.getBalances(exchange)

            balance_dict[exchange] = defaultdict(int)
            balances = api_balances["balances"]
            for asset, values in balances.items():
                quantity = values["total_balance"]

                # 1. Calculate USD, BTC value
                # Hack to work around USDT problem for now
                if quantity > 0:
                    if asset == "USDT":
                        btc_value = 0
                        usd_value = 0
                    if asset == "BTC":
                        btc_value = quantity
                        usd_value = Helpers.usdValue(asset, quantity, exchange)
                    else: 
                        btc_value = Helpers.btcValue(asset, quantity, exchange)
                        usd_value = Helpers.usdValue(asset, quantity, exchange)

                    # 2. Filter out unattractive/not useful assets 
                    # Accounts for :
                    #   - Unlisted assets
                    #   - Micro-quantities
                    #   - Zero balances
                    if usd_value > 5:
                        total_value += usd_value
                        total_btc += btc_value
                        exchange_usd += usd_value
                        exchange_btc += btc_value

                        # 3. Store desirable results in database, append to return list
                        balance_dict[exchange][asset] = values["total_balance"]
                        GenDatabaseLibrary.storeEntry(exchange, asset, quantity, btc_value, usd_value)

        GenDatabaseLibrary.storeEntry(exchange, "ALL", "N/A", exchange_btc, exchange_usd)

    GenDatabaseLibrary.storeEntry("ALL", "ALL", "N/A", total_btc, total_value)
    balance_dict["ALL"] = defaultdict(int)
    balance_dict["ALL"]["total_value_usd"] = total_value
    balance_dict["ALL"]["total_value_btc"] = total_btc
    print(balance_dict)
    return balance_dict

# FUNCTION: initializeFAE
# INPUT: fae_list - [(asset, exchange, proportion), ...]
# OUTPUT: N/A
# DESCRIPTION:
#   Purpose is to fill up fae table with our currently used asset/exchanges
def initializeFAE(fae_list):
    for fae in fae_list:
        GeDatabaseLibrary.storeEntry("ArbitrageDatabase", "IntendedFAE", fae)

# FUNCTION: initializeAssetInfo
# INPUT: assets    - list of assets used
#        exchanges - list of exchanges used
# OUTPUT: list of (exchange, asset) where the request failed
# DESCRIPTION:
#    Initializes the database with deposit addresses.
def initializeAssetInfo(assets, exchanges):
    errors = []

    for asset in assets:
        time.sleep(1)
        for exchange in exchanges:
            # DICT1: deposit address, withdrawaltag(for some currencies only)
            dict1 = ExchangeAPI.getDepositAddress(exchange, asset) 
            if dict1["success"]:

                address = dict1["address"]
                if dict1["withdrawal_tag"] != None:
                    withdrawal_tag = dict1["withdrawal_tag"]
                else: 
                    withdrawal_tag = ""

                if exchange == "binance":
                    withdrawal_fee = FeeScraper.getFee(exchange, asset)
                    withdrawal_tag = dict1["withdrawal_tag"] 
                    usd_value = Helpers.usdValue(asset, withdrawal_fee)
                else:
                    dict2 = ExchangeAPI.getCurrencies(exchange)
                    withdrawal_fee = dict2["currencies"][asset]["transaction_fee"]
                    withdrawal_tag = ""
                    usd_value = Helpers.usdValue(asset, withdrawal_fee)
                GenDatabaseLibrary.storeEntry(cursor, asset, exchange, address, withdrawal_tag, withdrawal_fee, usd_value)
            else:
                errors.append((exchange,asset)) 
    return errors

# FUNCTION: getPairings
# INPUT: exchange - string
# OUTPUT: list of strings [pairing_one, ...]
# DESCRIPTION:
#   Outputs list of traded pairings by the program on a given exchange 
#    based on the database in use.
# TODO - same function but API.
def getPairings():
    pass

# FUNCTION: getBalances
# DESCRIPTION:
#    Returns dictionary of assets to balances.
# TODO: this may work differently 
def getBalances(exchange, assets):
    balance_dict = {}
    for asset in assets:
        balance_dict[asset] = GenDatabaseLibrary.getEntry("ArbitrageDatabase", "Balances",  asset, exchange)
    return balance_dict

# FUNCTION: getAllBalances
# INPUT: exchanges - [string, ...]
# OUTPUT: dictionary of balances - {TODO}
# DESCRIPTION:
#   Retrieves all the balances from the exchanges, includes a total balance calculation
# test this, maybe only the above or the below is necessary.
def getAllBalances(exchanges):

    balance_dict = {}
    for exchange in exchanges:
        balance_dict[exchange] = defaultdict(lambda: (0,0,0))
        quantity_list = ArbitrageDatabase.getCurrenciesAmounts(cursor,exchange)
        for tup in quantity_list:
            balance_dict[exchange][tup[0]] = (tup[1], tup[2], tup[3])

    # # Retrive values for totals
    total_value_usd = DatabaseLibrary.getBalance("ALL", "ALL", "USD")
    total_value_btc = DatabaseLibrary.getBalance("ALL", "ALL", "BTC")
    balance_dict["ALL"] = defaultdict(int)
    balance_dict["ALL"]["total_value_usd"] = total_value_usd
    balance_dict["ALL"]["total_value_btc"] = total_value_btc
    return balance_dict
