import os
import urllib.request
import requests
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename

from transactions_db import TransactionsDB

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['csv'])
EXCHANGE_URL = 'http://api.exchangeratesapi.io/v1/latest'
EXCHANGE_PARAMS = {
    'access_key': 'd8ae73d38274fbf44d758e03560791c5',
    'symbols': 'EUR,USD'
}
# exchange_url = http://api.exchangeratesapi.io/v1/latest?access_key=d8ae73d38274fbf44d758e03560791c5&symbols=EUR,USD

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/trade', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if len(request.files) != 1:
        resp = jsonify({'message' : 'too much or no files error, need to have only 1 file'})
        resp.status_code = 400
        return resp

    for filename, file in request.files.items():
        print("working on " + filename)
        if file and allowed_file(file.filename):
            transactions = TransactionsDB()
            trans_db = transactions.execute_transactions(file)
            buy_dict = {x.id: x.report() for x in trans_db['Buy']}
            sell_dict = {x.id: x.report() for x in trans_db['Sell']}
            denied_dict = {x.id: x.report() for x in trans_db['Denied']}
            market_dict = {x.id: x.report() for x in trans_db['Market']}
            return_msg = {**buy_dict, **sell_dict, **denied_dict, **market_dict}
            # r = requests.get(url = EXCHANGE_URL, params = EXCHANGE_PARAMS)
            # extracting data in json format
            # data = r.json()
            # print('got data: ' + str(data))
            resp = jsonify(return_msg)
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({'message' : 'Allowed file types are .csv'})
            resp.status_code = 400
            return resp

if __name__ == "__main__":
    app.run()