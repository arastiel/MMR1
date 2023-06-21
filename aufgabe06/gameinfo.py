from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
import numpy as np
import sys
from matplotlib import pyplot as plt
from gamefield import Gamefield


class LiveDisplay(qw.QLabel):
    def __init__(self, player_id=1):
        super().__init__()
        self.player_id = player_id
        l = np.arange(0, 100)
        if player_id == 2:
            l = np.flip(l)
        l_norm = l/np.max(l)
        live_color = plt.cm.RdYlGn(l_norm)
        live_color = np.asarray(live_color*255, np.uint8)
        self.live_color_img = qg.QImage(live_color, 100, 1, qg.QImage.Format_RGBA8888)
        self.live_color_pix = qg.QPixmap.fromImage(self.live_color_img)
        live_color_pix_scaled = self.live_color_pix.scaled(self.size())
        self.setPixmap(live_color_pix_scaled)

    def resizeEvent(self, a0: qg.QResizeEvent):
        live_color_pix_scaled = self.live_color_pix.scaled(self.size())
        self.setPixmap(live_color_pix_scaled)

    def loose_livepoints(self, livepoints=25):
        l = np.arange(0, livepoints)
        if self.player_id == 2:
            l = np.flip(l)
        d = np.ones(100-livepoints)
        l = np.asarray(l)
        l_norm = l/100
        live_color = plt.cm.RdYlGn(l_norm)
        live_color = np.asarray(live_color*255, np.uint8)
        damage_color = plt.cm.binary(d)
        damage_color = np.asarray(damage_color*255, np.uint8)
        if self.player_id == 1:
            self.live_color_img = qg.QImage(np.append(live_color, damage_color), 100, 1, qg.QImage.Format_RGBA8888)
        if self.player_id ==2:
            self.live_color_img = qg.QImage(np.append(damage_color, live_color), 100, 1, qg.QImage.Format_RGBA8888)
        self.live_color_pix = qg.QPixmap.fromImage(self.live_color_img)
        live_color_pix_scaled = self.live_color_pix.scaled(self.size())
        self.setPixmap(live_color_pix_scaled)


class Gameinfo(qw.QLabel):
    def __init__(self, gamefield=None, time=qc.QTime(0, 0, 0)):
        super().__init__()
        if gamefield:
            self.gamefield = gamefield
        else:
            self.gamefield = Gamefield()
        self.time = time
        self.setStyleSheet(open("gamestylesheet.css").read())

        self.player1_info, self.player2_info, self.stopwatch = self.init_labels()
        self.player1, self.player2 = self.gamefield.get_player_info()

        self.setMinimumSize(908, 227)
        self.setMaximumHeight(227)

    def init_labels(self):
        player1, player2 = self.gamefield.get_player_info()

        # Player1 Info
        player1_name = qw.QLabel(player1.name)
        player1_name.setObjectName("player_name_score")
        player1_name.setToolTip("Name von Spieler 1")
        player1_score = qw.QLabel(str(player1.score))
        player1_score.setObjectName("player_name_score")
        player1_score.setToolTip(f"Score von {player1.name}")
        player1_live = LiveDisplay(1)
        player1_live.setToolTip(f"Lebensanzeige von {player1.name}")

        # ArsenalButtons for Player1
        p1arsenal = player1.list_arsenal()
        p1arsenal_1 = qw.QPushButton(p1arsenal[0])
        p1arsenal_1.setToolTip(f"Kanone von {player1.name}: (Anzahl x maximaler Schaden)")
        p1arsenal_2 = qw.QPushButton(p1arsenal[1])
        p1arsenal_2.setToolTip(f"Kanone von {player1.name}: (Anzahl x maximaler Schaden)")
        p1arsenal_3 = qw.QPushButton(p1arsenal[2])
        p1arsenal_3.setToolTip(f"Kanone von {player1.name}: (Anzahl x maximaler Schaden)")

        # Connect Buttons for Player1 with Function
        p1arsenal_1.clicked.connect(lambda: self.button_projectile(p1arsenal_1, 1))
        p1arsenal_2.clicked.connect(lambda: self.button_projectile(p1arsenal_2, 1))
        p1arsenal_3.clicked.connect(lambda: self.button_projectile(p1arsenal_3, 1))

        # Layout for Player 1
        vbox_player1 = qw.QVBoxLayout()
        vbox_player1.addWidget(player1_name)
        vbox_player1.addWidget(player1_live)

        hbox_player1_arsenal = qw.QHBoxLayout()
        hbox_player1_arsenal.addWidget(p1arsenal_1)
        hbox_player1_arsenal.addWidget(p1arsenal_2)
        hbox_player1_arsenal.addWidget(p1arsenal_3)
        hbox_player1_arsenal.addStretch()

        # Player2 Info
        player2_name = qw.QLabel(player2.name)
        player2_name.setObjectName("player_name_score")
        player2_name.setToolTip("Name von Spieler 2")
        player2_name.setAlignment(qc.Qt.AlignRight|qc.Qt.AlignCenter)
        player2_score = qw.QLabel(str(player2.score))
        player2_score.setObjectName("player_name_score")
        player2_score.setToolTip(f"Score von {player2.name}")
        player2_live = LiveDisplay(2)
        player2_live.setAlignment(qc.Qt.AlignRight|qc.Qt.AlignCenter)
        player2_live.setToolTip(f"Lebensanzeige von {player2.name}")

        # ArsenalButtons for Player2
        p2arsenal = player2.list_arsenal()
        p2arsenal.reverse()
        p2arsenal_1 = qw.QPushButton(p2arsenal[0])
        p2arsenal_1.setToolTip(f"Kanone  von {player2.name}: (Anzahl x maximaler Schaden)")
        p2arsenal_2 = qw.QPushButton(p2arsenal[1])
        p2arsenal_2.setToolTip(f"Kanone  von {player2.name}: (Anzahl x maximaler Schaden)")
        p2arsenal_3 = qw.QPushButton(p2arsenal[2])
        p2arsenal_3.setToolTip(f"Kanone  von {player2.name}: (Anzahl x maximaler Schaden)")
        p2arsenal_buttons = [p2arsenal_3, p2arsenal_2, p2arsenal_1]

        # Connect Buttons for Player2 with Function
        p2arsenal_1.clicked.connect(lambda: self.button_projectile(p2arsenal_1, 2))
        p2arsenal_2.clicked.connect(lambda: self.button_projectile(p2arsenal_2, 2))
        p2arsenal_3.clicked.connect(lambda: self.button_projectile(p2arsenal_3, 2))

        # Layout for Player2
        vbox_player2 = qw.QVBoxLayout()
        vbox_player2.addWidget(player2_name)
        vbox_player2.addWidget(player2_live)

        hbox_player2_arsenal = qw.QHBoxLayout()
        hbox_player2_arsenal.addStretch()
        hbox_player2_arsenal.addWidget(p2arsenal_1)
        hbox_player2_arsenal.addWidget(p2arsenal_2)
        hbox_player2_arsenal.addWidget(p2arsenal_3)

        # Timer
        stopwatch = qw.QLabel(self.time.toString("mm:ss"))
        stopwatch.setObjectName("stopwatch")
        stopwatch.setAlignment(qc.Qt.AlignCenter)
        stopwatch.setToolTip("Zeigt an wielange man sich noch bewegen kann")
        # Score
        score_trenner = qw.QLabel(":")
        score_trenner.setAlignment(qc.Qt.AlignCenter)
        hbox_score = qw.QHBoxLayout()
        hbox_score.addWidget(player1_score)
        hbox_score.addWidget(qw.QLabel(":"))
        hbox_score.addWidget(player2_score)

        grid = qw.QGridLayout()

        grid.addLayout(vbox_player1, 1, 1, 2, 2)
        grid.addWidget(qw.QLabel(""), 1, 3, 2, 1)
        grid.addLayout(hbox_score, 1, 4, 2, 1)
        grid.addWidget(qw.QLabel(""), 1, 5, 2, 1)
        grid.addLayout(vbox_player2, 1, 6, 2, 2)

        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(6, 1)

        grid.addLayout(hbox_player1_arsenal, 3, 1, 1, 1)
        grid.addWidget(stopwatch, 3, 4, 1, 1)
        grid.addLayout(hbox_player2_arsenal, 3, 6, 1, 1)

        self.setLayout(grid)

        return (player1_name, [player1_live, 100], player1_score), (player2_name, [player2_live, 100], player2_score, p2arsenal_buttons), stopwatch

    def button_projectile(self, button, player_id):
        text = button.text()

        if self.gamefield.projectileChoosen:
            return

        if self.gamefield.player and player_id == 1:
            liste = self.gamefield.player1.list_arsenal()
            for i in range(0, len(liste)):
                if liste[i] == text:
                    projectile_i = i
                    if self.gamefield.choose_Projectile(projectile_i):
                        self.gamefield.projectileChoosen = True
                        button.setText(self.gamefield.player1.list_arsenal()[i])

        elif not self.gamefield.player and player_id == 2 and not self.gamefield.ki:
            liste = self.gamefield.player2.list_arsenal()
            for i in range(0, len(liste)):
                if liste[i] == text:
                    projectile_i = i
                    if self.gamefield.choose_Projectile(projectile_i):
                        self.gamefield.projectileChoosen = True
                        button.setText(self.gamefield.player2.list_arsenal()[i])
        return

    def set_button_player2(self):
        buttons = self.player2_info[3]
        button_id = np.random.randint(0, len(buttons))
        if self.gamefield.choose_Projectile(button_id):
            buttons[button_id].setText(self.player2.list_arsenal()[button_id])
            self.gamefield.projectileChoosen = True
            return True
        return False

    def update_playerinfo(self):
        if self.player1.name != self.player1_info[0].text():
            self.player1_info[0].setText(self.player1.name)
        if self.player1.livepoints != self.player1_info[1][1]:
            self.player1_info[1][0].loose_livepoints(self.player1.livepoints)
            self.player1_info[1][1] = self.player1.livepoints
        if self.player1.score != self.player1_info[2].text():
            self.player1_info[2].setText(str(self.player1.score))

        if self.player2.name != self.player2_info[0].text():
            self.player2_info[0].setText(self.player2.name)
        if self.player2.livepoints != self.player2_info[1][1]:
            self.player2_info[1][0].loose_livepoints(self.player2.livepoints)
            self.player2_info[1][1] = self.player2.livepoints
        if self.player2.score != self.player2_info[2].text():
            self.player2_info[2].setText(str(self.player2.score))


    def update_time(self):
        self.time = self.time.addMSecs(-10)
        self.stopwatch.setText(self.time.toString("mm:ss"))

    def check_time(self):
        if self.time.toString("mm:ss") == "00:00":
            return True
        return False

    def setup_time(self):
        if self.gamefield.difficulty == "advanced":
            self.time = qc.QTime(0, 0, 16)
        if self.gamefield.difficulty == "hard":
            self.time = qc.QTime(0, 0, 11)
        if self.gamefield.difficulty == "expert":
            self.time = qc.QTime(0, 0, 6)


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    dis = Gameinfo()
    dis.show()
    app.exec_()