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

from robot.api import logger
from uiacore.modeling.webui.controls import (WebTextBox, WebButton, WebLabel, WebLink)
from ehc_e2e.auc.uimap.shared.basepage import BasePage
from ehc_e2e.auc.uimap.shared.loadingwindow import LoadingWindow
from ehc_e2e.auc.uimap.extension import WebTextBoxEx, WebComboEx


class DeployVMPage(BasePage):
    """
     Page for deploy vm request.
     TODO:  1. The page is using iframe to embed elements except "Save", "Submit"
            "Cancel". Will need to figure out the acurate way to locate those
            elements within iframe tags.
            2. storage tab and properties tab are still not fully covered,
            where we are using default for now.
    """
    def __init__(self):
        super(DeployVMPage, self).__init__()
        self.is_in_edit_areas = False

        self.xpath_template_vSphere_machine_treeview_item = \
            '//img[contains(@style, "https://com.vmware.csp.core.cafe.catalog.api.vproxy/icons/' \
            'Infrastructure.CatalogItem.Machine.Virtual.vSphere/download")]/parent::div/' \
            'span[text()="{}"]'.format

        # elements in Challenger
        # self.xpath_txt_desc = '//span[text()="Description:"]/parent::label/following-sibling::div/div/div/textarea'
        # self.txt_desc = WebTextBox(
        #     xpath='//span[text()="Description:"]/parent::label/following-sibling::div/div/div/textarea')
        #
        # self.txt_reason_for_request = WebTextBox(
        #     xpath='//span[text()="Reason for request:"]/parent::label/following-sibling::div/div/div/textarea')
        #
        # self.txt_instances = WebTextBox(
        #     xpath='//span[text()="Instances:"]/parent::label/following-sibling::div/div/div/input')
        #
        # self.txt_cpu = WebTextBoxEx(
        #     xpath='//span[text()="CPUs:"]/parent::label/following-sibling::div/div/div/input')
        # self.btn_cpu_up = WebButton(
        #     xpath='//span[text()="CPUs:"]/parent::label/following-sibling::div/div/div[2]/div[1]')
        # self.lbl_cpu_range = WebLabel(
        #     xpath='//span[text()="CPUs:"]/parent::label/parent::div/following-sibling::div/span[@class="range-field"]'
        # )
        #
        # self.txt_ram = WebTextBoxEx(
        #     xpath='//span[text()="Memory (MB):"]/parent::label/following-sibling::div/div/div/input')
        # self.btn_ram_up = WebButton(
        #     xpath='//span[text()="Memory (MB):"]/parent::label/following-sibling::div/div/div[2]/div[1]')
        # self.lbl_ram_range = WebLabel(
        #     xpath='//span[text()="Memory (MB):"]/parent::label/parent::div/following-sibling::div/'
        #           'span[@class="range-field"]')

        #
        # self.btn_instances_down = WebButton(
        #     xpath='//span[text()="Instances:"]/parent::label/following-sibling::div/div/div[2]/div[2]')
        #
        # self.btn_srm_drop_down = WebButton(
        #     xpath='//span[text()="SRM-Power-On-Priority:"]/parent::label/following-sibling::div/div/div[2]')
        #
        # self.lnk_srm_drop_down_list = WebLink(
        #     xpath='(//ul[starts-with(@id, "boundlist-") and contains(@id, "-listEl")])[last()]')
        #
        # self.btn_bkp_drop_down = WebButton(
        #     xpath='//span[text()="Set Backup Service Level:"]/parent::label/following-sibling::div/div/div[2]')
        #
        # self.btn_bkp_input = WebTextBox(
        #     xpath='//span[text()="Set Backup Service Level:"]/parent::label/following-sibling::div/div/div[1]/input')


        # Benson: xpath change in dozer!!
        self.xpath_txt_desc = \
            '//span[text()="Description:"]/parent::span/parent::label/following-sibling::div/div/div/textarea'
        self.txt_desc = WebTextBox(
            xpath='//span[text()="Description:"]/parent::span/parent::label/following-sibling::div/div/div/textarea')
        self.txt_reason_for_request = WebTextBox(
            xpath='//span[text()="Reason for request:"]/parent::span/parent::label/following-sibling::div/div/div/'
                  'textarea')
        self.txt_cpu = WebTextBoxEx(
            xpath='//span[text()="CPUs:"]/parent::span/parent::label/following-sibling::div/div/div/input')
        self.btn_cpu_up = WebButton(
            xpath='//span[text()="CPUs:"]/parent::span/parent::label/following-sibling::div/div/div[2]/div[1]')
        self.txt_ram = WebTextBoxEx(
            xpath='//span[text()="Memory (MB):"]/parent::span/parent::label/following-sibling::div/div/div/input')
        self.btn_ram_up = WebButton(
            xpath='//span[text()="Memory (MB):"]/parent::span/parent::label/following-sibling::div/div/div[2]/div[1]')
        self.lbl_ram_range = WebLabel(
            xpath='//span[text()="Memory (MB):"]/parent::span/parent::label/parent::div/parent::div/div[2]/'
                  'span[@class="range-field"]')
        self.lbl_cpu_range = WebLabel(
            xpath='//span[text()="CPUs:"]/parent::span/parent::label/parent::div/parent::div/div[2]/'
                  'span[@class="range-field"]')

        self.txt_instances = WebTextBox(
            xpath='//span[text()="Instances:"]/parent::span/parent::label/following-sibling::div/div/div/input')

        self.btn_instances_down = WebButton(
            xpath='//span[text()="Instances:"]/parent::span/parent::label/following-sibling::div/div/div[2]/div[2]')

        self.btn_srm_drop_down = WebButton(
            xpath='//span[text()="SRM-Power-On-Priority:"]/parent::span/parent::label/following-sibling::div/div/div[2]')

        self.lnk_srm_drop_down_list = WebLink(
            xpath='(//ul[starts-with(@id, "dropdownlist-") and contains(@id, "-picker-listEl")])[last()]')

        self.btn_bkp_drop_down = WebButton(
            xpath='//span[text()="Set Backup Service Level:"]/parent::span/parent::label/following-sibling::div/div/'
                  'div[2]')

        self.btn_bkp_input = WebTextBox(
            xpath='//span[text()="Set Backup Service Level:"]/parent::span/parent::label/following-sibling::div/div/'
                  'div[1]/input')

        # elements for rp4vm
        self.btn_ehc_rp4vm_policy_drop_down = WebButton(
            xpath='//Label[@data-qtip="EHC RP4VM Policy"]/following-sibling::div[1]/div[1]/div[2]')
        self.txt_ehc_rp4vm_cg = WebTextBox(
            xpath='//Label[@data-qtip="EHC RP4VM CG"]/following-sibling::div[1]/div[1]/div[1]/input'
        )
        self.cbo_ehc_rp4vm_policy = WebComboEx(xpath='//Label[@data-qtip="EHC RP4VM Policy"]/following-sibling::div')
        self.btn_ehc_rp4vm_boot_priority_up = WebButton(
            xpath='//span[text()="EHC RP4VM Boot Priority:"]/parent::label/following-sibling::div/div/div[1]'
        )
        self.txt_ehc_rp4vm_boot_priority = WebTextBox(
            xpath='//Label[@data-qtip="EHC RP4VM Boot Priority"]/following-sibling::div[1]/div[1]/div[1]/input')
        self.lbl_drop_down_list = WebLabel(xpath='(//div/div/ul)[last()]')
        self.lbl_error_request_form = WebTextBox(xpath='//span[@class="request-tree-status-panel-icon"]')

        self.gadget_2_frame_id = '__gadget_2'
        self.url_forms_gadget = 'com.vmware.vcac.core.design.blueprints.requestForm'
        self.xpath_forms_gadget = '//iframe[@extensionid="com.vmware.vcac.core.design.blueprints.requestForm"]'
        self.extensionid_self_service = 'csp.catalog.selfservice'
        self.url_self_service_gadget = \
            'https://com.vmware.csp.core.cafe.catalog.plugin.vproxy//selfservice/SelfServiceGadget.gadget.xml'

        # storage reservation policy edit.
        self.lnk_storage_tab = WebLink(xpath='//span[starts-with(@id, "tab") and text()="Storage"]')
        self.lnk_storage_first_row = WebLink(
            xpath='//div[starts-with(@id, "diskGrid") and contains(@id, "body")]/div/div/table/tbody/tr')
        self.btn_storage_edit = WebButton(xpath='//span[text()="Edit"]')
        self.btn_storage_reservation_policy_dropdownlist_open = WebButton(
            xpath='//div[starts-with(@id, "roweditor") and contains(@id, "-body")]/div/div/div[5]/div/div/div[2]')

        # Pay attention there are multiple dropdownlist element having identical properties within same html page,
        # We need to make sure choose the last one.
        self.lnk_storage_reservation_policy_dropdownlist = \
            WebLink(xpath='(//div[starts-with(@id, "dropdownlist") and contains(@id, "listWrap")]/ul)[last()]')
        self.btn_ok_in_floating_window = WebButton(xpath='//span[starts-with(@id, "button") and text()="OK"]')


        self.btn_save = WebButton(xpath='//*[@id="save"]')
        self.btn_submit = WebButton(xpath='//*[@id="submit"]')
        self.btn_cancel = WebButton(xpath='//*[@id="cancel"]')

    def switch_to_save_button_frame(self, current_browser):
        _browser = current_browser.instance._browser.current
        _browser.switch_to.default_content()
        first_level_id = BasePage().get_accurate_frameid(current_browser,
                                                         self.url_self_service_gadget)
        second_level_id = BasePage().get_accurate_frameid(current_browser,
                                                          self.url_forms_gadget)

        try:
            if first_level_id is None or second_level_id is None:
                identical_id = first_level_id if first_level_id else second_level_id
                logger.info('There are iframes with identical id: {}'.format(
                    identical_id), False, True)
                _browser.switch_to.frame(identical_id)
            else:
                _browser.switch_to.frame(first_level_id)
        except:
            pass

    def switch_to_edit_areas(self, current_browser):
        _browser = current_browser.instance._browser.current
        LoadingWindow().wait_loading(current_browser, 30)
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions
        if not self.is_in_edit_areas:
            try:
                _value_of_expect_condition = (By.XPATH, self.xpath_forms_gadget)
                # use WedDriverWait and expect_condition to check frame available and switch to it
                if not BasePage().wait_until(_browser, _value_of_expect_condition):
                    logger.error('Switch to requestForm frame failed.')
                    return False
                logger.info('Switch to requestForm frame succeed.')
                # forms_gadget_frame_id = BasePage().get_accurate_frameid(
                #     current_browser, self.url_forms_gadget, False, 'extensionid')
                # if forms_gadget_frame_id:
                #     _browser.switch_to.frame(forms_gadget_frame_id)
                #     logger.debug('Deploy vm page switched to requestform iframe, iframe id: {}.'
                #                 ''.format(forms_gadget_frame_id))
                # else:
                #     logger.error('Failed to find requestform iframe in deploy vm.')
                #     return False

                # Wenda: txt_machines is gone in Badger. so change it to description
                # if self.txt_desc.exists():
                #     self.is_in_edit_areas = True
                #     return True

                _value_of_expect_condition = (By.XPATH, self.xpath_txt_desc)
                expect_condition = expected_conditions.presence_of_element_located
                if not BasePage().wait_until(_browser, _value_of_expect_condition, expect_condition):
                    logger.error('Cannot find description textbox.')
                    return False
                logger.info('After switch to requestForm, find description textbox succeed.')
                return True
            except:
                import sys
                ex = sys.exc_info()
                logger.error('Switch to edit area frame failed, Error '
                             'caught: {}'.format(ex))
                return False
        return False

    def switch_to_default_frame(self, browser):
        if self.is_in_edit_areas:
            try:
                # Directly call to webdriver switch_to.default_content()
                # method to switch to default frame.
                browser.switch_to.default_content()
                browser.switch_to.frame(
                    self.gadget_2_frame_id)
                logger.debug(
                    'Switch back to frame {}'.format(self.gadget_2_frame_id))
                self.is_in_edit_areas = False
                return True
            except:
                import sys
                ex = sys.exc_info()
                logger.error('Switch back to default frame failed, Error '
                             'caught: {}'.format(ex))
                return False
        else:
            logger.info(
                'Switch to default frame not run, already in default frame')
            return False

    def open_vsphere_blueprint(self, vsphere_bluepritn_id):

        btn_vsphere_blueprint = WebButton(
            xpath=self.xpath_template_vSphere_machine_treeview_item(vsphere_bluepritn_id))
        if btn_vsphere_blueprint.exists():
            btn_vsphere_blueprint.click()
            logger.info('Clicked vsphere machine:{} to edit it.'.format(vsphere_bluepritn_id), False, True)
            return True
        return False

    def switch_to_service_gadget_frame(self, current_browser):
        _browser = current_browser.instance._browser.current
        _browser.switch_to.default_content()
        service_gadget_frame_id = BasePage().get_accurate_frameid(
            current_browser, self.extensionid_self_service, True, attribute_name='extensionid')
        try:
            if service_gadget_frame_id:
                _browser.switch_to.frame(service_gadget_frame_id)
                logger.info(
                    'Deploy VM switched to service_gadget frame {}'.format(service_gadget_frame_id),
                    False, True)
                return True
            else:
                logger.error('Deploy VM  looking for service_gadget iframe failed.')
        except:
            logger.error('Deploy VM switching to service_gadget iframe failed.')
            return False

        return False
