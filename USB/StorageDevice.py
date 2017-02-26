import os

class StorageDevice:
    def __init__(self, manufacturer, product, path):
        self.manufacturer = manufacturer
        self.product = product
        self.path = path

    def freeSpace(self):
        stat = os.statvfs(self.path)
