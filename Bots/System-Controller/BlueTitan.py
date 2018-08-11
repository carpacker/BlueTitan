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

# Relative path for imports
sys.path.append(os.path.realpath('../Arbitrage-Trader'))
sys.path.append(os.path.realpath('../Fund-Manager'))
sys.path.append(os.path.realpath('../../Components/Database-Manager'))
sys.path.append(os.path.realpath('../../Components/Libraries'))

# Internal-Imports
from ArbitrageMain import ArbitrageTrader
import DatabaseLibrary
from FundAllocator import FundAllocator
from GeneralizedDatabase import GenDatabaseLibrary
import Helpers
from PrintLibrary import PrintLibrary

# CLASS: BlueTitan
# DESCRIPTION:
#    Top level object for BlueTitan trading system.
class BlueTitan(object):

	# CLASS VARIABLES
	running_algos = []

	# INITIALIZATION: BlueTitan
	# INPUT: algorithms - list of algorithms desired to be running, additionally contains
	#                     information like acceptable exchanges and pairings to be run over.
	# DESCRIPTION:
	#    Performs initialization for BlueTitan trading system object. This includes base system
    #     database initialization, algorithm specific database initialization and scheduling for
    #     events.
    #
    #  The algorithm object in the algorithms is structure as follows:
    #  (alg_name, [pairings], [exchanges], (db_table_names), (table_exceptions))
	def __init__(self, algorithms, clean=True):
		PrintLibrary.header("BlueTitan Initialization")

        # Initialize databases for base functionalities
        
        # Runtime database
        DatabaseLibrary.initializeRuntimeDB()
        
        # FundAllocator database
        FundAllocator.initializeDatabase()
        
        # All metrics database
        PerformanceAnalysis.initializeDatabase()

        # Initialize databases for algorithms
		for algorithm in algorithms:
            PrintLibrary.displayVariables(algorithm)
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
				
		# if "IntendedFAE" not in orig_exceptions:
        #  BalancingLibrary.initializeFAE(assets, exchanges, class_balance_dict)

		# 2. Initialize scheduling events
        # NOTE: Change these, add more
        schedule.every().minute.do(ProfitTracker.runHourly, exchanges, assets)
        schedule.every().hour.do(ProfitTracker.runHourly, exchanges, assets)
        schedule.every().day.at("6:00").do(ProfitTracker.runDaily, exchanges, assets)

	# MAIN: BlueTitan
	# INPUT: N/A
	# OUTPUT: N/A
	# DESCRIPTION:
	#    Main loop for the top level. Starts off by creating relevant objects, then performs the
    #     continuous cycle of checking for scheduled events, rebalancing the fund when needed
    #     and otherwise running algorithms.
	def main(self):
        # Set algorithms
        algorithms = self.running_algos
        # Initialize fund allocator
        fund_allocator = FundAllocator(False)
        
		while 1:
            schedule.run_pending()
            
			# 1. Call fundAllocator to check for any changes
            fund_allocator.update()

            # 2. Run algorithms
            for algorithm in algorithms:
                # Each algorithm object is initialized with necessary variables; just calls main
                algorithm[0].main()

                # Future would potentially update algorithm local variables
                
if __name__ == "__main__":
	algorithms = []
    
    # ArbitrageTrader: market_exchanges, market_pairings, limit_exchanges, limit_pairings, assets
	algorithms.append(ArbitrageTrader(["Bittrex", "Binance"],
                                      ["BTC-KMD", "BTC-LTC", "BTC-ARK", "BTC-ADA", "BTC-XVG"],
                                      ["Bittrex", "Binance"],
                                      ["BTC-ETH"],
                                      ["ETH", "KMD", "BTC", "ARK", "ADA", "XVG"]))
	testbt = BlueTitan(algorithms).main()
