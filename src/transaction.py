class transaction():

    def __init__(self, line):
        id_str, type_str, price, amount = line.split(',')
        # field from the csv file.
        self.id = id_str
        self.type = type_str
        self.price = price
        self.amount = int(amount)

        # did the transation executed successfully
        self.status = "Denied"
        # the price in which the transaction was executed.
        self.trans_price = -1
        # total price of the transaction
        self.total = -1
    
    # try and execute the transaction.
    def execute(self, rate):
        self.trans_price = rate
        self.total = self.amount * rate
        if self.type == 'Buy':
            if self.price > rate:
                self.execute(rate)
                self.status = "Executed"
        
        elif self.type == 'Sell':
            if self.price < rate:
                self.execute(rate)
                self.status = "Executed"
        else:
            print('error in type:' + self.type)
        

    def to_json(self):
        return {self.id, {
            'status': self.status, 
            'amount': str(self.amount),
            'price': str(self.trans_price)
            'total': str()}
        }

