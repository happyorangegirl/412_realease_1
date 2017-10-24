"""
 Copyright 2017 EMC GSE SW Automation

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


class WorkflowRelationMapping(object):
    def __init__(self, cluster, reservation, computer_resource, network_path, blueprint, vsphere_machine_Id,
                 reservation_policy=None, storages=None, backup_svc_levels=[]):
        self._cluster = cluster
        self._reservation = reservation
        self._computer_resource = computer_resource
        self._network_path = network_path
        self._blueprint = blueprint
        self._vsphere_machine_Id = vsphere_machine_Id
        self._reservation_policy = reservation_policy
        self._storages = storages
        self._backup_svc_levels = backup_svc_levels

    def get_cluster(self):
        return self._cluster

    def get_reservation(self):
        return self._reservation

    def get_computer_resource(self):
        return self._computer_resource

    def get_network_path(self):
        return self._network_path

    def get_blueprint(self):
        return self._blueprint

    def get_vsphere_machine_Id(self):
        return self._vsphere_machine_Id

    def get_reservation_policy(self):
        return self._reservation_policy

    def get_storages(self):
        return self._storages

    def get_backup_svc_levels(self):
        return self._backup_svc_levels

    def update_backup_svc_levels(self, backup_svc_levels):
        assert isinstance(backup_svc_levels, list), \
            'backup_svc_levels passing to method update_backup_svc_levels for WorkflowRelationMapping object must be ' \
            'list.'
        self._backup_svc_levels = \
            backup_svc_levels + self._backup_svc_levels if self._backup_svc_levels else backup_svc_levels

    def set_reservation_policy(self, reservation_policy):
        self._reservation_policy = reservation_policy

    def set_blueprint(self, blueprint):
        self._blueprint = blueprint

    def update_storages(self, storages):
        self._storages = storages

    def __str__(self):
        return '\n{' + \
               '\n cluster name = {} ' \
               '\n reservation name = {} ' \
               '\n computer resource = {} ' \
               '\n network path = {} ' \
               '\n blueprint = {} ' \
               '\n vsphere machine id = {} ' \
               '\n reservation policy = {} ' \
               '\n storages = {} ' \
                   .format(self.get_cluster(), self.get_reservation(), self.get_computer_resource(),
                           self.get_network_path(), self.get_blueprint(), self.get_vsphere_machine_Id(),
                           self.get_reservation_policy(), self.get_storages()) \
               + '\n}\n'
