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

import sys
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared import ItemPage, BasePage
from ehc_e2e.auc.uimap.shared import LoadingWindow
from ehc_e2e.auc.uimap.specific import OperateVMPage
from ehc_e2e.auc.uimap.shared import MainPage
from robot.api import logger


class OnDemandBackupVM(BaseUseCase):
    """
    TAF-445: AUC-14 Day2 Operation - On Demand Backup
    """
    _formatter = 'Running on step: "On Demand Restore" - FAILED, {step}'

    def test_on_demand_backup(self):
        try:
            self.items_page = ItemPage(self.current_browser)
            self.loading_window = LoadingWindow()

            self.operatevm_page = OperateVMPage(self._deployed_vm)
            self.assertTrue(self.navigate_to_items_page(self.current_browser),
                            msg=self._formatter.format(step='switch to items page'))
            self._switch_to_target_item_frame()

            # In case of the items is empty, refresh it
            self.assertTrue(
                self.operatevm_page.btn_machine.exists(),
                msg=self._formatter.format(step='the button Machine does not exist.')
            )
            self.operatevm_page.btn_machine.click()
            self.operatevm_page.wait_for_loading_complete(5)
            if not self.operatevm_page.lnk_test_vm.exists():
                self.operatevm_page.btn_refresh_item.click()
                self.operatevm_page.wait_for_loading_complete(10)

            self.assertTrue(self.operatevm_page.lnk_test_vm.exists(),
                            msg=self._formatter.format(step='the vm {} does not exist.'.format(self._deployed_vm)))
            logger.debug('Clicking enable on demand backup button to fill the description & reason')
            self.operatevm_page.lnk_test_vm.click()
            self.loading_window.wait_loading(self.current_browser, 30)

            self.assertTrue(self.operatevm_page.btn_on_demand_backup.exists(),
                            msg=self._formatter.format(step='OnDemandBackup button does not exist'))
            self.operatevm_page.btn_on_demand_backup.click()
            self.loading_window.wait_loading(self.current_browser, 30)

            self.assertTrue(self.operatevm_page.txt_description.exists(),
                            msg=self._formatter.format(step='Description input box does not exist'))
            self.operatevm_page.txt_description.set(self._description)

            self.assertTrue(self.operatevm_page.txt_reasons.exists(),
                            msg=self._formatter.format(step='Reasons input box does not exist'))
            self.operatevm_page.txt_reasons.set(self._reason)

            self.assertTrue(self.operatevm_page.btn_next.exists(),
                            msg=self._formatter.format(step='Next button does not exist'))
            self.operatevm_page.btn_next.click()
            self.operatevm_page.wait_for_loading_complete(3)

            self.assertTrue(self.operatevm_page.btn_submit.exists(),
                            msg=self._formatter.format(step='Submit button does not exist'))
            self.operatevm_page.btn_submit.click()
            self.operatevm_page.wait_for_loading_complete(2)

            self.assertTrue(self.operatevm_page.btn_ok.exists(),
                            msg=self._formatter.format(step='OK button does not exist'))
            self.operatevm_page.btn_ok.click()

        except AssertionError:
            BasePage().save_request()
            raise
        except:
            ex = sys.exc_info()[:2]
            BasePage().save_request()
            logger.error('{0} encounters error: {1}'.format(self.test_on_demand_backup.__name__, ex))
            raise

    def navigate_to_items_page(self, current_browser):
        _browser = current_browser.instance._browser.current
        _browser.switch_to.frame(None)

        if MainPage().btn_items.exists():
            MainPage().btn_items.click()
            self.operatevm_page.wait_for_loading_complete(3)
            return True
        else:
            return False

    def _switch_to_target_item_frame(self):
        _basepage = BasePage()
        _browser = self.current_browser.instance._browser.current
        _browser.switch_to.default_content()
        target_frame_id = _basepage.get_accurate_frameid(
            self.current_browser,
            self.operatevm_page.gadget_url_str)

        if target_frame_id:
            _browser.switch_to.frame(target_frame_id)
            logger.info(
                'Switch to frame {}'.format(target_frame_id),
                False, True)
        else:
            logger.error('Looking for target iframe failed.')
        self.operatevm_page.wait_for_loading_complete(5)

    def runTest(self):
        self.test_on_demand_backup()

    def _validate_input_args(self, current_browser=None, is_login=False, description=None, vm_name=None):
        assert current_browser is not None, 'current_browser is None, may be there is no active browser.'
        assert is_login is True, "Can't do anything if you didn't login."
        assert vm_name is not None, 'Name of VM should not be None.'

        self.current_browser = current_browser
        self._description = description
        self._deployed_vm = vm_name
        self._reason = description

    def _finalize_context(self):
        pass
