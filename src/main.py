from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtGui import QIcon
import os
import sys
import threading
import keyboard  # Install with `pip install keyboard`



class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon('icon.ico'))  # Use the icon_path instead of "icon.png"


        # Initialize attributes first
        self.wins = 0
        self.losses = 0
        self.wlRatio = 0
        self.kd = 0
        self.kills = 0
        self.deaths = 0

        # Then initialize the UI
        self.initUI()
        self.setupSystemTray()

    def setupSystemTray(self):
        # Create a system tray icon
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon('icon.ico'))  # Again use the icon_path


        # Create a context menu for the tray icon
        trayMenu = QMenu(self)
        showAction = QAction("Show", self)
        showAction.triggered.connect(self.show)
        trayMenu.addAction(showAction)

        hideAction = QAction("Hide", self)
        hideAction.triggered.connect(self.hide)
        trayMenu.addAction(hideAction)

        quitAction = QAction("Quit", self)
        quitAction.triggered.connect(QApplication.instance().quit)
        trayMenu.addAction(quitAction)

        self.trayIcon.setContextMenu(trayMenu)
        self.trayIcon.show()

    def initUI(self):
        self.setWindowTitle("Win/Loss Tracker")
        self.setGeometry(100, 100, 400, 200)

        # change the color
        self.setStyleSheet("background-color: black;")

        mainLayout = QVBoxLayout()

        # add a win button and label
        winLayout = QHBoxLayout()
        self.winLabel = QLabel(f"Wins: {self.wins}", self)
        self.winLabel.setObjectName("winLabel")
        winLayout.addWidget(self.winLabel)

        self.winButton = QPushButton("+", self)
        self.winButton.setFixedSize(100, 40)
        self.winButton.setObjectName("winButton")
        self.winButton.setCursor(Qt.PointingHandCursor)
        self.winButton.setStyleSheet("font-size: 32px; color: white; background-color: darkblue;")
        self.winButton.clicked.connect(self.addWin)
        winLayout.addWidget(self.winButton)

        self.lessWinButton = QPushButton("-", self)
        self.lessWinButton.setFixedSize(100, 40)
        self.lessWinButton.setCursor(Qt.PointingHandCursor)
        self.lessWinButton.setStyleSheet("font-size: 32px; color: white; background-color: firebrick;")
        self.lessWinButton.clicked.connect(self.reduceWin)
        winLayout.addWidget(self.lessWinButton)

        mainLayout.addLayout(winLayout)

        # add a loss button and label
        lossLayout = QHBoxLayout()
        self.lossLabel = QLabel(f"Losses: {self.losses}", self)
        self.lossLabel.setObjectName("lossLabel")
        lossLayout.addWidget(self.lossLabel)

        self.lossButton = QPushButton("+", self)
        self.lossButton.setFixedSize(100, 40)
        self.lossButton.setCursor(Qt.PointingHandCursor)
        self.lossButton.setStyleSheet("font-size: 32px; color: white; background-color: darkblue;")
        self.lossButton.clicked.connect(self.addLoss)
        lossLayout.addWidget(self.lossButton)

        self.lessLossButton = QPushButton("-", self)
        self.lessLossButton.setFixedSize(100, 40)
        self.lessLossButton.setCursor(Qt.PointingHandCursor)
        self.lessLossButton.setStyleSheet("font-size: 32px; color: white; background-color: firebrick;")
        self.lessLossButton.clicked.connect(self.reduceLoss)
        lossLayout.addWidget(self.lessLossButton)

        mainLayout.addLayout(lossLayout)

        # add a kills button and label
        killsLayout = QHBoxLayout()
        self.killsLabel = QLabel(f"Kills: {self.kills}", self)
        self.killsLabel.setObjectName("killsLabel")
        killsLayout.addWidget(self.killsLabel)

        self.killsButton = QPushButton("+", self)
        self.killsButton.setFixedSize(100, 40)
        self.killsButton.setCursor(Qt.PointingHandCursor)
        self.killsButton.setStyleSheet("font-size: 32px; color: white; background-color: darkblue;")
        self.killsButton.clicked.connect(self.addKill)
        killsLayout.addWidget(self.killsButton)

        self.lessKillsButton = QPushButton("-", self)
        self.lessKillsButton.setFixedSize(100, 40)
        self.lessKillsButton.setCursor(Qt.PointingHandCursor)
        self.lessKillsButton.setStyleSheet("font-size: 32px; color: white; background-color: firebrick;")
        self.lessKillsButton.clicked.connect(self.reduceKill)
        killsLayout.addWidget(self.lessKillsButton)

        mainLayout.addLayout(killsLayout)

        # add a deaths button and label
        deathsLayout = QHBoxLayout()
        self.deathsLabel = QLabel(f"Deaths: {self.deaths}", self)
        self.deathsLabel.setObjectName("deathsLabel")
        deathsLayout.addWidget(self.deathsLabel)

        self.deathsButton = QPushButton("+", self)
        self.deathsButton.setFixedSize(100, 40)
        self.deathsButton.setCursor(Qt.PointingHandCursor)
        self.deathsButton.setStyleSheet("font-size: 32px; color: white; background-color: darkblue;")
        self.deathsButton.clicked.connect(self.addDeath)
        deathsLayout.addWidget(self.deathsButton)

        self.lessDeathsButton = QPushButton("-", self)
        self.lessDeathsButton.setFixedSize(100, 40)
        self.lessDeathsButton.setCursor(Qt.PointingHandCursor)
        self.lessDeathsButton.setStyleSheet("font-size: 32px; color: white; background-color: firebrick;")
        self.lessDeathsButton.clicked.connect(self.reduceDeath)
        deathsLayout.addWidget(self.lessDeathsButton)

        mainLayout.addLayout(deathsLayout)

        # add wlRatios section
        avgLayout = QHBoxLayout()
        self.avgLabel = QLabel(f"Win/Loss Ratio: {self.wlRatio:.2f}%", self)
        self.avgLabel.setObjectName("avgLabel")
        avgLayout.addWidget(self.avgLabel)

        self.kdLabel = QLabel(f"K/D: {self.kd}", self)
        self.kdLabel.setObjectName("kdLabel")
        avgLayout.addWidget(self.kdLabel)

        mainLayout.addLayout(avgLayout)

        self.setLayout(mainLayout)
    

    def addWin(self):
        self.wins += 1
        self.updateStats()

    def reduceWin(self):
        if self.wins >= 1:
            self.wins -= 1
        
        self.updateStats()

    def addLoss(self):
        self.losses += 1
        self.updateStats()

    def reduceLoss(self):
        if self.losses >= 1:
            self.losses -= 1
        
        self.updateStats()

    def addKill(self):
        self.kills += 1
        self.updateStats()

    def reduceKill(self):
        if self.kills >= 1:
            self.kills -= 1
        
        self.updateStats()

    def addDeath(self):
        self.deaths += 1
        self.updateStats()

    def reduceDeath(self):
        if self.deaths >= 1:
            self.deaths -= 1
        
        self.updateStats()

    def updateStats(self):
        self.winLabel.setText(f"Wins: {self.wins}")
        self.lossLabel.setText(f"Losses: {self.losses}")

        # Calculate the win/loss ratio
        if self.losses <= 0 and self.wins >= 1:
            self.wlRatio = 100
        elif self.wins == 0 and self.losses == 0:
            self.wlRatio = 0
        else:
            self.wlRatio = (self.wins / (self.wins + self.losses)) * 100

        self.killsLabel.setText(f"Kills: {self.kills}")
        self.deathsLabel.setText(f"Deaths: {self.deaths}")

        # Calculate the kill/death ratio
        if self.kills <= 0 or self.deaths <= 0:
            self.kd = 0
        else:
            self.kd = self.kills / self.deaths

        self.avgLabel.setText(f"Win/Loss Ratio: {self.wlRatio:.2f}%")
        self.kdLabel.setText(f"K/D: {self.kd:.1f}")

    def runHotkey(app):
        # Register a global hotkey to toggle the app visibility
        def toggleVisibility():
            if app.isVisible():
                app.hide()
            else:
                app.show()

        keyboard.add_hotkey("ctrl+shift+h", toggleVisibility)
        try:
            keyboard.wait()  # This will block until the program exits
        except:
            pass  # Allow thread to exit silently if interrupted

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                QTimer.singleShot(0, self.hide)
        super().changeEvent(event)



    def closeEvent(self, event):
        keyboard.unhook_all_hotkeys()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("C:/Users/Jacob/Documents/overlay/simple-python-app/src/style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = App()

    hotkeyThread = threading.Thread(target=App.runHotkey, args=(window,), daemon=True)
    hotkeyThread.start()

    window.show()
    sys.exit(app.exec_())