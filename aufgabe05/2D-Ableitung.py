import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# Bild einlesen (bild.jpg ist im selben Verzeichnis, wie diese Datei enthalten)
# convert("L") übersetzt das bild in ein Graustufenbild (nur ein Kanal, statt dreien)
image = Image.open("xqcWeird.png").convert("L")

# konvertieren in ein numpy-array
img = np.asarray(image, dtype='int64')


def x_deriv(img):
    #berechne Ableitung nach x
    img_x = [[0 for x in range(len(img[0]))] for y in range(len(img))]
    for y in range(len(img)):
        for x in range(len(img[0])):
            if x == 0:
                img_x[y][x] = (img[y][x+1] - img[y][x]) / 2
            if x == len(img[0]) - 1:
                img_x[y][x] = (img[y][x] - img[y][x-1]) / 2
            else:
                img_x[y][x] = (img[y][x + 1] - img[y][x - 1]) / 2
    return img_x

def y_deriv(img): 
    #berechne Ableitung nach y 
    img_y = [[0 for x in range(len(img[0]))] for y in range(len(img))]
    for y in range(len(img)):
        for x in range(len(img[0])):
            if y == 0:
                img_y[y][x] = (img[y+1][x] - img[y][x]) / 2
            if y == len(img) - 1:
                img_y[y][x] = (img[y][x] - img[y-1][x]) / 2
            else:
                img_y[y][x] = (img[y+1][x] - img[y-1][x]) / 2
    return img_y

def le_deriv(img, img_y, img_x):
    #berechne Längenableitung
    img_le = [[0 for x in range(len(img[0]))] for y in range(len(img))]
    for y in range(len(img)):
        for x in range(len(img[0])):
            img_le[y][x] = (img_x[y][x]**2 + img_y[y][x]**2)**(1/2)
    return img_le

img_x = x_deriv(img)
img_y = y_deriv(img)
img_le = le_deriv(img, img_y, img_x)



fig = plt.figure()
ax_topleft = fig.add_subplot(221, title="grayscale")
ax_topright = fig.add_subplot(222, title="X-Ableitung")
ax_botleft = fig.add_subplot(223, title="Y-Ableitung")
ax_botright = fig.add_subplot(224, title="Länge-Ableitung")

# plot
ax_topleft.imshow(img, cmap='gray')
ax_topright.imshow(img_x, cmap='gray')
ax_botleft.imshow(img_y, cmap='gray')
ax_botright.imshow(img_le, cmap='gray')

# Title spacing
plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                    wspace=0.35)


plt.show()



