"""
 Copyright 2016 EMC GSE SW Automation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""


class BackupServiceLevelResult(object):
    def __init__(self, name, result):
        self.name = name
        self.result = result


class AddedBackupServiceLevelCollection(object):
    def __init__(self, backup_to_operate_vm='', backup_to_set_backup_service=''):
        self.backup_to_operate_vm = backup_to_operate_vm if backup_to_operate_vm else ''
        self.backup_to_set_backup_service = backup_to_set_backup_service if backup_to_operate_vm else ''


class BackupServiceLevelSharedObj(object):
    def __init__(self, for_deletion=None, for_deploy_vm=None, for_set_backup_service_level=None):
        self.for_deletion = for_deletion
        self.for_deploy_vm = for_deploy_vm
        self.for_set_backup_service_level = for_set_backup_service_level
