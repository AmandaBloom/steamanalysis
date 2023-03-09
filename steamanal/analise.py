import pandas as pd
from test_loading import open_json_file

class Analiser:
    def __init__(self, path) -> None:
        self.item_table = self.create_item_table(path)
        self.covert_item_table()
        self.pretty_table = self.create_latest_statistics_table()

    def create_item_table(self, path):
        file = open_json_file(path)
        item_table = pd.read_json(file.read())
        file.close()
        return item_table

    def covert_item_table(self):
        self.item_table = self.item_table.transpose()
        self.item_table = self.item_table.reset_index()

    def create_latest_statistics_table(self):
        table_to_show = self.item_table[["index", "quantity", "buying_price", self.item_table.iloc[:,-1].name]]
        table_to_show["value"] = pd.to_numeric(self.item_table.iloc[:,-1]) * self.item_table["quantity"]
        table_to_show["profit"] = table_to_show["value"] - table_to_show["quantity"] * table_to_show["buying_price"]
        return table_to_show


if __name__ == "__main__":
    analiser = Analiser("src/generated.json")
    pass