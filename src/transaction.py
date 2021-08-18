class ExeInfo():
    
    def __init__(self, id_str, price, amount):
        self.id = id_str
        self.price = price
        self.amount = amount

class Transaction():

    def __init__(self, line):
        id_str, type_str, price, amount = line.split(',')
        # field from the csv file.
        self.id = id_str
        self.type = type_str
        
        self.is_market = False
        self.price = 0
        if price == 'Market':
            self.is_market = True
        else:
            self.price = float(price)

        self.amount = float(amount)
        self.curr_amount = float(amount)

        # did the transation executed successfully
        self.status = "Denied"
        # the price in which the transaction was executed.
        self.trans_price = -1

        self.trans_info = list()

    @property
    def total(self):
        total = 0
        for exe_info in self.trans_info:
            total += exe_info.price * exe_info.amount

        return total

    @property
    def avg_price(self):
        avg_price = 0
        #calc weighted price
        for exe_info in self.trans_info:
            avg_price += exe_info.price * exe_info.amount/self.amount
        
        return avg_price
        
    # try and execute the transaction.
    def execute(self, rate):
        self.trans_price = rate
        self.trans_info.append(ExeInfo("", self.trans_price, self.amount))
        if self.type == 'Buy':
            if self.price > rate:
                self.status = "Executed"
                return True
        
        elif self.type == 'Sell':
            if self.price < rate:
                self.status = "Executed"
                return True
        else:
            print('error in type:' + self.type)

        return False

    # try to match and execute transactions form matching list, starting from index "start_idx".
    # start buying/selling, each time reducing the amount that has been left in
    # matching list transactions. This function is taken into account that the matching list is
    #already ordered by price.
    # return the last index that we got so the next matching will start from that point.
    def match(self, match_list, start_idx):
        curr_idx = start_idx
        for trans in match_list[start_idx:]:
            # check if we can transfer the whole amount from trans to self
            if trans.curr_amount - self.curr_amount >= 0:
                # we can transfer the whole amount - execute and return the current index.
                tranfered_amount = self.curr_amount
                self.curr_amount = 0
                trans.curr_amount -= tranfered_amount
                self.trans_info.append(ExeInfo(trans.id, trans.price, tranfered_amount))
                self.status = "Executed"
                return curr_idx
            else:
                # the amount needed by self is bigger than the amount from trans
                # so we need to transfer what we can from trans and continue to the next
                # match on the matching list
                tranfered_amount = trans.curr_amount
                self.curr_amount -= tranfered_amount
                trans.curr_amount = 0
                self.trans_info.append(ExeInfo(trans.id, trans.price, tranfered_amount))
                curr_idx += 1
                self.status = "Executed"

    def report(self):
        report = {"status": self.status, "amount": str(self.amount), "price": str(self.avg_price), "total": str(self.total)}
        if self.is_market:
            order_report = [{"order": x.id, "amount": str(x.amount)} for x in self.trans_info]
            report['orders'] = order_report
        return report


