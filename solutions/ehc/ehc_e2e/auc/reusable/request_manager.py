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

from unittest import TestCase

from ehc_e2e.auc.uimap.shared.generic import ServicesMaintenancePage


class RequestManager(object):
    def __init__(self, case_owner):
        if case_owner and isinstance(case_owner, TestCase):
            self._case_checker = case_owner
        else:
            raise RuntimeError('Unable to validate page objects')

        self.svc_maintenance_page = ServicesMaintenancePage()

    def save_unsubmitted_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self.svc_maintenance_page.frm_catalog:
            if not self.svc_maintenance_page.lnk_all_services.exists() and (
                    self.svc_maintenance_page.btn_save.exists()):
                self.svc_maintenance_page.btn_save.click()

            self._case_checker.assertTrue(
                self.svc_maintenance_page.lnk_all_services.exists(),
                msg=_formatter(step='Show all services after saving request'))

    def cancel_request_submission(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self.svc_maintenance_page.frm_catalog:
            if not self.svc_maintenance_page.lnk_all_services.exists() and (
                    self.svc_maintenance_page.btn_cancel.exists()):
                self.svc_maintenance_page.btn_cancel.click()

            self._case_checker.assertTrue(
                self.svc_maintenance_page.lnk_all_services.exists(),
                msg=_formatter(step='Show all services after cancelling request submission'))
