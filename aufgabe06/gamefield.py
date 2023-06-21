from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
import numpy as np
import sys
from tank import tank_player
from Background_Functions import bildfunc


class Gamefield(qw.QLabel):
    """Label, dass Hügellandschaft darstellt, sowie Panzer, Schüsse und sonstige Visualisation"""
    def __init__(self, w=1500, h=750, difficulty="easy", ki=True,
                 player1=tank_player(0, [(0, 0)], c=qg.QColor(140, 140, 140), n="Spieler1"),
                 player2=tank_player(0, [(0, 0)], c=qg.QColor(140, 140, 140), n="Spieler2")):
        super().__init__()
        # Size
        self.width = w
        self.height = h
        self.resize(self.width, self.height)

        # Schwierigkeitslevel
        self.difficulty = difficulty

        # Zeichengrund
        self.canvas = qg.QPixmap(self.width, self.height)
        self.painter = qg.QPainter(self.canvas)

        self.mountains = 0 # 2D Array für Hügellandschaft
        self.randpixel = 0 # Hügelrand

        self.skycolor = qg.QColor(0, 153, 255, 255)
        self.init_background() # Initialisiert Hintergrundlandschaft

        # Playerinitialisierung
        self.player1 = player1
        self.player2 = player2
        self.player1.new_back(self.randpixel, int(self.width*1/4))
        self.player2.new_back(self.randpixel, int(self.width * 3/4))

        self.draw_tank() # Zeichnet Spieler
        rcanvas = self.canvas.scaled(self.size(), qc.Qt.KeepAspectRatio)
        self.setPixmap(rcanvas)

        # Variablen für Events
        self.setMouseTracking(True)

        self.i = 0
        self.einschlag = False
        self.shooting = False
        self.leftclick = False
        self.player = True #True für Player1
        self.ki = ki
        self.allowedtomove = True

        self.gameover = False
        self.pause = False
        self.projectileChoosen = False#
        self.zug_finished = False
        self.p1arsenal = True
        self.p2arsenal = True

        # Difficulty
        self.help = True
        self.move = True
        self.helpline = True
        self.start_difficulty()

        self.x_kords, self.y_kords, self.i_krater = [], [], 0

    def resizeEvent(self, a0: qg.QResizeEvent):
        rcanvas = self.canvas.scaled(self.size(), qc.Qt.KeepAspectRatio)
        self.setPixmap(rcanvas)
        #self.resize(rcanvas.size())

    def rescale(self):
        rcanvas = self.canvas.scaled(self.size(), qc.Qt.KeepAspectRatio)
        self.setPixmap(rcanvas)

    def init_difficulty(self):
        if self.difficulty == "easy":
            self.help = True
            self.move = False
            self.helpline = True
        elif self.difficulty == "advanced":
            self.help = True
            self.move = True
            self.helpline = True
        elif self.difficulty == "hard":
            self.help = False
            self.move = True
            self.helpline = False
        elif self.difficulty == "expert":
            self.help = False
            self.move = True
            self.helpline = False

    def start_difficulty(self):
        if self.difficulty == "easy":
            self.help = True
            self.move = False
            self.helpline = True
            if self.ki:
                self.player1.set_arsenal(5)
                self.player2.set_arsenal(5)
            else:
                self.player1.set_arsenal(2)
                self.player2.set_arsenal(2)
        elif self.difficulty == "advanced":
            self.help = True
            self.move = True
            self.helpline = True
            if self.ki:
                self.player1.set_arsenal(5)
                self.player2.set_arsenal(5)
            else:
                self.player1.set_arsenal(1)
                self.player2.set_arsenal(1)
        elif self.difficulty == "hard":
            self.help = False
            self.move = True
            self.helpline = False
            if self.ki:
                self.player1.set_arsenal(5)
                self.player2.set_arsenal(5)
            else:
                self.player1.set_arsenal(2)
                self.player2.set_arsenal(2)
        elif self.difficulty == "expert":
            self.help = False
            self.move = True
            self.helpline = False
            if self.ki:
                self.player1.set_arsenal(7)
                self.player2.set_arsenal(7)
            else:
                self.player1.set_arsenal(1)
                self.player2.set_arsenal(1)

    def init_background(self):
        # Himmel
        self.painter.fillRect(0, 0, self.width, self.height, self.skycolor)

        # Berge
        self.mountains, self.randpixel = bildfunc(self.width, self.height, self.difficulty)
        self.mountainPix = qg.QPixmap(qg.QPixmap.fromImage(self.mountains))

        # Zeichnen der Ebenen, Bauteine
        self.painter.drawPixmap(0, 0, self.mountainPix)

    def draw_tank(self):
        self.painter.setPen(qc.Qt.black)
        self.painter.setBrush(self.player1.color)
        if self.player1.livepoints:
            self.painter.drawEllipse(self.player1.dach)
            self.painter.drawRect(self.player1.rect)

        self.painter.setBrush(self.player2.color)

        if self.player2.livepoints:
            self.painter.drawEllipse(self.player2.dach)
            self.painter.drawRect(self.player2.rect)

        self.painter.setPen(qg.QPen(qc.Qt.black, 5))
        if self.player1.livepoints:
            self.painter.drawLine(self.player1.pipe)
        if self.player2.livepoints:
            self.painter.drawLine(self.player2.pipe)

    def reload(self, timestep=0.0):
        """Lädt Zeichenfläche neu nach Bewegungen"""
        self.painter.fillRect(0, 0, self.width, self.height, self.skycolor)
        self.painter.drawPixmap(0, 0, self.mountainPix)
        self.draw_tank()
        if self.help:
            self.shoot_help_line(timestep)
        rcanvas = self.canvas.scaled(self.size(), qc.Qt.KeepAspectRatio)
        self.setPixmap(rcanvas)

    def newback(self):
        """Erstellt neue Hintergrundflandschaft und setzt Spieler auf Anfangspositionen"""
        self.painter.fillRect(0, 0, self.width, self.height, self.skycolor)

        # Berge
        self.mountains, self.randpixel = bildfunc(self.width, self.height, self.difficulty)
        self.mountainPix.swap(qg.QPixmap(qg.QPixmap.fromImage(self.mountains)))

        # Zeichnen der Ebenen, Bauteine
        self.painter.drawPixmap(0, 0, self.mountainPix)
        self.player1.new_back(self.randpixel, int(self.width * 1 / 4))
        self.player2.new_back(self.randpixel, int(self.width * 3 / 4))
        self.draw_tank()
        rcanvas = self.canvas.scaled(self.size(), qc.Qt.KeepAspectRatio)
        self.setPixmap(rcanvas)

        self.i = 0
        self.einschlag = False
        self.shooting = False
        self.leftclick = False
        #self.player = True  # True für Player1
        self.help = True

        self.init_difficulty()

    def random_krater(self):
        """Erstellt zufälligen Krater(zur Veranschaulichung)"""
        # Mountain Painter für Krater
        mountainPainter = qg.QPainter(self.mountainPix)
        mountainPainter.setCompositionMode(qg.QPainter.CompositionMode_Clear)
        mountainPainter.setPen(qc.Qt.black)
        mountainPainter.setBrush(qc.Qt.black)

        z = np.random.randint(0, self.width)
        mountainPainter.drawEllipse(qc.QPoint(self.randpixel[z][1], self.randpixel[z][0]), 30, 30)
        self.reload()

    def draw_krater(self, x, y, strength):
        """Erstellt Krater an gegebener Position mit gegebener Stärke(abhängig vom Projektil)"""
        # Mountain Painter für Krater
        mountainPainter = qg.QPainter(self.mountainPix)
        mountainPainter.setCompositionMode(qg.QPainter.CompositionMode_Clear)
        mountainPainter.setPen(qc.Qt.black)
        mountainPainter.setBrush(qc.Qt.black)

        krater = qc.QRectF(x, y, strength*0.6, strength*0.6)
        krater.moveCenter(qc.QPoint(x, y))
        mountainPainter.drawEllipse(krater)
        self.reload()
        return krater

    def draw_shoot(self, timestep, i):
        """Schuss von gegebenem Startpunkt"""
        if timestep == 0.0:
            return

        if self.player:
            if i == 0:
                self.x_kords, self.y_kords, self.i_krater = self.player1.shoot(timestep, self.player2)
            color = self.player1.loadedProjectile.color
            einschlag = self.player1.loadedProjectile.body
        else:
            if i ==0:
                self.x_kords, self.y_kords, self.i_krater = self.player2.shoot(timestep, self.player1)
            color = self.player2.loadedProjectile.color
            einschlag = self.player2.loadedProjectile.body

        einschlagspunkt = qc.QPoint(int(self.x_kords[i]), int(self.y_kords[i]))
        einschlag.moveCenter(einschlagspunkt)

        self.painter.fillRect(0, 0, self.width, self.height, self.skycolor)
        self.painter.drawPixmap(0, 0, self.mountainPix)
        self.draw_tank()

        self.painter.setPen(color)
        self.painter.setBrush(color)
        self.painter.drawEllipse(einschlag)
        rcanvas = self.canvas.scaled(self.size(), qc.Qt.KeepAspectRatio)
        self.setPixmap(rcanvas)

        if i == self.i_krater:
            if self.player1.hit_something(self.x_kords[i], self.y_kords[i], self.player2):
                self.xy_einschlag = (self.x_kords[i], self.y_kords[i])
            elif self.player2.hit_something(self.x_kords[i], self.y_kords[i], self.player1):
                self.xy_einschlag = (self.x_kords[i], self.y_kords[i])
            else:
                self.xy_einschlag = (self.x_kords[i-1], self.y_kords[i-1])
            self.einschlag = True

    def shoot_help_line(self, timestep):
        self.painter.setPen(qg.QPen(qc.Qt.red, 4))
        self.painter.setBrush(qc.Qt.red)
        if timestep == 0.0:
            return
        if self.player:
            x_kords, y_kords, i = self.player1.shoot(timestep, self.player2)
        else:
            x_kords, y_kords, i = self.player2.shoot(timestep, self.player1)

        i = 0
        while x_kords[i] or y_kords[i]:
            self.painter.drawPoint(int(x_kords[i]), int(y_kords[i]))
            if i >= 1500:
                break
            i += 1

        self.setPixmap(self.canvas)

    def zug(self):
        time = qc.QTime(0, 0, 0)
        if self.pause:
            return False, time
        if not self.p1arsenal and self.player:
            self.zug_finished = True
            if self.ki:
                self.gameover = True
                return True, time
        if not self.p2arsenal and not self.player:
            self.zug_finished = True
        if not(self.p1arsenal or self.p2arsenal):
            self.gameover = True
            return True, time
        if not self.projectileChoosen:
            return False, time

        if self.zug_finished:
            self.p1arsenal = self.player1.check_arsenal()
            self.p2arsenal = self.player2.check_arsenal()
            self.zug_finished = False
            self.player = not self.player
            self.projectileChoosen = False
            self.allowedtomove = True
            if self.difficulty == "advanced":
                time = qc.QTime(0, 0, 16)
            if self.difficulty == "hard":
                time = qc.QTime(0, 0, 11)
            if self.difficulty == "expert":
                time = qc.QTime(0, 0, 6)
            self.reload()

        if not self.player and self.ki:
            if not self.shooting:
                self.help = False
                self.leftclick = False  # Zug zu Ende
                self.i = 0
                self.einschlag = False
                self.shooting = True
                self.player2.computergegner(self.player1, self.difficulty)

        # Während des Schusses, ohne Einschlag
        if self.shooting and not self.einschlag:
            self.draw_shoot(0.1, self.i)
            self.i += 1

        # Wenn Einschlag erfolgte
        elif self.einschlag and self.shooting:
            # Koordinaten des Einschlags holen
            x = int(self.xy_einschlag[0])
            y = int(self.xy_einschlag[1])

            # Kanone des schießenden Spielers auswählen
            if self.player:
                strength = self.player1.loadedProjectile.power
            else:
                strength = self.player2.loadedProjectile.power

            # Krater zeichnen
            krater = self.draw_krater(x, y, strength) #2

            # Treffer abfragen
            player1_treffer = krater.intersects(self.player1.rect)
            player2_treffer = krater.intersects(self.player2.rect)
            if self.player1.hit_self(x, y):
                player1_treffer = True
            if self.player2.hit_self(x, y):
                player2_treffer = True
            if self.player1.hit_somebody(x, y, self.player2):
                player2_treffer = True
            if self.player1.hit_somebody(x, y, self.player1):
                player1_treffer = True

            # Treffer abfragen und Schaden berechnen
            if player1_treffer:
                if self.player1.hit_something(x, y, self.player2):
                    schaden = strength
                else:
                    x_abs = x - self.player1.placement[0]
                    y_abs = y - self.player1.placement[1]
                    abstand = np.sqrt(x_abs**2 + y_abs**2)
                    schaden = int(strength - abstand + 1)
                self.player1.livepoints -= schaden

            if player2_treffer:
                if self.player2.hit_something(x, y, self.player1):
                    schaden = strength
                else:
                    x_abs = x - self.player2.placement[0]
                    y_abs = y - self.player2.placement[1]
                    abstand = np.sqrt(x_abs ** 2 + y_abs ** 2)
                    schaden = int(strength - abstand + 1)
                self.player2.livepoints -= schaden

            # Boolsche Werte zur Spielkontrolle zurücksetzen
            self.shooting = False
            self.einschlag = False

            # Spielerwechsel
            self.zug_finished = True

        # Gameover, Rückgabe ob Spiel weitergeht oder abgeschlossen ist, für Wechsel des Widgets entscheidend
        if self.player1.livepoints <= 0:
            self.player1.livepoints = 0
            self.player2.score += 1
            self.gameover = True
            self.reload(3)#Panzer verschwindet
            return True, time
        elif self.player2.livepoints <= 0:
            self.player2.livepoints = 0
            self.player1.score += 1
            self.gameover = True
            self.reload(3)#panzer verschwindet
            return True, time
        return False, time

    def get_player_info(self):
        return self.player1, self.player2

    def choose_Projectile(self, i=0):
        if self.player:
            if not self.player1.set_projectile(i):
                return False
            return True
        else:
            if not self.player2.set_projectile(i):
                return False
            return True

    def pause_game(self):
        if self.pause:
            self.pause = False
            self.reload()
        else:
            self.pause = True
            self.painter.setFont(qg.QFont("Verdana", pointSize=150))
            self.painter.setPen(qg.QPen(qc.Qt.black, 2))
            self.painter.setBrush(qg.QColor(255, 255, 255, 150))
            self.painter.drawRect(0, 0, self.width, self.height)
            self.painter.setPen(qc.Qt.red)
            self.painter.drawText(qc.QRectF(self.width*1/4, self.height*1/3, 1000, 500), "Pause")
            self.rescale()
        return

    def keyPressEvent(self, ev: qg.QKeyEvent):
        """Key Events"""
        if ev.key() == qc.Qt.Key_Escape:
            self.close()
        if ev.key() == qc.Qt.Key_B:
            self.pause_game()

        if self.gameover or self.pause:
            return

        # Bewegung der Panzer erfolgt vor Schuss, Timer noch nicht eingebaut
        if not self.shooting and self.move:
            if self.allowedtomove:
                if ev.key() == qc.Qt.Key_D:
                    if self.player:
                        self.player1.move_tank(True)
                    else:
                        if not self.ki:
                            self.player2.move_tank(True)
                    self.reload()
                if ev.key() == qc.Qt.Key_A:
                    if self.player:
                        self.player1.move_tank(False)
                    else:
                        if not self.ki:
                            self.player2.move_tank(False)
                    self.reload()

    def mousePressEvent(self, ev: qg.QMouseEvent):
        """Maustasten Events + Spielerwechsel/Kontrolle"""
        if self.gameover or not self.projectileChoosen:
            return
        if self.pause:
            return

        if ev.button() == qc.Qt.LeftButton:
            if not self.shooting:
                self.leftclick = True #Linksklick erfolgt Spieler macht Zug
                if self.helpline:
                    self.help = True
                if self.player:
                    self.player1.move_Pipe(ev.x(), ev.y())
                else:
                    if not self.ki:
                        self.player2.move_Pipe(ev.x(), ev.y())
                    elif self.ki:
                        self.player2.computergegner(self.player1, self.difficulty)
                    else: print(1)

                self.reload(3)

    def mouseMoveEvent(self, ev: qg.QMouseEvent):
        if self.gameover or not self.projectileChoosen:
            return
        if self.pause:
            return

        if self.leftclick:
            if self.player:
                self.player1.move_Pipe(ev.x(), ev.y())
            else:
                if not self.ki:
                    self.player2.move_Pipe(ev.x(), ev.y())
                elif self.ki:
                    self.player2.computergegner(self.player1, self.difficulty)
                else:
                    print(1)
            self.reload(3)

    def mouseReleaseEvent(self, ev: qg.QMouseEvent):
        if self.gameover or not self.projectileChoosen:
            return
        if self.pause:
            return

        if ev.button() == qc.Qt.LeftButton:
            if self.leftclick and not self.shooting:
                self.help = False
                self.leftclick = False #Zug zu Ende
                self.i = 0
                self.einschlag = False
                self.shooting = True

if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    dis = Gamefield(1000, 500)
    dis.show()
    app.exec_()