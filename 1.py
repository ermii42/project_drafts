import sys
from PyQt5.QtWidgets import (QWidget,
    QLabel, QApplication)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt               
from PyQt5.QtGui import QPainter, QColor, QBrush

#!!!у этой версии есть недочеты, нельзя бить больше одной шашки
#бить назад можно

class checkers(QWidget):


    def __init__(self):
        super().__init__()      
        self.initUI()

        
    def initUI(self):
        self.setGeometry(400, 100, 875, 870)
        self.setWindowTitle('шашки на поле более-менее логичны (уже не ходят как попало)')
        self.new_game()
        
        
    def new_game(self):
        #расставляет белые и черные шашки на поле
        
        self.black_shapes = list()
        #создаем список черных шашек
        for y in range(5, 226, 110): 
            for x in range(5, 776, 110):
                if y // 10 % 2 == 0:
                    if x // 10 % 2 == 1: 
                        self.black_shapes.append([QLabel(self), (x, y), False]) 
                        #1-это сама шашка 2-это ее нынешние координаты  
                        #3-это является ли эта шашка дамкой
                        
                else:
                    if x // 10 % 2 == 0:
                        self.black_shapes.append([QLabel(self), (x, y), False])
        
        #устанавливаем картинки черных шашек на доску
        for i in self.black_shapes:
            i[0].move(i[1][0], i[1][1])     
            i[0].setPixmap(QPixmap('shape_black.png'))
        
        #то же самое, только с белыми шашками
        self.white_shapes = list()
        #создаем список белых шашек и заполняем его
        
        for y in range(555, 776, 110):
            for x in range(5, 776, 110):
                if y // 10 % 2 == 0:
                    if x // 10 % 2 == 1: 
                        self.white_shapes.append([QLabel(self), (x, y), False])
                else:
                    if x // 10 % 2 == 0:
                        self.white_shapes.append([QLabel(self), (x, y), False])
                        
        #устанавливаем картинки черных шашек на доску
        for i in self.white_shapes:
            i[0].move(i[1][0], i[1][1])     
            i[0].setPixmap(QPixmap('shape_white.png'))
            
        #нужные мне переменные
        self.is_clicked = False #переменная показывает, зажата ли лкм на шашке
        self.figure_white = None #показывает, зажали ли вы белую шашку и если да, 
                                 #то какую (хранит ее индекс в списке белых шашек)
        self.figure_black = None # то же самое, только с черными шашками
        self.who_walks = 'w' #показывает, кто ходит >белые ходят первыми<
        self.brd = simple_board() #создаем списочную версию нашей шахматной доски
        self.start_coor_w = '' #начальные координаты шашки, которую мы двигаем (белой)
        self.start_coor_b = '' #(черной)
 
 
    def mouseMoveEvent(self, event):
        #реализует хождение шашек по полю, они ходят по очереди
        
        #узнаем, какая шашка должна ходить (белая или черная) 
        #и в пределах ли курсор мыши шахматной доски
        if self.who_walks == 'w' and event.x() in range(0, 880) \
           and event.y() in range(0, 880):
            if self.brd.must_eat(self.white_shapes, 'w') != []:
                #проверяем наличие шашек, которые могут есть; если такие существуют,
                #то мы берем во внимание только их (по правилам шашки обязаны бить)
                shapes_which_can_walk = self.brd.must_eat(self.white_shapes, 'w')
                
            else:
                #если таких нет, то мы рассматриваем все шашки
                shapes_which_can_walk = self.white_shapes
                
            for shape in shapes_which_can_walk:
                #пробегаемся по шашкам, которые мы рассматривам
                if self.figure_white != None: #'если определили схваченную шашку'
                    self.white_shapes[self.figure_white][0].raise_() #ставит картинку выше других
                    #двигаем шашку
                    self.white_shapes[self.figure_white][0].move(event.x() - 50,
                                                                 event.y() - 50)
                    #меняем ее координаты в списке белых шашек
                    self.white_shapes[self.figure_white][1] = (event.x(), event.y())
                    break
                    
                if (event.x() in range(shape[0].x(), shape[0].x() + 100) and event.y()
                    in range(shape[0].y(), shape[0].y() + 100)):
                    #определяем, какую именно шашку из списка мы схватили
                    self.start_coor_w = shape[1]
                    shape[0].move(event.x() - 50, event.y() - 50)
                    #'-50' нужно для того, чтобы при перетаскивании курсор мыши был в середине шашки
                    shape[1] = (event.x(), event.y())
                    self.figure_white = self.white_shapes.index(shape)
        
        #то же самое, только с черными шашками
        elif event.x() in range(0, 880) and event.y() in range(0, 880):
            if self.brd.must_eat(self.black_shapes, 'b') != []:
                shapes_which_can_walk = self.brd.must_eat(self.black_shapes, 'b')
            else:
                shapes_which_can_walk = self.black_shapes
            
            for shape in shapes_which_can_walk:
                
                    if self.figure_black != None:
                        self.black_shapes[self.figure_black][0].raise_()
                        self.black_shapes[self.figure_black][0].move(
                            event.x() - 50, event.y() - 50)
                        self.black_shapes[self.figure_black][1] = (event.x(), event.y())
                        break
                
                    if (event.x() in range(shape[0].x(), shape[0].x() + 100) and event.y()
                        in range(shape[0].y(), shape[0].y() + 100)):
                        self.start_coor_b = shape[1]
                        shape[0].move(event.x() - 50, event.y() - 50)
                        shape[1] = (event.x(), event.y())
                        self.figure_black = self.black_shapes.index(shape) 
                        

    def mouseReleaseEvent(self, e):
        #"если мы отпустили кнопку мыши"
        if e.button() == Qt.LeftButton:
            #шашки, наступая на черную клетку, становятся в ее середину
            if self.figure_black != None: #если мы ходили черной шашкой
                ways = self.brd.various_ways(self.start_coor_b, 'b', 
                                             self.black_shapes[self.figure_black][2])
                #ways-варианты ходов нажатой шашки
                
                if ways[1]: 
                    #ways[1] показывает, ест ли шашка
                    
                    for i in ways[0]: 
                        #ways[0][n][0] показывает координаты, куда шашка может встать
                        #ways[0][n][1] показывает координаты съеденной шашки, если мы
                        #сходили на ways[0][n][0]
                        #узнаем, на какую же именно черную клетку из дозволенных она встала
                        if self.black_shapes[self.figure_black][1][0] in \
                           range(i[0][0] - 5, i[0][0] - 5 + 111) and \
                           self.black_shapes[self.figure_black][1][1] in \
                           range(i[0][1] - 5, i[0][1] - 5 + 111):
                            
                            self.black_shapes[self.figure_black][0].move(i[0][0], i[0][1])
                            self.black_shapes[self.figure_black][1] = i[0]
                            
                            #если шашка дошла до противоположного края доски, она
                            #становится дамкой
                            if i[0] in [(5, 775), (225, 775), (445, 775), (665, 775)]:
                                self.black_shapes[self.figure_black][2] = True
                                self.black_shapes[self.figure_black][0].setPixmap(
                                    QPixmap('shape_black_q.png'))                            
                            
                            #теперь можно ходить белым
                            self.who_walks = 'w'
                            #изменяем списочное представление доски
                            self.brd.changing_board(self.start_coor_b, i[0], 'b')
                            #удалаяем со списочного представления доски съеденную 
                            #нами шашку
                            self.brd.eating(i[1])
                            
                            #ищем съеденную шашку в списке белых шашек
                            for j in self.white_shapes:
                                if j[1] == i[1]:
                                    #убираем картинку шашки с доски
                                    self.white_shapes[self.white_shapes.index(j)
                                                      ][0].clear()
                                    #удаляем шашку из списка
                                    del self.white_shapes[self.white_shapes.index(j)]
                                    break
                            break
                        
                    else:
                        #если игрок сходил туда, куда непозволено, то
                        #он делает свой ход заново
                        #шашка становится на начальное положение
                        self.black_shapes[self.figure_black][0].move(self.start_coor_b[0],
                                                                     self.start_coor_b[1])
                        self.black_shapes[self.figure_black][1] = self.start_coor_b
                        
                else:
                    #если шашка не ест, то:
                    for i in ways[0]:
                        
                        #в принципе, дальше все почти то же самое
                        #исключая съедение шашки
                        if self.black_shapes[self.figure_black][1][0] in range(
                            i[0] - 5, i[0] - 5 + 111)\
                          and self.black_shapes[self.figure_black][1][1] in range(
                              i[1] - 5, i[1] - 5 + 111):

                            self.black_shapes[self.figure_black][0].move(i[0], i[1])
                            self.black_shapes[self.figure_black][1] = i
                            
                            if i in [(5, 775), (225, 775), (445, 775), (665, 775)]:
                                self.black_shapes[self.figure_black][2] = True
                                self.black_shapes[self.figure_black][0].setPixmap(
                                    QPixmap('shape_black_q.png'))
                        
                            self.who_walks = 'w'
                            self.brd.changing_board(self.start_coor_b, i, 'b')
                            break
                    
                    else:
                        self.black_shapes[self.figure_black][0].move(
                            self.start_coor_b[0], self.start_coor_b[1])
                        self.black_shapes[self.figure_black][1] = self.start_coor_b
            
            #то же самое, только для белых шашек
            if self.figure_white != None:
                ways = self.brd.various_ways(self.start_coor_w, 'w', self.white_shapes[
                    self.figure_white][2])
                if ways[1]:
                    
                    for i in ways[0]:
                        
                        if self.white_shapes[self.figure_white][1][0] in range(
                            i[0][0] - 5, i[0][0] - 5 + 111)\
                           and self.white_shapes[self.figure_white][1][1] in range(
                               i[0][1] - 5, i[0][1] - 5 + 111):
                
                            self.white_shapes[self.figure_white][0].move(i[0][0], i[0][1])
                            self.white_shapes[self.figure_white][1] = i[0]
                            
                            if i[0] in [(115, 5), (335, 5), (555, 5), (775, 5)]:
                                self.white_shapes[self.figure_white][2] = True
                                self.white_shapes[self.figure_white][0].setPixmap(
                                    QPixmap('shape_white_q.png'))                            
                            
                            self.who_walks = 'b'
                            self.brd.changing_board(self.start_coor_w, i[0], 'w')
                            self.brd.eating(i[1])
                            for j in self.black_shapes:
                                if j[1] == i[1]:
                                    self.black_shapes[
                                        self.black_shapes.index(j)][0].clear()
                                    del self.black_shapes[self.black_shapes.index(j)]
                                    break
                            break
                        
                    else:
                        self.white_shapes[self.figure_white][0].move(self.start_coor_w[0],
                                                                     self.start_coor_w[1])
                        self.white_shapes[self.figure_white][1] = self.start_coor_w
                        
                else:
                    for i in ways[0]:
                        if self.white_shapes[self.figure_white][1][0] in \
                           range(i[0] - 5, i[0] - 5 + 111) and self.white_shapes[
                               self.figure_white][1][1] in range(i[1] - 5, i[1] - 5 + 111):
                            
                            self.white_shapes[self.figure_white][0].move(i[0], i[1])
                            self.white_shapes[self.figure_white][1] = i
                            
                            if i in [(115, 5), (335, 5), (555, 5), (775, 5)]:
                                self.white_shapes[self.figure_white][2] = True
                                self.white_shapes[self.figure_white][0].setPixmap(
                                    QPixmap('shape_white_q.png'))                            
                        
                            self.who_walks = 'b'
                            self.brd.changing_board(self.start_coor_w, i, 'w')
                            break
                    
                    else:
                        self.white_shapes[self.figure_white][0].move(self.start_coor_w[0],
                                                                     self.start_coor_w[1])
                        self.white_shapes[self.figure_white][1] = self.start_coor_w                
                    
            #обнуляем эти переменные
            #если этого не сделать, то за курсором мышки продолжит волочиться картинка
            #а черные шашки вообще не смогут больше ходить
            self.figure_white = None
            self.figure_black = None
    
    
    def paintEvent(self, e):
        #рисуем доску
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
                        #это для того, чтобы у нас не было черной обводки
                        qp.setPen(QColor('#DCD3BC')) 
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
                

#это класс со "списочным" (на самом деле словарным) представлением доски, у которого
#есть функция для рассчитывания возможных ходов шашек
class simple_board():
    
    
    #перечисялю диагонали;
    #Большая дорога
    GoldWay = [(5, 775), (115, 665), (225, 555), (335, 445), (445, 335),
               (555, 225), (665, 115), (775, 5)]#a1, b2, c3, d4, e5, f6, g7, h8
    
    #Двойники
    DoubleWayG1A7 = [(665, 775), (555, 665), (445, 555),#g1, f2, e3, d4, c5, b6, a7
                (335, 445), (225, 335), (115, 225), (5, 115)]
    DoubleWayH2B8 = [(775, 665), (665, 555), (555, 445),#h2, g3, f4, e5, d6, c7, b8
                    (445, 335), (335, 225), (225, 115), (115, 5)]
    
    #Тройники
    TripleWayC1A3 = [(225, 775), (115, 665), (5, 555)]#c1, b2, a3
    TripleWayC1H6 = [(225, 775), (335, 665), (445, 555),#c1, d2, e3, f4, g5, h6
                     (555, 445), (665, 335), (775, 225)]
    TripleWayH6F8 = [(775, 225), (665, 115), (555, 5)]#h6, g7, f8
    TripleWayA3F8 = [(5, 555), (115, 445), (225, 335),#a3, b4, c5, d6, e7, f8
                     (335, 225), (445, 115), (555, 5)]
    
    #Косяки
    UltraWayA5D8 = [(5, 335), (115, 225), (225, 115), (335, 5)]#a5, b6, c7, d8
    UltraWayH4D8 = [(775, 445), (665, 335), (555, 225),#h4, g5, f6, e7, d8 
                    (445, 115), (335, 5)]
    UltraWayE1A5 = [(445, 775), (335, 665), (225, 555),#e1, d2, c3, b4, a5
                    (115, 445), (5, 335)]
    UltraWayG1H2 = [(665, 775), (775, 665)]#g1, h2
    UltraWayE1H4 = [(445, 775), (555, 665), (665, 555), (775, 445)]#e1, f2, g3, h4
    UltraWayA7B8 = [(665, 775), (115, 5)]#a7, b8
    
    #список со всеми путями
    s = [GoldWay, DoubleWayG1A7, DoubleWayH2B8, TripleWayC1A3, TripleWayC1H6, 
         TripleWayH6F8, TripleWayA3F8, UltraWayA5D8, UltraWayE1A5, UltraWayE1H4, 
         UltraWayA7B8, UltraWayH4D8, UltraWayG1H2]


    def __init__(self):
        self.new_board()
        
    
    def new_board(self):
        #именно этот словарь я и называла 'списочным' представлением доски
        #'w'(white) - стоит белая шашка; 'b'(black) - стоит черная шашка;
        #None-клетка свободна, туда можно ходить
        self.brd = {(115, 5): 'b', (335, 5): 'b', (555, 5): 'b', (775, 5): 'b',
                (5, 115): 'b', (225, 115): 'b', (445, 115): 'b', (665, 115): 'b',
                (115, 225): 'b', (335, 225): 'b', (555, 225): 'b', (775, 225): 'b',
                (5, 335): None, (225, 335): None, (445, 335): None, (665, 335): None,
                (115, 445): None, (335, 445): None, (555, 445): None, (775, 445): None,
                (5, 555): 'w', (225, 555): 'w', (445, 555): 'w', (665, 555): 'w',
                (115, 665): 'w', (335, 665): 'w', (555, 665): 'w', (775, 665): 'w',
                (5, 775): 'w', (225, 775): 'w', (445, 775): 'w', (665, 775): 'w'}         


    #обновляет списочную доску при ходе шашки
    def changing_board(self, coor, new_coor, color):
        self.brd[new_coor] = color
        self.brd[coor] = None

    
    #убираем 'жертву' (съеденную шашку) с доски
    def eating(self, victim):
        self.brd[victim] = None
        
    
    #'должен есть', организует список шашек, которые бьют
    def must_eat(self, s, color):
        sp = []
        
        for i in s:
            if self.various_ways(i[1], color, i[2])[1]:
                sp.append(i)
        return sp
    
    
    #'различные пути' принимает на вход начальные координаты шашки, ее цвет
    #и является ли она дамкой (True/False)
    def various_ways(self, coor, color, is_q):
        #список путей
        ways = []
        
        #это хождение дамок (оно недоработано)
        #дамка не способна съесть больше одной шашки
        if is_q:
            for i in self.s: #пробегаемся по диагоналям шахматной доски
                
                if coor in i: #если шашка лежит на этой диагонали;
                    for j in range(i.index(coor), - 1, -1):
                        
                        if j - 2 >= 0:
                            if self.brd[i[j]] == None and self.brd[i[j - 1]] \
                               != color and self.brd[i[j - 1]] != None and \
                               self.brd[i[j - 2]] == None or i[j] == coor and \
                               self.brd[i[j - 1]] != color and \
                               self.brd[i[j - 1]]!= None and self.brd[i[j - 2]] == None:
                                ways.append((i[j - 2], i[j - 1]))                            
                                break
                            
                    for j in range(i.index(coor), len(i)):
                        
                        if j + 2 < len(i):
                            if self.brd[i[j]] == None and self.brd[i[j + 1]] \
                               != color and self.brd[i[j + 1]] != None and \
                               self.brd[i[j + 2]] == None or i[j] == coor and \
                               self.brd[i[j + 1]] != color and \
                               self.brd[i[j + 1]]!= None and self.brd[i[j + 2]] == None:
                                ways.append((i[j + 2], i[j + 1])) 
                                break
                            
            if ways != []: #если у дамки была возможность кого-то съесть,
                #то на этом ее возможности ходить и остаются
                return (ways, True)
            
            #если же нет, то дамка может ходить куда пожелает (кроме как через/на другие шашки)
            for i in self.s:
                if coor in i:
                    for j in range(i.index(coor) - 1, -1, -1):
                        
                        if self.brd[i[j]] == None:
                            ways.append(i[j]) 
                        else:
                            break
                        
                    for j in i[i.index(coor) + 1:]:
                        
                        if self.brd[j] == None:
                            ways.append(j)
                        else:
                            break
                        
            return (ways, False)
           
        #а это просчет ходов для простой шашки
        #тут тоже возможность бить недоработана, они тоже не могут съесть больше одной шашки
        for i in self.s:
            
                if coor in i:
                    if i.index(coor) + 2 < len(i):
                        if self.brd[i[i.index(coor) + 2]] == None and \
                           self.brd[i[i.index(coor) + 1]] != color and \
                           self.brd[i[i.index(coor) + 1]] in ['w', 'b']:
                            ways.append((i[i.index(coor) + 2], i[i.index(coor) + 1]))
                            
                    if i.index(coor) - 2 >= 0:
                        if self.brd[i[i.index(coor) - 2]] == None and self.brd[i[
                            i.index(coor) - 1]] != color and self.brd[i[i.index(coor) - 1
                                                                        ]] in ['w', 'b']:
                            ways.append((i[i.index(coor) - 2], i[i.index(coor) - 1]))
                            
        if ways != []:
            return (ways, True)
        
        if color == 'w':
            for i in self.s:
                
                if coor in i:
                    if i.index(coor) + 1 < len(i):
                        if self.brd[i[i.index(coor) + 1]] == None:
                            ways.append(i[i.index(coor) + 1])                
                
        else:
            
            for i in self.s:
                if coor in i:
                    if i.index(coor) - 1 >= 0:
                        if self.brd[i[i.index(coor) - 1]] == None:
                            ways.append(i[i.index(coor) - 1])
                            
        return (ways, False)
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ch = checkers()
    ch.show()
    sys.exit(app.exec_())