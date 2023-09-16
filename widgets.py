from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from webengine import WebEngine
from config_manager import load_config


class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderLabels(["Annotation", "Details", "Timestamp"])


class Browser(QWebEngineView):
    def __init__(self, url):
        super().__init__()
        self.setPage(WebEngine(self))
        self.setUrl(QUrl(url))
