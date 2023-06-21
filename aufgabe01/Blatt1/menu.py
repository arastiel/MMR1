import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg


class SnakeMenu(qw.QWidget):
    """Erstellt und initialisiert Menü für Snake, Daten abrufbar"""
    def __init__(self):
        super().__init__()
        # Initialisierung Variablen
        self.var = []
        self.init_var = []

        # Initialisierung Fenster
        self.init_mainWindow()

    def init_mainWindow(self):
        """Initialisiere Window"""
        width = 500
        heigth = 400
        self.setWindowTitle("Snake Menüeinstellungen")
        self.setFixedSize(width, heigth)
        self.setWindowIcon(qg.QIcon("snake_icon.jpg"))

        # Initialisiert Widgets
        self.init_Widgets()
        # Buttonevents für Gamestart
        self.events()

    def init_Widgets(self):
        """Initialisiert Widgets und Variablen zum übergeben"""
        # Erstellung der Widgets zur Eingabe
        sfeldw = qw.QLineEdit("15")
        sfeldh = qw.QLineEdit("15")
        validator = qg.QIntValidator(10, 99)
        sfeldw.setValidator(validator)
        sfeldh.setValidator(validator)

        spielfeldwh = qw.QHBoxLayout()
        spielfeldwh.addWidget(sfeldw)
        spielfeldwh.addWidget(qw.QLabel("x"))
        spielfeldwh.addWidget(sfeldh)

        sname = qw.QLineEdit("Spieler1")

        startv = qw.QSpinBox()
        startv.setRange(10, 100)
        a = qw.QSpinBox()
        a.setRange(1, 20)
        a.setValue(5)

        rand = qw.QCheckBox("On")
        wkeit = qw.QSpinBox()
        wkeit.setRange(1, 100)
        wkeit.setValue(30)
        wkeit.isReadOnly()

        zoom = qw.QSpinBox()
        zoom.setRange(1, 50)
        zoom.setValue(30)

        mehrspieler = qw.QCheckBox()

        # Tooltips
        tsname = qw.QLabel("Spielername:")
        tsname.setToolTip("Geben sie ihren Spielernamen ein (hat Pfeiltasten)")
        tspielfeldwh = qw.QLabel("Spielgröße:")
        tspielfeldwh.setToolTip("Gebe die Maße des Spielfeldes an von 10 - 99 Pixel")
        tstartv = qw.QLabel("Anfangsgeschwindigkeit:")
        tstartv.setToolTip("Gebe die Anfangsgeschwindigkeit an von 10-100")
        ta = qw.QLabel("Beschleunigung:")
        ta.setToolTip("Gebe die Beschleunigung der Schlange nach jedem Essen an von 1-20")
        trand = qw.QLabel("Randbegrenzung:")
        trand.setToolTip("Für Rand setze Häckchen, dann darf Schlange sich nur im Feld bewegen")
        twkeit = qw.QLabel("Fruchtwahrscheinlichkeit:")
        twkeit.setToolTip("Je höher die Wkeit, desto mehr Früchte erscheinen (1-100)")
        tzoom = qw.QLabel("Zoom")
        tzoom.setToolTip("Bestimmt den Zoomfaktor (Maße Spielfeld * Zoom)")
        tmehrspieler = qw.QLabel("Mehrspielermodus:")
        tmehrspieler.setToolTip("Spiele zu zweit gegeneinander, wer mehr Früchte isst gewinnt! (Spieler2 hat Tasten W, S, A, Y)")

        # Erstellung des Layout
        self.form = qw.QFormLayout()
        self.form.addRow(tsname, sname)
        self.form.addRow(tspielfeldwh, spielfeldwh)
        self.form.addRow(tstartv, startv)
        self.form.addRow(ta, a)
        self.form.addRow(trand, rand)
        self.form.addRow(twkeit, wkeit)
        self.form.addRow(tzoom, zoom)
        self.form.addRow(tmehrspieler, mehrspieler)

        start = qw.QPushButton("Start Game")

        self.vbox = qw.QVBoxLayout()
        self.vbox.addLayout(self.form)
        self.vbox.addWidget(start)

        self.setLayout(self.vbox)

        # Speicherung der Widgets, die Variablen zur Initialisierung enthalten
        self.var = [start, sname, (sfeldh, sfeldw), startv, a, wkeit, rand, zoom, mehrspieler]

    def start_game(self):
        """Speichert bei Klicken auf Start die nötigen Variablen fürs Spiel"""
        variables = self.var

        # holt variablen aus Widgets
        playername = variables[1].text()
        feld_wh = (variables[2][0].text(), variables[2][1].text())
        v_start = variables[3].value()
        a = variables[4].value()
        wkeit = variables[5].value()
        rand = variables[6].isChecked()
        zoom = variables[7].value()
        mehrspieler = variables[8].isChecked()

        # speichert diese in einer Liste, setzt Start auf True und schließt Fenster
        self.init_var = [playername, feld_wh, v_start, a, wkeit, rand, zoom, mehrspieler]
        self.close()

    def events(self):
        """Prüft ob Start betätigt wurde und ruft wenn, start_game auf"""
        start = self.var[0]
        start.clicked.connect(self.start_game)
        mehrspieler = self.var[8]
        mehrspieler.clicked.connect(self.start_mehrspieler)

    def start_mehrspieler(self):
        return

    def get_initvars(self):
        """Gibt Variablen zum Initialisieren des Spiels zurück"""
        return self.init_var

def spawn():
    app = qw.QApplication(sys.argv)
    sm = SnakeMenu()
    sm.show()
    app.exec_()
    return sm.get_initvars()


if __name__ == '__main__':
    init_vars = spawn()
    print(init_vars)
