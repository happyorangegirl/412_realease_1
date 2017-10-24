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

from ehc_e2e.auc.uimap.shared.generic import TenantMainPage


class PageNavigator(object):
    def __init__(self, case_owner):
        if case_owner and isinstance(case_owner, TestCase):
            self._case_checker = case_owner
        else:
            raise RuntimeError('Unable to validate page objects')

        self.main_page = TenantMainPage()

    def go_to_catalog_page(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        self.main_page.lnk_catalog.parent.switch_to.default_content()

        self._case_checker.assertTrue(
            self.main_page.lnk_catalog.exists(),
            msg=_formatter(step='Navigate to Catalog page')
        )
        self.main_page.lnk_catalog.click()

    def go_to_requests_page(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        self.main_page.lnk_requests.parent.switch_to.default_content()

        self._case_checker.assertTrue(
            self.main_page.lnk_requests.exists(),
            msg=_formatter(step='Navigate to Requests page')
        )
        self.main_page.lnk_requests.click()

    def go_to_items_page(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        self.main_page.lnk_items.parent.switch_to.default_content()

        self._case_checker.assertTrue(
            self.main_page.lnk_items.exists(),
            msg=_formatter(step='Navigate to Items page')
        )
        self.main_page.lnk_items.click()
