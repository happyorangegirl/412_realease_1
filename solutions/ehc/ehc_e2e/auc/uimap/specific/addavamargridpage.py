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
from uiacore.modeling.webui.controls import (WebTextBox, WebButton, WebLabel)
from ehc_e2e.auc.uimap.shared.basepage import BasePage
from ehc_e2e.auc.uimap.shared.loadingwindow import LoadingWindow


class AddAvamarGridPage(BasePage):
    def __init__(self):
        super(AddAvamarGridPage, self).__init__()
        self.txt_description = WebTextBox(id='description')
        self.btn_next = WebButton(id='next')
        self.lbl_provideName_for_hwi = WebLabel(
            xpath='//div[@title="Please provide the name for the new Hardware Island:"]')
        self.btn_operation_type = WebButton(xpath='//table[@id="provider-operationType"]/tbody/tr/td[1]')
        self.lbl_active_value = WebLabel(xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')
        self.lbl_proxy_list = WebLabel(xpath='//*[@id="provider-addRegisteredProxies"]/div/table')
        self.txt_provider_avamar_grid_name = WebTextBox(xpath='//input[@id="provider-name" and @class="gwt-TextBox"]')
        self.txt_provider_avamar_grid_fqdn_name = WebTextBox(
            xpath='//input[@id="provider-fqdn" and @class="gwt-TextBox"]')
        self.txt_provider_admin_user_name = WebTextBox(
            xpath='//input[@id="provider-admin_user" and @class="gwt-TextBox"]')
        self.txt_provider_admin_password = WebTextBox(xpath='//input[@id="provider-admin_password"]')
        self.txt_provider_soap_user_name = WebTextBox(
            xpath='//input[@id="provider-soapUserName" and @class="gwt-TextBox"]')
        self.txt_provider_soap_password = WebTextBox(xpath='//input[@id="provider-soapPassword"]')
        self.btn_provider_site = WebButton(xpath='//table[@id="provider-site"]/tbody/tr/td[1]')
        self.btn_submit = WebButton(id="submit")
        self.lbl_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(id="CONFIRMATION_OK_BUTTON")
        self.contains_text = ".//*[contains(text(), '{}')]"
        self.btn_cancel = WebButton(id="cancel")
        self.btn_data_protection_services = WebButton(xpath='//div[text()="Data Protection Services"]')
        self.btn_click = WebButton(xpath='//input[@id="provider-name" and @class="gwt-TextBox"]')
        self.lbl_submit_request = WebLabel(xpath='//div[text()="Review choices and click Submit"]')
        self.btn_save = WebButton(id="save")
        self.registered_proxies_errortext = "Registered proxies are not found."
        self.grid_fqdn_errortext = "Unable to connect to grid FQDN specified. Please validate"
        self.lbl_active_checkbox = WebLabel(xpath='//div[@id ="provider-addRegisteredProxies"]/div/table')

    def tab(self):
        self.btn_tab = WebButton(id='next')
        self.btn_tab.current.parent.execute_script('arguments[0].focus();', self.btn_tab.current)

    def add_avamar_grid_for_onboard_dr_cluster(self, current_browser, item, unselect_proxy):
        LoadingWindow().wait_loading(current_browser, 30)
        if self.txt_provider_avamar_grid_name.exists():
            self.txt_provider_avamar_grid_name.set(item.avamar_grid_name)
            logger.info('Filled {} in avamar grid name textbox.'.format(item.avamar_grid_name))
            self.tab()
            LoadingWindow().wait_loading(current_browser, 30)
        else:
            logger.error("Could not find the Enter new Avamar Grid Name input")
            return False

        if self.txt_provider_avamar_grid_fqdn_name.exists():
            self.txt_provider_avamar_grid_fqdn_name.set(item.avamar_grid_fqdn_name)
            logger.info('Filled {} in avamar grid fqdn textbox.'.format(item.avamar_grid_fqdn_name))
            self.tab()
            LoadingWindow().wait_loading(current_browser, 30)
        else:

            logger.error("Could not find the Enter new Avamar Grid FQDN Name input ")
            return False

        if self.txt_provider_admin_user_name.exists():
            self.txt_provider_admin_user_name.set(item.admin_user_name)
            logger.info('Filled {} in admin username textbox.'.format(item.admin_user_name))
            self.tab()
            LoadingWindow().wait_loading(current_browser, 30)
        else:
            logger.error("Could not find theEnter new Admin User Name input  ")
            return False

        if self.txt_provider_admin_password.exists():
            self.txt_provider_admin_password.set(item.admin_password)
            logger.info('Filled {} in admin password textbox.'.format(item.admin_password))
            self.tab()
            LoadingWindow().wait_loading(current_browser, 60)
        else:
            logger.error("Could not find Enter new Admin Password input ")
            return False

        if self.lbl_active_checkbox.exists():
            LoadingWindow().wait_loading(current_browser, 60)
            all_tag_input_elements = self.lbl_active_checkbox.current.find_elements_by_tag_name('input')
            if unselect_proxy:
                for x in range(len(all_tag_input_elements)):
                    if all_tag_input_elements[x].is_selected():
                        all_tag_input_elements[x].click()
                        LoadingWindow().wait_loading(current_browser, 10)
                        all_tag_input_elements = self.lbl_active_checkbox.current.find_elements_by_tag_name('input')
            elif len(all_tag_input_elements) < 2:
                error_label_text = self.lbl_active_checkbox.current.find_elements_by_tag_name('label')[0].text
                if error_label_text == self.registered_proxies_errortext \
                        or error_label_text == self.grid_fqdn_errortext:
                    logger.error('Encounters error in loading Registered proxies list, error message: {}'.format(
                        error_label_text))
                    return False
        else:
            logger.error("Could not find Registered Proxy List Options ")
            return False

        if self.btn_provider_site.exists():
            LoadingWindow().wait_loading(current_browser, 60)
            self.btn_provider_site.click()
            if self.click_drop_down_list(self.lbl_active_value, 'div', item.site_name) is False:
                logger.error('Site: "{}" does not exist.'.format(item.site_name))
                return False
            else:
                logger.info('Filled {} in site name textbox.'.format(item.site_name))
        else:

            logger.error("Option element does not exist: Enter new Site ")
            return False

        LoadingWindow().wait_loading(current_browser, 30)
        if self.txt_provider_soap_user_name.exists():
            self.txt_provider_soap_user_name.set(item.soap_user_name)
            logger.info('Filled {} in soap username textbox.'.format(item.soap_user_name))
            self.btn_click.click()
        else:

            logger.error("Could not find Avamar SOAP UserName input ")
            return False

        LoadingWindow().wait_loading(current_browser, 30)
        if self.txt_provider_soap_password.exists():
            self.txt_provider_soap_password.set(item.soap_password)
            logger.info('Filled {} in soap password textbox.'.format(item.soap_password))
            LoadingWindow().wait_loading(current_browser, 30)
            self.btn_next.click()
            LoadingWindow().wait_loading(current_browser, 30)
            return True
        else:

            logger.error("Could not find Avamar SOAP Password input.")
            return False
