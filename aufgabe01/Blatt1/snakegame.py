# Muss ausgeführt werden um Spiel zu starten
import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
from menu import SnakeMenu
from snakegamefeld import SnakeGameFeld


class MainGame(qw.QMainWindow):
    def __init__(self, sm):
        super().__init__()

        # hole Variablen aus Kontrollmenü
        self.snakeMenu = sm
        vars = self.snakeMenu.get_initvars()
        self.playername = vars[0]
        self.sb, self.sh = int(vars[1][0]), int(vars[1][1])
        self.v = 320 - int(vars[2]) * 2
        self.a = int(vars[3])
        self.wkeit = int(vars[4])
        self.rand = vars[5]
        self.zoom = vars[6]
        self.mehrspieler = vars[7]
        self.player2 = "Spieler2"

        # Initialisiere Timer
        self.timer = qc.QTimer()

        # Erstelle Spielfeld und andere essentielle Widgets
        self.Spielfeld = SnakeGameFeld(self.sb, self.sh, self.v, self.a, self.wkeit, self.rand, self.zoom, self.timer,
                                       self.mehrspieler)
        self.spielablauf = qw.QWidget()
        self.punktestand = self.Spielfeld.get_points()
        self.punktestand2 = 0

        self.Feld = qw.QWidget()
        self.stat = self.statusBar()
        self.enddialog = qw.QDialog()
        self.dialoglist = self.end_dialog()

        # Initialisiere Widgets und speicherung von weiteren Widgets
        self.widget_punktestand = self.set_spielablauf()
        self.set_MainWindow()
        self.rungame()
        self.show()

    def set_spielablauf(self):
        """Erstelle Anzeige zum Spielablauf"""
        widget_playername = qw.QLabel("Spieler: " + self.playername)
        widget_points = qw.QLabel("Punkte: " + str(self.Spielfeld.get_points()))
        wpointslist = [widget_points]

        hbox = qw.QHBoxLayout()
        hbox.addWidget(widget_playername)
        hbox.addStretch()
        hbox.addWidget(widget_points)
        vbox = qw.QVBoxLayout()
        vbox.addLayout(hbox)

        if self.mehrspieler:
            widget_player2 = qw.QLabel("Spieler2:" + self.player2)
            widget_points2 = qw.QLabel("Punkte: " + str(self.Spielfeld.get_points2()))
            hbox2 = qw.QHBoxLayout()
            hbox2.addWidget(widget_player2)
            hbox2.addStretch()
            hbox2.addWidget(widget_points2)
            vbox.addLayout(hbox2)
            wpointslist.append(widget_points2)

        self.spielablauf.setLayout(vbox)
        return wpointslist

    def set_MainWindow(self):
        """Initialisert MainWindow"""
        self.setWindowTitle("Snake")
        self.setCentralWidget(self.Feld)
        self.setWindowIcon(qg.QIcon("snake_icon.jpg"))

        menu = self.menuBar()
        m1 = menu.addMenu("Menü")

        close = qw.QAction("Spiel beenden", self)
        close.setShortcut(qc.Qt.Key_Escape)
        close.setStatusTip("Beendet das Spiel")
        close.triggered.connect(lambda: self.ende())
        m1.addAction(close)

        rest = qw.QAction("Spiel neu starten", self)
        rest.setShortcut(qc.Qt.Key_N)
        rest.setStatusTip("Startet das Spiel neu")
        rest.triggered.connect(lambda: self.restart())
        m1.addAction(rest)

        pause = qw.QAction("Pause", self)
        pause.setShortcut(qc.Qt.Key_Space)
        pause.setStatusTip("Pausiert das Spiel")
        pause.triggered.connect(lambda: self.pause())
        m1.addAction(pause)

        grid = qw.QGridLayout()
        grid.addWidget(self.spielablauf)
        grid.addWidget(self.Spielfeld)
        grid.setRowStretch(1, 2)
        self.Feld.setLayout(grid)

    def end_dialog(self):
        """Initialisiert Dialoganzeige fürs Spielende"""
        self.enddialog.setWindowTitle("Snake")
        self.enddialog.setWindowIcon(qg.QIcon("snake_icon.jpg"))
        end = qw.QPushButton("Beenden", self.enddialog)
        rest = qw.QPushButton("Neu starten", self.enddialog)

        text = qw.QLabel(self.playername + " hat " + str(self.punktestand) + " Punkte erreicht!")
        hbox = qw.QHBoxLayout()

        hbox.addWidget(end)
        hbox.addWidget(rest)

        vbox = qw.QVBoxLayout()
        vbox.addWidget(text)
        text2 = qw.QLabel(self.player2 + " hat " + str(self.punktestand2) + " Punkte erreicht!")
        winner = qw.QLabel(
            self.playername + " hat mit " + str(self.punktestand - self.punktestand2) + " Punkten gewonnen!")

        if self.mehrspieler:
            vbox.addWidget(text2)
            if self.punktestand >= self.punktestand2:
                winner = qw.QLabel(
                    self.playername + " hat mit " + str(self.punktestand - self.punktestand2) + " Punkten gewonnen!")
            else:
                winner = qw.QLabel(
                    self.player2 + " hat mit " + str(self.punktestand2 - self.punktestand) + " Punkten gewonnen!")
            vbox.addWidget(winner)

        vbox.addLayout(hbox)
        self.enddialog.setLayout(vbox)

        rest.clicked.connect(lambda: self.restart())
        rest.setDefault(True)
        end.clicked.connect(lambda: self.ende())

        if self.mehrspieler:
            return [text, text2, winner]
        else:
            return [text]

    def dialog(self):
        text = self.dialoglist[0]
        text.setText(self.playername + " hat " + str(self.punktestand) + " Punkte erreicht!")
        if self.mehrspieler:
            text2 = self.dialoglist[1]
            winner = self.dialoglist[2]
            text2.setText(self.player2 + " hat " + str(self.punktestand2) + " Punkte erreicht!")
            if self.punktestand >= self.punktestand2:
                winner.setText(self.playername + " hat mit " + str(self.punktestand - self.punktestand2) + " Punkten gewonnen!")
            else:
                winner.setText(self.player2 + " hat mit " + str(self.punktestand2 - self.punktestand) + " Punkten gewonnen!")
        self.enddialog.exec_()

    def pause(self):
        """Pausiert Spiel"""
        self.Spielfeld.set_pause()
        self.stat.showMessage("Pause! (zum weiterspielen Leertaste oder Pause-Button betätigen)", 2000)

    def check_points(self):
        """Überprüft Punktestand und aktualisiert Anzeige bei Veränderung"""
        if self.Spielfeld.get_points() != self.punktestand:
            self.widget_punktestand[0].setText("Punkte: " + str(self.Spielfeld.get_points()))
            self.punktestand = self.Spielfeld.get_points()
            if self.punktestand != 0:
                self.stat.showMessage("Frucht gegessen!", 1000)
        if self.mehrspieler:
            if self.Spielfeld.get_points2() != self.punktestand2:
                self.widget_punktestand[1].setText("Punkte: " + str(self.Spielfeld.get_points2()))
                self.punktestand2 = self.Spielfeld.get_points2()
                if self.punktestand2 != 0:
                    self.stat.showMessage("Frucht gegessen!", 1000)
        return

    def update(self):
        """Spielablauf"""
        self.Spielfeld.zug()
        self.check_points()
        if self.Spielfeld.ende:
            self.stat.showMessage("Du bist Tod... :/", 2000)
            self.dialog()

    def rungame(self):
        """Spiel"""
        self.timer.setInterval(self.v)
        self.timer.timeout.connect(lambda: self.update())
        self.timer.start(self.v)

    def restart(self):
        """Neustart des Spiels"""
        self.Spielfeld.v = self.v
        self.Spielfeld.restart()
        self.enddialog.close()
        self.stat.showMessage("Neustart efolgt", 2000)

    def ende(self):
        """Beendet Spiel, schließ alle offenen Fenster"""
        self.close()
        self.enddialog.close()

    def keyPressEvent(self, e):
        if e.key() == qc.Qt.Key_Up:
            self.Spielfeld.snake.set_richtung("U")
        if e.key() == qc.Qt.Key_Down:
            self.Spielfeld.snake.set_richtung("D")
        if e.key() == qc.Qt.Key_Right:
            self.Spielfeld.snake.set_richtung("R")
        if e.key() == qc.Qt.Key_Left:
            self.Spielfeld.snake.set_richtung("L")

        if self.mehrspieler:
            if e.key() == qc.Qt.Key_W:
                self.Spielfeld.snake2.set_richtung("U")
            if e.key() == qc.Qt.Key_Y:
                self.Spielfeld.snake2.set_richtung("D")
            if e.key() == qc.Qt.Key_S:
                self.Spielfeld.snake2.set_richtung("R")
            if e.key() == qc.Qt.Key_A:
                self.Spielfeld.snake2.set_richtung("L")

        if e.key() == qc.Qt.Key_N:
            self.restart()
        if e.key() == qc.Qt.Key_Escape:
            self.ende()


def anfang():
    app1 = qw.QApplication(sys.argv)
    sm = SnakeMenu()
    sm.show()
    app1.exec()
    app = qw.QApplication(sys.argv)
    MainGame(sm)
    app.exec_()


if __name__ == '__main__':
    anfang()
