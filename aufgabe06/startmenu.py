import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
from functools import partial


class StartMenu(qw.QLabel):
    def __init__(self, play_button):
        super().__init__()
        self.setStyleSheet(open("gamestylesheet.css").read())
        self.width = 1500
        self.height = 750
        #self.setFixedSize(self.width, self.height + 200)
        self.gamemode = "singleplayer"
        self.difficulty = "easy"

        vbox = qw.QVBoxLayout()
        vbox.setAlignment(qc.Qt.AlignCenter)
        vbox.setSpacing(20)
        vbox.addStretch()

        self.titleLabel = qw.QLabel()
        vbox.addWidget(self.titleLabel)
        self.titleLabel.setText("Artillery Simulator 2020")
        self.titleLabel.setObjectName("title")
        self.titleLabel.setAlignment(qc.Qt.AlignCenter)

        vbox.addStretch()

        ##### gamemode buttons #####

        self.b_single = qw.QPushButton("Singleplayer")
        self.b_single.clicked.connect(partial(self.setGamemode, "singleplayer"))
        vbox.addWidget(self.b_single)

        self.b_multi = qw.QPushButton("Multiplayer")
        self.b_multi.clicked.connect(partial(self.setGamemode, "multiplayer"))
        vbox.addWidget(self.b_multi)

        self.b_easy = qw.QPushButton("Easy")
        self.b_easy.clicked.connect(partial(self.setDifficulty, "easy"))
        vbox.addWidget(self.b_easy)

        self.b_advanced = qw.QPushButton("Advanced")
        self.b_advanced.clicked.connect(partial(self.setDifficulty, "advanced"))
        vbox.addWidget(self.b_advanced)

        self.b_hard = qw.QPushButton("Hard")
        self.b_hard.clicked.connect(partial(self.setDifficulty, "hard"))
        vbox.addWidget(self.b_hard)

        self.b_expert = qw.QPushButton("Expert")
        self.b_expert.clicked.connect(partial(self.setDifficulty, "expert"))
        vbox.addWidget(self.b_expert)

        ####### Player info #######

        hboxPlayer1 = qw.QHBoxLayout()
        hboxPlayer1.setAlignment(qc.Qt.AlignCenter)
        hboxPlayer1.setSpacing(2)
        hboxPlayer1.addStretch()

        self.player1Label = qw.QLabel()
        hboxPlayer1.addWidget(self.player1Label)
        self.player1Label.hide()

        self.player1Line = qw.QLineEdit()
        self.player1Line.setAlignment(qc.Qt.AlignCenter)
        hboxPlayer1.addWidget(self.player1Line)
        self.player1Line.hide()

        hboxPlayer1.addStretch()
        vbox.addLayout(hboxPlayer1)

        hboxPlayer2 = qw.QHBoxLayout()
        hboxPlayer2.setAlignment(qc.Qt.AlignCenter)
        hboxPlayer2.setSpacing(2)
        hboxPlayer2.addStretch()

        self.player2Label = qw.QLabel()
        hboxPlayer2.addWidget(self.player2Label)
        self.player2Label.hide()

        self.player2Line = qw.QLineEdit()
        self.player2Line.setAlignment(qc.Qt.AlignCenter)
        hboxPlayer2.addWidget(self.player2Line)
        self.player2Line.hide()

        hboxPlayer2.addStretch()
        vbox.addLayout(hboxPlayer2)

        ##### PLAY BUTTON #####
        self.b_play = play_button
        vbox.addWidget(self.b_play)
        #self.b_play.clicked.connect(self.startGame)

        self.b_back = qw.QPushButton("Back")
        self.b_back.setObjectName("back")
        self.b_back.clicked.connect(self.back)
        vbox.addWidget(self.b_back)

        vbox.addStretch()

        menu_buttons = [self.b_single, self.b_multi, self.b_easy, self.b_advanced, self.b_hard, self.b_expert,
                        self.b_play]
        menu_lines = [self.player1Line, self.player2Line]
        menu_labels = [self.player1Label, self.player2Label]
        hide_at_start = [self.b_easy, self.b_advanced, self.b_hard, self.b_expert, self.player1Line, self.player2Line,
                         self.player1Label, self.player2Label, self.b_play, self.b_back]

        [hide.hide() for hide in hide_at_start]

        self.setWindowTitle("Artillery Start Menu")
        vbox.addStretch()
        self.setLayout(vbox)

    def difficulty_menu(self):
        [button.hide() for button in [self.b_single, self.b_multi]]
        [button.show() for button in [self.b_easy, self.b_advanced, self.b_hard, self.b_expert, self.b_back]]

    def player_menu(self):
        [button.hide() for button in [self.b_easy, self.b_advanced, self.b_hard, self.b_expert]]
        if self.gamemode == "singleplayer":
            self.player1Label.setText("Player: ")
            [item.show() for item in [self.player1Label, self.player1Line, self.b_play, self.b_back]]

        if self.gamemode == "multiplayer":
            self.player1Label.setText("Player 1: ")
            self.player2Label.setText("Player 2: ")
            [item.show() for item in
             [self.player1Label, self.player1Line, self.player2Label, self.player2Line, self.b_play, self.b_back]]

    def setGamemode(self, mode):
        self.gamemode = mode
        self.difficulty_menu()

    def setDifficulty(self, diff):
        self.difficulty = diff
        self.player_menu()

    def back(self):
        if self.b_play.isVisible():
            [item.hide() for item in [self.player1Label, self.player1Line, self.player2Label, self.player2Line, self.b_play]]
            [button.show() for button in [self.b_easy, self.b_advanced, self.b_hard, self.b_expert]]
        else:
            [button.hide() for button in [self.b_easy, self.b_advanced, self.b_hard, self.b_expert, self.b_back]]
            [button.show() for button in [self.b_single, self.b_multi]]


    def get_settings(self):
        if self.gamemode == "singleplayer":
            return {"player1_name": self.player1Line.text(), "player2_name": None, "ki": True, "difficulty": self.difficulty}
        else:
            return {"player1_name": self.player1Line.text(), "player2_name": self.player2Line.text(), "ki": False, "difficulty": self.difficulty}
