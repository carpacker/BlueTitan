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
TODO 

C:
Test CSV file
```


## Fund-Manager
```
D:
TODO

C:

```

## Market-Tracker
Visit all files, re-name and re-organize, set-up polling again

## MA-Trader

## System Controller
D: TODO

C: TODO
