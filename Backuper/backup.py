#!/usr/bin/env python3
import datetime
import os
from distutils import dir_util

# Usage: 
#     backuper = Backuper()
#     backuper.make_backup(suorce, destination)


class Backuper(object):

    def __generate_backup_dir_name__(self, base_dest_directory):
        date = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
        return base_dest_directory + date

    def make_backup(self, source, destination):
        backup_directory = self.__generate_backup_dir_name__(destination)
        os.makedirs(backup_directory)
        dir_util.copy_tree(source, backup_directory)

if __name__ == '__main__':
    backuper = Backuper()
    backuper.make_backup("~/123", "./")
