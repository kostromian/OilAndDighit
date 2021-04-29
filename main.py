# from PyQt5.QtGui import QPainter, QPen
# from PyQt5 import QtCore
# from PyQt5 import *
# import pyqtgraph as pg


import sys  # sys нужен для передачи argv в QApplication
import random
import numpy as np

from PyQt5 import QtWidgets

import design
import designInfo

from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtCore import Qt


class SecondWindow(QtWidgets.QDialog, designInfo.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.widget.setChart(self.create_piechart(70, 30, 'Соотношение числа проектов'))
        self.widget_2.setChart(self.create_piechart(20, 80, 'Соотношение бюджетов проектов'))

    def create_piechart(self, x, y, title):
        series = QPieSeries()
        series.append("Зависимые", x)
        series.append("Независимые", y)

        # adding slice
        slice = QPieSlice()
        slice = series.slices()[1]
        slice.setExploded(True)
        slice.setLabelVisible(True)

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle(title)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        return chart
        # self.widget.setChart(chart)


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.infoWindow = None
        self.pushButton_2.clicked.connect(self.openWindow)

    def openWindow(self):
        self.infoWindow = SecondWindow()
        self.infoWindow.show()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()
