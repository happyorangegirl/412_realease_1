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

import sys
import time

from robot.api import logger

from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared import CatalogPage, RequestsPage, LoadingWindow
from ehc_e2e.auc.uimap.specific import BackupServiceLevelPage
from .backup_service_level_Intermediate_objects import BackupServiceLevelResult, BackupServiceLevelSharedObj, \
    AddedBackupServiceLevelCollection


def get_backup_service_level_name_prefix(keyword_method_name, counter_of_add):
    bksl_name_prefix = ('deploy-' if 'deploy_vm' in keyword_method_name else 'set-') if any(
        post_fix in keyword_method_name for post_fix in ['deploy_vm', 'set_vm']) else (
    'deploy-' if counter_of_add == 0 else 'set-')

    return bksl_name_prefix


class AddBackupServiceLevel(BaseUseCase):
    _ACTION = "Add Backup Service Level"
    """
    Add Backup Service Level

    Caveats!!!
    if keyword_separate_deploy_vm_and_set is True, then we need to specify keyword_method_name. This way,
    we will write context.added_backup_service
    We assume the first added backup service level will be used as backup_to_operate_vm,
    following added backup service levels are considered as being used for set_backup_service
    and will only update added_backup_service_level.set_backup_service
    """
    def __init__(self, name=None, method_name='runTest', **kwargs):
        super(AddBackupServiceLevel, self).__init__(name, method_name, **kwargs)
        self._validate_context(**kwargs)
        self.failure_formatter = 'Running on step: "Add Backup Service Level"-FAILED, {}'
        self.keyword_separate_deploy_vm_and_set = kwargs.get('separate_deploy_vm_and_set', False)
        self.keyword_method_name = name
        self.loading_window = LoadingWindow()
        self.add_backup_service_level_page = BackupServiceLevelPage()

    def test_add_backup_service_level(self):
        catalog_page = CatalogPage()
        timestamp = time.strftime('-%H%M%S')
        bksl_name_prefix = get_backup_service_level_name_prefix(self.keyword_method_name, 1)
        self.backup_svc_level_name = bksl_name_prefix + self.backup_svc_level_name + timestamp
        self.description = self.description + ': ' + self.backup_svc_level_name
        self.assertTrue(catalog_page.navigate_to_catalog(self.current_browser),
                        self.failure_formatter.format('failed to switch to catalog frame.'))

        try:
            self.add_backup_service_level_page.data_protection_services.click()
            self.assertTrue(
                catalog_page.btn_backup_service_level_request.exists(),
                self.failure_formatter.format('backup service level maintenance button does not exist.')
            )
            catalog_page.btn_backup_service_level_request.click()
            self.loading_window.wait_loading(self.current_browser, 30)
        except:
            logger.error('Try to open backup service level maintenance encounters error:{}.'.format(sys.exc_info()))
            raise

        try:
            self.assertTrue(
                self.add_backup_service_level_page.txt_description.exists(),
                self.failure_formatter.format(
                    '"description" textbox does not exist.')
            )
            self.add_backup_service_level_page.txt_description.set(self.description)
            self.add_backup_service_level_page.txt_reasons.set(self.reasons)
            self.loading_window.wait_loading(self.current_browser, 30)
            self.add_backup_service_level_page.btn_next.click()
            self.assertTrue(
                self.add_backup_service_level_page.btn_delete_backup_service_level.exists(),
                self.failure_formatter.format('failed to navigate to "Select Action" page')
            )
            self.add_backup_service_level_page.btn_add_backup_service_level.click()
            self.assertTrue(
                self.add_backup_service_level_page.click_drop_down_list(
                    self.add_backup_service_level_page.parent_element, "tr",
                    AddBackupServiceLevel._ACTION),
                self.failure_formatter.format(
                    '"{}" does not exist in Action dropdownlist.'.format(
                        AddBackupServiceLevel._ACTION
                    )
                )
            )
            self.loading_window.wait_loading(self.current_browser, 30)
            logger.info('Completed "Chose Action" page.', False, True)
            self.add_backup_service_level_page.btn_next.click()
            self.loading_window.wait_loading(self.current_browser, 30)

            self._set_backup_schedule()
            self._set_retention_schedule()
            self._set_replication_schedule()

            # Review and Submit page.
            self.add_backup_service_level_page.btn_next.click()
            
            self.loading_window.wait_loading(self.current_browser, 30)
            self.assertTrue(
                self.add_backup_service_level_page.btn_submit.exists(),
                self.failure_formatter.format('Navigate to Review and Submit page')
            )
            self.add_backup_service_level_page.btn_submit.click()

        except AssertionError:
            self.add_backup_service_level_page.save_request()
            raise
        except:
            self.add_backup_service_level_page.save_request()
            self.fail(
                self.failure_formatter.format(
                    'encounters error, more error info: {}'.format(
                        sys.exc_info()))
            )

        self.assertTrue(self.add_backup_service_level_page.lab_confirmation_success.exists(),
                        self.failure_formatter.format(
                            'after clicking submit button, cannot find the label: '
                            'The request has been submitted successfully.'))
        self.add_backup_service_level_page.btn_ok.click()
        # switch to request
        self.assertTrue(
            RequestsPage().navigate_to_request(self.current_browser),
            self.failure_formatter.format('switch to request frame failed.')
        )

        # check the request and set the refresh interval to 1 minute
        request_result = RequestsPage().get_request_result(self.description, slp=60)
        self.assertIsNotNone(
            request_result, self.failure_formatter.format('failed to get the request result.')
        )

        add_bkl_result = BackupServiceLevelResult(self.backup_svc_level_name, request_result)
        self.add_backup_service_level_results.append(add_bkl_result)

    def _set_backup_schedule(self):
        # Backup Schedule page.
        self.assertTrue(
            self.add_backup_service_level_page.txt_backup_service_name.exists(),
            self.failure_formatter.format('"Backup Service Level" textbox does not exit.')
        )
        self.add_backup_service_level_page.txt_backup_service_name.set(
            self.backup_svc_level_name
        )
        self.loading_window.wait_loading(self.current_browser, 30)
        logger.info('Input Backup service level name:{}'.format(self.backup_svc_level_name), False, True)

        self.assertTrue(
            self.add_backup_service_level_page.btn_select_a_schedule.exists(),
            msg=self.failure_formatter.format('failed to navigate to Backup Schedule page')
        )
        bk_schedule = self.backup_schedule.schedule_type.capitalize()
        self.add_backup_service_level_page.btn_select_a_schedule.click()
        self.loading_window.wait_loading(self.current_browser, 30)
        self.assertTrue(
            self.add_backup_service_level_page.click_drop_down_list(
                self.add_backup_service_level_page.parent_element, 'div', bk_schedule),
            self.failure_formatter.format('failed to select Schecule:{} from dropdown list.'.format(bk_schedule))
        )
        self.loading_window.wait_loading(self.current_browser, 30)
        if bk_schedule == 'Daily':
            self.add_backup_service_level_page.txt_start_time.set(self.backup_schedule.schedule_start_time)
        else:
            if bk_schedule == 'Monthly':
                self.add_backup_service_level_page.btn_week_number.click()
                item_week_number = self.backup_schedule.schedule_week_number.capitalize()
                self.assertTrue(
                    self.add_backup_service_level_page.click_drop_down_list(
                        self.add_backup_service_level_page.parent_element, "div", item_week_number),
                    self.failure_formatter.format(
                        'Week number:{} not found in drop-down list.'.format(self.backup_schedule.schedule_week_number))
                )
            self.loading_window.wait_loading(self.current_browser, 30)
            self.add_backup_service_level_page.btn_weekday.click()
            item_weekday = self.backup_schedule.schedule_weekday.capitalize()
            self.assertTrue(
                self.add_backup_service_level_page.click_drop_down_list(
                    self.add_backup_service_level_page.parent_element, "div", item_weekday),
                self.failure_formatter.format(
                    'Weekday:{} not found in drop-down list.'.format(self.backup_schedule.schedule_weekday))
            )
        logger.info('Completed "Backup Schedule" page.', False, True)
        self.loading_window.wait_loading(self.current_browser, 30)
        self.add_backup_service_level_page.btn_next.click()
        self.loading_window.wait_loading(self.current_browser, 30)

    def _set_retention_schedule(self):
        # Retention Policy page.
        self.assertTrue(
            self.add_backup_service_level_page.btn_regular_retention_policy.exists(),
            self.failure_formatter.format(
                'Retention Policy drop-down list open button does not exist.')
        )
        self.add_backup_service_level_page.btn_regular_retention_policy.click()
        self.assertTrue(
            self.add_backup_service_level_page.click_drop_down_list(
                self.add_backup_service_level_page.parent_element, "div", self.retention_schedule.retention_policy),
            self.failure_formatter.format(
                'Retention Policy:{} not found in drop-down list.'.format(self.retention_schedule.retention_policy)
            )
        )

        # we hardcocde default values.
        self.loading_window.wait_loading(self.current_browser, 30)
        if self.retention_schedule.retention_policy == 'For':
            self.assertTrue(
                self.add_backup_service_level_page.txt_retention_for_number.exists(),
                self.failure_formatter.format('"Retention Number Of" textbox does not exist.')
            )
            self.add_backup_service_level_page.txt_retention_for_number.set(self.retention_schedule.retention_number)
            self.add_backup_service_level_page.btn_retention_custom_phrase.click()
            self.assertTrue(
                self.add_backup_service_level_page.click_drop_down_list(
                    self.add_backup_service_level_page.parent_element, "div", self.retention_schedule.retention_unit),
                self.failure_formatter.format('"Retention Units" does not exist.')
            )
        elif self.retention_schedule.retention_policy == 'Until':
            self.assertTrue(
                self.add_backup_service_level_page.txt_retention_date.exists(),
                self.failure_formatter.format('"Retention Date " textbox does not exist.')
            )
            self.add_backup_service_level_page.txt_retention_date.set(self.retention_schedule.retention_date)
            self.assertTrue(
                self.add_backup_service_level_page.txt_retention_time.exists(),
                self.failure_formatter.format('"Retention Time " textbox does not exist.')
            )
            self.add_backup_service_level_page.txt_retention_time.set(self.retention_schedule.retention_time)

        self.loading_window.wait_loading(self.current_browser, 30)
        self.assertTrue(
            self.add_backup_service_level_page.txt_long_term_retention_policy.exists(),
            self.failure_formatter.format('"Long Term Retention (Years)" does not exist.')
        )
        self.add_backup_service_level_page.txt_long_term_retention_policy.set(self.retention_schedule.long_term_retention_year)
        logger.info('Completed "Backup Schedule" page.', False, True)
        self.add_backup_service_level_page.btn_next.click()
        self.loading_window.wait_loading(self.current_browser, 30)

    def _set_replication_schedule(self):
        # Replication Schedule page.
        self.assertIsNotNone(
            self.add_backup_service_level_page.btn_select_replication_schedule.
                current.location_once_scrolled_into_view,
            self.failure_formatter.format('can not scroll "replication schedule" into view.')
        )
        self.assertTrue(
            self.add_backup_service_level_page.btn_select_replication_schedule.exists(),
            self.failure_formatter.format('failed to navigate to Replication Schedule page')
        )
        self.add_backup_service_level_page.btn_select_replication_schedule.click()
        replication_schedule = self.replication_schedule.schedule_type.capitalize()
        self.assertTrue(
            self.add_backup_service_level_page.click_drop_down_list(
                self.add_backup_service_level_page.parent_element, "div", replication_schedule),
            self.failure_formatter.format(
                'Replication Schedule:{} not found in drop-down list.'.format(replication_schedule)
            )
        )
        self.loading_window.wait_loading(self.current_browser, 30)
        if self.replication_schedule.schedule_type == 'Daily':
            self.assertTrue(
                self.add_backup_service_level_page.txt_replication_start_time.exists(),
                self.failure_formatter.format(
                    'Editbox to open "Replication Start time" not found.')
            )
            self.add_backup_service_level_page.txt_replication_start_time.set(self.replication_schedule.schedule_start_time)
        else:
            if self.replication_schedule.schedule_type == 'Monthly':
                self.assertTrue(
                    self.add_backup_service_level_page.btn_replication_week_number.exists(),
                    self.failure_formatter.format(
                        'Drop-down list to open "Replication week number" not found.')
                )
                self.add_backup_service_level_page.btn_replication_week_number.click()
                self.assertTrue(
                    self.add_backup_service_level_page.click_drop_down_list(
                        self.add_backup_service_level_page.parent_element, "div",
                        self.replication_schedule.schedule_week_number
                    ), self.failure_formatter.format(
                        'Replication Week day:{} not found in dropdownlist.'.format(self.replication_schedule.schedule_week_number))
                )
            self.assertTrue(
                self.add_backup_service_level_page.btn_replication_week_day.exists(),
                self.failure_formatter.format(
                    'button to open "Replication Week day" drop-down list not found.')
            )
            self.loading_window.wait_loading(self.current_browser, 30)
            self.add_backup_service_level_page.btn_replication_week_day.click()
            replication_week_day = self.replication_schedule.schedule_weekday.capitalize()
            self.assertTrue(
                self.add_backup_service_level_page.click_drop_down_list(
                    self.add_backup_service_level_page.parent_element, "div",
                    replication_week_day
                ), self.failure_formatter.format(
                    'Replication Week day:{} not found in drop-down list.'.format(replication_week_day))
            )
        self.loading_window.wait_loading(self.current_browser, 30)
        logger.info('Completed Replication Schedule page.', False, True)

    def runTest(self):
        self.test_add_backup_service_level()

    def _validate_context(self, **kwargs):
        self.current_browser = kwargs.get('current_browser')
        assert self.current_browser is not None, self.failure_formatter.format('current_browser in yaml is None')
        self.select_operation = AddBackupServiceLevel._ACTION
        self.backup_svc_level_name = kwargs.get('backup_service_level_name')
        self.description = kwargs.get('description')
        self.reasons = kwargs.get('reasons')
        self.backup_schedule = kwargs.get('backup_schedule')
        self.retention_schedule = kwargs.get('retention_schedule')
        self.replication_schedule = kwargs.get('replication_schedule')
        self.add_backup_service_level_results = kwargs.get('output')

    def _finalize_context(self):
        pass
        # backup_flag = True
        # added_backup_service_level_collection = AddedBackupServiceLevelCollection()
        # if not hasattr(self.ctx_out, 'added_backup_service_level'):
        #     setattr(self.ctx_out, 'added_backup_service_level', added_backup_service_level_collection)
        # if not hasattr(self.ctx_out.shared, 'backup_service_levels'):
        #     setattr(self.ctx_out.shared, 'backup_service_levels', BackupServiceLevelSharedObj())
        # for index, backup_item in enumerate(self.add_backup_service_level_results):
        #     if backup_item.result.status == 'Failed':
        #         backup_flag = False
        #         logger.error(
        #             'the request status of Add Backup Service Level:{name} is: {status}, the status detaial is: '
        #             '{status_detail}'.format(
        #                 name=backup_item.result.description,
        #                 status=backup_item.result.status,
        #                 status_detail=backup_item.result.status_details)
        #         )
        #     else:
        #
        #         if self.keyword_separate_deploy_vm_and_set is True:
        #             if 'for_deploy_vm' in self.keyword_method_name:
        #                 setattr(
        #                     self.ctx_out.added_backup_service_level, 'backup_to_operate_vm', backup_item.name)
        #                 logger.info(
        #                     'Added backup service level:{} for deploy vm.'.format(backup_item.name),
        #                     False, True)
        #             elif 'for_set_vm' in self.keyword_method_name:
        #                 setattr(
        #                     self.ctx_out.added_backup_service_level, 'backup_to_set_backup_service', backup_item.name)
        #                 logger.info(
        #                     'Added backup service level:{} for set backup service level.'.format(
        #                         backup_item.name), False, True)
        #             else:
        #                 # This should not be called.
        #                 logger.warn(
        #                     'We do not support this call from baseworkflow. calling keyword method '
        #                     'is:{}, it should specify keyword_separate_deploy_vm_and_set to True'.format(
        #                         self.keyword_method_name)
        #                 )
        #         else:
        #             bksl_for_deploy_vm = getattr(self.ctx_in.added_backup_service_level, 'backup_to_operate_vm', None)
        #             if not bksl_for_deploy_vm:
        #                 # if we have not set backup_to_operate_vm, just set it.
        #                 setattr(
        #                     self.ctx_out.added_backup_service_level, 'backup_to_operate_vm', backup_item.name)
        #                 logger.info(
        #                     'Added backup service level:{} for deploy vm.'.format(backup_item.name), False, True)
        #             elif getattr(self.ctx_out.shared.backup_service_levels, 'for_deletion', None) and \
        #                             bksl_for_deploy_vm not in self.ctx_out.shared.backup_service_levels.for_deletion:
        #                 # This maybe that the added_backup_service_level.backup_to.operate_vm already has value
        #                 # configure in disk yaml file, in this case, we will not use it, will use this workflow
        #                 # generated insttead.
        #                 setattr(
        #                     self.ctx_out.added_backup_service_level, 'backup_to_operate_vm', backup_item.name)
        #                 logger.info(
        #                     'Data from backup_to_operate_vm is not generated by this workflow run, use the workflow '
        #                     'newly added backup service level:{} for deploy vm.'.format(backup_item.name),
        #                     False, True
        #                 )
        #             else:
        #                 setattr(
        #                     self.ctx_out.added_backup_service_level, 'backup_to_set_backup_service', backup_item.name)
        #                 logger.info(
        #                     '"backup_to_operate_vm" already set, put added backup service level:{} for set backup '
        #                     'service level.'.format(backup_item.name), False, True)
        #
        #         # add those backup service levels into shared.backup_service_levels.for_deletion, this list keeps all
        #         # backup service levels for later deletion.
        #         if getattr(self.ctx_out.shared.backup_service_levels, 'for_deletion', None):
        #             self.ctx_out.shared.backup_service_levels.for_deletion.append(backup_item.name)
        #             logger.info(
        #                 'Stored backup service level:{} into shared.backup_service_levels.for_deletion.'
        #                 ''.format(backup_item.name), False, True
        #             )
        #         else:
        #             setattr(
        #                 self.ctx_out.shared.backup_service_levels, 'for_deletion', [backup_item.name])
        #             logger.info(
        #                 'Stored backup service level:{} into shared.backup_service_levels.for_deletion.'
        #                 ''.format(backup_item.name), False, True
        #             )
        #
        # # Make sure we cleared them up after use.
        # self.add_backup_service_level_results[:] = []
        # self.assertTrue(
        #     backup_flag, self.failure_formatter.format('the request results contain error.')
        # )
