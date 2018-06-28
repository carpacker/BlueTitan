import sys
sys.path.append("U:/Directory/Projects/BlueTitan/Bots/Fund-Manager")

import CoinbaseTxProcessor as TransactionProcessor

if __name__ == "__main__":
    TransactionProcessor.main(["poloniex", "binance", "bittrex"])
