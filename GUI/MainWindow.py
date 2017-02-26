from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from Backuper import Backuper


class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        centralWidget = QWidget()
        mainLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()
        foldersLayout = QHBoxLayout()
        backupFolderLayout = QHBoxLayout()
        self.usbDevices = QComboBox()

        self.pathToFolders = QLineEdit()
        self.pathToFolders.setPlaceholderText("Path to folders you want to backup")
        self.pathToBackupFolder = QLineEdit()
        self.pathToBackupFolder.setPlaceholderText("Path to backup destination folder")

        self.browseFoldersButton = QPushButton("Browse...")
        self.browseFoldersButton.clicked.connect(self.on_browseFolders_clicked)
        self.browseBackupFolderButton = QPushButton("Browse...")
        self.browseBackupFolderButton.clicked.connect(self.on_browseBackupFolder_clicked)

        foldersLayout.addWidget(self.pathToFolders)
        foldersLayout.addWidget(self.browseFoldersButton)
        foldersLayout.setSpacing(5)

        backupFolderLayout.addWidget(self.pathToBackupFolder)
        backupFolderLayout.addWidget(self.browseBackupFolderButton)
        backupFolderLayout.setSpacing(5)

        self.startBackupButton = QPushButton("Start Backup")
        self.startBackupButton.clicked.connect(self.on_startBackup_clicked)

        self.exitButton = QPushButton("Exit")
        self.exitButton.clicked.connect(self.on_exit_clicked)

        buttonLayout.addWidget(self.startBackupButton)
        buttonLayout.addWidget(self.exitButton)
        buttonLayout.setSpacing(10)


        mainLayout.addLayout(backupFolderLayout)
        mainLayout.addLayout(foldersLayout)
        mainLayout.addLayout(buttonLayout)

        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle("Nice Backup")
        self.setMinimumSize(600, 200)

    def on_exit_clicked(self, widget):
        sys.exit()

    def on_browseFolders_clicked(self, widget):
        fname = QFileDialog.getExistingDirectory(self, 'Open file', '/home')
        self.pathToFolders.setText(fname)

    def on_browseBackupFolder_clicked(self, widget):
        fname = QFileDialog.getExistingDirectory(self, 'Open file', '/home')
        self.pathToBackupFolder.setText(fname)

    def on_startBackup_clicked(self, widget):
        print("Starting backup")
        backuper = Backuper.Backuper()
        backuper.make_backup(self.pathToFolders.text(), self.pathToBackupFolder.text())
        print('Done')
