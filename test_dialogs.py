# test_dialogs.py
from unittest.mock import MagicMock
import pytest
from PyQt5.QtWidgets import QApplication
from dialogs import showDialog, showConfig


# A fixture for QApplication instance
@pytest.fixture(scope="module")
def app():
    return QApplication([])


# Test for showDialog function
# Assuming showDialog configures and shows a dialog but does not return it
def test_show_dialog_creation(app, qtbot):
    parent = None
    title = "Test Title"
    dialog = QMessageBox(parent)  # Create the dialog here
    showDialog(dialog, title)  # Configure it using the function

    assert dialog.windowTitle() == title


# Test for showConfig function
def test_show_config_creation(app):
    parent = MagicMock()
    browser = MagicMock()  # Mock the browser argument
    dialog = showConfig(parent, browser)

    assert dialog is not None
