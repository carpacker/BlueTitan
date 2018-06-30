# BlueTitan.py
# Carson Packer
# DESCRIPTION:
#    This is the top level script which manages and automates the flow of the program. It
#     initializes databases, controls the pipelines of flow and performs scheduling actions.

# External-Imports
import schedule
import sys
import threading
import time

# WINDOWS main-desktop
sys.path.append()

# WINDOWS laptop
#

# LINUX main-server
#

# Internal-Imports


class BlueTitan(object):

	# INITIALIZATION
	# INPUT:
	#  TODO
	# DESCRIPTION:
	#    Performs database initialization, sets up scheduling tasks
	def __init__(self, exchanges, pairings, clean=True):
		PrintLibrary.header("Initialization")

		# Pull assets from pairing
		assets = Helpers.convertPairingListAsset(pairings)
		
        PrintLibrary.displayVariables(exchanges, "Exchanges")
        PrintLibrary.displayVariables(assets, "Assets")
        PrintLibrary.displayVariables(pairings, "Pairings")

		# 1. Database initialization
        arbitrage_tables = ["AccountBalances", "BalancingHistory", "AssetInformation", "FailureTrades",
                            "IntendedFAE"]
         metrics_tables = ["Metrics", "FailureMetrics"]
         assetmetrics_tables = ["AssetMetrics", "AssetFailureMetrics"]
         databases = [("ArbitrageDatabase", ArbitrageDatabase, arbitrage_tables),
                       ("MetricsDatabase", MetricsDatabase, metrics_tables),
                       ("AssetMetricsDatabase", AssetMetricsDatabase, assetmetrics_tables)]


        orig_exceptions = ["ArbitrageTrades", "Metrics", "AssetInformation", "FailureTrades", "BalancingHistory"]
        exceptions = ["ArbitrageTrades", "Metrics", "AssetInformation", "FailureTrades", "BalancingHistory"]


        # Clean database [tables - exceptions]
        if clean == True:
            temporary solution for doing a complete database wipe when necessary
            superclean = False

             # Messy, only works since it gets added to table that then gets instantly deleted. Figure out workaround 
             #   for the future.
             fae_list = BalancingLibrary.initializeFAEProportions(assets, exchanges, True)

            for database_tuple in databases:
                PrintLibrary.displayVariables(database_tuple)
                set_tables = set(database_tuple[2])
                set_i_tables = set(DatabaseLibraryBase.listTablesDB(database_tuple[1]))

                print("Intended Tables: ", set_tables)
                print("Database tables", set_i_tables)
                PrintLibrary.delimiter()
                if (set_tables.issubset(set_i_tables) and set_tables.issuperset(set_i_tables)) or superclean==True:
                    exceptions = DatabaseLibraryBase.cleanDatabase(database_tuple[1], database_tuple[2])
                else:
                    exceptions = DatabaseLibraryBase.cleanDatabase(database_tuple[1], database_tuple[2], exceptions)

                DatabaseLibrary.initialize(exceptions, assets, exchanges)
				
        if "IntendedFAE" not in orig_exceptions:
            BalancingLibrary.initializeFAE(assets, exchanges, class_balance_dict)

		# 2. Initialize scheduling events
        schedule.every().minute.do(ProfitTracker.runHourly, exchanges, assets)
        schedule.every().hour.do(ProfitTracker.runHourly, exchanges, assets)
        schedule.every().day.at("6:00").do(ProfitTracker.runDaily, exchanges, assets)

		# 3. Run arbitrage algorithm
		# NOTE: only running algorithm for now
		BTArbitrage.
