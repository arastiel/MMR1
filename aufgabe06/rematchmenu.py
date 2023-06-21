import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
from functools import partial


class RematchMenu(qw.QWidget):
    def __init__(self, b_yes, b_no):
        super().__init__()
        vbox = qw.QVBoxLayout()
        vbox.setAlignment(qc.Qt.AlignCenter)
        vbox.setSpacing(20)
        vbox.addStretch()

        self.titleLabel = qw.QLabel()
        vbox.addWidget(self.titleLabel)
        self.titleLabel.setText("Rematch?")
        self.titleLabel.setObjectName("rematch")
        self.titleLabel.setAlignment(qc.Qt.AlignCenter)

        vbox.addStretch()

        self.b_yes = b_yes
        vbox.addWidget(self.b_yes)

        self.b_no = b_no
        vbox.addWidget(self.b_no)

        vbox.addStretch()

        self.setStyleSheet(open("gamestylesheet.css").read())
        self.setLayout(vbox)


class GameOverview(qw.QWidget):
    def __init__(self, b_yes, b_no, init_dict=None):
        super().__init__()
        self.b_yes = b_yes
        self.b_no = b_no
        self.init_dict = init_dict
        self.setStyleSheet(open("gamestylesheet.css").read())
        self.rematch_layout = self.init_rematch()
        self.init_view()

    def init_rematch(self):
        vbox = qw.QVBoxLayout()
        vbox.setAlignment(qc.Qt.AlignCenter)
        hbox = qw.QHBoxLayout()
        hbox.setAlignment(qc.Qt.AlignCenter)
        title = qw.QLabel("Rematch?")
        title.setObjectName("rematch")
        title.setAlignment(qc.Qt.AlignCenter)

        hbox.addStretch()
        hbox.addWidget(self.b_yes)
        hbox.addWidget(self.b_no)
        hbox.addStretch()

        vbox.addStretch()
        vbox.addWidget(title)
        vbox.addLayout(hbox)
        vbox.addStretch()

        return vbox

    def init_view(self):
        if not self.init_dict:
            self.setLayout(self.rematch_layout)
            return
        vbox = qw.QVBoxLayout()
        vbox.setAlignment(qc.Qt.AlignCenter)
        vbox.addStretch()
        if self.init_dict["Type"] == 0:
            if not self.init_dict["Ki"]:
                title = qw.QLabel("Tie!")
                title.setObjectName("gameovertitle")
                title.setAlignment(qc.Qt.AlignCenter)

                vs = qw.QLabel(f"{self.init_dict['Player1']} vs. {self.init_dict['Player2']}")
                vs.setObjectName("vs")
                vs.setAlignment(qc.Qt.AlignCenter)

                score = qw.QLabel(f"{self.init_dict['Score'][0]} : {self.init_dict['Score'][1]}")
                score.setObjectName("score")
                score.setAlignment(qc.Qt.AlignCenter)

                vbox.addWidget(title)
                vbox.addWidget(vs)
                vbox.addWidget(score)

        elif self.init_dict["Type"] == 1:
            if not self.init_dict["Ki"]:
                if self.init_dict["Score"][0] > self.init_dict["Score"][1]:
                    title1 = qw.QLabel(f"Victory for {self.init_dict['Player1']}!")
                    title2 = qw.QLabel(f"Try harder next time {self.init_dict['Player2']}")
                else:
                    title1 = qw.QLabel(f"Victory for {self.init_dict['Player2']}!")
                    title2 = qw.QLabel(f"Try harder next time {self.init_dict['Player1']}")
                title1.setObjectName("gameovertitle")
                title1.setAlignment(qc.Qt.AlignCenter)
                title2.setObjectName("secondPlayer")
                title2.setAlignment(qc.Qt.AlignCenter)

                vs = qw.QLabel(f"{self.init_dict['Player1']} vs. {self.init_dict['Player2']}")
                vs.setObjectName("vs")
                vs.setAlignment(qc.Qt.AlignCenter)

                score = qw.QLabel(f"{self.init_dict['Score'][0]} : {self.init_dict['Score'][1]}")
                score.setObjectName("score")
                score.setAlignment(qc.Qt.AlignCenter)

                vbox.addWidget(title1)
                vbox.addWidget(title2)
                vbox.addWidget(vs)
                vbox.addWidget(score)

        elif self.init_dict["Type"] == 2:
            if self.init_dict["Ki"]:
                title = qw.QLabel("Game End!")
                title.setObjectName("gameovertitle")
                title.setAlignment(qc.Qt.AlignCenter)

                vs = qw.QLabel(f"{self.init_dict['Player1']} vs. Computer")
                vs.setObjectName("vs")
                vs.setAlignment(qc.Qt.AlignCenter)

                score = qw.QLabel(f"{self.init_dict['Score'][0]} : {self.init_dict['Score'][1]}")
                score.setObjectName("score")
                score.setAlignment(qc.Qt.AlignCenter)

                vbox.addWidget(title)
                vbox.addWidget(vs)
                vbox.addWidget(score)

                if self.init_dict["Highscore"]:
                    highscore = qw.QLabel("You created a new Highscore! Congratulations!")
                    highscore.setObjectName("highscore")
                    highscore.setAlignment(qc.Qt.AlignCenter)
                    vbox.addWidget(highscore)

        elif self.init_dict["Type"] == 3:
            if self.init_dict["Ki"]:
                title = qw.QLabel("Game Over...")
                title.setObjectName("gameovertitle")
                title.setAlignment(qc.Qt.AlignCenter)

                vs = qw.QLabel(f"{self.init_dict['Player1']} vs. Computer")
                vs.setObjectName("vs")
                vs.setAlignment(qc.Qt.AlignCenter)

                score = qw.QLabel(f"{self.init_dict['Score'][0]} : {self.init_dict['Score'][1]}")
                score.setObjectName("score")
                score.setAlignment(qc.Qt.AlignCenter)

                vbox.addWidget(title)
                vbox.addWidget(vs)
                vbox.addWidget(score)

                if self.init_dict["Highscore"]:
                    highscore = qw.QLabel("You created a new Highscore! Congratulations!")
                    highscore.setObjectName("highscore")
                    highscore.setAlignment(qc.Qt.AlignCenter)
                    vbox.addWidget(highscore)

        vbox.addLayout(self.rematch_layout)
        vbox.addStretch()
        self.setLayout(vbox)


if __name__== "__main__":
    app = qw.QApplication(sys.argv)
    dis = RematchMenu(qw.QPushButton("Yes"), qw.QPushButton("No"))
    over = GameOverview(qw.QPushButton("Yes"), qw.QPushButton("No"))
    #dis.show()
    over.show()
    app.exec_()