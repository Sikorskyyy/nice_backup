import usb.core
import usb.util
import usb.backend.libusb1 as libusb1
import os
import glob
import sys
from USB.StorageDevice import StorageDevice

SYS_USB_DEVICES = '/sys/bus/usb/devices'
SYS_BLOCK_DEVICES = '/sys/class/block'

class Utils:

    def __parse_mount_point__(self, line):
        device, mount_point, _ = line.split(None, 2)
        device = os.path.basename(device)
        return device, mount_point

    def __get_mass_storage_devices__(self, devices):
        mass_storage_devices = []
        for device in devices:
            for configuration in device:
                for interface in configuration:
                    if interface.bInterfaceClass == 0x8:
                        mass_storage_devices.append(device)
        return mass_storage_devices


    def __get_device_mount_point__(self, devices):
        device_list = []

        with open('/proc/mounts') as file:
            mount_points = dict(map(self.__parse_mount_point__, file.readlines()))

        for device in devices:
            try:
                usbId = str(device.bus) + "-" + str(device.port_numbers[0]) + "." + str(device.port_numbers[1])
            except IndexError:
                usbId = str(device.bus) + "-" + str(device.port_number)

            temp = glob.glob(os.path.join(SYS_USB_DEVICES, usbId, '*/host*/target*/*:*:*:*'))
            possible_paths = []
            for i in temp:
                possible_paths.append(os.path.basename(i))

            for device_name in os.listdir(SYS_BLOCK_DEVICES):
                device_path = os.path.join(SYS_BLOCK_DEVICES, device_name)
                device_link = os.path.join(device_path, 'device')

                if not os.path.islink(device_link):
                    continue

                scsi_id = os.path.basename(os.readlink(device_link))

                if not scsi_id in possible_paths:
                    continue

                parts = glob.glob(os.path.join(device_path, '*/partition'))

                for part_path in parts:
                    part_name = os.path.basename(os.path.dirname(part_path))
                    if mount_points.get(part_name):
                        device_list.append((device.manufacturer, device.product, mount_points.get(part_name)))
        return device_list

    def get_storage_device(self):
        devices = list(usb.core.find(find_all=True, backend=libusb1.get_backend()))
        storage_device = []
        device_list = self.__get_device_mount_point__(self.__get_mass_storage_devices__(devices))
        for device in device_list:
            storage_device.append(StorageDevice(device))
        return storage_device