#   ArbitrageTrades : [Time_stamp, Uuid, Symbol, Total_quantity, Total_btc, Executed_qauntity
#                       Buy_exchange, Sell_exchange, Avg_buy_rate, Avg_sell_rate, Profit_ratio,
#                       Profit]


table_names = ["ArbitrageTrades", "FailureTrades", "AccountBalances", "IntendedFAE", "BalancingHistory",
                "AssetInformation"]

# FUNCTION: create_table
# INPUT: cursor       - *
#        table_name   - string
#        table_tuples - (column_name, column_type, 'NULL'||'NOT NULL')
# OUTPUT: creates SQL table
# DESCRIPTION:
#   Creates a given table based on input. Can create a new table, if trying to create
#    a specific table it checks for that table to create.
def createTable(cursor, table_name, table_tuples=None):
    print("ArbitrageDatabase: Initializing Table as ", table_name)
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
        for tup in table_tuples:
            added_s = ",%s %s %s" % tup
        sql_s += added_s
    ArbitrageDatabase.table_names.append(table_name)
    cursor.execute(sql_s)

# FUNCTION: initializeTrades
# INPUT: N/A
# OUTPUT: TODO
# DESCRIPTION:
#   Creates trade database if it doesn't already exist, places a filler trade to signify a new session.
def initializeTrades():
    connect, cursor = ArbitrageDatabase.connect()
    timestamp = Helpers.createTimestamp()
    table_name = ArbitrageDatabase.TRADE_TABLE_NAME
    init_tuple = (timestamp, "", 0, 0, 0, "", "", 0, 0, 0, 0)
    checkTableNameExists(cursor, table_name, ArbitrageDatabase)
    ArbitrageDatabase.insertTrade(cursor, "ArbitrageTrades", timestamp, init_tuple)
    disconnect(connect)

# FUNCTION: initializeFailureTrades
# INPUT: N/A
# OUTPUT: N/A
# DESCRIPTION:
#   Creates failure-trades database if it doesn't already exist, places a filler trade to
#    signify a new session.
def initializeFailureTrades():
    connect, cursor = ArbitrageDatabase.connect()
    timestamp = Helpers.createTimestamp()
    uuid = createSessionNum()
    # Market Arbitrage
    table_name = ArbitrageDatabase.MFAILURETRADES_TABLE_NAME
    checkTableNameExists(cursor, table_name, ArbitrageDatabase)
    init_tuple = ("", 0, 0, "", "", 0, 0, 0, 0, "", "", 0)
    ArbitrageDatabase.insertMFailure(cursor, timestamp, uuid, *init_tuple)
    disconnect(connect)

# FUNCTION: initializeBalances
# INPUT: exchanges - [string, ...] : (list of exchanges to initialize database with)
# OUTPUT: 'same kind of dictionary that getDbBalances returns'
# DESCRIPTION:
#   Initializes the balances for each asset in the used exchanges. index into balance_dict 
#    using the notation: dict[exchange][asset].
def initializeBalances(exchanges):
    connect,cursor = ArbitrageDatabase.connect()
    balance_dict = {}
    total_value = 0
    total_btc = 0

    for exchange in exchanges:
        exchange_usd = 0
        exchange_btc = 0
        api_balances = ExchangeAPI.getBalances(exchange)
        if api_balances["success"]:
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
                        DatabaseLibrary.storeBalance(exchange, asset, quantity, btc_value, usd_value)

        DatabaseLibrary.storeBalance(exchange, "ALL", "N/A", exchange_btc, exchange_usd)

    DatabaseLibrary.storeBalance("ALL", "ALL", "N/A", total_btc, total_value)
    balance_dict["ALL"] = defaultdict(int)
    balance_dict["ALL"]["total_value_usd"] = total_value
    balance_dict["ALL"]["total_value_btc"] = total_btc
    disconnect(connect)
    print(balance_dict)
    return balance_dict

# FUNCTION: initializeFAE
# INPUT: fae_list - [(asset, exchange, proportion), ...]
# OUTPUT: N/A
# DESCRIPTION:
#   Purpose is to fill up fae table with our currently used asset/exchanges
def initializeFAE(fae_list):
    connect, cursor = ArbitrageDatabase.connect()
    table_name = ArbitrageDatabase.FAE_NAME
    table_names = listTables(cursor)
    checkTableNameExists(cursor, table_name, table_names)
    for fae in fae_list:
        DatabaseLibrary.storeFAE(fae[0], fae[1], fae[2], fae[3])
    disconnect(connect)   

# FUNCTION: initializeTransferHistory
# INPUT: N/A
# OUTPUT: N/A
def initializeTransferHistory():
    connect, cursor = ArbitrageDatabase.connect()
    timestamp = Helpers.createTimestamp()
    table_name = ArbitrageDatabase.BALANCING_HISTORY_NAME
    table_names = listTables(cursor)
    # Add session number to init tuple
    init_tuple = (0, 0, 0, "", "", "", 0, 0, 0)
    checkTableNameExists(cursor, table_name, table_names)
    ArbitrageDatabase.insertTransfer(cursor, timestamp, *init_tuple, table_name)
    disconnect(connect)

# FUNCTION: initializeAssetInfoes
# INPUT: exchanges - list of exchanges used
#        pairing   - list of pairings used
# OUTPUT: list of (exchange, asset) where the request failedA
# DESCRIPTION:
#   Goes through a list of pairings & exchanges and fills up the depositaddress database
#    Initializes the database with deposit addresses.
def initializeAssetInfo(assets, exchanges):
    connect, cursor = ArbitrageDatabase.connect()
    errors = []
    table_name = ArbitrageDatabase.ASSET_INFO_NAME
    table_names = listTables(cursor)
    checkTableNameExists(cursor, table_name, table_names)
    print(assets)
    print(exchanges)

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
                ArbitrageDatabase.insertAssetInformation(cursor, asset, exchange, address, withdrawal_tag, withdrawal_fee, usd_value)
            else:
                errors.append((exchange,asset)) 
    disconnect(connect)
    return errors

# TODO
def initializeErrors():
    connect, cursor = ArbitrageDatabase.connect()
    timestamp = Helpers.createTimestamp()
    # Error values: error (text), code(text), type(text)
    input_tuple = ("N/A", "", "initialization")
    table_name = ArbitrageDatabase.ERROR_TABLE_NAME
    table_names = listTables(cursor)
    checkTableNameExists(cursor, table_name, table_names)
    createTable(cursor, table_name, timestamp, *input_tuple)
    disconnect(connect)

############################################################################################################

# FUNCTION: getPairings
# INPUT: exchange - string
# OUTPUT: list of strings [pairing_one, ...]
# DESCRIPTION:
#   Outputs list of traded pairings by the program on a given exchange 
#    based on the database in use.
# TODO - same function but API.
def getPairings():
    pass

# FUNCTION: getWithdrawalFee
# INPUT: asset      - string
#        exchange   - string
#        type_value - TODO
# OUTPUT: float
# DESCRIPTION: 
#   Grabs the withdrawal fee for a given asset on a given exchange from the
#    asset information database.
def getWithdrawalFee(asset, exchange, type_value = ""):
    connect, cursor = ArbitrageDatabase.connect()
    table_name = ArbitrageDatabase.ASSET_INFO_NAME
    table_names = listTables(cursor)
    checkTableNameExists(cursor, table_name, table_names)
    fee = ArbitrageDatabase.getWithdrawalFee(cursor, asset, exchange)
    if type_value == "BTC":     
        fee = Helpers.btcValue(asset, fee, exchange)
    disconnect(connect)
    return fee

# FUNCTION: getBalance
# INPUT: exchange - string
#        asset    - string
# OUTPUT: float
# DESCRIPTION:
#   Retrieves a balance for a given asset from the balance database.
# *If it returns -1, its unavailable
def getBalance(asset, exchange, type_value=""):
    connect, cursor = ArbitrageDatabase.connect()
    balance = ArbitrageDatabase.getBalanceAsset(cursor, asset, exchange)
    if type_value == "BTC":
        balance = ArbitrageDatabase.getBalanceBTCVal(cursor, asset, exchange)
    elif type_value == "USD":
        balance = ArbitrageDatabase.getBalanceUSDVal(cursor, asset, exchange)
    disconnect(connect)
    return balance  

# FUNCTION: getBalances
# * TODO flip assets and exchange for STOREBALANCE, UPDATEBALANCE, GETBALANCES
def getBalances(exchange, assets, cursor=None):
    if cursor == None:
        connect, cursor = ArbitrageDatabase.connect()
        balance_dict = {}
        for asset in assets:
            balance_dict[asset] = ArbitrageDatabase.getBalanceAll(cursor, asset, exchange)
        disconnect(connect)
        return balance_dict
    else:
        balance_dict = {}
        for asset in assets:
            balance_dict[asset] = ArbitrageDatabase.getBalanceAll(cursor, asset, exchange)
        return balance_dict

def getBalanceTotal(type_a): 
    connect, cursor = ArbitrageDatabase.connect()
    if type_a == "BTC":
        value = ArbitrageDatabase.getBalanceBTCVal(cursor, 'ALL', 'ALL')
    elif type_a == "USD":
        value = ArbitrageDatabase.getBalanceUSDVal(cursor, 'ALL', 'ALL')

    print("total", value)
    return value

# FUNCTION: GetAllBalances
# INPUT: exchanges - [string, ...]
# OUTPUT: dictionary of balances - {TODO}
# DESCRIPTION:
#   Retrieves all the balances from the exchanges, includes a total balance calculation
def getAllBalances(exchanges):
    connect,cursor = ArbitrageDatabase.connect()
    # TODO, check database exists shit

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