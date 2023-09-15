from datetime import datetime

from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QAction,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMenuBar,
    QMessageBox,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from config_manager import load_config
from webengine import WebEngine


class Gallivant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.browser.loadFinished.connect(self.onLoadFinished)

    def setupUI(self):
        self.setWindowTitle("Gallivant")
        self.setWindowIcon(QIcon("images/gallivant.png"))

        self.menuBar = QMenuBar(self)
        fileMenu, optionsMenu, helpMenu = (
            QMenu("&Session", self),
            QMenu("&Options", self),
            QMenu("&Help", self),
        )

        self.addActions(fileMenu, [("E&xit", self.exitApp)])
        self.addActions(optionsMenu, [("&Change URL", self.showConfig)])
        self.addActions(helpMenu, [("&About", self.showAbout)])

        self.menuBar.addMenu(fileMenu)
        self.menuBar.addMenu(optionsMenu)
        self.menuBar.addMenu(helpMenu)

        self.setMenuBar(self.menuBar)

        self.treeWidget = self.initTreeWidget()
        self.browser = self.initBrowser(load_config()["url"])

        layout = QHBoxLayout()
        layout.addWidget(self.treeWidget)
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def addActions(self, menu, actions):
        for name, func in actions:
            action = QAction(name, self)
            action.triggered.connect(func)
            menu.addAction(action)

    def initTreeWidget(self):
        tree = QTreeWidget()
        tree.setHeaderLabels(["Annotation", "Details", "Timestamp"])
        return tree

    def initBrowser(self, url):
        browser = QWebEngineView()
        browser.setPage(WebEngine(browser))
        browser.setUrl(QUrl(url))
        return browser

    def exitApp(self):
        self.close()

    def showUrlDialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Enter URL")

        layout = QVBoxLayout()

        label = QLabel("Enter the URL:")
        layout.addWidget(label)

        urlInput = QLineEdit()
        layout.addWidget(urlInput)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.setLayout(layout)

        result = dialog.exec_()
        if result == QDialog.Accepted:
            entered_url = urlInput.text()
            # Do something with the entered URL, like loading it into the browser
            self.browser.setUrl(QUrl(entered_url))

    def showDialog(self, title):
        dialog = QMessageBox(self)
        dialog.setWindowTitle(title)
        dialog.setText(
            "Gallivant is a simple exploratory testing tool. Set the URL you want to start at, and browse the site as you wish.  If you come across something you want to note, Ctrl-Click the element of interest, and write an annotation. This is stored and you can continue to explore.",
        )
        dialog.setIcon(QMessageBox.Information)
        dialog.exec()

    def showAbout(self):
        self.showDialog("About Gallivant")

    def showConfig(self):
        self.showUrlDialog()

    @pyqtSlot(bool)
    def onLoadFinished(self, ok):
        if ok:
            with open("js/qwebchannel.js", "r") as f:
                js = f.read()

            self.browser.page().runJavaScript(js)
            self.browser.page().runJavaScript(
                """
                var channel = new QWebChannel(qt.webChannelTransport, function(channel) {
                    window.myObj = channel.objects.myObj;

                    document.addEventListener('click', function(event) {
                        if (event.ctrlKey) {
                            var element = event.target;
                            var elementInfo = {
                                'tag': element.tagName,
                                'id': element.id,
                                'class': element.className,
                                'text': element.innerText.substring(0, 30)
                            };
                            window.myObj.elementClicked(JSON.stringify(elementInfo));
                        }
                    });
                });
            """,
            )

    @pyqtSlot(str)
    def elementClicked(self, elementInfo):
        elementInfo = eval(elementInfo)
        current_url = self.browser.url().toString()
        text, okPressed = QInputDialog.getText(
            self,
            "Annotation",
            "Your annotation:",
            QLineEdit.Normal,
            "",
        )
        if okPressed and text != "":
            entry = f"{text}"
            timestamp = datetime.now().strftime("%H:%M:%S")  # Get current time

            item = QTreeWidgetItem(self.treeWidget)
            item.setText(0, entry)
            item.setText(2, timestamp)  # Add timestamp to the new colum

            child1 = QTreeWidgetItem(item)
            child1.setText(0, "URL")
            child1.setText(1, current_url)

            child2 = QTreeWidgetItem(item)
            child2.setText(0, "XPath")
            child2.setText(1, elementInfo["tag"])

            child3 = QTreeWidgetItem(item)
            child3.setText(0, "ID")
            child3.setText(1, elementInfo["id"])

            child4 = QTreeWidgetItem(item)
            child4.setText(0, "Class")
            child4.setText(1, elementInfo["class"])

            child5 = QTreeWidgetItem(item)
            child5.setText(0, "Text")
            child5.setText(1, elementInfo["text"])
