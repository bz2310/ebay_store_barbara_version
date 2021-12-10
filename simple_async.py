import grequests
import requests
import json
from datetime import datetime


prod_urls = [
    'http://127.0.0.1:5000/api/products/1',
    'http://127.0.0.1:5000/api/products/2',
    'http://127.0.0.1:5000/api/products/3',
    'http://127.0.0.1:5000/api/products/4'
]


def t1():                       # Get all product names/ total money
    charity_store_valuation = 0
    total_money_per_seller = {}
    s = datetime.now()
    rs = (grequests.get(u) for u in prod_urls)
    print("rs",rs)
    x = grequests.map(rs)
    print("x", x)
    e = datetime.now()

    print("Asynchronous (Parallel) Composition")
    print("Elapsed time = ", e - s)

    for r in x:
        if r is None:
            continue
        #print('r', r)
        #print(r.content, r.url, r.status_code)

        prod = json.loads(r.content)
        #print('--=---')
        #print(prod)
        for p in prod:
            p_total_val = float(p['price']) * float(p['inventory'])
            charity_store_valuation += p_total_val
            total_money_per_seller[p['product_no']] = p_total_val

    print(total_money_per_seller)
    print("The charity store now has a valuation of ", charity_store_valuation, "!")



        
def t2():
                
    print('---------------------')  
    s = datetime.now()
    result = []
    charity_store_valuation = 0
    total_money_per_seller = {}
    for u in prod_urls:
        r = requests.get(u)
        result.append([u, r.status_code, r.content])

    e = datetime.now()

    print("Synchronous (Series) Composition")
    print("Elapsed time = ", e - s)

    for u,s,c in result:
        if s == 200:
            cJson = json.loads(c)
            p = cJson[0]
            p_total_val = float(p['price']) * float(p['inventory'])
            charity_store_valuation += p_total_val
            total_money_per_seller[p['product_no']] = p_total_val
            #print('---------------------')  
    print(total_money_per_seller)
    print("The charity store now has a valuation of ", charity_store_valuation, "!")

t1()
t2()
