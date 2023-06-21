import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("data.txt", skiprows=3)
rr = data[:, 6]  # y
time = np.arange(len(rr))  # x

M = 50  # größe fenster
p_grad = 3

midpunkte_x = np.arange(((M - 1) // 2), len(rr) - (M // 2))  # alle midpunkte der jeweiligen fenster
midpunkte_y = np.zeros(len(rr) - M + 1)


def MLS(x, i):
    coeff = np.polyfit(time[i:M + i], rr[i:M + i], x)  # rechne polynom im interval aus und setze mittelpunkt ein
    p = np.poly1d(coeff)  # speicher diesen wert ab
    wert = p(midpunkte_x[i])
    midpunkte_y[i] = wert


for i in range(len(midpunkte_y)):
    MLS(p_grad, i)

plt.plot(time, rr, '.', label="Werte")
plt.plot(midpunkte_x, midpunkte_y, label='MLS mit Polynomgrad ' + str(p_grad) + ' und Intervalgröße ' + str(M))
plt.ylim([min(midpunkte_y) - 5, max(midpunkte_y) + 5])
plt.legend()
plt.show()
