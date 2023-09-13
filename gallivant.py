from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QHBoxLayout, QWidget

class MyPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        print("JS console message:", msg)

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.setWindowIcon(QIcon('images/gallivant.png'))
        self.setWindowTitle("Gallivant - an exploratory testing tool")

        self.browser = QWebEngineView()
        self.browser.setPage(MyPage(self.browser))
        self.browser.setUrl(QUrl("https://www.google.com"))
        
        self.browser.loadFinished.connect(self.onLoadFinished)

        # Initialize QListWidget to keep track of clicked elements and sentences
        self.listWidget = QListWidget()

        # Main layout and widget
        layout = QHBoxLayout()
        layout.addWidget(self.listWidget)
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Set up QWebChannel
        self.channel = QWebChannel()
        self.channel.registerObject('myObj', self)
        self.browser.page().setWebChannel(self.channel)

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
        sentence = "This is a sample sentence."

        entry = f"Tag: {elementInfo['tag']}, ID: {elementInfo['id']}, Class: {elementInfo['class']}, Text: {elementInfo['text']}\nSentence: {sentence}"
        self.listWidget.addItem(entry)


if __name__ == "__main__":
    app = QApplication([])
    myWin = MyWindow()
    myWin.show()
    app.exec_()
