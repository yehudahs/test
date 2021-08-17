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
    if 'transactions.csv' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['transactions.csv']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        transactions = TransactionsDB()
        transactions.execute_transactions(file)
        message = {x.id: {"status": x.status, "price": x.trans_price, "total": x.total} for x in transactions.trans_list}
        # r = requests.get(url = EXCHANGE_URL, params = EXCHANGE_PARAMS)
        # extracting data in json format
        # data = r.json()
        # print('got data: ' + str(data))
        resp = jsonify(message)
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

if __name__ == "__main__":
    app.run()