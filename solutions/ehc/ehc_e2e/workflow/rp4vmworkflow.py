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
from datetime import datetime
from re import search
from robot.api import logger
from robot.errors import ExecutionFailed
from ehc_e2e.utils.service import VroItems
import ehc_e2e.constants.vro_vra_constants as vro_constants
from ehc_e2e.workflow.baseworkflow import BaseWorkflow
from ehc_e2e.auc.executable.generic import RequestChecker
from ehc_e2e.auc.executable.rp4vm import ClusterManager
from ehc_e2e.auc.executable.rp4vm import PolicyManager
from ehc_e2e.auc.executable.rp4vm import ProvisionRP4VMManager
from ehc_e2e.auc.executable.rp4vm import RP4VMOperationManager
from ehc_e2e.auc.executable.rp4vm import VCenterRelationshipManager
from ehc_e2e.auc.executable.rp4vm import VROvRPAClustersRetriever
from ehc_e2e.auc.executable.rp4vm import VRPAClustersManager
from ehc_e2e.auc.executable.rp4vm import VRPAProtectedVMsManager
from ehc_e2e.auc.executable.rp4vm import PreFailoverManager
from ehc_e2e.auc.executable.add_vcenter_relationship import AddVcenterRelationObj
from ehc_e2e.auc.rest.get_datastore_from_vro import GetDatastoreFromvRO


def catch_assert_exception(f):
    '''
    For handling assert error and raise ExecutionFailed to let workflow continue running.
    '''
    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except AssertionError as ex:
            raise ExecutionFailed(ex.message, continue_on_failure=True)

    return func


class RP4VMWorkflow(BaseWorkflow):
    @catch_assert_exception
    def cloud_administrator_onboards_vsan_cluster(self):
        cur_browser = self.wf_context.shared.current_browser
        action = self.wf_context.cluster_maintenance.onboard_vsan_cluster_for_rp4vm
        assert hasattr(self.wf_context, 'added_hwi') \
            and self.wf_context.added_hwi \
            and len(self.wf_context.added_hwi) > 1, "No hwi added or added hwi amount is not greater than 1."
        action.vsan_cluster_hardware_island = self.wf_context.added_hwi[0]
        action.partner_vsan_cluster_hardware_island = self.wf_context.added_hwi[1]

        output = []
        kw = {
            'vsan_cluster_hardware_island': action.vsan_cluster_hardware_island,
            'vsan_cluster_name': action.vsan_cluster_name,
            'partner_vsan_cluster_hardware_island': action.partner_vsan_cluster_hardware_island,
            'partner_vsan_cluster_name': action.partner_vsan_cluster_name,
            'cur_browser': cur_browser,
            'output': output
        }
        _method_name = ClusterManager.Func.ONBOARD_VSAN_CLUSTER
        ClusterManager(self.cloud_administrator_onboards_vsan_cluster.__name__,
                       method_name=_method_name,
                       **kw).run()
        request_result = []
        RequestChecker(self.cloud_administrator_onboards_vsan_cluster.__name__,
                       description=_method_name,
                       output=request_result).run()

        if request_result and \
                (len(request_result) == 1) and \
                (request_result[0].status == 'Successful') and \
                (len(output) == 1):
            # Write back on-boarded clusters to "existed_clusters"
            added_clusters = output[0]
            newly_added_clusters = [added_clusters.get('vsan_cluster'), added_clusters.get('partner_vsan_cluster_name')]
            if hasattr(self.wf_context, 'existed_clusters') and \
                    isinstance(self.wf_context.existed_clusters, list) and \
                            len(self.wf_context.existed_clusters) > 0:
                self.wf_context.existed_clusters.extend(newly_added_clusters)
            else:
                setattr(self.wf_context, 'existed_clusters', newly_added_clusters)
            # Write back to "added_cloud_storage"
            # added_cloud_storage:
            # -
            #     hwi_name: *hwi_a
            #     cluster_name: *protected_cluster
            #     name:
            #     - LON-AVP-Templates01
            #     srp: []
            # -
            #     hwi_name: *hwi_b
            #     cluster_name: *recovery_cluster
            #     name:
            #     - WSW-Local_1474500403137
            #     srp: []
            assert (hasattr(self.wf_context, 'added_cloud_storage') and
                    isinstance(self.wf_context.added_cloud_storage, list)), "'added_cloud_storage' is not defined."
            hwi_cluster = {kw.get('vsan_cluster_hardware_island'): added_clusters.get('vsan_cluster'),
                           kw.get('partner_vsan_cluster_hardware_island'): added_clusters.get(
                               'partner_vsan_cluster_name')}
            print hwi_cluster
            newly_added_datastores = self.wf_context.added_cloud_storage
            logger.info("Getting newly added datastore for every cluster-hwi pairs")
            for i in range(0, len(hwi_cluster)):
                newly_added_datastores[i].hwi_name = hwi_cluster.keys()[i]
                newly_added_datastores[i].cluster_name = hwi_cluster.values()[i]
                newly_added_datastores[i].name = []
                newly_added_datastores[i].srp = []
                datastore_list = GetDatastoreFromvRO().get_datastore_from_vro(
                    self.wf_context.vro,
                    newly_added_datastores[i].hwi_name,
                    newly_added_datastores[i].cluster_name
                )

                if datastore_list:
                    datastore_name = sorted(datastore_list, key=lambda datastore: int(datastore.id))[-1].name
                    newly_added_datastores[i].name.append(datastore_name)
                    logger.info("Got datastore name {0} based on cluster {1},hwi {2}"
                                .format(datastore_name, newly_added_datastores[i].cluster_name,
                                        newly_added_datastores[i].hwi_name))
            # sorting the newly_added_datastores based on the order of clusters added.
            for datastore in newly_added_datastores:
                assert datastore.cluster_name in newly_added_clusters, \
                    "Cluster name {} for  datastore {}  not found in newly added clusters"\
                        .format(datastore.cluster_name, datastore.name)
            newly_added_datastores.sort(key=lambda datastore: newly_added_clusters.index(datastore.cluster_name))
            self.wf_context.added_cloud_storage = newly_added_datastores


    @catch_assert_exception
    def cloud_administrator_onboards_local_cluster(self):
        cur_browser = self.wf_context.shared.current_browser
        action = self.wf_context.cluster_maintenance.onboard_local_cluster_for_rp4vm
        assert hasattr(self.wf_context, 'added_hwi') \
            and self.wf_context.added_hwi \
            and len(self.wf_context.added_hwi) > 1, "No hwi added or added hwi amount is not greater than 1."
        action.local_cluster_hardware_island = self.wf_context.added_hwi[0]
        action.partner_cluster_hardware_island = self.wf_context.added_hwi[1]

        output = []
        kw = {
            'local_cluster_hardware_island': action.local_cluster_hardware_island,
            'local_cluster_name': action.local_cluster_name,
            'partner_cluster_hardware_island': action.partner_cluster_hardware_island,
            'partner_cluster_name': action.partner_cluster_name,
            'cur_browser': cur_browser,
            'output': output
        }
        _method_name = ClusterManager.Func.ONBOARD_LOCAL_CLUSTER
        ClusterManager(self.cloud_administrator_onboards_local_cluster.__name__,
                       method_name=_method_name,
                       **kw).run()
        request_result = []
        RequestChecker(self.cloud_administrator_onboards_local_cluster.__name__,
                       description=_method_name,
                       output=request_result).run()

        if request_result and \
                (len(request_result) == 1) and \
                (request_result[0].status == 'Successful') and \
                (len(output) == 1):
            added_clusters = output[0]
            if hasattr(self.wf_context, 'existed_clusters') and \
                    isinstance(self.wf_context.existed_clusters, list) and \
                            len(self.wf_context.existed_clusters) > 0:
                self.wf_context.existed_clusters.extend([added_clusters.get('local_cluster'),
                                                         added_clusters.get('partner_cluster_name')])
            else:
                setattr(self.wf_context, 'existed_clusters',
                        [added_clusters.get('local_cluster'), added_clusters.get('partner_cluster_name')])

    def cloud_administrator_adds_rp4vm_vcenter_relationship(self):
        if hasattr(self.wf_context, 'added_vcenter'):
            added_vCenters = self.wf_context.added_vcenter
        else:
            added_vCenters = None
        method_name = VCenterRelationshipManager.Func.ADD_RELATIONSHIP
        cur_browser = self.wf_context.shared.current_browser
        related_vCenters = []
        if added_vCenters \
                and isinstance(added_vCenters, list) \
                and (len(added_vCenters) == 2):
            protected_vCenter_name = added_vCenters[0]
            recovery_vCenter_name = added_vCenters[1]
            protected_vCenter_user = self.wf_context.vCenter_relationship_to_add.protected_vCenter_credential.username
            protected_vCenter_pwd = self.wf_context.vCenter_relationship_to_add.protected_vCenter_credential.password
            recovery_vCenter_user = self.wf_context.vCenter_relationship_to_add.recovery_vCenter_credential.username
            recovery_vCenter_pwd = self.wf_context.vCenter_relationship_to_add.recovery_vCenter_credential.password

            protected_vCenter = {
                'vCenter_name': protected_vCenter_name,
                'vCenter_user': protected_vCenter_user,
                'vCenter_pwd': protected_vCenter_pwd
            }
            recovery_vCenter = {
                'vCenter_name': recovery_vCenter_name,
                'vCenter_user': recovery_vCenter_user,
                'vCenter_pwd': recovery_vCenter_pwd
            }
        else:
            protected_vCenter = None
            recovery_vCenter = None

        NSX_is_available = self.wf_context.vCenter_relationship_to_add.NSX_is_available
        if NSX_is_available:
            protected_NSX = self.wf_context.vCenter_relationship_to_add.protected_NSX_manager
            protected_NSX_mgr = {
                'mgr_url': protected_NSX.url,
                'mgr_user': protected_NSX.username,
                'mgr_pwd': protected_NSX.password
            }
            recovery_NSX = self.wf_context.vCenter_relationship_to_add.recovery_NSX_manager
            recovery_NSX_mgr = {
                'mgr_url': recovery_NSX.url,
                'mgr_user': recovery_NSX.username,
                'mgr_pwd': recovery_NSX.password
            }
        else:
            protected_NSX_mgr = None
            recovery_NSX_mgr = None

        VCenterRelationshipManager(
            self.cloud_administrator_adds_vcenter_relationship.__name__,
            method_name=method_name,
            browser=cur_browser,
            protected_vcenter=protected_vCenter,
            recovery_vcenter=recovery_vCenter,
            NSX_available=NSX_is_available,
            protected_nsx_mgr=protected_NSX_mgr,
            recovery_nsx_mgr=recovery_NSX_mgr,
            output=related_vCenters
            ).run()
        request_result = []
        RequestChecker(self.cloud_administrator_adds_rp4vm_vcenter_relationship.__name__,
                       description=method_name,
                       output=request_result).run()
        if len(request_result) == 1 \
                and (request_result[0].status == 'Successful') \
                and len(related_vCenters) == 1:
            setattr(self.wf_context.shared.RP4VM_related_vCenters, 'protected_vCenter',
                    related_vCenters[-1].get('protected_vcenter'))
            setattr(self.wf_context.shared.RP4VM_related_vCenters, 'recovery_vCenter',
                    related_vCenters[-1].get('recovery_vcenter'))
            # keep original logic and add code to save  vcenter relationship info into added_vcenter_relationship,
            # use to delete vcenter relationship wisely and scenario tear town
            vcenter_relationship_obj = AddVcenterRelationObj()
            vcenter_relationship_obj.protected_vcenter = related_vCenters[-1].get('protected_vcenter')
            vcenter_relationship_obj.recovery_vcenter = related_vCenters[-1].get('recovery_vcenter')
            if not isinstance(getattr(self.wf_context, 'added_vcenter_relationship', None), list):
                setattr(self.wf_context, 'added_vcenter_relationship', [])
            getattr(self.wf_context, 'added_vcenter_relationship').append(vcenter_relationship_obj)

    def cloud_administrator_deletes_rp4vm_vcenter_relationship(self):
        related_vCenters = self.wf_context.shared.RP4VM_related_vCenters
        method_name = VCenterRelationshipManager.Func.DELETE_RELATIONSHIP
        cur_browser = self.wf_context.shared.current_browser
        if related_vCenters \
                and hasattr(related_vCenters, 'protected_vCenter') \
                and hasattr(related_vCenters, 'recovery_vCenter'):
            protected_vCenter = {'vCenter_name': related_vCenters.protected_vCenter}
            recovery_vCenter = {'vCenter_name': related_vCenters.recovery_vCenter}
        else:
            protected_vCenter = None
            recovery_vCenter = None
        VCenterRelationshipManager(
            self.cloud_administrator_deletes_rp4vm_vcenter_relationship.__name__,
            method_name=method_name,
            browser=cur_browser,
            protected_vcenter=protected_vCenter,
            recovery_vcenter=recovery_vCenter
        ).run()

        request_result = []
        RequestChecker(self.cloud_administrator_deletes_rp4vm_vcenter_relationship.__name__,
                       description=method_name,
                       output=request_result).run()
        if len(request_result) == 1\
                and (request_result[0].status == 'Successful'):
            self.wf_context.shared.RP4VM_related_vCenters.protected_vCenter = None
            self.wf_context.shared.RP4VM_related_vCenters.recovery_vCenter = None

    def cloud_administrator_adds_vRPA_clusters(self):
        self.wf_context.shared.RP4VM_vRPA_clusters.primary.__dict__= dict(ip='',
                 user='',
                 password='',
                 port=443)
        self.wf_context.shared.RP4VM_vRPA_clusters.secondary.__dict__ = dict(ip='',
                 user='',
                 password='',
                 port=443)

        vRPA_info = self.wf_context.vRPA_cluster_to_add
        cur_browser = self.wf_context.shared.current_browser
        method_name = VRPAClustersManager.Func.ADD_CLUSTER
        created_vRPA_cluster = []
        _to_create_vRPA_clusters = []
        if vRPA_info:
            primary_cluser = vRPA_info.primary_clusetr
            primary_ip = primary_cluser.ip
            primary_admin = primary_cluser.admin
            primary_pwd = primary_cluser.password
            secondary_cluster = vRPA_info.secondary_cluster
            secondary_ip = secondary_cluster.ip
            secondary_admin = secondary_cluster.admin
            secondary_pwd = secondary_cluster.password
            _to_create_vRPA_clusters.extend([primary_ip, secondary_ip])
            primary_info = {
                'management_ip': primary_ip,
                'admin_user': primary_admin,
                'admin_password': primary_pwd
            }

            secondary_info = {
                'management_ip': secondary_ip,
                'admin_user': secondary_admin,
                'admin_password': secondary_pwd
            }
        else:
            primary_info = {}
            secondary_info = {}

        _available_vRPA_clusters = []
        try:
            VROvRPAClustersRetriever(
                self.cloud_administrator_gets_vRPA_clusters_from_vRO.__name__,
                vro_address=self.wf_context.vro.address,
                vro_username=self.wf_context.vro.username,
                vro_password=self.wf_context.vro.password,
                pri_ip=primary_info.get('management_ip'),
                sec_ip=secondary_info.get('management_ip'),
                output=_available_vRPA_clusters
            ).run()
        except:
            pass

        if len(_available_vRPA_clusters) > 0 and \
            len(_to_create_vRPA_clusters) > 0 and \
                (set(_to_create_vRPA_clusters)
                     <= set([cluster.cluster_mgmt_ip for cluster in _available_vRPA_clusters])):
            self.wf_context.shared.RP4VM_vRPA_clusters.primary.__dict__.update(
                dict(ip=primary_info.get('management_ip'),
                     user=primary_info.get('admin_user'),
                     password=primary_info.get('admin_password'),
                     port=443))
            self.wf_context.shared.RP4VM_vRPA_clusters.secondary.__dict__.update(
                dict(ip=secondary_info.get('management_ip'),
                     user=secondary_info.get('admin_user'),
                     password=secondary_info.get('admin_password'),
                     port=443))
        else:
            VRPAClustersManager(
                self.cloud_administrator_adds_vRPA_clusters.__name__,
                method_name=method_name,
                browser=cur_browser,
                primary_cluster=primary_info,
                secondary_cluster=secondary_info,
                output=created_vRPA_cluster).run()

            request_result = []
            RequestChecker(self.cloud_administrator_adds_vRPA_clusters.__name__,
                           description=method_name,
                           ignore_failure=True,
                           output=request_result).run()

            if (len(request_result) == 1) \
                    and (request_result[0].status == 'Successful') \
                    and (len(created_vRPA_cluster) == 1):
                self.wf_context.shared.RP4VM_vRPA_clusters.primary.__dict__.update(
                    dict(ip=created_vRPA_cluster[-1].get('primary_mgmt_ip'),
                         user=primary_info.get('admin_user'),
                         password=primary_info.get('admin_password'),
                         port=443))
                self.wf_context.shared.RP4VM_vRPA_clusters.secondary.__dict__.update(
                    dict(ip=created_vRPA_cluster[-1].get('secondary_mgmt_ip'),
                         user=secondary_info.get('admin_user'),
                         password=secondary_info.get('admin_password'),
                         port=443))

    def cloud_administrator_deletes_vRPA_clusters(self):
        if not hasattr(self.wf_context, 'shared') or \
            not hasattr(self.wf_context.shared, 'RP4VM_vRPA_clusters'):
            logger.info("It's not an RP4VM workflow or scenario, no vRPA clusters is added.")
        else:
            _available_vRPA_clusters = []
            method_name = VRPAClustersManager.Func.DELETE_CLUSTER
            _primary_cluster_name = None

            _added_clusters = self.wf_context.shared.RP4VM_vRPA_clusters
            if not (hasattr(_added_clusters, 'primary')
                   and hasattr(_added_clusters.primary, 'ip')
                   and _added_clusters.primary.ip
                    and hasattr(_added_clusters, 'secondary')
                   and hasattr(_added_clusters.secondary, 'ip')
                   and _added_clusters.secondary.ip):
                logger.warn("VRPA cluster pair primary IP or secondary IP is not provided.")
            else:
                primary_mgmt_ip = _added_clusters.primary.ip
                secondary_mgmt_ip = _added_clusters.secondary.ip
                try:
                    VROvRPAClustersRetriever(
                        self.cloud_administrator_gets_vRPA_clusters_from_vRO.__name__,
                        vro_address=self.wf_context.vro.address,
                        vro_username=self.wf_context.vro.username,
                        vro_password=self.wf_context.vro.password,
                        pri_ip=primary_mgmt_ip,
                        sec_ip=secondary_mgmt_ip,
                        output=_available_vRPA_clusters
                    ).run()
                except:
                    pass
                assert len(_available_vRPA_clusters) > 0, \
                    "No vRPA clusters are matched in vRO with provided vRPA clusters."
                for cluster in _available_vRPA_clusters:
                    if cluster.cluster_mgmt_ip == primary_mgmt_ip:
                        _primary_cluster_name = cluster.name
                        break

                cur_browser = self.wf_context.shared.current_browser
                VRPAClustersManager(
                    self.cloud_administrator_deletes_vRPA_clusters.__name__,
                    method_name=method_name,
                    browser=cur_browser,
                    primary_clusert_name=_primary_cluster_name
                ).run()

                request_result = []
                RequestChecker(self.cloud_administrator_deletes_vRPA_clusters.__name__,
                               description=method_name,
                               output=request_result).run()

                if len(request_result) == 1 \
                        and (request_result[0].status == 'Successful'):
                    for key in self.wf_context.shared.RP4VM_vRPA_clusters.primary.__dict__.iterkeys():
                        setattr(self.wf_context.shared.RP4VM_vRPA_clusters.primary, key, None)
                    for key in self.wf_context.shared.RP4VM_vRPA_clusters.secondary.__dict__.iterkeys():
                        setattr(self.wf_context.shared.RP4VM_vRPA_clusters.secondary, key, None)
                logger.info("VRPA cluster pair with primary ip:{0} and secondary ip:{1} is deleted."
                            .format(primary_mgmt_ip, secondary_mgmt_ip))

    def cloud_administrator_gets_vRPA_clusters_from_vRO(self):
        VROvRPAClustersRetriever(
            self.cloud_administrator_gets_vRPA_clusters_from_vRO.__name__,
            vro_address=self.wf_context.vro.address,
            vro_username=self.wf_context.vro.username,
            vro_password=self.wf_context.vro.password,
            output=self.wf_context.get_vrpa_clusters_from_vro.available_vrpa_clusters
        ).run()

    def cloud_administrator_adds_rp4vm_policy(self):
        cur_browser = self.wf_context.shared.current_browser
        assert hasattr(self.wf_context, 'policy_info'), 'No policy_info find in YAML file.'
        policy_info = self.wf_context.policy_info
        added_rp4vm_policy = []
        kwargs = {
            'policy_name': policy_info.policy_name,
            'policy_type': policy_info.policy_type,
            'journal_size': policy_info.journal_size,
            'rpo_number': policy_info.rp_number,
            'rpo_units': policy_info.rp_units
        }

        (vro_response_dict, vro_rest_base) = VroItems(
            self.wf_context).get_all_items_from_vro(vro_constants.RP4VM_POLICY_API)
        rp4vm_policy_existed_dict = self._check_rp4vm_policy_existence(policy_info, vro_response_dict,
                                                                       vro_rest_base)
        if rp4vm_policy_existed_dict['name'] and rp4vm_policy_existed_dict['configuration']:
            added_rp4vm_policy.append(policy_info.policy_name)
            logger.info('RP4VM policy with same name and configuration already existed, no need to add.', False, True)
        elif rp4vm_policy_existed_dict['name'] and not rp4vm_policy_existed_dict['configuration']:
            raise AssertionError('RP4VM policy with name: {} already existed, '
                                 'but not same configuration, please change name.'.format(policy_info.policy_name))
        else:
            if 'Synchronous'.lower() == policy_info.policy_type.lower():
                description = 'test_add_synchronous_policy_{}'.format(policy_info.policy_name)
                kwargs['description'] = description
                PolicyManager(
                    self.cloud_administrator_adds_rp4vm_policy.__name__,
                    method_name=PolicyManager.Func.ADD_SYNC_POLICY,
                    browser=cur_browser,
                    **kwargs
                ).run()
            elif 'Asynchronous'.lower() == policy_info.policy_type.lower():
                description = 'test_add_asynchronous_policy_{}'.format(kwargs['policy_name'])
                kwargs['description'] = description
                PolicyManager(
                    self.cloud_administrator_adds_rp4vm_policy.__name__,
                    method_name=PolicyManager.Func.ADD_ASYNC_POLICY,
                    browser=cur_browser,
                    **kwargs
                ).run()
            else:
                raise AssertionError('replication_type should be in [Asynchronous, Synchronous]')

            logger.info("Add RP4VM Policy: {policy_name}, TYPE: {policy_type}".format(
                policy_name=policy_info.policy_name, policy_type=policy_info.policy_type), False, True)

            request_result = []
            RequestChecker(self.cloud_administrator_adds_rp4vm_policy.__name__,
                           description=description,
                           output=request_result).run()
            if request_result and request_result[0].status == 'Successful':
                added_rp4vm_policy.append(policy_info.policy_name)

        setattr(self.wf_context, 'added_rp4vm_policy', added_rp4vm_policy)
        logger.info("Added RP4VM Policy: {}".format(added_rp4vm_policy), False, True)

    def cloud_administrator_deletes_rp4vm_policy(self):

        cur_browser = self.wf_context.shared.current_browser
        policy_to_delete = getattr(self.wf_context, 'added_rp4vm_policy', [])
        if not policy_to_delete:
            logger.info('No RP4VM Policy need to delete.', False, True)
            return

        logger.info('All RP4VM Policy need to delete: {}'.format(policy_to_delete), False, True)

        for policy in policy_to_delete:
            logger.info('Start to delete RP4VM Policy: {}'.format(policy), False, True)
            kwargs = {
                'policy_name': policy,
                'description': 'test_delete_rp4vm_policy_{}'.format(policy)
            }
            PolicyManager(
                self.cloud_administrator_deletes_rp4vm_policy.__name__,
                method_name=PolicyManager.Func.DELETE_POLICY,
                browser=cur_browser,
                **kwargs
            ).run()

            RequestChecker(self.cloud_administrator_deletes_rp4vm_policy.__name__,
                           description=kwargs['description']).run()

            logger.info("Deleted RP4VM Policy: {policyname}".format(
                policyname=policy), False, True)

    def cloud_administrator_provisions_vm_without_rp4vm(self):
        cur_browser = self.wf_context.shared.current_browser

        kwargs = {
            'blueprint': self.wf_context.deploy_vm.blueprint.name,
        }
        ProvisionRP4VMManager(
            self.cloud_administrator_provisions_vm_without_rp4vm.__name__,
            method_name=ProvisionRP4VMManager.Func.PROVISION_VM,
            browser=cur_browser,
            **kwargs
        ).run()

        deployed_vms_info = []
        RequestChecker(self.cloud_administrator_provisions_vm_without_rp4vm.__name__,
                       description='',
                       output=deployed_vms_info).run()

        vm_details = deployed_vms_info[-1].status_details
        vm_pattern = r'^Request succeeded. Created (.*)\.$'
        match = search(vm_pattern, vm_details)
        if match:
            vm_str = str(match.group(1))
            if not self.wf_context.deployed_vms:
                self.wf_context.deployed_vms = [vm_str]
            else:
                self.wf_context.deployed_vms.append(vm_str)
            logger.info("Provision VM: {vm_str}".format(vm_str=vm_str), False, True)

    def cloud_administrator_provisions_rp4vm_using_new_cg(self):
        cur_browser = self.wf_context.shared.current_browser
        cg_name = "Auto_CG_%s" % datetime.now().strftime('%m%d%H%M')
        backup_service = ''
        if hasattr(self.wf_context, 'added_backup_service_level'):
            backup_service = getattr(self.wf_context.added_backup_service_level, 'backup_to_operate_vm', None)
        kwargs = {
            'blueprint': self.wf_context.rp4vm_info.blueprint,
            'vsphere_blueprint_id': self.wf_context.rp4vm_info.vsphere_blueprint_id,
            'cg': cg_name,
            'sequence': str(self.wf_context.rp4vm_info.sequence),
            'policy': self.wf_context.policy_info.policy_name,
            'backup_service':  backup_service,
        }
        deployed_vms_info = []

        ProvisionRP4VMManager(
            self.cloud_administrator_provisions_rp4vm_using_new_cg.__name__,
            method_name=ProvisionRP4VMManager.Func.PROVISION_RP4VM,
            browser=cur_browser,
            **kwargs
        ).run()

        RequestChecker(self.cloud_administrator_provisions_rp4vm_using_new_cg.__name__,
                       description=ProvisionRP4VMManager.Func.PROVISION_RP4VM,
                       method_name=RequestChecker.Func.BLUEPRINT_REQUEST,
                       output=deployed_vms_info).run()

        vm_str = deployed_vms_info[-1].deployed_vms[-1]

        if not self.wf_context.deployed_vms:
            self.wf_context.deployed_vms = [vm_str]
        else:
            self.wf_context.deployed_vms.append(vm_str)

        if not self.wf_context.rp4vm_info.protected_vms:
            self.wf_context.rp4vm_info.protected_vms = [vm_str]
        else:
            self.wf_context.rp4vm_info.protected_vms.append(vm_str)

        if not self.wf_context.rp4vm_info.cg_list:
            self.wf_context.rp4vm_info.cg_list = [cg_name]
        else:
            self.wf_context.rp4vm_info.cg_list.append(cg_name)
        logger.info("Provision RP4VM: {vm_str}, CG: {cg_name}".format(vm_str=vm_str, cg_name=cg_name), False, True)

    def cloud_administrator_provisions_rp4vm_using_existing_cg(self):
        cur_browser = self.wf_context.shared.current_browser
        cg_name = self.wf_context.rp4vm_info.cg_list[-1]
        backup_service = ''
        if hasattr(self.wf_context, 'added_backup_service_level'):
            backup_service = getattr(self.wf_context.added_backup_service_level, 'backup_to_operate_vm', None)
        kwargs = {
            'blueprint': self.wf_context.rp4vm_info.blueprint,
            'vsphere_blueprint_id': self.wf_context.rp4vm_info.vsphere_blueprint_id,
            'cg': cg_name,
            'sequence': str(self.wf_context.rp4vm_info.sequence),
            'policy': self.wf_context.policy_info.policy_name,
            'backup_service': backup_service,
        }
        deployed_vms_info = []
        ProvisionRP4VMManager(
            self.cloud_administrator_provisions_rp4vm_using_existing_cg.__name__,
            method_name=ProvisionRP4VMManager.Func.PROVISION_RP4VM,
            browser=cur_browser,
            **kwargs
        ).run()
        RequestChecker(self.cloud_administrator_provisions_rp4vm_using_existing_cg.__name__,
                       description=ProvisionRP4VMManager.Func.PROVISION_RP4VM,
                       method_name=RequestChecker.Func.BLUEPRINT_REQUEST,
                       output=deployed_vms_info).run()

        vm_str = deployed_vms_info[-1].deployed_vms[-1]

        if not self.wf_context.deployed_vms:
            self.wf_context.deployed_vms = [vm_str]
        else:
            self.wf_context.deployed_vms.append(vm_str)

        if not self.wf_context.rp4vm_info.protected_vms:
            self.wf_context.rp4vm_info.protected_vms = [vm_str]
        else:
            self.wf_context.rp4vm_info.protected_vms.append(vm_str)

        logger.info("Provision RP4VM: {vm_str}, CG: {cg_name}".format(vm_str=vm_str, cg_name=cg_name), False, True)

    def cloud_administrator_protects_vm_using_new_cg(self):
        cur_browser = self.wf_context.shared.current_browser
        cg_name = "Auto_CG_%s" % datetime.now().strftime('%m%d%H%M')
        vm_str = self.wf_context.deployed_vms[-1]
        kwargs = {
            'vm': vm_str,
            'is_new_cg': True,
            'cg': cg_name,
            'sequence': str(self.wf_context.rp4vm_info.sequence),
            'policy': self.wf_context.policy_info.policy_name
        }
        RP4VMOperationManager(
            self.cloud_administrator_protects_vm_using_new_cg.__name__,
            method_name=RP4VMOperationManager.Func.PROTECT_VM,
            browser=cur_browser,
            **kwargs
        ).run()

        RequestChecker(self.cloud_administrator_protects_vm_using_new_cg.__name__,
                       description=RP4VMOperationManager.Func.PROTECT_VM).run()

        if not self.wf_context.rp4vm_info.cg_list:
            self.wf_context.rp4vm_info.cg_list = [cg_name]
        else:
            self.wf_context.rp4vm_info.cg_list.append(cg_name)

        if not self.wf_context.rp4vm_info.protected_vms:
            self.wf_context.rp4vm_info.protected_vms = [vm_str]
        else:
            self.wf_context.rp4vm_info.protected_vms.append(vm_str)
        logger.info("Protect VM: {vm_str}, CG: {cg_name}".format(vm_str=vm_str, cg_name=cg_name), False, True)

    def cloud_administrator_protects_vm_using_existing_cg(self):

        cur_browser = self.wf_context.shared.current_browser
        vm_str = self.wf_context.deployed_vms[-1]
        cg_name = self.wf_context.rp4vm_info.cg_list[-1]
        kwargs = {
            'vm': vm_str,
            'is_new_cg': False,
            'cg': cg_name,
            'sequence': str(self.wf_context.rp4vm_info.sequence),
            'policy': self.wf_context.policy_info.policy_name
        }
        RP4VMOperationManager(
            self.cloud_administrator_protects_vm_using_existing_cg.__name__,
            method_name=RP4VMOperationManager.Func.PROTECT_VM,
            browser=cur_browser,
            **kwargs
        ).run()

        RequestChecker(self.cloud_administrator_protects_vm_using_existing_cg.__name__,
                       description=RP4VMOperationManager.Func.PROTECT_VM).run()

        if not self.wf_context.rp4vm_info.protected_vms:
            self.wf_context.rp4vm_info.protected_vms = [vm_str]
        else:
            self.wf_context.rp4vm_info.protected_vms.append(vm_str)
        logger.info("Protect VM: {vm_str}, CG: {cg_name}".format(vm_str=vm_str, cg_name=cg_name), False, True)

    def cloud_administrator_changes_to_a_new_cg(self):

        cur_browser = self.wf_context.shared.current_browser
        cg_name = "Auto_CG_%s" % datetime.now().strftime('%m%d%H%M')
        vm_str = self.wf_context.rp4vm_info.protected_vms[-1]
        kwargs = {
            'vm': vm_str,
            'is_new_cg': True,
            'cg': cg_name,
            'sequence': str(self.wf_context.rp4vm_info.sequence),
            'policy': self.wf_context.policy_info.policy_name
        }
        RP4VMOperationManager(
            self.cloud_administrator_changes_to_a_new_cg.__name__,
            method_name=RP4VMOperationManager.Func.CHANGE_CG,
            browser=cur_browser,
            **kwargs
        ).run()

        RequestChecker(self.cloud_administrator_changes_to_a_new_cg.__name__,
                       description=RP4VMOperationManager.Func.CHANGE_CG).run()

        self.wf_context.rp4vm_info.cg_list.append(cg_name)
        logger.info("RP4VM: {vm_str}, change CG to:{cg_name}".format(vm_str=vm_str, cg_name=cg_name), False, True)

    def cloud_administrator_changes_to_an_existing_cg(self):
        if len(self.wf_context.rp4vm_info.cg_list) < 2:
            logger.warn('Number of existing CGs is less than 2. Cannot perform changing action. Task ignored.')
            return

        cur_browser = self.wf_context.shared.current_browser
        vm_str = self.wf_context.rp4vm_info.protected_vms[-1]

        kwargs = {
            'vm': vm_str,
            'is_new_cg': False,
            'cg': self.wf_context.rp4vm_info.cg_list[-2],
            'sequence': str(self.wf_context.rp4vm_info.sequence),
            'policy': self.wf_context.policy_info.policy_name
        }
        RP4VMOperationManager(
            self.cloud_administrator_changes_to_an_existing_cg.__name__,
            method_name=RP4VMOperationManager.Func.CHANGE_CG,
            browser=cur_browser,
            **kwargs
        ).run()

        RequestChecker(self.cloud_administrator_changes_to_an_existing_cg.__name__,
                       description=RP4VMOperationManager.Func.CHANGE_CG).run()

        logger.info("RP4VM: {vm_str}, CHANGE CG From: {cg_name1} To: {cg_name2}".format(
            vm_str=vm_str, cg_name1=self.wf_context.rp4vm_info.cg_list[-1],
            cg_name2=self.wf_context.rp4vm_info.cg_list[-2]), False, True)

        self.wf_context.rp4vm_info.cg_list[-2], self.wf_context.rp4vm_info.cg_list[-1] = \
            self.wf_context.rp4vm_info.cg_list[-1], self.wf_context.rp4vm_info.cg_list[-2]

    def cloud_administrator_changes_boot_sequence(self):
        cur_browser = self.wf_context.shared.current_browser
        kwargs = {
            'vm': self.wf_context.rp4vm_info.protected_vms[-1],
            'is_new_cg': False,
            'cg': self.wf_context.rp4vm_info.cg_list[-1],
            'sequence': str(self.wf_context.rp4vm_info.sequence),
            'policy': self.wf_context.policy_info.policy_name
        }
        RP4VMOperationManager(
            self.cloud_administrator_changes_boot_sequence.__name__,
            method_name=RP4VMOperationManager.Func.CHANGE_BOOT_PRIORITY,
            browser=cur_browser,
            **kwargs
        ).run()

        RequestChecker(self.cloud_administrator_changes_boot_sequence.__name__,
                       description=RP4VMOperationManager.Func.CHANGE_BOOT_PRIORITY).run()

    def cloud_administrator_unprotects_vm(self):
        cur_browser = self.wf_context.shared.current_browser
        vm_str = self.wf_context.rp4vm_info.protected_vms[-1]
        kwargs = {
            'vm': vm_str,
            'is_new_cg': False,
            'sequence': str(self.wf_context.rp4vm_info.sequence),
            'policy': self.wf_context.policy_info.policy_name
        }
        RP4VMOperationManager(
            self.cloud_administrator_unprotects_vm.__name__,
            method_name=RP4VMOperationManager.Func.UNPROTECT_VM,
            browser=cur_browser,
            **kwargs
        ).run()

        RequestChecker(self.cloud_administrator_unprotects_vm.__name__,
                       description=RP4VMOperationManager.Func.UNPROTECT_VM).run()

        logger.info("Unprotecded VM: {vm_str}".format(vm_str=vm_str), False, True)
        self.wf_context.rp4vm_info.protected_vms.pop()

    def cloud_administrator_unprotects_all_vms(self):
        cur_browser = self.wf_context.shared.current_browser
        while self.wf_context.rp4vm_info.protected_vms:
            # Wenda: remove try-except-finally blocks
            vm_str = self.wf_context.rp4vm_info.protected_vms[-1]
            kwargs = {
                'vm': vm_str,
                'is_new_cg': False,
                'sequence': str(self.wf_context.rp4vm_info.sequence),
                'policy': self.wf_context.policy_info.policy_name
            }
            RP4VMOperationManager(
                self.cloud_administrator_unprotects_vm.__name__,
                method_name=RP4VMOperationManager.Func.UNPROTECT_VM,
                browser=cur_browser,
                **kwargs
            ).run()

            RequestChecker(self.cloud_administrator_unprotects_vm.__name__,
                           description=RP4VMOperationManager.Func.UNPROTECT_VM).run()

            logger.info("Unprotecded VM: {vm_str}".format(vm_str=vm_str), False, True)
            self.wf_context.rp4vm_info.protected_vms.pop()

    def cloud_administrator_performs_failover_on_protected_vms(self):
        # get password of current user.
        _current_user = self._get_current_user_info()
        assert _current_user, 'Failed to get current user, please login to vra first.'
        username = _current_user['username']
        domain = _current_user['domain']
        self.wf_context.shared.RP4VM_Failover.consistency_group_name = \
            '%s@%s-%s' % (username,
                          domain,
                          self.wf_context.rp4vm_info.cg_list[-1])

        _vrpa_mgmt_node = self.wf_context.shared.RP4VM_vRPA_clusters.primary

        # Below line only chose one CG which could make the workflow pass, but this was due to
        # an EHC RP4VM bug. we updated this now after the bug being fixed.
        # _failover_cg_name = self.wf_context.shared.RP4VM_Failover.consistency_group_name
        failover_cg_names = \
            ['{}@{}-{}'.format(username, domain, cg) for cg in self.wf_context.rp4vm_info.cg_list]

        for cg_name in failover_cg_names:
            logger.info('Started to failover VMs under CG:{}'.format(cg_name), False, True)
            kwargs = {
                'hostname_ip_adds': _vrpa_mgmt_node.ip,
                'port': _vrpa_mgmt_node.port,
                'username': _vrpa_mgmt_node.user,
                'password': _vrpa_mgmt_node.password,
                'cg_name': cg_name}

            VRPAProtectedVMsManager(
                self.cloud_administrator_performs_failover_on_protected_vms.__name__,
                method_name=VRPAProtectedVMsManager.Func.FAILOVER,
                **kwargs
            ).run()
            logger.info('Completed failover VMs under CG:{}'.format(cg_name), False, True)

        self.wf_context.shared.RP4VM_vRPA_clusters.primary, self.wf_context.shared.RP4VM_vRPA_clusters.secondary = \
            self.wf_context.shared.RP4VM_vRPA_clusters.secondary, self.wf_context.shared.RP4VM_vRPA_clusters.primary

    def cloud_administrator_adds_post_failover_synchronization(self):
        VRPAProtectedVMsManager(
            self.cloud_administrator_adds_post_failover_synchronization.__name__,
            method_name=VRPAProtectedVMsManager.Func.POST_FAILOVER_SYNC,
            browser=self.wf_context.shared.current_browser
        ).run()

        RequestChecker(
            self.cloud_administrator_adds_post_failover_synchronization.__name__,
            description=VRPAProtectedVMsManager.Func.POST_FAILOVER_SYNC
        ).run()

    def cloud_administrator_prefailovers_stage_cgs(self):
        cur_browser = self.wf_context.shared.current_browser
        # get password of current user.
        _current_user = self._get_current_user_info()
        assert _current_user, 'Failed to get current user, please login to vra first.'
        username = _current_user['username']
        domain = _current_user['domain']
        kwargs = {
            'user': "%s@%s" % (username, domain),
            'cgs': self.wf_context.rp4vm_info.cg_list,
            'bg': self.wf_context.vra.business_group
        }
        PreFailoverManager(
            self.cloud_administrator_prefailovers_stage_cgs.__name__,
            method_name=PreFailoverManager.Func.STAGE_CGs,
            browser=cur_browser,
            **kwargs
        ).run()

        RequestChecker(self.cloud_administrator_prefailovers_stage_cgs.__name__,
                       description=PreFailoverManager.Func.STAGE_CGs
                      ).run()

        logger.info("Stage CGs: {cg_list}".format(cg_list=self.wf_context.rp4vm_info.cg_list), False, True)

    def cloud_administrator_prefailovers_unstage_cgs(self):
        cur_browser = self.wf_context.shared.current_browser
        # get password of current user.
        _current_user = self._get_current_user_info()
        assert _current_user, 'Failed to get current user, please login to vra first.'
        username = _current_user['username']
        domain = _current_user['domain']
        kwargs = {
            'user': "%s@%s" % (username, domain),
            'cgs': self.wf_context.rp4vm_info.cg_list,
            'bg': self.wf_context.vra.business_group
        }
        PreFailoverManager(
            self.cloud_administrator_prefailovers_unstage_cgs.__name__,
            method_name=PreFailoverManager.Func.UNSTAGE_CGs,
            browser=cur_browser,
            **kwargs
        ).run()

        RequestChecker(self.cloud_administrator_prefailovers_unstage_cgs.__name__,
                       description=PreFailoverManager.Func.UNSTAGE_CGs
                      ).run()

        logger.info("UNStage CGs: {cg_list}".format(cg_list=self.wf_context.rp4vm_info.cg_list), False, True)

    def _check_rp4vm_policy_existence(self, rp4vm_policy_item, vro_response_dict, vro_rest_base):
        """

        Args:
            rp4vm_policy_item: rp4vm_policy to add(Object)
            vro_response_dict: vro request response dict(dict)
            vro_rest_base: vro_rest_base: VRORestBase Object(Object)
        Returns: rp4vm_policy_name_varray_existed_dict(dict)

        """
        rp4vm_policy_existed_dict = dict(name=False, configuration=False)

        for item in vro_response_dict.get('relations', {}).get('link', []):
            item_attr = vro_rest_base.name_value_pairs_to_dict(item.get('attributes', {}))
            if item_attr:
                if rp4vm_policy_item.policy_name == item_attr.get('name'):
                    rp4vm_policy_existed_dict['name'] = True
                    logger.debug("RP4VM policy name {0} is already in use.".format(rp4vm_policy_item.policy_name))
                    if 'Synchronous'.lower() == rp4vm_policy_item.policy_type.lower():
                        if rp4vm_policy_item.policy_type == item_attr.get('replication_type') and \
                                        str(rp4vm_policy_item.journal_size) == item_attr.get('journal_size'):
                            rp4vm_policy_existed_dict['configuration'] = True
                            logger.info('Same rp4vm policy name, also same configuration.', False, True)
                        else:
                            logger.warn('Same rp4vm policy name, but not same configuration, '
                                        'Configuration of policy to be added: replication_type: {}, journal_size: {}.'
                                        'Configuration of policy existed: replication_type: {}, journal_size: {}.'.
                                format(
                                rp4vm_policy_item.policy_type, str(rp4vm_policy_item.journal_size),
                                item_attr.get('replication_type'), item_attr.get('journal_size')))

                    elif 'Asynchronous'.lower() == rp4vm_policy_item.policy_type.lower():
                        if rp4vm_policy_item.policy_type == item_attr.get('replication_type') and \
                                        str(rp4vm_policy_item.journal_size) == item_attr.get('journal_size') and \
                                        str(rp4vm_policy_item.rp_number) == item_attr.get('rpo_number') and \
                                        rp4vm_policy_item.rp_units == item_attr.get('rpo_units'):
                            rp4vm_policy_existed_dict['configuration'] = True
                            logger.debug('Same rp4vm policy name, also same configuration.')
                        else:
                            logger.warn('Same rp4vm policy name, but not same configuration,\nConfiguration of policy '
                                        'to be added: \nreplication_type: {}, journal_size: {}, rpo_number: {}, '
                                        'rpo_units: {}.\nConfiguration of policy existed: \n'
                                        'replication_type: {}, journal_size: {}, rpo_number: {}, rpo_units: {}.'.
                                format(
                                rp4vm_policy_item.policy_type, str(rp4vm_policy_item.journal_size),
                                str(rp4vm_policy_item.rp_number), rp4vm_policy_item.rp_units,
                                item_attr.get('replication_type'), item_attr.get('journal_size'),
                                item_attr.get('rpo_number'), item_attr.get('rpo_units')))
                    break

        return rp4vm_policy_existed_dict
