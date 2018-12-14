import sys
from PyQt5.QtWidgets import (QWidget,
    QLabel, QApplication, QLineEdit, QPushButton)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.is_clicked = False #переменная показывает, зажата ли лкм на шашке

    def initUI(self):
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('шашка')
        
        self.pixmap = QPixmap('shape_black.png')
        self.shape = QLabel(self)
        self.shape.move(100, 100)      
        self.shape.setPixmap(self.pixmap)
        
 
    def mouseMoveEvent(self, event):
        if (event.x() in range(self.shape.x(), self.shape.x() + 100) and event.y()
            in range(self.shape.y(), self.shape.y() + 100)) or self.is_clicked:
            #проверяем, нажали ли мы на шашку; если да-двигаем ее
            self.shape.move(event.x(), event.y())
            self.is_clicked = True
            

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton: #если лкм мыши не зажата (отпущена) переменная принимает значение False
            self.is_clicked = False
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())