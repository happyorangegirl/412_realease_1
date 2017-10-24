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

import os

from os.path import isfile, join
import filecmp
from shutil import copyfile

from util import file_backup
from yamloperator import update_single_yaml


def runner(root_path_target_yaml, root_path_reference_yaml,
           root_path_updated_yaml, backup_folder_name):

    backup_folder_path = join(
        root_path_reference_yaml, backup_folder_name)

    # if the backup folder exists, clear it first.
    if os.path.exists(backup_folder_path) and os.listdir(backup_folder_path):
        for f in os.listdir(backup_folder_path):
            os.remove(join(backup_folder_path, f))

    target_yaml_files = {}
    reference_yaml_files = {}

    for f_name in [i for i in os.listdir(root_path_target_yaml) if
                   isfile(join(root_path_target_yaml, i))]:
        target_yaml_files.update(
            {f_name: join(root_path_target_yaml, f_name)})

    print '[INFO]Start to backup all files specified as reference files ' \
          'to folder:{}'.format(backup_folder_path)
    for f_name in [i for i in os.listdir(root_path_reference_yaml) if
                   isfile(join(root_path_reference_yaml, i))]:
        reference_yaml_files.update(
            {f_name: join(root_path_reference_yaml, f_name)})

        # We will backup all reference files.
        file_backup(
            join(root_path_reference_yaml, f_name), backup_folder_path)
    print '[INFO]Finished backup for all reference files!'

    for target_yaml_name, target_yaml_name_path in target_yaml_files.iteritems():
        reference_yaml_path = reference_yaml_files.get(target_yaml_name)
        updated_yaml_file_path = join(root_path_updated_yaml, target_yaml_name)

        if reference_yaml_path:
            reference_yaml_name = os.path.split(os.path.abspath(reference_yaml_path))[1]

            if filecmp.cmp(target_yaml_name_path, reference_yaml_path):
                print '[INFO]No change found for file: {}, no need to update.' \
                      ''.format(reference_yaml_name)
            else:
                print '[INFO]Start to update yaml file {}.'.format(
                    reference_yaml_path)
                update_single_yaml(target_yaml_name_path, reference_yaml_path,
                                   updated_yaml_file_path)
        else:
            copyfile(target_yaml_name_path, updated_yaml_file_path)
            print(
                '[WARN]The reference file for :{} not found, we just copy it '
                'from {} to {}'.format(
                    target_yaml_name, root_path_target_yaml,
                    updated_yaml_file_path)
            )

    if root_path_reference_yaml != root_path_updated_yaml:
        print(
            '[INFO]The root_path to reference_yaml is different from '
            'UPDATED_YAML_RESULT_PATH, will copy updated files to '
            'UPDATED_YAML_RESULT_PATH:{}'.format(root_path_updated_yaml))
        for updated_ref_yaml, ref_yaml_path in reference_yaml_files.iteritems():
            updated_yaml_file_path = join(
                root_path_updated_yaml, updated_ref_yaml)
            copyfile(ref_yaml_path, updated_yaml_file_path)
    else:
        print(
            '[INFO]Done updating yaml files, root_path_reference_yaml is '
            'identical with UPDATED_YAML_RESULT_PATH:{}'.format(
                root_path_updated_yaml))
