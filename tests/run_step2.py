import os, sys, requests
with open(os.path.join(sys.path[0], 'step2.csv'), 'rb') as f:
    # r = requests.post('http://127.0.0.1:5000/api/trade', files={'step2.csv': f})
    r = requests.post('http://172.17.0.2:5000/api/trade', files={'step2.csv': f})
    print(r.text)