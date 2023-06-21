import skfmm
from PyQt5 import QtGui as qg
import numpy as np
from math import pi
from matplotlib import pyplot as plt


class sinfunc():
    """Container für verschiedene zufällige Sinusfunktionen"""
    def __init__(self, w):
        self.z1 = np.random.uniform(0, 2 * pi)
        self.z2 = np.random.uniform(-1, 1)
        self.w = w

    def __call__(self, x):
        """Gibt Wert der Funktion an Stelle x zurück"""
        return (1/np.sqrt(self.w/7)) * np.sin(self.w*x + self.z1) * self.z2


def func(W, X):
    """Funktion die Anhand übergebener Listen zufällige SInusfunktionen auswertet"""
    sinfunc_list = []
    for w in W:
        sinfunc_list.append(sinfunc(w))
    f = np.zeros(np.size(X))
    for i in range(np.size(f)):
        summe = 0
        for s in sinfunc_list:
            summe += s(i)
        f[i] = summe
    return f


def bildfunc(width, heigth, difficulty):
    """Erstellt Hügellandschaft anhand gegebener Weite und Höhe"""
    if difficulty == "easy":
        W = np.linspace(0.001, 0.01, 20)
    elif difficulty == "advanced":
        W = np.linspace(0.005, 0.02, 20)
    elif difficulty == "hard":
        W = np.linspace(0.01, 0.02, 20)
    elif difficulty == "expert":
        W = np.linspace(0.01, 0.02, 30)
    else:
        raise ValueError("Value of Difficulty not valid")

    X = np.linspace(0, 10, width)
    f = func(W, X) + heigth * 2/3
    huegel = np.zeros([heigth, width], dtype=np.bool)
    randpixel = np.zeros(width, dtype=tuple)

    for i in range(width):
        for j in range(heigth):
            if j > f[i]:
                huegel[j, i] = True
                if randpixel[i] == 0:
                    randpixel[i] = (j, i)
            else:
                huegel[j, i] = False

    # Farbverlauf
    map_dist = skfmm.distance(huegel)
    map_dist = map_dist / np.max(map_dist) * 1.2 + 0.6
    world = plt.cm.YlGn(map_dist)
    world[:, :, 3] = huegel
    world = np.asarray(world * 255, np.uint8)

    # Bildumwandlung
    return qg.QImage(world.data, width, heigth, qg.QImage.Format_RGBA8888), randpixel


if __name__ == "__main__":
    bild = bildfunc(1000, 500, "easy")
    bild1 = bildfunc(1500, 750, "hard")