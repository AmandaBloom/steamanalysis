from steammarket import get_multiple, get_csgo_item

with open("src/item_names.txt", "r") as file:
    for name in file:
        print(get_csgo_item(name))

