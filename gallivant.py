from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from menubar import MenuBarManager
from widgets import TreeWidget, Browser
from dialogs import showDialog, showConfig
from config_manager import load_config


class Gallivant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Gallivant")
        self.setWindowIcon(QIcon("images/gallivant.png"))

        self.menuBarManager = MenuBarManager(
            self, self.exitApp, self.showConfig, self.showAbout
        )
        self.setMenuBar(self.menuBarManager.createMenuBar())

        self.treeWidget = TreeWidget()
        self.browser = Browser(load_config()["url"])

        layout = QHBoxLayout()
        layout.addWidget(self.treeWidget)
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def exitApp(self):
        self.close()

    def showAbout(self):
        showDialog(self, "About Gallivant")

    def showConfig(self):
        showConfig(self, self.browser)
