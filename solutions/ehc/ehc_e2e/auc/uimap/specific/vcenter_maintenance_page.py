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

from uiacore.modeling.webui.controls import (WebTextBox, WebButton,
                                             WebLabel, WebLink)
from ehc_e2e.auc.uimap.shared.basepage import BasePage


class VCenterMaintenancePage(BasePage):
    def __init__(self):
        super(VCenterMaintenancePage, self).__init__()
        ##add vcenter
        self.txt_description = WebTextBox(id='description')
        self.txt_reasons = WebTextBox(id='reasons')
        self.btn_next = WebButton(id='next')
        self.lab_select_operation = WebLabel(xpath='//div[@title="Action:"]')

        self.select_action = WebButton(xpath='//table[@id="provider-vCenterAction"]/tbody/tr/td[1]')
        self.parent_element = WebLabel(xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')
        self.txt_name_for_vcenter = WebTextBox(id='provider-VCNameForEndpoint')
        self.name_for_vcenter_endpoint_label = WebLabel(xpath='//div[@title="vCenter Object:"]')
        self.select_vc_fqdn_to_add = WebButton(xpath='//table[@id="provider-SelectVCToAdd"]/tbody/tr/td[1]')
        self.new_vcenter_associated_sites = WebButton(
            xpath='//div[@id="provider-SiteToAdd"]/div/table')
        self.select_datacenter_to_add_label = WebButton(xpath='//div[@title="Datacenter:"]')
        self.select_datacenter = WebLink(
            xpath='//table[@id="provider-datacenterToAdd"]/tbody/tr/td[1]')
        self.btn_submit = WebButton(id='submit')
        self.lab_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(id='CONFIRMATION_OK_BUTTON')
        self.btn_cancel = WebButton(id='cancel')
        self.ehc_configure = WebButton(xpath='//div[text()="EHC Configuration"]')
        self.new_vcenter_associated_sites_xpath = '//label[contains(text(),"{}")]'
        self.btn_save = WebButton(id="save")
        # update_vcenter
        self.btn_existing_vcenter = WebButton(xpath='//*[@id="provider-vCenterToUpdate"]/tbody/tr/td[1]')
        self.txt_vcenter_name = WebTextBox(id='provider-vCenterNameToUpdate')
        self.btn_vcenter_fqdn = WebButton(xpath='//*[@id="provider-vCenterFQDNToUpdate"]/tbody/tr/td[1]')
        self.btn_datacenter = WebButton(xpath='//*[@id="provider-datacenterToUpdate"]/tbody/tr/td[1]')
        self.btn_sites = WebButton(xpath='//*[@id="provider-vcSiteToUpdate"]/div/table')
        self.txt_vcenter_username = WebTextBox(id='provider-vcUserNameToUpdate')
        self.txt_vcenter_password = WebTextBox(id='provider-vcPasswordToUpdate')
        #delete vcenter
        self.lbl_calalog = WebLabel(xpath="//div[@class='gwt-Label GJPN4V0DODD GJPN4V0DJ3C']")
        self.lbl_vcenter_title = WebLabel(xpath="//a[@title='vCenter Endpoint Maintenance']")
        self.lnk_vcenter_request = WebLink(id="CATALOG_ITEM_REQUEST_BUTTON")
        self.btn_provider_vcenter_action = WebLink(xpath="//table[@id='provider-vCenterAction']/tbody/tr/td[1]")
        self.lbl_select_actionlist_value = WebLabel(
            xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')

        self.lbl_delete_vcenter_tab = WebLabel(id='tab-Delete-vCenter')

        self.btn_vcenter_to_del = WebButton(xpath="//table[@id='provider-vCenterToDelete']/tbody/tr/td[1]")
        self.lbl_select_vcenterlist_value = WebLabel(
            xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')
        self.btn_confirm_to_del = WebButton(xpath="//table[@id='provider-confirmToDelete']/tbody/tr/td[2]")
        self.lbl_select_confirmlist_value = WebLabel(
            xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')
        self.lbl_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(id="CONFIRMATION_OK_BUTTON")
