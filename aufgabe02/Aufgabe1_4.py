import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("data.txt", skiprows=3)
rr = data[:, 6]             #y
time = np.arange(len(rr))   #x

"""
#falls man nur ein fenster auswählen will

von_ = 267
bis_ = 450

time = time[max(von_-1,0):min(bis_,500)]
rr = rr[max(von_-1,0):min(bis_,500)]

#print(time)
"""

mean_y = np.mean(rr)
mean_x = np.mean(time)

xy_sum = np.prod((rr,time),axis=0)
xy_sum = np.sum(xy_sum)

x_sum = rr**2
x_sum = np.sum(x_sum)

m = np.true_divide((len(time)*mean_x*mean_y)-xy_sum,((len(time))*(mean_x**2)) - x_sum)
b = mean_y - (m * mean_x)

#print("y = " + str(m)+"x + " + str(b))

y = m*time + b

def polyxgrad(x):
    coeff = np.polyfit(time,rr,x)
    p = np.poly1d(coeff)
    #werte = p(np.linspace(0,499,500))
    werte = p(time)
    plt.plot(time,werte,label="Polynom mit Grad: " + str(x))


#desto höher der grad, desto genauer wird die funktion

plt.plot(time, rr, '.', label="Werte")
plt.plot(time, y, label="lineare Regression")

polyxgrad(3)
polyxgrad(5)
polyxgrad(10)

plt.legend()
plt.show()