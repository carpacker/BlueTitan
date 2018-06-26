import sys
sys.path.append("U:/Directory/Projects/BlueTitan/Components/Performance-Analysis")

import CoinbaseTxProcessor as TransactionProcessor

if __name__ == "__main__":
    TransactionProcessor.main(["poloniex", "binance", "bittrex"])
