#  Copyright 2016 EMC HCE SW Automation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


import errno
import sys
import os
from shutil import copyfile


class Logger(object):
    def __init__(self, log_name):
        self.terminal = sys.stdout
        self.log = open(log_name, 'w')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)


def r_replace(original_str, search_str, replace_str):
    """
    return a new string instance whose right first occurent of the given search
    string is found and replaced by the replace_str, return original string if
     given search string is not found.
    :param original_str: the string that replace will occur on.
    :param search_str: the string to search in the original_string.
    :param replace_str: the string to be used for replacement.
    :return: the replaced string
    """
    if original_str:
        if original_str.rfind(search_str) == -1:
            # we don't find any string matching givin search string.
            return original_str
        else:
            index_of_search_str = original_str.rfind(search_str)

            # The original string is separated by the given search string
            # and the search string is replaced by replace_str
            # [sub_string_before_search_string, replace_str, rest_part ]
            str_pieces = [original_str[:index_of_search_str], replace_str,
                          original_str[index_of_search_str + len(search_str):]]
            return ''.join(str_pieces)
    else:
        return None


def check_path_exist_create(path_str):
    if not os.path.exists(path_str):
        try:
            os.makedirs(path_str)
        except OSError as ex:  # Guard in case race condition
            if ex.errno != errno.EEXIST:
                raise


def file_backup(file_path, backup_folder_path):
    file_name = os.path.split(os.path.abspath(file_path))[1]
    bk_file = os.path.join(backup_folder_path, file_name)
    print '[INFO]Try to backup file:{} to: {}.'.format(file_path, bk_file)

    check_path_exist_create(backup_folder_path)

    copyfile(file_path, bk_file)
    print '[INFO]Backup file:{} to: {} succeeded.'.format(file_path, bk_file)
