import sys
from PyQt5.QtWidgets import (QWidget,
    QLabel, QApplication, QLineEdit, QPushButton)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt                         #осталось реализовать самое сложное-логику хождения шашек, их съедание, дамки и тд и тп
from PyQt5.QtGui import QPainter, QColor, QBrush    #пока всего 137 строк(((

#!!!!! ЕСТЬ БАГ, ПРИ ХОЖДЕНИИ ВЫШЕ ТА КАРТИКА, ЧТО БЫЛА ДОБАВЛЕНА ПОЗЖЕ!!!
#НУЖНО ЗАГУГЛИТЬ И ИСПРАВИТЬ (ЕСЛИ ЭТО РЕАЛЬНО)
class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(400, 100, 880, 880)
        self.setWindowTitle('шашки на поле нелогичны (ходят как попало)')
        self.new_game()
        
        
    def new_game(self):
        #расставляет белые и черные шашки на поле
        self.black_shapes = list()
        for y in range(5, 226, 110):
            for x in range(5, 776, 110):
                if y // 10 % 2 == 0:
                    if x // 10 % 2 == 1: 
                        self.black_shapes.append([QLabel(self), (x, y)])
                else:
                    if x // 10 % 2 == 0:
                        self.black_shapes.append([QLabel(self), (x, y)])

        for i in self.black_shapes:
            i[0].move(i[1][0], i[1][1])     
            i[0].setPixmap(QPixmap('shape_black.png'))
        
        
        self.white_shapes = list()
        for y in range(555, 776, 110):
            for x in range(5, 776, 110):
                if y // 10 % 2 == 0:
                    if x // 10 % 2 == 1: 
                        self.white_shapes.append([QLabel(self), (x, y)])
                else:
                    if x // 10 % 2 == 0:
                        self.white_shapes.append([QLabel(self), (x, y)])
        
        for i in self.white_shapes:
            i[0].move(i[1][0], i[1][1])     
            i[0].setPixmap(QPixmap('shape_white.png'))
            
        #нужные переменные   
        self.is_clicked = False #переменная показывает, зажата ли лкм на шашке
        self.figure_white = None #показывает, зажали ли вы белую шашку и если да, то какую (хранит ее индекс в списке белых шашек)
        self.figure_black = None # то же самое, только с черными шашками
        self.who_walks = 'w' #показывает, кто ходит >белые ходят первыми<
        self.walk = False #показывает, нажали ли мы на шашку или же на пустое поле
 
 
    def mouseMoveEvent(self, event):
        
        #реализует хождение шашек по полю, они ходят по очереди
        if self.who_walks == 'w':
            for shape in self.white_shapes:
                
                if self.figure_white != None:
                    self.white_shapes[self.figure_white][0].move(event.x(), event.y())
                    shape[1] = (event.x(), event.y())
                    break
                    
                if (event.x() in range(shape[0].x(), shape[0].x() + 100) and event.y()
                    in range(shape[0].y(), shape[0].y() + 100)):
                    shape[0].move(event.x(), event.y())
                    shape[1] = (event.x(), event.y())
                    self.figure_white = self.white_shapes.index(shape)
                    self.walk = True
        else:
            for shape in self.black_shapes:
                
                    if self.figure_black != None:
                        self.black_shapes[self.figure_black][0].move(event.x(), event.y())
                        shape[1] = (event.x(), event.y())
                        break
                
                    if (event.x() in range(shape[0].x(), shape[0].x() + 100) and event.y()
                        in range(shape[0].y(), shape[0].y() + 100)):
                        shape[0].move(event.x(), event.y())
                        shape[1] = (event.x(), event.y())
                        self.figure_black = self.black_shapes.index(shape) 
                        self.walk = True
             
                

    def mouseReleaseEvent(self, e):
        
        if e.button() == Qt.LeftButton: 
            #если лкм мыши не зажата (отпущена), разрешается ходить
            #другому игроку (если мы не нажали на пустое поле и все-таки ходили шашкой)
            self.figure_white = None
            self.figure_black = None
            if self.who_walks == 'w' and self.walk:
                self.who_walks = 'b'
            elif self.walk:
                self.who_walks = 'w'
            self.walk = False
    
    
    def paintEvent(self, e):
        
        qp = QPainter()
        qp.begin(self)
        self.draw_board(qp)
        qp.end()


    def draw_board(self, qp):
        
        #рисуем шахматную доску
        for y in range(0, 771, 110):
            for x in range(0, 771, 110):
                if y // 10 % 2 == 0:
                    if x // 10 % 2 == 0:
                        qp.setPen(QColor('#DCD3BC')) #это для того, чтобы у нас не было черной обводки
                        qp.setBrush(QColor('#DCD3BC')) #это "белые" клеточки
                    else:
                        qp.setPen(QColor('#74624E')) 
                        qp.setBrush(QColor('#74624E')) #а это "черные"
                else:
                    if x // 10 % 2 == 1:
                        qp.setPen(QColor('#DCD3BC'))
                        qp.setBrush(QColor('#DCD3BC'))
                    else:
                        qp.setPen(QColor('#74624E'))
                        qp.setBrush(QColor('#74624E'))
                qp.drawRect(x, y, 110, 110)                    
                

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())