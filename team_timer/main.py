from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from collections import namedtuple
import logging
import datetime
import sys


ROUND_LENGTH = 3
TICK = 100


class Team:
    def __init__(self, name, team_color, text_color='black'):
        self.name = name
        self.text_color = text_color
        self.background = team_color

teams = [Team('foo\nbarr', 'blue'),
         Team('bar', 'black', 'lightgray')]


class TeamLabel(QLabel):
    def __init__(self, team):
        super().__init__()
        self.setStyleSheet('QLabel {{color: {0}; background-color: {1}; font-size: 150px; font-style: bold; font-family: DejaVu Sans mono}}'.format(team.text_color, team.background))
        self.setAlignment(Qt.AlignCenter)
        self.setText(team.name)


class TeamBlock(QHBoxLayout):
    def __init__(self):
        super().__init__()
        for team in teams:
            self.addWidget(TeamLabel(team))


class StatusBar(QHBoxLayout):
    def __init__(self, stretch=1, button_bind=None):
        super().__init__()

        self.stretch(stretch)
        self.countdown = QProgressBar()
        self.countdown.setMaximum(ROUND_LENGTH*1000)
        self.addWidget(self.countdown)

        self.time = QLabel()
        label_font = QFont()
        label_font.setPixelSize(50)
        self.start_button = QPushButton()
        self.start_button.setText('Toggle countdown')
        if button_bind is not None:
            self.start_button.clicked.connect(button_bind)
        self.addWidget(self.start_button)

    def tick(self):
        next_val = self.countdown.value() + TICK
        next_val %= 1000 * ROUND_LENGTH
        self.countdown.setValue(next_val)
        return next_val == (1000*ROUND_LENGTH - 1)


class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.ticker = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.setInterval(TICK)

        self.init_ui()

    def init_ui(self):
        self.resize(1280, 720)
        self.setWindowTitle('Hello, LTT!')
        team_bar = TeamBlock()
        team_bar.stretch(3)

        # Bottom status bar
        self.status_bar = StatusBar(stretch=1, button_bind=self.toggle_timer)

        vbox = QVBoxLayout()
        vbox.addItem(team_bar)
        vbox.addItem(self.status_bar)
        self.setLayout(vbox)

    def toggle_timer(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start()

    def tick(self):

        should_swap = self.status_bar.tick()
        if should_swap:
            self.swap_teams()
        logging.debug('Current amount: %s / %s', self.status_bar.countdown.value(), self.status_bar.countdown.maximum())
        logging.debug(should_swap)

        app.processEvents()
        self.timer.start()

    def swap_teams(self):
        # TODO: implement
        pass

if __name__ == '__main__':
    app = QApplication([])

    win = Main()
    win.showFullScreen()

    sys.exit(app.exec_())
