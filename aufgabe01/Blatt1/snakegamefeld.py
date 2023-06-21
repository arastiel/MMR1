import random
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
from snakefrucht import Schlange, Frucht


class SnakeGameFeld(qw.QLabel):
    def __init__(self, spielhoehe, spielbreite, v, a, wkeit, rand, zoom, timer, mehrspieler):
        super().__init__()
        # Variableninitialisierung
        self.spielhoehe = spielhoehe
        self.spielbreite = spielbreite
        self.v = v
        self.a = a
        self.wkeit = wkeit
        self.rand = rand
        self.zoom = zoom
        self.mehrspieler = mehrspieler

        self.pause = False
        self.ende = False

        self.width = self.spielbreite * self.zoom
        self.heigth = self.spielhoehe * self.zoom

        self.timer = timer

        # Initialisiere Spielfeld
        self.spielfeld = qg.QImage(self.spielbreite, self.spielhoehe, qg.QImage.Format_RGBA8888)
        self.spielfeld.fill(qg.QColor(0, 0, 0))
        self.resize(self.width, self.heigth)

        # Initialisiere Schlange
        self.snakelist = []
        self.set_snakelist()

        # Initialisiere Fruchtliste
        self.fruchtlist = []

        self.timer.setInterval(self.v)
        self.zug()
        self.rescale()
        self.timer.start()

    def set_snakelist(self):
        self.snake = Schlange(self.spielbreite, self.spielhoehe, qg.QColor(0, 128, 0))

        if self.mehrspieler:
            self.snake2 = Schlange(self.spielbreite, self.spielhoehe, qg.QColor(0, 0, 255))

            self.snake.xylist = [(self.spielbreite//4, self.spielhoehe//2)]
            self.snake2.xylist = [(int(3*self.spielbreite/4), self.spielhoehe//2)]

            self.snakelist = [self.snake, self.snake2]
            self.spielfeld.setPixelColor(self.snake2.get_head_x(),
                                         self.snake2.get_head_y(),
                                         self.snake2.color)
        else:
            self.snakelist = [self.snake]
        self.spielfeld.setPixelColor(self.snake.get_head_x(),
                                     self.snake.get_head_y(),
                                     self.snake.color)

    def newFrucht(self):
        """Um Wkeit der Furcht gleichzuhalten bei unterschiedlichen v"""
        w = random.randint(0, 300)
        wf = random.randint(0, 100)
        if w <= self.v:
            if wf <= self.wkeit:
                return True
        return False

    def delFrucht(self):
        w = random.randint(0, 300)
        wf = random.randint(0, 100)
        if w <= self.v:
            if wf <= self.wkeit // 2:
                return True
        return False

    def drawFrucht(self):
        """Zeichnet Früchte und erzeugt neue"""
        for i in self.fruchtlist:
            for s in self.snakelist:
                if not i.checkPos(s):
                    self.spielfeld.setPixelColor(i.xy[0], i.xy[1], qg.QColor(204, 0, 204))
                    self.rescale()
                else:
                    self.fruchtlist.remove(i)
                    break
        new_frucht = Frucht(self.spielbreite, self.spielhoehe, self.wkeit)
        if new_frucht.setRandom() & self.newFrucht():
            self.fruchtlist.append(new_frucht)

        # löscht zufällig Früchte aus der Liste
        l = len(self.fruchtlist)
        if l > 1:
            if self.delFrucht():
                j = random.randint(0, l - 1)
                remove_frucht = self.fruchtlist.pop(j)
                self.spielfeld.setPixelColor(remove_frucht.xy[0], remove_frucht.xy[1], qg.QColor(0, 0, 0))
                self.rescale()

    def draw(self):
        """Zeichnet Schlange und löscht letzte Position"""
        for s in self.snakelist:
            if s.get_richtung() != "":
                self.spielfeld.setPixelColor(s.get_head_x() % self.spielbreite,
                                             s.get_head_y() % self.spielhoehe,
                                             s.color)  # zeichnet Kopf(Körper)
                self.spielfeld.setPixelColor(s.get_tail_x() % self.spielbreite,
                                             s.get_tail_y() % self.spielhoehe,
                                             qg.QColor(0, 0, 0))  # Löscht letztes Element(Schwanzspitze)

                s.pop_tail()
        self.rescale()

    def eatFrucht(self):
        """Checkt ob Schlange eine Frucht gegessen hat"""
        for i in self.fruchtlist:
            for s in self.snakelist:
                if i.checkEat(s):
                    self.fruchtlist.remove(i)
                    self.v = self.v - self.a
                    if self.v == 0:
                        self.v = 1
                    self.timer.setInterval(self.v)
                    s.points += 1
                    new_part = s.get_tail()
                    s.addTail(new_part)

    def eatothersnake(self):
        for i in self.snakelist[0].xylist:
            if i in self.snakelist[1].xylist:
                return True
        return False

    def rescale(self):
        """scaliert das Feld"""
        rspielfeld = self.spielfeld.scaled(self.size(), qc.Qt.KeepAspectRatio)
        self.setPixmap(qg.QPixmap.fromImage(rspielfeld))

    def death(self):
        """Füllt Spielfeld Rot, wenn Regeln verletzt wurden"""
        self.spielfeld.fill(qg.QColor(128, 0, 0))
        self.rescale()
        self.ende = True

    def zug(self):
        """Ereignisse, die während eines Zuges geschehen werden ausgeführt"""
        # wenn ende oder pause muss Zug nicht ausgeführt werdebnn
        if self.pause:
            return
        if self.ende:
            return

        for s in self.snakelist:
            # Randkollision
            if s.death() &self.rand:
                self.death()
                return
            # Schlange beißt sich selbst
            if s.eat_self():
                self.death()
                return
            if self.mehrspieler:
                if self.eatothersnake():
                    self.death()
                    return
            s.move()

        self.eatFrucht()
        self.drawFrucht()

        self.draw()

    def restart(self):
        """"Startet SPiel neu und besetzt dafür Variablen neu"""
        self.points = 0
        # Initialisiere Spielfeld
        self.spielfeld = qg.QImage(self.spielbreite, self.spielhoehe, qg.QImage.Format_RGBA8888)
        self.spielfeld.fill(qg.QColor(0, 0, 0))
        self.resize(self.width, self.heigth)

        # Initialisiere Schlange
        self.snakelist = []
        self.set_snakelist()

        # Initialisiere Fruchtliste
        self.fruchtlist = []

        self.ende = False

        self.timer.setInterval(self.v)
        self.zug()
        self.rescale()

    def set_pause(self):
        """Pausiert das Spiel"""
        if not self.pause:
            self.pause = True
        else:
            self.pause = False

    def get_points(self):
        """Gibt Punktestand zurück"""
        return self.snakelist[0].points
    def get_points2(self):
        return self.snakelist[1].points