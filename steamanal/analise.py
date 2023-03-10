import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from test_loading import open_json_file

class Analiser:
    def __init__(self, path) -> None:
        self.item_table = self.create_item_table(path)
        self.covert_item_table()
        self.create_latest_statistics_table()

    def create_item_table(self, path):
        file = open_json_file(path)
        item_table = pd.read_json(file.read())
        file.close()
        return item_table

    def covert_item_table(self):
        self.item_table = self.item_table.transpose()
        self.item_table = self.item_table.reset_index()

    def create_latest_statistics_table(self):
        self.pretty_table = self.item_table[["index", "quantity", "buying_price", self.item_table.iloc[:,-1].name]]
        self.pretty_table["value"] = pd.to_numeric(self.item_table.iloc[:,-1]) * self.item_table["quantity"]
        self.pretty_table["profit"] = self.pretty_table["value"] - self.pretty_table["quantity"] * self.pretty_table["buying_price"]

    
    def sort_by(self, column_name):
        self.pretty_table.sort_values(by=[column_name], ascending=False, inplace=True)
    
    def find_corresponding_item(self, index):
        return self.item_table.loc[[index]]



if __name__ == "__main__":
    analiser = Analiser("src/generated.json")