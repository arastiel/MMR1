import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
from gamewidget import Game
from dialogwidgets import Help
from startmenu import StartMenu
from rematchmenu import RematchMenu, GameOverview
from highscoreview import HighscoreView


class GameMainWindow(qw.QMainWindow):
    def __init__(self):
        """MainWindow des Spiels zur Verwaltung/Ablauf des Spieles"""
        super().__init__()
        self.setStyleSheet(open("gamestylesheet.css").read())

        self.init_game_data = dict()
        self.gameoverbutton = qw.QPushButton("Gameover")
        self.play_button = qw.QPushButton("Play")
        self.yes_button = qw.QPushButton("Yes")
        self.no_button = qw.QPushButton("No")

        self.game = Game(gameoverbutton=self.gameoverbutton)
        self.startmenu = StartMenu(self.play_button)
        self.help = Help()
        self.rematch = RematchMenu(self.yes_button, self.no_button)
        self.gameover = GameOverview(self.yes_button, self.no_button)
        self.highscore = None

        self.stackedWidget = qw.QStackedWidget()
        self.stackedWidget.addWidget(self.game)
        self.stackedWidget.addWidget(self.startmenu)
        self.stackedWidget.addWidget(self.rematch)
        self.stackedWidget.addWidget(self.gameover)
        self.stackedWidget.setCurrentWidget(self.startmenu)

        self.play_button.clicked.connect(self.start_game)
        self.yes_button.clicked.connect(self.rematch_game)
        self.no_button.clicked.connect(self.new_game)
        self.gameoverbutton.clicked.connect(self.gameover_view)

        self.setCentralWidget(self.stackedWidget)
        self.resize(self.game.size())

        self.init_menu()

    def init_menu(self):
        self.setWindowTitle("Artillery Game")
        menu = self.menuBar()
        menu.setNativeMenuBar(False)

        highscore_menu = menu.addMenu("Highscores")
        h_easy = highscore_menu.addAction("Easy")
        h_advanced = highscore_menu.addAction("Advanced")
        h_hard = highscore_menu.addAction("Hard")
        h_expert = highscore_menu.addAction("Expert")
        h_easy.triggered.connect(lambda: self.highscore_view("easy"))
        h_advanced.triggered.connect(lambda: self.highscore_view("advanced"))
        h_hard.triggered.connect(lambda: self.highscore_view("hard"))
        h_expert.triggered.connect(lambda: self.highscore_view("expert"))

        new = menu.addAction("New Game")
        new.triggered.connect(self.new_game)
        new.setShortcut("Ctrl-N")
        new.setToolTip("Neues Spiel starten")

        help = menu.addAction("Help")
        help.setShortcut(qc.Qt.Key_F1)
        help.setToolTip("Klicke hier, wenn du Hilfe zum Spiel brauchst!")
        help.triggered.connect(lambda : self.help_dialog())

        pause = menu.addAction("Pause")
        pause.setShortcut(qc.Qt.Key_B)
        pause.setToolTip("Klicke hier oder betätige die Taste B, um das Spiel anzuhalten")
        pause.triggered.connect(lambda : self.pause())

        close = menu.addAction("Close")
        close.setShortcut(qc.Qt.Key_Escape)
        close.setToolTip("Schließt die Anwendung")
        close.triggered.connect(lambda: self.close())
        close.setShortcut(qc.Qt.Key_Escape)

    def highscore_view(self, difficulty):
        if self.highscore:
            self.stackedWidget.removeWidget(self.highscore)
        self.highscore = HighscoreView(difficulty)
        self.stackedWidget.addWidget(self.highscore)
        self.stackedWidget.setCurrentWidget(self.highscore)

    def pause(self):
        self.game.gamefield.pause_game()

    def help_dialog(self):
        self.game.break_game()
        self.help.show()

    def new_game(self):
        self.stackedWidget.removeWidget(self.startmenu)
        self.startmenu = StartMenu(self.play_button)
        self.stackedWidget.addWidget(self.startmenu)
        self.stackedWidget.setCurrentWidget(self.startmenu)

    def start_game(self, rematch=False):
        if not rematch:
            init_data = self.startmenu.get_settings()
            self.init_game_data = init_data
        else:
            init_data = self.init_game_data
        difficulty = init_data["difficulty"]
        ki = init_data["ki"]
        player1_name = init_data["player1_name"]
        if init_data["player2_name"]:
            player2_name = init_data["player2_name"]
            self.init_game(difficulty=difficulty, ki=ki, player1_name=player1_name, player2_name=player2_name)
        else:
            self.init_game(difficulty=difficulty, ki=ki, player1_name=player1_name)
        self.stackedWidget.setCurrentWidget(self.game)

    def init_game(self, difficulty="advanced", ki=True, player1_name="Player 1", player2_name="Player 2"):
        self.stackedWidget.removeWidget(self.game)
        self.game = Game(gameoverbutton=self.gameoverbutton, difficulty=difficulty, ki=ki, player1_name=player1_name, player2_name=player2_name)
        self.stackedWidget.addWidget(self.game)

    def rematch_game(self):
        self.start_game(rematch=True)

    def gameover_view(self):
        init_dict = self.game.get_gamover_infos()
        self.stackedWidget.removeWidget(self.gameover)
        self.gameover = GameOverview(self.yes_button, self.no_button, init_dict=init_dict)
        self.stackedWidget.addWidget(self.gameover)
        self.stackedWidget.setCurrentWidget(self.gameover)

    def keyPressEvent(self, ev: qg.QKeyEvent):
        if ev.key() == qc.Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    dis = GameMainWindow()
    dis.show()
    app.exec_()