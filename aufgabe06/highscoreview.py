import sys
import csv
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc


class HighscoreView(qw.QWidget):
    def __init__(self, difficulty="hard"):
        super().__init__()
        self.setStyleSheet(open("gamestylesheet.css").read())
        self.difficulty = difficulty

        title = qw.QLabel(f"Highscore for Level: {self.difficulty}")
        title.setObjectName("gameovertitle")
        title.setAlignment(qc.Qt.AlignCenter)

        grid = self.set_content()

        vbox = qw.QVBoxLayout()
        vbox.addWidget(title)
        vbox.addLayout(grid)
        vbox.addStretch()
        self.setLayout(vbox)

    def read_highscore(self):
        content = []
        if self.difficulty == "easy":
            file = "highscore_easy.csv"
        if self.difficulty == "advanced":
            file = "highscore_advanced.csv"
        if self.difficulty == "hard":
            file = "highscore_hard.csv"
        if self.difficulty == "expert":
            file = "highscore_expert.csv"

        with open(file, "r") as hst:
            reader = csv.reader(hst)
            for lines in reader:
                if lines:
                    lines = lines[0].split(";")
                    content.append(lines)
        return content

    def set_content(self):
        content = self.read_highscore()
        grid = qw.QGridLayout()
        grid.setAlignment(qc.Qt.AlignCenter)
        if not content:
            no_high = qw.QLabel("No Highscores yet")
            no_high.setObjectName("highscore_item")
            grid.addWidget(no_high, 1, 1, 1, 1)

        for n in range(0, len(content)):
            for m in range(0, len(content[0])):
                item = qw.QLabel(content[n][m])
                item.setObjectName("highscore_item")
                grid.addWidget(item, n, m, 1, 1)
        return grid


if __name__== "__main__":
    app = qw.QApplication(sys.argv)
    high = HighscoreView()
    high.show()


    app.exec_()