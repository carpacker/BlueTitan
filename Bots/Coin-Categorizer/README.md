# Coin-Categorizer
The technical goal involves iterating through a list of cryptocurrencies with defined attributes,
give them an aggregate score based on these attributes, identify coins whic hare 'to be bought'
and then go through the API of whatever sites are necessary to buy them.

## Categories
Description here
- Coins are valued based on these categories

[Asset :  (PRICE, VOLUME, MARKETS, TIMELINE, SOCIAL_NEWS, WEBSITE,
               SOURCE_CODE, PRICE_MOV, MINEABLE, WHITEPAPER)]  
## Scoring System
Description here
- Go over the scoring system, the baseline & nuances

[ETH   :   (8, 10, 8, ...)] --> 8

## Pseudocode & flow
Part One: Coin ranker
 Dictionary for each grouping:
 OUTER DICTIONARY: [grouping : grouping_dict]
 INNER DICTIONARY: [currency : aggregate_score]
 FOR EACH GROUPING:
   Output aggregate score for a currency using logic functions
   FUNCTION(TUPLE)
       FUNCTION(PRICE) :: DO THIS TO SCORE
       FUNCTION(VOLUME) :: DO THIS TO SCORE (+1)
       RETURN AGGREGATE SCORE
   Add [currency : aggregate_score] to current grouping_dict

Part two
 INPUT: grouping dictionary from previous part
 OUTER DICTIONARY: [grouping : value_dict]
 INNER DICTIONARY: [currency : percentage_allocated]
 FOR each grouping
   allocate certain percentage of fund based on grouping type
   allocate percentage of grouping_fund to each currency based on aggregate_score
 Return outer dictionary to coinbuyer
 
## Allocation Method
Description here
-how funds will be allocated based on score.

## Acquiring Coins
Description here

INPUT:  dictionary of [grouping : [pairing : percentage_allocated]
        total value to be allocated
1. Check exchanges pairing is on
2. Allocate quantity based on input
3. Buy from exchange with API written
   a. Return error if exchange API doesn't exist
4. Validate buy went through
5. Store result in database
6. Move onto next coin

# TODO:
# - Minimum buy all coins (? $2, .0005 btc minimum)
# - Given list of coins, find all exchanges needed
# - First round buys all coins on exchanges that are already supported
# - Function that outputs BTC quantity required, function that transfers necessary funds to buy
#    all coins to appropiate exchanges
# - Logic functions should deal with percentage of total input

