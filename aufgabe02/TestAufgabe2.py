import numpy as np
import matplotlib.pyplot as plt


# Extrapolation
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


def aufg1_2(rr, time):
    gitter = np.arange(0, len(rr), len(rr) // 6)
    rr_2 = rr[gitter]
    time_2 = time[gitter]

    x_list = np.array(time)
    y_list = np.zeros(len(rr))

    i = 0
    for x in x_list:
        y_list[i] = polynom(x, time_2, rr_2)
        i += 1

    return x_list, y_list, time_2, rr_2

def polyxgrad(x, time, rr, cl="#04b404"):
    coeff = np.polyfit(time, rr, x)
    p = np.poly1d(coeff)
    werte = p(time)
    plt.plot(time, werte, color=cl, label="Polynom mit Grad: " + str(x))
    return p, werte


def E(y, M_x):
    n = len(M_x)
    summanden = (M_x - y) ** 2
    summe = np.sum(summanden) / n
    return summe


data = np.loadtxt("data.txt", skiprows=3)
rr = data[:, 6]  # y
time = np.arange(len(rr))  # x

train_size = int(len(rr) * 3 / 4)
train_y = rr[:train_size]
train_x = time[:train_size]

test_y = rr[train_size:]
test_x = time[train_size:]

# Aufgabe 1
tr_x1, tr_y1, trr, ttime = aufg1_2(train_y, train_x)

test_x1 = test_x
test_y1 = np.zeros(len(test_y))
i = 0
for x in test_x1:
    test_y1[i] = polynom(x, trr, ttime)
    i += 1

# Qualität Aufgabe 1_2
qualitaet_test1 = E(test_y, test_y1)
quali_train1 = E(train_y, tr_y1)
print("Qualität der Naherung anhand Aufgabe 1_2")
print("Im Testteil: ", qualitaet_test1)
print("Im Train-teil: ", quali_train1)

# Aufgabe 1_4, Qualität
p, train_y2 = polyxgrad(5, train_x, train_y, "#088A29")
werte = p(test_x)
plt.plot(test_x, werte, color="#74DF00", label="Polynom mit Grad: ")

qualitaet_test2 = E(test_y, werte)
quali_train2 = E(train_y, train_y2)
print("Qualität der Naherung anhand Aufgabe 1_4")
print("Im Testteil: ", qualitaet_test2)
print("Im Train-teil: ", quali_train2)


plt.plot(time, rr, '.', color="#1183cf", label="Punkte")
plt.plot(tr_x1, tr_y1, color="#c40202", label="Näherungspolynom-train-bereich")
plt.plot(test_x1, test_y1, color="#df7401", label="Testbereich")
plt.ylim([-20, 50])
plt.legend()
plt.title("Aufgabe 2")
plt.show()
