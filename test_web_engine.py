import sys
import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from webengine import WebEngine

# Create an instance of QApplication. Required for PyQt5.
app = QApplication(sys.argv)


def test_java_script_console_message(mocker):
    # Mock the built-in print function
    mock_print = mocker.patch("builtins.print")

    page = WebEngine()
    page.javaScriptConsoleMessage(None, "Test message", 0, "source")

    # Assert that the print function is called with the correct arguments.
    mock_print.assert_called_once_with("JS console message:", "Test message")
