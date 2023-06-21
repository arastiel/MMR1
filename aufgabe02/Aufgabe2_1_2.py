'''Aufgabe 2 Extrapolation Qualitätsvergelich für Aufgabe 1_2'''
import numpy as np
import matplotlib.pyplot as plt


def larange_polynom(x, x_kords, k):
    """Bestimmt den Wert des Larange-Polynoms für ein x"""
    xk = x_kords[k]
    nenner_parts = xk - x_kords
    nenner_parts = np.delete(nenner_parts, k)
    zaehler_parts = x - x_kords
    zaehler_parts = np.delete(zaehler_parts, k)
    return np.prod(zaehler_parts / nenner_parts)


def polynom(x, x_kords, y_kords):
    """Bestimmt den Wert des Näherungspolynoms für ein x"""
    p = np.zeros(len(x_kords))
    for k in range(len(x_kords)):
        produkt = y_kords[k] * larange_polynom(x, x_kords, k)
        p[k] = produkt
    return np.sum(p)


def aufg1_2(rr, time, a):
    gitter = np.arange(0, len(rr), len(rr) // a)
    rr_2 = rr[gitter]
    time_2 = time[gitter]

    x_list = np.array(time)
    y_list = np.zeros(len(rr))

    i = 0
    for x in x_list:
        y_list[i] = polynom(x, time_2, rr_2)
        i += 1

    return x_list, y_list, time_2, rr_2


def E(y, M_x):
    n = len(M_x)
    summanden = (M_x - y) ** 2
    summe = np.sum(summanden) / n
    return summe


def quali1_2(train_size, time, rr):
    train_y = rr[:train_size]
    train_x = time[:train_size]

    test_y = rr[train_size:]
    test_x = time[train_size:]

    quali1 = np.ones(6)
    quali1x = np.arange(len(quali1))
    t = 0
    # Aufgabe 1
    for j in range(1, 7):
        tr_x1, tr_y1, trr, ttime = aufg1_2(train_y, train_x, j)

        test_x1 = test_x
        test_y1 = np.zeros(len(test_y))
        i = 0
        for x in test_x1:
            test_y1[i] = polynom(x, trr, ttime)
            i += 1

        # Qualität Aufgabe 1_2
        qualitaet_test1 = E(test_y, test_y1)
        quali1[t] = qualitaet_test1
        t += 1
    plt.plot(quali1x, quali1, label="Qualität Näherung Aufgabe 1_2, für train-size "+ str(train_size))

data = np.loadtxt("data.txt", skiprows=3)
rr = data[:, 6]  # y
time = np.arange(len(rr))  # x

quali1_2(420, time, rr)
quali1_2(440,time, rr)
quali1_2(460,time, rr)
quali1_2(480, time, rr)

plt.title("Aufgabe 2 - Qualität Aufgabe 1_2")
plt.legend()
plt.xlabel("Anzahl Datenpunkte")
plt.show()
