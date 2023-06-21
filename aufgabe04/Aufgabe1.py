import numpy as np
from matplotlib import pyplot as plt

data = np.loadtxt("data.txt", skiprows=3)
y_data = data[:, 6]
x_data = np.arange(len(y_data))

"als tupel"
tuple_data = np.vstack((x_data, y_data)).T

sin_func = np.sin
sin_func2 = lambda x: np.sin(1/x)
norm_func = lambda x: (x**3)
vorzeige_func = lambda x: (1/8)*(x**4) - (1/4)*(x**3) - (13/8)*(x**2) + (7/4)*x + 1

x_cords = np.arange(-10, 11, 0.001)
x_cords2 = np.arange(-4, 4, 0.001)


def newt_1(h, data, function, my_function=0):
    if function:
        y_cords = my_function(data)
        diff_x_cords = data+h
        diff_y_cords = my_function(diff_x_cords)
        newt_diff = (diff_y_cords - y_cords) / h
        return newt_diff, y_cords

    else:
        data_req_tupel = np.vstack((data[h:-h, 0], data[h:-h, 1])).T
        f_xh = data_req_tupel[:, 1]
        f_x = data[:-h * 2, 1]
        newt_diff = (f_xh - f_x) / h
        return newt_diff


def newt_2(h, data, function, my_function=0):
    if function:
        y_cords = my_function(data)
        xh1 = data+h
        f_xh1 = my_function(xh1)
        xh2 = data-h
        f_xh2 = my_function(xh2)
        newt_diff = (f_xh1 - f_xh2) / (2*h)
        return newt_diff, y_cords
    else:
        data_req_tupel = np.vstack((data[h:-h, 0], data[h:-h, 1])).T
        f_xh1 = data[h*2:, 1]
        f_xh2 = data[:-h * 2, 1]
        newt_diff = (f_xh1 - f_xh2) / (2*h)
        return newt_diff


"kleiners h approximiert Minima/Maxima besser"
def maxmin(der_y, orig_y, orig_x):
    for i in range(len(der_y)-1):
        if der_y[i] <= 0:
            if der_y[i+1] > 0:
                plt.plot(orig_x[i], orig_y[i], "ob", color="red")
        else:
            if der_y[i+1] <= 0:
                plt.plot(orig_x[i], orig_y[i], "ob", color="green")


"""Aufgabe 1.1a"""


def DiffQuoFunc(my_function, h, x_cords, newt):
    if newt == 1:
        newt_diff = newt_1(h, x_cords, True, my_function)
        print(newt_diff[0])
        plt.plot(x_cords, newt_diff[1], label="my function")
        plt.plot(x_cords, newt_diff[0], label="derivative of my function with h=" + str(h))
    else:
        newt_diff = newt_2(h, x_cords, True, my_function)
        plt.plot(x_cords, newt_diff[1], label="my function")
        plt.plot(x_cords, newt_diff[0], label="derivative of my function with h=" + str(h))
    maxmin(newt_diff[0], newt_diff[1], x_cords)


"uncomment for diff with function (h freiwählbar)"
DiffQuoFunc(sin_func, 1, x_cords, 1)
#DiffQuoFunc(sin_func2, 0.1, x_cords, 2)
#DiffQuoFunc(norm_func, 1, x_cords, 1)
#DiffQuoFunc(vorzeige_func, 0.1, x_cords2, 2)


"""Aufgabe 1.1b"""


def DiffQuoData(h, data_tuple, newt):
    if newt == 1:
        newt_diff = (newt_1(h, data_tuple, False))
        plt.plot(data_tuple[:, 0], data_tuple[:, 1], label="orig. data")
        plt.plot(data_tuple[:-h*2, 0], newt_diff, label="derivative of data with h="+ str(h))
    else:
        newt_diff = (newt_2(h, data_tuple, False))
        plt.plot(data_tuple[:, 0], data_tuple[:, 1], label="orig. data")
        plt.plot(data_tuple[h:-h, 0], newt_diff, label="derivative of data with h=" + str(h))
    "maxmin sieht nicht so gut aus bei den punkten... "
    #maxmin(newt_diff, data_tuple[:, 1], data_tuple[:, 0])


"uncomment for diff with data (h 1er Schritte)"
#DiffQuoData(1, tuple_data, 1)


"""Aufgabe 1.2"""


def polyf(grad, data_tupel):
    coeff = np.polyfit(data_tupel[:, 0], data_tupel[:, 1], grad)
    p = np.poly1d(coeff)
    new_y = p(data_tupel[:, 0])
    return data_tupel[:, 0], new_y, p


def DiffQuoPolyf(h, data_tuple, newt):
    polyf_req_tupel = np.vstack((data_tuple[h:-h, 0], data_tuple[h:-h, 1])).T
    new_werte = polyf(5, polyf_req_tupel)
    DiffQuoFunc(new_werte[2], h, new_werte[0], newt)
    plt.plot(data_tuple[:, 0], data_tuple[:, 1], label="orig. data")


"uncomment for diff with data (polyfitted, h 1er Schritte)"
#DiffQuoPolyf(1, tuple_data, 1)


plt.grid()
plt.legend()
plt.show()
