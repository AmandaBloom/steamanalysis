from analise import Analiser
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import pyqtSlot, Qt, QTimer, QObject, QAbstractTableModel
import analiser_window_ui as analiser_window_ui
import pandas as pd
import webbrowser
import sys

class TableWidget(QTableWidget):
    def __init__(self, df, item_table, parent=None):
        QTableWidget.__init__(self, parent)
        self.df = df
        self.item_table = item_table
        self.nRows = len(self.df.index)
        self.nColumns = len(self.df.columns)
        self.setRowCount(self.nRows)
        self.setColumnCount(self.nColumns)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setHorizontalHeaderLabels(list(self.df.columns))
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.stylesheet = """
QTableWidget
{
background: #e9e9e9;
selection-color: black;
border: 1px solid lightgrey;
selection-background-color: rgba(209, 255, 82, 50%);
color: black;
outline: 0;
} 
QTableWidget::item::focus
{
background: rgba(159, 186, 86, 50%);
border: 1px solid black;
}
"""
        self.setStyleSheet(self.stylesheet)

        self.setItems(df)


        # self.cellChanged.connect(self.onCellChanged)
        self.cellClicked.connect(self.clickedAction)
    

    def setItems(self, df):
        self.df = df
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                cell = self.df.iloc[i, j]
                if type(cell) == float:
                    cell ='{:.2f}'.format(cell)

                cell = str(cell)
                self.setItem(i, j, QTableWidgetItem(cell))

    def colorColumn(self, column_name):
        column = self.df.columns.get_loc(column_name)
        for i in range(self.rowCount()):
            if self.df.iloc[i, column] > 0:
                self.item(i, column).setBackground(QColor(0, 100, 0, 80))
            else:
                self.item(i, column).setBackground(QColor(100, 0, 0, 80))

    @pyqtSlot(int, int)
    def clickedAction(self, row, column):
        if column == 0:
            row = self.df.reset_index().loc[row]["level_0"]
            url = self.item_table.iloc[row, 1]
            webbrowser.open_new_tab(url)
            



    # @pyqtSlot(int, int)
    # def onCellChanged(self, row, column):
    #     text = self.item(row, column).text()
    #     number = float(text)
    #     self.df.set_value(row, column, number)


class AnaliserWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = analiser_window_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.sort_button.clicked.connect(self.sort)
        self.analiser = Analiser("src/generated.json")
        self.setupTable()
        self.ui.verticalLayout_2.addWidget(self.ui.tableWidget)

    def setupTable(self):
        self.df = self.analiser.pretty_table
        self.item_table = self.analiser.item_table
        self.ui.tableWidget = TableWidget(self.df, self.item_table, self)
        self.ui.tableWidget.setSortingEnabled(True)
        self.ui.tableWidget.colorColumn("profit")


    
    def sort(self):
        pass
        self.analiser.sort_by("profit")
        self.ui.tableWidget.setItems(self.analiser.pretty_table)
        self.ui.tableWidget.colorColumn("profit")
        pass


def guiMain(args):
    app = QApplication(args)
    window = AnaliserWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    guiMain(sys.argv)
