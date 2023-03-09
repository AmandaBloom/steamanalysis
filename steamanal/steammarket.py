import requests
import time
import json
import datetime


class Raise429Error(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class RaiseUnableToCatchDataError(Exception):
    def __init__(self, code) -> None:
        super().__init__()
        self.error_code = code



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
    # market_item = {'success': False}
    market_item = make_request(name)
    time.sleep(1)
    if market_item.status_code == 429:
        raise Raise429Error
    if market_item.status_code == 200:
        return market_item.json()
    else:
        raise RaiseUnableToCatchDataError(market_item.status_code)
