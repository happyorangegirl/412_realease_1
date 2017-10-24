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

# pylint: disable=fixme, protected-access, too-few-public-methods, too-many-instance-attributes

import sys
import random

from selenium.webdriver.common.keys import Keys
from robot.api import logger

from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared import BasePage, CatalogPage, LoadingWindow
from ehc_e2e.auc.uimap.specific import DeployVMPage

from ehc_e2e.auc.reusable import context_util
from ehc_e2e.auc.reusable import close_relaunch_browser_operation


def arithmetic_progression_sequence_random_integer(low, high, increment):
    l = [(low + increment * i) for i in xrange((high - low) / increment + 1) if (low + increment * i) <= high]
    return l[random.randint(0, len(l) - 1)] if l else [low]


def get_value_range_from_range_text(range_text):
    """
    :param range_text: (Select 512-8192)
    :return: a tuple of (min, max)
    """
    current = 0
    numbers = []
    for c in range_text:
        if ord('0') <= ord(c) <= ord('9'):
            current = current * 10 + int(c)
        elif current > 0:
            numbers.append(current)
            current = 0
        else:
            continue
    return min(numbers), max(numbers)


class DeployVmParallel(BaseUseCase):
    # """
    #         Test deploying VMs from blueprints
    # """
    class Func(object):
        DEPLOY_VM_PARALLEL_NO_DP, DEPLOY_VM_PARALLEL_DP, DEPLOY_VM_PARALLEL_DR_NO_DP, DEPLOY_VM_PARALLEL_DR_DP, \
        DEPLOY_VM_PARALLEL_RP4VM_NO_DP, DEPLOY_VM_PARALLEL_RP4VM_DP = (
            'test_deploy_vm_parallel_no_dp', 'test_deploy_vm_parallel_dp', 'test_deploy_vm_parallel_dr_no_dp',
            'test_deploy_vm_parallel_dr_dp', 'test_deploy_vm_parallel_rp4vm_no_dp', 'test_deploy_vm_parallel_rp4vm_dp')

    deployed_vms = []
    _formatter_without_dp = 'Running on step:"Deploy VM parallel"- FAILED, {}.'
    _formatter_with_dp = 'Running on step:"Deploy VM parallel with DP"- FAILED, {}.'
    _formatter = ''
    DEPLOYVM_DP_BACKUP_SVC_LEVEL_NAME_PATTERN = r'^deploy-.*?-\d{6}'

    def __init__(self, name=None, method_name=Func.DEPLOY_VM_PARALLEL_NO_DP, **kwargs):
        super(DeployVmParallel, self).__init__(name, method_name, **kwargs)
        _auc_name = ' '.join([word.capitalize() for word in name.split('_')])
        self._formatter = ('Running on step: ' + _auc_name + ' - FAILED, {}')
        self._validate_init_input(**kwargs)
        self._init_page_objects()

    def _init_page_objects(self):
        self.catalog_page = CatalogPage()
        self.base_page = BasePage()
        self.loading_window = LoadingWindow()

    def _init_deploy_vm_page(self):
        self.deploy_vm_page = DeployVMPage()

    def test_deploy_vm_parallel_no_dp(self):
        self._deploy_vm_request_open(self._blueprint_name)
        self._init_deploy_vm_page()
        self._deploy_vm_request_switch_to_edit_area()
        self._deploy_vm_request_fill_edit_textboxes()
        if self._srp:
            self._deploy_vm_request_set_storage_resrevation_policy()
        else:
            logger.warn('Storage Reservation Policy is empty for storage:{}, will not set.'.format(self._storage))
        self._deploy_vm_request_submit_ok()

    def test_deploy_vm_parallel_dp(self):
        self._deploy_vm_request_open(self._blueprint_name)
        self._init_deploy_vm_page()
        self._deploy_vm_request_switch_to_edit_area()
        self._deploy_vm_request_fill_edit_textboxes()
        self._deploy_vm_request_set_backup_svc_level()
        if self._srp:
            self._deploy_vm_request_set_storage_resrevation_policy()
        else:
            logger.warn('Storage Reservation Policy is empty for storage:{}, will not set.'.format(self._storage))
        self._deploy_vm_request_submit_ok()

    def test_deploy_vm_parallel_dr_no_dp(self):
        self._deploy_vm_request_open(self._blueprint_name)
        self._init_deploy_vm_page()
        self._deploy_vm_request_switch_to_edit_area()
        self._deploy_vm_request_fill_edit_textboxes()
        self._deploy_vm_request_set_srm_power_on_priority()
        if self._srp:
            self._deploy_vm_request_set_storage_resrevation_policy()
        else:
            logger.warn('Storage Reservation Policy is empty for storage:{}, will not set.'.format(self._storage))
        self._deploy_vm_request_submit_ok()

    def test_deploy_vm_parallel_dr_dp(self):
        self._deploy_vm_request_open(self._blueprint_name)
        self._init_deploy_vm_page()
        self._deploy_vm_request_switch_to_edit_area()
        self._deploy_vm_request_fill_edit_textboxes()
        self._deploy_vm_request_set_backup_svc_level()
        self._deploy_vm_request_set_srm_power_on_priority()
        if self._srp:
            self._deploy_vm_request_set_storage_resrevation_policy()
        else:
            logger.warn('Storage Reservation Policy is empty for storage:{}, will not set.'.format(self._storage))
        self._deploy_vm_request_submit_ok()

    def test_deploy_vm_parallel_rp4vm_no_dp(self):
        self._deploy_vm_request_open(self._blueprint_name)
        self._init_deploy_vm_page()
        self._deploy_vm_request_switch_to_edit_area()
        self._deploy_vm_request_fill_edit_textboxes()
        self._deploy_vm_request_set_rp4vm_properties()
        if self._srp:
            self._deploy_vm_request_set_storage_resrevation_policy()
        else:
            logger.warn('Storage Reservation Policy is empty for storage:{}, will not set.'.format(self._storage))
        self._deploy_vm_request_submit_ok()

    def test_deploy_vm_parallel_rp4vm_dp(self):
        self._deploy_vm_request_open(self._blueprint_name)
        self._init_deploy_vm_page()
        self._deploy_vm_request_switch_to_edit_area()
        self._deploy_vm_request_fill_edit_textboxes()
        self._deploy_vm_request_set_rp4vm_properties()
        self._deploy_vm_request_set_backup_svc_level()
        if self._srp:
            self._deploy_vm_request_set_storage_resrevation_policy()
        else:
            logger.warn('Storage Reservation Policy is empty for storage:{}, will not set.'.format(self._storage))
        self._deploy_vm_request_submit_ok()

    def _validate_init_input(self, **kwargs):
        self._blueprint_name = kwargs.get('blueprint_name')
        self._description = kwargs.get('description')
        self._reason_for_request = kwargs.get('reason')
        self._num_of_vm = kwargs.get('num_of_vm')
        self._backup_service_level = kwargs.get('backup_service_level')
        self._vsphere_machine_id = kwargs.get('vsphere_machine_id')
        self._browser_type = kwargs.get('browser_type')
        self._current_browser = kwargs.get('current_browser')
        self._cpu_max = kwargs.get('cpu_max', 0)
        self._ram_max = kwargs.get('ram_max', 512)
        self._srm_power_on_priority = kwargs.get('srm_power_on_priority')
        self._rp4vm_boot_priority = kwargs.get('rp4vm_boot_priority')
        self._rp4vm_policy = kwargs.get('rp4vm_policy')
        self._rp4vm_cg = kwargs.get('rp4vm_cg')
        self._srp = kwargs.get('storage_reservation_policy')
        self._assign_srp = kwargs.get('assign_srp')
        self._storage = kwargs.get('storage')

    def _deploy_vm_request_open(self, blueprint_name):
        self.assertTrue(
            self.catalog_page.navigate_to_catalog(self._current_browser),
            msg=self._formatter.format('switch to catalog page failed.'))

        self.assertTrue(
            self.catalog_page.txt_search.exists(),
            msg=self._formatter.format('Catalog service search button does not exist.'))
        self.catalog_page.txt_search.set(blueprint_name)
        logger.info(
            'Input: {0} in {1} search textbox'.format(
                blueprint_name, self.catalog_page.__class__.__name__))
        self.catalog_page.btn_search.click()
        logger.info(
            'Clicked search button in {} search textbox'.format(self.catalog_page.__class__.__name__))

        self.catalog_page.btn_blueprint_request = self.catalog_page.retrieve_blueprint_request_buttons(
            blueprint_name).get(blueprint_name)
        try:
            self.assertTrue(
                self.catalog_page.btn_blueprint_request.exists(), msg=self._formatter.format(
                    'request button does not exist for blueprint: {}'.format(blueprint_name)))
        except AssertionError:
            logger.info('Exit deploy vm since blueprint: {} is not found.'.format(blueprint_name), False, True)
            self.catalog_page.txt_search.set('')
            raise

        self.catalog_page.btn_blueprint_request.click()
        logger.info('Clicked request button in blueprint {}'.format(blueprint_name), False, True)

        # Benson: We have a commond loading window and a mask loading window after clicking
        # the deploy vm request from catalog page.
        self.loading_window.wait_loading(self._current_browser, timeout=60)
        self.loading_window.wait_loading_deploy_vm_page(self._current_browser, timeout=60)

    def _deploy_vm_request_switch_to_edit_area(self):
        self._init_deploy_vm_page()
        try:
            _is_switched_edit = self.deploy_vm_page.switch_to_edit_areas(self._current_browser)
            if not _is_switched_edit:
                logger.warn('Switch to deploy vm edit page failed, try to close and relaunch '
                            'browser for a second attempt.')
                close_relaunch_browser_operation()
                self._current_browser = context_util.get_last_baseworkflow_instance().wf_context.shared.current_browser
                logger.info('Re-instantiating catalogpage, basepage and deployvmpage.', False, True)
                self._init_page_objects()
                logger.info('Done re-instantiate catalogpage, basepage and deployvmpage.', False, True)
                self._deploy_vm_request_open(self._blueprint_name)
                _is_switched_edit = self.deploy_vm_page.switch_to_edit_areas(self._current_browser)

            self.assertTrue(_is_switched_edit, msg=self._formatter.format('switch to deploy vm edit page failed.'))

        except:
            logger.error('Encounters exception, exception details: {}'.format(sys.exc_info()))
            raise

    def _deploy_vm_request_fill_edit_textboxes(self):
        # reason for request.
        if self._reason_for_request and self.deploy_vm_page.txt_reason_for_request.exists():
            self.deploy_vm_page.txt_reason_for_request.set(self._reason_for_request)
            logger.info('Input: {} in description textbox'.format(self._reason_for_request), False, True)

        # If set description after machines, the description textbox
        # reference will become stale.
        if self.deploy_vm_page.txt_desc.exists():
            self.deploy_vm_page.txt_desc.set(self._description)
            logger.info('Input: {} in description textbox'.format(self._description), False, True)

        # Wenda: UI change in Badger. need to click machines button first then set the number of VMs
        self.assertTrue(
            self.deploy_vm_page.open_vsphere_blueprint(self._vsphere_machine_id),
            msg=self._formatter.format('failed to open designated vSphere blueprint')
        )

        self.assertTrue(
            self.deploy_vm_page.txt_instances.exists(),
            msg=self._formatter.format('cannot find instances textbox'))
        # original clear method is not working here as expected.
        # if we don't "click" btn_num_machines_down
        # the input will start with default value 1.
        # This work around cleared the default value in machines.
        default_instances_num = int(self.deploy_vm_page.txt_instances.current.get_attribute('value'))

        if self._num_of_vm != default_instances_num:
            logger.info(
                'num_of_vm provided in YAML is different with default value {0}. Use num_of_vm'.format(
                    default_instances_num), False, True)

            self.assertTrue(
                self.deploy_vm_page.txt_instances.current.get_attribute('readonly') != 'true',
                msg=self._formatter.format('failed to deploy VMs. Cannot set number of instances, textbox is readonly'))

            self.deploy_vm_page.btn_instances_down.click()
            self.deploy_vm_page.txt_instances.set(Keys.BACKSPACE)
            self.deploy_vm_page.txt_instances.set(self._num_of_vm)
            self.base_page.wait_for_loading_complete(1)

            if self.deploy_vm_page.txt_instances.current.get_attribute('data-errorqtip'):
                logger.error('Number of instances out of range..')
                raise AssertionError(
                    'Failed to deploy VM. specified "Number of instances":"{}" is out of range'.format(self._num_of_vm))
            logger.info('Set number of instances to: {}'.format(self._num_of_vm), False, True)

        else:
            logger.info('num_of_vm provided in YAML is same with default value: {0}. No need to change..'.format(
                default_instances_num))

        # setting CPU and Memory.
        self._deploy_vm_set_cpu_or_ram(
            'cpu', 1, 1, self._cpu_max, self.deploy_vm_page.txt_cpu, self.deploy_vm_page.lbl_cpu_range,
            self.deploy_vm_page.btn_cpu_up, self._blueprint_name)

        self._deploy_vm_set_cpu_or_ram(
            'ram', 512, 512, self._ram_max, self.deploy_vm_page.txt_ram, self.deploy_vm_page.lbl_ram_range,
            self.deploy_vm_page.btn_ram_up, self._blueprint_name)

    def _deploy_vm_set_cpu_or_ram(
            self, name_of_value_to_set, range_init_value, range_inrement, range_config_max,
            txt_element_to_set, lbl_range_element, btn_edit_up_element, blueprint):
        range_min = range_max = range_init_value
        if txt_element_to_set.current.get_attribute('readonly') == 'true':
            logger.warn(
                '{} is not configured for editing in current blueprint:{}, default value is:"{}", will not edit it.'
                ''.format(name_of_value_to_set, blueprint, txt_element_to_set.current.get_attribute('value')
                )
            )
        else:
            if lbl_range_element.exists() and lbl_range_element.value:
                range_min, range_max = get_value_range_from_range_text(lbl_range_element.value)
                logger.info('{} range is:"{}-{}"'.format(name_of_value_to_set, range_min, range_max), False, True)
                if range_config_max < range_min or range_config_max > range_max:
                    logger.warn(
                        '{}_max from yaml config is:{}, out of blueprint configured range:"{}-{}", will directly use '
                        'configured range'.format(name_of_value_to_set, range_config_max, range_min, range_max))
            actual_value_to_set = arithmetic_progression_sequence_random_integer(range_min, range_max, range_inrement)
            name_of_value_to_set = 'Memory(MB)' if 'ram' in name_of_value_to_set else name_of_value_to_set
            logger.info(
                'Trying to input "{}" with a randomly selected number:"{}"'.format(
                    name_of_value_to_set, actual_value_to_set),
                False, True
            )
            if btn_edit_up_element.exists():
                btn_edit_up_element.click()
            # TODO: This is not working now, need further investigation anyway.
            # self.assertTrue(
            #     self.deploy_vm_page.txt_cpu.exists(), self._formatter.format('Edit box for "CPUs:" does not exit.'))
            if txt_element_to_set.exists():
                self.base_page.wait_for_loading_complete(1)
                txt_element_to_set.set(actual_value_to_set)
                logger.info(
                    'Completed input "{}" with "{}"'.format(name_of_value_to_set, actual_value_to_set), False, True)

    def _deploy_vm_request_set_srm_power_on_priority(self):
        # set SRM priority
        if self._srm_power_on_priority:
            logger.info('Tring to select SRM power on priority:{}'.format(self._srm_power_on_priority), False, True)
            self.assertTrue(
                self.deploy_vm_page.btn_srm_drop_down.exists(),
                msg=self._formatter.format(
                    'cannot find SRM drop down list, Remove SRM_power_on_priority value or field in YAML if you do not'
                    ' need to set SRM priority')
            )
            self.deploy_vm_page.btn_srm_drop_down.click()
            self.assertTrue(
                self.deploy_vm_page.click_drop_down_list(
                    self.deploy_vm_page.lnk_srm_drop_down_list, 'li', str(self._srm_power_on_priority)),
                msg=self._formatter.format(
                    'failed to select SRM priority in the drop down list. Please verify the value "{}" exists in the '
                    'list. Remove SRM_power_on_priority value or field in YAML if you do not need to set SRM priority'
                    ''.format(self._srm_power_on_priority))
            )
            logger.info('Selected SRM power on priority:"{}"'.format(str(self._srm_power_on_priority)), False, True)

    def _deploy_vm_request_set_backup_svc_level(self):
        # DP = True. set Backup Service Level
        self.base_page.wait_for_loading_complete(5)
        logger.info('Tring to select backup service level:{}'.format(self._backup_service_level), False, True)
        if self._browser_type == 'firefox':
            # firefox has problem to select item of li type element in ul dropdownlist
            # TODO: figure out a reliable solution later.
            self.assertTrue(
                self.deploy_vm_page.btn_bkp_input.exists(),
                msg=self._formatter.format('backup service level textbox does not exist.'))
            self.deploy_vm_page.btn_bkp_input.set(self._backup_service_level)
            logger.info('Finished setting backup service level: {}.'.format(self._backup_service_level), False, True)
        else:
            self.assertTrue(
                self.deploy_vm_page.btn_bkp_drop_down.exists(),
                msg=self._formatter.format('cannot find Backup Service Level drop down list'))
            self.deploy_vm_page.btn_bkp_drop_down.click()
            self.assertTrue(
                self.deploy_vm_page.click_drop_down_list(
                    self.deploy_vm_page.lbl_drop_down_list, 'li', self._backup_service_level),
                msg=self._formatter.format(
                    'failed to select Backup Service Level in the drop down list. Please verify if "{}" exists'.format(
                        self._backup_service_level)
                )
            )
        logger.info('Selected backup service level:{}'.format(self._backup_service_level), False, True)
        self.deploy_vm_page.wait_for_loading_complete(5)

    def _wait_for_rp4vm_present(self, timeout):
        import time
        from ehc_e2e.auc.reusable.context_util import get_driver
        while self.deploy_vm_page.txt_ehc_rp4vm_cg.is_read_only and timeout:
            time.sleep(1)
            logger.info('Waiting 1 sec for the rp4vm items to be editable.', False, True)
            timeout -= 1
        if timeout == 0:
            logger.warn('Wait for RP4VM items to be editable exceeded timeout of :{}'.format(timeout))
            return False
        return True

    def _deploy_vm_request_set_rp4vm_properties(self):
        if self._rp4vm_policy:
            logger.info('RP4VM Policy is provided as: {}, will set it.'.format(self._rp4vm_policy), False, True)
            self.assertTrue(
                self.deploy_vm_page.btn_ehc_rp4vm_policy_drop_down.exists(),
                self._formatter.format('EHC RP4VM Policy dropdown open button does not exists')
            )
            self.assertTrue(
                self._wait_for_rp4vm_present(30), msg=self._formatter.format('waiting for RP4VM items to edit failed'))
            self.deploy_vm_page.btn_ehc_rp4vm_policy_drop_down.click()
            self.assertTrue(
                self.deploy_vm_page.click_drop_down_list(
                    self.deploy_vm_page.lbl_drop_down_list, 'li', self._rp4vm_policy),
                msg=self._formatter.format(
                    'failed to select rp4vm policy in the drop down list. Please verify if "{}" exists'.format(
                        self._rp4vm_policy)
                )
            )
            logger.info('Done setting RP4VM Policy to : {}'.format(self._rp4vm_policy), False, True)

        if self._rp4vm_cg:
            logger.info('RP4VM CG is provided as: {}, will set it.'.format(self._rp4vm_cg), False, True)
            self.assertTrue(
                self.deploy_vm_page.txt_ehc_rp4vm_cg.exists(),
                self._formatter.format('EHC RP4VM Policy input box does not exists'))
            self.deploy_vm_page.txt_ehc_rp4vm_cg.set(self._rp4vm_cg)
            logger.info('Done setting RP4VM CG to : {}'.format(self._rp4vm_cg), False, True)

        self.assertTrue(
            self.deploy_vm_page.txt_ehc_rp4vm_boot_priority.exists(),
            self._formatter.format('EHC RP4VM BootPriority input textbox does not exist.')
        )
        self.deploy_vm_page.txt_ehc_rp4vm_boot_priority.set(self._rp4vm_boot_priority)
        logger.info('Done setting rp4vm boot priority to :{}'.format(self._rp4vm_boot_priority), False, True)

    def _deploy_vm_request_set_storage_resrevation_policy(self):
        self.assertTrue(
            self.deploy_vm_page.lnk_storage_tab.exists(), self._formatter.format('"Storage tab does not exists"')
        )
        self.deploy_vm_page.lnk_storage_tab.click()
        logger.info('Clicked "Storage" tab to try to assign storage reservation policy.', False, True)
        BasePage().wait_for_loading_complete(1)
        self.assertTrue(self.deploy_vm_page.lnk_storage_first_row.exists(),
            self._formatter.format('storage reservation policy first item does not exist.'))
        self.deploy_vm_page.lnk_storage_first_row.click()
        self.assertTrue(self.deploy_vm_page.btn_storage_edit.exists(),
            self._formatter.format('storage resevation policy edit button does not exist.'))
        self.deploy_vm_page.btn_storage_edit.click()
        BasePage().wait_for_loading_complete(1)
        logger.info('Clicked "Edit" icon done, should open assign storage reservation policy edit box.', False, True)
        self.assertTrue(self.deploy_vm_page.btn_storage_reservation_policy_dropdownlist_open.exists(),
            self._formatter.format('storage reservation policy dropdown open button does not exist.'))
        self.deploy_vm_page.btn_storage_reservation_policy_dropdownlist_open.click()
        BasePage().wait_for_loading_complete(1)
        logger.info('clicked button for storage reservation policy dropdownlist.', False, True)
        self.assertTrue(
            BasePage().click_drop_down_list(
                self.deploy_vm_page.lnk_storage_reservation_policy_dropdownlist, 'li', self._srp),
            self._formatter.format('select storage reservation policy: {} from dropdownlist.'.format(self._srp)
            )
        )

        self.assertTrue(
            self.deploy_vm_page.btn_ok_in_floating_window.exists(),
            self._formatter.format('Storage reservation policy set OK button does not exist')
        )
        self.deploy_vm_page.btn_ok_in_floating_window.click()
        logger.info('Storage reservation policy {} is found and set.'.format(self._srp), False, True)

    def _deploy_vm_request_submit_ok(self):
        self.deploy_vm_page.switch_to_service_gadget_frame(self._current_browser)
        self.assertTrue(
            self.deploy_vm_page.btn_submit.exists(), msg=self._formatter.format('submit button does not exist'))

        self.deploy_vm_page.btn_submit.click()
        logger.info('Clicked submit button in blueprint {} request page.'.format(self._blueprint_name))

        self._current_browser.instance._browser.current.implicitly_wait(10)

        if self.catalog_page.lbl_success.exists():
            self.catalog_page.btn_ok.click()
            logger.info('Clicked request successful OK button.')
        else:
            switched_edit_after_submit = self.deploy_vm_page.switch_to_edit_areas(self._current_browser)
            if switched_edit_after_submit:
                logger.info(
                    'Trying to detect if the error label appears after submit successful label not found.', False, True)
                self._current_browser.instance._browser.current.implicitly_wait(2)
                if self.deploy_vm_page.lbl_error_request_form.exists():
                    logger.error('Deploy vm request has some fields not set properly, submit button will not proceed.')
                self._current_browser.instance._browser.current.implicitly_wait(30)
            from ehc_e2e.utils.snapshot import SnapShot
            SnapShot.takes_screen_shot()
            raise AssertionError(
                self._formatter.format(
                    'submit button failed to proceed to "The request has been submitted successfully" page'))

        self._current_browser.instance._browser.current.implicitly_wait(30)
