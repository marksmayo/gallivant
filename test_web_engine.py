import sys
import pytest
from PyQt5.QtWidgets import QApplication
from webengine import WebEngine

def test_java_script_console_message(mocker):
    app = QApplication(sys.argv)
    mock_print = mocker.patch("builtins.print")

    page = WebEngine()
    page.javaScriptConsoleMessage(None, "Test message", 0, "source")

    mock_print.assert_called_once_with("JS console message:", "Test message")
