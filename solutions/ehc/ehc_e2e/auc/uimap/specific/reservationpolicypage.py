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

from uiacore.modeling.webui.controls import WebTextBox, WebButton, WebLabel
from ehc_e2e.auc.uimap.shared.basepage import BasePage


class ReservationPolicyPage(BasePage):
    def __init__(self):
        super(ReservationPolicyPage, self).__init__()
        self.rsv_policy_frame_id = 'csp.places.iaas.iframe'
        self.lbl_rsv_policy_frame = WebLabel(id="csp.places.iaas.iframe")
        self.btn_new_rsv_policy = \
            WebButton(
                xpath='//span[starts-with(@class, "x-btn-icon-el") and contains(@class, "add-grid-icon")]/../span[2]'
            )
        self.btn_new_rsv_policy_xpath = '//*[@id="button-1035-btnInnerEl"]'
        self.lbl_name_header = WebLabel(xpath='//span[text()="Name"]')
        self.lbl_rsv_policy_name_column = WebLabel(xpath='//span[text()="Description"]')
        self.txt_create_rsv_policy_name = \
            WebTextBox(xpath='//input[starts-with(@id, "textfield") and @name="name"]')
        self.txt_create_rsv_policy_description = \
            WebTextBox(xpath='//input[starts-with(@id, "textfield") and @name="description"]')
        self.btn_img_save = \
            WebButton(
                xpath=
                '//a[starts-with(@class, "x-btn x-row-editor-") and contains(@class, "update-button")]/span[1]/span[1]'
            )
        self.body_rsv_policy_table = WebLabel(
            xpath='//*[starts-with(@id,"reservation-reservationPolicyListGrid") and contains(@id,"-body")]')
        self.body_rsv_policy_table_xpath = \
            '//*[starts-with(@id,"reservation-reservationPolicyListGrid") and contains(@id,"-body")]'
        self.row_rsv_policy_table_class = '  x-grid-row'
        self.column_rsv_name_xpath = './td[1]'
        self.column_type_xpath = './td[2]'
        self.btn_next = WebButton(
            xpath='//*[starts-with(@id,"vcacPagingToolbar") and @class="x-box-inner"]/div/div[last()]/../a[3]')
        self.label_page_number = WebLabel(
            xpath='//*[starts-with(@id,"vcacPagingToolbar") and @class="x-box-inner"]/div/div[last()]')

        self.btn_yes = WebButton(xpath='//*[@id="button-1006-btnInnerEl"]')
        self.btn_confirm_cancel = WebButton(xpath='//*[@id="button-1007-btnEl"]')
        self.btn_delete_enabled = \
            WebButton(
                xpath='//span[starts-with(@class, "x-btn-icon-el") and contains(@class, "delete-grid-icon")]/../span[2]'
            )

        # delete reservation policy result webelement
        self.lbl_can_not_delete_xpath = '//*[text()="Cannot delete reservation policy:"]'
        self.btn_close_cannot_delete = WebButton(
            xpath='//*[text()="Cannot delete reservation policy:"]/../../../../../../td[last()]/img')
        self.lbl_failed_delete_detail = WebLabel(
            xpath='//*[text()="Cannot delete reservation policy:"]/../../../tr[2]/td/div')
        self.xpath_failed_delete_detail_hidden = \
            '//table[@aria-hidden="true"]//*[text()="Cannot delete reservation policy:"]/../../../tr[2]/td/div'
        # create reseravtion policy result weblemement
        self.lbl_can_not_save_xpath = '//*[text()="Cannot save reservation policy:"]'
        self.btn_close_cannot_create = WebButton(
            xpath='//*[text()="Cannot save reservation policy:"]/../../../../../../td[last()]/img')
        self.lbl_failed_detail = WebLabel(xpath='//*[text()="Cannot save reservation policy:"]/../../../tr[2]/td/div')
        self.xpath_failed_detail_hidden = \
            '//table[@aria-hidden="true"]//*[text()="Cannot save reservation policy:"]/../../../tr[2]/td/div'
