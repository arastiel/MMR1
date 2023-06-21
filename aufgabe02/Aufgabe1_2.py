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


data = np.loadtxt("data.txt", skiprows=3)
rr = data[:, 6]
time = np.arange(len(rr))

# Auswahl Punkte
gitter = np.arange(0, len(rr), len(rr) // 4)
rr_2 = rr[gitter]
time_2 = time[gitter]

# Initialisierung für Näherungspolynom
x_list = np.array(time)
y_list = np.zeros(len(rr))

# Bestimme Näherungspolynom auf Wertebereich
i = 0
for x in x_list:
    y_list[i] = polynom(x, time_2, rr_2)
    i += 1

# Bestimme und plotte Larange_Polynome für jeweiligen k-Werte
ii = 0
larange_poly = np.zeros(len(time))
for k in range(len(time_2)):
    for x in x_list:
        larange_poly[ii] = rr_2[k] * larange_polynom(x, time_2, k)
        ii += 1
    if k < len(time_2) - 1:
        plt.plot(x_list, larange_poly, color="#c40202", alpha=0.3)
    ii = 0

# Zeichne ausgewählte Punkte und Näherungspolynom
plt.plot(x_list, larange_poly, color="#c40202", alpha=0.3, label="Larange-Polynome")
plt.plot(time_2, rr_2, '.', color="#1183cf", label="Punkte")
plt.plot(x_list, y_list, color="#c40202", label="Näherungspolynom")
plt.ylim([-20, 50])  # Nur zur besseren/übersichtlicheren Ansicht
plt.legend()
plt.title("Aufgabe 1.2 Polynominterpolation")
plt.show()
