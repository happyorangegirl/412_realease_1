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

# pylint: disable=no-member, too-few-public-methods

import time

from robot.api import logger

from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared import CatalogPage
from ehc_e2e.auc.uimap.shared import LoadingWindow
from ehc_e2e.auc.uimap.specific import AvamarProxyPage


class AvamarProxyManager(BaseUseCase):
    class Func(object):
        ADD_AVAMAR_PROXY, DELETE_AVAMAR_PROXY = (
            'test_add_avamar_proxy',
            'test_delete_avamar_proxy'
        )
    REQUEST_SUCCESSFUL = 'Successful'
    _formatter = 'Running on step: "Deploy Avamar Proxy"-FAILED, {}'

    def __init__(self, name=None, method_name=Func.ADD_AVAMAR_PROXY, **kwargs):
        super(AvamarProxyManager, self).__init__(
            name, method_name, **kwargs)
        _auc_name = ' '.join([word.capitalize() for word in name.split('_')])
        self._formatter = ('Running on step: ' + _auc_name + ' - FAILED, {step}').format
        self._added_avamar_proxies = []

    def setUp(self):
        self._avamar_proxy_maintenance_page = AvamarProxyPage()
        self._loading_window = LoadingWindow()

    def test_add_avamar_proxy(self):
        self._start_avamar_proxy_maintenance()
        self._choose_action(self._add_avamar_proxy_action)
        self._fill_proxy_information()
        self._fill_avamar_infomation()
        self._fill_deployment_server_information()
        self._review_submit_request()

    def test_delete_avamar_proxy(self):
        pass

    def _dropdownlist_selection(self,
                                dropdownlist_name,
                                btn_dropdownlist_open,
                                item_to_select=None,
                                default_select_first=False):
        self.assertTrue(
            btn_dropdownlist_open.exists(),
            self._formatter(step='"{}" dropdownlist open button does not exist.'.format(dropdownlist_name)))

        if default_select_first:
            btn_dropdownlist_open.click()
            if not self._avamar_proxy_maintenance_page.click_drop_down_list(
                    self._avamar_proxy_maintenance_page.lnk_dropdownlist, 'div', item_to_select, True):
                logger.info(
                    'Selecting first item by default since given item"{} is not found in dropdownlist.'.format(
                        item_to_select), False, True)
                self.assertTrue(
                    self._avamar_proxy_maintenance_page.select_drop_down_list_by_index(
                        self._avamar_proxy_maintenance_page.lnk_dropdownlist, 'div', 0),
                    self._formatter(
                        step='item:{} not found from {} dropdownlist but try to select first item also failed.'.format(
                            dropdownlist_name, item_to_select)
                    )
                )
        else:
            btn_dropdownlist_open.click()
            self.assertTrue(
                self._avamar_proxy_maintenance_page.click_drop_down_list(
                    self._avamar_proxy_maintenance_page.lnk_dropdownlist, 'div', item_to_select, True),
                self._formatter(
                    step='Selecting item:{} from {} dropdwonlist failed.'.format(item_to_select, dropdownlist_name))
            )
        self._loading_window.wait_loading(self._current_browser, 30)

    def _fill_in_text_box(self,
                          text_box_name, text_box_element, text_to_fill, use_default_value=False, default_value=''):
        self.assertTrue(
            text_box_element.exists(),
            self._formatter(step='textbox: "{}" does not exist.'.format(text_box_name)))

        if use_default_value:
            if text_box_element.value.strip() == default_value.strip():
                logger.info(
                    'Default value for textbox: "{}" is "{}", match our expectation, will use it directly.'.format(
                        text_box_name, default_value)
                )
            else:
                logger.warn(
                    'We expected default value of textbox: "{}" to be "{}", but it is not. will use given value:{} to '
                    'set.'.format(text_box_name, default_value, text_to_fill))
                text_box_element.set(text_to_fill)
        else:
            text_box_element.set(text_to_fill)

        # self._avamar_proxy_maintenance_page.wait_for_loading_complete(1)
        logger.info('Filled in "{}" with: {}'.format(text_box_name, text_to_fill), False, True)
        self._loading_window.wait_loading(self._current_browser, 30)

    def _start_avamar_proxy_maintenance(self):
        catalog_page = CatalogPage()
        self.assertTrue(
            catalog_page.navigate_to_catalog(self._current_browser, wait_loading_time=1),
            msg=self._formatter(step='failed to switch to catalog frame.'))
        self.assertTrue(
            catalog_page.lnk_data_protection_services.exists(),
            msg=self._formatter(step='cannot find Data Protection Services button in the left page.'))
        catalog_page.lnk_data_protection_services.click()
        catalog_page.wait_for_loading_complete(1)
        self.assertTrue(
            catalog_page.btn_avamar_proxy_maintenance_request.exists(),
            msg=self._formatter(step='cannot find Avamar Proxy Maintenance request button in catalog page.'))
        catalog_page.btn_avamar_proxy_maintenance_request.click()
        logger.info('Completed clicking Avamar Proxy maintenance request button.', False, True)
        self._loading_window.wait_loading(self._current_browser, 30)

    def _choose_action(self, action):
        logger.info(msg='Start to fill info in tab: Request Information')
        self.assertTrue(
            self._avamar_proxy_maintenance_page.txt_description.exists(),
            msg=self._formatter(step='there is no description textbox.'))
        self._avamar_proxy_maintenance_page.txt_description.set(self._description)
        logger.info('Filled in description textbox with: {}.'.format(self._description))
        if self._avamar_proxy_maintenance_page.txt_reasons.exists():
            self._avamar_proxy_maintenance_page.txt_reasons.set(
                'Avamar Proxy Maintenance:{}'.format(action))
            logger.info(
                'Filled in reasons textbox with: {}'.format('Avamar Proxy Maintenance:{}'.format(action)))
        time.sleep(3)
        logger.info(msg='Completed filling Request information tab.')
        self._click_next_button()

        logger.info(msg='Start to fill in tab: Action Choice')
        self.assertTrue(
            self._avamar_proxy_maintenance_page.btn_actions_menu_open.exists(),
            msg=self._formatter(step='Actions DropDownList open button does not exist.'))

        self._avamar_proxy_maintenance_page.btn_actions_menu_open.click()
        self.assertTrue(
            self._avamar_proxy_maintenance_page.click_drop_down_list(
                self._avamar_proxy_maintenance_page.lnk_dropdownlist, 'div', action),
            msg=self._formatter(step='there is no action: {} in Actions dropdownlist.'.format(action)))

        self._loading_window.wait_loading(self._current_browser, 30)
        logger.info(msg='Completed fill info in tab: Action Choice')
        self._click_next_button()

    def _fill_proxy_information(self):
        logger.info('Start to fill in Proxy Information tab.', False, True)
        self._dropdownlist_selection(
            'DNS Updated', self._avamar_proxy_maintenance_page.btn_dns_updated_menu_open, self._dns_updated)
        self._dropdownlist_selection(
            'Cluster', self._avamar_proxy_maintenance_page.btn_cluster_menu_open, self._tenant_cluster)
        self._dropdownlist_selection(
            'Datastore', self._avamar_proxy_maintenance_page.btn_datastore_menu_open, self._datastore, True)
        self._dropdownlist_selection(
            'Network', self._avamar_proxy_maintenance_page.btn_network_menu_open, self._proxy_network)

        self._fill_in_text_box('VM Name', self._avamar_proxy_maintenance_page.txt_vm_name, self._proxy_vm_name)
        self._fill_in_text_box('Avamar Path', self._avamar_proxy_maintenance_page.txt_avamar_path, self._avamar_path)
        self._fill_in_text_box('IP', self._avamar_proxy_maintenance_page.txt_ip, self._proxy_ip)
        self._fill_in_text_box('NetMask', self._avamar_proxy_maintenance_page.txt_net_mask, self._proxy_netmask)
        self._fill_in_text_box('Gateway', self._avamar_proxy_maintenance_page.txt_gateway, self._proxy_gateway)
        self._fill_in_text_box(
            'DNS Server IP', self._avamar_proxy_maintenance_page.txt_dns_svr_ip, self._dns_server_ip)
        self._fill_in_text_box(
            'Proxy User Name', self._avamar_proxy_maintenance_page.txt_proxy_username,
            self._proxy_username, use_default_value=True, default_value='root')
        self._fill_in_text_box(
            'Proxy Password', self._avamar_proxy_maintenance_page.txt_proxy_password, self._proxy_password)
        logger.info('Completed filling in Proxy Information tab.', False, True)
        self._click_next_button()

    def _fill_avamar_infomation(self):
        logger.info('Start to fill in Avamar Information tab.', False, True)
        self._dropdownlist_selection(
            'Avamar Grid', self._avamar_proxy_maintenance_page.btn_avamar_grid_name_menu_open, self._avamar_grid)
        self._fill_in_text_box(
            'Avamar Domain', self._avamar_proxy_maintenance_page.txt_avamar_domain, self._avamar_domain)
        self._avamar_proxy_maintenance_page.wait_for_loading_complete(1)
        self._fill_in_text_box('OVA', self._avamar_proxy_maintenance_page.txt_ova_location, self._ova)
        logger.info('Completed filling in Avamar Information tab.', False, True)
        self._click_next_button()

    def _fill_deployment_server_information(self):
        logger.info('Start to fill in Server Information tab.', False, True)
        self._fill_in_text_box(
            'Deployment Server', self._avamar_proxy_maintenance_page.txt_deployment_server, self._deployment_server)
        self._fill_in_text_box(
            'Deployment Username', self._avamar_proxy_maintenance_page.txt_deployment_server_username,
            self._deployment_server_username)
        self._fill_in_text_box(
            'Deployment Password', self._avamar_proxy_maintenance_page.txt_deployment_server_password,
            self._deployment_server_password)
        self._dropdownlist_selection(
            'Disable Verification', self._avamar_proxy_maintenance_page.btn_disable_verification_menu_open,
            self._disable_verification)
        logger.info('Completed filling Server Information tab.', False, True)
        self._click_next_button()

    def _review_submit_request(self):
        logger.info(msg='Start to process "Review and Submit" tab.')
        self.assertTrue(
            self._avamar_proxy_maintenance_page.lbl_review_and_submit_tab.exists(),
            msg=self._formatter(step='Action label in tab Review and Submit does not exist.'))

        self.assertTrue(
            self._avamar_proxy_maintenance_page.btn_submit.exists(), self._formatter(step='there is no Submit button.'))
        logger.info('Completed processing "Review and Submit" tab.', False, True)

        self._avamar_proxy_maintenance_page.btn_submit.click()
        logger.info('Clicked Submit button.')
        self._avamar_proxy_maintenance_page.wait_for_loading_complete(2)

        self.assertTrue(
            self._avamar_proxy_maintenance_page.lbl_confirmation_success.exists(),
            msg=self._formatter(step='label "The request has been submitted successfully" does not exist.'))

        self.assertTrue(
            self._avamar_proxy_maintenance_page.btn_ok.exists(), msg=self._formatter(step='there is no OK button.'))
        self._avamar_proxy_maintenance_page.btn_ok.click()
        logger.info('Click OK button in "The request has been submitted successfully" page.')

    def _click_next_button(self):
        self.assertTrue(
            self._avamar_proxy_maintenance_page.btn_next.exists(), msg=self._formatter(step='there is no Next button.'))
        self._avamar_proxy_maintenance_page.btn_next.click()
        logger.info('Clicked next button.', False, True)
        self._loading_window.wait_loading(self._current_browser, 30)

    def _validate_input_args(self, **kwargs):
        if self._testMethodName == self.Func.ADD_AVAMAR_PROXY:
            self._init_config_data_of_add_avamar_proxy(**kwargs)
        elif self._testMethodName == self.Func.DELETE_AVAMAR_PROXY:
            self._init_config_data_of_delete_avamar_proxy(**kwargs)
        else:
            raise ValueError('Unsupported test method:{} for Avamar Proxy maintenance.'.format(self._testMethodName))

    def _init_config_data_of_add_avamar_proxy(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, '_{}'.format(k), v)
        self._add_avamar_proxy_action = 'Add Proxy'

    def _init_config_data_of_delete_avamar_proxy(self, **kwargs):
        pass

    def _finalize_output_params(self):
        # TODO: may need change after environment is back, see what is representation of added Avamar Proxy.
        pass
