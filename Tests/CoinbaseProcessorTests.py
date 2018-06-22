import sys
sys.path.append("U:/Directory/Projects/BlueTitan/Bots/Fund-Manager/")

from CoinbaseTxProcessor import TransactionProcessor

if __name__ == "__main__":
    TransactionProcessor.main(["Poloniex"])
