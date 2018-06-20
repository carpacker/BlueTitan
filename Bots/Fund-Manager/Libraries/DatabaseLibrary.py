# ProfiT Tracking Database stuff
class AssetMetricsDatabase():
    path = os.path.join(os.path.dirname(__file__), 'AssetMetricsDB.sqlite3')

    def createTable(cursor, table_name, table_tuples=None):
        if table_name == "AssetMetrics":
            sql_s = """
            CREATE TABLE %s (                
                Time_stamp text NOT NULL,
                Uuid text NOT NULL,
                Asset text NOT NULL,
                Primary_sell_ex text NOT NULL,
                Primary_buy_ex text NOT NULL,
                Initial_balance real NOT NULL,
                End_balance real NOT NULL,
                Volume real NOT NULL,
                Volume_delta real NOT NULL,
                Profit_ratio real NOT NULL,
                Profit_ratio_delta real NOT NULL,
                Utilization real NOT NULL,
                Utilization_delta real NOT NULL, 
                Quantity_trades real NOT NULL,
                Quantity_trades_delta real NOT NULL)
            """ % table_name        
        elif table_name == "AssetFailureMetrics":
            sql_s = """
            CREATE TABLE %s (                
                Time_stamp text NOT NULL,
                Uuid text NOT NULL,
                Asset text NOT NULL,
                Stage text NOT NULL,
                Primary_sell_ex text NOT NULL,
                Primary_buy_ex text NOT NULL,
                Volume real NOT NULL,
                Volume_delta real NOT NULL,
                Profit_ratio real NOT NULL,
                Profit_ratio_delta real NOT NULL,
                Quantity_trades_f real NOT NULL,
                Quantity_trades_f_delta real NOT NULL,
                Avg_success_rate real NOT NULL,
                Avg_success_rate_delta real NOT NULL)
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

        
# CLASS: MetricsDatabase
class MetricsDatabase():

    def createTable(cursor, table_name, table_tuples=None):
        if table_name == "Metrics":
            sql_s = """
            CREATE TABLE %s (
                Time_stamp text NOT NULL,
                Uuid text NOT NULL,
                Pairings text NOT NULL,
                Initial_balance real NOT NULL,
                End_balance real NOT NULL,
                Volume real NOT NULL,
                Volume_delta real NOT NULL,
                Profit_ratio real NOT NULL,
                Profit_ratio_delta real NOT NULL,
                Profit real NOT NULL,
                Profit_delta real NOT NULL,
                Utilization real NOT NULL,
                Utilization_delta real NOT NULL,
                Quantity_trades real NOT NULL,
                Quantity_trades_delta real NOT NULL)
            """ % table_name
        elif table_name == "FailureMetrics":
            sql_s = """
            CREATE TABLE %s (
                Time_stamp text NOT NULL,
                Uuid text NOT NULL,
                Pairings text NOT NULL,
                Volume real NOT NULL,
                Volume_delta real NOT NULL,
                Profit_ratio real NOT NULL,
                Profit_ratio_delta real NOT NULL,
                Utilization real NOT NULL,
                Utilization_delta real NOT NULL, 
                Quantity_trades_f real NOT NULL,
                Quantity_trades_f_delta real NOT NULL,
                Quantity_stage1 real NOT NULL,
                Quantity_stage2 real NOT NULL,
                Avg_success_rate real NOT NULL,
                Avg_success_rate_delta real NOT NULL)
            """ % table_name   
        elif table_name == "ProfitMetrics":
            pass
        elif table_name == "LiquidationHistory":
            pass
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

    # FUNCTION: initializeTables
    def initializeTables(self):
        for table in self.table_names:
            pass
        
# CLASS: ExchangeRecords
class ExchangeRecords():
    path = 0
    table_names = []

# CLASS: HistoricalDatabase
class HistoricalDatabase():
    path = 0
    table_names = []
        
# CLASS: RunningDatabase
class RunningDatabase():
    pass

# CLASS: RuntimeDatabase
class RuntimeDatabase():
    pass
