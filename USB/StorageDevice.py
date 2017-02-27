import os
from enum import Enum

class DeviceInfo(Enum):
    Manufacturer = 0
    Product = 1
    Path = 2

class StorageDevice:
    def __init__(self, device):
        self.manufacturerName = device[0]
        self.productName = device[1]
        self.path = device[2]

    def freeSpace(self):
        stat = os.statvfs(self.path)
        return (stat.f_frsize * stat.f_bavail) / 2**30

    def totalSpace(self):
        stat = os.statvfs(self.path)
        return (stat.f_frsize * stat.f_blocks) / 2**30

    def __str__(self):
       return '{} {} ({:3.2} Gb)'.format(self.manufacturerName, self.productName, self.freeSpace())

    def getPath(self):
        return self.path