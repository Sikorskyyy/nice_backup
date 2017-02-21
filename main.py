from GUI.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
