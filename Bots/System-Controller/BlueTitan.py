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

# WINDOWS main-desktop, LINUX main-server
sys.path.append("U:/Directory/Projects/Work/BlueTitan/Components/Libraries")
sys.path.append("U:/Directory/Projects/Work/BlueTitan/Components/Database-Manager")
sys.path.append("U:/Directory/Projects/Work/BlueTitan/Bots/Fund-Manager")
sys.path.append("U:/Directory/Projects/Work/BlueTitan/Bots/Arbitrage-Trader")

# WINDOWS laptop
#sys.path.append()


# Internal-Imports
from FundAllocator import FundAllocator
from PrintLibrary import PrintLibrary
import Helpers
from ArbitrageMain import ArbitrageTrader
from GeneralizedDatabase import GenDatabaseLibrary

class BlueTitan(object):

	# CLASS VARIABLES
	running_algos = []

	# What to do with these guys
	arbitrage_tables = ["AccountBalances", "BalancingHistory", "AssetInformation", "FailureTrades",
                            "IntendedFAE"]
    metrics_tables = ["Metrics", "FailureMetrics"]
    assetmetrics_tables = ["AssetMetrics", "AssetFailureMetrics"]
    databases = [("ArbitrageDatabase", ArbitrageDatabase, arbitrage_tables),
                 ("MetricsDatabase", MetricsDatabase, metrics_tables),
                 ("AssetMetricsDatabase", AssetMetricsDatabase, assetmetrics_tables)]
    orig_exceptions = ["ArbitrageTrades", "Metrics", "AssetInformation", "FailureTrades", "BalancingHistory"]
    exceptions = ["ArbitrageTrades", "Metrics", "AssetInformation", "FailureTrades", "BalancingHistory"]

	# INITIALIZATION: BlueTitan
	# INPUT: algorithms - list of algorithms desired to be running, additionally contains
	#                     information like acceptable exchanges and pairings to be run over.
	# DESCRIPTION:
	#    Performs initialization for BlueTitan trading system object
	def __init__(self, algorithms, clean=True):
		PrintLibrary.header("BlueTitan Initialization")

        # Initialize databases for base functionalities
        # TODO
        
        # Initialize databases for algorithms
		for algorithm in algorithms:
			print(algorithm)
			self.running_algos.append(algorithm)

            pairings = algorithm[1]
			assets = Helpers.convertPairingListAsset(pairings)
			exchanges = algorithm[2]
		
			PrintLibrary.displayVariables(exchanges, "Exchanges")
			PrintLibrary.displayVariables(assets, "Assets")
			PrintLibrary.displayVariables(pairings, "Pairings")
			
			# Clean database [tables - exceptions]
			if clean == True:
				# temporary solution for doing a complete database wipe when necessary
				superclean = False

				# Messy, only works since it gets added to table that then gets instantly deleted. Figure out workaround 
				#   for the future.
				fae_list = BalancingLibrary.initializeFAEProportions(assets, exchanges, True)

				for database_tuple in databases:
					PrintLibrary.displayVariables(database_tuple)
					set_tables = set(database_tuple[2])
					set_i_tables = set(GenDatabaseLibrary.listTables(database_tuple[1]))

					PrintLibrary.displayVariables(set_table, "Intended Tables")
			        PrintLibrary.displayVariables(set_i_tables, "Database Tables")
					PrintLibrary.delimiter()
					if (set_tables.issubset(set_i_tables) and set_tables.issuperset(set_i_tables)) or superclean==True:
						exceptions = GenDatabaseLibrary.cleanDatabase(database_tuple[1], database_tuple[2])
					else:
						exceptions = GenDatabaseLibrary.cleanDatabase(database_tuple[1], database_tuple[2], exceptions)

					DatabaseLibrary.initialize(exceptions, assets, exchanges)
				
		if "IntendedFAE" not in orig_exceptions:
            BalancingLibrary.initializeFAE(assets, exchanges, class_balance_dict)

		# 2. Initialize scheduling events
        schedule.every().minute.do(ProfitTracker.runHourly, exchanges, assets)
        schedule.every().hour.do(ProfitTracker.runHourly, exchanges, assets)
        schedule.every().day.at("6:00").do(ProfitTracker.runDaily, exchanges, assets)

	# MAIN: BlueTitan
	# INPUT: N/A
	# OUTPUT: N/A
	# DESCRIPTION:
	#    
	def main(self):
        algorithms = self.running_algos
        fund_allocator = FundAllocator()
		while 1:
			# 1. Call fundAllocator
            # 2. Run algorithms
            for algorithm in algorithms:
                # Run each algorithm
			    # NOTE: only running algorithm for now
		
`

if __name__ == "__main__":
	algorithms = {}
	algorithm["Arbitrage"] = [("pairing1", ("exchange1", "exchange2"))]
	testbt = BlueTitan(algorithms).main()
