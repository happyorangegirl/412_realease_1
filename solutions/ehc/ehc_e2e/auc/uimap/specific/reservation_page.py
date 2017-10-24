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
                                             WebLabel)
from ehc_e2e.auc.uimap.shared.basepage import BasePage


class ReservationPage(BasePage):
    """

    """
    formatter = '"Running on step {step}" - FAILED'

    def __init__(self):
        """
        Reservation web UI elements
        """
        # Reservation page
        super(ReservationPage, self).__init__()
        self.rservation_extensionid = "com.vmware.vcac.core.cafe.reservation.reservations"
        self.rservation_detaild_extensionid = "com.vmware.vcac.iaas.reservation.details"
        self.lbl_reservation_advanced_search_header_xpath = \
            '//*[starts-with(@id, "reservation-searchPanel-") and contains(@id, "-placeholder-innerCt")]'
        self.lbl_reservation_save_error = WebLabel(xpath='//table[@class="HLIIMNB-b-i"]')
        self.lbl_reservation_validation_error_details = \
            WebLabel(xpath='//table[@class="HLIIMNB-b-i"]')
        # Create new reservation
        self.btn_new_rsrvtn = WebButton(
            xpath='//span[text()="New"]')
        self.tbl_popup_rsrvtn_type = WebLabel(
            xpath='//div[starts-with(@id, "ext-comp-") and contains(@id, "targetEl")]')

        # Reservation information
        self.tbl_general_info = WebButton(xpath='//span[text()="General"]')
        self.lbl_bsns_grp = WebLabel(xpath='//*[@id="reservation-businessGroupComboBox-1025-labelEl"]')
        self.btn_cmptr_rsrce = WebButton(
            xpath='//div[starts-with(@id, "reservation-computeResourceComboBox") and contains(@id, "trigger-picker")]')
        self.lst_cmptr_rsrce = WebLabel(
            xpath='//ul[starts-with(@id, "reservation-computeResourceComboBox") and contains(@id, "picker-listEl")]'
        )

        self.txt_rsrvtn_name = WebTextBox(
            xpath='//*[@class="x-form-field x-form-required-field x-'
                  'form-text x-form-text-default  x-form-invalid-field x-form-invalid-field-default"]')
        self.btn_tenant = WebButton(
            xpath='//span[text()="Tenant:" and contains(@id, "combobox")]/../../following-sibling::div[1]'
                  '//div[contains(@id, "trigger-picker")]')
        self.lst_tenant = WebLabel(
            xpath='//ul[starts-with(@id, "combobox") and contains(@id, "picker-listEl")]')
        self.input_bsns_grp_xpath = \
            '//*[starts-with(@id, "reservation-businessGroupComboBox-") and contains(@id, "-inputEl")]'

        self.btn_bsns_grp = WebButton(
            xpath='//div[starts-with(@id, "reservation-businessGroupComboBox") and contains(@id, "trigger-picker")]')
        self.lst_bsns_grp = WebLabel(
            xpath='//ul[starts-with(@id, "reservation-businessGroupComboBox") and contains(@id, "picker-listEl")]')

        self.btn_rsrvtn_policy = WebButton(
            xpath='//*[starts-with(@id, "reservation-reservationPolicyComboBox") and '
                  'contains(@id, "-trigger-picker")]')
        self.lst_rsrvtn_policy = WebLabel(
            xpath='//*[starts-with(@id, "reservation-reservationPolicyComboBox") and contains(@id, "listEl")]')
        self.txt_reservation_policy = WebTextBox(
            xpath='//*[starts-with(@id, "reservation-reservationPolicyComboBox") and contains(@id, "inputEl")]')
        self.lbl_priority = WebLabel(
            xpath='//*[@id="reservation-reservationPolicyComboBox-1024-inputEl')

        self.dwnkey_priority = WebButton(
            xpath='//div[contains(@class, "x-form-spinner-down")]')
        self.txt_priority = WebTextBox(
            xpath='//input[starts-with(@id, "numberfield") and contains(@id, "inputEl")]')

        # Resources
        self.tbl_resources = WebButton(
            xpath='//span[text()="Resources"]')
        self.txt_computer_resources = WebTextBox(
            xpath='//*[starts-with(@id, "reservation-computeResourceComboBox-") and contains(@id, "-inputEl")]')
        self.computer_resources_input_xpath = \
            '//*[starts-with(@id, "reservation-computeResourceComboBox-") and contains(@id, "inputEl")]'
        self.dwnkey_memory = WebButton(
            xpath='//*[@name="RESERVATION_MEMORY_GRID_THIS_RESERVATION"]/../..//'
                  'div[contains(@class, "x-form-spinner-down")]'
        )
        self.txt_memory = WebTextBox(xpath='//*[@name="RESERVATION_MEMORY_GRID_THIS_RESERVATION"]')
        self.lbl_tbl_storage = \
            WebLabel(xpath='//div[starts-with(@id, "reservation-storageGrid") and contains(@id, "body")]/div[1]/div[2]')
        self.checkbox_storage_path = None
        self.checkbox_storage_path_xpath = './tbody/tr/td[2]/div/div'
        self.txt_storage_path_xpath = './tbody/tr/td[3]/div/span[2]'
        self.txt_physical_xpath = './tbody/tr/td[4]/div'
        self.btn_storage_edit_xpath = './tbody/tr/td[1]/div/div'
        self.txt_storage_disabled_xpath = './tbody/tr/td[10]/div'
        self.txt_storage_size_xpath = './tbody/tr/td[7]/div'
        self.txt_storage_priority_xpath = './tbody/tr/td[9]/div'
        # storage message box
        self.lbl_messagebox_toolbar = \
            WebLabel(xpath='//div[starts-with(@id, "messagebox") and contains(@id, "toolbar-innerCt")]')
        self.btn_messagebox_toolbar_confirm_xpath = './div/a[2]/span/span'
        # storage edit grid
        self.lbl_storage_edit_grid = WebLabel(xpath='//div[starts-with(@id, "roweditor") and contains(@id, "body")]')
        self.storage_edit_row_xpath = './div/div'
        self.txt_edit_storage_size_xpath = './div[7]/div/div/div[1]/input'
        self.txt_edit_storage_priority_xpath = './div[9]/div/div/div[1]/input'
        self.checkbox_edit_storage_disabled_xpath = './div[10]/div/div/input'
        self.cell_edit_storage_disabled_xpath = './div[10]'
        self.lbl_edit_storage_confirm = \
            WebLabel(xpath='//div[starts-with(@id, "roweditorbuttons") and contains(@id, "outerCt")]')
        self.btn_edit_confirm_storage_xpath = './div/a[1]/span/span'


        # Network
        self.tbl_network = WebButton(xpath='//span[text()="Network"]')
        self.tbl_network_paths_xpath =\
            '//*[starts-with(@id, "reservation-networkPathGrid") and contains(@id, "-body")]/div/div[2]'
        self.checkbox_network_path = None
        self.checkbox_network_path_xpath = './tbody/tr/td[1]/div/div'
        self.btn_network_profile = None
        self.btn_network_profile_xpath = './tbody/tr/td[3]/div/div/div/div/div[2]'
        self.lst_network_profile = None
        self.btn_ok = WebButton(xpath='//span[text()="OK"]')
        self.btn_cancel = WebButton(xpath='//div[starts-with(@id, "formFooter")]//span[text()="Cancel"]')
        self.lbl_cant_save_rsrvtn = WebLabel(
            xpath="//*[contains(text(), 'The reservation name') and contains(text(), 'exists')]"
        )
        self.lbl_validation_error = WebLabel(
            xpath="//*[contains(text(), 'Validation error')]"
        )

        # Delete Reservation
        self.btn_delete_res = WebButton(xpath='//span[text()="Delete"]')
        self.btn_delete_res_OK = WebButton(xpath='//span[text()="Yes"]')
        self.lbl_res_table = \
            WebButton(xpath='//*[starts-with(@id, "reservation-listGrid-") and contains(@id, "-body")]//table[1]')

        # unselect