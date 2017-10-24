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

from uiacore.modeling.webui.controls import (WebTextBox, WebButton, WebLabel)
from ehc_e2e.auc.uimap.shared.basepage import BasePage


class AddVcenterRelationshipPage(BasePage):
    def __init__(self):
        super(AddVcenterRelationshipPage, self).__init__()
        self.txt_description = WebTextBox(id='description')
        self.txt_reasons = WebTextBox(id='reasons')
        self.btn_next = WebButton(id='next')
        self.select_parent_element = WebLabel(xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')
        self.lab_select_operation = WebLabel(xpath='//div[@title="Action:"]')
        self.btn_select_the_operation = WebButton(xpath='//table[@id="provider-mainAction"]/tbody/tr/td[1]')
        self.protected_vcenter_title = WebLabel(xpath='//div[@title="Protected vCenter:"]')
        self.protected_vcenter = WebButton(xpath='//table[@id="provider-ProtectedVCenterDTName"]/tbody/tr/td[1]')
        self.txt_protected_vcenter_username = WebTextBox(id='provider-ProtectedVCenterUsername')
        self.txt_protected_vcenter_password = WebTextBox(id='provider-ProtectedVCenterPassword')
        self.recovery_vcenter = WebButton(xpath='//table[@id="provider-RecoveryVCenterDTName"]/tbody/tr/td[1]')
        self.txt_recovery_vcenter_username = WebTextBox(id='provider-RecoveryVCenterUsername')
        self.txt_recovery_vcenter_password = WebTextBox(id='provider-RecoveryVCenterPassword')

        self.lab_nsx_available_for_this_setup = WebLabel(xpath='//div[@title="NSX Available for this setup?:"]')
        self.nsx_available_for_this_setup = WebButton(xpath='//table[@id="provider-NSXAvailable"]/tbody/tr/td[1]')
        self.lab_protected_site_nsx_endpoint_name = WebLabel(xpath='//div[@title="Protected site NSX endpoint Name:"]')
        # site nsx configure
        self.txt_enter_protected_site_nsx_manager_fqdn = WebTextBox(id='provider-protectedNSXHostURL')
        self.txt_protected_site_nsx_manager_username = WebTextBox(id='provider-protectedNSXuserName')
        self.txt_protected_site_nsx_manager_password = WebTextBox(id='provider-protectedNSXPassword')

        self.txt_enter_recovery_site_nsx_manager_fqdn = WebTextBox(id='provider-NSXRecoverySiteHostURL')
        self.txt_recovery_site_nsx_manager_username = WebTextBox(id='provider-recoveryNSXUserName')
        self.txt_recovery_site_nsx_manager_password = WebTextBox(id='provider-recoveryNSXPassword')
        # srm plugin information
        # self.select_protected_srm_site = WebButton(xpath='//table[@id="provider-SRMProtectedSite"]/tbody/tr/td[1]')
        self.select_protected_srm_site = WebButton(
            xpath='//table[starts-with(@id, "provider-SRMProtectedSite")]/tbody/tr/td[1]')

        # self.txt_protected_srm_username_with_privileges_to_srm = WebTextBox(id='provider-SRMProtectedSiteUsername')
        self.txt_protected_srm_username_with_privileges_to_srm = WebTextBox(
            xpath='//*[starts-with(@id, "provider-SRMProtectedSiteUsername")]')

        # self.txt_protected_srm_password = WebTextBox(id='provider-SRMProtectedSitePassword')
        self.txt_protected_srm_password = WebTextBox(
            xpath='//*[starts-with(@id, "provider-SRMProtectedSitePassword")]')

        # self.select_recovery_srm_site = WebButton(xpath='//table[@id="provider-SRMRecoverySite"]/tbody/tr/td[1]')
        self.select_recovery_srm_site = WebButton(
            xpath='//table[starts-with(@id, "provider-SRMRecoverySite")]/tbody/tr/td[1]')

        # self.txt_recovery_srm_username_with_privileges_to_srm = WebTextBox(id='provider-SRMRecoverySiteUsername')
        self.txt_recovery_srm_username_with_privileges_to_srm = WebTextBox(
            xpath='//*[starts-with(@id, "provider-SRMRecoverySiteUsername")]')

        # self.txt_srm_recovery_password = WebTextBox(id='provider-SRMRecoverySitePassword')
        self.txt_srm_recovery_password = WebTextBox(
            xpath='//*[starts-with(@id, "provider-SRMRecoverySitePassword")]')

        # srm sql site information
        self.lab_protected_srm_sql_host_name = WebLabel(xpath='//div[@title="Protected SRM SQL host Name :"]')
        # self.txt_srm_protected_site_sql_database_host = WebTextBox(id='provider-ProtectedSiteSQLHost')
        self.txt_srm_protected_site_sql_database_host = WebTextBox(
            xpath='//*[starts-with(@id, "provider-ProtectedSiteSQLHost")]')
        # self.txt_protected_site_sql_database_port = WebTextBox(id='provider-ProtectedSiteSQLPort')
        self.txt_protected_site_sql_database_port = WebTextBox(
            xpath='//*[starts-with(@id, "provider-ProtectedSiteSQLPort")]')
        self.protected_select_authentication_type = WebButton(
            xpath='//table[starts-with(@id, "provider-ProtectedSiteDBAuthType")]/tbody/tr/td[1]')
        # self.txt_protected_site_sql_username = WebTextBox(id='provider-ProtectedSiteSQLUsername')
        self.txt_protected_site_sql_username = WebTextBox(
            xpath='//*[starts-with(@id, "provider-ProtectedSiteSQLUsername")]')
        # self.txt_protected_site_sql_password = WebTextBox(id='provider-ProtectedSiteSQLPassword')
        self.txt_protected_site_sql_password = WebTextBox(
            xpath='//*[starts-with(@id, "provider-ProtectedSiteSQLPassword")]')
        # self.txt_protected_site_sql_user_domain = WebTextBox(id='provider-ProtectedSiteSQLUserDomain')
        self.txt_protected_site_sql_user_domain = WebTextBox(
            xpath='//*[starts-with(@id, "provider-ProtectedSiteSQLUserDomain")]')
        # self.txt_protected_site_sql_database_name = WebTextBox(id='provider-ProtectedSiteSQLDatabaseName')
        self.txt_protected_site_sql_database_name = WebTextBox(
            xpath='//*[starts-with(@id, "provider-ProtectedSiteSQLDatabaseName")]')
        # self.txt_srm_recovery_site_sql_database_host = WebTextBox(id='provider-RecoverySiteSQLHost')
        self.txt_srm_recovery_site_sql_database_host = WebTextBox(
            xpath='//*[starts-with(@id, "provider-RecoverySiteSQLHost")]')
        # self.txt_recovery_site_sql_database_port = WebTextBox(id='provider-RecoverySiteSQLPort')
        self.txt_recovery_site_sql_database_port = WebTextBox(
            xpath='//*[starts-with(@id, "provider-RecoverySiteSQLPort")]')
        # self.recovery_select_authentication_type = WebButton(
        #     xpath='//table[@id="provider-RecoverySiteDBAuthType"]/tbody/tr/td[1]')
        self.recovery_select_authentication_type = WebButton(
            xpath='//table[starts-with(@id, "provider-RecoverySiteDBAuthType")]/tbody/tr/td[1]')
        # self.txt_recovery_site_sql_username = WebTextBox(id='provider-RecoverySiteSQLUsername')
        self.txt_recovery_site_sql_username = WebTextBox(
            xpath='//*[starts-with(@id, "provider-RecoverySiteSQLUsername")]')

        # self.txt_recovery_site_sql_Password = WebTextBox(id='provider-RecoverySiteSQLPassword')
        self.txt_recovery_site_sql_Password = WebTextBox(
            xpath='//*[starts-with(@id, "provider-RecoverySiteSQLPassword")]')
        # self.txt_recovery_site_sql_user_domain = WebTextBox(id='provider-RecoverySiteSQLUserDomain')
        self.txt_recovery_site_sql_user_domain = WebTextBox(
            xpath='//*[starts-with(@id, "provider-RecoverySiteSQLUserDomain")]')
        # self.txt_recovery_site_sql_database_name = WebTextBox(id='provider-RecoverySiteSQLDatabaseName')
        self.txt_recovery_site_sql_database_name = WebTextBox(
            xpath='//*[starts-with(@id, "provider-RecoverySiteSQLDatabaseName")]')
        # srm soap information
        self.lab_protected_srm_soap_host_name = WebLabel(xpath='//div[@title="Protected SRM Soap host Name :"]')
        # self.txt_protected_srm_soap_host_fqdn = WebTextBox(id='provider-ProtectedSiteSOAPHostFQDN')
        self.txt_protected_srm_soap_host_fqdn = WebTextBox(
            xpath='//*[starts-with(@id, "provider-ProtectedSiteSOAPHostFQDN")]')
        # self.txt_protected_srm_soap_username = WebTextBox(id='provider-ProtectedSiteSOAPUsername')
        self.txt_protected_srm_soap_username = WebTextBox(
            xpath='//*[starts-with(@id, "provider-ProtectedSiteSOAPUsername")]')
        # self.txt_protected_srm_soap_password = WebTextBox(id='provider-ProtectedSiteSOAPPassword')
        self.txt_protected_srm_soap_password = WebTextBox(
            xpath='//*[starts-with(@id, "provider-ProtectedSiteSOAPPassword")]')
        # self.txt_recovery_srm_soap_host_fqdn = WebTextBox(id='provider-RecoverySiteSOAPHostFQDN')
        self.txt_recovery_srm_soap_host_fqdn = WebTextBox(
            xpath='//*[starts-with(@id, "provider-RecoverySiteSOAPHostFQDN")]')
        # self.txt_recovery_srm_soap_username = WebTextBox(id='provider-RecoverySiteSOAPUsername')
        self.txt_recovery_srm_soap_username = WebTextBox(
            xpath='//*[starts-with(@id, "provider-RecoverySiteSOAPUsername")]')
        # self.txt_recovery_srm_soap_password = WebTextBox(id='provider-RecoverySiteSOAPPassword')
        self.txt_recovery_srm_soap_password = WebTextBox(
            xpath='//*[starts-with(@id, "provider-RecoverySiteSOAPPassword")]')

        self.btn_submit = WebButton(id='submit')
        self.lab_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(id='CONFIRMATION_OK_BUTTON')
        self.ehc_configure = WebButton(xpath='//div[text()="EHC Configuration"]')
        self.btn_save = WebButton(id="save")
