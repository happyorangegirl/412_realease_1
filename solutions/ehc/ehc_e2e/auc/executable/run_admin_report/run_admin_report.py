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
from ehc_e2e.auc.uimap.specific import RunAdminReportPage
from ehc_e2e.auc.uimap.shared import CatalogPage, RequestsPage
from ehc_e2e.auc.uimap.shared import LoadingWindow
from robot.api import logger


class RunAdminReport(BaseUseCase):
    """
    Run Admin Report
    """
    step_failed_msg = 'Running on step: "Run Admin Report"-FAILED'

    def test_run_admin_report(self):
        self.catalog_page = CatalogPage()
        self.assertTrue(self.catalog_page.navigate_to_catalog(self.current_browser),
                        msg='Running on step:"Run Admin Report"-FAILED, '
                            'switch to catalog frame failed.')
        self.run_admin_report_page = RunAdminReportPage()
        self.loading_window = LoadingWindow()
        self.run_admin_report_page.data_protection_services.click()
        self.catalog_page.btn_run_admin_report_request.click()

        _formatter = 'Running on step: "{step}" - FAILED'
        try:
            self.assertTrue(
                self.run_admin_report_page.txt_description.exists(),
                msg=_formatter.format(step='Navigate to Request Information page')
            )
            self.run_admin_report_page.txt_description.set(self.ctx_in.run_admin_report.description)
            self.run_admin_report_page.txt_reasons.set(self.ctx_in.run_admin_report.reasons)
            self.loading_window.wait_loading(self.current_browser, 30)
            self.run_admin_report_page.btn_next.click()

            self.assertTrue(
                self.run_admin_report_page.lab_select_backup_level_name.exists(),
                msg=_formatter.format(step='Navigate to Run reports fro a Backup Service Level page')
            )

            self.run_admin_report_page.btn_set_backup_service_name.click()
            if self.run_admin_report_page.click_drop_down_list(
                    self.run_admin_report_page.parent_element, 'div',
                    self.select_a_backup_service_level_name) is False:
                logger.error('{},does not exist'.format(self.select_a_backup_service_level_name))
                self.fail('{},does not exist'.format(self.select_a_backup_service_level_name))
            else:
                self.run_admin_report_page.wait_for_loading_complete(3)
                if self.ctx_in.run_admin_report.select_pdf_page_orientation is not None:
                    self.run_admin_report_page.btn_select_pdf_page_orientation.click()
                    if self.run_admin_report_page.click_drop_down_list(
                            self.run_admin_report_page.parent_element, 'div',
                            self.ctx_in.run_admin_report.select_pdf_page_orientation) is False:
                        logger.error('{},does not exist'.format(
                            self.ctx_in.run_admin_report.select_pdf_page_orientation))
                        self.fail('{},does not exist'.format(
                            self.ctx_in.run_admin_report.select_pdf_page_orientation))
                self.run_admin_report_page.wait_for_loading_complete(3)
                self.run_admin_report_page.select_listbox(
                    self.run_admin_report_page.select_one_or_more_reports_to_run, 'input')
                self.run_admin_report_page.wait_for_loading_complete(3)
                if self.ctx_in.run_admin_report.select_a_time_frame is not None:
                    self.run_admin_report_page.btn_select_a_time_frame.current.location_once_scrolled_into_view
                    self.run_admin_report_page.btn_select_a_time_frame.click()
                    if self.run_admin_report_page.click_drop_down_list(
                            self.run_admin_report_page.parent_element, 'div',
                            self.ctx_in.run_admin_report.select_a_time_frame) is False:
                        self.run_admin_report_page.btn_select_a_time_frame.click()
                        logger.error('{},does not exist'.format(self.ctx_in.run_admin_report.select_a_time_frame))
                        self.fail('{},does not exist'.format(
                            self.ctx_in.run_admin_report.select_a_time_frame))
                    self.loading_window.wait_loading(self.current_browser, 30)
                if self.ctx_in.run_admin_report.email_results is not None \
                        and self.ctx_in.run_admin_report.email_results:
                    self.run_admin_report_page.btn_email_results.current.location_once_scrolled_into_view
                    self.run_admin_report_page.btn_email_results.click()
                    if self.run_admin_report_page.click_drop_down_list(
                            self.run_admin_report_page.parent_element, 'div',
                            'Yes') is False:
                        logger.error('{},does not exist'.format(self.ctx_in.run_admin_report.email_results))
                        self.fail('{},does not exist'.format(self.ctx_in.run_admin_report.email_results))
                    self.loading_window.wait_loading(self.current_browser, 30)
                    if self.ctx_in.run_admin_report.email_address is not None:
                        self.run_admin_report_page.txt_email_address.current.location_once_scrolled_into_view
                        self.run_admin_report_page.txt_email_address.set(self.ctx_in.run_admin_report.email_address)

                self.assertTrue(self.run_admin_report_page.btn_submit.exists(),
                                msg=_formatter.format(step='Navigate to Review and Submit page'))
                self.run_admin_report_page.btn_submit.click()

        except AssertionError:
            self.run_admin_report_page.save_request()
            raise
        except:
            self.run_admin_report_page.save_request()
            self.fail(self.step_failed_msg + ', more error info: {}'.format(sys.exc_info()[:2]))

        self.assertTrue(self.run_admin_report_page.lab_confirmation_success.exists(),
                        msg='Running on step:"Run Admin Report"-FAILED,'
                            'after clicking submit button, cannot find the label: '
                            'The request has been submitted successfully.')
        self.run_admin_report_page.btn_ok.click()
        # switch to request
        self.assertTrue(RequestsPage().navigate_to_request(self.current_browser),
                        msg='Running on step:"Run Admin Report"-FAILED, '
                            'switch to request frame failed.')

        # check the request
        self.request_result = RequestsPage().get_request_result(self.ctx_in.run_admin_report.description)
        self.assertIsNotNone(self.request_result,
                             msg='Running on step:"Run Admin Report"-FAILED, ''failed to get the request result.')

    def runTest(self):
        self.test_run_admin_report()

    def _validate_context(self):
        if self.ctx_in:
            self.request_result = None
            self.current_browser = self.ctx_in.shared.current_browser
            assert self.current_browser is not None, 'current_browser in yaml is None, ' \
                                                     'may be there is no active browser'
            self.assertTrue(self.current_browser.is_login,
                            msg='Your are log out now, please login to vRA.')

            assert self.ctx_in.run_admin_report.description is not None, "yaml data of description value is None"
            if self.ctx_in.added_backup_service_level is not None and \
                    self.ctx_in.added_backup_service_level.backup_to_operate_vm != '':
                self.select_a_backup_service_level_name =\
                    self.ctx_in.added_backup_service_level.backup_to_operate_vm
            else:
                self.select_a_backup_service_level_name = \
                    self.ctx_in.run_admin_report.select_a_backup_service_level_name

    def _finalize_context(self):
        if self.request_result is not None:
            if self.request_result.status == 'Failed':
                msg = 'the request status of run admin report:{name} is:' \
                      ' {status}, the status detaial is: {status_detail}'\
                        .format(name=self.request_result.description,
                                status=self.request_result.status,
                                status_detail=self.request_result.status_details)
                logger.error(msg)
                raise AssertionError(msg)
            else:
                logger.info(
                    'the request status of run admin report:{name} request result is successful'.format(
                        name=self.request_result.description))
