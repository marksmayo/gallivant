from PyQt5.QtWidgets import QApplication

from gallivant import Gallivant

if __name__ == "__main__":
    app = QApplication([])
    myWin = Gallivant()
    myWin.show()
    app.exec_()
