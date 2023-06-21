import random
from PyQt5 import QtGui as qg


class Schlange:
    """Klasse der Schlange, die für diese Informationen speichert"""
    def __init__(self, x_spielfeldwidth=0, y_spielfeldheigth=0, color = qg.QColor(0, 128, 0)):
        self.richtung = ""
        self.xylist = [(x_spielfeldwidth//2, y_spielfeldheigth//2)]
        self.sw = x_spielfeldwidth
        self.sh = y_spielfeldheigth
        self.color = color
        self.points = 0
        self.lasttail = []

    def move(self):
        """Bewegung der Schlange"""
        if self.richtung == "R":
            x = self.xylist[-1][0] + 1
            if x > self.sw-1:
                x = 0
            xy = (x, self.xylist[-1][1])
        elif self.richtung == "L":
            x = self.xylist[-1][0] - 1
            if x < 0:
                x = self.sw-1
            xy = (x, self.xylist[-1][1])
        elif self.richtung == "U":
            y = self.xylist[-1][1] - 1
            if y < 0:
                y = self.sh-1
            xy = (self.xylist[-1][0], y)
        elif self.richtung == "D":
            y = self.xylist[-1][1] + 1
            if y > self.sh-1:
                y = 0
            xy = (self.xylist[-1][0], y)
        if self.richtung != "":
            self.xylist.append(xy)

    def set_richtung(self, string):
        self.richtung = string

    def length(self):
        return len(self.xylist)

    def death(self):
        """Prüft ob Schlange an Bande ist"""
        (x, y) = self.xylist[-1]
        if x == 0 and self.richtung == "L":
            return True
        if y == 0 and self.richtung == "U":
            return True
        if x == self.sw -1 and self.richtung == "R":
            return True
        if y == self.sh -1 and self.richtung == "D":
            return True
        return False

    def eat_self(self):
        """Prüft ob Schlange sich selbst beißt"""
        x, y = self.xylist[-1]
        for i in self.xylist[0:-1]:
            sx, sy = i
            if (x == sx) & (y == sy):
                return True
        if (x, y) == self.lasttail:
            return True
        return False

    def get_head_x(self):
        return self.xylist[-1][0]

    def get_head_y(self):
        return self.xylist[-1][1]

    def get_tail_x(self):
        return self.xylist[0][0]

    def get_tail_y(self):
        return self.xylist[0][1]

    def get_tail(self):
        return self.xylist[0]

    def get_richtung(self):
        return self.richtung

    def pop_tail(self):
        self.lasttail = self.xylist.pop(0)

    def addTail(self, new):
        self.xylist.insert(0, new)


class Frucht:
    """Klasse der Frucht"""
    def __init__(self, spielwidth, spielheigth, wkeit):
        self.sw = spielwidth
        self.sh = spielheigth
        self.wkeit = wkeit
        self.xy = (-1, -1)
        self.set = False

    def setPos(self, x, y):
        self.xy = (x, y)

    def checkPos(self, snake):
        snake_xy = snake.xylist
        x, y = self.xy
        for i in snake_xy:
            sx, sy = i
            if x == sx:
                if y == sy:
                    return True
        return False

    def checkEat(self, snake):
        snakeh_xy = snake.xylist[-1]
        sx, sy = snakeh_xy
        x, y = self.xy
        if x == sx:
            if y == sy:
                return True
        return False

    def setRandom(self):
        w = random.randint(0, 100)
        if w <= self.wkeit:
            x = random.randint(0, self.sw -1)
            y = random.randint(0, self.sh -1)
            self.xy = (x, y)
            self.set = True
            return True
        return False
