'''Aufgabe 2 Extrapolation Qualitätsvergelich für Aufgabe 1_4'''

import numpy as np
import matplotlib.pyplot as plt


def E(y, M_x):
    n = len(M_x)
    summanden = (M_x - y) ** 2
    summe = np.sum(summanden) / n
    return summe

def polyxgrad(x, time, rr):
    coeff = np.polyfit(time, rr, x)
    p = np.poly1d(coeff)
    werte = p(time)
    return p, werte


def E(y, M_x):
    n = len(M_x)
    summanden = (M_x - y) ** 2
    summe = np.sum(summanden) / n
    return summe

def quali1_4(train_size, time, rr):
    train_y = rr[:train_size]
    train_x = time[:train_size]

    test_y = rr[train_size:]
    test_x = time[train_size:]

    quali1 = np.ones(8)
    quali1x = np.arange(len(quali1))
    t = 0

    for x in range(1, 9):
        p, train_y2 = polyxgrad(x, train_x, train_y)
        werte = p(test_x)

        qualitaet_test2 = E(test_y, werte)
        quali1[t] = qualitaet_test2
        t += 1

    plt.plot(quali1x, quali1, label="Qualität Aufgabe 1_4 für train-size " + str(train_size))


data = np.loadtxt("data.txt", skiprows=3)
rr = data[:, 6]  # y
time = np.arange(len(rr))  # x
train_size = int(len(rr) * 3 / 4)
quali1_4(420, time, rr)
quali1_4(440, time, rr)
quali1_4(460, time, rr)
quali1_4(480, time, rr)

plt.title("Aufgabe 2 - Qualität Aufgabe 1_4")
plt.legend()
plt.xlabel("Polynomgrad")
plt.show()
