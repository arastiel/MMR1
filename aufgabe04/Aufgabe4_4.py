from math import *
import numpy as np
import sys
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc

from Aufgabe4_2_2 import *
from Aufgabe4_3 import *


class FunkPlot(qw.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FUnktionsplotter")

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.menu = PlotMenu()
        self.func_feld = self.menu.func_feld
        self.f = self.menu.get_func()
        self.x1, self.x2 = self.menu.xrange
        self.update_layout()
        self.plot()

        self.func_feld.editingFinished.connect(self.update_func)
        self.x1.editingFinished.connect(self.update_x)
        self.x2.editingFinished.connect(self.update_x)

    def update_x(self):
        self.ax.clear()
        self.plot()

    def update_layout(self):
        layout = qw.QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.menu)
        self.setLayout(layout)

    def update_func(self):
        if self.menu.check():
            self.f = self.menu.get_func()
            self.ax.clear()
            self.plot()

    def plot(self):
        x1 = int(self.x1.text())
        x2 = int(self.x2.text())
        step = (x2 - x1) * 100
        if step < 100:
            step = 100
        x = np.linspace(x1, x2, step)
        y = np.zeros(len(x))
        ya = np.zeros(len(x))
        abl = True
        for i in range(len(x)):
            d = self.f(x[i])
            y[i] = d.wert
            if type(d.ableitung) != str:
                ya[i] = d.ableitung
            else:
                abl = False
        self.ax.plot(x, y, color="red")
        if abl:
            self.ax.plot(x, ya, color="orange")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.canvas.draw()


class PlotMenu(qw.QWidget):
    def __init__(self):
        super().__init__()
        self.func_feld, self.xrange = self.init_menu()
        self.f = self.func_feld.text()
        self.func_feld.textChanged.connect(self.check_func)
        self.func_feld.editingFinished.connect(self.get_func)

    def init_menu(self):
        func_feld = qw.QLineEdit("** x 2")
        tfunc_feld = qw.QLabel("Function: ")

        x1 = qw.QLineEdit("-5")
        x2 = qw.QLineEdit("5")
        tx1_x2 = qw.QLabel("x-Range")

        xrange = qw.QHBoxLayout()
        xrange.addWidget(x1)
        xrange.addWidget(qw.QLabel("-"))
        xrange.addWidget(x2)

        validator = qg.QIntValidator()
        x1.setValidator(validator)
        x2.setValidator(validator)

        form = qw.QFormLayout()
        form.addRow(tfunc_feld, func_feld)
        form.addRow(tx1_x2, xrange)
        vbox = qw.QVBoxLayout()
        vbox.addLayout(form)
        self.setLayout(vbox)
        return func_feld, (x1, x2)

    def get_func(self):
        if self.check():
            f = Parser(self.func_feld.text())
            return f
        return self.f

    def check(self):
        try:
            Parser(self.func_feld.text())
            return True
        except:
            return False

    def check_func(self):
        try:
            Parser(self.func_feld.text())
            self.func_feld.setStyleSheet("color: black;")
        except:
            self.func_feld.setStyleSheet("color: red;")


if __name__ == "__main__":
    app = qw.QApplication(sys.argv)
    plot = FunkPlot()
    plot.show()

    sys.exit(app.exec_())
