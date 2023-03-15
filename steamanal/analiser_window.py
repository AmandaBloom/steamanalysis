from analise import Analiser
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QColor, QImage, QPixmap
import requests
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
        self.sortBy = "index"
        self.ui = analiser_window_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.sort_button.clicked.connect(self.sort)
        self.analiser = Analiser("src/generated.json")
        self.setupTable()
        self.ui.verticalLayout_2.addWidget(self.ui.tableWidget)
        self.ui.profit_label.setText(str(self.analiser.get_profit_sum()) + "zł")
        self.ui.tax_label.setText(str(self.analiser.get_tax_sum()) + "zł")
        self.ui.netto_label.setText(str(self.analiser.get_netto_sum()) + "zł")
        self.ui.profit_precentage_label.setText(str(self.analiser.get_profit_precentage()) + "%")

        self.ui.comboBox.activated[str].connect(self.changedSortBy)
        self.setup_combobox()
        self.temp_window = TempWindow(self)
        self.temp_window.show()


    def setupTable(self):
        self.df = self.analiser.pretty_table
        self.item_table = self.analiser.item_table
        self.ui.tableWidget = TableWidget(self.df, self.item_table, self)
        self.ui.tableWidget.setSortingEnabled(True)
        self.ui.tableWidget.colorColumn("profit")

    def sort(self):
        pass
        self.analiser.sort_by(self.sortBy)
        self.ui.tableWidget.setItems(self.analiser.pretty_table)
        self.ui.tableWidget.colorColumn("profit")
        pass

    def setup_combobox(self):
        self.ui.comboBox.addItems(list(self.df.columns))

    def changedSortBy(self, columnName):
        self.sortBy = columnName

class TempWindow(QMainWindow):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.url = "https://pages.mini.pw.edu.pl/~strozynae/images/EStr2.jpg"
        self.image = QImage()
        self.image.loadFromData(requests.get(self.url).content)
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap(self.image).scaled(1920, 1080))
        self.setCentralWidget(self.image_label)
        self.showFullScreen()

def guiMain(args):
    app = QApplication(args)
    window = AnaliserWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    guiMain(sys.argv)
