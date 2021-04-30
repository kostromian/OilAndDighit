import functools
import sys
import Company
import math# sys нужен для передачи argv в QApplication
from PyQt5.QtWidgets import *
import design
import designInfo
from PyQt5 import QtCore
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice

global alldata
global data
class SecondWindow(QDialog, designInfo.Ui_Dialog):
    def __init__(self):
        global data
        global alldata
        super().__init__()
        self.setupUi(self)
        self.label_2.setText(data.name)
        self.label_4.setText(self.getChildren(data.id))
        self.label_6.setText(self.getMother(data.mother))
        self.label_8.setText(str(int(data.count_prj_our) + int(data.count_prj_imp)))
        self.label_10.setText(str(data.count_prj_imp))
        self.label_12.setText(str(data.count_prj_our))
        self.label_14.setText(str(int(data.count_mln_our) + int(data.count_mln_imp)) + "Млн")
        self.widget.setChart(self.create_piechart(data.count_prj_our, data.count_prj_imp, 'Соотношение числа проектов'))
        self.widget_2.setChart(self.create_piechart(data.count_mln_our, data.count_prj_imp, 'Соотношение бюджетов проектов'))

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
        chart.legend().setAlignment(QtCore.Qt.AlignBottom)

        return chart

    def getChildren(self, motherId):
        global alldata
        buff = ""
        for it in alldata:
            if it.mother == motherId:
                buff += it.name + '-'
        buff = buff[:-1]
        return buff

    def getMother(self, id):
        global alldata
        for it in alldata:
            if it.id == id:
                return it.name


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: rgb(255, 239, 219);");
        #QMainWindow.setIconSize(self, QSizeiconSize)
        self.data = Company.innit_data()
        global alldata
        alldata = self.data
        self.setWindowTitle("GetLucky")
        self.button = QPushButton(self)
        self.button.clicked.connect(self.openWindow)
        self.motherbutton = QPushButton(self)
        self.searchText = QLineEdit(self)
        self.searchText.setGeometry(0, 0, 100, 30)
        self.searchbutton = QPushButton(self)
        self.searchbutton.setText("Найти")
        self.searchbutton.clicked.connect(self.search)
        self.searchbutton.setGeometry(100, 0, 90, 30)
        self.motherbutton.setStyleSheet("border-radius : 30; border : 2px solid black; background-color: rgb(234, 214, 238)")
        self.button.setStyleSheet("border-radius : 60; border : 2px solid black; background-color: rgb(227, 189, 229)")
        self.motherbutton.setGeometry(300, 300, 60, 60)
        self.button.setGeometry(300 - 30, 300 - 30, 120, 120)
        self.label = QLabel(self)
        self.label.setStyleSheet("background-color: rgb(227, 189, 229)")
        #self.label.setText("test")
        self.label.setGeometry(300 + 18, 300 - 20, 35, 15)
        self.childrenButtons = []
        self.countInit = 0
        self.selectedCompany = self.data[0]
        self.draw()
        self.motherbutton.hide()

    def getChildren(self, motherId):
        self.children = []
        for it in self.data:
            if it.mother == motherId:
                self.children.append(it)

    def search(self):
        for it in self.data:
            if it.name == self.searchText.text():
                self.reuse(it)

    def draw(self):
        self.label.setText(self.selectedCompany.name)
        self.getChildren(self.selectedCompany.id)
        angle = 0
        R = 160
        for i in range(len(self.children)):
            if self.countInit <= i:
                self.childrenButtons.append(QPushButton(self))
                self.countInit += 1
                self.childrenButtons[i].setGeometry(300, 300, 60, 60)
                self.childrenButtons[i].move(int(R * math.cos(angle * math.pi / 180)) + 300,
                                             -int(R * math.sin(angle * math.pi / 180)) + 300)
                self.childrenButtons[i].clicked.connect(functools.partial(self.reuse, selectedCompany=self.children[i]))
                angle += 30
                if angle >= 360:
                    R += 80
                    angle = angle % 60 + 30
            else:
                self.childrenButtons[i].show()
            self.childrenButtons[i].setText(self.children[i].name + " " + str(self.children[i].imp_depend))
            font = "background-color:rgb(100,"+ str(255 * self.children[i].imp_depend / 100) + ",150)";
            self.childrenButtons[i].setStyleSheet("border-radius : 15; border : 2px solid black; " + font)

    def clear(self):
        for it in self.childrenButtons:
            it.hide()

    def getMother(self, id):
        for it in self.data:
            if it.id == id:
                return it

    def reuse(self, selectedCompany):
        if selectedCompany == self.data[0]:
            self.motherbutton.hide()
            self.label.text = ""
        else:
            self.motherbutton.show()
            self.motherbutton.clicked.connect(functools.partial(self.reuse, selectedCompany = self.getMother(selectedCompany.mother)))
            self.motherbutton.setText(self.getMother(selectedCompany.mother).name + " " +
                                      str(self.getMother(selectedCompany.mother).imp_depend))
        self.selectedCompany = selectedCompany
        self.clear()
        self.draw()

    def openWindow(self):
        global data
        data = self.selectedCompany
        self.infoWindow = SecondWindow()
        self.infoWindow.show()





# def main():
#     app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
#     window = ExampleApp()  # Создаём объект класса ExampleApp
#     window.show()  # Показываем окно
#     app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем


    app = QApplication(sys.argv)
    window = Window()
    window2 = Window()

    window.show()
    sys.exit(app.exec_())
    #main()  то запускаем функцию main()