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

# pylint: disable=too-many-instance-attributes

from uiacore.modeling.webui.controls import (WebButton, WebLabel, WebLink, WebTextBox)
from ehc_e2e.auc.uimap.extension import WebTextBoxEx
from ehc_e2e.auc.uimap.shared.basepage import BasePage

class AvamarProxyPage(BasePage):

    def __init__(self):
        super(AvamarProxyPage, self).__init__()

        self.btn_next = WebButton(xpath='//button[@id="next"]')
        self.btn_back = WebButton(xpath='//button[@id="previous"]')
        self.btn_submit = WebButton(xpath='//button[@id="submit"]')

        self.txt_description = WebTextBoxEx(xpath='//input[@id="description"]')
        self.txt_reasons = WebTextBoxEx(xpath='//textarea[@id="reasons"]')

        self.btn_actions_menu_open = WebButton(xpath='//table[@id="provider-operationType"]/tbody/tr/td[2]')

        self.btn_dns_updated_menu_open = WebButton(xpath='//table[@id="provider-dnsUpdated"]/tbody/tr/td[2]')
        self.btn_cluster_menu_open = WebButton(xpath='//table[@id="provider-clusterName"]/tbody/tr/td[2]')
        self.btn_datastore_menu_open = WebButton(xpath='//table[@id="provider-datastoreName"]/tbody/tr/td[2]')
        self.btn_network_menu_open = WebButton(xpath='//table[@id="provider-networkName"]/tbody/tr/td[2]')
        self.lnk_dropdownlist = WebLink(xpath='//*[@class="listBoxEx"]/div/table/tbody')
        self.txt_vm_name = WebTextBoxEx(xpath='//*[@id="provider-proxyVMName"]')
        self.txt_avamar_path = WebTextBoxEx(xpath='//*[@id="provider-proxyFQDNName"]')
        self.txt_ip = WebTextBoxEx(xpath='//*[@id="provider-proxyIP"]')
        self.txt_net_mask = WebTextBoxEx(xpath='//*[@id="provider-proxyNetMask"]')
        self.txt_gateway = WebTextBoxEx(xpath='//*[@id="provider-proxyGateway"]')
        self.txt_dns_svr_ip = WebTextBoxEx(xpath='//*[@id="provider-proxyDNS"]')
        self.txt_proxy_username = WebTextBoxEx(xpath='//*[@id="provider-proxyUserName"]')
        self.txt_proxy_password = WebTextBoxEx(xpath='//*[@id="provider-proxyPassword"]')

        self.btn_avamar_grid_name_menu_open = WebButton(xpath='//table[@id="provider-avamarGridName"]/tbody/tr/td[2]')
        self.txt_avamar_domain = WebTextBox(xpath='//input[@id="provider-avamarDomain"]')
        self.txt_ova_location = WebTextBox(xpath='//input[@id="provider-ovaLocation"]')

        self.txt_deployment_server = WebTextBox(xpath='//input[@id="provider-deploymentServer"]')
        self.txt_deployment_server_username = WebTextBox(xpath='//input[@id="provider-deploymentServerLogin"]')
        self.txt_deployment_server_password = WebTextBox(xpath='//input[@id="provider-deploymentServerPassword"]')
        self.btn_disable_verification_menu_open = WebButton(
            xpath='//table[@id="provider-disableVerification"]/tbody/tr/td[2]')

        self.lbl_review_and_submit_tab = WebLabel(xpath='//div[@id="tab-Review-and-Submit"]')
        self.lbl_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(xpath='//button[@id="CONFIRMATION_OK_BUTTON"]')
