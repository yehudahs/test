import csv
from transaction import Transaction
from exchangeratesapi import ExchangeRates

class TransactionsDB():
    def __init__(self):
        self.exchanges = ExchangeRates()
        self.trans_list = list()

    # get a list of transactions and execute them.
    def execute_transactions(self, csvfile):
        for trans in self.transaction_list(csvfile):
            curr_rate = self.exchanges.get_rate()
            trans.execute(curr_rate)
            self.trans_list.append(trans)

    def transaction_list(self, csvfile):
        csvfile.seek(0)
        row=''
        for char in csvfile.read().decode("utf-8"):
            if char == '\n':
              yield Transaction(row)
              row = ''
              
            else:
                row += char
        
        if row:
            yield Transaction(row)
        return
