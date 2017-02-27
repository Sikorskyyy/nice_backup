from PyQt5.QtWidgets import (QFileDialog, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QComboBox, QLineEdit, QWidget, QTreeView, QAbstractItemView, QListView, QFileSystemModel)
import sys
import getpass
from Backuper import Backuper
from USB.utils import Utils 
import USB.StorageDevice


class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        centralWidget = QWidget()
        mainLayout = QVBoxLayout()
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
        backuper.make_backup(sources, destination)
        print('Done')
