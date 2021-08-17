import requests
class ExchangeRates():
    
    EXCHANGE_URL = 'http://api.exchangeratesapi.io/v1/latest'
    EXCHANGE_PARAMS = {
        'access_key': 'd8ae73d38274fbf44d758e03560791c5',
        'symbols': 'EUR,USD'
    }

    def __init__(self):
        return

    def get_rate(self):
        r = requests.get(url = ExchangeRates.EXCHANGE_URL, params = ExchangeRates.EXCHANGE_PARAMS)
        response = r.json()
        return float(response['rates']['USD'])