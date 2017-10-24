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
from ehc_e2e.auc.uimap.shared import RequestsPage, LoadingWindow, CatalogPage
from ehc_e2e.auc.uimap.specific import EditAvamarGridPage


class EditAvamarGrid(BaseUseCase):
    """
    Edit a AvamarGrid
    """
    REQUEST_SUCCESSFUL = 'Successful'
    _formatter = 'Running on step: "Edit Avamar Grid"-FAILED, {}'

    def test_edit_avamar_grid(self):
        loading_window = LoadingWindow()
        for counter, item in enumerate(self.edit_avamar_grid_list):
            try:
                self.edit_avamar_grid_list[counter].request = None
                catalog_page = CatalogPage()
                edit_avamar_grid_page = EditAvamarGridPage()
                self.assertTrue(catalog_page.navigate_to_catalog(self.current_browser),
                                self._formatter.format('failed to navigate to catalog page.'))
                self.assertTrue(edit_avamar_grid_page.btn_data_protection_services.exists(),
                                self._formatter.format('data protection button does not exist.'))
                edit_avamar_grid_page.btn_data_protection_services.click()
                self.assertTrue(catalog_page.btn_avamar_grid_maintenance_request.exists(),
                                self._formatter.format('avamar grid maintenance button does not exist.'))
                catalog_page.btn_avamar_grid_maintenance_request.click()
                loading_window.wait_loading(self.current_browser, 30)

                # input description.
                logger.info(msg='Start to fill items in the Request information tab')
                self.assertTrue(edit_avamar_grid_page.txt_description.exists(),
                                self._formatter.format('description textbox does not exist.'))
                logger.info(msg='Filling items in the Choose Option tab')
                edit_avamar_grid_page.txt_description.set(item.description)
                loading_window.wait_loading(self.current_browser, 30)
                self.assertTrue(edit_avamar_grid_page.btn_next.exists(),
                                self._formatter.format('Next button does not exist.'))
                edit_avamar_grid_page.btn_next.click()
                loading_window.wait_loading(self.current_browser, 30)

                # providing operation type
                logger.info(msg='Start to fill items in the Action Choice tab')
                self.assertTrue(edit_avamar_grid_page.btn_operation_type.exists(),
                                self._formatter.format('Action DropDownList open button does not exist.'))
                edit_avamar_grid_page.btn_operation_type.click()
                self.assertTrue(edit_avamar_grid_page.click_drop_down_list(
                    edit_avamar_grid_page.lbl_active_value, 'div', item.select_operation_type),
                                self._formatter.format('Select Action {} does not exist.'
                                                       .format(item.select_operation_type)))
                logger.info(msg='Selected Action {} '.format(item.select_operation_type))
                loading_window.wait_loading(self.current_browser, 30)
                self.assertTrue(edit_avamar_grid_page.btn_next.exists(),
                                self._formatter.format('Next button does not exist.'))
                edit_avamar_grid_page.btn_next.click()
                loading_window.wait_loading(self.current_browser, 30)

                # Providing the Input values
                logger.info(msg='Start to fill items in the Edit Avamar Grid Details tab')
                self.assertTrue(edit_avamar_grid_page.edit_avamar_grid_detail_for_onboard_ca_cluster(
                    self.current_browser, item), self._formatter.format('failed to edit Avamar Grid Details.'))
                self.edit_avamar_grid_name_list.append(item.new_avamar_grid_name)

                # Submit request.
                logger.info(msg='Start to fill items in the Review and Submit tab')
                self.assertTrue(edit_avamar_grid_page.btn_submit.exists(),
                                self._formatter.format('submit button does not exist.'))
                edit_avamar_grid_page.btn_submit.click()
                logger.info('Clicked submit button.', False, True)
                loading_window.wait_loading(self.current_browser, 30)
                self.assertTrue(edit_avamar_grid_page.lbl_confirmation_success.exists(),
                                self._formatter.format('label: "confirm information in Review and Submit, '
                                                       'click submit button" does not exist.'))
                self.assertTrue(edit_avamar_grid_page.btn_ok.exists(),
                                self._formatter.format('OK button in confirm success page does not exist.'))
                edit_avamar_grid_page.btn_ok.click()
                logger.info('Clicked ok button in confirm success page.', False, True)
                loading_window.wait_loading(self.current_browser, 30)

                # switch to request
                requests_page = RequestsPage()
                self.assertTrue(requests_page.navigate_to_request(self.current_browser),
                                self._formatter.format('switch to request frame failed.'))

                # check the request
                request_result = requests_page.get_request_result(item.description)
                self.assertIsNotNone(request_result, self._formatter.format(
                    'getting request failed for NO.{} avamar grid'.format(counter)))
                self.edit_avamar_grid_list[counter].request = request_result

                # check request result after each request completes.
                if request_result.status == self.REQUEST_SUCCESSFUL:
                    if item.new_avamar_grid_name in self.edit_avamar_grid_name_list:
                        self.added_avamar_grid = [c.replace(item.avamar_grid_name,
                                                            item.new_avamar_grid_name) for c in
                                                  self.added_avamar_grid]

                else:
                    raise AssertionError(self._formatter.format(
                        'No.{} edit avamar grid request failed, request status detail: {}.'.format(
                            counter, request_result.status_details)))
            except:

                raise


    def runTest(self):
        self.test_edit_avamar_grid()

    def _validate_context(self):
        self.edit_avamar_grid_name_list = []
        if self.ctx_in:
            assert self.ctx_in.shared.current_browser.is_login is True, \
                self._formatter.format("can't do anything if you are not logged in")
            self.current_browser = self.ctx_in.shared.current_browser
            assert self.ctx_in.edit_avamar_grid is not None, \
                self._formatter.format("the edit_avamar_grid in yaml file is None.")
            self.onboard_cluster_type = self.ctx_in.onboard_cluster_type
            assert self.onboard_cluster_type is not None, \
                self._formatter.format('please provide onboard cluster type.')
            self.edit_avamar_grid_list = self.ctx_in.edit_avamar_grid

            self.added_avamar_grid = getattr(self.ctx_in, "added_avamar_grid", [])
            # comments assert len of added_avamar_grid, because just edit avamar provided in yaml item: edit_avamar_grid
            # assert len(self.added_avamar_grid) > 0, "the added_avamar_grid in yaml file is None"
            for grid in self.edit_avamar_grid_list:
                for key, value in grid.__dict__.iteritems():
                    assert value is not None, \
                        self._formatter.format(
                            'the {key} attribute of edit_avamar_grid in yaml file is None'.format(key=key))

            _cluster_types = ('LC1S', 'DR2S', 'CA1S', 'CA2S', 'MP2S', 'MP3S', 'LC2S', 'VS1S', 'VS2S')
            _cluster_type = str(self.onboard_cluster_type).upper()
            self.assertIn(_cluster_type, _cluster_types,
                          msg=self._formatter.format('the "onboard cluster type" is unspecified.'))

            # _required_sites, _required_vcenters, _required_hwis = (0, 0, 0)
            # if _cluster_type in ('LC1S', 'CA1S', 'VS1S'):
            #     _required_sites, _required_vcenters, _required_hwis = (1, 1, 1)
            #
            # if _cluster_type in ('DR2S', 'CA2S', 'MP2S', 'MP3S', 'LC2S', 'VS2S'):
            #     _required_sites, _required_vcenters, _required_hwis = (2, 2, 2)
            #
            # if _cluster_type == 'CA1S':
            #     _required_hwis = 2
            # elif _cluster_type == 'CA2S':
            #     _required_vcenters = 1
            # elif _cluster_type == 'MP2S':
            #     _required_hwis = 3
            # elif _cluster_type == 'MP3S':
            #     _required_sites, _required_hwis = (3, 3)
            # else:
            #     pass
            #
            # self.assertGreaterEqual(
            #     len(self.ctx_in.added_sites), _required_sites,
            #     msg='At least {} site(s) are required'.format(_required_sites))
            # self.assertGreaterEqual(
            #     len(self.ctx_in.added_vcenter), _required_vcenters,
            #     msg='At least {} vCenter(s) are required'.format(_required_vcenters))
            # self.assertGreaterEqual(
            #     len(self.ctx_in.added_hwi), _required_hwis,
            #     msg='At least {} hardware island(s) are required'.format(_required_hwis))

    def _finalize_context(self):
        setattr(self.ctx_out, 'added_avamar_grid', self.added_avamar_grid)
