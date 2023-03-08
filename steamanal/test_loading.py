from steammarket import get_item
import time
from decimal import Decimal, getcontext
import json
getcontext().prec = 10  # Setting 10 digits precision for Decimal numbers

with open("src/item_data.json", "r") as file:
    data = json.load(file)
    for item in data:
        requested_item = get_item(item)
        if requested_item != {'success': False}:
            price_now = Decimal(requested_item["lowest_price"][:-2].replace(',', '.'))

            print(price_now)
            earnded = price_now - Decimal(data[item]["buying_price"]).normalize()
            print("Earned", earnded * data[item]["quantity"])
            print(item, requested_item, '\n')
            if "prices" in data[item]:
                data[item]["prices"][time.ctime()] = str(price_now)
            else:
                data[item]["prices"] = {time.ctime(): str(price_now)}
        else:
            if "prices" in data[item]:
                data[item]["prices"][time.ctime()] = "couldn't be loaded"
            else:
                data[item]["prices"] = {time.ctime(): "couldn't be loaded"}

with open("src/generated.json", "w") as output:
    json.dump(data, output)

