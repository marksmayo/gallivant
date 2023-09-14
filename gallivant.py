from datetime import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QHBoxLayout, QWidget, QAction, QMenu, QMenuBar, QInputDialog, QLineEdit, QMessageBox, QTreeWidget


class MyPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        print("JS console message:", msg)


class Gallivant(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon('images/gallivant.png'))
        self.setWindowTitle("Gallivant - an exploratory testing tool")

        # Create menu bar
        self.menuBar = QMenuBar()

        # Create File menu and add it to menu bar
        self.fileMenu = QMenu('Session', self)
        self.menuBar.addMenu(self.fileMenu)

        # Initialize QTreeWidget to keep track of clicked elements and sentences
        self.treeWidget = QTreeWidget()
        self.treeWidget.setHeaderLabels(["Annotation", "Details", "Timestamp"])

        # Create Exit action and add it to File menu
        self.exitAction = QAction('Exit', self)
        self.exitAction.triggered.connect(self.exitApp)
        self.fileMenu.addAction(self.exitAction)

        self.helpMenu = QMenu('Help', self)
        self.menuBar.addMenu(self.helpMenu)

        self.aboutAction = QAction('About', self)
        self.aboutAction.triggered.connect(self.showAbout)
        self.helpMenu.addAction(self.aboutAction)

        # Set the menu bar
        self.setMenuBar(self.menuBar)

        self.browser = QWebEngineView()
        self.browser.setPage(MyPage(self.browser))
        self.browser.setUrl(QUrl("https://www.google.com"))

        self.browser.loadFinished.connect(self.onLoadFinished)

        # Main layout and widget
        layout = QHBoxLayout()
        layout.addWidget(self.treeWidget)
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Set up QWebChannel
        self.channel = QWebChannel()
        self.channel.registerObject('myObj', self)
        self.browser.page().setWebChannel(self.channel)

    def exitApp(self):
        """Exit the application."""
        self.close()

    def showAbout(self):
        dialog = QMessageBox(self)
        dialog.setText("Gallivant is a simple exploratory testing tool. Set the URL you want to start at, and browse the site as you wish.  If you come across something you want to note, Ctrl-Click the element of interest, and write an annotation. This is stored and you can continue to explore.")
        dialog.setWindowTitle("About Gallivant")
        dialog.setIcon(QMessageBox.Information)
        dialog.exec()

    @pyqtSlot(bool)
    def onLoadFinished(self, ok):
        if ok:
            with open("js/qwebchannel.js", "r") as f:
                js = f.read()

            self.browser.page().runJavaScript(js)
            self.browser.page().runJavaScript("""
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
            """)

    @pyqtSlot(str)
    def elementClicked(self, elementInfo):
        elementInfo = eval(elementInfo)
        current_url = self.browser.url().toString()
        text, okPressed = QInputDialog.getText(self, "Annotation", "Your sentence:", QLineEdit.Normal, "")
        if okPressed and text != '':
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
            child2.setText(1, elementInfo['tag'])

            child3 = QTreeWidgetItem(item)
            child3.setText(0, "ID")
            child3.setText(1, elementInfo['id'])

            child4 = QTreeWidgetItem(item)
            child4.setText(0, "Class")
            child4.setText(1, elementInfo['class'])

            child5 = QTreeWidgetItem(item)
            child5.setText(0, "Text")
            child5.setText(1, elementInfo['text'])


if __name__ == "__main__":
    app = QApplication([])
    myWin = Gallivant()
    myWin.show()
    app.exec_()
