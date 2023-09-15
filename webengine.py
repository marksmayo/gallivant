from PyQt5.QtWebEngineWidgets import QWebEnginePage


class WebEngine(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        print("JS console message:", msg)
