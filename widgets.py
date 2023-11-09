import json
from datetime import datetime

from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
)
from PyQt5.QtGui import QIcon

from webengine import WebEngine


class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderLabels(["Annotation", "Details", "Timestamp", "Screenshot"])


class Browser(QWebEngineView):
    def __init__(self, url, treeWidget):
        super().__init__()
        self.treeWidget = treeWidget
        self.annotation = ""
        # Initialize WebEngine
        self.setPage(WebEngine(self))

        # Load URL
        self.setUrl(QUrl(url))

        # Connect signals
        self.loadFinished.connect(self.onLoadFinished)

        self.screenshotLabel = None

        # Initialize WebChannel
        self.channel = QWebChannel()
        self.channel.registerObject("myObj", self)
        self.page().setWebChannel(self.channel)

    @pyqtSlot(bool)
    def onLoadFinished(self, ok):
        if ok:
            with open("js/qwebchannel.js", "r") as f:
                js = f.read()
            print(js)
            self.page().runJavaScript(js)
            self.page().runJavaScript(
                """
                var channel = new QWebChannel(qt.webChannelTransport, function(channel) {
                    window.myObj = channel.objects.myObj;

                    document.addEventListener('click', function(event) {
                        if (event.ctrlKey) {
                            var element = event.target;
                            element.style.border = "2px solid #FF0000";  // Red border
                            var elementInfo = {
                                'tag': element.tagName,
                                'id': element.id,
                                'class': element.className,
                                'text': element.innerText.substring(0, 30),
                            };
                            window.myObj.elementClicked(JSON.stringify(elementInfo));
                            // Remove the highlight after 2 seconds
                            setTimeout(function() {
                                element.style.backgroundColor = "";  // Remove background color
                                element.style.border = "";  // Remove border
                            }, 5000);  // 20 seconds
                        }
                    });
                });
                """,
            )

    @pyqtSlot(str)
    def elementClicked(self, json_string):
        print("elementClicked called with:", json_string)

        dialog = QDialog(self)
        dialog.setWindowTitle("Add Annotation")

        layout = QVBoxLayout()

        info_label = QLabel("Add your annotation below:")
        layout.addWidget(info_label)

        annotation_field = QLineEdit()
        layout.addWidget(annotation_field)

        submit_button = QPushButton("Submit")
        layout.addWidget(submit_button)

        def close_dialog():
            # Here, you can get the annotation and do something with it
            self.annotation = annotation_field.text()
            print(f"Annotation: {self.annotation}")
            dialog.close()

        submit_button.clicked.connect(close_dialog)

        dialog.setLayout(layout)
        dialog.exec_()
        print(f"Annotation{self.annotation}")
        if self.annotation != "":
            entry = f"{self.annotation}"
            timestamp = datetime.now().strftime("%H:%M:%S")  # Get current time
            pixmap = self.grab()
            icon = QIcon(pixmap)

            json_string = json.loads(json_string)
            item = QTreeWidgetItem(self.treeWidget)
            item.setText(0, entry)
            item.setText(2, timestamp)  # Add timestamp to the new colum
            item.setIcon(3, icon)

            self.treeWidget.itemClicked.connect(self.showFullSizeScreenshot)

            child1 = QTreeWidgetItem(item)
            child1.setText(0, "URL")
            child1.setText(1, self.url().toString())

            child2 = QTreeWidgetItem(item)
            child2.setText(0, "XPath")
            child2.setText(1, json_string.get("tag"))

            child3 = QTreeWidgetItem(item)
            child3.setText(0, "ID")
            child3.setText(1, json_string["id"])

            child4 = QTreeWidgetItem(item)
            child4.setText(0, "Class")
            child4.setText(1, json_string["class"])

            child5 = QTreeWidgetItem(item)
            child5.setText(0, "Text")
            child5.setText(1, json_string["text"])

            child6 = QTreeWidgetItem(item)
            child6.setText(0, "Screenshot")
            child6.setIcon(1, icon)

    def showFullSizeScreenshot(self, item, column):
        if item.text(0) == "Screenshot" and column == 1:
            self.screenshotLabel = QLabel()
            pixmap = self.grab()  # Capture current screenshot
            self.screenshotLabel.setPixmap(pixmap)
            self.screenshotLabel.show()
