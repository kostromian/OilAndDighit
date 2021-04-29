import sys
from PyQt5 import Qt
import math# sys нужен для передачи argv в QApplication
from PyQt5.QtWidgets import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QHBoxLayout Example")
        self.button = QPushButton(self)
        self.button.setStyleSheet("border-radius : 60; border : 2px solid black; background-color: red")
        self.button.setGeometry(300 - 30, 300 - 30, 120, 120)
        self.draw()

    def draw(self):
        self.button.setText("Газпром")
        self.children = []
        t = 0
        angle = 0
        R = 120
        for i in range(20):
            self.children.append(QPushButton(self))
            # self.connect(self.children[i], PYQT_SIGNAL("clicked()"), self.clear())
            # self.b1 = QPushButton("Button1")
            self.children[i].setText("Дочка")
            self.children[i].setStyleSheet("border-radius : 15; border : 2px solid black; background-color: red")
            self.children[i].clicked.connect(self.reuse)
            self.children[i].setGeometry(300, 300, 45, 45)
            x = 1 * math.cos(angle)
            y = 1 * math.sin(angle)
            self.children[i].move(int(R * math.cos(angle * math.pi / 180)) + 300,
                                  -int(R * math.sin(angle * math.pi / 180)) + 300)
            angle += 60
            if angle >= 360:
                R += 60
                angle = angle % 60 + 15

    def clear(self):
        for it in self.children:
            it.hide()

    def redraw(self):
        for it in self.children:
            it.show()

    def reuse(self):
        self.clear()
        self.redraw()





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