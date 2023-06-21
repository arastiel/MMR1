import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from math import *

fig = plt.figure()
ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
line, = ax.plot([], [], ".", markersize=13, color="red")
line2, = ax.plot([], [], "-", color="green", lw=1)
ax.plot(0, 0, "x", color="black")

m = 1
l = 1
g = 9.81
friction = 0.98

gt = 10
delta_t = 0.05


def alpha2(al):
    n_a = -g / l * sin(al)
    return n_a


def alpha(al, v, dt):
    n_a = v * dt + al
    return n_a


def alpha1(al, v, dt):
    al = alpha2(al)
    n_v = (al * dt + v)*friction
    return n_v


def get_simulation():
    d_t = np.arange(0, gt, delta_t)
    s = len(d_t)
    x1 = np.zeros(s)
    x2 = np.zeros(s)
    a1 = np.zeros(s)
    a = np.zeros(s)
    a[0] = radians(60)
    a1[0] = 0
    x1[0] = l * sin(a[0])
    x2[0] = -l * cos(a[0])

    for t in range(1, s):
        a[t] = alpha(a[t - 1], a1[t - 1], delta_t)
        a1[t] = alpha1(a[t - 1], a1[t - 1], delta_t)
        x1[t] = l * sin(a[t])
        x2[t] = -l * cos(a[t])
    return x1, x2, a, a1


x1, x2, a, v = get_simulation()

def init():
    line2.set_data([0, x1[0]], [0, x2[0]])
    line.set_data(x1[0], x2[0])
    return line2, line,


def animate(dt):
    line2.set_data([0, x1[dt]], [0, x2[dt]])
    line.set_data(x1[dt], x2[dt])
    return line2, line,


anim = FuncAnimation(fig, animate, init_func=init,
                     frames=np.arange(0, int(gt / delta_t), 1), interval=10, blit=True)

anim.save('Fadenpendel.gif', writer='imagemagick')
