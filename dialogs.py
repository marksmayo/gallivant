from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QInputDialog,
)


def showDialog(parent, title):
    dialog = QMessageBox(parent)
    dialog.setWindowTitle(title)
    dialog.setText(
        "Gallivant is a simple exploratory testing tool. Set the URL you want to start at, and browse the site as you wish."
    )
    dialog.setIcon(QMessageBox.Information)
    dialog.exec_()


def showConfig(parent, browser):
    dialog = QDialog(parent)
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
        browser.setUrl(QUrl(entered_url))
