# BOTS
Each 'bot' folder contains files and code that act as a independent sub-system. Each one uses aspects from the general libraries and components, but typically do not interact with each other. Below will be a synopsis of the current state of each bot for accurate record keeping. The shorthand format for each component is as follows:

```
Sample
General description goes here
Current big-picture task description
```

## Arbitrage
```
D:
Arbitrage is a trading sub-system that performs trades across exchanges leveraging the difference in price. There 
are two different types of arbitrage that run: limit-based and market-based. The first kind involves place trades 
that are intended to resolve over certain periods of time, for instance 15 minutes or 1 day. Once that period of 
time has elapsed, that program checks whether the trades have filled which denotes whether or not arbitrage has 
been successful. If the trades are not filled, it performs handling to minimize losses. This type of arbitrage
only needs to be run every so often, at the specified intervals. Market-based arbitrage is a free-running
algorithm: it runs all the time and attempts to perform arbitrage in the current state of the market.

C:
- New database integration
- Auto-balancing must be completed
- Limit arbitrage needs to be started
```
## Coin-Categorizer
```
D:
This system attempts to exploit the extreme, volatile swings of small & unknown cryptocurrencies. These cryptocurrencies in the past have
fluctuated to the degree that, in extreme cases, $100 becomes worth $1million over the course of a year. This is not the standard, however,
there seems to be a pattern of upswings that can be leveraged. This program will process an input CSV file ranking cryptocurrencies starting
below rank 100 [on coinmarketcap.com]. It then automatically makes a degree of small investments across the most attractive of these
cryptocurrencies, based on user definition. 

C:
- Test CSV file
- Parse cryptocurrencies
- Clean up comments
- Project org doc
```


## Fund-Manager
```
D:
Plays the part allocating the fund to various parts of the system and routine functions involving the fund. This includes tasks such as
liquidation, tracking value (and profit/loss) and others. 

C:
- TODO

```

## Market-Tracker
```
D:
Performs the task of tracking market data over time and performs polling of running algorithms. The main functionality is to track metrics
of the market in order to keep a granular record of the market for analysis, manipulation and testing. The secondary functionality, which
will be tackled further down the line, is to run a trimmed down version of each algorithm in order to test the efficacy of the algorithm
over a greater number of pairings relative to the main runtime. This allows the system controller to re-balance the fund to a different
algorithm that is more successful in the short term.

C:
- Re-evaluate and set up tracking skeleton (main metric tracking, algorith tracking)
- Main metric tracking script
- Adapt arbitrage polling script
- Database creation

```

## MA-Trader
```
D:
* Deferred to potential-garbazno

C:
* Deferred to potential-garbanzo
```

## Performance-Tracker
```
D:
Tracks the performance of the program in various ways from specific algorithms to TODO.

C:
- TODO
```
## System Controller
```
D: 
Top level portion that calls other sub-systems and manages interactions between them.

C:
- TODO
```
