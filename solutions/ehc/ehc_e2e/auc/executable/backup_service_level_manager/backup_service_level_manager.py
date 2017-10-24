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


import time
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.reusable import LoadingPopupWaiter, PageNavigator, RequestManager
from ehc_e2e.auc.uimap.specific.busl import CatalogPage, BackupServiceLevelPage


class BackupServiceLevelManager(BaseUseCase):
    class Func(object):
        ADD_BACKUP_SERVICE_LEVEL, DELETE_BACKUP_SERVICE_LEVEL, DISPLAY_BACKUP_SERVICE_LEVEL = (
            'test_adding_backup_service_level',
            'test_deleting_backup_service_level',
            'test_displaying_backup_service_level'
        )

    def __init__(self, name=None, method_name=Func.ADD_BACKUP_SERVICE_LEVEL, **kwargs):
        super(BackupServiceLevelManager, self).__init__(
            name, method_name, **kwargs)

    def setUp(self):
        self.navigator = PageNavigator(self)
        self._request_page = BackupServiceLevelPage()
        if hasattr(self, '_browser'):
            self.wait_loading = LoadingPopupWaiter(self, browser=self._browser)
        else:
            self.wait_loading = LoadingPopupWaiter(self, browser=None)
        self._added_backup_service_level = None

    def tearDown(self):
        RequestManager(self).save_unsubmitted_request()

    def test_deleting_backup_service_level(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._delete_backup_service_level()
        self._submit_request()

    def test_adding_backup_service_level(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._add_backup_service_level()
        self._submit_request()

    def test_displaying_backup_service_level(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._display_backup_service_level()
        self._submit_request()

    def _start_new_service_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.navigator.go_to_catalog_page()
        time.sleep(2)

        _catalog_page = CatalogPage()

        with _catalog_page.frm_catalog:
            self.assertTrue(
                _catalog_page.lnk_data_protection_services.exists(),
                msg=_formatter(
                    step='Validate side bar button Data Protection Services'
                ))

            _catalog_page.lnk_data_protection_services.click()
            self.assertTrue(
                _catalog_page.btn_backup_service_level_maintenance.exists(),
                msg=_formatter(
                    step='Validate Request button of RP4VM vRPA Cluster Maintenance')
            )
            time.sleep(2)
            _catalog_page.btn_backup_service_level_maintenance.click()

    def _fill_out_request_info(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self._request_page.frm_catalog:
            self.assertTrue(
                self._request_page.txt_description.exists(60),
                msg=_formatter(step='Display Description text box')
            )

            self._request_page.txt_description.set(self._testMethodName)
            self._request_page.txt_reasons.set(self._name)

            self._request_page.btn_next.click()

    def _add_backup_service_level(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self._request_page.frm_catalog:
            self.assertTrue(
                self._request_page.cbo_operation.exists(60),
                msg=_formatter(step='Display Operation dropdown list')
            )
            self._request_page.cbo_operation.select(by_visible_text='Add Backup Service Level')
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.txt_busl_to_add.set(self._backup_service_level_name)
            self._request_page.btn_next.click()
            self.wait_loading.wait_for_popup_loading_finish()

            self.assertTrue(self._request_page.cbo_bkup_schedule_type.exists(),
                            msg=_formatter(step='Display schedule comboBox'))
            self._request_page.cbo_bkup_schedule_type.select(
                by_visible_text=self._bkup_schedule_dict.get('schedule_type'))
            self.wait_loading.wait_for_popup_loading_finish()

            if self._bkup_schedule_dict.get('schedule_type') == 'Daily':
                self._request_page.txt_bkup_daily_time.set(self._bkup_schedule_dict.get('time'))
            elif self._bkup_schedule_dict.get('schedule_type') == 'Weekly':
                self._request_page.cbo_bkup_weekly_day.select(by_visible_text=self._bkup_schedule_dict.get('day'))
            else:
                self._request_page.cbo_bkup_monthly_week.select(by_visible_text=self._bkup_schedule_dict.get('week'))
                self._request_page.cbo_bkup_weekly_day.select(by_visible_text=self._bkup_schedule_dict.get('day'))
            self._request_page.btn_next.click()
            self.wait_loading.wait_for_popup_loading_finish()

            self.assertTrue(self._request_page.cbo_retention_policy.exists(),
                            msg=_formatter(step='Display retention policy comboBox'))
            self._request_page.cbo_retention_policy.select(by_visible_text=self._retention_policy.get('policy_name'))
            self.wait_loading.wait_for_popup_loading_finish()
            if self._retention_policy.get('policy_name') == 'thisSchedule':
                self._request_page.txt_retention_adv_daily.set(self._retention_policy.get('daily_number'))
                self._request_page.cbo_retention_dv_daily_unit.select(
                    by_visible_text=self._retention_policy.get('daily_unit'))
                self._request_page.txt_retention_adv_weekly.set(self._retention_policy.get('weekly_number'))
                self._request_page.cbo_retention_dv_weekly_unit.select(
                    by_visible_text=self._retention_policy.get('weekly_unit'))
                self._request_page.txt_retention_adv_monthly.set(self._retention_policy.get('monthly_number'))
                self._request_page.cbo_retention_dv_monthly_unit.select(
                    by_visible_text=self._retention_policy.get('monthly_unit'))
                self._request_page.txt_retention_adv_yearly.set(self._retention_policy.get('yearly_number'))
                self._request_page.cbo_retention_dv_yearly_unit.select(
                    by_visible_text=self._retention_policy.get('yearly_unit'))
            elif self._retention_policy.get('policy_name') == 'until':
                self._request_page.txt_retention_until_date.set(self._retention_policy.get('until_date'))
                self._request_page.txt_retention_until_time.set(self._retention_policy.get('until_time'))
            elif self._retention_policy.get('policy_name') == 'for':
                self._request_page.txt_retention_for_number.set(self._retention_policy.get('for_number'))
                self._request_page.cbo_retention_for_units.select(
                    by_visible_text=self._retention_policy.get('for_units'))
            else:
                pass
            self._request_page.txt_long_term_retention_years.set(
                self._retention_policy.get('long_term_retention_years'))
            self._request_page.btn_next.click()
            self.wait_loading.wait_for_popup_loading_finish()

            self.assertTrue(self._request_page.cbo_rp_schedule_type.exists(),
                            msg=_formatter(step='Display replication schedule type comboBox'))
            self._request_page.cbo_rp_schedule_type.select(by_visible_text=self._rp_schedule_dict.get('schedule_type'))
            self.wait_loading.wait_for_popup_loading_finish()

            if self._rp_schedule_dict.get('schedule_type') == 'Daily':
                self._request_page.txt_rp_daily_time.set(self._rp_schedule_dict.get('time'))
            elif self._rp_schedule_dict.get('schedule_type') == 'Weekly':
                self._request_page.cbo_rp_weekly_day.select(by_visible_text=self._rp_schedule_dict.get('day'))
            else:
                self._request_page.cbo_rp_monthly_week.select(by_visible_text=self._rp_schedule_dict.get('week'))
                self.wait_loading.wait_for_popup_loading_finish()
                self._request_page.cbo_rp_weekly_day.select(by_visible_text=self._rp_schedule_dict.get('day'))
            self._request_page.btn_next.click()

    def _delete_backup_service_level(self):

        _formatter = 'Running on step: "{step}" - FAILED'.format
        with self._request_page.frm_catalog:
            self.assertTrue(
                self._request_page.cbo_operation.exists(60),
                msg=_formatter(step='Display Operation dropdown list')
            )
            self._request_page.cbo_operation.select(by_visible_text='Delete Backup Service Level')

            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(
                self._request_page.btn_next.exists(60),
                msg=_formatter(step='Find Next button.')
            )
            self._request_page.btn_next.click()
            self.assertTrue(
                self._request_page.cbo_busl_to_delete.exists(60),
                msg=_formatter(step='Select Backup Service Level to delete')
            )
            self._request_page.cbo_busl_to_delete.select(by_visible_text=self._backup_service_level_name)
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.cbo_confirm.select(by_visible_text='Confirm')
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.btn_next.click()

    def _display_backup_service_level(self):

        _formatter = 'Running on step: "{step}" - FAILED'.format
        with self._request_page.frm_catalog:
            self.assertTrue(
                self._request_page.cbo_operation.exists(60),
                msg=_formatter(step='Display Operation dropdown list')
            )
            self._request_page.cbo_operation.select(by_visible_text='Display Backup Service Levels')

            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.btn_next.click()
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.btn_next.click()
            self.assertTrue(self._request_page.lbl_review_action.exists(),
                            msg=_formatter(step='Display action review label'))

    def _submit_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        with self._request_page.frm_catalog:
            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(self._request_page.btn_submit.exists(),
                            msg=_formatter(step='Click submit button'))

            self._request_page.btn_submit.click()

        with self._request_page.frm_catalog:
            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(self._request_page.lbl_success_msg.exists(),
                            msg='Failed to submit request')
            self._request_page.btn_ok.click()
            if self._testMethodName == self.Func.ADD_BACKUP_SERVICE_LEVEL:
                self._added_backup_service_level = self._backup_service_level_name

    def _validate_input_args(self, **kwargs):
        if self._testMethodName == self.Func.ADD_BACKUP_SERVICE_LEVEL:
            self._validate_args_of_adding_backup_service_level(**kwargs)
        elif self._testMethodName == self.Func.DELETE_BACKUP_SERVICE_LEVEL:
            self._validate_args_of_deleting_backup_service_level(**kwargs)
        elif self._testMethodName == self.Func.DISPLAY_BACKUP_SERVICE_LEVEL:
            self._validate_args_of_displaying_backup_service_level(**kwargs)
        else:
            pass

    def _finalize_output_params(self):
        if self._testMethodName == self.Func.ADD_BACKUP_SERVICE_LEVEL and self._added_backup_service_level:
            self._output.append(self._added_backup_service_level)
        else:
            pass

    def _validate_args_of_adding_backup_service_level(self, backup_service_level_name, backup_schedule_dict,
                                                      replication_schedule_dict, retention_policy_dict, browser=None):
        _formatter = 'Validate input parameter: "{step}" - FAILED'.format

        self.assertTrue((isinstance(backup_service_level_name, basestring) and backup_service_level_name.strip()),
                        msg=_formatter(step='backup_service_level_name'))
        self._backup_service_level_name = backup_service_level_name

        self.__validate_args_of_schedule_dict(backup_schedule_dict, 'backup_schedule_dict')
        self._bkup_schedule_dict = backup_schedule_dict

        self.__validate_args_of_schedule_dict(replication_schedule_dict, 'replication_schedule_dict')
        self._rp_schedule_dict = replication_schedule_dict

        self.__validate_args_of_retention_policy_dict(retention_policy_dict, 'retention_policy_dict')
        self._retention_policy = retention_policy_dict
        self._browser = browser

    def __validate_args_of_schedule_dict(self, schedule_dict, schedule_dict_name):
        _formatter = 'Validate input parameter: "{step}" - FAILED'.format
        _schedule_type = ['Daily', 'Weekly', 'Monthly']
        _weekly_day = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        _monthly_week = ['first', 'second', 'third', 'fourth', 'last']

        self.assertTrue((isinstance(schedule_dict, dict) and
                         (schedule_dict.get('schedule_type', None) in _schedule_type)),
                        msg=_formatter(step=schedule_dict_name))
        _schedule_type = schedule_dict.get('schedule_type')
        if _schedule_type == 'Daily':
            self.assertTrue(schedule_dict.get('time', None),
                            msg=_formatter(step=schedule_dict_name + '["time"]'))
        elif _schedule_type == 'Weekly':
            self.assertTrue((schedule_dict.get('day', None) in _weekly_day),
                            msg=_formatter(step=schedule_dict_name + '["day"]'))
        else:
            self.assertTrue((schedule_dict.get('week', None) in _monthly_week),
                            msg=_formatter(step=schedule_dict_name + '["week"]'))
            self.assertTrue((schedule_dict.get('day', None) in _weekly_day),
                            msg=_formatter(step=schedule_dict_name + '["day"]'))

    def __validate_args_of_retention_policy_dict(self, dict_entity, dict_name):
        _formatter = 'Validate input parameter: "{step}" - FAILED'.format
        _retention_policy_type = ['forever', 'for', 'until', 'thisSchedule']
        _for_units = ['days', 'weeks', 'months', 'years']

        self.assertTrue((isinstance(dict_entity, dict) and
                         (dict_entity.get('policy_name', None) in _retention_policy_type)),
                        msg=_formatter(step=dict_name))
        _policy_name = dict_entity.get('policy_name')
        if _policy_name == 'for':
            self.assertTrue(str(dict_entity.get('for_number', None)).isdigit(),
                            msg=_formatter(step=dict_name + '["for_number"]'))
            self.assertTrue((dict_entity.get('for_units', None) in _for_units),
                            msg=_formatter(step=dict_name + '["for_units"]'))
        elif _policy_name == 'until':
            self.assertTrue(str(dict_entity.get('until_date', None)).strip(),
                            msg=_formatter(step=dict_name + '["until_date"]'))
            self.assertTrue(str(dict_entity.get('until_time', None)).strip(),
                            msg=_formatter(step=dict_name + '["until_time"]'))
        elif _policy_name == 'thisSchedule':
            self.assertTrue(str(dict_entity.get('daily_number', None)).isdigit(),
                            msg=_formatter(step=dict_name + '["daily_number"]'))
            self.assertTrue((dict_entity.get('daily_unit', None) in _for_units),
                            msg=_formatter(step=dict_name + '["daily_unit"]'))
            self.assertTrue(str(dict_entity.get('weekly_number', None)).isdigit(),
                            msg=_formatter(step=dict_name + '["weekly_number"]'))
            self.assertTrue((dict_entity.get('weekly_unit', None) in _for_units),
                            msg=_formatter(step=dict_name + '["weekly_unit"]'))
            self.assertTrue(str(dict_entity.get('monthly_number', None)).isdigit(),
                            msg=_formatter(step=dict_name + '["monthly_number"]'))
            self.assertTrue((dict_entity.get('monthly_unit', None) in _for_units),
                            msg=_formatter(step=dict_name + '["monthly_unit"]'))
            self.assertTrue(str(dict_entity.get('yearly_number', None)).isdigit(),
                            msg=_formatter(step=dict_name + '["yearly_number"]'))
            self.assertTrue((dict_entity.get('yearly_unit', None) in _for_units),
                            msg=_formatter(step=dict_name + '["yearly_unit"]'))
        else:
            pass
        self.assertTrue(str(dict_entity.get('long_term_retention_years', None)).isdigit(),
                        msg=_formatter(step=dict_name + '["long_term_retention_years"]'))

    def _validate_args_of_deleting_backup_service_level(self, backup_service_level_name, browser=None):
        self.assertTrue((isinstance(backup_service_level_name, basestring) and backup_service_level_name.strip()),
                        msg='Validate input parameter: "backup_service_level_name" - FAILED')
        self._backup_service_level_name = backup_service_level_name
        self._browser = browser

    def _validate_args_of_displaying_backup_service_level(self, browser=None):
        self._browser = browser
