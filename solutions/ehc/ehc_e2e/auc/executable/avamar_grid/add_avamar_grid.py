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
import ehc_e2e.constants.vro_vra_constants as vro_constants
from ehc_e2e.auc.uimap.shared import CatalogPage
from ehc_e2e.auc.uimap.shared import LoadingWindow
from ehc_e2e.auc.uimap.shared import RequestsPage
from ehc_e2e.utils.service import VroItems
from ehc_e2e.auc.uimap.specific import AddAvamarGridPage


class AddAvamarGrid(BaseUseCase):
    def __init__(self, name=None, method_name='runTest',
                 ctx_in=None, ctx_out=None, unselect_proxy=False, **kwargs):
        super(AddAvamarGrid, self).__init__(name, method_name, ctx_in, ctx_out, **kwargs)
        self.unselect_proxy = unselect_proxy

    """
    add a AvamarGrid
    """
    REQUEST_SUCCESSFUL = 'Successful'
    _formatter = 'Running on step: "Add Avamar Grid"-FAILED, {}'

    def test_add_avamar_grid(self):
        loading_window = LoadingWindow()
        (vro_response_dict, vro_rest_base) = VroItems(
            self.ctx_in).get_all_items_from_vro(vro_constants.AVAMARGRID_API)
        for counter, item in enumerate(self.add_avamar_grid_list):
            avamar_grid_existed = self._avamar_grid_exist(item,
                                                          vro_response_dict,
                                                          vro_rest_base)
            if not avamar_grid_existed['name'] and \
                    not avamar_grid_existed['fqdn']:
                # self.add_avamar_grid_list[counter].request = None
                catalog_page = CatalogPage()
                add_avamar_grid_page = AddAvamarGridPage()
                self.assertTrue(catalog_page.navigate_to_catalog(self.current_browser),
                                self._formatter.format('failed to navigate to catalog page.'))
                self.assertTrue(add_avamar_grid_page.btn_data_protection_services.exists(),
                                self._formatter.format('data protection button does not exist.'))
                add_avamar_grid_page.btn_data_protection_services.click()
                self.assertTrue(catalog_page.btn_avamar_grid_maintenance_request.exists(),
                                self._formatter.format('avamar grid maintenance button does not exist.'))
                catalog_page.btn_avamar_grid_maintenance_request.click()
                loading_window.wait_loading(self.current_browser, 30)

                # input description.
                logger.info(msg='Start to fill items in the Request information tab')
                self.assertTrue(add_avamar_grid_page.txt_description.exists(),
                                self._formatter.format('description textbox does not exist.'))
                logger.info('Filling description textbox', True, False)
                add_avamar_grid_page.txt_description.set(item.description)
                logger.info('Filled description textbox', True, False)
                self.assertTrue(add_avamar_grid_page.btn_next.exists(),
                                self._formatter.format('Next button does not exist.'))
                add_avamar_grid_page.btn_next.click()
                loading_window.wait_loading(self.current_browser, 30)

                # providing operation type
                logger.info(msg='Start to fill items in the Action Choose tab')
                self.assertTrue(add_avamar_grid_page.btn_operation_type.exists(),
                                self._formatter.format('Action DropDownList open button does not exists'))
                add_avamar_grid_page.btn_operation_type.click()
                self.assertTrue(add_avamar_grid_page.click_drop_down_list(
                    add_avamar_grid_page.lbl_active_value, 'div', item.select_operation_type),
                    self._formatter.format('Select Action {} does not exist'
                                           .format(item.select_operation_type)))
                logger.info(msg='Selected Action {} '.format(item.select_operation_type))
                loading_window.wait_loading(self.current_browser, 30)
                self.assertTrue(add_avamar_grid_page.btn_next.exists(),
                                self._formatter.format('Next button does not exist.'))
                add_avamar_grid_page.btn_next.click()
                # Adding try except to take the snapshot of page if any error occurs
                try:
                    logger.info(msg='Start to fill items in the Add Avamar')
                    self.assertTrue(
                        add_avamar_grid_page.add_avamar_grid_for_onboard_dr_cluster(self.current_browser, item, self.unselect_proxy),
                        self._formatter.format(
                            'Add Avamar Grid {} Filling values page.'.format(item.avamar_grid_name)))

                    loading_window.wait_loading(self.current_browser, 30)
                    self.assertTrue(add_avamar_grid_page.btn_next.exists(),
                                    self._formatter.format('Next button does not exist.'))
                    add_avamar_grid_page.btn_next.click()
                    loading_window.wait_loading(self.current_browser, 30)
                    logger.info(msg='Start to go into the Review and submit tab.')
                    # Submit request.
                    self.assertTrue(add_avamar_grid_page.btn_submit.exists(),
                                    self._formatter.format('submit button does not exist'))
                    add_avamar_grid_page.btn_submit.click()
                    logger.info('Clicked submit button.', False, True)
                    loading_window.wait_loading(self.current_browser, 30)
                    self.assertTrue(add_avamar_grid_page.lbl_confirmation_success.exists(),
                                    self._formatter.format('label: "confirm information in Review and Submit, '
                                                           'click submit button" does not exist'))
                    self.assertTrue(add_avamar_grid_page.btn_ok.exists(),
                                    self._formatter.format('OK button in confirm submit success page does not exist'))
                    add_avamar_grid_page.btn_ok.click()
                    loading_window.wait_loading(self.current_browser, 30)
                    logger.info('Clicked ok button in confirm success page.', False, True)
                except:
                    import sys
                    logger.error('Encounters exception, exception details: {}'.format(sys.exc_info()))
                    raise

                # switch to request
                requests_page = RequestsPage()
                self.assertTrue(requests_page.navigate_to_request(self.current_browser),
                                self._formatter.format('switch to request frame failed.'))

                # check the request
                request_result = requests_page.get_request_result(item.description)
                self.assertIsNotNone(request_result, self._formatter.format(
                    'getting request failed for NO.{} avamar grid'.format(counter)))
                item.request = request_result

                # check request result after each request completes.
                if request_result.status == self.REQUEST_SUCCESSFUL:
                    self.added_avamar_grid.append(item.avamar_grid_name)
                else:
                    self.added_failed_avamargrids.append(item.avamar_grid_name)
                    raise AssertionError(self._formatter.format(
                        'Add avamar grid {} request failed, request status detail: {}'
                            .format(item.avamar_grid_name, request_result.status_details)))
            elif avamar_grid_existed['name'] and not avamar_grid_existed['fqdn']:
                raise AssertionError(self._formatter.format('Avamar grid with same name {0} but different fqdn already exit'.format(item.avamar_grid_name)))
            elif not avamar_grid_existed['name'] and avamar_grid_existed['fqdn']:
                raise AssertionError(self._formatter.format('Avamar grid with same fqdn {0} but different name already exit'.format(item.avamar_grid_fqdn_name)))
            elif avamar_grid_existed['name'] and avamar_grid_existed['fqdn']:
                self.added_avamar_grid.append(item.avamar_grid_name)
                logger.info("avamar grid: {0} with FQDN: {1} does not need to add again, it already exists. "
                            "Put it in added_avamar_grid directly.".format(
                    item.avamar_grid_name, item.avamar_grid_fqdn_name))


    def runTest(self):
        self.test_add_avamar_grid()

    def _validate_context(self):
        self.added_avamar_grid = []
        self.added_failed_avamargrids = []
        if self.ctx_in:
            assert self.ctx_in.shared.current_browser.is_login is True, \
                self._formatter.format("can't do anything if you are not logged in")
            self.current_browser = self.ctx_in.shared.current_browser
            assert self.ctx_in.add_avamar_grid is not None, \
                self._formatter.format("the add_avamar_grid in yaml file is None")
            self.onboard_cluster_type = self.ctx_in.onboard_cluster_type
            assert self.onboard_cluster_type is not None, self._formatter.format('please provide onboard cluster type.')
            self.add_avamar_grid_list = self.ctx_in.add_avamar_grid

            for grid in self.add_avamar_grid_list:
                for key, value in grid.__dict__.iteritems():
                    assert value is not None, \
                        self._formatter.format(
                            'the {key} attribute of add_avamar_grid in yaml file is None'.format(key=key))

            _cluster_types = ('LC1S', 'DR2S', 'CA1S', 'CA2S', 'MP2S', 'MP3S', 'LC2S', 'VS1S', 'VS2S')
            _cluster_type = str(self.onboard_cluster_type).upper()
            self.assertIn(_cluster_type, _cluster_types,
                          msg='The "onboard cluster type" is unspecified.')

            _required_sites, _required_vcenters, _required_hwis = (0, 0, 0)
            if _cluster_type in ('LC1S', 'CA1S', 'VS1S'):
                _required_sites, _required_vcenters, _required_hwis = (1, 1, 1)

            if _cluster_type in ('DR2S', 'CA2S', 'MP2S', 'MP3S', 'LC2S', 'VS2S'):
                _required_sites, _required_vcenters, _required_hwis = (2, 2, 2)

            if _cluster_type == 'CA1S':
                _required_hwis = 2
            elif _cluster_type == 'CA2S':
                _required_vcenters = 1
            elif _cluster_type == 'MP2S':
                _required_hwis = 3
            elif _cluster_type == 'MP3S':
                _required_sites, _required_hwis = (3, 3)
            else:
                pass

            self.assertGreaterEqual(
                len(self.ctx_in.added_sites), _required_sites,
                msg=self._formatter.format('at least {} site(s) are required'.format(_required_sites)))
            self.assertGreaterEqual(
                len(self.ctx_in.added_vcenter), _required_vcenters,
                msg=self._formatter.format('at least {} vCenter(s) are required'.format(_required_vcenters)))
            self.assertGreaterEqual(
                len(self.ctx_in.added_hwi), _required_hwis,
                msg=self._formatter.format('at least {} hardware island(s) are required'.format(_required_hwis)))

    def _finalize_context(self):
        setattr(self.ctx_out, 'added_avamar_grid', self.added_avamar_grid)
        if len(self.added_avamar_grid) > 0:
            logger.info('Added Avamar Grids: {}'.format(
                ' '.join([str(item) for item in self.added_avamar_grid])), False, True)
        if len(self.added_failed_avamargrids) > 0:
            logger.error('Failed Avamar Grids: {}'.format(
                ' '.join([str(item) for item in self.added_failed_avamargrids])), False)


    def _avamar_grid_exist(self,
                           avamar_grid,
                           vro_response_dict,
                           vro_rest_base):
        """  
        Args:
            avamar_grid: avamar_grid input parameters object(Object)            
            vro_response_dict: vro request response dict(dict)
            vro_rest_base: VRORestBase Object(Object)
        """
        avamar_grid_existed_dict = dict(name=False, fqdn=False)
        for item in vro_response_dict.get('relations', {}).get('link', []):
            item_attr = vro_rest_base.name_value_pairs_to_dict(item.get('attributes', {}))
            avamar_grid_existed_dict = dict(name=False, fqdn=False)
            if item_attr:
                if avamar_grid.avamar_grid_name == item_attr.get('name'):
                    avamar_grid_existed_dict['name'] = True
                    logger.info("avamar grid name: {0} is already in use.".format(avamar_grid.avamar_grid_name))
                if avamar_grid.avamar_grid_fqdn_name == item_attr.get('fqdn'):
                    avamar_grid_existed_dict['fqdn'] = True
                    logger.info("FQDN: {0} is already in use with avamar grid name : {1}.".format(
                        avamar_grid.avamar_grid_fqdn_name,avamar_grid.avamar_grid_name))

            # If the avamar_grid's name or fqdn is occupied, end the loop
            if avamar_grid_existed_dict['name'] or \
                    avamar_grid_existed_dict['fqdn']:
                break
        return avamar_grid_existed_dict
