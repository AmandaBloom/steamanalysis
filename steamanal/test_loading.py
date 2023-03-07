from steammarket import get_multiple, get_csgo_item
from decimal import Decimal, getcontext
import json
getcontext().prec = 10 # Setting 10 digits precision for Decimal numbers

with open("src/item_data.json", "r") as file:
    data = json.load(file)
    for item in data:
        requested_item = get_csgo_item(item)
        price_now = Decimal(requested_item["lowest_price"][:-2].replace(',', '.'))

        print(price_now)
        earnded = price_now - Decimal(data[item]["buying_price"]).normalize()
        print("Earned", earnded * data[item]["quantity"])
        print(requested_item)

