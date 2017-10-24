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
import os
import sys
import time
import random
from weakref import WeakSet
from urlparse import urlparse
from robot.api import logger
from robot.errors import ExecutionFailed
from ehc_e2e.entity import CloudStorageObject, WorkflowRelationMapping
from ehc_e2e.auc.executable.add_vcenter_relationship import AddVcenterRelationship
from ehc_e2e.auc.executable.arr_manager import (AddARR, DeleteARR, EditARR)
from ehc_e2e.auc.executable.assign_reservation_policy_to_blueprint import AssignReservationPolicyToBlueprint
from ehc_e2e.auc.executable.assign_datastores_and_rp_to_reservation import \
    AssignDatastoresAndReservationPolicyToReservation
from ehc_e2e.auc.executable.assign_reservation_policy_to_reservation import AssignReservationPolicyToReservation
from ehc_e2e.auc.executable.assign_storage_reservation_policy_to_blueprint import \
    AssignStorageReservationPolicyToBlueprint
from ehc_e2e.auc.executable.assign_rp_to_all_vsphere_blueprint import AssignRPtoAllvSphereBlueprint
from ehc_e2e.auc.executable.avamar_grid import (
    AddAvamarGrid, DeleteAvamarGrid, EditAdminFull, EditAvamarGrid)
from ehc_e2e.auc.executable.avamar_site_relationship import (
    AddAvamarSiteRelationship, DeleteAvamarSiteRelationship, EditAvamarSiteRelationship)
from ehc_e2e.auc.executable.backup_service_level_manager import (
    AddBackupServiceLevel, DeleteBackupServiceLevel, DisplayBackupServiceLevel)
from ehc_e2e.auc.executable.backup_service_level_manager import BackupServiceLevelManager
from ehc_e2e.auc.executable.clean_up import CleanUp
from ehc_e2e.auc.executable.close_browser import CloseBrowser
from ehc_e2e.auc.executable.cluster_manager import (
    AssociateAvamarProxiesWithCluster, ClusterManager)
from ehc_e2e.auc.executable.delete_datastore import DeleteDataStore
from ehc_e2e.auc.executable.delete_vcenter_relationship import DeleteVcenterRelationship
from ehc_e2e.auc.executable.deploy_multiple_vms import DeployMultipleVM
from ehc_e2e.auc.executable.deploy_vm import DeployVM, DeployVmParallel
from ehc_e2e.auc.executable.destroy_vms import DestroyVMs
from ehc_e2e.auc.executable.generic import RequestChecker
from ehc_e2e.auc.executable.get_arr_from_vro import GetARRFromvRO
from ehc_e2e.auc.executable.get_asr_from_vro import GetASRFromvRO as AUC_GetASRFromvRO
from ehc_e2e.auc.executable.get_backup_summary import GetBackupSummary
from ehc_e2e.auc.executable.get_datastore_from_vro import GetDatastoreFromvRO
from ehc_e2e.auc.executable.hwi import HwiManager
from ehc_e2e.auc.executable.launch_browser import LaunchBrowser
from ehc_e2e.auc.executable.login_to_vra import LoginTovRA
from ehc_e2e.auc.executable.logout_from_vra import LogoutFromvRA
from ehc_e2e.auc.executable.on_demand_backup_vm import OnDemandBackupVM
from ehc_e2e.auc.executable.on_demand_restore_vm import OnDemandRestoreVM, NoBackupPointFoundException
from ehc_e2e.auc.executable.operate_vm import OperateVM
from ehc_e2e.auc.executable.provision_cloud_storage import ProvisionCloudStorage
from ehc_e2e.auc.executable.remove_reservation_policy_from_blueprint import RemoveReservationPolicyFromBlueprint
from ehc_e2e.auc.executable.remove_reservation_policy_from_reservation import RemoveReservationPolicyFromReservation
from ehc_e2e.auc.executable.remove_rp_from_all_vsphere_blueprint import RemoveRPfromAllvSphereBlueprint
from ehc_e2e.auc.executable.reservation_manager import (CreateReservation, DeleteReservation)
from ehc_e2e.auc.executable.reservation_policy import (CreateReservationPolicy, DeleteReservationPolicy)
from ehc_e2e.auc.executable.run_admin_report import RunAdminReport
from ehc_e2e.auc.executable.set_backup_service_level import SetBackupServiceLevel
from ehc_e2e.auc.executable.site_manager import SiteManager
from ehc_e2e.auc.executable.vcenter_endpoint_maintenance import VCenterManager
from ehc_e2e.auc.executable.fabric_group import FabricGroup
from ehc_e2e.auc.executable.dump_context import DumpContext
from ehc_e2e.utils.context import DataContext
from ehc_e2e.utils.service import VraRestUtil
from ehc_e2e.auc.rest.get_datastore_from_vro import GetDatastoreFromvRO
from ehc_e2e.utils.service import VroItems
from ehc_e2e.setting import workflow_continue_on_failure, resume_also_include_workflow_yaml_file
from ehc_e2e.utils.context.model import YAMLData
from ehc_e2e.auc.executable.cluster_manager import ClusterManager
import ehc_e2e.constants.vro_vra_constants as vro_constants
import ehc_e2e.constants.ehc_constants as ehc_constants
from ehc_e2e.entity.bsl_configurations import BSLSchedule,BSLRetention
from ehc_e2e.constants.yaml_config_constants import ADD_AVAMAR_PROXY_CONFIG_ATTR_NAMES
from ehc_e2e.auc.executable.avamar_proxy_manager import AvamarProxyManager
from ehc_e2e.auc.rest.get_asr_from_vro import GetASRFromvRO as REST_GetASRFromvRO
from ehc_e2e.auc.executable.avamar_site_relationship import ASRManager
from ehc_e2e.auc.executable.avamar_site_relationship import AvamarSiteRelationshipInfo
from ehc_e2e.auc.executable.avamar_site_relationship.asr_helper import filter_latest_added_asr
from ehc_e2e.auc.executable.avamar_site_relationship.asr_constants import (backup_env_type_prefix_two_copies,
                                                                           backup_env_type_prefix_three_copies,
                                                                           backup_env_type_map,
                                                                           cluster_type_to_backup_env_type)


def catch_assert_exception(f):
    """
    Just used for handling assert error and raise ExecutionFailed to let workflow continue running.
    """

    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except AssertionError as ex:
            raise ExecutionFailed(ex.message, continue_on_failure=workflow_continue_on_failure)

    return func


def filter_config_file(config_files, file_name_string):
    if config_files:
        for item in config_files:
            if file_name_string in item.lower():
                return item

    return None


class BaseWorkflow(object):
    # Below is for tracking all instances of the class.
    # Both sub class and base class will keep tracking instances for base and sub class.
    # use weak reference here to keep the type as its original behavior, we don't need them last forever.
    weak_instances = WeakSet()
    YAML_KEY_TO_WORKFLOW_CONFIG_FILE = 'config_file_workflow'
    YAML_KEY_TO_GLOBAL_CONFIG_FILE = 'config_file_global'
    YAML_KEY_TO_MANDATORY_SECTION = 'mandatory'
    WORKFLOW_RELATION_LIST = 'workflow_relation_list'

    def __init__(self, ctx=None):
        self.__class__.weak_instances.add(self)
        self._GC_TAG = 'GC'
        self._WORKFLOW_TAG = 'WORKFLOW'

        if not ctx or not hasattr(ctx, self._GC_TAG):
            self.ctx = DataContext(None, self._GC_TAG)
            self.ctx.update_context(None, self._WORKFLOW_TAG)

        self.wf_context = getattr(self.ctx, self._WORKFLOW_TAG)
        self.gc_context = getattr(self.ctx, self._GC_TAG)

    def apply_settings_from_files(self, global_file, *workflow_files):
        assert os.path.isfile(global_file), '"{}" is not provided.'.format(global_file)
        config_files = []
        self.ctx.update_context(global_file, self._GC_TAG)
        config_files.append(global_file)
        for yaml_file in workflow_files:
            assert os.path.isfile(yaml_file), 'Workflow config file "{}" is not provided.'.format(yaml_file)
            self.ctx.update_context(yaml_file, self._WORKFLOW_TAG)
            config_files.append(yaml_file)

        # also update workflow context using global file since currently, we are using workflow config and global
        # config and combine them into workflow context.
        self.ctx.update_context(global_file, self._WORKFLOW_TAG)
        workflow_config = filter_config_file(config_files, 'e2ewf-')
        setattr(self.wf_context, self.__class__.YAML_KEY_TO_WORKFLOW_CONFIG_FILE, workflow_config)
        setattr(self.wf_context, self.__class__.YAML_KEY_TO_GLOBAL_CONFIG_FILE, global_file)

    @catch_assert_exception
    def apply_settings_from_dump(self, dump_file):
        import pickle
        assert os.path.isfile(dump_file), '"{}" is not provided.'.format(dump_file)
        try:
            with open(dump_file, 'rb') as dump_f:
                dump_context = pickle.load(dump_f)
                if resume_also_include_workflow_yaml_file is True:
                    logger.info('Use workflow yaml file to update mandatory keys in dump context.')
                    workflow_yaml_context = DataContext(None, 'DUMP_CONTEXT')
                    wf_yaml_file = getattr(
                        dump_context, self.__class__.YAML_KEY_TO_WORKFLOW_CONFIG_FILE, None)
                    gl_yaml_file = getattr(
                        dump_context, self.__class__.YAML_KEY_TO_GLOBAL_CONFIG_FILE, None)
                    assert wf_yaml_file, 'failed to get workflow yaml file path from dump file.'
                    assert gl_yaml_file, 'failed to get global yaml file path from dump file.'
                    workflow_yaml_context.update_context(wf_yaml_file, 'DUMP_CONTEXT')
                    workflow_yaml_context.update_context(gl_yaml_file, 'DUMP_CONTEXT')
                    assert getattr(
                        dump_context, self.__class__.YAML_KEY_TO_MANDATORY_SECTION, None) is not None, \
                        'dump content does not contain {} section'.format(
                            self.__class__.YAML_KEY_TO_MANDATORY_SECTION)
                    assert getattr(
                        workflow_yaml_context.DUMP_CONTEXT,
                        self.__class__.YAML_KEY_TO_MANDATORY_SECTION, None) is not None, \
                        'workflow yaml content does not contain {} section'.format(
                            self.__class__.YAML_KEY_TO_MANDATORY_SECTION)
                    from uiacore.modeling.webui.browser import Browser
                    update_exclusive_keys = ['added', 'existed', 'backup_service_levels']
                    self.data_context_attributes_compare_update(
                        dump_context, workflow_yaml_context.DUMP_CONTEXT, [Browser], update_exclusive_keys,
                        ['blueprint_machine_pairs'])
                    logger.info(
                        'Updated dump context object mandatory keys using workflow config:{}'.format(
                            wf_yaml_file))
                self.wf_context = dump_context
                setattr(self.wf_context.shared.current_browser, 'is_login', False)
                setattr(self.wf_context.shared.current_browser, 'current_user', None)
                setattr(self.wf_context.shared.current_browser, 'launched', False)
                logger.info('Reset flag of is_login and launched.', False, True)
        except IOError:
            logger.error('Opening dump file:{} encountered error:{}'.format(dump_file, sys.exc_info()))
            raise

    def data_context_attributes_compare_update(
            self, left_obj, right_obj, exclusive_types, exclusive_keys, force_to_use_right_keys):
        """
            method to do DataContext object comparison and attri value update.
            This method will do a DFS lookup for attributes within the given DataContext object. the node which is not
            of type YAMLDATA is considered leaf node.

            NOTE: This method uses recursive strategy so is possiblly case stack overflow issue when the object tree
            is too deep.

        :param left_obj: the DataContext object that will be updated.
        :param right_obj: the DataContext object whose value will be used for updating.
        :param exclusive_types: type list that will ignored for the update.
        :param exclusive_keys: list of keys that will not update.
        :param force_to_use_right_keys: keys in left object where method will not go deep for update and comparision.
                                        and will use right object's corresponding key value to update forcely.
        :return: True if all updates succeeds, False otherwise.
        """
        try:
            for k in left_obj.__dict__.keys():
                if any(exclusive_key in k.lower() for exclusive_key in exclusive_keys):
                    logger.debug('Key:{} is found in exclusive_keys, will not update for it.'.format(k))
                elif any(k.lower() in force_right_key for force_right_key in force_to_use_right_keys):
                    logger.info(
                        'Key:{} is specified to be forcely replaced with right object value:{}'.format(
                            k, right_obj[k]), False, True)
                    left_obj[k] = right_obj[k]
                else:
                    right_v = right_obj.__dict__.get(k, None)
                    left_v = left_obj.__dict__.get(k)
                    if isinstance(left_v, YAMLData) and right_v:
                        self.data_context_attributes_compare_update(
                            left_v, right_v, exclusive_types, exclusive_keys, force_to_use_right_keys)
                    else:
                        logger.debug('Context object compare updater found leaf item {}:{}'.format(k, left_v))

                        if any(isinstance(left_v, exclusive_type) for exclusive_type in exclusive_types):
                            logger.debug(
                                'Found leaf object different but no need to update:{}, type:{}'.format(k, type(left_v)))
                        if any(not isinstance(left_v, exclusive_type) for exclusive_type in exclusive_types)\
                            and left_v != right_v:
                            if getattr(right_obj, k, None) is not None:
                                left_obj[k] = right_obj[k]
                                logger.info('Updated different key:{}'.format(k), False, True)
                            else:
                                logger.debug(
                                    'No key:{} in right object:{}, will not update left object:{} for this item.'
                                    .format(k, right_obj, left_obj))
                        if left_v == right_v:
                            logger.debug('Equal object {}:{}, no update'.format(k, left_v))
        except:
            logger.warn('Encoutered error when doing datacontext object compare and update, error detail:{}'
                        .format(sys.exc_info()))
            return False

        return True

    def initialize_workflow_relation_mapping(self):
        workflow_relation_list = []
        if getattr(self.wf_context, 'workflow_relation_mappings', None):
            for key, relationship_mapping in self.wf_context.workflow_relation_mappings.__dict__.iteritems():
                workflow_relation_mapping = WorkflowRelationMapping(relationship_mapping['mapping_cluster_name'],
                                                                    relationship_mapping['mapping_reservation_name'],
                                                                    relationship_mapping['mapping_computer_resource'],
                                                                    relationship_mapping['mapping_network_path'],
                                                                    relationship_mapping['mapping_blueprint'],
                                                                    relationship_mapping['mapping_vsphere_machine_id'],
                                                                    relationship_mapping['mapping_reservation_policy_name'])
                workflow_relation_list.append(workflow_relation_mapping)
            setattr(self.wf_context, self.__class__.WORKFLOW_RELATION_LIST, workflow_relation_list)
            logger.info('[AUC] - "{}" - {}'.format(' '.join([word.capitalize() for word in
                                                             self.initialize_workflow_relation_mapping.
                                                            __name__.split('_')]), 'PASSED'), False, True)
        else:
            logger.info('[AUC] - "{}" - {}'.format(
                    ' '.join([word.capitalize()
                              for word in self.initialize_workflow_relation_mapping.__name__.split('_')]),
                    'FAILED'), False, True)
            raise AssertionError(
                'Error occurred when try to get workflow_relation_mappings, please make sure they are configured'
                ' properly in YAML file.')

    def clean_up_environment(self):
        try:
            CleanUp(
                name=self.clean_up_environment.__name__,
                ctx_in=self.wf_context,
                ctx_out=self.wf_context
            ).run()
        except:
            logger.warn('Failed to clean up chrome browser, please check the running processes manually!', True)

        try:
            DumpContext(
                name=self.clean_up_environment.__name__,
                ctx_in=self.wf_context,
                ctx_out=self.wf_context
            ).run()
        except:
            import traceback
            logger.warn('error:{}'.format(sys.exc_info()))
            logger.warn('trace:{}'.format(traceback.print_stack()))
            logger.warn(
                'Failed to generate the dump file due to some corrupt data in run time! resume workflow may not work!',
                True)

    def reset_settings(self):
        self.wf_context = None
        self.gc_context = None
        self.ctx = None

    def user_opens_browser(self, browser_type=None, base_url=None):
        self.cloud_administrator_opens_browser()

    def opens_browser_to_resume(self, browser_type=None, base_url=None):
        self.cloud_administrator_opens_browser()

    def cloud_administrator_opens_browser(self, browser_type=None, base_url=None):
        self.wf_context.launch_browser.browserType = (
            browser_type or self.wf_context.launch_browser.browserType)
        self.wf_context.launch_browser.baseUrl = (
            base_url or self.wf_context.launch_browser.baseUrl)
        if self.wf_context.shared.current_browser.launched:
            logger.info('Have already launch the browser. No need launch again.', False, True)
            return
        LaunchBrowser(
            self.cloud_administrator_opens_browser.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context,
        ).run()

    def _get_current_user_info(self):
        _current_user = getattr(self.wf_context.shared.current_browser, 'current_user', None)
        _users = getattr(self.wf_context, 'user_roles', YAMLData(**{}))

        if _current_user:
            for key, value in _users.__dict__.items():
                if value['username'] == _current_user:
                    kwargs = {
                        'username': _current_user,
                        'password': value['password'],
                        'domain': value['domain']
                    }
                    return kwargs
        return {}

    def _get_special_user_info(self, user_name_to_login):
        assert hasattr(self.wf_context.user_roles, user_name_to_login), \
            'Please provide account info about: {} for login.'.format(user_name_to_login)
        _user_info = getattr(self.wf_context.user_roles, user_name_to_login)
        kwargs = {
            'username': getattr(_user_info, 'username', None),
            'password': getattr(_user_info, 'password', None),
            'domain': getattr(_user_info, 'domain', None)
        }
        return kwargs

    @catch_assert_exception
    def _login_as_user(self, user_name_to_login):
        current_browser = self.wf_context.shared.current_browser
        _cur_user_info_dict = self._get_current_user_info()
        _special_user_info_dict = self._get_special_user_info(user_name_to_login)
        # if has logged in pre-steps by resume
        if _cur_user_info_dict:
            if _cur_user_info_dict['username'].strip() != _special_user_info_dict['username'].strip():
                logger.info('<{}> has already login to vRA, go to login as <{}>.'.format(
                    _cur_user_info_dict['username'], _special_user_info_dict['username']), False, True)
                kwargs = _special_user_info_dict
            else:
                logger.info('<{}> has logged, no need to login again'.format(_cur_user_info_dict['username']), False, True)
                return
        elif _cur_user_info_dict:
            logger.info('The current user is: {}, will use it to login'.format(_cur_user_info_dict['username']),
                        False, True)
            kwargs = _cur_user_info_dict
        else:
            kwargs = _special_user_info_dict

            logger.info('Current user is not set, will try to use {} to login'.format(kwargs['username']),
                        False, True)
        assert kwargs, 'Please provide user info to login in: {}'.format(user_name_to_login)
        kwargs['current_browser'] = current_browser
        LoginTovRA(
            self.cloud_administrator_login.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context.shared.current_browser,
            **kwargs
        ).run()

    def login_browser_to_resume(self):
        self._login_as_user('Config_Admin')

    def cloud_administrator_login(self):
        self._login_as_user('Config_Admin')

    def login_to_vra_as_config_admin(self):
        self._login_as_user('Config_Admin')

    def login_to_vra_as_backup_admin(self):
        self._login_as_user('Backup_Admin')

    def login_to_vra_as_storage_admin(self):
        self._login_as_user('Storage_Admin')

    def login_to_vra_as_tenant_bg_user(self):
        self._login_as_user('Tenant_BG_User')

    @catch_assert_exception
    def cloud_administrator_adds_vcenter(self):
        setattr(self.wf_context, 'added_vcenter', [])
        current_browser = self.wf_context.shared.current_browser
        add_vcenter = self.wf_context.add_vcenter
        method_name = VCenterManager.Func.ADD_VCENTER
        add_sites = self.wf_context.added_sites
        output = []
        add_vcenter_list = []
        if self.wf_context:
            assert current_browser is not None, 'current_browser in yaml is None, ' \
                                                'may be there is no active browser'
            assert current_browser.is_login, 'Please login to vRA, The flag value is_login is: False.'
            assert self.wf_context.onboard_cluster_type is not None, 'Please provide onboard cluster type.'
            assert self.wf_context.onboard_cluster_type in ['LC1S', 'VS1S', 'DR2S', 'CA1S', 'CA2S', 'MP2S', 'MP3S',
                                                            'LC2S', 'VS2S'], \
                "Onboard cluster type should be in [LC1S, 'VS1S', DR2S, CA1S, CA2S, MP2S, MP3S, LC2S, 'VS2S']"
            assert add_sites is not None and add_sites > 0, "yaml data of added_sites is None"
            for item in add_vcenter:
                for key, value in item.__dict__.iteritems():
                    assert value is not None, 'yaml data of "{}" value is None'.format(key)
        (vro_response_dict, vro_rest_base) = VroItems(
            self.wf_context).get_all_items_from_vro(vro_constants.VCENTER_API)
        for counter, item in enumerate(add_vcenter):
            kwargs = {
                'select_operation': item.select_operation,
                'name_for_vcenter_endpoint': item.name_for_vcenter_endpoint,
                'select_vc_fqdn_to_add': item.select_vc_fqdn_to_add,
                'new_vcenter_associated_sites': item.new_vcenter_associated_sites,
                'select_datacenter_to_add': item.select_datacenter_to_add,
                'current_browser': current_browser,
                'add_sites': add_sites,
                'add_vcenter': add_vcenter,
                'onboard_cluster_type': self.wf_context.onboard_cluster_type,
                'output': output,
            }
            # vcenter name and fqdn shold be unique
            vcenter_name_fqdn_existed_dict = self._check_vcenter_existence(item,
                                                                          vro_response_dict,
                                                                          vro_rest_base)
            if not vcenter_name_fqdn_existed_dict['name'] and \
                    not vcenter_name_fqdn_existed_dict['fqdn']:
                VCenterManager(self.cloud_administrator_adds_vcenter.__name__,
                               method_name=method_name,
                               **kwargs).run()

                # check the request
                request_result = []
                RequestChecker(
                    self.cloud_administrator_adds_vcenter.__name__,
                    description=method_name,
                    output=request_result
                ).run()

                if request_result and output:
                    if request_result[-1].status == 'Successful':
                        add_vcenter_list.append(output[-1])
                    else:
                        logger.error(
                            'The request status of add vcenter:{name} is: {status}, '
                            'The status details are: {status_detail}'.format(
                                name=request_result[-1].description, status=request_result[-1].status,
                                status_detail=request_result[-1].status_details))

            elif vcenter_name_fqdn_existed_dict['name'] and \
                    vcenter_name_fqdn_existed_dict['sites'] and \
                    vcenter_name_fqdn_existed_dict['fqdn']:
                add_vcenter_list.append(item.name_for_vcenter_endpoint)
                logger.info("vcenter: {0} with FQDN: {1} and sites: {2} doesnt need to add again, it already exists. "
                            "Put it in added_vcenter directly.".format(
                    item.name_for_vcenter_endpoint, item.select_vc_fqdn_to_add, item.new_vcenter_associated_sites))
            else:
                raise AssertionError("Vcenter doesnt exist yet, but still can't add."
                                     "Check if vcenter name: {0}, vcenter FQDN: {1}, sites: {2} "
                                     "are applied in other vcenters separately.".format(
                    item.name_for_vcenter_endpoint, item.select_vc_fqdn_to_add, item.new_vcenter_associated_sites))
        setattr(self.wf_context, 'added_vcenter', add_vcenter_list)
        logger.debug('Added vCenter: {}'.format(self.wf_context.added_vcenter))

    @catch_assert_exception
    def cloud_administrator_adds_hwi(self):
        assert self.wf_context.shared.current_browser.is_login is True, "can't do anything if you are not logged in"
        assert self.wf_context.add_hwi is not None, "the add_hwi in yaml file is None"
        onboard_cluster_type = self.wf_context.onboard_cluster_type
        assert onboard_cluster_type is not None, 'Please provide onboard cluster type.'
        for hwi in self.wf_context.add_hwi:
            for key, value in hwi.__dict__.iteritems():
                assert value is not None, \
                    'The {key} attribute of add_hwi in yaml file is None'.format(key=key)

        cluster_types = ehc_constants.CLUSTER_TYPES
        cluster_type = str(onboard_cluster_type).upper()

        required_sites, required_vcenters = (0, 0)
        if cluster_type in ('LC1S', 'VS1S', 'CA1S'):
            required_sites, required_vcenters = (1, 1)
        elif cluster_type in ('DR2S', 'MP2S', 'LC2S', 'VS2S'):
            required_sites, required_vcenters = (2, 2)
        elif cluster_type == 'CA2S':
            required_sites, required_vcenters = (2, 1)
        elif cluster_type == 'MP3S':
            required_sites, required_vcenters(3, 2)
        else:
            logger.debug("Cluster type should be one of the followed: {}".format(cluster_types))
            raise AssertionError("Cluster type should be one of the followed: {}".format(cluster_types))

        if len(self.wf_context.added_sites) != required_sites:
            raise AssertionError('At least {0} site(s) are required to support cluster type: {1}'
                                 .format(required_sites, cluster_type))
        if len(self.wf_context.added_vcenter) != required_vcenters:
            raise AssertionError('At least {0} vCenter(s) are required to support cluster type: {1}'
                                 .format(required_vcenters, cluster_type))

        cur_browser = self.wf_context.shared.current_browser
        output = []
        added_hwi = []
        (vro_response_dict, vro_rest_base) = VroItems(
            self.wf_context).get_all_items_from_vro(vro_constants.HARDWARE_ISLAND_API)
        for counter, item in enumerate(self.wf_context.add_hwi):
            kwargs = {
                'hwi_name': item.hwi_name,
                'performed_active': item.performed_active,
                'vcenter_name_active': item.vcenter_name_active,
                'site_name_active': item.site_name_active,
                'storage_type': item.storage_type,
                'vipr_active': item.vipr_active,
                'vipr_active_check': item.vipr_active_check,
                'added_vcenter': self.wf_context.added_vcenter,
                'added_sites': self.wf_context.added_sites,
                'onboard_cluster_type': onboard_cluster_type,
                'output': output
            }
            # hwi name and\or vipr array should be unique
            hwi_name_varray_existed_dict = self._check_hwi_existence(item,
                                                                    vro_response_dict,
                                                                    vro_rest_base)
            if not hwi_name_varray_existed_dict['name'] and \
                    not hwi_name_varray_existed_dict['varray']:
                HwiManager(
                    self.cloud_administrator_adds_hwi.__name__,
                    method_name=HwiManager.Func.ADD_HWI,
                    browser=cur_browser,
                    **kwargs
                ).run()

                request_result = []
                RequestChecker(
                    self.cloud_administrator_adds_hwi.__name__,
                    description=HwiManager.Func.ADD_HWI,
                    output=request_result
                ).run()

                if request_result and output:
                    if request_result[-1].status == 'Successful':
                        added_hwi.append(output[-1])
            elif hwi_name_varray_existed_dict['name'] and \
                hwi_name_varray_existed_dict['site'] and \
                    hwi_name_varray_existed_dict['vcenter']:
                if item.storage_type == 'VSAN':
                    added_hwi.append(item.hwi_name)
                    logger.info("hwi: {} already exists, doesn't need to add again, put it in added_hwi directly.".format(item.hwi_name))
                if item.storage_type == 'BLOCK':
                    if hwi_name_varray_existed_dict['varray']:
                        added_hwi.append(item.hwi_name)
                        logger.info("hwi: {0} with varray: {1} already exists, doesn't need to add again, "
                                    "put it in added_hwi directly.".format(item.hwi_name, item.vipr_active_check))
                    else:
                        raise AssertionError("HWI doesnt exist but cannot be added either."
                                             "Check if hwi name: {0}, varray: {1}, site:{2}, vcenter:{3} are applied in other HWIs separately."
                                             .format(item.hwi_name, item.vipr_active_check, item.site_name_active,
                                                     item.vcenter_name_active))
            else:
                raise AssertionError("HWI doesnt exist but cannot be added either."
                                     "Check if hwi name: {0}, varray: {1}, site:{2}, vcenter:{3} are applied in other HWIs separately."
                    .format(item.hwi_name, item.vipr_active_check, item.site_name_active, item.vcenter_name_active))

        setattr(self.wf_context, 'added_hwi', added_hwi)
        logger.info('Added hwi: {}'.format(self.wf_context.added_hwi))

    @catch_assert_exception
    def cloud_administrator_adds_site(self):
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login
        add_sites_context = self.wf_context.add_sites
        onboard_cluster_type = self.wf_context.onboard_cluster_type
        len_add_sites = len(add_sites_context)
        setattr(self.wf_context, 'added_sites', [])

        assert onboard_cluster_type is not None, 'Please provide onboard cluster type.'
        cluster_type_list = ehc_constants.CLUSTER_TYPES
        assert onboard_cluster_type in cluster_type_list, \
            "Onboard cluster type should be in {0}.".format(cluster_type_list)

        if onboard_cluster_type in ('LC1S', 'VS1S', 'CA1S'):
            site_num = 1
        elif onboard_cluster_type in ('DR2S', 'CA2S', 'MP2S', 'LC2S', 'VS2S'):
            site_num = 2
        else:
            site_num = 3

        assert len_add_sites >= site_num, \
            'Need to provide {0} sites data for cluster type: {}.'.format(site_num, onboard_cluster_type)
        if len_add_sites > site_num:
            logger.warn(msg='Only need {0} sites, you provided {1} sites info, '
                            'add the first three sites by default.'.format(site_num, len_add_sites))

        add_sites = add_sites_context[:site_num]
        output = []
        added_sites = []
        (vro_response_dict, vro_rest_base) = VroItems(
            self.wf_context).get_all_items_from_vro(vro_constants.SITE_API)
        for site_name in add_sites:
            description = 'add site {0}'.format(site_name)
            kwargs = {
                'current_browser': current_browser,
                'is_login': is_login,
                'site_name': site_name,
                'description': description,
                'output': output
            }
            # site name should be unique

            if self._site_is_able_to_add(site_name, vro_response_dict, vro_rest_base):
                SiteManager(
                    self.cloud_administrator_adds_site.__name__,
                    method_name=SiteManager.Func.ADD_SITES,
                    **kwargs
                ).run()

                request_result = []
                RequestChecker(
                    self.cloud_administrator_adds_site.__name__,
                    description=description,
                    ignore_failure=True,
                    output=request_result
                ).run()

                if request_result and output:
                    if request_result[-1].status == 'Successful':
                        added_sites.append(output[-1])

            else:
                added_sites.append(site_name)
        setattr(self.wf_context, 'added_sites', added_sites)
        logger.info('Added Sites: {}'.format(self.wf_context.added_sites))

    @catch_assert_exception
    def cloud_administrator_deletes_cluster(self):
        cur_browser = self.wf_context.shared.current_browser
        _clusters = []
        if hasattr(self.wf_context, 'delete_cluster') and len(self.wf_context.delete_cluster) > 0:
            _clusters = self.wf_context.delete_cluster
        elif hasattr(self.wf_context, 'existed_clusters') and len(self.wf_context.existed_clusters) > 0:
            _clusters = self.wf_context.existed_clusters
        else:
            logger.info('No clusters need to delete.', False, True)
            logger.info('[AUC] - "{}" - {}'.format(' '.join([word.capitalize() for word in
                                                             self.cloud_administrator_deletes_cluster.__name__.split(
                                                                 '_')]),
                                                   'PASSED'), False, True)
        for cluster in _clusters:
            kwargs = {
                'current_browser': cur_browser,
                'delete_cluster': cluster
            }
            (vro_response_dict, vro_rest_base) = VroItems(
                self.wf_context).get_all_items_from_vro(vro_constants.CLUSTER_API)
            if self._cluster_is_onboarded(cluster, vro_response_dict, vro_rest_base):
                ClusterManager(
                    self.cloud_administrator_deletes_cluster.__name__,
                    method_name=ClusterManager.Func.DELETE_CLUSTER,
                    browser=cur_browser, **kwargs) \
                    .run()

                RequestChecker(self.cloud_administrator_deletes_cluster.__name__,
                               description=ClusterManager.Func.DELETE_CLUSTER).run()

    def _site_is_able_to_add(self, site_name, vro_response_dict, vro_rest_base):
        """

        Args:
            site_name: site name to add (STRING)
            vro_response_dict: vro request response dict(dict)
            vro_rest_base: VRORestBase Object(Object)

        Returns: True or False

        """
        if vro_response_dict:
            for item in vro_response_dict.get('relations', {}).get('link', []):
                item_attr = vro_rest_base.name_value_pairs_to_dict(item.get('attributes', {}))
                if site_name == item_attr.get('name'):
                    logger.info("Site name: {} already exist, doesn't need to add again.".format(site_name))
                    return False

            logger.info("Site name:{0} is able to add".format(site_name))
            return True
        else:
            return False


    def _check_vcenter_existence(self,
                                vcenter_item,
                                vro_response_dict,
                                vro_rest_base):
        """

        Args:
            vcenter_item: vcenter input parameters object(Object)
            vro_response_dict: vro request response dict(dict)
            vro_rest_base: VRORestBase Object(Object)

        Returns: vcenter_name_fqdn_existed_dict(dict)

        """
        vcenter_name_fqdn_existed_dict = dict(name=False, sites=False, fqdn=False)
        if vro_response_dict:
            for item in vro_response_dict.get('relations', {}).get('link', []):
                item_attr = vro_rest_base.name_value_pairs_to_dict(item.get('attributes', {}))
                vcenter_name_fqdn_existed_dict = dict(name=False, sites=False, fqdn=False)
                if item_attr:
                    if vcenter_item.name_for_vcenter_endpoint == item_attr.get('name'):
                        vcenter_name_fqdn_existed_dict['name'] = True
                        logger.info("vcenter name: {0} is already in use.".format(vcenter_item.name_for_vcenter_endpoint))
                    if vcenter_item.select_vc_fqdn_to_add == item_attr.get('fqdn'):
                        vcenter_name_fqdn_existed_dict['fqdn'] = True
                        logger.info("FQDN: {0} is already in use by vCenter: {1}.".format(
                            vcenter_item.select_vc_fqdn_to_add, item_attr.get('name')), False, True)

                    if item_attr.get('sites'):
                        for index, site in enumerate(vcenter_item.new_vcenter_associated_sites):
                            if site not in item_attr.get('sites'):
                                break
                            if index == len(vcenter_item.new_vcenter_associated_sites) - 1:
                                vcenter_name_fqdn_existed_dict['sites'] = True
                                logger.info("Sites: {} to associate for vcenter are already in use.".format(
                                    vcenter_item.new_vcenter_associated_sites))
                # If the vcenter's name or fqdn is occupied, end the loop
                if vcenter_name_fqdn_existed_dict['name'] or vcenter_name_fqdn_existed_dict['fqdn']:
                    break
        return vcenter_name_fqdn_existed_dict

    def vcenter_relationship_with_same_name_exists(self):
        added_vcenter_name_list = self.wf_context.added_vcenter
        partner_vcenter_name_list = []
        added_vcenter_relationship = getattr(self.wf_context, 'added_vcenter_relationship', [])
        if not added_vcenter_relationship:
            raise AssertionError("Please provide vCenter relationship info your used.")
        (vro_response_dict, vro_rest_base) = VroItems(
            self.wf_context).get_all_items_from_vro(vro_constants.VCENTER_API)
        if vro_response_dict:
            for item in vro_response_dict.get('relations', {}).get('link', []):
                item_attr = vro_rest_base.name_value_pairs_to_dict(item.get('attributes', {}))
                if item_attr:
                    current_vcenter_name = item_attr.get('name')
                    partner_vcenter = item_attr.get('dr_partner_name')
                    vcenter_designation = item_attr.get('dr_designation')
                    if partner_vcenter is not None:
                        if ((vcenter_designation == u'Protected' and
                                        added_vcenter_relationship[0]['protected_vcenter'] == current_vcenter_name )
                            or
                                (vcenter_designation == u'Recovery' and
                                        added_vcenter_relationship[0]['recovery_vcenter'] == current_vcenter_name)):

                            partner_vcenter_name_list.append(partner_vcenter)
                            logger.info("vCenter: {0} is now :{1}".format(current_vcenter_name, vcenter_designation))

        if len(added_vcenter_name_list) > 1 and len(partner_vcenter_name_list) > 1 and \
                        set(added_vcenter_name_list) == set(partner_vcenter_name_list):
            logger.info("vCenters: {} are paired already.".format(added_vcenter_name_list))
            logger.info(
                '[AUC] - "{}" - {}'.format(
                    ' '.join([word.capitalize() for word in
                              self.vcenter_relationship_with_same_name_exists.__name__.split('_')]), 'PASSED'),
                False, True)

        else:
            logger.error("vCenters: {} are not paired yet, please add vcenter relationship for them manually first."
                        .format(added_vcenter_name_list))
            logger.info('[AUC] - "{}" - {}'.format(
                ' '.join([word.capitalize()
                          for word in self.vcenter_relationship_with_same_name_exists.__name__.split('_')]),
                'FAILED'), html=False, also_console=True)
            raise AssertionError("vCenters: {} are not paired yet, please add vcenter relationship for them manually first."
                        .format(added_vcenter_name_list))

    def vcenter_with_same_name_exists(self):
        add_vcenter = self.wf_context.added_vcenter
        for vcenter_name in add_vcenter:
            if not VroItems(self.wf_context).get_specific_item_by_name_from_vro\
                        (vcenter_name, vro_constants.VCENTER_API):
                logger.info('[AUC] - "{}" - {}'.format(
                    ' '.join([word.capitalize()
                              for word in self.vcenter_with_same_name_exists.__name__.split('_')]),
                    'FAILED'), html=False, also_console=True)
                raise AssertionError(
                    'Error occurred when try to get vcenter(s) by name from vro.')
        else:
            logger.info('[AUC] - "{}" - {}'.format(' '.join([word.capitalize() for word in
                                                             self.vcenter_with_same_name_exists.
                                                            __name__.split('_')]), 'PASSED'), False, True)


    def site_with_same_name_exists(self):
        add_site = self.wf_context.added_sites
        for site_name in add_site:
            if not VroItems(self.wf_context).get_specific_item_by_name_from_vro\
                        (site_name, vro_constants.SITE_API):
                logger.info('[AUC] - "{}" - {}'.format(
                    ' '.join([word.capitalize()
                              for word in self.site_with_same_name_exists.__name__.split('_')]),
                    'FAILED'), html=False, also_console=True)
                raise AssertionError(
                    'Error occurred when try to get site(s) by name from vro.')
        else:
            logger.info('[AUC] - "{}" - {}'.format(' '.join([word.capitalize() for word in
                                                             self.site_with_same_name_exists.
                                                            __name__.split('_')]), 'PASSED'), False, True)

    def hwi_with_same_name_exists(self):
        added_hwi = self.wf_context.added_hwi
        for hwi_name in added_hwi:
            if not VroItems(self.wf_context).get_specific_item_by_name_from_vro\
                        (hwi_name, vro_constants.HARDWARE_ISLAND_API):
                logger.info('[AUC] - "{}" - {}'.format(
                    ' '.join([word.capitalize()
                              for word in self.hwi_with_same_name_exists.__name__.split('_')]),
                    'FAILED'), html=False, also_console=True)
                raise AssertionError(
                    'Error occurred when try to get vcenter(s) by name from vro.')
        else:
            logger.info('[AUC] - "{}" - {}'.format(' '.join([word.capitalize() for word in
                                                             self.hwi_with_same_name_exists.
                                                            __name__.split('_')]), 'PASSED'), False, True)

    def _check_hwi_existence(self, hwi_item, vro_response_dict, vro_rest_base):
        """

        Args:
            hwi_item:  hwi item to add(Object)
            vro_response_dict: vro request response dict(dict)
            vro_rest_base: vro_rest_base: VRORestBase Object(Object)
        Returns: hwi_name_varray_existed_dict(dict)

        """
        hwi_name_varray_existed_dict = dict(name=False, site=False, vcenter=False, varray=False)
        for item in vro_response_dict.get('relations', {}).get('link', []):
            item_attr = vro_rest_base.name_value_pairs_to_dict(item.get('attributes', {}))
            hwi_name_varray_existed_dict = dict(name=False, site=False, vcenter=False, varray=False)
            if item_attr:
                if hwi_item.hwi_name == item_attr.get('name'):
                    hwi_name_varray_existed_dict['name'] = True
                    logger.info("hwi name {0} is already in use.".format(hwi_item.hwi_name))
                if hwi_item.site_name_active == item_attr.get('site') :
                    hwi_name_varray_existed_dict['site'] = True
                    logger.info("Site {0} is already in use.".format(hwi_item.site_name_active))
                if hwi_item.vcenter_name_active == item_attr.get('vcenter'):
                    hwi_name_varray_existed_dict['vcenter'] = True
                    logger.info("vcenter {0} is already in use.".format(hwi_item.vcenter_name_active))

                if hwi_item.storage_type == 'BLOCK' and item_attr.get('varrays'):  # already have hwi existed in vro
                    for index, varray in enumerate(hwi_item.vipr_active_check):
                        if varray not in item_attr.get('varrays'):
                            break
                        if index == len(hwi_item.vipr_active_check)-1:
                            logger.debug("varray: {0} already in use, can not be applied again."
                                         .format(hwi_item.vipr_active_check))
                            hwi_name_varray_existed_dict['varray'] = True

            # if the hwi'name, and \ or varray is occupied, end the loop
            if hwi_item.storage_type == 'BLOCK':
                if hwi_name_varray_existed_dict['name'] or \
                        hwi_name_varray_existed_dict['varray']:
                    break
            if hwi_item.storage_type == 'VSAN':
                if hwi_name_varray_existed_dict['name']:
                    break
        return hwi_name_varray_existed_dict

    @catch_assert_exception
    def _cluster_is_onboarded(self, cluster_name, vro_response_dict, vro_rest_base):
        """

        Args:
            site_name: site name to add (STRING)
            vro_response_dict: vro request response dict(dict)
            vro_rest_base: VRORestBase Object(Object)

        Returns: True or False

        """
        try:
            for item in vro_response_dict.get('relations', {}).get('link', []):
                item_attr = vro_rest_base.name_value_pairs_to_dict(item.get('attributes', {}))
                if cluster_name == item_attr.get('name'):
                    logger.debug("Cluster: {} is onboarded, need to delete.".format(cluster_name))
                    return True

            logger.debug("Cluster: {} has been deleted.".format(cluster_name))
            return False
        except Exception as e:
            raise AssertionError("Exception: {} occurs in _cluster_is_onboarded.".format(e))

    def validate_sites_vcenters_count_for_hwi(self, cluster_type):

        cluster_types = ehc_constants.CLUSTER_TYPES

        assert cluster_type in cluster_types, 'The {} is unspecified.'.format(cluster_type)

        if cluster_type in ('LC1S', 'VS1S', 'CA1S'):
            required_sites, required_vcenters = 1, 1
        else:
            required_sites = 3 if cluster_type == 'MP3S' else 2
            required_vcenters = 1 if cluster_type == 'CA2S' else 2

        assert len(self.wf_context.added_sites) == required_sites, \
            'At least {} site(s) are required'.format(required_sites)

        assert len(self.wf_context.added_vcenter) == required_vcenters, \
            'At least {} vCenter(s) are required'.format(required_vcenters)

    def cloud_administrator_adds_an_avamar_replication_relationship(self):
        AddARR(
            self.cloud_administrator_adds_an_avamar_replication_relationship.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_edits_an_avamar_replication_relationship(self):
        EditARR(
            self.cloud_administrator_edits_an_avamar_replication_relationship.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_deletes_an_avamar_replication_relationship(self):
        DeleteARR(
            self.cloud_administrator_deletes_an_avamar_replication_relationship.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    @catch_assert_exception
    def cloud_administrator_on_demand_backup_vm(self):
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login

        assert (hasattr(self.wf_context, 'deployed_vms') and
                self.wf_context.deployed_vms and
                len(self.wf_context.deployed_vms) >= 1), 'Number of VMs to be deployed should be greater than 0.'
        _deployed_vm = self.wf_context.deployed_vms[-1]
        _method_name = self.cloud_administrator_on_demand_backup_vm.__name__
        kwargs = {
            'current_browser': current_browser,
            'is_login': is_login,
            'description': _method_name,
            'vm_name': _deployed_vm,
        }
        OnDemandBackupVM(
            self.cloud_administrator_on_demand_backup_vm.__name__,
            **kwargs
        ).run()

        RequestChecker(
            self.cloud_administrator_on_demand_backup_vm.__name__,
            description=_method_name
        ).run()

    @catch_assert_exception
    def cloud_administrator_on_demand_backup_vm_b(self):
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login

        assert (hasattr(self.wf_context, 'dp_vms') and
                self.wf_context.dp_vms and
                len(self.wf_context.dp_vms) >= 1), 'Number of DP-protected VMs should be greater than 0.'
        _deployed_vm = self.wf_context.dp_vms[-1]
        _method_name = self.cloud_administrator_on_demand_backup_vm_b.__name__
        kwargs = {
            'current_browser': current_browser,
            'is_login': is_login,
            'description': _method_name,
            'vm_name': _deployed_vm,
        }
        OnDemandBackupVM(
            self.cloud_administrator_on_demand_backup_vm_b.__name__,
            **kwargs
        ).run()

        RequestChecker(
            self.cloud_administrator_on_demand_backup_vm_b.__name__,
            description=_method_name
        ).run()

    @catch_assert_exception
    def cloud_administrator_on_demand_backup_for_all_vms(self):
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login

        assert (hasattr(self.wf_context, 'deployed_vms') and
                self.wf_context.deployed_vms and
                len(self.wf_context.deployed_vms) >= 1), 'Number of VMs to be deployed should be greater than 0.'
        _method_name = self.cloud_administrator_on_demand_backup_vm.__name__
        for _deployed_vm in self.wf_context.deployed_vms:
            logger.info('Start to on demand backup in VM: {}'.format(_deployed_vm))
            description = 'test_on_demand_backup_for_vm ' + _deployed_vm
            kwargs = {
                'current_browser': current_browser,
                'is_login': is_login,
                'description': description,
                'vm_name': _deployed_vm,
            }
            OnDemandBackupVM(
                _method_name,
                **kwargs
            ).run()

            RequestChecker(
                self.cloud_administrator_on_demand_backup_vm.__name__,
                description=description
            ).run()

    @catch_assert_exception
    def cloud_administrator_on_demand_restore_for_all_vms(self):

        # if you want to power off the target vm, you can use operate_vm like this.
        # And in yaml you should add keywords user_action_list and value 'Power Off' below operate_vm.
        # =======================================================
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login

        assert (hasattr(self.wf_context, 'deployed_vms') and
                self.wf_context.deployed_vms and
                len(self.wf_context.deployed_vms) >= 1), 'Number of VMs to be deployed should be greater than 0.'
        assert (hasattr(self.wf_context, 'operate_vm') and
                hasattr(self.wf_context.operate_vm, 'user_action_list')), \
            'The user_action_list does not exist in yaml.'
        _user_action_list = self.wf_context.operate_vm.user_action_list
        for _deployed_vm in self.wf_context.deployed_vms:
            logger.info('Start to on demand restore in VM: {}'.format(_deployed_vm))
            kwargs = {
                'current_browser': current_browser,
                'is_login': is_login,
                'vm_name': _deployed_vm,
                'user_action_list': _user_action_list
            }
            OperateVM(
                self.cloud_administrator_operates_vm.__name__,
                **kwargs
            ).run()
            # =======================================================
            description_test_restore = 'test_on_demand_restore_for_vm ' + _deployed_vm
            import time
            waiting_timeout = 60 * 15
            logger.info('Start to check whether backup-point display and submit request of on demand restore '
                        'in {} seconds'.format(waiting_timeout), False, True)
            method_name = self.cloud_administrator_on_demand_restore_for_all_vms.__name__
            keyword_name = ' '.join([item.capitalize() for item in method_name.split('_')])
            while waiting_timeout > 0:
                try:
                    kwargs_restore = {
                        'current_browser': current_browser,
                        'is_login': is_login,
                        'description': description_test_restore,
                        'vm_name': _deployed_vm,
                        'wait_in_workflow': True
                    }
                    OnDemandRestoreVM(
                        method_name,
                        **kwargs_restore
                    ).run()
                    break

                except NoBackupPointFoundException:
                    logger.debug('Checking backup-point, still empty.')
                    snap = 10
                    time.sleep(snap)
                    waiting_timeout -= snap
                except:
                    assert False, '{0} - Failed, detail info: {1}'.format(keyword_name, sys.exc_info())

            assert waiting_timeout > 0, '{0} - Failed, There is no backup-point.'.format(keyword_name)
            RequestChecker(method_name,
                           description=description_test_restore).run()

    @catch_assert_exception
    def cloud_administrator_on_demand_restore_vm(self):

        # if you want to power off the target vm, you can use operate_vm like this.
        # And in yaml you should add keywords user_action_list and value 'Power Off' below operate_vm.
        # =======================================================
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login

        assert (hasattr(self.wf_context, 'deployed_vms') and
                self.wf_context.deployed_vms and
                len(self.wf_context.deployed_vms) >= 1), 'Number of VMs to be deployed should be greater than 0.'
        assert (hasattr(self.wf_context, 'operate_vm') and
                hasattr(self.wf_context.operate_vm, 'user_action_list')), \
            'The user_action_list does not exist in yaml.'
        _user_action_list = self.wf_context.operate_vm.user_action_list
        _deployed_vm = self.wf_context.deployed_vms[-1]

        kwargs = {
            'current_browser': current_browser,
            'is_login': is_login,
            'vm_name': _deployed_vm,
            'user_action_list': _user_action_list
        }
        OperateVM(
            self.cloud_administrator_operates_vm.__name__,
            **kwargs
        ).run()
        # =======================================================
        import time
        waiting_timeout = 60 * 15
        logger.info('Start to check whether backup-point display and submit request of on demand restore '
                    'in {} seconds'.format(waiting_timeout), False, True)
        method_name = self.cloud_administrator_on_demand_restore_vm.__name__
        keyword_name = ' '.join([item.capitalize() for item in method_name.split('_')])
        while waiting_timeout > 0:
            try:
                kwargs_restore = {
                    'current_browser': current_browser,
                    'is_login': is_login,
                    'description': method_name,
                    'vm_name': _deployed_vm,
                    'wait_in_workflow': True
                }
                OnDemandRestoreVM(
                    method_name,
                    **kwargs_restore
                ).run()
                break
            except NoBackupPointFoundException:
                logger.debug('Checking backup-point, still empty.')
                snap = 60
                time.sleep(snap)
                waiting_timeout -= snap
            except:
                assert False, '{0} - Failed, detail info: {1}'.format(keyword_name, sys.exc_info())
        assert waiting_timeout > 0, '{0} - Failed, There is no backup-point.'.format(keyword_name)
        RequestChecker(method_name,
                       description=method_name).run()

    @catch_assert_exception
    def cloud_administrator_on_demand_restore_vm_b(self):

        # if you want to power off the target vm, you can use operate_vm like this.
        # And in yaml you should add keywords user_action_list and value 'Power Off' below operate_vm.
        # =======================================================
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login

        assert (hasattr(self.wf_context, 'dp_vms') and
                self.wf_context.dp_vms and
                len(self.wf_context.dp_vms) >= 1), 'Number of VMs to be deployed should be greater than 0.'
        assert (hasattr(self.wf_context, 'operate_vm') and
                hasattr(self.wf_context.operate_vm, 'user_action_list')), \
            'The user_action_list does not exist in yaml.'
        _user_action_list = self.wf_context.operate_vm.user_action_list
        _deployed_vm = self.wf_context.dp_vms[-1]

        kwargs = {
            'current_browser': current_browser,
            'is_login': is_login,
            'vm_name': _deployed_vm,
            'user_action_list': _user_action_list
        }
        OperateVM(
            self.cloud_administrator_operates_vm.__name__,
            **kwargs
        ).run()
        # =======================================================
        import time
        waiting_timeout = 60 * 15
        logger.info('Start to check whether backup-point display and submit request of on demand restore '
                    'in {} seconds'.format(waiting_timeout), False, True)
        method_name = self.cloud_administrator_on_demand_restore_vm_b.__name__
        keyword_name = ' '.join([item.capitalize() for item in method_name.split('_')])
        while waiting_timeout > 0:
            try:
                kwargs_restore = {
                    'current_browser': current_browser,
                    'is_login': is_login,
                    'description': method_name,
                    'vm_name': _deployed_vm,
                    'wait_in_workflow': True
                }
                OnDemandRestoreVM(
                    method_name,
                    **kwargs_restore
                ).run()
                break
            except NoBackupPointFoundException:
                logger.debug('Checking backup-point, still empty, timeout: {}'.format(waiting_timeout))
                snap = 10
                time.sleep(snap)
                waiting_timeout -= snap
            except:
                assert False, '{0} - Failed, detail info: {1}'.format(keyword_name, sys.exc_info())
        assert waiting_timeout > 0, '{0} - Failed, There is no backup-point.'.format(keyword_name)
        RequestChecker(method_name,
                       description=method_name).run()

    @catch_assert_exception
    def cloud_administrator_operates_vm(self):
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login

        assert (hasattr(self.wf_context, 'deployed_vms') and
                self.wf_context.deployed_vms and
                len(self.wf_context.deployed_vms) >= 1), 'Number of deployed VMs should be greater than 0.'
        assert (hasattr(self.wf_context, 'operate_vm') and
                hasattr(self.wf_context.operate_vm, 'basic_action_list')), \
            'The basic_action_list does not exist in yaml.'
        _basic_action_list = self.wf_context.operate_vm.basic_action_list
        assert 'Power On' in _basic_action_list, \
            'Power On must be listed in basic_action_list.'
        assert 'Power Off' in _basic_action_list, \
            'Power Off must be listed in basic_action_list.'
        assert 'Reboot' in _basic_action_list, 'Reboot must be listed in basic_action_list.'
        assert len(_basic_action_list) == 3, \
            "The basic_action_list should be only covered by Power On, Power Off and Reboot. "

        _deployed_vm = self.wf_context.deployed_vms[0]
        kwargs = {
            'current_browser': current_browser,
            'is_login': is_login,
            'vm_name': _deployed_vm,
        }
        OperateVM(
            self.cloud_administrator_operates_vm.__name__,
            **kwargs
        ).run()

    @catch_assert_exception
    def cloud_administrator_operates_vm_b(self):
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login

        assert (hasattr(self.wf_context, 'deployed_vms') and
                self.wf_context.deployed_vms and
                len(self.wf_context.deployed_vms) >= 1), 'Number of deployed VMs should be greater than 0.'
        assert (hasattr(self.wf_context, 'operate_vm') and
                hasattr(self.wf_context.operate_vm, 'basic_action_list')), \
            'The basic_action_list does not exist in yaml.'
        _basic_action_list = self.wf_context.operate_vm.basic_action_list
        assert 'Power On' in _basic_action_list, \
            'Power On must be listed in basic_action_list.'
        assert 'Power Off' in _basic_action_list, \
            'Power Off must be listed in basic_action_list.'
        assert 'Reboot' in _basic_action_list, 'Reboot must be listed in basic_action_list.'
        assert len(_basic_action_list) == 3, \
            "The basic_action_list should be only covered by Power On, Power Off and Reboot. "

        for _deployed_vm in self.wf_context.deployed_vms:
            kwargs = {
                'current_browser': current_browser,
                'is_login': is_login,
                'vm_name': _deployed_vm,
            }
            OperateVM(
                self.cloud_administrator_operates_vm_b.__name__,
                **kwargs
            ).run()

    @catch_assert_exception
    def cloud_administrator_deletes_hwi(self):
        cur_browser = self.wf_context.shared.current_browser
        output = []
        for item in self.wf_context.added_hwi:
            kwargs = {
                'del_performed_active': self.wf_context.delete_hwi.del_performed_active,
                'isdel_obj': self.wf_context.delete_hwi.isdel_obj,
                'hwi_name': item,
                'output': output

            }
            HwiManager(
                self.cloud_administrator_deletes_hwi.__name__,
                method_name=HwiManager.Func.DELETE_HWI,
                browser=cur_browser,
                **kwargs
            ).run()

            RequestChecker(self.cloud_administrator_deletes_hwi.__name__,
                           description=HwiManager.Func.DELETE_HWI).run()

    @catch_assert_exception
    def cloud_administrator_edits_hwi(self):

        assert self.wf_context.shared.current_browser.is_login is True, "can't do anything if you are not logged in"
        assert self.wf_context.update_hwi is not None, "No update_hwi entry in yaml file"
        cur_browser = self.wf_context.shared.current_browser
        output = []
        added_hwi_list = []
        for counter, item in enumerate(self.wf_context.update_hwi):
            kwargs = {
                'old_hwi_name': item.old_hwi_name,
                'edit_hwi_name': item.edit_hwi_name,
                'performed_active': item.performed_active,
                'edit_vipr_active': item.vipr_active,
                'edit_vipr_active_check': item.vipr_active_check,
                'edit_vcenter_name_active': item.edit_vcenter_name_active,
                'edit_site_name_active': item.edit_site_name_active,
                'output': output

            }
            HwiManager(
                self.cloud_administrator_edits_hwi.__name__,
                method_name=HwiManager.Func.UPDATE_HWI,
                browser=cur_browser,
                **kwargs
            ).run()

            request_result = []
            RequestChecker(
                self.cloud_administrator_edits_hwi.__name__,
                description=HwiManager.Func.UPDATE_HWI,
                output=request_result
            ).run()

            if request_result and output:
                if request_result[-1].status == 'Successful':
                    added_hwi_list.append(output[counter])
        for counter, item in enumerate(self.wf_context.update_hwi):
            if item.old_hwi_name in self.wf_context.added_hwi and item.edit_hwi_name in added_hwi_list:
                self.wf_context.added_hwi[counter] = item.edit_hwi_name

        setattr(self.wf_context, 'added_hwi', self.wf_context.added_hwi)

    def cloud_administrator_assigns_reservation_policy_to_reservation(self):
        AssignReservationPolicyToReservation(
            self.cloud_administrator_assigns_reservation_policy_to_reservation.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_assigns_datastores_and_reservation_policy_to_reservation(self):
        assert hasattr(self.wf_context, 'added_reservation_policy'), \
            'added_reservation_policy name should be in context object'
        tenant_name = self.wf_context.vra.tenant
        assert tenant_name is not None, 'Please provide tenant.'
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login
        assert is_login is True, "Can't do anything if you didn't login."
        list_storage_names = []
        protected_storage_names = []
        recovery_storage_names = []
        list_reservations_assigned_reservation_policy = []
        list_storages = []
        output = []
        assert isinstance(self.wf_context.existed_clusters, list), 'Existed cluster is not list type.'
        assert len(self.wf_context.existed_clusters) > 0, 'Existed cluster is not provided.'
        list_cluster = self.wf_context.existed_clusters
        added_cloud_storage_list = self.wf_context.added_cloud_storage
        assert isinstance(added_cloud_storage_list, list), \
            'Added cloud storage is not list type.'
        assert len(added_cloud_storage_list) > 0, \
            'Target datastore(s) is not provided.'
        for storage in added_cloud_storage_list:
            assert storage.name, 'Storage name should not be None.'
            assert storage.cluster_name, 'Cluster name of storage should not be None.'
            if len(list_cluster) == 1:
                list_storage_names.append(storage.name[0])
            elif len(list_cluster) == 2:
                if storage.cluster_name == list_cluster[0]:
                    protected_storage_names.append(storage.name[0])
                else:
                    recovery_storage_names.append(storage.name[0])
            else:
                raise AssertionError('Can not support more than 2 cluster.')
        if list_storage_names:
            list_storages.append(list_storage_names)
        else:
            list_storages.append(protected_storage_names)
            list_storages.append(recovery_storage_names)
        assert hasattr(self.wf_context, 'added_reservation'), '"added_reservation" should be in context object.'
        assert isinstance(self.wf_context.added_reservation, list), 'Reservation names should be list type.'
        assert len(self.wf_context.added_reservation) > 0, 'Please provide reservation name(s).'
        reservation_names = self.wf_context.added_reservation
        if self.wf_context.added_reservation_policy:
            logger.info(
                'Using "added_reservation_policy" from YAML file as reservation policy names.', False, True)
            reservation_policy_names = self.wf_context.added_reservation_policy
        else:
            logger.info(
                'Using "reservation_policy_name" from assign_reservation_policy_to_reservation'
                ' in YAML data as reservation policy names.', False, True)
            reservation_policy_names = \
                self.wf_context.assign_datastores_and_reservation_policy_to_reservation.reservation_policy_names

        assert len(reservation_policy_names) > 0, 'Reservation policy names used should not be empty.'
        cluster_reservation_rp_blueprint_relation_obj = []
        for i, reservation_name in enumerate(reservation_names):
            kwargs = {
                'current_browser': current_browser,
                'tenant_name': tenant_name,
                'reservation_name': reservation_name.strip(),
                'reservation_policy': reservation_policy_names[i],
                'storages': list_storages[i],
                'output': output
            }
            AssignDatastoresAndReservationPolicyToReservation(
                self.cloud_administrator_assigns_datastores_and_reservation_policy_to_reservation.__name__,
                **kwargs
            ).run()
            list_reservations_assigned_reservation_policy.append(output[-1])
            relation_obj = WorkflowRelationMapping(
                list_cluster[i], reservation_name.strip(), None, None, None, None, reservation_policy_names[i])
            cluster_reservation_rp_blueprint_relation_obj.append(relation_obj)
        setattr(
            self.wf_context, 'added_cluster_reservation_rp_blueprint_relation',
            cluster_reservation_rp_blueprint_relation_obj
        )
        setattr(
            self.wf_context, 'assigned_reservation_policy_reservations',
            list_reservations_assigned_reservation_policy
        )
        logger.info(
            'Reservatioins assigned datastores and reservation policy: {}'.format(
                self.wf_context.assigned_reservation_policy_reservations)
        )

    def cloud_administrator_removes_reservation_policy_from_reservation(self):
        RemoveReservationPolicyFromReservation(
            self.cloud_administrator_removes_reservation_policy_from_reservation.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_assigns_reservation_policy_to_blueprint(self):
        assert hasattr(self.wf_context, 'blueprints'), \
            'blueprints key should be in YAML file.'
        assert hasattr(self.wf_context, 'added_reservation_policy'), \
            'added_reservation_policy name should be in context object'
        assert self.wf_context.blueprint_machine_pairs is not None, \
            'blueprint_machine_pairs should contain blueprint-machine pairs.'
        current_browser = self.wf_context.shared.current_browser
        assigned_reservation_policy_blueprints = []
        blueprint_machine_pairs = self.wf_context.blueprint_machine_pairs.__dict__
        blueprint_names = \
            (self.wf_context.blueprint_machine_pairs.__dict__.keys() if self.wf_context.blueprint_machine_pairs
             else None)
        assert blueprint_names is not None, 'blueprint names should not be empty.'

        for i, blueprint in enumerate(blueprint_names):
            output = []
            machine_name = blueprint_machine_pairs.get(blueprint, None)
            assert machine_name, 'Machine name for blueprint:{} should not be None.'.format(blueprint)
            if self.wf_context.added_reservation_policy:
                logger.info(
                    'Using "added_reservation_policy" from context data as reservation policy name.')
                reservation_policy_name = (self.wf_context.added_reservation_policy[i] if
                                           self.wf_context.added_reservation_policy else None)
            else:
                logger.info('Using "reservation_policy_name" from  assign_reservation_policy_to_blueprint'
                            ' in YAML data as reservation policy name.')
                reservation_policy_name = \
                    self.wf_context.assign_reservation_policy_to_blueprint.reservation_policy_name
            assert reservation_policy_name is not None, \
                'reservation policy should not be None.'
            kwargs = {
                'blueprint_name': blueprint,
                'machine_name': machine_name,
                'reservation_policy_name': reservation_policy_name,
                'current_browser': current_browser,
                'output': output
            }
            AssignReservationPolicyToBlueprint(
                self.cloud_administrator_assigns_reservation_policy_to_blueprint.__name__,
                **kwargs
            ).run()
            if output:
                assigned_blueprints = output[0]
                assigned_reservation_policy_blueprints.append(assigned_blueprints)

            cluster_blueprint_relation = getattr(
                self.wf_context, 'added_cluster_reservation_rp_blueprint_relation', None
            )
            if cluster_blueprint_relation:
                logger.debug('Using mapping relation object to store cluster blueprint relation.')
                for relation in cluster_blueprint_relation:
                    if relation.get_reservation_policy() == reservation_policy_name:
                        relation.set_blueprint(blueprint)
                        logger.info(
                            'Set blueprint: {} to relation obj: {}.'.format(relation.get_blueprint(), relation)
                        )
        setattr(self.wf_context, 'assigned_reservation_policy_blueprints', assigned_reservation_policy_blueprints)

    def cloud_administrator_assigns_rp_to_all_vsphere_blueprint(self):
        rp_list = getattr(self.wf_context, 'added_reservation_policy', [])
        assert len(rp_list) > 0, 'Please validate there is at least 1 reservation policy added'
        for vm_setting in self.wf_context.deploy_multiple_vms.vm_settings:
            rp = vm_setting.reservation_policy
            if rp is None or (isinstance(rp, str) and rp.isspace()):
                vm_setting.reservation_policy = rp_list[0]

        AssignRPtoAllvSphereBlueprint(
            self.cloud_administrator_assigns_rp_to_all_vsphere_blueprint.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_removes_reservation_policy_from_blueprint(self):
        RemoveReservationPolicyFromBlueprint(
            self.cloud_administrator_removes_reservation_policy_from_blueprint.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_removes_rp_from_all_vsphere_blueprint(self):
        RemoveRPfromAllvSphereBlueprint(
            self.cloud_administrator_assigns_rp_to_all_vsphere_blueprint.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_assigns_storage_reservation_policy_to_blueprint(self):
        AssignStorageReservationPolicyToBlueprint(
            self.cloud_administrator_assigns_storage_reservation_policy_to_blueprint.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_associates_avamar_proxies_with_cluster(self):
        AssociateAvamarProxiesWithCluster(
            self.cloud_administrator_associates_avamar_proxies_with_cluster.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_deploys_multiple_vms(self):
        if hasattr(self.wf_context, 'added_backup_service_level'):
            for vm_setting in self.wf_context.deploy_multiple_vms.vm_settings:
                if hasattr(vm_setting.deployment_properties, 'backup_service_level'):
                    bsl = vm_setting.deployment_properties.backup_service_level
                    if bsl is None or (isinstance(bsl, str) and bsl.isspace()):
                        vm_setting.deployment_properties.backup_service_level \
                            = self.wf_context.added_backup_service_level.backup_to_operate_vm

        DeployMultipleVM(
            self.cloud_administrator_deploys_multiple_vms.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_deploys_vm(self):
        DeployVM(
            self.cloud_administrator_deploys_vm.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_deploys_vm_parallel(self):
        added_storages = getattr(self.wf_context, 'added_cloud_storage', [])
        deploy_vm_context = self.wf_context.deploy_vm_parallel
        with_dp = deploy_vm_context.with_dp

        added_backup_service_levels = ['NoProtection'] + \
                                      getattr(self.wf_context.shared.backup_service_levels, 'for_deletion', []) \
            if with_dp else []

        assert added_storages, \
            'There is no item in added_cloud_storage from context object, it is likely provision cloud storage failed.'
        cluster_blueprint_relation = getattr(
            self.wf_context, 'added_cluster_reservation_rp_blueprint_relation', None
        )
        assert cluster_blueprint_relation, \
            'Key:"added_cluster_reservation_rp_blueprint_relation" should be set by Keyword Cloud Administrator ' \
            'Assigns Reservation Policy To Blueprint'
        blueprint_machine_pairs = self.wf_context.blueprint_machine_pairs.__dict__ \
            if getattr(self.wf_context, 'blueprint_machine_pairs', None) else None
        assert blueprint_machine_pairs, 'configuration should contain blueprint_machine_paris which should not be empty'
        assert all(
            relation_obj.get_blueprint() in blueprint_machine_pairs.keys()
            for relation_obj in cluster_blueprint_relation), \
            'Not all blueprint are configured in key "blueprint_machine_pairs" in yaml file.'
        for relation in cluster_blueprint_relation:
            assert relation.get_cluster(), 'Cluster in relation_obj: {} should not be None.'.format(relation())
            provisioned_storages = [
                storage for storage in added_storages if storage.cluster_name == relation.get_cluster()
                ]
            assert relation.get_blueprint(), \
                'Blueprint in relation_obj: {} should not be None.'.format(relation)
            vsphere_machine_id = blueprint_machine_pairs[relation.get_blueprint()]
            assert vsphere_machine_id, 'vsphere_machine_id in blueprint_machine_pairs should not be None.'
            blueprint_machine_id_pairs = {relation.get_blueprint(): vsphere_machine_id}
            self._deploys_vm_parallel(
                keyword_name='cloud_administrator_deploys_vm_parallel',
                cloud_storages=provisioned_storages, backup_svc_levels=added_backup_service_levels,
                blueprint_machine_id_pairs=blueprint_machine_id_pairs
            )

    def cloud_administrator_deploys_vm_parallel_for_relation_mappings(self):
        self._deploys_vm_parallel_with_relation_mappings(
            keyword_name='cloud_administrator_deploys_vm_parallel_for_relation_mappings',
            key_to_relation_mappings='workflow_relation_list'
        )

    def _deploys_vm_parallel_with_relation_mappings(self, keyword_name, key_to_relation_mappings):
        relation_mappings = getattr(self.wf_context, key_to_relation_mappings, None)
        assert relation_mappings, 'There is no key:"{}" in context object in current workflow.'.format(
            key_to_relation_mappings)

        for mapping_obj in relation_mappings:
            blueprint = mapping_obj.get_blueprint()
            assert blueprint, 'Please provide blueprint in relation mappings: {}'.format(mapping_obj)
            provisioned_storages = mapping_obj.get_storages()
            assert provisioned_storages, 'storages in relation mappings: {} should not be None.'.format(mapping_obj)
            deploy_vm_context = self.wf_context.deploy_vm_parallel
            with_dp = deploy_vm_context.with_dp
            added_backup_service_levels = ['NoProtection'] + mapping_obj.get_backup_svc_levels() if with_dp else []
            vsphere_machine_id = mapping_obj.get_vsphere_machine_Id()
            assert vsphere_machine_id, 'vsphere_machine_id in relation mappings: {}.'.format(mapping_obj)

            self._deploys_vm_parallel(
                keyword_name=keyword_name, cloud_storages=provisioned_storages,
                backup_svc_levels=added_backup_service_levels,
                blueprint_machine_id_pairs={blueprint: vsphere_machine_id},
            )

    def _deploys_vm_parallel(self, keyword_name, cloud_storages, backup_svc_levels, blueprint_machine_id_pairs):
        """
        :param keyword_name: name of the keyword that actually calls into this implementation.
        :param cloud_storages: the group of cloud storages that are of a certain cluster.
        :param backup_svc_levels: the list of backup service levels.
        :param blueprint_machine_id_pairs: the blueprint:vsphere_machine_id pairs.
        Caveats: This method will use permutations of storages and backup service level to apply them on all pairs of
        blueprint_machine_id_pairs for the vm deployment.

        This keyword is for deploy vm in parallel. The request checking follows below algorithm:
        Submit a request , get request_id for tracking it
        Repeat above until submitting all requests
        Loop the list of request_ids to check each's result  via API call. The check will wait until each result
        returns(either fail or succeed) to proceed with next check(loop).
        Write back to context for deployed vms(even there might be both failed and passed requests though).
        AUC is considered pass if there is at least one request succeeds

        """
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login
        browser_type = self.wf_context.launch_browser.browserType
        deploy_vm_context = self.wf_context.deploy_vm_parallel
        with_dp = deploy_vm_context.with_dp
        assign_srp = getattr(deploy_vm_context, 'assign_storage_reservation_policy', None)
        rp4vm_boot_priority = int(getattr(deploy_vm_context, 'rp4vm_boot_priority', None)) \
            if getattr(deploy_vm_context, 'rp4vm_boot_priority', None) else None
        rp4vm_cg = getattr(deploy_vm_context, 'rp4vm_cg', None)
        rp4vm_policy = getattr(deploy_vm_context, 'rp4vm_policy', None)
        srm_power_on_priority = getattr(deploy_vm_context, 'SRM_power_on_priority', None)

        cpu_max = getattr(deploy_vm_context, 'cpu_max', None)
        ram_max = getattr(deploy_vm_context, 'ram_max', None)

        assert blueprint_machine_id_pairs, 'given blueprint:machineid pairs should not be empty.'

        assert current_browser is not None, 'current_browser is None, may be there is no active browser.'
        assert is_login is True, 'is_login attribute is not True, can not do anything if you do not login.'

        request_ids = []
        newly_deployed_vms = []
        final_result_list = {}

        import itertools
        # this is generated from permutations of provisioned storage and backup service levels.
        deploy_vm_requests_list = \
            list(itertools.product(cloud_storages, backup_svc_levels)) if with_dp else \
                [(i, '') for i in cloud_storages]
        for request_data in deploy_vm_requests_list:
            assert deploy_vm_context.number_of_vm is not None, 'number of VMs to be deployed should not be None'
            assert int(deploy_vm_context.number_of_vm) > 0, 'number of VMs to be deployed should be greater than 0'
            logger.debug('Deploy VM using storage:{}, Backup Service Level:{}'.format(request_data[0], request_data[1]))

            description = 'deploy vm for storage:' + request_data[0].name[0] + (
                ' and bsl:{}'.format(request_data[1]) if with_dp else '')
            num_of_vm = deploy_vm_context.number_of_vm
            reason_for_request = 'deploy vm test'
            backup_service_level = request_data[1] if with_dp else ''
            storage = request_data[0].name[0]
            storage_reservation_policy = request_data[0].srp[0] if request_data[0].srp else ''
            if assign_srp and not storage_reservation_policy:
                logger.warn('Storage Reservation Policy is empty for storage:{}, will not set.'.format(request_data[0]))

            if with_dp:
                if rp4vm_boot_priority:
                    test_method = DeployVmParallel.Func.DEPLOY_VM_PARALLEL_RP4VM_DP
                elif srm_power_on_priority:
                    test_method = DeployVmParallel.Func.DEPLOY_VM_PARALLEL_DR_DP
                else:
                    test_method = DeployVmParallel.Func.DEPLOY_VM_PARALLEL_DP
            else:
                if rp4vm_boot_priority:
                    test_method = DeployVmParallel.Func.DEPLOY_VM_PARALLEL_RP4VM_NO_DP
                elif srm_power_on_priority:
                    test_method = DeployVmParallel.Func.DEPLOY_VM_PARALLEL_DR_NO_DP
                else:
                    test_method = DeployVmParallel.Func.DEPLOY_VM_PARALLEL_NO_DP
            logger.info('Deploy VM in Parallel will be using test method:{}'.format(test_method), False, True)

            for blueprint_name,  vsphere_machine_id in blueprint_machine_id_pairs.iteritems():
                logger.info('Configured CPU range will be between 1 and {}'.format(cpu_max), False, True)
                logger.info('Configured RAM range will be between 512 and {}'.format(ram_max), False, True)
                kwargs={
                    'blueprint_name': blueprint_name,
                    'vsphere_machine_id': vsphere_machine_id,
                    'description': description, 'num_of_vm': num_of_vm,
                    'reason_for_request': reason_for_request, 'backup_service_level': backup_service_level,
                    'browser_type': browser_type, 'current_browser': current_browser,
                    'srm_power_on_priority': srm_power_on_priority,
                    'rp4vm_boot_priority': rp4vm_boot_priority,
                    'rp4vm_cg': rp4vm_cg,
                    'rp4vm_policy': rp4vm_policy,
                    'cpu_max': cpu_max,
                    'ram_max': ram_max,
                    'storage_reservation_policy': storage_reservation_policy,
                    'assign_srp': assign_srp,
                    'storage': storage
                }

                DeployVmParallel(
                    name=keyword_name,
                    method_name=test_method,
                    **kwargs
                ).run()

                RequestChecker(
                    keyword_name,
                    method_name=RequestChecker.Func.GET_LATEST_REQUEST_ID, description=description, ignore_failure=True,
                    output=request_ids).run()

        # TODO: We will figure our a more elegant way to organize those variables.
        vra_host = urlparse(self.wf_context.launch_browser.baseUrl).netloc
        vra_tenant = self.wf_context.vra.tenant
        vra_username = self.wf_context.user_roles.Config_Admin.username
        vra_password = self.wf_context.user_roles.Config_Admin.password

        for request_item in request_ids:
            request_id, description = request_item
            logger.info('Start checking result for request of id:{}'.format(request_id))
            request_result = []
            RequestChecker(
                keyword_name,
                method_name=RequestChecker.Func.GET_REQUEST_RESULT_BY_REST, description=description,
                ignore_failure=True, output=request_result, request_id=request_id).run()
            if request_result:
                if request_result[0].status == 'Successful':
                    vra_rest = VraRestUtil(vra_host, vra_tenant, vra_username, vra_password)
                    vm_name = vra_rest.get_vm_name_by_request_id(request_id)
                    newly_deployed_vms.append(vm_name)
                    logger.info(
                        'Successfully deployed vm:"{}" for deploy vm request:"{}".'.format(
                            vm_name, request_id), False, True
                    )
                    final_result_list.update({request_id: True})

                else:
                    logger.error(
                        'Deploy VM request:"{}" failed, error details:{}'.format(
                            request_id, request_result[0].status_details))
                    final_result_list.update({request_id: False})
            else:
                logger.error('Getting request result for request:"{}" failed.'.format(request_id))
                final_result_list.update({request_id: False})

        failed_requests = [k for k, v in final_result_list.iteritems() if v is False]
        if len(newly_deployed_vms) > 0:
            logger.info('Newly deployed following VMs:{}'.format(newly_deployed_vms), False, True)
            if getattr(self.wf_context, 'deployed_vms'):
                logger.info(
                    'There are items:{} in deployed_vms in context object.'.format(self.wf_context.deployed_vms))
                self.wf_context.deployed_vms.extend(newly_deployed_vms)
                logger.info(
                    'Appended newly deployed vms:{} to original context object deployed_vms.'.format(
                        newly_deployed_vms))
            else:
                setattr(self.wf_context, 'deployed_vms', newly_deployed_vms)
                logger.info('Added newly deployed vms:{} to context object deployed_vms.'.format(newly_deployed_vms))
            if failed_requests:
                logger.warn('There are still requests failed, request ids:{}'.format(failed_requests))
        else:
            error_msg = 'Deploy VM in parallel failed, there are no VM deployed.{}'.format(
                ' failed requests:{}'.format(failed_requests) if failed_requests else '')
            raise AssertionError(error_msg)

    @catch_assert_exception
    def cloud_administrator_provisions_cloud_storage(self):
        # list saved all provision storage info
        added_cloud_storage = []
        current_browser = self.wf_context.shared.current_browser
        provision_cloud_storage_list = self.wf_context.provision_cloud_storage
        # get password of current user.
        # Storage Admin Password
        assert hasattr(self.wf_context.user_roles, 'Storage_Admin'), \
            'Please provide account info about: Storage_Admin.'
        _user_info = getattr(self.wf_context.user_roles, 'Storage_Admin')
        password = getattr(_user_info, 'password', None)
        existed_clusters = getattr(self.wf_context, "existed_clusters", [])
        vro = self.wf_context.vro
        assert len(existed_clusters) > 0, 'existed_clusters is None'
        assert current_browser is not None, 'current_browser in context object is None.'
        assert provision_cloud_storage_list is not None, 'provision_cloud_storage is ' \
                                                         'not configured in yaml file.'
        assert password is not None, 'Please provide password of Storage_Admin.'

        for item in provision_cloud_storage_list:
            assert item.description is not None, 'the description of provision_cloud_storage ' \
                                                 'is None in yaml file.'
            assert item.storage_type is not None, 'the storage_type of provision_cloud_storage' \
                                                  ' is None in yaml file.'
            assert item.size_in_gb is not None, 'the size_in_gb of provision_cloud_storage' \
                                                ' is None in yaml file'
        for counter, item in enumerate(provision_cloud_storage_list):
            cluster_name = existed_clusters[counter]

            kwargs = {
                'current_browser': current_browser,
                'vro': vro,
                'description': item.description,
                'hwi_name': item.hwi_name,
                'storage_type': item.storage_type,
                'vipr_storage_tier': item.vipr_storage_tier,
                'size_in_gb': item.size_in_gb,
                'password': password,
                'cluster_name': cluster_name,
            }

            logger.info('Begin to provision storage for cluster: {}'.format(cluster_name), False, True)
            ProvisionCloudStorage(
                self.cloud_administrator_provisions_cloud_storage.__name__,
                **kwargs
            ).run()

            request_result = []
            RequestChecker(
                self.cloud_administrator_provisions_cloud_storage.__name__,
                description=item.description, requestcheckingtimeout=7200,
                requestcheckingfirstwaitduration=60, sleep=300,
                output=request_result
            ).run()

            assert request_result[0].status == 'Successful', 'The request status: {0}, detail info: {1}'.format(
                request_result[0].status, request_result[0].status_details)
            # get srp and storage after provisioned.

            logger.info('The request status: {0}, detail info: {1}'.format(
                request_result[0].status, request_result[0].status_details), False, True)
            datastore_name, srp = GetDatastoreFromvRO().filter_latest_storage(vro, item.hwi_name, cluster_name)
            assert datastore_name, 'No datastore find in vRO, filter condition: \n' \
                                   'Hwi: {0}, cluster: {1}'.format(item.hwi_name, cluster_name)
            added_storage = CloudStorageObject([datastore_name], [srp], item.hwi_name, cluster_name)
            logger.info('New storage provisioned: {0}, Srp: {1}'.format([datastore_name], [srp]), False, True)
            added_cloud_storage.append(added_storage)

        setattr(self.wf_context, "added_cloud_storage", added_cloud_storage)

    @catch_assert_exception
    def cloud_administrator_provision_multiple_cloud_storage(self):
        """
        Description:
        This AUC will need to loop creating storages.
        For each ViPR vPool,
        vPool_DS_Small number of datastores will be provisioned at a size randomly generated between 50 GB and 499 GB,
        and vPool_DS_Large number datastores will be provisioned at a size randomly generated between 500G and 2000 GB.
        CheckPoint: At least one datastore is successfully deployed
        """
        current_browser = self.wf_context.shared.current_browser
        provision_mul_storage = getattr(self.wf_context, 'provision_multiple_cloud_storage', None)
        added_cloud_storage = []
        # Storage Admin Password
        assert hasattr(self.wf_context.user_roles, 'Storage_Admin'), \
            'Please provide account info about: Storage_Admin.'
        _user_info = getattr(self.wf_context.user_roles, 'Storage_Admin')
        password = getattr(_user_info, 'password', None)
        vro = self.wf_context.vro
        assert current_browser is not None, 'current_browser in context object is None.'
        assert provision_mul_storage, 'provision_multiple_cloud_storage is not configured in yaml file.'
        assert password is not None, 'Please provide password of Storage_Admin.'
        logger.info('Start to validate configuration in: provision_multiple_cloud_storage.', False, True)
        for cloud_storage in provision_mul_storage:
            added_cloud_storage_for_cluster = []
            vpool_ds_small = int(cloud_storage.vPool_DS_Small)
            vpool_ds_large = int(cloud_storage.vPool_DS_Large)
            assert cloud_storage.cluster is not None, 'Please provide cluster for provision.'
            assert cloud_storage.hwi_name is not None, 'Please provide hwi name for provision..'
            assert cloud_storage.storage_type is not None, 'Please provide storage_type for provision.'
            assert cloud_storage.virtual_pools, \
                'Please provide virual pools list of cluster: {} for provision.'.format(
                    cloud_storage.cluster)
            assert vpool_ds_small >= 0, 'vPool_DS_Small should not be negative integer.'
            assert vpool_ds_large >= 0, 'vPool_DS_Large should not be negative integer.'
            virtual_pools = cloud_storage.virtual_pools.split(',')
            for item in virtual_pools:
                formatter = '%I%M%S%p'
                _prefix_vpool = item.split(';')[0]
                logger.info('Start to provision {} small datastores, {} large datastores in vpool prefix: {} '
                            'for cluster: {}, hwi: {}.'.format(vpool_ds_small, vpool_ds_large, _prefix_vpool,
                                                      cloud_storage.cluster, cloud_storage.hwi_name), False, True)
                kwargs = {
                    'current_browser': current_browser,
                    'vro': vro,
                    'description': '',
                    'hwi_name': cloud_storage.hwi_name,
                    'storage_type': cloud_storage.storage_type,
                    'vipr_storage_tier': item.strip(),
                    'size_in_gb': 0,
                    'password': password,
                    'cluster_name': cloud_storage.cluster,
                }
                for i in range(0, vpool_ds_small + vpool_ds_large):
                    if i <= vpool_ds_small-1:
                        description = 'test_provision_small_DS_in_{}_{}'.format(
                            _prefix_vpool, time.strftime(formatter, time.localtime()))
                        logger.info('Begin to provision the {} small DS'.format(i+1), False, True)
                        kwargs['description'] = description
                        kwargs['size_in_gb'] = random.randint(50, 499)
                    else:
                        description = 'test_provision_large_DS_in_{}_{}'.format(
                            _prefix_vpool, time.strftime(formatter, time.localtime()))
                        logger.info('Begin to provision the {} large DS'.format(i + 1 - vpool_ds_small), False, True)
                        kwargs['description'] = description
                        kwargs['size_in_gb'] = random.randint(500, 2000)

                    ProvisionCloudStorage(
                        self.cloud_administrator_provision_multiple_cloud_storage.__name__,
                        **kwargs
                    ).run()

                    request_result = []

                    RequestChecker(
                        self.cloud_administrator_provision_multiple_cloud_storage.__name__,
                        description=description,
                        not_fail_on_request_failed=True,
                        output=request_result
                    ).run()

                    if request_result and request_result[0].status == 'Successful':
                        # get srp and storage after provisioned.
                        datastore_name, srp = GetDatastoreFromvRO().filter_latest_storage(vro,
                                                                                          cloud_storage.hwi_name,
                                                                                          cloud_storage.cluster)
                        assert datastore_name, 'No datastore find in vRO, filter condition: \n' \
                                               'Hwi: {0}, cluster: {1}'.format(cloud_storage.hwi_name,
                                                                               cloud_storage.cluster)
                        added_storage = CloudStorageObject([datastore_name], [srp], cloud_storage.hwi_name,
                                                           cloud_storage.cluster)
                        logger.info('New storage provisioned: {0}, Srp: {1}'.format([datastore_name], [srp]), False, True)
                        added_cloud_storage.append(added_storage)
                        added_cloud_storage_for_cluster.append(added_storage)
                    else:
                        logger.error('The request status: {0}, detail info: {1}'.format(request_result[0].status,
                                     request_result[0].status_details))
            assert len(added_cloud_storage_for_cluster) >= 1, 'At least one datastore for cluster: {} and hwi: {} ' \
                'should be successfully deployed.'.format(cloud_storage.cluster, cloud_storage.hwi_name)
        setattr(self.wf_context, 'added_cloud_storage', added_cloud_storage)
        logger.info('All datastores provisioned: {}'.format([storage.name[0] for storage in added_cloud_storage]),
                    False, True)

    def cloud_administrator_creates_reservation(self):
        CreateReservation(
            self.cloud_administrator_creates_reservation.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    @catch_assert_exception
    def cloud_administrator_deletes_vcenter(self):
        current_browser = self.wf_context.shared.current_browser
        added_vcenter = self.wf_context.added_vcenter
        method_name = VCenterManager.Func.DELETE_VCENTER
        output = []
        if self.wf_context:
            assert current_browser is not None, 'current_browser in yaml is None, ' \
                                                'may be there is no active browser'
            assert current_browser.is_login, 'Please login to vRA, The flag value is_login is: False.'
            assert self.wf_context.delete_vcenter.select_operation is not None, 'select_operation in yaml is None,'
            assert self.wf_context.delete_vcenter.ensure_delete_info is not None, 'ensure_delete_info in yaml is None,'
        for item in added_vcenter:
            kwargs = {
                'select_operation': self.wf_context.delete_vcenter.select_operation,
                'select_vcenter_name': item,
                'ensure_delete_info': self.wf_context.delete_vcenter.ensure_delete_info,
                'current_browser': current_browser,
                'output': output,
            }
            VCenterManager(self.cloud_administrator_deletes_vcenter.__name__,
                           method_name=method_name,
                           **kwargs).run()

            # check the request
            RequestChecker(self.cloud_administrator_deletes_vcenter.__name__,
                           description=method_name,).run()

    def cloud_administrator_deletes_datastore(self):
        DeleteDataStore(
            self.cloud_administrator_deletes_datastore.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_deletes_vcenter_relationship(self):
        DeleteVcenterRelationship(
            self.cloud_administrator_deletes_vcenter_relationship.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_adds_vcenter_relationship(self):
        AddVcenterRelationship(
            self.cloud_administrator_adds_vcenter_relationship.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_extends_vcenter_relationship(self):
        AddVcenterRelationship(
            self.cloud_administrator_extends_vcenter_relationship.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context,
            extend_rp4vm=True
        ).run()

    def cloud_administrator_creates_reservation_policy(self):
        new_rsv_policy_name = None
        rsv_policys = []
        new_rsv_policy_description = 'create reservation policy'
        cur_browser = self.wf_context.shared.current_browser
        assert cur_browser is not None, 'current_browser in yaml is None, ' \
                                        'may be there is no active browser'
        assert hasattr(self.wf_context, 'create_reservation_policy') is True, \
            'Please add YAML Item: create_reservation_policy'
        assert hasattr(self.wf_context.create_reservation_policy, 'names') is True, \
            'Please add YAML Item: names in item create_reservation_policy'

        if len(self.wf_context.create_reservation_policy.names) > 0:
            _reservation_policys = self.wf_context.create_reservation_policy.names
            for reservation_policy in _reservation_policys:
                new_rsv_policy_name = reservation_policy
                output = []
                kw = {
                    'reservation_policy_name': new_rsv_policy_name,
                    'reservation_policy_description': new_rsv_policy_description,
                    'cur_browser': cur_browser,
                    'output': output
                }
                CreateReservationPolicy(
                    self.cloud_administrator_creates_reservation_policy.__name__,
                    'runTest',
                    **kw
                ).run()

                if output and len(output) == 1:
                    added_reservation_policy = output[0]
                    rsv_policys.append(added_reservation_policy)
            setattr(self.wf_context, 'added_reservation_policy', rsv_policys)
        else:
            logger.error('No Reservation Policy need to add.', False)
            logger.info('[AUC] - "{}" - {}'.format(' '.join([word.capitalize() for word in
                                                             self.cloud_administrator_creates_reservation_policy.
                                                             __name__.split('_')]), 'FAILED'), False, True)

    def cloud_administrator_deletes_reservation_policy(self):
        delete_rsv_policy_name = None
        cur_browser = self.wf_context.shared.current_browser
        assert cur_browser is not None, 'current_browser in yaml is None, ' \
                                        'may be there is no active browser'

        if not isinstance(getattr(self.wf_context, 'added_reservation_policy', None), list):
            setattr(self.wf_context, 'added_reservation_policy', [])

        if len(self.wf_context.added_reservation_policy) > 0:
            _reservation_policys = self.wf_context.added_reservation_policy
            for reservation_policy in _reservation_policys:
                delete_rsv_policy_name = reservation_policy
                output = []
                kw = {
                    'delete_rsv_policy_name': delete_rsv_policy_name,
                    'cur_browser': cur_browser,
                    'output': output
                }

                DeleteReservationPolicy(
                    self.cloud_administrator_deletes_reservation_policy.__name__,
                    'runTest',
                    **kw
                ).run()

        else:
            logger.warn(msg='No Reservation Policy need to delete.')
            logger.info('[AUC] - "{}" - {}'.format(' '.join([word.capitalize() for word in
                                                             self.cloud_administrator_deletes_reservation_policy.
                                                             __name__.split('_')]), 'FAILED'), False, True)

    def cloud_administrator_destroy_vms(self):
        DestroyVMs(
            self.cloud_administrator_destroy_vms.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_adds_backup_service_level(self):
        current_browser = self.wf_context.shared.current_browser
        output = []
        bsl_to_add = []
        added_bsl = []
        if len(self.wf_context.add_backup_service_level)>2:
            logger.warn('More than 2 entries are provided to create backup service level, only the first two will '
                        'take effect!')
            bsl_to_add = self.wf_context.add_backup_service_level[:2]
        else:
            bsl_to_add = self.wf_context.add_backup_service_level
        for auc_context in bsl_to_add:
            description = auc_context.description if hasattr(auc_context, 'description') else \
                'Add backup service default description.'
            reasons = auc_context.reasons if hasattr(auc_context, 'reasons') else \
                'add backup service level default reasons'
            bsl_name = auc_context.specify_the_service_level_name

            schedule_type = auc_context.select_backup_schedule
            schedule_start_time = auc_context.schedule_start_time
            schedule_week_number = auc_context.schedule_week_number
            schedule_weekday = auc_context.schedule_weekday
            backup_schedule = BSLSchedule(schedule_type, schedule_week_number, schedule_weekday, schedule_start_time)
            assert backup_schedule.validate_schedule(), 'Some backup schedule configuration is not valid'

            retention_policy = auc_context.regular_retention_policy
            retention_long_term_policy = auc_context.long_term_retention_policy
            retention_for_number = auc_context.retention_for_number
            retention_unit = auc_context.retention_unit
            retention_date = auc_context.retention_date
            retention_time = auc_context.retention_time
            retention_config = BSLRetention(retention_policy, retention_long_term_policy, retention_for_number,
                                            retention_unit, retention_date, retention_time)
            assert retention_config.validate_retention(), 'Some retention configuration is not valid'

            replication_schedule_type = auc_context.replication_schedule_type
            replication_week_number = auc_context.replication_week_number
            replication_weekday = auc_context.replication_weekday
            replication_start_time = auc_context.replication_start_time
            replication_schedule = BSLSchedule(replication_schedule_type, replication_week_number, replication_weekday,
                                               replication_start_time)
            assert replication_schedule.validate_schedule(), 'Some replication schedule configuration is not valid'

            kwargs = {
                'current_browser': current_browser,
                'backup_service_level_name': bsl_name,
                'description': description,
                'reasons': reasons,
                'backup_schedule': backup_schedule,
                'retention_schedule': retention_config,
                'replication_schedule': replication_schedule,
                'output': output,
            }
            AddBackupServiceLevel(
                self.cloud_administrator_adds_backup_service_level.__name__,
                **kwargs
            ).run()
        for request in output:
            if request.result.status == 'Successful':
                added_bsl.append(request.name)
            else:
                logger.error("Request failed with details: {}".format(request.result.status_details), True)
        if not hasattr(self.wf_context.shared, 'backup_service_levels'):
            setattr(self.wf_context.shared, 'backup_service_levels', YAMLData())
            if not hasattr(self.wf_context.shared.backup_service_levels, 'for_deletion'):
                setattr(self.wf_context.shared.backup_service_levels, 'for_deletion', [])
        self.wf_context.shared.backup_service_levels.for_deletion.extend(added_bsl)
        assert len(added_bsl) == len(bsl_to_add), 'Some requests failed in creating backup service level, please check!'
        setattr(self.wf_context.added_backup_service_level, 'backup_to_operate_vm', added_bsl[0])
        if len(added_bsl) == 2:
            setattr(self.wf_context.added_backup_service_level, 'backup_to_set_backup_service', added_bsl[1])

    def cloud_administrator_deletes_backup_service_level(self):
        DeleteBackupServiceLevel(
            self.cloud_administrator_deletes_backup_service_level.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_closes_browser(self):
        if not self.wf_context.shared.current_browser.instance:
            return

        CloseBrowser(
            self.cloud_administrator_closes_browser.__name__,
            ctx_in=self.wf_context.shared.current_browser,
            ctx_out=self.wf_context.shared.current_browser
        ).run()

    def cloud_administrator_gets_datastores_from_vRO(self):
        GetDatastoreFromvRO(
            self.cloud_administrator_gets_datastores_from_vRO.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_gets_ARRs_from_vRO(self):
        GetARRFromvRO(
            self.cloud_administrator_gets_ARRs_from_vRO.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_gets_ASRs_from_vRO(self):
        AUC_GetASRFromvRO(
            self.cloud_administrator_gets_ASRs_from_vRO.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_adds_avamar_grid(self):
        AddAvamarGrid(
            self.cloud_administrator_adds_avamar_grid.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_adds_avamar_grid_unselect_proxy(self):
        AddAvamarGrid(
            self.cloud_administrator_adds_avamar_grid_unselect_proxy.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context,
            unselect_proxy=True
        ).run()

    def cloud_administrator_deletes_avamar_grid(self):
        DeleteAvamarGrid(
            self.cloud_administrator_deletes_avamar_grid.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    @catch_assert_exception
    def cloud_administrator_adds_avamar_proxy(self):
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login
        add_proxy_contexts = self.wf_context.add_avamar_proxy

        assert current_browser is not None, 'current_browser is None, may be there is no active browser.'
        assert is_login is True, 'is_login attribute is not True, can not do anything if you do not login.'

        output = []
        added_avamar_proxies = []
        for proxy_context in add_proxy_contexts:
            description = 'add proxy for avamar grid:{}'.format(proxy_context.avamar_path)
            kwargs = {'current_browser': current_browser, 'is_login': is_login, 'description': description,
                      'output': output}

            for config_attr_name in ADD_AVAMAR_PROXY_CONFIG_ATTR_NAMES:
                assert getattr(proxy_context, config_attr_name, None) is not None, \
                    'Add Avamar Proxy config attribute: "{}" is not configured.'.format(config_attr_name)
                kwargs.update({config_attr_name: getattr(proxy_context, config_attr_name)})

            # proxy full name should be like: /client/Giza-ave01-p2.vlab.local
            avamar_domain = getattr(proxy_context, 'avamar_domain')
            proxy_vm_name = getattr(proxy_context, 'proxy_vm_name')
            proxy_full_name = '{}{}'.format(
                avamar_domain if avamar_domain.endswith('/') else avamar_domain + '/', proxy_vm_name)
            AvamarProxyManager(
                self.cloud_administrator_adds_avamar_proxy.__name__,
                method_name=AvamarProxyManager.Func.ADD_AVAMAR_PROXY,
                **kwargs).run()

            request_result = []
            RequestChecker(self.cloud_administrator_adds_site.__name__, description=description,
                ignore_failure=True, output=request_result).run()

            if request_result:
                if request_result[-1].status == 'Successful':
                    added_avamar_proxies.append(proxy_full_name) # we may use vRA api to retrieve the name for proxy.
                else:
                    raise AssertionError(
                        'Add Avamar Proxy failed, error details:{}'.format(request_result[-1].status_details))
            else:
                raise AssertionError('Add Avamar Proxy failed, failed to get request result.')

        setattr(self.wf_context, 'added_avamar_proxies', added_avamar_proxies)
        logger.info('Added Avamar Proxies: {}'.format(added_avamar_proxies))

    @catch_assert_exception
    def cloud_administrator_sets_backup_service_level(self):
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login

        assert (hasattr(self.wf_context, 'deployed_vms') and
                self.wf_context.deployed_vms and
                len(self.wf_context.deployed_vms) >= 1), 'Number of VMs to be deployed should be greater than 0.'

        if (hasattr(self.wf_context, 'set_backup_service_level') and
                hasattr(self.wf_context.set_backup_service_level, 'backup_service_level_name') and
                self.wf_context.set_backup_service_level.backup_service_level_name is not None):
            _backup_service_level_name = self.wf_context.set_backup_service_level.backup_service_level_name
        elif (hasattr(self.wf_context, 'added_backup_service_level') and
              hasattr(self.wf_context.added_backup_service_level, 'backup_to_set_backup_service') and
              self.wf_context.added_backup_service_level.backup_to_set_backup_service is not None):
            _backup_service_level_name = self.wf_context.added_backup_service_level.backup_to_set_backup_service
        else:
            assert False, 'Backup service name is not provided. Please make sure backup_service_level ' \
                          'of set_backup_service_level or backup_to_set_backup_service of ' \
                          'added_backup_service_level in YAML file is not None. '

        _deployed_vm = self.wf_context.deployed_vms[-1]
        _method_name = self.cloud_administrator_sets_backup_service_level.__name__
        kwargs = {
            'current_browser': current_browser,
            'is_login': is_login,
            'description': _method_name,
            'vm_name': _deployed_vm,
            'backup_service_level_name': _backup_service_level_name
        }
        SetBackupServiceLevel(
            _method_name,
            **kwargs
        ).run()

    @catch_assert_exception
    def cloud_administrator_sets_backup_service_level_for_all_vms(self):
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login

        assert (hasattr(self.wf_context, 'deployed_vms') and
                self.wf_context.deployed_vms and
                len(self.wf_context.deployed_vms) >= 1), 'Number of VMs to be deployed should be greater than 0.'

        if (hasattr(self.wf_context, 'set_backup_service_level') and
                hasattr(self.wf_context.set_backup_service_level, 'backup_service_level_name') and
                self.wf_context.set_backup_service_level.backup_service_level_name is not None):
            _backup_service_level_name = self.wf_context.set_backup_service_level.backup_service_level_name
        elif (hasattr(self.wf_context, 'added_backup_service_level') and
              hasattr(self.wf_context.added_backup_service_level, 'backup_to_set_backup_service') and
              self.wf_context.added_backup_service_level.backup_to_set_backup_service is not None):
            _backup_service_level_name = self.wf_context.added_backup_service_level.backup_to_set_backup_service
        else:
            assert False, 'Backup service name is not provided. Please make sure backup_service_level ' \
                          'of set_backup_service_level or backup_to_set_backup_service of ' \
                          'added_backup_service_level in YAML file is not None. '
        for _deployed_vm in self.wf_context.deployed_vms:
            logger.info('Start to set backup service level in VM: {}'.format(_deployed_vm))
            _method_name = self.cloud_administrator_sets_backup_service_level.__name__
            kwargs = {
                'current_browser': current_browser,
                'is_login': is_login,
                'description': 'test_set_backup_service_for_vm ' + _deployed_vm,
                'vm_name': _deployed_vm,
                'backup_service_level_name': _backup_service_level_name
            }
            SetBackupServiceLevel(
                _method_name,
                **kwargs
            ).run()

    @catch_assert_exception
    def cloud_administrator_sets_no_protection_backup_service_level(self):
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login

        assert (hasattr(self.wf_context, 'deployed_vms') and
                self.wf_context.deployed_vms and
                len(self.wf_context.deployed_vms) >= 1), 'Number of VMs to be deployed should be greater than 0.'

        _deployed_vm = self.wf_context.deployed_vms[-1]
        _method_name = self.cloud_administrator_sets_no_protection_backup_service_level.__name__
        _backup_name = 'NoProtection'

        kwargs = {
            'current_browser': current_browser,
            'is_login': is_login,
            'description': _method_name,
            'vm_name': _deployed_vm,
            'backup_service_level_name': _backup_name
        }
        SetBackupServiceLevel(
            _method_name,
            **kwargs
        ).run()

    @catch_assert_exception
    def cloud_administrator_sets_origin_backup_service_level(self):
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login

        assert (hasattr(self.wf_context, 'deployed_vms') and
                self.wf_context.deployed_vms and
                len(self.wf_context.deployed_vms) >= 1), 'Number of VMs to be deployed should be greater than 0.'

        if (hasattr(self.wf_context, 'added_backup_service_level') and
                hasattr(self.wf_context.added_backup_service_level, 'backup_to_operate_vm') and
                self.wf_context.added_backup_service_level.backup_to_operate_vm is not None):
            _origin_backup_name = self.wf_context.added_backup_service_level.backup_to_operate_vm
        elif (hasattr(self.wf_context, 'deploy_vm') and
              hasattr(self.wf_context.deploy_vm, 'backup_service_level') and
              self.wf_context.deploy_vm.backup_service_level is not None):
            _origin_backup_name = self.wf_context.deploy_vm.backup_service_level
        else:
            assert False, 'Backup service name is not provided. Please make sure backup_to_operate_vm ' \
                          'of added_backup_service_level or backup_service_level of ' \
                          'deploy_vm in YAML file is not None. '

        _deployed_vm = self.wf_context.deployed_vms[-1]
        _method_name = self.cloud_administrator_sets_origin_backup_service_level.__name__
        kwargs = {
            'current_browser': current_browser,
            'is_login': is_login,
            'description': _method_name,
            'vm_name': _deployed_vm,
            'backup_service_level_name': _origin_backup_name
        }
        SetBackupServiceLevel(
            _method_name,
            **kwargs
        ).run()

    def cloud_administrator_gets_backup_summary(self):
        GetBackupSummary(
            self.cloud_administrator_gets_backup_summary.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_displays_backup_service_level(self):
        DisplayBackupServiceLevel(
            self.cloud_administrator_displays_backup_service_level.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_deletes_reservation(self):
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login
        if not isinstance(getattr(self.wf_context, 'added_reservation', None), list):
            setattr(self.wf_context, 'added_reservation', [])

        _added_reservations = self.wf_context.added_reservation
        if not _added_reservations:
            logger.warn(
                msg='No reservation is picked to be deleted in yaml.')
            return
        for _delete_res in _added_reservations:
            kwargs = {
                'current_browser': current_browser,
                'is_login': is_login,
                'reservation': _delete_res,
            }
            DeleteReservation(
                self.cloud_administrator_deletes_reservation.__name__,
                **kwargs
            ).run()

    def cloud_administrator_logout(self):
        LogoutFromvRA(
            self.cloud_administrator_logout.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def user_logout(self):
        self.cloud_administrator_logout()

    def cloud_administrator_run_admin_report(self):
        RunAdminReport(
            self.cloud_administrator_run_admin_report.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()


    @catch_assert_exception
    def cloud_administrator_associates_cluster_to_asr(self):
        current_browser = self.wf_context.shared.current_browser
        assert current_browser is not None, 'shared.current_browser is None.'
        assert current_browser.is_login, 'Please login to vRA, The flag is_login is False.'
        output = []
        _method_name = ClusterManager.Func.ASSOCIATE_CLUSTER_TO_ASR

        assert (hasattr(self.wf_context, 'existed_clusters') and len(self.wf_context.existed_clusters) > 0)\
               is True, "No cluster is on boarded, please check if 'existed_clusters' is in your config file."
        clusters = self.wf_context.existed_clusters
        assert (hasattr(self.wf_context, 'added_avamar_site_relationship')) is True, \
            "No ASR is added. please check if 'added_avamar_site_relationship' is in your config file."
        asr = self.wf_context.added_avamar_site_relationship

        kw = {
            'current_browser': current_browser,
            'asr': asr,
            'cluster': clusters,
            'output': output
        }

        ClusterManager(
            self.cloud_administrator_associates_cluster_to_asr.__name__,
            method_name=_method_name,
            **kw
        ).run()

        RequestChecker(self.cloud_administrator_associates_cluster_to_asr.__name__,
                       description=_method_name).run()

    @catch_assert_exception
    def cloud_administrator_onboard_cluster(self):
        current_browser = self.wf_context.shared.current_browser
        assert current_browser is not None, 'shared.current_browser is None.'
        assert current_browser.is_login, 'Please login to vRA, The flag is_login is False.'
        onboard_cluster_type = self.wf_context.onboard_cluster_type
        assert onboard_cluster_type is not None, 'Please provide onboard cluster type.'
        assert onboard_cluster_type in ['LC1S', 'VS1S', 'DR2S', 'CA1S', 'CA2S', 'MP2S', 'MP3S'], \
            "Onboard cluster type should be in [LC1S, VS1S, DR2S, CA1S, CA2S, MP2S, MP3S]"
        output = []
        cluster = []
        get_onboard_cluster_action = {
            'LC1S': 'onboard_local_cluster',
            'VS1S': 'onboard_vsan_cluster',
            'DR2S': 'onboard_dr_cluster',
            'CA1S': 'onboard_ca_cluster',
            'CA2S': 'onboard_ca_cluster',
            'MP2S': 'onboard_mp_cluster',
            'MP3S': 'onboard_mp_cluster'
        }
        _method_name = ClusterManager.Func.ONBOARD_CLUSTER
        onboard_cluster_action = get_onboard_cluster_action.get(onboard_cluster_type)
        assert hasattr(self.wf_context, onboard_cluster_action), 'No item: {0} in YAML, when {1}'.format(
            onboard_cluster_action, onboard_cluster_type)
        action = getattr(self.wf_context, onboard_cluster_action)

        kw = {
            'current_browser': current_browser,
            'onboard_cluster_type': onboard_cluster_type,
            'action': action,
            'added_hwi': self.wf_context.added_hwi,
            'output': output
        }

        ClusterManager(
            self.cloud_administrator_onboard_cluster.__name__,
            method_name=_method_name,
            **kw
        ).run()

        RequestChecker(self.cloud_administrator_onboard_cluster.__name__,
                       description=_method_name).run()

        if output and len(output) == 1:
            onboard_cluster_entity = output[0]
            if onboard_cluster_type in ['LC1S', 'CA1S', 'CA2S', 'VS1S']:
                cluster = [onboard_cluster_entity.unprepared_cluster]
                if onboard_cluster_type in ['CA1S', 'CA2S']:
                    assert getattr(onboard_cluster_entity, 'hwi_host_pairs', None), \
                        'HWI-Host pair was not set back to context object in onboard CA cluster.'
                    setattr(self.wf_context, 'hwi_host_pairs', onboard_cluster_entity.hwi_host_pairs)
                    logger.info(
                        'Set HWI-Host pairs to context with value:{}'.format(
                            onboard_cluster_entity.hwi_host_pairs), False, True)
            if onboard_cluster_type in ['DR2S', 'MP2S', 'MP3S']:
                cluster = [onboard_cluster_entity.unprepared_protected_cluster,
                           onboard_cluster_entity.unprepared_recovery_cluster]
            setattr(self.wf_context, 'existed_clusters', cluster)
            logger.info('Onboarded cluster:{}'.format(self.wf_context.existed_clusters), False, True)

            # fill the storage and cluster, hwi name into added_cloud_storage for vs1s cluster.
            #     added_cloud_storage:
            #     -
            #     hwi_name: *hwi_name01
            #     cluster_name: *cluster_name
            #     name:
            #     []
            #     srp: []
            if onboard_cluster_type == 'VS1S':
                added_datastore = self.wf_context.added_cloud_storage
                added_datastore[0].hwi_name = onboard_cluster_entity.select_a_hwi
                added_datastore[0].cluster_name = onboard_cluster_entity.unprepared_cluster
                added_datastore[0].name = []
                added_datastore[0].srp = []

                datastore_list = GetDatastoreFromvRO().get_datastore_from_vro(
                    self.wf_context.vro, onboard_cluster_entity.select_a_hwi,
                    onboard_cluster_entity.unprepared_cluster)
                if datastore_list:
                    added_datastore[0].name.append(
                        sorted(datastore_list, key=lambda datastore: int(datastore.id))[-1].name)
                setattr(self.wf_context, 'added_cloud_storage', added_datastore)

    @catch_assert_exception
    def cloud_administrator_edits_cluster_site(self):
        current_browser = self.wf_context.shared.current_browser
        assert current_browser is not None, 'shared.current_browser is None.'
        assert current_browser.is_login, 'Please login to vRA, The flag is_login is False.'

        _method_name = ClusterManager.Func.EDIT_CLUSTER_SITE
        assert hasattr(self.wf_context, 'edit_cluster_site'), 'No item: edit_cluster_site in YAML.'

        action = getattr(self.wf_context, 'edit_cluster_site')
        for edit_cluster_site in action:
            kw = {
                'current_browser': current_browser,
                'edit_cluster_site': edit_cluster_site,
            }

            ClusterManager(self.cloud_administrator_edits_cluster_site.__name__,
                           method_name=_method_name,
                           **kw).run()

            RequestChecker(self.cloud_administrator_edits_cluster_site.__name__,
                           description=_method_name).run()

        if len(action) == 0:
            logger.info('No clusters need to edit site.', False, True)
            logger.info('[AUC] - "{}" - {}'.format(' '.join([word.capitalize() for word in
                                                             self.cloud_administrator_edits_cluster_site.__name__.split(
                                                                 '_')]),
                                                   'PASSED'), False, True)

    @catch_assert_exception
    def cloud_administrator_edits_cluster_hwi(self):
        current_browser = self.wf_context.shared.current_browser
        assert current_browser is not None, 'shared.current_browser is None.'
        assert current_browser.is_login, 'Please login to vRA, The flag is_login is False.'

        _method_name = ClusterManager.Func.EDIT_CLUSTER_HWI
        assert hasattr(self.wf_context, 'edit_cluster_hwi'), 'No item: edit_cluster_hwi in YAML.'

        action = getattr(self.wf_context, 'edit_cluster_hwi')
        for edit_cluster_hwi in action:
            kw = {
                'current_browser': current_browser,
                'edit_cluster_hwi': edit_cluster_hwi,
            }

            ClusterManager(self.cloud_administrator_edits_cluster_hwi.__name__,
                           method_name=_method_name,
                           **kw).run()

            RequestChecker(self.cloud_administrator_edits_cluster_hwi.__name__,
                           description=_method_name).run()

        if len(action) == 0:
            logger.info('No clusters need to edit hwi.', False, True)
            logger.info('[AUC] - "{}" - {}'.format(' '.join([word.capitalize() for word in
                                                             self.cloud_administrator_edits_cluster_hwi.__name__.split(
                                                                 '_')]),
                                                   'PASSED'), False, True)

    @catch_assert_exception
    def cloud_administrator_deletes_site(self):
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login
        if hasattr(self.wf_context, 'added_sites') and \
                self.wf_context.added_sites and \
                        len(self.wf_context.added_sites) >= 1:

            for site_name in self.wf_context.added_sites:
                description = 'delete site {0}'.format(site_name)
                kwargs = {
                    'current_browser': current_browser,
                    'is_login': is_login,
                    'site_name': site_name,
                    'description': description,
                }
                SiteManager(
                    self.cloud_administrator_deletes_site.__name__,
                    method_name=SiteManager.Func.DELETE_SITES,
                    **kwargs
                ).run()

                RequestChecker(self.cloud_administrator_deletes_site.__name__,
                               description=description).run()
        else:
            logger.error('No site is picked to be deleted in yaml.')

    @catch_assert_exception
    def cloud_administrator_edits_site(self):
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login

        if hasattr(self.wf_context, 'edit_sites') \
                and self.wf_context.edit_sites \
                and len(self.wf_context.edit_sites) >= 1:
            _edit_sites = self.wf_context.edit_sites
            for _edit_site in _edit_sites:
                _old_site_name = _edit_site.site_name
                _new_site_name = _edit_site.new_site_name
                description = 'edit site {0}'.format(_old_site_name)
                kwargs = {
                    'current_browser': current_browser,
                    'is_login': is_login,
                    'site_name': _old_site_name,
                    'new_site_name': _new_site_name,
                    'description': description,
                }
                SiteManager(
                    self.cloud_administrator_edits_site.__name__,
                    method_name=SiteManager.Func.EDIT_SITES,
                    **kwargs
                ).run()

                RequestChecker(
                    self.cloud_administrator_edits_site.__name__,
                    description=description
                ).run()

                if hasattr(self.wf_context, 'added_sites'):
                    if _new_site_name not in self.wf_context.added_sites and _old_site_name != _new_site_name:
                        if _old_site_name in self.wf_context.added_sites:
                            index = self.wf_context.added_sites.index(_old_site_name)
                            self.wf_context.added_sites[index] = _new_site_name
                        else:
                            self.wf_context.added_sites.append(_new_site_name)
                print 'added_sites : ', self.wf_context.added_sites
        else:
            logger.info('No site is picked to be edited in yaml.')

    @catch_assert_exception
    def cloud_administrator_edits_vcenter(self):
        current_browser = self.wf_context.shared.current_browser
        added_vcenter = self.wf_context.added_vcenter
        method_name = VCenterManager.Func.EDIT_VCENTER
        update_vcenter = self.wf_context.update_vcenter
        output = []
        update_vcenter_list = []
        if self.wf_context:
            assert current_browser is not None, 'current_browser in yaml is None, ' \
                                                'may be there is no active browser'
            assert current_browser.is_login, 'Please login to vRA, The flag value is_login is: False.'
            for item in update_vcenter:
                for key, value in item.__dict__.iteritems():
                    assert value is not None, 'yaml data of "{}" value is None'.format(key)
        for counter, item in enumerate(update_vcenter):
            kwargs = {
                'select_operation': item.select_operation,
                'existing_vcenter_object': item.existing_vcenter_object,
                'vcenter_name': item.vcenter_name,
                'vcenter_fqdn': item.vcenter_fqdn,
                'datacenter': item.datacenter,
                'sites': item.sites,
                'added_vcenter': added_vcenter,
                'current_browser': current_browser,
                'output': output,

            }
            VCenterManager(self.cloud_administrator_edits_vcenter.__name__,
                           method_name=method_name,
                           **kwargs).run()
            # check the request
            request_result = []
            RequestChecker(
                self.cloud_administrator_edits_vcenter.__name__,
                description=method_name,
                output=request_result
            ).run()

            if request_result and output:
                if request_result[-1].status == 'Successful':
                    update_vcenter_list.append(output[counter])
                else:
                    logger.error(
                        'the request status of edit vcenter:{name} is: {status}, the status detaial is: {status_detail}'
                        .format(
                            name=request_result[-1].description, status=request_result[-1].status,
                            status_detail=request_result[-1].status_details))

        for counter, item in enumerate(update_vcenter):
            if item.existing_vcenter_object in added_vcenter and item.vcenter_name in update_vcenter_list:
                added_vcenter[counter] = item.vcenter_name

        setattr(self.wf_context, 'added_vcenter', added_vcenter)

    def cloud_administrator_edits_avamar_grid(self):
        EditAvamarGrid(
            self.cloud_administrator_edits_avamar_grid.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_edits_avamar_grid_admin_full(self):
        EditAdminFull(
            self.cloud_administrator_edits_avamar_grid_admin_full.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_adds_backup_service_level_for_deploy_vm(self):
        current_browser = self.wf_context.shared.current_browser
        output = []
        bsl_to_add = []
        added_bsl = []
        if len(self.wf_context.add_backup_service_level) > 1:
            logger.warn('More than 1 entry is provided to create backup service level, only the first will '
                        'take effect!')
            bsl_to_add = self.wf_context.add_backup_service_level[:1]
        else:
            bsl_to_add = self.wf_context.add_backup_service_level
        for auc_context in bsl_to_add:
            description = auc_context.description
            reasons = auc_context.reasons
            bsl_name = auc_context.specify_the_service_level_name

            schedule_type = auc_context.select_backup_schedule
            schedule_start_time = auc_context.schedule_start_time
            schedule_week_number = auc_context.schedule_week_number
            schedule_weekday = auc_context.schedule_weekday
            backup_schedule = BSLSchedule(schedule_type, schedule_week_number, schedule_weekday, schedule_start_time)
            assert backup_schedule.validate_schedule(), 'Some backup schedule configuration is not valid'

            retention_policy = auc_context.regular_retention_policy
            retention_long_term_policy = auc_context.long_term_retention_policy
            retention_for_number = auc_context.retention_for_number
            retention_unit = auc_context.retention_unit
            retention_date = auc_context.retention_date
            retention_time = auc_context.retention_time
            retention_config = BSLRetention(retention_policy, retention_long_term_policy, retention_for_number,
                                            retention_unit, retention_date, retention_time)
            assert retention_config.validate_retention(), 'Some retention configuration is not valid'

            replication_schedule_type = auc_context.replication_schedule_type
            replication_week_number = auc_context.replication_week_number
            replication_weekday = auc_context.replication_weekday
            replication_start_time = auc_context.replication_start_time
            replication_schedule = BSLSchedule(replication_schedule_type, replication_week_number, replication_weekday,
                                               replication_start_time)
            assert replication_schedule.validate_schedule(), 'Some replication schedule configuration is not valid'

            kwargs = {
                'current_browser': current_browser,
                'backup_service_level_name': bsl_name,
                'description': description,
                'reasons': reasons,
                'backup_schedule': backup_schedule,
                'retention_schedule': retention_config,
                'replication_schedule': replication_schedule,
                'output': output,
            }
            AddBackupServiceLevel(
                self.cloud_administrator_adds_backup_service_level.__name__,
                **kwargs
            ).run()
        for request in output:
            if request.result.status == 'Successful':
                added_bsl.append(request.name)
                logger.info("Request succeeded with details: {}".format(request.result.status_details), True, True)
            else:
                logger.error("Request failed with details: {}".format(request.result.status_details), True)
        if not hasattr(self.wf_context.shared, 'backup_service_levels'):
            setattr(self.wf_context.shared, 'backup_service_levels', YAMLData())
            if not hasattr(self.wf_context.shared.backup_service_levels, 'for_deletion'):
                setattr(self.wf_context.shared.backup_service_levels, 'for_deletion', [])
        self.wf_context.shared.backup_service_levels.for_deletion.extend(added_bsl)
        assert len(added_bsl) == len(bsl_to_add), 'Some requests failed in creating backup service level, please check!'
        setattr(self.wf_context.added_backup_service_level, 'backup_to_operate_vm', added_bsl[0])

    def cloud_administrator_adds_backup_service_level_for_set_vm(self):
        current_browser = self.wf_context.shared.current_browser
        output = []
        bsl_to_add = []
        added_bsl = []
        if len(self.wf_context.add_backup_service_level) > 1:
            logger.warn('More than 1 entry is provided to create backup service level, only the first will '
                        'take effect!')
            bsl_to_add = self.wf_context.add_backup_service_level[:1]
        else:
            bsl_to_add = self.wf_context.add_backup_service_level
        for auc_context in bsl_to_add:
            description = auc_context.description
            reasons = auc_context.reasons
            bsl_name = auc_context.specify_the_service_level_name

            schedule_type = auc_context.select_backup_schedule
            schedule_start_time = auc_context.schedule_start_time
            schedule_week_number = auc_context.schedule_week_number
            schedule_weekday = auc_context.schedule_weekday
            backup_schedule = BSLSchedule(schedule_type, schedule_week_number, schedule_weekday, schedule_start_time)
            assert backup_schedule.validate_schedule(), 'Some backup schedule configuration is not valid'

            retention_policy = auc_context.regular_retention_policy
            retention_long_term_policy = auc_context.long_term_retention_policy
            retention_for_number = auc_context.retention_for_number
            retention_unit = auc_context.retention_unit
            retention_date = auc_context.retention_date
            retention_time = auc_context.retention_time
            retention_config = BSLRetention(retention_policy, retention_long_term_policy, retention_for_number,
                                            retention_unit, retention_date, retention_time)
            assert retention_config.validate_retention(), 'Some retention configuration is not valid'

            replication_schedule_type = auc_context.replication_schedule_type
            replication_week_number = auc_context.replication_week_number
            replication_weekday = auc_context.replication_weekday
            replication_start_time = auc_context.replication_start_time
            replication_schedule = BSLSchedule(replication_schedule_type, replication_week_number, replication_weekday,
                                               replication_start_time)
            assert replication_schedule.validate_schedule(), 'Some replication schedule configuration is not valid'

            kwargs = {
                'current_browser': current_browser,
                'backup_service_level_name': bsl_name,
                'description': description,
                'reasons': reasons,
                'backup_schedule': backup_schedule,
                'retention_schedule': retention_config,
                'replication_schedule': replication_schedule,
                'output': output,
            }
            AddBackupServiceLevel(
                self.cloud_administrator_adds_backup_service_level.__name__,
                **kwargs
            ).run()
        for request in output:
            if request.result.status == 'Successful':
                added_bsl.append(request.name)
                logger.info("Request succeeded with details: {}".format(request.result.status_details), True, True)
            else:
                logger.error("Request failed with details: {}".format(request.result.status_details), True)
        if not hasattr(self.wf_context.shared, 'backup_service_levels'):
            setattr(self.wf_context.shared, 'backup_service_levels', YAMLData())
            if not hasattr(self.wf_context.shared.backup_service_levels, 'for_deletion'):
                setattr(self.wf_context.shared.backup_service_levels, 'for_deletion', [])
        self.wf_context.shared.backup_service_levels.for_deletion.extend(added_bsl)
        assert len(added_bsl) == len(bsl_to_add), 'Some requests failed in creating backup service level, please check!'
        setattr(self.wf_context.added_backup_service_level, 'backup_to_set_backup_service', added_bsl[0])

    def cloud_administrator_deletes_backup_service_level_all(self):
        _busl_node = getattr(self.wf_context.shared, 'backup_service_levels', None)
        _added_busl_list = None
        if _busl_node:
            _added_busl_list = getattr(_busl_node, 'for_deletion')

        _method_name = BackupServiceLevelManager.Func.DELETE_BACKUP_SERVICE_LEVEL
        _cur_browser = self.wf_context.shared.current_browser.instance._browser
        if _added_busl_list and isinstance(_added_busl_list, list):
            _deleted_busl_list = []
            for _busl_name in _added_busl_list:
                BackupServiceLevelManager(
                    self.cloud_administrator_deletes_backup_service_level_all.__name__,
                    method_name=_method_name,
                    backup_service_level_name=_busl_name,
                    browser=_cur_browser
                ).run()
                request_result = []
                RequestChecker(self.cloud_administrator_deletes_backup_service_level_all.__name__,
                               description=_method_name,
                               output=request_result).run()
                if len(request_result) == 1 \
                        and (request_result[0].status == 'Successful'):
                    _deleted_busl_list.append(_busl_name)
            for item in _deleted_busl_list:
                _added_busl_list.remove(item)
            setattr(self.wf_context.shared.backup_service_levels, 'for_deletion', _added_busl_list)
            _busl_for_vm = getattr(_busl_node, 'for_deploy_vm', None)
            _busl_for_set = getattr(_busl_node, 'for_set_backup_service_level', None)
            if _busl_for_vm in _deleted_busl_list:
                setattr(_busl_node, 'for_deploy_vm', None)
                ### need to revise later
                if hasattr(self.wf_context, 'added_backup_service_level'):
                    setattr(self.wf_context.added_backup_service_level, 'backup_to_operate_vm', None)
            if _busl_for_set in _deleted_busl_list:
                setattr(_busl_node, 'for_set_backup_service_level', None)
                ### need to revise later
                if hasattr(self.wf_context, 'added_backup_service_level'):
                    setattr(self.wf_context.added_backup_service_level, 'backup_to_set_backup_service', None)
        else:
            BackupServiceLevelManager(
                self.cloud_administrator_deletes_backup_service_level_all.__name__,
                method_name=_method_name,
                backup_service_level_name=None,
                browser=_cur_browser
            ).run()

    def cloud_administrator_displays_backup_service_level_all(self):
        DisplayBackupServiceLevel(
            self.cloud_administrator_displays_backup_service_level_all.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def cloud_administrator_checks_protection_group_created_for_datastore(self):
        added_cloud_storage = getattr(self.wf_context, "added_cloud_storage", [])
        datastore = getattr(added_cloud_storage[0], "name", []) if added_cloud_storage else []
        if datastore:
            logger.info("******************************** Confirmation Required ***********************************",
                        False, True)
            logger.info("If protection groups for {} have been created,\n"
                        "please Enter 'YES' to continue:".format(datastore), False, True)
            confirm = raw_input()
            assert confirm.upper() == 'YES', 'Workflow task cancelled'
        else:
            logger.warn('No need to check protection group because of no storage provisioned.')

    def cloud_administrator_add_fabric_group(self, fg_name, admin_list):
        current_browser = self.wf_context.shared.current_browser
        assert current_browser is not None, 'current_browser in yaml is None. There is no active browser'

        params = {
            'fg_name': fg_name,
            'admin_list': admin_list,
            'current_browser': current_browser
        }

        FabricGroup(**params).run()

    def cloud_administrator_adds_avamar_site_relationship(self):
        sites = []
        added_asr = []
        description = 'test add an ASR'
        current_browser = self.wf_context.shared.current_browser
        assert current_browser is not None, \
            'Current browser is None, may be there is no active browser.'
        is_login = self.wf_context.shared.current_browser.is_login
        # assert is_login is True, "Can't do anything if you are not logged in."
        vro = self.wf_context.vro
        assert vro is not None, "Please provide vro."
        onboard_cluster_type = self.wf_context.onboard_cluster_type
        assert onboard_cluster_type in cluster_type_to_backup_env_type.keys(), \
            'The given onboard_cluster_type is invalid, it should be one of {}'.format(
                cluster_type_to_backup_env_type.keys())
        backup_env_type = cluster_type_to_backup_env_type.get(onboard_cluster_type)
        assert backup_env_type is not None, \
            'backup_env_type {0} is not valid, supported type:{1}'.format(
                backup_env_type, backup_env_type_map.keys())
        added_sites = self.wf_context.added_sites

        pick_sites_from_add_avamar_site_relationship = False
        if added_sites:
            sites.append(added_sites[0])
            logger.info('Retrieved first site: {} from added_sites.'.format(added_sites[0]), False, True)
        else:
            pick_sites_from_add_avamar_site_relationship = True
            assert self.wf_context.add_avamar_site_relationship.site_first is not None, \
                '"site_first" of add_avamar_site_relationship in YAML should not be None.'
            sites.append(self.wf_context.add_avamar_site_relationship.site_first)
            logger.info(
                'Retrieved first site: {} from YAML data add_avamar_site_relationship.'.format(
                    self.wf_context.add_avamar_site_relationship.site_first), False, True)

        if backup_env_type.startswith(backup_env_type_prefix_two_copies) or \
                backup_env_type.startswith(backup_env_type_prefix_three_copies) \
                or backup_env_type == "MC2VC":

            if pick_sites_from_add_avamar_site_relationship:
                assert self.wf_context.add_avamar_site_relationship.site_second is not None, \
                    '"site_second" of add_avamar_site_relationship in YAML should not None if added_sites is not valid.'
                sites.append(self.wf_context.add_avamar_site_relationship.site_second)
                logger.info('Retrieved second site: {} from YAML data add_avamar_site_relationship.'.format(
                    self.wf_context.add_avamar_site_relationship.site_second), False, True)
            else:
                assert len(added_sites) > 1, \
                    'There should be two sites added for backup_environment_type: {}'.format(backup_env_type)
                sites.append(added_sites[1])
                logger.info(
                    'Retrieved second site: {} from added_sites.'.format(added_sites[1]), False, True)
        if backup_env_type.startswith(
                backup_env_type_prefix_three_copies):
            if pick_sites_from_add_avamar_site_relationship:
                assert self.wf_context.add_avamar_site_relationship.site_third is not None, \
                    '"site_third" of add_avamar_site_relationship in YAML should not None if added_sites is not valid.'
                sites.append(self.wf_context.add_avamar_site_relationship.site_third)
                logger.info(
                    'Retrieved third site: {} from YAML data add_avamar_site_relationship.'.format(
                        self.wf_context.add_avamar_site_relationship.site_third), False, True)
            else:
                assert len(added_sites) == 3, \
                    'There should be three sites added for backup_environment_type: {}'.format(backup_env_type)
                sites.append(added_sites[2])
                logger.info(
                    'Retrieved third site: {} from added_sites.'.format(added_sites[2]),
                    False, True)

        (vro_response_dict, vro_rest_base) = VroItems(
            self.wf_context).get_all_items_from_vro(vro_constants.ASR_ISLAND_API)

        asr_exist_flag, asr_name = self._asr_is_able_to_add(
            vro_response_dict,
            vro_rest_base,
            backup_env_type,
            *sites
        )

        if asr_exist_flag:
            added_asr_obj = AvamarSiteRelationshipInfo(asr_name, backup_env_type, *sites)
            added_asr.append(added_asr_obj)
            logger.info('ASR: {} does not need to add again, put it in added_avamar_site_relationship directly.'
                        .format(added_asr_obj))
            logger.info(
                '[AUC] - "{}" - {}'.format(
                    ' '.join([word.capitalize() for word in
                              self.cloud_administrator_adds_avamar_site_relationship.__name__.split('_')]), 'PASSED'),
                False, True)

        else:
            kwargs = {
                'current_browser': current_browser,
                'backup_env_type': backup_env_type,
                'sites': sites,
                'description': description
            }

            ASRManager(
                self.cloud_administrator_adds_avamar_site_relationship.__name__,
                method_name=ASRManager.Func.ADD_ASR,
                **kwargs
            ).run()

            request_result = []
            RequestChecker(
                self.cloud_administrator_adds_avamar_site_relationship.__name__,
                description=description,
                output=request_result
            ).run()

            assert request_result, 'The request result is None.'
            assert request_result[0].status == 'Successful', 'The request status: {0}, detail info: {1}'.format(
                request_result[0].status, request_result[0].status_details)

            list_asr = REST_GetASRFromvRO().get_asr_from_vro(vro)
            assert list_asr is not None, 'ASR name from vRO is None.'
            asr_name = filter_latest_added_asr(list_asr, backup_env_type, *sites)
            assert asr_name is not None, 'Retrieving ASR name from vRO:{} failed'.format(vro.address)
            added_asr_obj = AvamarSiteRelationshipInfo(asr_name, backup_env_type, *sites)
            added_asr.append(added_asr_obj)

        setattr(self.wf_context, 'added_avamar_site_relationship', added_asr)
        logger.info('Added avamar_site_relationship: {} .'.format(added_asr_obj), False, True)

    def _asr_is_able_to_add(
            self, vro_response_dict, vro_rest_base, backup_env_type, *sites):
        asr_exist_flag = False
        asr_name = ''
        for item in vro_response_dict.get('relations', {}).get('link', []):
            item_attr = vro_rest_base.name_value_pairs_to_dict(item.get('attributes', {}))

            if backup_env_type == item_attr.get('asr_type') \
                    and item_attr.get('site1', '').lower() == (sites[0].lower() if len(sites) > 0 else '') \
                    and item_attr.get('site2', '').lower() == (sites[1].lower() if len(sites) > 1 else '') \
                    and item_attr.get('site3', '').lower() == (sites[2].lower() if len(sites) > 2 else ''):
                asr_name = item_attr.get('name')
                logger.debug("asr: {} already exist.".format(asr_name))
                asr_exist_flag = True
                break
        return asr_exist_flag, asr_name

    def cloud_administrator_edits_an_avamar_site_relationship(self):
        description = 'test edit an ASR'
        current_browser = self.wf_context.shared.current_browser
        assert current_browser is not None, \
            'Current browser is None, may be there is no active browser.'
        is_login = self.wf_context.shared.current_browser.is_login
        assert is_login is True, "Can't do anything if you are not logged in."
        vro = self.wf_context.vro
        assert vro is not None, "Please provide vro."
        added_asr = self.wf_context.added_avamar_site_relationship
        assert len(added_asr) > 0, \
            '"added_avamar_site_relationship" should not be None.'
        last_added_asr = added_asr[-1]
        backup_env_type = last_added_asr.backup_env_type
        sites = []
        edit_asr = self.wf_context.edit_avamar_site_relationship
        assert edit_asr.site_first is not None, \
            '"site_first" of edit_avamar_site_relationship in YAML file should not be None.'
        site_first = edit_asr.site_first
        sites.append(site_first)
        site_second = edit_asr.site_second if edit_asr.site_second else ''
        sites.append(site_second)
        site_third = edit_asr.site_third if edit_asr.site_third else ''
        sites.append(site_third)
        assert last_added_asr.asr_name is not None, '"asr_name" of added asr should not be None.'
        kwargs = {
            'current_browser': current_browser,
            'description': description,
            'added_asr': last_added_asr,
            'sites': sites
        }
        ASRManager(
            self.cloud_administrator_edits_an_avamar_site_relationship.__name__,
            method_name=ASRManager.Func.EDIT_ASR,
            **kwargs
        ).run()

        request_result = []
        RequestChecker(
            self.cloud_administrator_edits_an_avamar_site_relationship.__name__,
            description=description,
            output=request_result
        ).run()
        assert request_result, 'The request result is None.'
        assert request_result[0].status == 'Successful', 'The request status: {0}, detail info: {1}'.format(
            request_result[0].status, request_result[0].status_details)
        list_asr = REST_GetASRFromvRO().get_asr_from_vro(vro)
        assert list_asr is not None, 'ASR name from vRO is None.'
        asr_name = filter_latest_added_asr(list_asr, backup_env_type, *sites)
        assert asr_name is not None, 'Retrieving ASR name from vRO:{} failed'.format(vro.address)
        added_asr_obj = AvamarSiteRelationshipInfo(asr_name, backup_env_type, *sites)
        self.wf_context.added_avamar_site_relationship[-1] = added_asr_obj
        logger.info('Edited avamar_site_relationship: {} .'.format(added_asr_obj), False, True)

    def cloud_administrator_deletes_an_avamar_site_relationship(self):
        description = 'test delete ASR(s)'
        current_browser = self.wf_context.shared.current_browser
        assert current_browser is not None, \
            'Current browser is None, may be there is no active browser.'
        is_login = self.wf_context.shared.current_browser.is_login
        assert is_login is True, "Can't do anything if you are not logged in."
        added_asr_list = self.wf_context.added_avamar_site_relationship
        assert len(added_asr_list) > 0, \
            '"added_avamar_site_relationship" should not be None.'
        for item in added_asr_list:
            if not item.asr_name:
                logger.debug('The asr to delete is none, no need to delete.')
                continue
            kwargs = {
                'current_browser': current_browser,
                'description': description,
                'added_asr': item
            }
            ASRManager(
                self.cloud_administrator_deletes_an_avamar_site_relationship.__name__,
                method_name=ASRManager.Func.DELETE_ASR,
                **kwargs
            ).run()

            request_result = []
            RequestChecker(
                self.cloud_administrator_deletes_an_avamar_site_relationship.__name__,
                description=description,
                output=request_result
            ).run()
            assert request_result, 'The request result is None.'
            assert request_result[0].status == 'Successful', 'The request status: {0}, detail info: {1}'.format(
                request_result[0].status, request_result[0].status_details)

    def cloud_administrator_creates_reservation_policy_with_mapping(self):
        rsv_policys = []
        new_rsv_policy_description = 'create reservation policy'
        cur_browser = self.wf_context.shared.current_browser
        assert cur_browser is not None, 'current_browser in yaml is None, ' \
                                        'may be there is no active browser'
        assert hasattr(self.wf_context, 'create_reservation_policy'), \
            'Please add YAML Item: create_reservation_policy'
        assert hasattr(self.wf_context.create_reservation_policy, 'names') is True, \
            'Please add YAML Item: names in item create_reservation_policy'

        if len(self.wf_context.create_reservation_policy.names) > 0:
            _reservation_policys = self.wf_context.create_reservation_policy.names
            for reservation_policy in _reservation_policys:
                new_rsv_policy_name = reservation_policy
                output = []
                kw = {
                    'reservation_policy_name': new_rsv_policy_name,
                    'reservation_policy_description': new_rsv_policy_description,
                    'cur_browser': cur_browser,
                    'output': output
                }
                CreateReservationPolicy(
                    self.cloud_administrator_creates_reservation_policy_with_mapping.__name__,
                    'runTest',
                    **kw
                ).run()

                if output and len(output) == 1:
                    added_reservation_policy = output[0]
                    rsv_policys.append(added_reservation_policy)
            setattr(self.wf_context, 'added_reservation_policy', rsv_policys)
            assert hasattr(self.wf_context, 'workflow_relation_list'), \
                'workflow_relation_list should be in context object'
            workflow_relation_lists = self.wf_context.workflow_relation_list
            assert len(workflow_relation_lists) == len(rsv_policys), \
                'The count of reservation policy should equal to the count of relation mapping.'
            for i, mapping_obj in enumerate(workflow_relation_lists):
                mapping_obj.set_reservation_policy(rsv_policys[i])
        else:
            logger.error('No Reservation Policy need to add.', False)
            logger.info('[AUC] - "{}" - {}'.format(' '.join([word.capitalize() for word in
                                                             self.cloud_administrator_creates_reservation_policy.
                                                            __name__.split('_')]), 'FAILED'), False, True)

    def cloud_administrator_assigns_reservation_policy_to_blueprint_with_mapping(self):
        assigned_reservation_policy_blueprints = []
        current_browser = self.wf_context.shared.current_browser
        assert hasattr(self.wf_context, 'workflow_relation_list'), \
            'workflow_relation_list should be in context object'
        workflow_relation_list = self.wf_context.workflow_relation_list
        assert len(workflow_relation_list) > 0, 'workflow_relation_list should not be None.'
        for mapping_obj in workflow_relation_list:
            output = []
            assert mapping_obj.get_blueprint(), \
                'Blueprint name in mapping obj: {} should not be None.'.format(mapping_obj)
            assert mapping_obj.get_vsphere_machine_Id(), \
                'vsphere_machine_Id in mapping obj: {} should not be None.'.format(mapping_obj)
            assert mapping_obj.get_reservation_policy(), \
                'Reservation policy in mapping obj: {} should not be None.'.format(mapping_obj)
            kwargs = {
                'blueprint_name': mapping_obj.get_blueprint(),
                'machine_name': mapping_obj.get_vsphere_machine_Id(),
                'reservation_policy_name': mapping_obj.get_reservation_policy(),
                'current_browser': current_browser,
                'output': output
            }
            AssignReservationPolicyToBlueprint(
                self.cloud_administrator_assigns_reservation_policy_to_blueprint_with_mapping.__name__,
                **kwargs
            ).run()
            if output and len(output) == 1:
                assigned_blueprints = output[0]
                assigned_reservation_policy_blueprints.append(assigned_blueprints)
        setattr(self.wf_context, 'assigned_reservation_policy_blueprints', assigned_reservation_policy_blueprints)

    def cloud_administrator_assigns_datastores_and_reservation_policy_to_reservation_with_mapping(self):
        list_reservations_assigned_reservation_policy = []
        tenant_name = self.wf_context.vra.tenant
        assert tenant_name is not None, 'Please provide tenant.'
        current_browser = self.wf_context.shared.current_browser
        is_login = self.wf_context.shared.current_browser.is_login
        assert is_login is True, "Can't do anything if you didn't login."
        assert hasattr(self.wf_context, 'workflow_relation_list'), \
            'workflow_relation_list should be in context object'
        workflow_relation_list = self.wf_context.workflow_relation_list
        assert len(workflow_relation_list) > 0, 'workflow_relation_list should not be None.'
        assert hasattr(self.wf_context, 'added_cloud_storage'), 'added_cloud_storage should be in yaml file.'
        added_cloud_storage_list = self.wf_context.added_cloud_storage
        assert isinstance(added_cloud_storage_list, list), \
            'Added cloud storage is not list type.'
        assert len(added_cloud_storage_list) > 0, \
            'Target datastore(s) is not provided.'
        for mapping_obj in workflow_relation_list:
            assert mapping_obj.get_reservation(), \
                'reservation name in mapping obj: {} should not be None.'.format(mapping_obj)
            assert mapping_obj.get_reservation_policy() is not None, \
                'reservation policy in mapping obj: {} should not be None.'.format(mapping_obj)
            assert mapping_obj.get_cluster(), \
                'cluster name in mapping obj: {} should not be None.'.format(mapping_obj)
            provisioned_storage_list = []
            for added_cloud_storage in added_cloud_storage_list:
                assert added_cloud_storage.cluster_name, 'Cluster name should not be None.'
                if added_cloud_storage.cluster_name == mapping_obj.get_cluster():
                    provisioned_storage_list.append(added_cloud_storage)
            mapping_obj.update_storages(provisioned_storage_list)
            storages = [storage.name[0] for storage in provisioned_storage_list]
            output = []
            kwargs = {
                'current_browser': current_browser,
                'tenant_name': tenant_name,
                'reservation_name': mapping_obj.get_reservation(),
                'reservation_policy': mapping_obj.get_reservation_policy(),
                'storages': storages,
                'output': output
            }
            AssignDatastoresAndReservationPolicyToReservation(
                self.cloud_administrator_assigns_datastores_and_reservation_policy_to_reservation_with_mapping.__name__,
                **kwargs
            ).run()
            list_reservations_assigned_reservation_policy.append(output[-1])
        setattr(
            self.wf_context, 'assigned_reservation_policy_reservations',
            list_reservations_assigned_reservation_policy
        )


if __name__ == '__main__':
    pass