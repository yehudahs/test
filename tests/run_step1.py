import os, sys, requests
with open(os.path.join(sys.path[0], 'step1.csv'), 'rb') as f:
    r = requests.post('http://127.0.0.1:5000/api/trade', files={'step1.csv': f})
    print(r.status_code)