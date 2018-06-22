# Heuristic Processer 
'''

 Part 1: Processing Input
		Grabbing information from various databases
			What data is important?
			How can we test efficacy of extrapolation over the data?
			How do we validate certain data being 'more important' than other data?

Part 2: Evaluating Input
		Requires preset states [see, heuristic] that will eventually become 
		 a message [see, input] for components of the system
		Will entail a series of logic functions that decide
		
		Part 2.5: Heuristic Formation
			What heuristics are useful?
				Market movement, volume, ??? 
				inputs --> Market is moving down in this sector for next ??? period of time
			Databse stuff

Part 3: Messaging
		Sending this heuristic to components to derive meaning as an input

Part 4: Evaluation
		Assessing the effectiveness of the current heuristic formation system
		 (and set of heuristics)

 '''

 # Potentially top level functions
 def processInput():
 	pass

 def evaluateInput():
 	pass

 def formHeuristic():
 	pass

 def initiateDistribuition():
 	pass

# ------------------------------------ GENERAL HEURISTICS ------------------------------------
# VOLATILITY
#  Description goes here
# MARKET MOVEMENT
#  Description goes here
# SENTIMENT
#  Description goes here
# INTEREST
#  Description goes here
# CONGESTION
#  Description goes here

# FUNCTION: evaluateVolatility
# DESCRIPTION: 
#	Evaluate an asset's volatility and return an indicator of how volatile it is for a period of time
def evaluateVolatility(period):
	# Determine volatility using an algorithm that acts over data
	return volatility

def evaluateMarketMovem(period):
	pass

def evaluateSentiment():
	pass

def evaluateInterest():
	pass

def evaluateCongestion():
	pass

# ------------------------------------ COMPONENT BASED HEURISTICS------------------------------------
#
# These would be similar to the above, except they would be general performance indicators of various
# components in the working system (mining, bots and shit)