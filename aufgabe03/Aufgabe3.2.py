import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc

import numpy as np
from matplotlib import pyplot as plt


class mandelbild(qw.QLabel):
    def __init__(self, w, h, n, x1, y1, x2, y2):
        super().__init__()
        self.width = w
        self.heigth = h
        self.n = n
        self.xy = (x1, y1, x2, y2)
        self.mousedownxy = x1, y1
        self.draw_bild()
        self.show()

    def draw_bild(self):
        x1, y1, x2, y2 = self.xy
        M = mandelbrot(self.n, self.width, self.heigth, x1, y1, x2, y2)
        colormap = plt.get_cmap("RdGy")
        colfloat = colormap(M)
        colint = np.asarray(colfloat * 255, dtype=np.uint8)

        img = qg.QImage(colint.data, self.width, self.heigth, qg.QImage.Format_RGBA8888)
        pixmap = qg.QPixmap.fromImage(img)
        self.setPixmap(pixmap)

    def keyPressEvent(self, e):
        if e.key() == qc.Qt.Key_Escape:
            self.close()

    def mousePressEvent(self, e):
        self.clickedx_1 = e.x()
        self.clickedy_1 = e.y()

    def mouseReleaseEvent(self, e):
        self.clickedx_2 = e.x()
        self.clickedy_2 = e.y()
        print(self.clickedx_2)
        print(self.clickedy_2)

        x_1 = self.xy[0]
        x_2 = self.xy[1]
        y_1 = self.xy[2]
        y_2 = self.xy[3]

        new_x1 = (self.clickedx_1 / self.width) * abs(x_1 - x_2) + x_1
        new_x2 = (self.clickedx_2 / self.width) * abs(x_1 - x_2) + x_1
        new_y1 = (self.clickedy_1 / self.heigth) * abs(y_1 - y_2) + y_1
        new_y2 = (self.clickedy_2 / self.heigth) * abs(y_1 - y_2) + y_1

        #umscalen (viel zu lange gebraucht dafür)

        self.xy = (new_x1,new_x2,new_y1,new_y2)

        self.draw_bild()

def mandelbrot(n, width, heigth, x1, y1, x2, y2):
    a = np.linspace(x1, y1, num=heigth).reshape((1, heigth))
    b = np.linspace(x2, y2, num=width).reshape((width, 1))
    c = np.tile(a, (heigth, 1)) + 1j * np.tile(b, (1, width))
    #print(c)
    zn = np.zeros((width, heigth), dtype=complex)
    l = np.full((width, heigth), True, dtype=bool)

    M = np.zeros((width, heigth), dtype=np.uint8)

    for i in range(n):
        zn[l] = zn[l] * zn[l] + c[l]
        l[np.abs(zn) > 2] = False
        M[l] = i
    return M

app = qw.QApplication(sys.argv)
mbild = mandelbild(700, 700, 100, -2, 1, -1, 1)
app.exec_()
