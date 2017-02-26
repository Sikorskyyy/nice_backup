from PyQt5.QtWidgets import (QFileDialog, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLineEdit
                             , QWidget)
import sys
from Backuper import Backuper
import USB.utils
import USB.StorageDevice
import getpass

class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        centralWidget = QWidget()
        mainLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()
        foldersLayout = QHBoxLayout()
        backupFolderLayout = QHBoxLayout()
        self.usbDevicesChooser = QComboBox()
        self.usbDevices = USB.utils.getStorageDevice()

        for device in self.usbDevices:
            self.usbDevicesChooser.addItem(device.__str__())

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

        mainLayout.addWidget(self.usbDevicesChooser)
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
        index = self.usbDevicesChooser.currentIndex()
        fname = QFileDialog.getExistingDirectory(self.window(), 'Open file', '{}'.format(self.usbDevices[index].getPath()))
        self.pathToFolders.setText(fname)

    def on_browseBackupFolder_clicked(self, widget):
        fname = QFileDialog.getExistingDirectory(self.window(), 'Open file', '/home/{}'.format(getpass.getuser()))
        self.pathToBackupFolder.setText(fname)

    def on_startBackup_clicked(self, widget):
        print("Starting backup")
        backuper = Backuper.Backuper()
        backuper.make_backup(self.pathToFolders.text(), self.pathToBackupFolder.text())
        print('Done')
