from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
import sys
from gamefield import Gamefield
from gameinfo import Gameinfo
from tank import tank_player
import csv


class Game(qw.QWidget):
    def __init__(self,gameoverbutton=None, difficulty="advanced", ki=True, player1_name="Player 1", player2_name="Player 2"):
        super().__init__()
        self.setStyleSheet(open("gamestylesheet.css").read())
        self.gamefield = Gamefield(difficulty=difficulty, ki=ki,
                                   player1=tank_player(0, [(0, 0)], c=qg.QColor(140, 140, 140), n=player1_name),
                                   player2=tank_player(0, [(0, 0)], c=qg.QColor(140, 140, 140), n=player2_name))
        self.gameinfo = Gameinfo(gamefield=self.gamefield)
        self.gameoverbutton = gameoverbutton

        self.player1, self.player2 = self.gamefield.get_player_info()
        self.player1.name = player1_name
        self.player2.name = player2_name

        self.timer = qc.QTimer()
        self.new_level = False
        self.new_highscore = False
        self.gameovertype = 5

        self.init_layout()
        self.rungame()

    def init_layout(self):
        vbox = qw.QVBoxLayout()
        vbox.addWidget(self.gameinfo)
        vbox.addWidget(self.gamefield, alignment=qc.Qt.AlignCenter)

        self.setLayout(vbox)
        self.setMinimumSize(934, 714)
        self.resize(qc.QSize(1490, 991))

    def newlevel(self):
        self.gamefield.newback() # weitere Übergabe Schwierigkeitsstufe
        self.player1.livepoints = 100
        self.player2.livepoints = 100
        self.gameinfo.update_playerinfo()

    def change_background(self):
        self.gamefield.newback() # weitere Übergabe Schwierigkeitsstufe
        self.gameinfo.update_playerinfo()

    def break_game(self):
        self.gamefield.pause = False
        self.gamefield.pause_game()

    def update(self):
        if self.gamefield.pause:
            return
        self.gameinfo.update_playerinfo()

        if self.new_level:
            self.newlevel()
            self.new_level = False
            self.gamefield.gameover = False
            self.gamefield.player = True
            self.timer.setInterval(10)

        # Checken ob Spieler noch Munition haben
        if self.gamefield.player:
            if not self.player1.check_arsenal():
                self.gamefield.projectileChoosen = True
        else:
            if not self.player2.check_arsenal():
                self.gamefield.projectileChoosen = True

        # Zug kann erst gemacht werden, wenn Kanone gewählt wurde
        if not self.gamefield.projectileChoosen:
            if self.gameinfo.check_time():
                self.gamefield.allowedtomove = False
            else:
                self.gameinfo.update_time()
            # wenn gegen Computergegner gespielt wird, automatische Auswahl für KI
            if self.gamefield.ki and not self.gamefield.player:
                self.gameinfo.set_button_player2()
            else:
                return

        gameover, self.gameinfo.time = self.gamefield.zug()  # Spielzug
        # Checkt Spielende
        if gameover:
            if not self.gamefield.ki:
                self.gameinfo.update_playerinfo()
                self.timer.stop()
                self.gameovertype = 1
                self.gameoverbutton.click()
            elif self.player1.livepoints != 0 and self.gamefield.ki:
                if not self.player1.check_arsenal():
                    self.gameinfo.update_playerinfo()
                    self.timer.stop()
                    self.highscore()
                    self.gameovertype = 2
                    self.gameoverbutton.click()
                else:
                    self.gameinfo.update_playerinfo()
                    self.new_level = True
                    self.timer.setInterval(300)
            else:
                self.gameinfo.update_playerinfo()
                self.timer.stop()
                if self.gamefield.ki:
                    self.highscore()
                self.gameovertype = 3
                self.gameoverbutton.click()
            # Change Widget to GameoverView

    def rungame(self):
        self.gameinfo.setup_time()
        self.timer.setInterval(10)
        self.timer.timeout.connect(lambda: self.update())
        self.timer.start()

    def get_gamover_infos(self):
        if self.gameovertype == 1:
            if self.player1.livepoints and self.player2.livepoints:
                self.gameovertype = 0

        return {"Ki": self.gamefield.ki, "Player1": self.player1.name, "Player2": self.player2.name,
                "Score": (self.player1.score, self.player2.score), "Highscore": self.new_highscore,
                "Type": self.gameovertype}

    def compare_highscore(self, score1, score2):
        s1 = int(score1[0])-int(score1[2])
        s2 = int(score2[0])-int(score2[2])
        if s1 >= s2:
            return True
        return False

    def highscore(self):
        if self.player1.score == 0:
            self.new_highscore = False
            return
        content = self.read_highscore()
        content.sort()
        self.new_highscore = self.write_highscore(content)

    def read_highscore(self):
        content = []
        if self.gamefield.difficulty == "easy":
            file = "highscore_easy.csv"
        if self.gamefield.difficulty == "advanced":
            file = "highscore_advanced.csv"
        if self.gamefield.difficulty == "hard":
            file = "highscore_hard.csv"
        if self.gamefield.difficulty == "expert":
            file = "highscore_expert.csv"

        with open(file, "r") as hst:
            reader = csv.reader(hst)
            for lines in reader:
                if lines:
                    lines = lines[0].split(";")
                    content.append(lines)

        if content:
            content.pop(0)
        return content

    def write_highscore(self, content):
        score = f"{self.player1.score}:{self.player2.score}"

        if not content:
            place = 1
            content.append([str(place), self.player1, score])
        else:
            place = 1
            place_found = False
            for c in content:
                if not place_found:
                    if self.compare_highscore(score, c[2]):
                        place_found = True
                        c[0] = str(int(c[0])+1)
                    else:
                        place += 1
                else:
                    c[0] = str(int(c[0])+1)

            content.append([str(place), self.player1, score])
            content.sort()

            if len(content) >= 10:
                content = content[:10]

        if self.gamefield.difficulty == "easy":
            file = "highscore_easy.csv"
        if self.gamefield.difficulty == "advanced":
            file = "highscore_advanced.csv"
        if self.gamefield.difficulty == "hard":
            file = "highscore_hard.csv"
        if self.gamefield.difficulty == "expert":
            file = "highscore_expert.csv"

        with open(file, "w") as hst:
            fnames = ["Place", "Player", "Score"]
            writer = csv.writer(hst, delimiter=";")
            writer.writerow(fnames)
            for l in content:
                writer.writerow(l)

        if place >10:
            return False
        return True

    def keyPressEvent(self, ev: qg.QKeyEvent):
        if ev.key() == qc.Qt.Key_Escape:
            self.close()
        if ev.key() == qc.Qt.Key_R:
            self.change_background()

        self.gamefield.keyPressEvent(ev)


if __name__== "__main__":
    app = qw.QApplication(sys.argv)
    dis = Game()
    dis.show()
    app.exec_()