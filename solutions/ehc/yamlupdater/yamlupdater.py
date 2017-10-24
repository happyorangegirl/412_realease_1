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


import argparse
import os
import sys
import time

from time import gmtime, strftime

from runner import runner
from util import  Logger, check_path_exist_create


LOG_FILE_NAME = 'log_yamlupdater.log'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='yamlupdater',
        add_help=True,
        description='Update yaml files by processing anchor values between '
                    'yaml files',
        epilog="""Example:
                    YamlUpdater.py -o '/usr/lib/python2.7/site-packages/config' -r '/root/automation/ehc/config' -b
                    'backup' -u '/root/automation/ehc/config'"""
    )
    parser.add_argument('-o', type=str,
                        help='the path for original yaml files.')
    parser.add_argument('-r', type=str,
                        help='the path for referenced yaml files whose anchor '
                             'values will be referenced and used for updating.')
    parser.add_argument('-b', type=str,
                        help='the path for backup referenced files, here are '
                             'files in SIT VMs.')
    parser.add_argument('-u', type=str,
                        help='the path for placing the updated files.')

    args = parser.parse_args()
    if not args.o or not args.r or not args.b or not args.u:
        print parser.print_help()
        parser.exit()
        sys.exit(1)

    sys.stdout = Logger(LOG_FILE_NAME)
    print '[INFO][{}]Started yaml file update operations.'.format(
        strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    start_time = time.time()

    print 'argument -o:"{}"'.format(args.o)
    print 'argument -r:"{}"'.format(args.r)
    print 'argument -b:"{}"'.format(args.b)
    print 'argument -u:"{}"'.format(args.u)

    root_path_target_yaml = args.o  # r'C:\Gitrepo\challenger\solutions\ehc\ehc_e2e\conf'
    root_path_reference_yaml = args.r  # r'C:\GSE_team\EHC_E2E_Automation\src\yamlupdate\config_sit'
    backup_folder_name = args.b
    root_path_updated_yaml = args.u

    check_path_exist_create(root_path_updated_yaml)

    runner(
        root_path_target_yaml, root_path_reference_yaml,
        root_path_updated_yaml, backup_folder_name)
    print '[INFO][{}]Finished yaml file update operations.'.format(
        strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    print '[INFO]It takes {} seconds for the whole process.'.format(
        time.time() - start_time)
    print '[INFO]Original yaml files are backed up under:{}'.format(
        os.path.join(root_path_reference_yaml, backup_folder_name)
    )
    print '[INFO]Updated yaml files are placed under:{}'.format(
        root_path_updated_yaml)
