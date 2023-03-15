import steammarket as sm
import time
from decimal import Decimal, getcontext
import json
import datetime
from printf import printf
getcontext().prec = 10  # Setting 10 digits precision for Decimal numbers

def open_json_file(path=""):
    file = open(path, "r", encoding='utf-8')
    return file


def load_data_file(path=""):
    logs = {}
    start_time = time.ctime()
    file = open_json_file(path)
    generated_file = open_json_file("src/generated.json")
    data = json.load(file)
    generated_data = json.load(generated_file)
    for item in data:
        
        requested_item = {'success': False}
        try:
            requested_item = sm.get_item(item)
        except sm.Raise429Error:
            time.sleep(100)
            requested_item = sm.get_item(item)
        except sm.RaiseUnableToCatchDataError as e:
            error_string = str(
                "On Item: " + item + " HTTP Code Number: " + str(e.error_code) + 
                "! Check https://en.wikipedia.org/wiki/List_of_HTTP_status_codes for more details!"
            )
            printf(error_string)
            logs[str(datetime.datetime.now())[:-7].replace(':', '')] = error_string

        if item not in generated_data:
            generated_data[item] = data[item]

        if requested_item != {'success': False}:

            price_now = Decimal(requested_item["lowest_price"][:-2].replace(',', '.')) 

            printf(price_now)
            earnded = price_now - Decimal(data[item]["buying_price"]).normalize() 
            printf("Earned" + str(earnded * data[item]["quantity"]))
            printf(str(item) + str(requested_item) + '\n')

            generated_data[item].update({start_time: str(price_now)})
    file.close()
    generated_file.close()
    return generated_data, logs

def save_market_info(data, path="src/gen.json"):
    with open(path, "w", encoding='utf-8') as output:
        json.dump(data, output, indent=4, ensure_ascii=False)

def save_logs(logs):
    with open("logs/log"+str(datetime.datetime.now())[:-7].replace(':', '')+".log", "w", encoding='utf-8') as output:
        json.dump(logs, output, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    data, logs = load_data_file(path = "src/item_data.json")
            
    save_market_info(data)
    if logs != {}:
        save_logs(logs)
    a = input("Press ANY key to shutdown")
