from analise import Analiser
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import pyqtSlot, Qt, QTimer, QObject
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

        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                cell = self.df.iloc[i, j]
                if type(cell) == float:
                    cell = round(cell, 2)

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
        self.initUI()

    def initUI(self):
        self.setGeometry(700, 100, 350, 380)
        analiser = Analiser("src/generated.json")

        df = analiser.pretty_table
        self.table = QTableWidget(self)
        layout = QHBoxLayout()

        self.table = TableWidget(df, self)
        self.setCentralWidget(self.table)

        form = QWidget()
        layout = QFormLayout(form)
        form.setLayout(layout)

def guiMain(args):
    app = QApplication(args)
    window = AnaliserWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    guiMain(sys.argv)
