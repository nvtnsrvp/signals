import config
import csv

class Tickers:
    def __init__(self):
        self.tickers_path = config.tickers_path
        self.symbols = self.load()

    def load(self):
        print(f"Loading tickers from '{self.tickers_path}'")
        with open(self.tickers_path, mode='r') as tickers_csv:
            reader = csv.DictReader(tickers_csv)
            return set(row['Symbol'] for row in reader)
    

if __name__ == "__main__":
    tickers = Tickers()
    print(tickers.symbols)