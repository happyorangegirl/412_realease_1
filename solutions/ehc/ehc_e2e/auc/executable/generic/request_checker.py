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
from robot.api import logger
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.reusable import PageNavigator, LoadingPopupWaiter
from ehc_e2e.auc.reusable.browser_relauncher import close_relaunch_browser_operation
from ehc_e2e.auc.uimap.shared import RequestsPage
from ehc_e2e.auc.uimap.specific import DeployVmRequestPage


class RequestChecker(BaseUseCase):
    CLOSE_RELAUNCH_COUNT = 0

    class Func(object):
        CATALOG_REQUEST, BLUEPRINT_REQUEST, GET_LATEST_REQUEST_ID, GET_REQUEST_RESULT_BY_REST = (
            'test_latest_catalog_request', 'test_latest_blueprint_request', 'test_get_latest_request_id',
            'test_get_request_result_by_rest')

    def __init__(self, name=None, method_name=Func.CATALOG_REQUEST, **kwargs):
        super(RequestChecker, self).__init__(name + '_request_checking', method_name, **kwargs)

        self.navigator = PageNavigator(self)
        self.request_page = RequestsPage()
        self.loading_waiter = LoadingPopupWaiter(self)
        self.request_result = None
        self.deployed_vms = []
        self.slp = 10
        self.request_id = kwargs.get('request_id', None)

    def _re_init_navigate_and_go_to_request_page(self):
        # we need to re-instatiate the instance, this forced original references to Browser
        # update to new Browser instance.
        self.navigator = PageNavigator(self)
        self.request_page = RequestsPage()
        self.loading_waiter = LoadingPopupWaiter(self)
        self.request_result = None
        self.navigator.go_to_requests_page()

    def _get_request_result(self):
        try:
            try:
                self.navigator.go_to_requests_page()
                with self.request_page.frm_requests:
                    self.request_result = self.request_page.get_request_result(self.description, slp=self.slp)
            except:
                logger.warn('RequestChecker get request encounters error:{}\n trying to close and'
                            ' relaunch browser.'.format(sys.exc_info()))
                close_relaunch_browser_operation()
                RequestChecker.CLOSE_RELAUNCH_COUNT += 1
                self._re_init_navigate_and_go_to_request_page()
                with self.request_page.frm_requests:
                    self.request_result = self.request_page.get_request_result(self.description, slp=self.slp)

            if not self.request_result:
                if RequestChecker.CLOSE_RELAUNCH_COUNT == 0:
                    logger.warn(
                        'RequestChecker get request result returns None, trying to close and '
                        'relaunch browser.')
                    close_relaunch_browser_operation()
                    self._re_init_navigate_and_go_to_request_page()
                    with self.request_page.frm_requests:
                        self.request_result = self.request_page.get_request_result(self.description, slp=self.slp)
                else:
                    logger.warn('We have had one time attempt for close and relaunch to get request result but still '
                                'failed, no further attempt.')
        except:
            raise

        finally:
            RequestChecker.CLOSE_RELAUNCH_COUNT = 0

    def test_latest_catalog_request(self):
        self._get_request_result()
        self._check_latest_catalog_request()

    def test_latest_blueprint_request(self):
        self._get_request_result()
        self._check_latest_blueprint_request()

    def test_get_latest_request_id(self):
        self.assertIsNotNone(self.description, 'Description is not provided when initializing RequestChecker.')
        request_id = None
        try:
            self.navigator.go_to_requests_page()
            with self.request_page.frm_requests:
                request_id = self.request_page.get_current_request_item_id(self.description)
                if not request_id:
                    logger.warn('RequestChecker get latest request id failed, close and '
                                'relaunch browser to try again, exception details:{}'.format(sys.exc_info()))
                    close_relaunch_browser_operation()
                    self._re_init_navigate_and_go_to_request_page()
                    with self.request_page.frm_requests:
                        request_id = self.request_page.get_current_request_item_id(self.description)
        except:
            logger.warn('RequestChecker get latest request id encounters exception, close and '
                        'relaunch browser to try again, exception details:{}'.format(sys.exc_info()))
            close_relaunch_browser_operation()
            self._re_init_navigate_and_go_to_request_page()
            with self.request_page.frm_requests:
                request_id = self.request_page.get_current_request_item_id(self.description)

        self.request_id = request_id

    def test_get_request_result_by_rest(self):
        self.assertIsNotNone(self.request_id, 'Request id is not provided when initializing RequestChecker.')
        self.request_result = self.request_page.get_request_result_in_rest(
            key='requestNumber', value=self.request_id, timeout=3600, slp=180)

    def _check_latest_catalog_request(self):
        _formatter = 'Running on step: "{step}", status_details: "{status_details}" - FAILED'.format

        self.assertIsNotNone(self.request_result, msg='Can not get the request result')
        logger.info("Request id: {}, status: {}, \n status details: {}".format(
            self.request_result.request, self.request_result.status, self.request_result.status_details))

        self.assertIsNotNone(self.request_result.status, msg='Request status can not be captured')
        self.assertTrue(self.request_result.status != 'Unsubmitted',
                        msg='Request status should not be "Unsubmitted"')
        self.assertIsNotNone(self.request_result.status_details,
                             msg='Request status details can not be captured')
        if self.ignore_failure and (self.request_result.status == 'Failed') \
                and (self.request_result.status_details.find('already exists') > -1):
            self.request_result.status = 'Successful'
        elif not self.not_fail_on_request_failed:
            self.assertTrue(self.request_result.status == 'Successful',
                            msg=_formatter(step=self.description, status_details=self.request_result.status_details))
        else:
            if self.request_result.status != 'Successful':
                logger.error('Request status: {}, status detail: {}.'.format(self.request_result.status,
                                                                             self.request_result.status_details))
    def _check_latest_blueprint_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.assertIsNotNone(self.request_result, msg=_formatter(step='Validate blueprint request'))

        self.assertTrue(self.request_result.status.lower() == 'successful',
            msg=_formatter(step='Validate blueprint request status'))

        with self.request_page.frm_requests:
            self.request_page.get_request_link_by_id(self.request_result.request).click()

        self.loading_waiter.wait_for_popup_loading_finish()

        self.blueprint_request_page = DeployVmRequestPage()
        with self.blueprint_request_page.frm_request_details:
            with self.blueprint_request_page.frm_blueprint_request:
                self.blueprint_request_page.lnk_execution_info.click()
                self.loading_waiter.wait_for_popup_loading_finish()

                cells = self.blueprint_request_page.__class__.get_provision_details_cells()
                self.deployed_vms.extend(
                    [cell.value.split()[-1].strip('.') for cell in cells if 'Request succeeded.' in cell.value])

        with self.blueprint_request_page.frm_request_details:
            self.blueprint_request_page.btn_ok.click()

    def _validate_input_args(self, **kwargs):
        if self._testMethodName == self.Func.CATALOG_REQUEST:
            self.__validate_args_of_catalog_request(**kwargs)
        elif self._testMethodName in (self.Func.BLUEPRINT_REQUEST, self.Func.GET_LATEST_REQUEST_ID):
            self.__validate_args_of_blueprint_request(**kwargs)
        else:
            pass

    def _finalize_output_params(self):
        if self.request_result:
            if self.deployed_vms and (self._testMethodName == self.Func.BLUEPRINT_REQUEST):
                setattr(self.request_result, 'deployed_vms', self.deployed_vms)
            if self._testMethodName == self.Func.GET_REQUEST_RESULT_BY_REST:
                self._output.append(self.request_result)

            self._output.append(self.request_result)
        if getattr(self, 'request_id') and self._testMethodName == RequestChecker.Func.GET_LATEST_REQUEST_ID \
                and isinstance(self._output, list):
            # Since _output in baseusecase only supports mutable type like list, set, we here expect it as list.
            self._output.append((self.request_id, self.description))

    def __validate_args_of_catalog_request(self, **kwargs):
        self.description = kwargs.get('description')
        self.ignore_failure = kwargs.get('ignore_failure')
        self.not_fail_on_request_failed = kwargs.get('not_fail_on_request_failed')
        self.slp = int(kwargs.get('sleep')) if kwargs.get('sleep') else 10
        self.requestcheckingtimeout = \
            int(kwargs.get('requestcheckingtimeout')) if kwargs.get('requestcheckingtimeout') else 2500
        self.requestcheckingfirstwaitduration = \
            int(kwargs.get('requestcheckingfirstwaitduration')) if kwargs.get('requestcheckingfirstwaitduration') else 0

    def __validate_args_of_blueprint_request(self, description, **kwargs):
        self.description = description
        if 'sleep' in kwargs:
            self.slp = int(kwargs['sleep'])
        else:
            self.slp = 60
