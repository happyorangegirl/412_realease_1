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

from robot.api import logger

from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared import LoadingWindow
from ehc_e2e.auc.uimap.shared import RequestsPage
from ehc_e2e.auc.uimap.specific import DestroyVMsPage


class DestroyVMs(BaseUseCase):
    """
    Destory VMs
    """
    _formatter = 'Running on step: "Destroy VMs" - FAILED, {step}'

    def test_destroy_vms(self):
        for destroy_item in self.deployd_vms:
            logger.info('Start to destroy vm: {}'.format(destroy_item), False, True)
            self.loading_window = LoadingWindow()
            self.destroy_vms_page = DestroyVMsPage(destroy_item)
            self.assertTrue(self.destroy_vms_page.navigate_to_items_page(self.current_browser),
                            msg=self._formatter.format(step='failed to switch to items page'))
            self.loading_window.wait_loading(self.current_browser, 30)
            target_frame_id_item = self.destroy_vms_page.get_accurate_frameid(
                self.current_browser,
                self.destroy_vms_page.item_page_iframe_url)
            ## switch iframe
            browser = self.current_browser.instance._browser.current
            if target_frame_id_item:
                browser.switch_to.frame(target_frame_id_item)
            self.loading_window.wait_loading(self.current_browser, 30)
            iframe_flag = False
            if not self.destroy_vms_page.btn_machines.exists():
                iframes = browser.find_elements_by_tag_name('iframe')
                iframes_list = []
                import re
                for iframe in iframes:
                    iframe_id = iframe.get_attribute('id')
                    if re.match('__gadget_', iframe_id) and iframe_id != 'target_frame_id_item':
                        iframes_list.append(iframe_id)
                        self.current_browser.instance._browser.current.switch_to.frame(iframe_id)
                        if self.destroy_vms_page.element_exists(
                                self.destroy_vms_page.btn_machines.machines_xpath, browser, timeout=3):
                            iframe_flag = True
                            break
            else:
                iframe_flag = True
            if not iframe_flag:
                self.fail(msg=self._formatter.format(step='failed to switch to Items frame.'))
            else:
                self.destroy_vms_page.btn_machines.click()
                if self.destroy_vms_page.destroy_vm_item.exists(2):
                    self.destroy_vms_page.destroy_vm_item.click()

                self.loading_window.wait_loading(self.current_browser, 30)
                self.assertTrue(
                    self.destroy_vms_page.btn_destroy.exists(),
                    msg=self._formatter.format(step='failed to navigate to Item Details page.')
                )
                self.destroy_vms_page.btn_destroy.click()
                self.assertTrue(
                    self.destroy_vms_page.service_destroy_lab.exists(),
                    msg=self._formatter.format(step='failed to navigate to Destroy a virtual machine page')
                )
                self.destroy_vms_page.btn_submit.click()
                self.assertTrue(self.destroy_vms_page.lab_confirmation_success.exists(),
                                msg=self._formatter.format(
                                    step='after clicking submit button, cannot find the label: '
                                         'The request has been submitted successfully.'))
                self.destroy_vms_page.btn_ok.click()
                self.destroy_vms_page.btn_close.click()
                # switch to request
                self.assertTrue(RequestsPage().navigate_to_request(self.current_browser),
                                msg=self._formatter.format(step='after clicking Close button, '
                                                                'failed to switch to request frame.'))

                # check the request

                deploy_item = "Destroy - {0}".format(destroy_item)
                # set the refresh interval to 1 minute
                request_result = RequestsPage().get_request_result(item=deploy_item, slp=60)
                self.assertIsNotNone(request_result,
                                     msg=self._formatter.format(step='failed to get the request result.'))

                if request_result.status == 'Successful':
                    logger.info(
                        'the request status of destroy_vms:{name} is: {status}, '
                        'the status detail is: {status_detail}'.format(
                            name=request_result.item, status=request_result.status,
                            status_detail=request_result.status_details))
                    self.destroy_vms.append(self.destroy_vms_page.destroy_vm_item)

                else:
                    logger.error(
                        'the request status of destroy_vms:{name} is: {status}, '
                        'the status detail is: {status_detail}'.format(
                            name=request_result.item, status=request_result.status,
                            status_detail=request_result.status_details))
                    self.destroy_failed_vms.append(destroy_item)

    def runTest(self):
        if self.deployd_vms:
            self.test_destroy_vms()
        else:
            logger.warn('There is no VM items to destroy in context deployed_vms object')

    def _validate_context(self):
        if self.ctx_in:
            self.current_browser = self.ctx_in.shared.current_browser
            assert self.current_browser is not None, \
                self._formatter.format(step='current_browser in yaml is None, may be there is no active browser')
            self.assertTrue(self.current_browser.is_login,
                            msg=self._formatter.format(step='please login to vRA, The flag value is_login is: False.'))
            self.deployd_vms = getattr(self.ctx_in, 'deployed_vms')

        self.destroy_failed_vms = []
        self.destroy_vms = []

    def _finalize_context(self):
        self.assertTrue(len(self.destroy_failed_vms) == 0,
                        msg='VMs destroy failed: {}.'.format(self.destroy_failed_vms))
        if self.destroy_vms:
            self.assertTrue(self.destroy_vms_page.navigate_to_items_page(self.current_browser),
                            msg=self._formatter.format(step='failed to switch to items page.'))

            self.loading_window.wait_loading(self.current_browser, 30)
            target_frame_id_item = self.destroy_vms_page.get_accurate_frameid(
                self.current_browser,
                self.destroy_vms_page.item_page_iframe_url)
            ## switch iframe
            self.current_browser.instance._browser.current.switch_to.frame(target_frame_id_item)
            for destroy_item in self.destroy_vms:
                if self.destroy_vms_page.btn_machines.exists():
                    timeout = 5 * 60
                    while timeout > 0:
                        if destroy_item.exists(5):
                            self.destroy_vms_page.btn_item_page_table_refresh.click()
                            self.destroy_vms_page.wait_for_loading_complete(10)
                            timeout -= 10
                        else:
                            break
