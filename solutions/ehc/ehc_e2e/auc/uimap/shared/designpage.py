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

from uiacore.modeling.webui.controls import (WebTextBox, WebButton, WebLabel,
                                             WebLink)
from .basepage import BasePage
import sys
from robot.api import logger
from ehc_e2e.auc.uimap.shared.loadingwindow import LoadingWindow
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions


class DesignPage(BasePage):

    def __init__(self):

        self.design_items_extensionid = 'com.vmware.vcac.core.design'
        self.blueprints_extensionid = 'com.vmware.vcac.core.design.blueprints'
        self.blueprints_createoredit_extensionid = 'com.vmware.vcac.core.design.blueprints.createoredit'
        self.xpath_blueprints_createoredit_extensionid = \
            '//*[@extensionid="com.vmware.vcac.core.design.blueprints.createoredit"]'
        self.design_dialoghost_fullpage_extensionid = 'csp.navigation.dialoghost.gwt.fullpage'

        # self.lnk_blueprints_table = WebLink(
        #     xpath='//*[@id="BLUEPRINTS_LIST-body"]/div/div/table/tbody'
        # )

        self.btn_design = WebButton(id='com.vmware.vcac.core.design')
        self.btn_blueprints = WebButton(
            id='com.vmware.vcac.core.design.blueprints'
        )
        self.software_components = WebButton(
            id='com.vmware.vcac.core.design.software'
        )
        self.xaas = WebButton(
            id='csp.designer'
        )
        self.btn_finish = WebButton(id='submit')
        self.btn_save = WebButton(id='save')
        self.btn_cancel = WebButton(id='cancel')
        self.btn_blueprint_publish = WebButton(
            xpath='//*[@id="BLUEPRINTS_LIST"]/div[2]/div/div/a[4]'
        )

        # blueprints
        self.lbl_blueprint_edit_header = WebLabel(
            xpath='//*[starts-with(text(),"Edit Blueprint:")]'
        )
        self.btn_open_blueprint_properties = WebButton(xpath='//*[@title="Blueprint Properties"]')
        self.lbl_blueprint_properties = WebLabel(
            xpath='//*[starts-with(@id, "vcacwindow-") and contains(@id, "header-targetEl")]'
        )

        self.lnk_blueprint_editor_canvas = WebLink(id='BLUEPRINT_EDITOR_CANVAS')

        #vSphere Machine
        # vSphere_Machine_1
        self.xpath_template_vsphere_machine_item = '//*[@data-qtip="vSphere Machine ({})"]'
        self.xpath_template_vsphere_machine = '//div[contains(@data-qtip,"vSphere (vCenter) Machine")]'
        self.lnk_template_vsphere_machine = WebLink(xpath='//div[contains(@data-qtip,"vSphere (vCenter) Machine")]')
        self.lnk_vsphere_machine_edit_tab_general = WebLink(
            xpath='//span[text()="General"]'
        )
        self.btn_open_reservation_policy_dropdownlist = WebButton(
            xpath='//span[text()="Reservation policy:"]/parent::span/parent::label/'
                  'following-sibling::div//div[contains(@id,"trigger-picker")]'
        )
        self.xpath_open_reservation_policy_dropdownlist = \
            '//span[text()="Reservation policy:"]/parent::label/following-sibling::div' \
            '//div[contains(@id,"trigger-picker")]'

        self.lnk_reservation_policy_dropdownlist = WebLink(
            xpath='//div[starts-with(@class,"x-boundlist")]/div/ul'
        )
        self.lnk_storage_tab = WebLink(
            xpath='//span[text()="Storage"]'
        )
        self.lnk_storage_first_row = WebLink(
            xpath='//div[starts-with(@id, "diskGrid") and contains(@id, "body")]/div/div/table/tbody/tr'
        )
        self.btn_storage_edit = WebButton(xpath='//span[text()="Edit"]')
        self.btn_storage_reservation_policy_dropdownlist_open = WebButton(
            xpath='//div[starts-with(@id, "roweditor") and contains(@id, "-body")]/div/div/div[5]/div/div/div[2]'
        )
        self.lnk_storage_reservation_policy_dropdownlist = WebLink(
            xpath='/html/body/div[4]/div[1]/ul'
        )
        self.btn_ok_in_floading_window = WebButton(xpath='//span[text()="OK"]')

        # nsx settings Reservation policy:
        self.lnk_nsx_settings = WebLink(
            xpath='//*[starts-with(@id, "tabbar-") and contains(@id,"innerCt")]/div/a[2]'
        )
        self.txt_nsx_reservation_policy = WebTextBox(
            xpath='//*[starts-with(@id, "dropdownlist") and @name="edgeReservationPolicy"]'
        )
        self.btn_nsx_open_reservation_policy_dropdownlist = WebButton(
            xpath='//*[@id="dropdownlist-1069-inputEl"]')
        self.lnk_nsx_reservation_policy_dropdownlist = WebLink(
            xpath='//*[starts-with(@id, "boundlist-") and contains(@id, "-listEl")]'
        )
        self.btn_nsx_settings_ok = WebButton(xpath='//*[text()="OK"]')

    def finish_blueprint_edit(self, current_browser, blueprint_name):
        try:
            _browser = current_browser.instance._browser.current
            self.wait_for_loading_complete(2)
            _browser.switch_to.default_content()
            dialoghost_iframe_id = self.get_accurate_frameid(current_browser,
                                                             self.design_dialoghost_fullpage_extensionid,
                                                             False, 'extensionid')
            _browser.switch_to.frame(dialoghost_iframe_id)
            if self.btn_finish.exists():
                self.btn_finish.click()
                # Wait for the save to be effective.
                self.wait_for_loading_complete(3)
                logger.info('Submitted changes to blueprint: {}'.format(blueprint_name), False, True)
                _browser.switch_to.default_content()
                return True
            else:
                return False
        except:
            logger.error('Encounter exception in method finish_blueprint_edit, detail info: ' + sys.exc_info())
            return False

    def publish_blueprint_edit(self, current_browser):
        self.switch_to_blueprints_iframe(current_browser)
        if self.btn_blueprint_publish.exists():
            self.btn_blueprint_publish.click()
            return True
        else:
            return False

    def switch_to_blueprints_iframe(self, current_browser, from_top=True):
        _browser = current_browser.instance._browser.current
        try:
            if from_top:
                _browser.switch_to.default_content()
                design_iframe_id = self.get_accurate_frameid(
                    current_browser,
                    self.design_items_extensionid, False, 'extensionid')
                if design_iframe_id:
                    _browser.switch_to.frame(design_iframe_id)
                    logger.info(
                        'Switch_to_blueprints_frame firstly switch to design page'
                        ' design iframe', False, True)
            blueprint_iframe_id = self.get_accurate_frameid(
                current_browser,
                self.blueprints_extensionid, False, 'extensionid')
            if blueprint_iframe_id:
                _browser.switch_to.frame(blueprint_iframe_id)
                logger.info('Switched to design page blueprints iframe', False,
                            True)
            self.wait_for_loading_complete(2)

            return True
        except:
            ex = sys.exc_info()[:2]
            logger.warn('Switch to design page blueprints iframe failed, {}.'.format(ex))

        return False

    def navigate_to_design(self, current_browser):
        _browser = current_browser.instance._browser.current
        _browser.switch_to.default_content()
        if self.btn_design.exists():
            self.btn_design.click()
            BasePage().wait_for_loading_complete(3)
            logger.info('Clicked design tab button to navigate to design page.', False, True)
            design_iframe_id = self.get_accurate_frameid(current_browser,
                                                         self.design_items_extensionid, False, 'extensionid')
            if design_iframe_id:
                _browser.switch_to.frame(design_iframe_id)
                logger.info('Navigated to design page', False, True)
                return True
        else:
            logger.error('Design tab button is not found, failed to navigate to design page.')

            return False

    def navigate_to_sub_page(self, current_browser, btn_first_level, btn_dest=None, two_Level=False):
        _browser = current_browser.instance._browser.current
        try:
            to_blueprints_iframe = self.navigate_to_design(current_browser)
            if to_blueprints_iframe:
                if btn_first_level.exists():
                    btn_first_level.click()
                    logger.info('Design page navigating to sub page clicked'
                                ' first level button.', False, True)
                    self.wait_for_loading_complete(1)
                    if two_Level:
                        logger.info('Trying to select design page 2nd level button.', False, True)
                        if btn_dest.exists():
                            btn_dest.click()
                            self.wait_for_loading_complete(5)
                            logger.info(
                                'Design page navigating to sub page clicked'
                                ' destination page button.', False, True)

                            return True
                        else:
                            logger.error(
                                'Design page destination level button does not exist.')
                    else:
                        return True
                else:
                    logger.error(
                        'Design page first level button does not exist.')
            else:
                logger.error(
                    'iframe for elements of design with extensionid {} not found.'.
                    format(self.design_items_extensionid))
        except:
            ex = sys.exc_info()[:2]
            if two_Level and btn_dest:
                logger.error('Navigating to design page destination sub page '
                             '{0} failed with exception {1}'.format(
                                 btn_dest.current.text, ex))
            else:
                logger.error('Navigating to design sub page failed'
                             ' with exception {0}'.format(ex))

        logger.error('Navigating to design sub page failed.')
        return False

    def get_blueprint_item_link(self, current_browser, blueprint_name):
        try:
            _browser = current_browser.instance._browser.current
            blueprints_table_iframe_id = self.get_accurate_frameid(
                current_browser, self.blueprints_extensionid, False, 'extensionid')
            if not blueprints_table_iframe_id:
                return None
            _browser.switch_to.frame(blueprints_table_iframe_id)
            logger.info('Switched to blueprints table iframe.', False, True)
            # lnk_return = WebLink(xpath='//*[@title="{}"]'.format(blueprint_name))
            # if lnk_return.exists():
            #     return lnk_return
            lnk_blueprints_table = _browser.find_element_by_id('BLUEPRINTS_LIST-body')

            blueprints = lnk_blueprints_table.find_elements_by_tag_name('tr')
            i = 0
            for blueprint_row_item in blueprints:
                td_items = blueprint_row_item.find_elements_by_tag_name('td')
                if len(td_items) > 0:
                    if td_items[0].text.strip() == blueprint_name.strip():
                        logger.info('Blueprint {} found.'.format(blueprint_name), False, True)
                        # xpath elements base index is 1.
                        result_td = td_items[0]
                        if result_td:
                            # Only click action happens on span item will open the edit page.
                            lnk_return = result_td.find_element_by_tag_name('span')
                            return lnk_return
                        else:
                            return None
                else:
                    logger.info(
                        'Row {} within blueprints table is invalid.'.format(i))
        except:
            logger.error('Encounter exception in get_blueprint_item_link, detail info:' + sys.exc_info())

        return None

    def click_blueprint_item_to_edit(self, current_browser, lnk_blueprint):
        if not lnk_blueprint:
            logger.error('Openning blueprint edit page failed.')
            return False
        try:
            _browser = current_browser.instance._browser.current
            lnk_blueprint.click()
            logger.info('Clicked blueprint item to open it for editing.', False, True)
            LoadingWindow().wait_loading_infra_page(current_browser, timeout=30,
                                                    element_xpath='//td/img[@class="gwt-Image"]')
            _browser.switch_to.default_content()
            dialoghost_iframe_id = self.get_accurate_frameid(
                current_browser, self.design_dialoghost_fullpage_extensionid,
                False, 'extensionid')
            if not dialoghost_iframe_id:
                logger.error('The frame id is: {}, returned by get_accurate_frameid'.format(dialoghost_iframe_id))
                return False
            _browser.switch_to.frame(dialoghost_iframe_id)
            if self.lbl_blueprint_edit_header.exists():
                logger.info('Opened blueprint edit page.', False, True)
                return True
        except:
            logger.error('Encounter exception in click_blueprint_item_to_edit, detail info:' + sys.exc_info())
        return False

    def click_blueprint_properties_to_edit(self, current_browser, lnk_blueprint):
        if not lnk_blueprint:
            logger.error('The blueprint item link is None.')
            return False

        _browser = current_browser.instance._browser.current

        lnk_blueprint.click()
        self.wait_for_loading_complete(3)
        _browser.switch_to.default_content()
        dialoghost_iframe_id = self.get_accurate_frameid(current_browser,
                                                         self.design_dialoghost_fullpage_extensionid,
                                                         False, 'extensionid')
        _browser.switch_to.frame(dialoghost_iframe_id)
        if self.btn_open_blueprint_properties.exists():
            self.btn_open_blueprint_properties.click()
            logger.info('Clicked blueprint properties button.', False, True)
            self.wait_for_loading_complete(2)
            edit_iframe_id = self.get_accurate_frameid(
                current_browser, self.blueprints_createoredit_extensionid, False,
                'extensionid')
            _browser.switch_to.frame(edit_iframe_id)
            if self.lbl_blueprint_properties.exists():
                logger.info('Open blueprint properties edit page succeeded.', True, False)
                return True
        else:
            logger.error('blueprint open properties button does not exist.')
            return False

        return False

    def click_vsphere_machine_item_to_edit(self, current_browser, machine_name):
        try:
            _browser = current_browser.instance._browser.current

            # edit_iframe_id = self.get_accurate_frameid(current_browser,
            #     self.blueprints_createoredit_extensionid, False, 'extensionid')
            # _browser.switch_to.frame(edit_iframe_id)
            # link_vsphere_machine = WebLink(
            #     xpath=self.xpath_template_vsphere_machine_item.format(machine_name)
            # )
            # if link_vsphere_machine and link_vsphere_machine.exists():
            #     link_vsphere_machine.click()
            #     logger.info('Clicked vSpherer machine: {} to try to edit.'.format(machine_name), False, True)
            #     LoadingWindow().wait_loading_infra_page(current_browser, timeout=2)
            #     if self.lnk_vsphere_machine_edit_tab_general.exists():
            #         return True
            #
            # return False

            _value_of_expect_condition = (By.XPATH, self.xpath_blueprints_createoredit_extensionid)
            # use WedDriverWait and expect_condition to check frame available and switch to it
            if not BasePage().wait_until(_browser, _value_of_expect_condition):
                logger.error('Switch to blueprints.createoredit frame failed.')
                return False
            logger.info('Switching to blueprints.createoredit frame succeed.')

            _value_of_expect_condition = (By.XPATH, self.xpath_template_vsphere_machine)
            expect_condition = expected_conditions.presence_of_element_located
            if not BasePage().wait_until(_browser, _value_of_expect_condition, expect_condition):
                logger.error('Cannot find vSphere Machine in blueprint Design Canvas.')
                return False
            logger.info('After switch to blueprints.createoredit, find vSphere Machine textbox succeed.')

            self.lnk_template_vsphere_machine.click()
            logger.info('Clicked vSphere machine: {} to try to edit.'.format(machine_name), False, True)
            LoadingWindow().wait_loading_infra_page(current_browser)
            if self.lnk_vsphere_machine_edit_tab_general.exists():
                logger.info('Have find General tab.')
                return True
            else:
                logger.error('Cannot find General tab after clicked vSphere machine.')
                return False
        except:
            ex = sys.exc_info()
            logger.error('call method click_vsphere_machine_item_to_edit encounter error, detail info: {}'.format(ex))
            return False
