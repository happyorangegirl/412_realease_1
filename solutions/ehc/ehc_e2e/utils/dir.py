#  Copyright 2016 EMC GSE SW Automation
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


def get_e2e_root_dir():
    _curr_dir = os.path.dirname(os.path.realpath(__file__))
    e2e_root = os.path.abspath(os.path.join(_curr_dir, os.pardir))
    return e2e_root


def get_e2e_config_dir():
    root_dir = get_e2e_root_dir()
    return os.path.abspath(os.path.join(root_dir, 'conf'))


def get_e2e_workflow_conf_path(file_name):
    """
    >>> get_e2e_workflow_conf_path('generic.yaml')
    'C:\\Users\\fanm1\\emc\\solutions\\ehc\\ehc_e2e\\conf\\generic.yaml'
    """
    config_dir = get_e2e_config_dir()
    file_pathname = os.path.join(config_dir, file_name)
    assert os.path.exists(file_pathname)
    return file_pathname


def get_e2e_file_pathname(file_name):
    root_dir = get_e2e_root_dir()
    file_pathname = os.path.join(root_dir, file_name)
    assert os.path.exists(file_pathname)
    return file_pathname
