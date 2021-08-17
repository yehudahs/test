import csv
from src.transaction import Transaction
from src.exchangeratesapi import ExchangeRates

class TransactionsDB():
    def __init__(self, file_name):
        #save only the file name, don't load the data until it is used, row by row.
        self.file_name = file_name
        self.exchanges = ExchangeRates()
        self.trans_list = list()

    # get a list of transactions and execute them.
    def execute_transactions(self):
        for trans in self.transaction_list():
            curr_rate = self.exchanges.get_rate()
            trans.execute(curr_rate)
            self.trans_list.append(trans)

    def transaction_list(self):
        with open(self.file_name, "rb") as csvfile:
            datareader = csv.reader(csvfile)
            for row in datareader:
                trans = Transaction(row)
                yield trans