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
from ehc_e2e.auc.uimap.shared import BasePage, LoadingWindow, CatalogPage
from ehc_e2e.auc.uimap.specific import HwiManagerPage


class HwiManager(BaseUseCase):
    # Pressing a TAB button after providing value in textbox field ,Otherwise the page is not loading/updating
    # with this change.
    # Removed selecting and unselecting the first element in HWI Array checkboxes since need to activate the
    # checkboxes before clicking, as it is fixed with after Tab Click.
    class Func(object):
        ADD_HWI, DELETE_HWI, UPDATE_HWI = (
            'test_adding_hwi',
            'test_deleting_hwi',
            'test_updating_hwi')

    def __init__(self, name=None, method_name=Func.ADD_HWI, **kwargs):
        super(HwiManager, self).__init__(
            name, method_name, **kwargs)

        self._add_hwi_name = None

        self._update_hwi_name = None

        self._auc_name = ' '.join([word.capitalize() for word in name.split('_')])
        self._formatter = ('Running on step: ' + self._auc_name + ' - FAILED, "{}"').format

    def setUp(self):
        self.catalog_page = CatalogPage()
        self.loading_window = LoadingWindow()
        self.hwi_manager_page = HwiManagerPage()

    def tearDown(self):
        pass

    # Moved the txt_hwi_name element in _add_hwi to down as we are facing issues with the click_drop_down_list
    # element next to it is failing
    def test_adding_hwi(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._add_hwi()
        self._submit_request()

    # Moved the txt_update_hwi_name element in _update_hwi to down as we are facing issues with the
    # click_drop_down_list element next to it is failing
    def test_updating_hwi(self):
        self._start_new_service_request()
        try:
            self._fill_out_request_info()
            self._update_hwi()
            self._submit_request()
        except:
            self.fail('Edit Hardware Island encounters exception: {}'.format(sys.exc_info()))

    def test_deleting_hwi(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._delete_hwi()
        self._submit_request()

    def _start_new_service_request(self):

        self.assertTrue(self.catalog_page.navigate_to_catalog(self._browser),
                        msg=self._formatter('failed to switch to catalog frame.'))

        self.hwi_manager_page.btn_ehc_configure.click()
        self.loading_window.wait_loading(self._browser, 90)
        self.catalog_page.btn_hwi_maintenance_request.click()

    def _fill_out_request_info(self):

        self.assertTrue(self.hwi_manager_page.txt_description.exists(),
                        msg=self._formatter('failed to navigate to Hardware Island Endpoint Maintenance Request page'))
        self.hwi_manager_page.txt_description.set(self._testMethodName)
        logger.info('Typed description: {}.'.format(self._testMethodName), False, True)
        self.hwi_manager_page.txt_reasons.set(self._name)
        logger.info('Typed reasons: {}.'.format(self._name), False, True)
        self.hwi_manager_page.btn_next.click()
        logger.info('Clicked next button.', False, True)

    def _submit_request(self):

        BasePage().wait_for_loading_complete(wait_time=2)
        LoadingWindow().wait_loading(self._browser)
        self.assertTrue(self.hwi_manager_page.btn_submit.exists(), self._formatter('No Submit button found.'))
        self.hwi_manager_page.btn_submit.click()
        logger.info('Clicked submit button.', False, True)
        if self.hwi_manager_page.lbl_confirmation_success.exists():
            self.hwi_manager_page.wait_for_loading_complete(2)
            self.hwi_manager_page.btn_ok.click()
            logger.info('Clicked ok button.')
        else:
            self.fail(msg=self._formatter('label: "The request has been submitted successfully" does not exist'))

    def _add_hwi_block(self):
        _formatter = 'Running on step:Add VxRack(Flex)/VxBlock based Hardware Island - FAILED, "{step}".'

        self.assertTrue(self.hwi_manager_page.btn_provider_vcenter_vipr.exists(),
                        msg=_formatter.format(step='vCenter dropdownlist open button does not exist')
                       )
        self.hwi_manager_page.btn_provider_vcenter_vipr.click()
        logger.info('Clicked dropdown list: vCenter.', False, True)
        self.assertTrue(self.hwi_manager_page.click_drop_down_list(self.hwi_manager_page.lbl_active_value,
                                                                   'div', self.hwi_info['vcenter_name_active']),
                        msg=_formatter.format(
                            step='vCenter:{} not found from dropdownlist'.format(self.hwi_info['vcenter_name_active']))
                       )
        logger.info('Selected vCenter: {}.'.format(self.hwi_info['vcenter_name_active']), False, True)
        self.loading_window.wait_loading(self._browser, 90)
        self.assertTrue(self.hwi_manager_page.btn_provider_site_vipr.exists(),
                        msg=_formatter.format(step='site dropdownlist open button does not exist'))

        self.hwi_manager_page.btn_provider_site_vipr.click()
        logger.info('Clicked dropdown list: Site Name.', False, True)
        self.assertTrue(self.hwi_manager_page.click_drop_down_list(self.hwi_manager_page.lbl_active_value,
                                                                   'div', self.hwi_info['site_name_active']),
                        msg=_formatter.format(
                            step='site:{} not found from dropdownlist'.format(self.hwi_info['site_name_active'])))
        logger.info('Selected site name: {}'.format(self.hwi_info['site_name_active']), False, True)
        self.loading_window.wait_loading(self._browser, 90)

        self.assertTrue(self.hwi_manager_page.btn_provider_vipr_to_add.exists(),
                        msg=_formatter.format(step='ViPR instance open button does not exist'))
        self.loading_window.wait_loading(self._browser, 90)
        self.hwi_manager_page.btn_provider_vipr_to_add.click()
        logger.info('Clicked drop down list ViPR Instance.', False, True)
        self.assertTrue(self.hwi_manager_page.click_drop_down_list(self.hwi_manager_page.lbl_active_value,
                                                                   'div', self.hwi_info['vipr_active']),
                        msg=_formatter.format(
                            step='ViPR:{} not found from dropdownlist'.format(self.hwi_info['vipr_active'])))
        logger.info('Selected ViPR Instance: {}.'.format(self.hwi_info['vipr_active']), False, True)
        self.assertTrue(self.hwi_manager_page.txt_hwi_name_vipr.exists(),
                        msg=_formatter.format(
                            step='hwi name textbox does not exist'))
        self.hwi_manager_page.txt_hwi_name_vipr.set(self.hwi_info['hwi_name'])
        logger.info('Input hwi name:{} into textbox.'.format(self.hwi_info['hwi_name']), False, True)

        self.hwi_manager_page.send_tab_key(self.hwi_manager_page.txt_hwi_name_vipr)

        BasePage().wait_for_loading_complete(wait_time=2)
        self.loading_window.wait_loading(self._browser, 90)

        self.assertTrue(self.hwi_manager_page.lbl_active_checkbox.exists(),
                        msg=_formatter.format(step='HWI Arrays checkbox does not exist'))

        # selecting the provided vipr arrays in the config file
        for vipr_array in self.hwi_info['vipr_active_check']:
            try:
                self.hwi_manager_page.lbl_active_checkbox.current.find_element_by_xpath(
                    self.hwi_manager_page.contains_text.format(vipr_array)
                ).click()
                logger.info('ViPR Array: {} is selected'.format(vipr_array), False, True)
                self.loading_window.wait_loading(self._browser, 90)
            except Exception as ex:
                logger.error(ex.message)
                raise AssertionError(_formatter.format(
                    step='ViPR Array:{} not found from ViPR checkbox items'.format(vipr_array)))
        self.loading_window.wait_loading(self._browser, 90)
        self._add_hwi_name = self.hwi_info['hwi_name']
        self.hwi_manager_page.btn_next.click()
        logger.info('Clicked next button.', False, True)
        self.loading_window.wait_loading(self._browser, 90)

    def _add_hwi_vsan(self):
        _formatter = 'Running on step: Add VxRail based Hardware Island - FAILED, {step}'

        self.assertTrue(self.hwi_manager_page.btn_provider_vcenter.exists(),
                        msg=_formatter.format(step='vCenter dropdownlist open button does not exist')
                       )

        self.hwi_manager_page.btn_provider_vcenter.click()
        self.assertTrue(self.hwi_manager_page.click_drop_down_list(self.hwi_manager_page.lbl_active_value,
                                                                   'div', self.hwi_info['vcenter_name_active']),
                        msg=_formatter.format(
                            step='vCenter:{} not found from dropdownlist'.format(self.hwi_info['vcenter_name_active']))
                       )
        logger.info('Selected vCenter:{} from dropdownlist.'.format(self.hwi_info['vcenter_name_active']), False, True)
        self.loading_window.wait_loading(self._browser, 90)
        self.assertTrue(self.hwi_manager_page.btn_provider_site.exists(),
                        msg=_formatter.format(step='site dropdownlist open button does not exist'))

        self.hwi_manager_page.btn_provider_site.click()
        self.assertTrue(self.hwi_manager_page.click_drop_down_list(self.hwi_manager_page.lbl_active_value,
                                                                   'div', self.hwi_info['site_name_active']),
                        msg=_formatter.format(
                            step='site:{} not found from dropdownlist'.format(self.hwi_info['site_name_active']))
                       )
        logger.info('Selected Site:{} from dropdownlist.'.format(self.hwi_info['site_name_active']), False, True)
        self.loading_window.wait_loading(self._browser, 90)
        self.assertTrue(self.hwi_manager_page.txt_hwi_name.exists(),
                        msg=_formatter.format(
                            step='hwi name textbox does not exist'))
        self.hwi_manager_page.txt_hwi_name.set(self.hwi_info['hwi_name'])
        self.hwi_manager_page.send_tab_key(self.hwi_manager_page.txt_hwi_name)
        BasePage().wait_for_loading_complete(wait_time=2)
        logger.info('Input hwi name:{} into textbox.'.format(self.hwi_info['hwi_name']), False, True)
        self._add_hwi_name = self.hwi_info['hwi_name']
        self.hwi_manager_page.btn_next.click()
        logger.info('Clicked Next Button', False, True)
        self.loading_window.wait_loading(self._browser, 90)

    def _add_hwi(self):
        _formatter = 'Running on step:Add Hardware Island - FAILED, "{step}".'
        try:
            self.assertTrue(self.hwi_manager_page.btn_performed_tab.exists(),
                            msg=_formatter.format(
                                step='after clicking the next button, can not find the Action to be performed input')
                           )
            self.hwi_manager_page.btn_performed_tab.click()
            logger.info('Clicked drop down list: Action', False, True)

            self.assertTrue(self.hwi_manager_page.click_drop_down_list(self.hwi_manager_page.lbl_active_value,
                                                                       'div', self.hwi_info['performed_active']),
                            msg=_formatter.format(
                                step='select performed_active type {} does not exist'.format(
                                    self.hwi_info['performed_active']))
                           )
            logger.info('Selected action:{} from drop down list.'.format(self.hwi_info['performed_active']),
                        False, True)
            self.loading_window.wait_loading(self._browser, 90)
            self.hwi_manager_page.btn_next.click()
            logger.info('clicked Next Button', False, True)
            self.loading_window.wait_loading(self._browser, 90)

            if self.hwi_info['performed_active'] == 'Add VxRack(Flex)/VxBlock based Hardware Island':
                self._add_hwi_block()
            elif self.hwi_info['performed_active'] == 'Add VxRail based Hardware Island':
                self._add_hwi_vsan()
            else:
                raise NotImplementedError('Unsupported action {} for Add HWI.'.format(
                    self.hwi_info['performed_active']))

        except AssertionError:
            self.hwi_manager_page.save_request()
            raise

        except:
            self.hwi_manager_page.save_request()
            self.fail(
                _formatter.format(step='add Hardware Island') + ', more error info: {}'.format(sys.exc_info()[:2]))

    def _update_hwi_vsan(self):
        _formatter = 'Running on step: Edit VxRAil based Hardware Island - FAILED, "{step}".'

        self.assertTrue(self.hwi_manager_page.btn_provider_update_hwi_name.exists(),
                        msg=_formatter.format(step='HWI dropdownlist open button does not exist')
                       )
        self.hwi_manager_page.btn_provider_update_hwi_name.click()
        logger.info('Clicked drop down list: Hardware Instance.', False, True)
        self.assertTrue(self.hwi_manager_page.click_drop_down_list(self.hwi_manager_page.lbl_active_value,
                                                                   'div', self.hwi_info['old_hwi_name']),
                        msg=_formatter.format(
                            step='HWI:{} not found from dropdownlist'.format(self.hwi_info['old_hwi_name']))
                       )
        logger.info('Selected HWI:{} from drop down list.'.format(self.hwi_info['old_hwi_name']), False, True)
        self.loading_window.wait_loading(self._browser, 90)

        self.assertTrue(self.hwi_manager_page.btn_provider_update_vcenter.exists(),
                        msg=_formatter.format(step='vCenter dropdownlist open button does not exist'))
        self.hwi_manager_page.btn_provider_update_vcenter.click()
        logger.info('Clicked drop down list: vCenter.', False, True)

        self.assertTrue(self.hwi_manager_page.click_drop_down_list(self.hwi_manager_page.lbl_active_value,
                                                                   'div', self.hwi_info['edit_vcenter_name_active']),
                        msg=_formatter.format(
                            step='vCenter:{} not found from dropdownlist'.format(
                                self.hwi_info['edit_vcenter_name_active'])
                        )
                       )
        logger.info('Selected vCenter:{} from drop down list.'.format(
            self.hwi_info['edit_vcenter_name_active']), False, True)
        self.loading_window.wait_loading(self._browser, 90)
        self.assertTrue(self.hwi_manager_page.btn_provider_update_site.exists(),
                        msg=_formatter.format(step='site drop down list open button does not exist'))
        self.hwi_manager_page.btn_provider_update_site.click()
        logger.info('Clicked drop down list: Site Name.', False, True)
        self.assertTrue(self.hwi_manager_page.click_drop_down_list(self.hwi_manager_page.lbl_active_value,
                                                                   'div', self.hwi_info['edit_site_name_active']),
                        msg=_formatter.format(
                            step='site:{} not found from dropdownlist'.format(self.hwi_info['edit_site_name_active']))
                       )
        logger.info('Selected site:{} from dropdownlist.'.format(self.hwi_info['edit_site_name_active']), False, True)
        self.loading_window.wait_loading(self._browser, 90)

        self.assertTrue(self.hwi_manager_page.txt_update_hwi_name.exists(),
                        msg=_formatter.format(
                            step='update hwi name textbox does not exists'))
        self.hwi_manager_page.txt_update_hwi_name.set(self.hwi_info['edit_hwi_name'])
        self.hwi_manager_page.send_tab_key(self.hwi_manager_page.txt_update_hwi_name)
        BasePage().wait_for_loading_complete(wait_time=2)
        logger.info('Input new hwi name:{} into textbox.'.format(self.hwi_info['edit_hwi_name']), False, True)
        BasePage().wait_for_loading_complete(wait_time=5)
        logger.info('Waited 5 seconds for loading window to appear.', False, True)
        self.loading_window.wait_loading(self._browser, 90)
        self._update_hwi_name = self.hwi_info['edit_hwi_name']
        self.hwi_manager_page.btn_next.click()
        logger.info('clicked Next Button', False, True)
        self.loading_window.wait_loading(self._browser, 90)

    def _update_hwi_block(self):
        _formatter = 'Running on step:Edit VxRack(Flex)/VxBlock based Hardware Island - FAILED, "{step}".'

        self.assertTrue(self.hwi_manager_page.btn_provider_update_hwi_name_vipr.exists(),
                        msg=_formatter.format(step='HWI dropdownlist open button does not exist')
                       )
        self.hwi_manager_page.btn_provider_update_hwi_name_vipr.click()
        logger.info('Clicked drop down list: Hardware Island.', False, True)
        self.assertTrue(self.hwi_manager_page.click_drop_down_list(self.hwi_manager_page.lbl_active_value,
                                                                   'div', self.hwi_info['old_hwi_name']),
                        msg=_formatter.format(
                            step='HWI:{} not found from dropdownlist'.format(self.hwi_info['old_hwi_name']))
                       )
        logger.info('Selected HWI:{} from dropdownlist.'.format(self.hwi_info['old_hwi_name']), False, True)
        self.loading_window.wait_loading(self._browser, 90)

        self.assertTrue(self.hwi_manager_page.btn_provider_update_vcenter_vipr.exists(),
                        msg=_formatter.format(step='vCenter dropdownlist open button does not exist'))
        self.hwi_manager_page.btn_provider_update_vcenter_vipr.click()
        logger.info('Clicked drop down list: vCenter.', False, True)
        self.assertTrue(self.hwi_manager_page.click_drop_down_list(self.hwi_manager_page.lbl_active_value,
                                                                   'div', self.hwi_info['edit_vcenter_name_active']),
                        msg=_formatter.format(
                            step='vCenter:{} not found from dropdownlist'.format(
                                self.hwi_info['edit_vcenter_name_active']))
                       )
        logger.info('Selected vCenter:{} from dropdownlist.'.format(
            self.hwi_info['edit_vcenter_name_active']), False, True)
        self.loading_window.wait_loading(self._browser, 90)
        self.assertTrue(self.hwi_manager_page.btn_provider_update_site_vipr.exists(),
                        msg=_formatter.format(step='site dropdownlist open button does not exist'))
        self.hwi_manager_page.btn_provider_update_site_vipr.click()
        self.assertTrue(self.hwi_manager_page.click_drop_down_list(self.hwi_manager_page.lbl_active_value,
                                                                   'div', self.hwi_info['edit_site_name_active']),
                        msg=_formatter.format(
                            step='site:{} not found from dropdownlist'.format(self.hwi_info['edit_site_name_active']))
                       )
        logger.info('Selected site:{} from dropdownlist.'.format(self.hwi_info['edit_site_name_active']), False, True)
        self.loading_window.wait_loading(self._browser, 90)
        self.assertTrue(self.hwi_manager_page.btn_provider_update_vipr.exists(),
                        msg=_formatter.format(step='ViPR instance open button does not exist'))
        self.loading_window.wait_loading(self._browser, 90)
        self.hwi_manager_page.btn_provider_update_vipr.click()
        logger.info('Clicked drop down list: ViPR Instance.', False, True)
        self.assertTrue(self.hwi_manager_page.click_drop_down_list(self.hwi_manager_page.lbl_active_value,
                                                                   'div', self.hwi_info['edit_vipr_active']),
                        msg=_formatter.format(
                            step='ViPR:{} not found from dropdownlist'.format(self.hwi_info['edit_vipr_active']))
                       )
        logger.info('Selected ViPR:{} from dropdownlist.'.format(self.hwi_info['edit_vipr_active']), False, True)
        self.assertTrue(self.hwi_manager_page.lbl_provider_update_vipr_checkbox.exists(),
                        msg=_formatter.format(step='HWI Arrays checkbox does not exist'))

        all_tag_input_elements = self.hwi_manager_page.lbl_provider_update_vipr_checkbox.current.\
            find_elements_by_tag_name('input')

        self.assertTrue(len(all_tag_input_elements), msg="No vipr options shown.")

        for counter in range(len(all_tag_input_elements)):
            if self.hwi_manager_page.lbl_provider_update_vipr_checkbox.current.find_elements_by_tag_name(
                    'input')[counter].get_attribute('checked') is not None:
                self.hwi_manager_page.lbl_provider_update_vipr_checkbox.current.find_element_by_xpath(
                    self.hwi_manager_page.contains_text.format(
                        self.hwi_manager_page.lbl_provider_update_vipr_checkbox.current.find_elements_by_tag_name(
                            'label')[counter].text)).click()
            self.loading_window.wait_loading(self._browser, 90)
        logger.info('Unselected all the HWI Array Checkboxes', False, True)
        for vipr_array_item in self.hwi_info['edit_vipr_active_check']:
            self.hwi_manager_page.lbl_provider_update_vipr_checkbox.current.find_element_by_xpath(
                self.hwi_manager_page.contains_text.format(
                    vipr_array_item)).click()
            logger.info('Selected HWI Array:{} Checkbox.'.format(vipr_array_item), False, True)
            self.loading_window.wait_loading(self._browser, 90)

        self.assertTrue(self.hwi_manager_page.txt_update_hwi_name_vipr.exists(),
                        msg=_formatter.format(
                            step='update hwi name textbox does not exists'))
        self.hwi_manager_page.txt_update_hwi_name_vipr.set(self.hwi_info['edit_hwi_name'])
        logger.info('Input new hwi name:{} into textbox.'.format(self.hwi_info['edit_hwi_name']), False, True)
        BasePage().wait_for_loading_complete(wait_time=5)
        logger.info('Waited 5 seconds for loading window to appear.', False, True)
        self.loading_window.wait_loading(self._browser, 90)
        self._update_hwi_name = self.hwi_info['edit_hwi_name']
        self.assertTrue(self.hwi_manager_page.btn_next.exists())
        self.hwi_manager_page.send_tab_key(self.hwi_manager_page.btn_next)
        BasePage().wait_for_loading_complete(wait_time=5)
        self.loading_window.wait_loading(self._browser, 90)
        self.hwi_manager_page.btn_next.click()
        logger.info('Clicked Next button.', False, True)
        self.loading_window.wait_loading(self._browser, 90)
        if not self.hwi_manager_page.btn_submit.exists():
            logger.warn('Submit button not found after clicking Next button, try 5 times to click next button.')
            # add code to try click next button until validate success and go into summit page.
            i = 0
            while i < 5 and not self.hwi_manager_page.btn_submit.exists():
                i += 1
                BasePage().wait_for_loading_complete(3)
                logger.warn('Try to click Next Button in {} times'.format(i))
                self.loading_window.wait_loading(self._browser, 90)
                self.hwi_manager_page.btn_next.click()

    def _update_hwi(self):
        _formatter = 'Running on step:Edit Hardware Island - FAILED, "{step}".'
        try:
            self.assertTrue(self.hwi_manager_page.btn_performed_tab.exists(),
                            msg=_formatter.format(
                                step='after clicking the next button, cannot find the Action to be performed input'))
            self.hwi_manager_page.btn_performed_tab.click()
            self.loading_window.wait_loading(self._browser, 90)
            self.assertTrue(self.hwi_manager_page.click_drop_down_list(self.hwi_manager_page.lbl_active_value,
                                                                       'div', self.hwi_info['performed_active']),
                            msg=_formatter.format(
                                step='select performed_active type {} does not exist'.format(
                                    self.hwi_info['performed_active']))
                           )
            logger.info('Selected action:{} from dropdownlist.'.format(self.hwi_info['performed_active']), False, True)
            self.loading_window.wait_loading(self._browser, 90)
            self.hwi_manager_page.btn_next.click()
            logger.info('clicked Next Button', False, True)
            self.loading_window.wait_loading(self._browser, 90)

            if self.hwi_info['performed_active'] == 'Edit VxRack(Flex)/VxBlock based Hardware Island':
                self._update_hwi_block()
            elif self.hwi_info['performed_active'] == 'Edit VxRail based Hardware Island':
                self._update_hwi_vsan()
            else:
                raise NotImplementedError('Unsupported action {} for Update HWI '.format(
                    self.hwi_info['performed_active']))
        except AssertionError:
            self.hwi_manager_page.save_request()
            raise

        except:
            self.hwi_manager_page.save_request()
            self.fail(
                _formatter.format(step='update Hardware Island') + ', more error info: {}'.format(sys.exc_info()[:2]))

    def _delete_hwi(self):
        _formatter = 'Running on step:Delete Hardware Island - FAILED, "{step}".'
        try:
            self.assertTrue(self.hwi_manager_page.btn_performed_tab.exists(),
                            msg=_formatter.format(
                                step='after clicking the next button, can not find the Action to be performed input')
                           )
            self.hwi_manager_page.btn_performed_tab.click()
            logger.info('Clicked drop down list: Action.', False, True)
            self.assertTrue(self.hwi_manager_page.click_drop_down_list(self.hwi_manager_page.lbl_active_value,
                                                                       'div', self.hwi_info['del_performed_active']),
                            msg=_formatter.format(
                                step='select performed_active type {} does not exist'.format(
                                    self.hwi_info['del_performed_active']))
                           )
            logger.info('Selected action:{} from dropdownlist.'.format(
                self.hwi_info['del_performed_active']), False, True)
            self.loading_window.wait_loading(self._browser, 90)
            self.hwi_manager_page.btn_next.click()
            self.loading_window.wait_loading(self._browser, 90)

            self.assertTrue(self.hwi_manager_page.btn_delete_hwi_name.exists(),
                            msg=_formatter.format(
                                step='HWI dropdownlist open button does not exist')
                           )
            self.hwi_manager_page.btn_delete_hwi_name.click()
            logger.info('Clicked dropdown list: Hardware Island.', False, True)
            self.loading_window.wait_loading(self._browser, 90)
            self.assertTrue(self.hwi_manager_page.click_drop_down_list(self.hwi_manager_page.lbl_active_value,
                                                                       'div', self.hwi_info['hwi_name']),
                            msg=_formatter.format(
                                step='HWI:{} not found from dropdownlist'.format(self.hwi_info['hwi_name']))
                           )
            logger.info('Selected HWI:{} from dropdownlist.'.format(self.hwi_info['hwi_name']), False, True)
            self.loading_window.wait_loading(self._browser, 90)
            self.assertTrue(self.hwi_manager_page.isdel_obj.exists(),
                            msg=_formatter.format(
                                step='option element does not exist: Confirm the delete Hardware Island Obj'))
            self.loading_window.wait_loading(self._browser, 90)
            self.hwi_manager_page.isdel_obj.click()
            logger.info('Clicked drop down list: Confirm.', False, True)
            self.assertTrue(self.hwi_manager_page.click_drop_down_list(self.hwi_manager_page.lbl_active_value,
                                                                       'div', self.hwi_info['isdel_obj']),
                            msg=_formatter.format(
                                step='select delete confirm does not exist')
                           )
            logger.info('Selected Confirm:{} from dropdownlist.'.format(self.hwi_info['isdel_obj']), False, True)
            self.loading_window.wait_loading(self._browser, 90)
            self.hwi_manager_page.btn_next.click()
            logger.info('Clicked Next Button', False, True)
            self.loading_window.wait_loading(self._browser, 90)

        except AssertionError:
            self.hwi_manager_page.save_request()
            raise

        except:
            self.hwi_manager_page.save_request()
            self.fail(_formatter.format(step='delete Hardware Island') + ', more error info: {}'.format(
                sys.exc_info()[:2])
                     )

    def _validate_input_args(self, **kwargs):
        if self._testMethodName == self.Func.ADD_HWI:
            self._validate_args_of_adding_hwi(**kwargs)
        elif self._testMethodName == self.Func.DELETE_HWI:
            self._validate_args_of_deleting_hwi(**kwargs)
        elif self._testMethodName == self.Func.UPDATE_HWI:
            self._validate_args_of_updating_hwi(**kwargs)
        else:
            raise NotImplementedError('Validate method %s '.format(**kwargs))

    def _validate_args_of_adding_hwi(self, browser=None, **hwi_info):

        self.assertIsNotNone(hwi_info, msg=self._formatter('add hwi info should not be None.'))
        self.hwi_info = hwi_info
        self._browser = browser

    def _validate_args_of_updating_hwi(self, browser=None, **hwi_info):
        self.assertIsNotNone(hwi_info, msg=self._formatter('update hwi info should not be None.'))
        self.hwi_info = hwi_info
        self._browser = browser

    def _validate_args_of_deleting_hwi(self, browser=None, **hwi_info):
        self.assertIsNotNone(hwi_info, msg=self._formatter('delete hwi info should not be None.'))
        self.hwi_info = hwi_info
        self._browser = browser

    def _finalize_output_params(self):
        if self._testMethodName == self.Func.ADD_HWI:
            if self._add_hwi_name:
                self._output.append(self._add_hwi_name)
        elif self._testMethodName == self.Func.UPDATE_HWI:
            if self._update_hwi_name:
                self._output.append(self._update_hwi_name)
        else:
            pass
