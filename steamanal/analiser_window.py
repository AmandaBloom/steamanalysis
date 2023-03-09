from analise import Analiser
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import pyqtSlot, Qt, QTimer, QObject
import analiser_window_ui as analiser_window_ui
import pandas as pd
import sys

class TableWidget(QTableWidget):
    def __init__(self, df, parent=None):
        QTableWidget.__init__(self, parent)
        self.df = df
        nRows = len(self.df.index)
        nColumns = len(self.df.columns)
        self.setRowCount(nRows)
        self.setColumnCount(nColumns)
        self.setHorizontalHeaderLabels(list(self.df.columns))
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                cell = self.df.iloc[i, j]
                if type(cell) == float:
                    cell ='{:.2f}'.format(cell)

                cell = str(cell)
                self.setItem(i, j, QTableWidgetItem(cell))

        self.cellChanged.connect(self.onCellChanged)

    @pyqtSlot(int, int)
    def onCellChanged(self, row, column):
        text = self.item(row, column).text()
        number = float(text)
        self.df.set_value(row, column, number)



class AnaliserWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = analiser_window_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupTable()

    def setupTable(self):
        analiser = Analiser("src/generated.json")

        df = analiser.pretty_table
        self.ui.tableWidget = TableWidget(df, self)
        self.ui.tableWidget.setSortingEnabled(True)

        self.ui.verticalLayout_2.addWidget(self.ui.tableWidget)

def guiMain(args):
    app = QApplication(args)
    window = AnaliserWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    guiMain(sys.argv)
