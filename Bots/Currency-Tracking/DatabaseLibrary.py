import sys
sys.path.append('C:/C-directory/Projects/Work-i/Bots/Arbitrage/Libraries')
sys.path.append('C:/C-directory/Projects/Work-i/Bots/Currency-Tracking')

# Internal-Imports
import time

# External-Imports
import Helpers

# FUNCTION: checkTableNameExists
# INPUT: table_name - string
# OUTPUT: N/A
#   Wrapper function to ensure that the table exists before performing an operation.
def checkTableNameExists(cursor, table_name, database):
    table_names = listTables(cursor)
    if table_name not in table_names:
        database.createTable(cursor, table_name)

# FUNCTION: createUUID
# INPUT: item_type - string
# OUTPUT: int
# DESCRIPTION:
#   Creates a unique identifier for a given trade, metric, transfer, etc.
def createUuid():
    # Use letter at beginning to designate what type of thing it is 
    return 0

class DatabaseLibrary(object):
    
    # ---------------------------------------- METRICS DATABASE ---------------------------------------

    # FUNCTION: initializeMetrics
    # INPUT: N/A
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Initializes the metrics table in the appropiate database.
    def initializeMetrics():
        table_name = MetricsDatabase.METRICS_TABLE_NAME
        connect, cursor = MetricsDatabase.connect()
        timestamp = Helpers.createTimestamp()
        uuid = createUuid()
        init_tuple = ("", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        checkTableNameExists(cursor, table_name, table_names)
        MetricsDatabase.insertMetric(cursor, timestamp, uuid, *init_tuple, table_name)
        disconnect(connect)

    # FUNCTION: initializeFailureMetrics
    # INPUT: N/A
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Initializes the failure metrics table in the appropiate database.
    def initializeFailureMetrics():
        table_name = MetricsDatabase.METRICSFAILURES_TABLE_NAME
        connect, cursor = MetricsDatabase.connect()
        timestamp = Helpers.createTimestamp()
        uuid = createUuid()
        init_tuple = ("", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        checkTableNameExists(cursor, table_name, MetricsDatabase)
        MetricsDatabase.insertFailureMetric(cursor, timestamp, uuid, *init_tuple, table_name)
        disconnect(connect)

    # FUNCTION: storeMetrics
    # INPUT: success_values - tuple
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Stores a metric entry.
    def storeMetric(success_values):
        table_name = MetricsDatabase.METRICS_TABLE_NAME
        connect, cursor = MetricsDatabase.connect()
        timestamp = Helpers.createTimestamp()
        uuid = createUuid()
        checkTableNameExists(cursor, table_name, MetricsDatabase)
        MetricsDatabase.insertMetric(cursor, timestamp, uuid, *success_values, table_name)
        disconnect(connect)

    # FUNCTION: storeFailureMetric
    # INPUT: failure_values - tuple
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Stores a failure metric entry.
    def storeFailureMetric(failure_values):
        table_name = MetricsDatabase.METRICSFAILURES_TABLE_NAME
        connect, cursor = MetricsDatabase.connect()
        timestamp = Helpers.createTimestamp()
        uuid = createUuid()
        checkTableNameExists(cursor, table_name, MetricsDatabase)
        MetricsDatabase.insertFailureMetric(cursor, timestamp, uuid, *failure_values, table_name)
        disconnect(connect)

    # --------------------------------------- ASSET METRICS  ---------------------------------------

    # FUNCTION: initializeAssetMetrics
    # INPUT: N/A
    # OUTPUT: N/A
    # DESCRIPTION:
    #   
    def initializeAssetMetrics():
        table_name = AssetMetricsDatabase.ASSETMETRICS_TABLE_NAME
        connect, cursor = AssetMetricsDatabase.connect()
        timestamp = Helpers.createTimestamp()
        uuid = createUuid()
        table_names = listTables(cursor)
        # Add session number to init tuple
        init_tuple = ("", "", "", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        checkTableNameExists(cursor, table_name, table_names)
        AssetMetricsDatabase.insertAssetMetric(cursor, timestamp, uuid, *init_tuple, table_name)
        disconnect(connect)

    # FUNCTION: initializeAssetMetricsFailure
    # INPUT: N/A
    # OUTPUT: N/A
    # DESCRIPTION:
    #   
    def initializeAssetMetricsFailure():
        table_name = AssetMetricsDatabase.ASSETMETRICSFAILURES_TABLE_NAME
        connect, cursor = AssetMetricsDatabase.connect()
        timestamp = Helpers.createTimestamp()
        uuid = createUuid()
        table_names = listTables(cursor)
        # Add session number to tuple, dont need in init probably
        init_tuple = ("", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        checkTableNameExists(cursor, table_name, table_names)
        AssetMetricsDatabase.insertAssetMetricFailure(cursor, timestamp, uuid, *init_tuple, table_name)
        disconnect(connect)

    # FUNCTION: storeAssetMetric
    # INPUT: success_values - tuple
    #        asset          - string
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Entry for single asset over period of time.
    def storeAssetMetric(success_values, asset):
        table_name = AssetMetricsDatabase.METRICSFAILURESASSET_TABLE_NAME
        connect, cursor = AssetMetricsDatabase.connect()
        timestamp = Helpers.createTimestamp()
        uuid = createUuid()
        checkTableNameExists(cursor, table_name, AssetMetricsDatabase)
        AssetMetricsDatabase.insertAssetMetric(cursor, timestamp, uuid, *success_values, asset, table_name)
        disconnect(connect)

    # FUNCTION: storeAssetFailureMetric
    # INPUT: success_values - tuple
    #        asset          - string
    # OUTPUT: N/A
    # DESCRIPTION:
    #   Entry for single asset over period of time.
    def storeAssetFailureMetric(failure_values, asset):
        table_name = AssetMetricsDatabase.METRICSFAILURESASSET_TABLE_NAME
        timestamp = Helpers.createTimestamp()
        uuid = createUuid()
        connect, cursor = AssetMetricsDatabase.connect()
        checkTableNameExists(cursor, table_name, AssetMetricsDatabase)
        AssetMetricsDatabase.insertFailureMetricsAsset(cursor, timestamp, uuid, *failure_values, asset, table_name)
        disconnect(connect)