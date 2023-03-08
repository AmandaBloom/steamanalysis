import requests
import time

def make_request(name):
    url = 'http://steamcommunity.com//market/priceoverview'
    request_data = requests.get(
        url,
        params={
            'appid': 730,
            'market_hash_name': name,
            'currency': 6
        },
        # headers= {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'}
    )
    return request_data


def get_item(name):
    market_item  = make_request(name)
    time.sleep(1)
    while market_item.status_code == 429:
        market_item  = make_request(name)
        print("wyjebało!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        time.sleep(10)
    return market_item.json()
