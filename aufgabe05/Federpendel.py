import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure()
ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
line, = ax.plot([], [], ".", markersize=13, color="red")
line2, = ax.plot([], [], "-", color="green", lw=1, alpha=0.5)
ax.plot(0, 0, "x", color="black")

#D1 = 0.8
#D2 = 0.6
D1 = 1
D2 = 1
m = 1
friction = 0.9995
delta_t = 0.02
gt = 10


def a(x1, x2):
    a1 = -(D1 / m) * x1
    a2 = -(D2 / m) * x2
    return a1, a2


def x(x1, x2, v1, v2, dt):
    n_x1 = v1 * dt + x1
    n_x2 = v2 * dt + x2
    return n_x1, n_x2


def v(x1, x2, v1, v2, dt):
    a1, a2 = a(x1, x2)
    n_v1 = (a1 * dt + v1)*friction
    n_v2 = (a2 * dt + v2)*friction
    return n_v1, n_v2


def get_simulation():
    d_t = np.arange(0, gt, delta_t)
    s = len(d_t)
    x1 = np.zeros(s)
    x2 = np.zeros(s)
    v1 = np.zeros(s)
    v2 = np.zeros(s)
    x1[0] = 1
    x2[0] = 0
    v1[0] = -0.5
    v2[0] = 0.5
    #x1[0] = 1
    #x2[0] = 0.5
    #v1[0] = -0.2
    #v2[0] = 0.2
    for t in range(1, s):
        x1[t], x2[t] = x(x1[t - 1], x2[t - 1], v1[t - 1], v2[t - 1], delta_t)
        v1[t], v2[t] = v(x1[t - 1], x2[t - 1], v1[t - 1], v2[t - 1], delta_t)
    return x1, x2, v1, v2


x1, x2, v1, v2 = get_simulation()

def init():
    ax.plot(x1, x2, "-", color="blue", lw=1)
    line.set_data(x1[0], x2[0])
    return line,


def animate(dt):
    line.set_data(x1[dt], x2[dt])
    line2.set_data([x1[dt], x1[dt]+v1[dt]], [x2[dt], x2[dt]+v2[dt]])
    return line, line2,


anim = FuncAnimation(fig, animate, init_func=init,
                     frames=np.arange(0, int(gt / delta_t), 1), interval=20, blit=True)

anim.save('Federpendel.gif', writer='imagemagick')
