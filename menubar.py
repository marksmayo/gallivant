from PyQt5.QtWidgets import QAction, QMenu, QMenuBar


class MenuBarManager:
    def __init__(self, parent, exitApp, showConfig, showAbout):
        self.parent = parent
        self.exitApp = exitApp
        self.showConfig = showConfig
        self.showAbout = showAbout

    def createMenuBar(self):
        menuBar = QMenuBar(self.parent)
        fileMenu, optionsMenu, helpMenu = (
            QMenu("&Session", self.parent),
            QMenu("&Options", self.parent),
            QMenu("&Help", self.parent),
        )

        self.addActions(fileMenu, [("E&xit", self.exitApp)])
        self.addActions(optionsMenu, [("&Change URL", self.showConfig)])
        self.addActions(helpMenu, [("&About", self.showAbout)])

        menuBar.addMenu(fileMenu)
        menuBar.addMenu(optionsMenu)
        menuBar.addMenu(helpMenu)

        return menuBar

    def addActions(self, menu, actions):
        for name, func in actions:
            action = QAction(name, self.parent)
            action.triggered.connect(func)
            menu.addAction(action)
