import usb.core
import usb.util
import usb.backend.libusb1 as libusb1
import os
import glob
from USB.StorageDevice import StorageDevice
import sys

SYS_USB_DEVICES = '/sys/bus/usb/devices'
SYS_BLOCK_DEVICES = '/sys/class/block'

def parse_mountPoint(line):
    device, mountPoint, _ = line.split(None, 2)
    device = os.path.basename(device)
    return device, mountPoint


def getMassStorageDevices(devices):
    massStorageDevices = []
    for device in devices:
        for configuration in device:
            for interface in configuration:
                if interface.bInterfaceClass == 0x8:
                    massStorageDevices.append(device)
    return massStorageDevices


def getDeviceMountPoint(devices):
    deviceList = []

    with open('/proc/mounts') as file:
        mountPoints = dict(map(parse_mountPoint, file.readlines()))

    for device in devices:
        try:
            usbId = str(device.bus) + "-" + str(device.port_numbers[0]) + "." + str(device.port_numbers[1])
        except IndexError:
            usbId = str(device.bus) + "-" + str(device.port_number)

        temp = glob.glob(os.path.join(SYS_USB_DEVICES, usbId, '*/host*/target*/*:*:*:*'))
        possiblePaths = []
        for i in temp:
            possiblePaths.append(os.path.basename(i))

        for deviceName in os.listdir(SYS_BLOCK_DEVICES):
            devicePath = os.path.join(SYS_BLOCK_DEVICES, deviceName)
            deviceLink = os.path.join(devicePath, 'device')

            if not os.path.islink(deviceLink):
                continue

            scsiId = os.path.basename(os.readlink(deviceLink))

            if not scsiId in possiblePaths:
                continue

            parts = glob.glob(os.path.join(devicePath, '*/partition'))

            for partPath in parts:
                partName = os.path.basename(os.path.dirname(partPath))
                if mountPoints.get(partName):
                    deviceList.append((device.manufacturer, device.product, mountPoints.get(partName)))
    return deviceList

def getStorageDevice():
    devices = list(usb.core.find(find_all=True, backend=libusb1.get_backend()))
    storageDevice = []
    deviceList = getDeviceMountPoint(getMassStorageDevices(devices))
    for device in deviceList:
        storageDevice.append(StorageDevice(device))
    return storageDevice