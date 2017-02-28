from PyQt5.QtWidgets import (QFileDialog, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QComboBox, QLineEdit, QWidget, QTreeView, QAbstractItemView, QListView, QFileSystemModel,
                             QProgressDialog, QApplication, QProgressBar, QMessageBox)
import sys
import getpass
from Backuper import Backuper
from USB.utils import Utils 
import USB.StorageDevice
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        centralWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()
        foldersLayout = QHBoxLayout()
        backupFolderLayout = QHBoxLayout()
        self.usbDevicesChooser = QComboBox()
        
        usb_util = Utils()
        self.usbDevices = usb_util.get_storage_device()

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

        self.mainLayout.addWidget(self.usbDevicesChooser)
        self.mainLayout.addLayout(backupFolderLayout)
        self.mainLayout.addLayout(foldersLayout)
        self.mainLayout.addLayout(buttonLayout)

        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle("Nice Backup")
        self.setMinimumSize(600, 200)

    def on_exit_clicked(self, widget):
        sys.exit()

    def on_browseFolders_clicked(self, widget):
        index = self.usbDevicesChooser.currentIndex()
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        file_view = file_dialog.findChild(QListView, 'listView')

        if file_view:
            file_view.setSelectionMode(QAbstractItemView.MultiSelection)

        ftree_view = file_dialog.findChild(QTreeView)

        if ftree_view:
            ftree_view.setSelectionMode(QAbstractItemView.MultiSelection)

        file_dialog.setDirectory(self.usbDevices[index].getPath())

        if file_dialog.exec():
            paths = file_dialog.selectedFiles()

        self.pathToFolders.setText(";".join(paths))

    def on_browseBackupFolder_clicked(self, widget):
        fname = QFileDialog.getExistingDirectory(self.window(), 'Open file', '/home/{}'.format(getpass.getuser()))
        self.pathToBackupFolder.setText(fname)

    def on_startBackup_clicked(self, widget):
        print("Starting backup")
        backuper = Backuper.Backuper()
        sources = self.pathToFolders.text().split(";")
        destination = self.pathToBackupFolder.text()

        progress = QProgressBar()
        progress.setMinimum(0)
        progress.setMaximum(len(sources))
        self.mainLayout.addWidget(progress)

        for source in sources:
            backuper.make_backup(source, destination)
            progress.setValue(sources.index(source))
            QApplication.processEvents()
        doneDialog = QMessageBox()

        doneDialog.setIcon(QMessageBox.Information)
        doneDialog.setText("Copying data is completed")
        doneDialog.setWindowTitle("Copy event")
        doneDialog.setStandardButtons(QMessageBox.Ok)

        index = self.mainLayout.indexOf(progress)
        self.mainLayout.itemAt(index).widget().setParent(None)

        doneDialog.exec()