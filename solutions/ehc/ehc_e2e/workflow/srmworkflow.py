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

import functools
from robot.errors import ExecutionFailed
from ehc_e2e.workflow.setting import workflow_continue_on_failure
from ehc_e2e.auc.executable.generic import RequestChecker
from ehc_e2e.auc.executable.srm import SRMDRMigrationManager
from ehc_e2e.auc.executable.operate_vm import OperateVM
from .baseworkflow import BaseWorkflow


def catch_assert_exception(f):
    '''
    Just used for handling assert error and raise ExecutionFailed to let workflow continue running.
    '''
    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except AssertionError as ex:
            raise ExecutionFailed(ex.message, continue_on_failure=workflow_continue_on_failure)
    return func


class SRMDRWorkflow(BaseWorkflow):
    def cloud_administrator_prepares_for_srm_dp_failover(self):
        _cur_browser = self.wf_context.shared.current_browser
        SRMDRMigrationManager(
            self.cloud_administrator_prepares_for_srm_dp_failover.__name__,
            method_name=SRMDRMigrationManager.Func.PREPARE,
            browser=_cur_browser,
            protected_cluster=self.wf_context.srm_migration.protected_cluster,
        ).run()

        RequestChecker(
            self.cloud_administrator_prepares_for_srm_dp_failover.__name__,
            description=SRMDRMigrationManager.Func.PREPARE,
        ).run()

    def cloud_administrator_performs_srm_dr_recovery(self):
        # before srm dr recovery, pow off vm, or in turn off step of dr recovery maybe failed.
        _user_action_list = self.wf_context.operate_vm.user_action_list
        _deployed_vm = self.wf_context.deployed_vms[-1]
        _current_browser = self.wf_context.shared.current_browser
        _is_login = self.wf_context.shared.current_browser.is_login
        kwargs = {
            'current_browser': _current_browser,
            'is_login': _is_login,
            'vm_name': _deployed_vm,
            'user_action_list': _user_action_list
        }
        OperateVM(
            self.cloud_administrator_operates_vm.__name__,
            **kwargs
        ).run()

        kwargs = {
            'local_srm_hostname': self.wf_context.srm_migration.local_server.hostname,
            'username': self.wf_context.srm_migration.local_server.username,
            'password': self.wf_context.srm_migration.local_server.password,
            'remote_srm_hostname': self.wf_context.srm_migration.remote_server.hostname,
            'remote_username': self.wf_context.srm_migration.remote_server.username,
            'remote_password': self.wf_context.srm_migration.remote_server.password,
            'recovery_plan_name': self.wf_context.srm_migration.recovery_plan}

        SRMDRMigrationManager(
            self.cloud_administrator_performs_srm_dr_recovery.__name__,
            method_name=SRMDRMigrationManager.Func.RECOVER,
            **kwargs).run()

    def cloud_administrator_performs_srm_dr_reprotect(self):
        output = []
        kwargs = {
            'local_srm_hostname': self.wf_context.srm_migration.local_server.hostname,
            'username': self.wf_context.srm_migration.local_server.username,
            'password': self.wf_context.srm_migration.local_server.password,
            'remote_srm_hostname': self.wf_context.srm_migration.remote_server.hostname,
            'remote_username': self.wf_context.srm_migration.remote_server.username,
            'remote_password': self.wf_context.srm_migration.remote_server.password,
            'recovery_plan_name': self.wf_context.srm_migration.recovery_plan,
            'output': output
        }

        SRMDRMigrationManager(
            self.cloud_administrator_performs_srm_dr_reprotect.__name__,
            method_name=SRMDRMigrationManager.Func.REPROTECT,
            **kwargs).run()

        if len(output) == 1 and output[-1] == 'Successful':
            # if request success, exchagne protected site, protected clsuter, protected data center,
            # local server with recovery site, recovery clsuter, recovery data center, remote server
            (self.wf_context.srm_migration.local_server, self.wf_context.srm_migration.remote_server) = \
                (self.wf_context.srm_migration.remote_server, self.wf_context.srm_migration.local_server)
            (self.wf_context.srm_migration.protected_cluster, self.wf_context.srm_migration.recovery_cluster) = \
                (self.wf_context.srm_migration.recovery_cluster, self.wf_context.srm_migration.protected_cluster)

            (self.wf_context.dr_remediator.protected_sites, self.wf_context.dr_remediator.recovery_sites) = \
                (self.wf_context.dr_remediator.recovery_sites, self.wf_context.dr_remediator.protected_sites)

            (self.wf_context.dr_remediator.protected_data_center,
             self.wf_context.dr_remediator.recovery_data_center) = (self.wf_context.dr_remediator.recovery_data_center,
                                                                    self.wf_context.dr_remediator.protected_data_center)

    @catch_assert_exception
    def cloud_administrator_remediate_manages_srm_dr_protected_workloads(self):
        _cur_browser = self.wf_context.shared.current_browser
        _method_name = self.cloud_administrator_remediate_manages_srm_dr_protected_workloads.__name__
        SRMDRMigrationManager(
            _method_name,
            method_name=SRMDRMigrationManager.Func.REMEDIATE_MANAGEMENT,
            browser=_cur_browser,
            # Confirm with karman, for recovery cluster in Cluster choice tab should always the protect clsuter.
            recovery_cluster=self.wf_context.srm_migration.protected_cluster,
            email_address=self.wf_context.srm_migration.email_address,
        ).run()

    def cloud_administrator_validates_protection_for_srm_dr_workloads(self):
        _cur_browser = self.wf_context.shared.current_browser
        _protected_sites = self.wf_context.dr_remediator.protected_sites
        _protected_dc = self.wf_context.dr_remediator.protected_data_center
        _protected_cluster = self.wf_context.srm_migration.protected_cluster

        if len(_protected_sites) == 1:
            _protected_cluster = \
                '["{protected_site}"][{protected_dc}] {protected_cluster}'\
                    .format(protected_site=_protected_sites[0],
                            protected_dc=_protected_dc,
                            protected_cluster=_protected_cluster)
        elif len(_protected_sites) == 2:
            _protected_cluster = \
                '["{protected_site_1}","{protected_site_2}"][{protected_dc}] {protected_cluster}' \
                    .format(protected_site_1=_protected_sites[0],
                            protected_site_2=_protected_sites[1],
                            protected_dc=_protected_dc,
                            protected_cluster=_protected_cluster)
        _datastore_list = [_added_datastore.name for _added_datastore in self.wf_context.added_cloud_storage]
        _added_datastores = []
        for item in _datastore_list:
            _added_datastores.extend(item)
        _vm_list = getattr(self.wf_context, 'deployed_vms', [])
        SRMDRMigrationManager(
            self.cloud_administrator_validates_protection_for_srm_dr_workloads.__name__,
            method_name=SRMDRMigrationManager.Func.VALIDATE_PROTECTION,
            protected_cluster=_protected_cluster,
            browser=_cur_browser,
            datastore_list=_added_datastores,
            vm_list=_vm_list
        ).run()
        RequestChecker(
            self.cloud_administrator_validates_protection_for_srm_dr_workloads.__name__,
            description=SRMDRMigrationManager.Func.VALIDATE_PROTECTION
        ).run()

    def cloud_administrator_dr_remediator_all_datastores_and_vms(self):
        _cur_browser = self.wf_context.shared.current_browser
        _protected_sites = self.wf_context.dr_remediator.protected_sites
        _protected_dc = self.wf_context.dr_remediator.protected_data_center
        _protected_cluster = getattr(self.wf_context, 'existed_clusters', None)
        if isinstance(_protected_cluster, list) and len(_protected_cluster) > 0:
            _protected_cluster = _protected_cluster[0]
            if len(_protected_sites) == 1:
                _protected_cluster = \
                    '["{protected_site}"][{protected_dc}] {protected_cluster}' \
                        .format(protected_site=_protected_sites[0],
                                protected_dc=_protected_dc,
                                protected_cluster=_protected_cluster)
            elif len(_protected_sites) == 2:
                _protected_cluster = \
                    '["{protected_site_1}","{protected_site_2}"][{protected_dc}] {protected_cluster}' \
                        .format(protected_site_1=_protected_sites[0],
                                protected_site_2=_protected_sites[1],
                                protected_dc=_protected_dc,
                                protected_cluster=_protected_cluster)
        SRMDRMigrationManager(
            self.cloud_administrator_dr_remediator_all_datastores_and_vms.__name__,
            method_name=SRMDRMigrationManager.Func.VALIDATE_PROTECTION,
            protected_cluster=_protected_cluster,
            browser=_cur_browser,
            datastore_list=None,
            vm_list=None
        ).run()
        RequestChecker(
            self.cloud_administrator_dr_remediator_all_datastores_and_vms.__name__,
            description=SRMDRMigrationManager.Func.VALIDATE_PROTECTION
        ).run()
