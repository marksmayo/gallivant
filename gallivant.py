from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QWidget

from config_manager import load_config
from dialogs import showConfig, showDialog
from menubar import MenuBarManager
from widgets import Browser, TreeWidget


class Gallivant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Gallivant")
        self.setWindowIcon(QIcon("images/gallivant.png"))

        self.menuBarManager = MenuBarManager(
            self, self.exitApp, self.showConfig, self.showAbout,
        )
        self.setMenuBar(self.menuBarManager.createMenuBar())

        self.treeWidget = TreeWidget()
        self.browser = Browser(load_config()["url"], self.treeWidget)

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
