import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from math import *

fig = plt.figure()
ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
line, = ax.plot([], [], ".", markersize=13, color="red")
line3, = ax.plot([], [], ".", markersize=13, color="orange")
line2, = ax.plot([], [], "-", color="green", lw=1)
ax.plot(0, 0, "x", color="black")

m1 = 1
m2 = 1
l1 = 1
l2 = 1
g = 9.81
friction = 0.99

gt = 7
delta_t = 0.05


def alphabetha2(al, be, al1, al2, be1, be2):
    n_al = -g/l1 * sin(al) - ((l2*m2) / l1*(m1+m2)) * (cos(al-be) * be2 + sin(al-be) * be1**2)
    n_be = -g/l2 * sin(be) - l1/l2 * (cos(al-be) * al2 - sin(al-be) * al1**2)
    return n_al, n_be


def alpha(al, al1, be, be1, dt):
    n_al = al1 * dt + al
    n_bl = be1 * dt + be
    return n_al, n_bl


def alpha1(al2, al1, be2, be1, dt):
    n_al1 = (al2 * dt + al1)*friction
    n_be1 = (be2 * dt + be1)*friction
    return n_al1, n_be1


def get_simulation():
    d_t = np.arange(0, gt, delta_t)
    s = len(d_t)
    a = np.zeros(s)
    a1 = np.zeros(s)
    a2 = np.zeros(s)
    a[0] = radians(60)
    a1[0] = 0

    b = np.zeros(s)
    b1 = np.zeros(s)
    b2 = np.zeros(s)
    b[0] = radians(90)
    b1[0] = 0
    a2[0], b2[0] = alphabetha2(a[0], b[0], a1[0], a2[0], b1[0], b2[0])
    for t in range(1, s):
        a[t], b[t] = alpha(a[t - 1], a1[t - 1], b[t-1], b1[t-1], delta_t)
        a1[t], b1[t] = alpha1(a2[t - 1], a1[t - 1], b2[t-1], b1[t-1], delta_t)
        a2[t], b2[t] = alphabetha2(a[t], b[t], a1[t], a2[t], b1[t], b2[t])

    return a, b


a, b = get_simulation()
ax1 = l1 * np.sin(a)
ax2 = -l1 * np.cos(a)
bx1 = l2 * np.sin(b) + ax1
bx2 = -l2 * np.cos(b) + ax2

def init():
    line2.set_data([0, ax1[0], bx1[0]], [0, ax2[0], bx2[0]])
    line.set_data(ax1[0], ax2[0])
    line3.set_data(bx1[0], bx2[0])
    return line2, line, line3,


def animate(dt):
    line2.set_data([0, ax1[dt], bx1[dt]], [0, ax2[dt], bx2[dt]])
    line.set_data(ax1[dt], ax2[dt])
    line3.set_data(bx1[dt], bx2[dt])
    return line2, line, line3,


anim = FuncAnimation(fig, animate, init_func=init,
                     frames=np.arange(0, int(gt / delta_t), 1), interval=10, blit=True)

anim.save('Doppelpendel.gif', writer='imagemagick')
