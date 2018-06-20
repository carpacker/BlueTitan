# Mining Database library

# CLASS: MiningDatabase
# createTable(), 
class MiningDatabase(object):
    path = 0
    table_names = []

    # FUNCTION: createTable
    def createTable(cursor, table_name, table_tuples=None):
        if table_name == "MiningProfits":
            sql_s = """
            CREATE TABLE %s (
                Time_stamp text NOT NULL,
                Mining_pool text NOT NULL,
                Primary text NOT NULL,
                Mined_primary real NOT NULL,
                Secondary text NOT NULL,
                Mined_secondary real NOT NULL)
            """ % table_name    
        elif table_name == "MiningStatistics":
            sql_s = """
            CREATE TABLE %s (
                Time_stamp text NOT NULL,
                Eth_difficulty real NOT NULL,
                Zec_difficulty real NOT NULL,
                Sc_difficulty real NOT NULL,
                Dcr_difficulty real NOT NULL)
            """ % table_name   
        elif table_name == "MiningMetrics":
            sql_s = """
            CREATE TABLE %s (
                Time_stamp text NOT NULL,
                Mining_pool text NOT NULL,
                Primary text NOT NULL,
                Mined_primary real NOT NULL,
                Secondary text NOT NULL,
                Mined_secondary real NOT NULL)
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

    # FUNCTION: initializeTables
    def initializeTables():
        pass
