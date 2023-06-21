import numpy as np
import matplotlib.pyplot as plt


data = np.loadtxt("data.txt", skiprows=3)
#data = data[1:5,:]
tx = data[:,6]
rr = data[:,12]
time = np.arange(len(tx))



#create figur + temperatur axis
fig, ax1 = plt.subplots()
ax1.plot(time, tx, color="#c40202")
ax1.set_xlabel("Zeitpunkt")
ax1.set_ylabel("Temperatur", color="#c40202")
ax1.tick_params('y', colors='#c40202')


#niederschlag axis
ax2 = ax1.twinx()       #create axis with same x-axis as ax1
ax2.plot(time, rr, '.', color="#1183cf")
ax2.set_ylabel("Niederschlag", color="#1183cf")
ax2.tick_params('y', colors='#1183cf')

plt.show()


