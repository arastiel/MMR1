from PyQt5 import QtCore as qc
import numpy as np


class tank_player():
    """Klasse für Spieler/Panzer, Container der Daten für Spielernamen und Score, sowie Visualisierungselemente des
    Panzers """

    def __init__(self, x, randpixel, n="Player", c=qc.Qt.black):
        """Initialisierung eines Spielers"""
        self.name = n
        self.score = 0
        self.livepoints = 100
        self.color = c
        self.arsenal = [[Projectile(50), 2],[Projectile(75), 2], [Projectile(100), 2]]
        self.loadedProjectile = Projectile(50, qc.Qt.magenta)  # ausgewählte Kanone für den Schuss

        # Position des Panzers anhand gegebenen x-Wert und Liste der Hügelgrenze
        self.randpixel = randpixel
        self.placement = (randpixel[x][1], randpixel[x][0])  # Mittelpunkt des Panzers
        self.x = x

        # Erstellung der Zeichenelemente
        self.rect = qc.QRectF(self.placement[0], self.placement[1], 40, 30)
        self.rect.moveCenter(qc.QPoint(self.placement[0], self.placement[1]))
        self.dach = qc.QRectF(self.placement[0], self.placement[1], 30, 30)
        self.dach.moveCenter(qc.QPoint(self.placement[0], self.placement[1] - 15))
        self.pipe_xy = (self.placement[0], self.placement[1] - 22)  # Endpunkt des Kanonenrohrs (relevant für Schussstartpunkt)
        self.pipe = qc.QLine(self.pipe_xy[0], self.pipe_xy[1], self.placement[0] + 30, self.placement[1] - 22)

        self.cos, self.sin = (0, 0)

    def move_Pipe(self, x, y):
        """Passt die Koordinaten des Kanonenrohrs an, um Bewegung zu simulieren; Übergabe von x und y Koordinaten"""
        xdist = x - self.placement[0]
        ydist = y - self.placement[1]
        betrag = np.sqrt(xdist * xdist + ydist * ydist)
        x2 = 30 * xdist / betrag + self.placement[0]
        y2 = 30 * ydist / betrag + self.placement[1] -22

        self.pipe = qc.QLine(x2, y2, self.placement[0], self.placement[1]-22)
        self.pipe_xy = (x2, y2)

        # für Schuss
        self.cos = xdist/betrag
        self.sin = ydist/betrag

    def move_tank(self, right):
        """Bewegt Panzer nach rechts(right=True) und links(right=False)"""
        if right:
            self.x = self.x + 1
            if self.x >= len(self.randpixel):
                self.x = 0
        else:
            self.x = self.x - 1
            if self.x < 0:
                self.x = len(self.randpixel)-1
        self.placement = (self.randpixel[self.x][1], self.randpixel[self.x][0])
        self.rect = qc.QRectF(self.placement[0], self.placement[1], 40, 30)
        self.rect.moveCenter(qc.QPoint(self.placement[0], self.placement[1]))
        self.dach = qc.QRectF(self.placement[0], self.placement[1], 30, 30)
        self.dach.moveCenter(qc.QPoint(self.placement[0], self.placement[1] - 15))
        self.pipe_xy = (self.placement[0], self.placement[1] - 22)
        self.pipe = qc.QLine(self.pipe_xy[0], self.pipe_xy[1], self.placement[0] + 30, self.placement[1] - 22)

    def new_back(self, randpixel, x):
        """Passt Panzer zu neuem Hintergrund an"""
        self.randpixel = randpixel
        self.placement = (randpixel[x][1], randpixel[x][0])
        self.x = x
        self.rect = qc.QRectF(self.placement[0], self.placement[1], 40, 30)
        self.rect.moveCenter(qc.QPoint(self.placement[0], self.placement[1]))
        self.dach = qc.QRectF(self.placement[0], self.placement[1], 30, 30)
        self.dach.moveCenter(qc.QPoint(self.placement[0], self.placement[1] - 15))
        self.pipe_xy = (self.placement[0], self.placement[1] - 22)
        self.pipe = qc.QLine(self.pipe_xy[0], self.pipe_xy[1], self.placement[0] + 30, self.placement[1] - 22)

    def computergegner(self, gegner, difficulty):
        variance = 0

        if difficulty == "easy":
            variance = np.random.randint(-200, 200)
        elif difficulty == "advanced":
            variance = np.random.randint(-150, 150)
        elif difficulty == "hard":
            variance = np.random.randint(-60, 60)
        elif difficulty == "expert":
            variance = np.random.randint(-20, 20)

        x_gegner = gegner.placement[0] + variance
        y_gegner = gegner.randpixel[x_gegner][1]

        v0 = 90
        t = 20

        self.cos = (x_gegner - self.pipe_xy[0])/(t * v0)
        self.sin = (y_gegner - self.pipe_xy[1])/(t * v0) - (9.81*t)/(2*v0)

        x2 = 30 * self.cos + self.placement[0]
        y2 = 30 * self.sin + self.placement[1] - 22

        self.pipe = qc.QLine(x2, y2, self.placement[0], self.placement[1] - 22)
        self.pipe_xy = (x2, y2)

    def hit_something(self, x, y, gegner):
        if self.rect.contains(x, y) or self.dach.contains(x, y):
            return True
        if gegner.rect.contains(x, y) or gegner.dach.contains(x, y):
            return True
        return False

    def hit_self(self, x, y):
        if self.rect.contains(x, y) or self.dach.contains(x, y):
            return True
        return False

    def hit_somebody(self, x, y, gegner):
        if gegner.rect.contains(x, y) or gegner.dach.contains(x, y):
            return True
        return False

    def shoot(self, timestep, gegner):
        v0 = 90
        t = 0
        i = 0
        anz = len(self.randpixel)
        x_kords = np.zeros(anz)
        y_kords = np.zeros(anz)

        while i < len(self.randpixel):
            if i > 1500:
                break
            x_kords[i] = v0 * self.cos * t + self.pipe_xy[0]
            y_kords[i] = v0 * self.sin * t + 1/2 * 9.81 * t**2 + self.pipe_xy[1]
            t += timestep
            # Abbruchbedingungen
            if x_kords[i] > len(self.randpixel):  # Rand überschritten
                break
            if x_kords[i] < 0:
                break
            if self.hit_something(x_kords[i], y_kords[i], gegner):
                break

            if y_kords[i] >= self.randpixel[int(x_kords[i])][0]:  # Boden getroffen
                x_kords[i] = 0
                y_kords[i] = 0
                break
            i += 1

        return x_kords, y_kords, i

    def str_arsenal(self):
        s = str()
        for i in self.arsenal:
            s += f"({i[1]}x{i[0]})"
        return s

    def list_arsenal(self):
        l = list()
        for i in self.arsenal:
            l.append(f"({i[1]}x{i[0]})")
        return l

    def get_projectile(self, i=0):
        if self.arsenal:
            projectile = self.arsenal[i][0]
            if self.arsenal[i][1] == 0:
                return
            self.arsenal[i][1] -= 1
            return projectile

    def set_projectile(self, i=0):
        if self.arsenal[i][1] == 0:
            return False
        projectile = self.arsenal[i][0]
        self.arsenal[i][1] -= 1
        self.loadedProjectile = projectile
        return True

    def check_arsenal(self):
        for i in self.arsenal:
            if i[1]:
                return True
        return False

    def set_arsenal(self, anzahl:int):
        for p in self.arsenal:
            p[1] = anzahl

    def __str__(self):
        return self.name

class Projectile():
    """Klasse für Projektil/Kanonenkugel"""

    def __init__(self, p=50, c=qc.Qt.black):
        self.power = p  # Schusskaft
        self.color = c
        self.body = qc.QRectF(0, 0, 10, 10)  # zum zeichnen analog wie beim Panzer

    def __str__(self): return f"{self.power}"

    def __repr__(self): return f"{self.power}"
