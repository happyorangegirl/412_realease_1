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

from selenium.webdriver.remote.webdriver import WebDriver
from robot.api import logger
from uiacore.modeling.webui.controls import (WebTextBox, WebButton, WebLabel)
from ehc_e2e.auc.uimap.shared.basepage import BasePage
from ehc_e2e.auc.uimap.shared.loadingwindow import LoadingWindow


class EditAvamarGridPage(BasePage):
    def __init__(self):
        super(EditAvamarGridPage, self).__init__()
        self.txt_description = WebTextBox(id='description')
        self.btn_next = WebButton(id='next')
        self.btn_save = WebButton(id="save")
        self.btn_operation_type = WebButton(xpath='//table[@id="provider-operationType"]/tbody/tr/td[1]')
        self.btn_edit_action = WebButton(xpath='//table[@id="provider-editOperation"]/tbody/tr/td[1]')
        self.avamar_grid_name_action = WebButton(xpath='//table[@id="provider-avamarGridName"]/tbody/tr/td[1]')
        self.lbl_active_value = WebLabel(xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')
        self.lbl_proxy_list = WebLabel(xpath='//*[@id="provider-addRegisteredProxies"]/div/table')
        self.txt_edit_provider_avamar_grid_name = WebTextBox(xpath='//input[@id="provider-editAvamarGridName"]')
        self.txt_edit_provider_avamar_grid_fqdn_name = WebTextBox(xpath='//input[@id="provider-editFqdn"]')
        self.txt_edit_provider_admin_user_name = WebTextBox(xpath='//input[@id="provider-editAdmin_user"]')
        self.txt_edit_provider_admin_password = WebTextBox(id='provider-editAdmin_password')
        self.txt_edit_provider_soap_user_name = WebTextBox(xpath='//input[@id="provider-editSoapUser"]')
        self.txt_edit_provider_soap_password = WebTextBox(id='provider-editSoapPassword')
        self.btn_edit_provider_site = WebButton(xpath='//table[@id="provider-editSite"]/tbody/tr/td[1]')
        self.btn_edit_provider_email = WebButton(xpath='//table[@id="provider-eMail"]/tbody/tr/td[1]')
        self.btn_edit_admin_full = WebButton(xpath='//table[@id="provider-admin_full"]/tbody/tr/td[1]')
        self.btn_avamar_grid_name_admin_full = WebButton(xpath='//table[@id="provider-setAvamarGrid"]/tbody/tr/td[1]')
        self.btn_submit = WebButton(id="submit")
        self.lbl_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(id="CONFIRMATION_OK_BUTTON")
        self.contains_text = ".//*[contains(text(), '{}')]"
        self.btn_cancel = WebButton(id="cancel")
        self.btn_data_protection_services = WebButton(xpath='//div[text()="Data Protection Services"]')
        self.btn_click = WebButton(xpath='//input[@id="provider-name" and @class="gwt-TextBox"]')
        self.lbl_submit_request = WebLabel(xpath='//div[text()="Review choices and click Submit"]')

    def tab(self):
        self.btn_tab = WebButton(id='next')
        self.btn_tab.current.parent.execute_script('arguments[0].focus();', self.btn_tab.current)

    def select_radio_button(self, current_browser, lbl_active_value):
        _browser = current_browser if isinstance(current_browser,
                                                 WebDriver) else current_browser.instance._browser.current
        index = 1 if lbl_active_value == 'True' else 0
        radio_buttons = _browser.find_elements_by_xpath('//input[@type="radio"]')
        if len(radio_buttons) > index:
            # Here the radio button is first activated by using execute_script line and clicking the
            # radio button using click method.
            _browser.execute_script("arguments[0].click();", radio_buttons[index])
            LoadingWindow().wait_loading(current_browser, 30)
            _browser.find_elements_by_xpath('//input[@type="radio"]')[index].click()
            LoadingWindow().wait_loading(current_browser, 30)
        else:
            logger.error('Radio Button with value {} does not exists'.format(lbl_active_value))

    def edit_avamar_grid_detail_for_onboard_ca_cluster(self, current_browser, item):

        if self.avamar_grid_name_action.exists():
            LoadingWindow().wait_loading(current_browser, 30)
            self.avamar_grid_name_action.click()
            if self.click_drop_down_list(self.lbl_active_value, 'div', item.avamar_grid_name) is False:
                logger.error('Select avamar grid name {} is not exist'.format(item.avamar_grid_name))
                LoadingWindow().wait_loading(current_browser, 60)
                return False
        else:
            logger.error("Avamar Grid Name DropDownList open button does not exist.")
            return False

        if self.txt_edit_provider_avamar_grid_name.exists():
            LoadingWindow().wait_loading(current_browser, 60)
            self.txt_edit_provider_avamar_grid_name.set(item.new_avamar_grid_name)
            self.tab()
            LoadingWindow().wait_loading(current_browser, 30)
        else:
            logger.error("Could not find the Enter new Avamar Grid Name input")
            return False

        if self.txt_edit_provider_avamar_grid_fqdn_name.exists():
            self.txt_edit_provider_avamar_grid_fqdn_name.set(item.edit_avamar_grid_fqdn_name)
            self.tab()
            LoadingWindow().wait_loading(current_browser, 30)
        else:
            logger.error("Could not find the Enter new Avamar Grid FQDN Name input ")
            return False

        if self.txt_edit_provider_admin_user_name.exists():
            self.txt_edit_provider_admin_user_name.set(item.edit_admin_user_name)
            self.tab()
            LoadingWindow().wait_loading(current_browser, 30)
        else:
            logger.error("Could not find theEnter new Admin User Name input  ")
            return False

        if self.txt_edit_provider_admin_password.exists():
            self.txt_edit_provider_admin_password.set(item.edit_admin_password)
            self.tab()
            LoadingWindow().wait_loading(current_browser, 60)
        else:
            logger.error("Could not find Enter new Admin Password input ")
            return False

        if self.btn_edit_provider_site.exists():
            LoadingWindow().wait_loading(current_browser, 60)
            self.btn_edit_provider_site.click()
            if self.click_drop_down_list(self.lbl_active_value, 'div', item.edit_site_name) is False:
                logger.error('Select Site is not exist')
                return False

        else:
            logger.error("Option element does not exist: Enter new Site ")
            return False

        LoadingWindow().wait_loading(current_browser, 60)
        if self.txt_edit_provider_soap_user_name.exists():
            self.txt_edit_provider_soap_user_name.set(item.edit_soap_user_name)
            self.tab()
            LoadingWindow().wait_loading(current_browser, 30)
        else:
            logger.error("Could not find Avamar SOAP UserName input ")
            return False

        if self.txt_edit_provider_soap_password.exists():
            self.txt_edit_provider_soap_password.set(item.edit_soap_password)
            LoadingWindow().wait_loading(current_browser, 30)
            self.btn_next.click()
            LoadingWindow().wait_loading(current_browser, 30)
            return True
        else:
            logger.error("Could not find Avamar SOAP Password input  ")
            return False

    def edit_avamar_grid_admin_full_for_onboard_ca_cluster(self, current_browser, item):
        if self.btn_avamar_grid_name_admin_full.exists():
            LoadingWindow().wait_loading(current_browser, 30)
            self.btn_avamar_grid_name_admin_full.click()
            if self.click_drop_down_list(self.lbl_active_value, 'div', item.avamar_grid_name) is False:
                logger.error('Select avamar grid name is not exist')
                LoadingWindow().wait_loading(current_browser, 60)
                return False
        else:
            logger.error("Option element does not exist: Avamar Grid Name ")
            return False

        if self.btn_edit_admin_full.exists():
            self.wait_for_loading_complete(2)
            if item.admin_full:
                self.select_radio_button(current_browser, 'True')
            else:
                self.select_radio_button(current_browser, 'False')
            self.wait_for_loading_complete(2)
            LoadingWindow().wait_loading(current_browser, 30)
            self.btn_next.click()
            LoadingWindow().wait_loading(current_browser, 30)
            return True
        else:
            logger.error("Could not find Admin Full input  ")
            return False
