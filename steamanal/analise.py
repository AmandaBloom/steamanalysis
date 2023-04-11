import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from test_loading import open_json_file

class Analiser:
    
    def __init__(self, path) -> None:
        self.TAX = 0.1304   # tax given to steam from 100PLN
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
        self.pretty_table["net_val"] = (1 - self.TAX)*pd.to_numeric(self.item_table.iloc[:,-1]) #round((1 - self.TAX)*pd.to_numeric(self.item_table.iloc[:,-1]),2) #* self.item_table["quantity"]
        self.pretty_table["profit"] = self.pretty_table["quantity"] * (self.pretty_table["net_val"] - self.pretty_table["buying_price"])
        #self.pretty_table["tax"] = (self.pretty_table["value"] * self.TAX) / 100
        #self.pretty_table["netto"] = self.pretty_table["value"] - self.pretty_table["tax"]

    
    def sort_by(self, column_name):
        self.pretty_table.sort_values(by=[column_name], ascending=False, inplace=True)
    
    def find_corresponding_item(self, index):
        return self.item_table.loc[[index]]
    
    def get_profit_sum(self):
        return round(self.pretty_table["profit"].sum(), 2)

    #def get_tax_sum(self):
    #    return round(self.pretty_table["tax"].sum(), 2)

    def get_net_val_sum(self):
        return round((self.pretty_table["quantity"] * self.pretty_table["net_val"]).sum(), 2)

    #def get_netto_sum(self):
    #    return round(self.pretty_table["netto"].sum(), 2)
    
    def get_profit_precentage(self):
        return round((self.get_net_val_sum()/(self.get_net_val_sum() - self.get_profit_sum())) * 100, 2)



if __name__ == "__main__":
    analiser = Analiser("src/generated.json")