import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("data.txt", skiprows=3)
rr = data[:, 6]

#konstante Approximation
mean = np.mean(rr)

#Stückweiser Mittelwert
N = 50      #Anzahl Abstand
split = np.arange(N-1, len(rr), N)
submean = np.zeros(len(split))

submean_ind = 0
for i in split:
    rr_split = rr[i-N+1:i+1]
    submean[submean_ind] = np.mean(rr_split)
    submean_ind += 1

#wenn die teile klein sind, ist der graph stark springend. wenn die teile größer werden, glättet sich der graph. das modell ist eventuell passend für periodische entwicklungen (jahreszeiten)

#Laufender Mittelwert
M = 6       #größe intervall
rmean_x = np.arange(((M-1)//2),len(rr)-((M)//2))
rmean_y = np.zeros(len(rr)-M+1)

for i in range(len(rr)-M+1):
    rr_rmean = rr[i:M+i]
    rmean_y[i] = np.mean(rr_rmean)

#gewichtet je nach größe des intervalls vergangene/zukünftige werte stark

plt.plot(rr, '.', label="Werte")
plt.plot(split, submean, label="Stückweiser Mittelwert")
plt.plot(rmean_x, rmean_y, label="Laufender Mittelwert")
plt.axhline(y=mean, color="#c40202", label="konstante Approximation")
plt.legend()
plt.show()