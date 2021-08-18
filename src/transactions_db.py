import csv
from transaction import Transaction
from exchangeratesapi import ExchangeRates

class TransactionsDB():
    def __init__(self):
        self.exchanges = ExchangeRates()

    # get a list of transactions and execute them.
    def execute_transactions(self, csvfile):
        #create a pending list of all "Market transactions"
        # they will be processed after all other transactions are done.
        trans_db = dict()
        trans_db['Buy'] = list()
        trans_db['Sell'] = list()
        trans_db['Denied'] = list()
        trans_db['Market'] = list()

        # first iterate over all non market transaction and try to execute
        for trans in self.transaction_list(csvfile):
            if trans.is_market:
                trans_db['Market'].append(trans)
            else:
                curr_rate = self.exchanges.get_rate()
                did_executed = trans.execute(curr_rate)
                if did_executed:
                    trans_db[trans.type].append(trans)
                else:
                    trans_db['Denied'].append(trans)


        # sort the buying from high to low
        trans_db['Buy'].sort(key=lambda x: x.avg_price, reverse=True)

        # sort the buying from low to high
        trans_db['Sell'].sort(key=lambda x: x.avg_price, reverse=False)

        # second, iterate over all pending (market) transactions and try to find
        # match
        curr_sell_idx = 0
        curr_buy_idx = 0
        for trans in trans_db['Market']:
            if trans.type == 'Buy' and len(trans_db['Sell']) > curr_sell_idx:
                curr_sell_idx = trans.match(trans_db['Sell'], curr_sell_idx)
            elif trans.type == 'Sell' and len(trans_db['Buy']) > curr_buy_idx:
                curr_buy_idx = trans.match(trans_db['Buy'], curr_buy_idx)

        return trans_db


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
