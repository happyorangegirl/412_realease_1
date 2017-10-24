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

from ehc_e2e.auc.uimap.shared import BasePage
from ehc_e2e.auc.uimap.extension.webtextbox_ex import WebTextBoxEx
from uiacore.modeling.webui.controls import (WebTextBox, WebButton,
                                             WebLabel)


class BackupServiceLevelPage(BasePage):
    def __init__(self):
        super(BackupServiceLevelPage, self).__init__()
        # add backup service level page
        self.backup_to_operate_vm = ''
        self.backup_to_set_backup_service = ''
        self.result = None
        self.data_protection_services = WebButton(xpath='//div[text()="Data Protection Services"]')
        self.txt_description = WebTextBox(id='description')
        self.txt_reasons = WebTextBox(id='reasons')
        self.btn_next = WebButton(id='next')
        self.lab_select_action_for_backup = WebLabel(
            xpath='//div[@title="Action:"]')
        # self.btn_add_backup_service_level = WebButton(xpath='//table[@id="provider-SvcLvlAction"]/tbody/tr/td[1]')
        self.btn_add_backup_service_level = WebButton(xpath='//*[@id="provider-currentAction"]/tbody/tr/td[2]')
        self.parent_element = WebLabel(xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')
        self.txt_backup_service_name = WebTextBox(id='provider-ServiceLevelName')
        self.btn_choose_avamar_or_datadomain = WebButton(xpath='//table[@id="provider-BackupTarget"]/tbody/tr/td[1]')
        # self.btn_select_a_schedule = WebButton(xpath='//table[@id="provider-BackupSchedule"]/tbody/tr/td[1]')
        self.btn_select_a_schedule = WebButton(xpath='//*[@id="provider-BackupSchedule"]/tbody/tr/td[@align="right"]')
        self.btn_weekday = WebButton(xpath='//table[@id="provider-WeekDay"]/tbody/tr/td[1]')
        self.txt_start_time = WebTextBoxEx(xpath='//*[@id="provider-DailyScheduleTime"]')
        self.btn_week_number = WebButton(xpath='//*[@id="provider-WeekNumber"]/tbody/tr/td[1]/div')

        self.btn_regular_retention_policy = WebButton(xpath='//table[@id="provider-RetentionTime"]/tbody/tr/td[1]')
        self.txt_retention_for_number = WebTextBoxEx(id='provider-RetentionForNumber')
        self.txt_retention_date = WebTextBoxEx(xpath='//*[@id="provider-RetainUntil_DATE_BOX-input"]')
        self.txt_retention_time = WebTextBoxEx(xpath='//*[@id="provider-RetainUntil_TIME_BOX-input"]')
        self.btn_retention_custom_phrase = WebButton(
            xpath='//table[@id="provider-RetentionCustomPhrase"]/tbody/tr/td[1]')
        self.txt_long_term_retention_policy = WebTextBoxEx(id='provider-DefinedLongTermRetentionPolicies')
        self.btn_select_replication_schedule = WebButton(
            xpath='//table[@id="provider-ReplicationSchedule"]/tbody/tr/td[1]')
        self.txt_replication_start_time = WebTextBoxEx(xpath='//*[@id="provider-ReplicationDailyScheduleTime"]')
        self.btn_replication_week_day = WebButton(xpath='//table[@id="provider-ReplicationWeekDay"]/tbody/tr/td[1]')
        self.btn_replication_week_number = WebButton(xpath='//*[@id="provider-ReplicationWeekNumber"]/tbody/tr/td[1]/div')
        self.btn_submit = WebButton(id='submit')
        self.lab_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')

        # delete backup service page
        self.data_protection_services = WebButton(xpath='//div[text()="Data Protection Services"]')
        self.btn_delete_backup_service_level = WebButton(xpath='//*[@id="provider-currentAction"]/tbody/tr/td[1]')
        self.parent_element = WebLabel(xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')
        self.btn_select_backup_service_level_to_delete = WebButton(
            xpath='//table[@id="provider-SvcLevelToDelete"]/tbody/tr/td[1]')
        self.btn_choose_avamar_or_datadomain = WebButton(xpath='//table[@id="provider-BackupTarget"]/tbody/tr/td[1]')
        self.btn_confirm_deletion_of_backup_service_level = WebButton(
            xpath='//table[@id="provider-ConfirmDelete"]/tbody/tr/td[1]')
        self.lab_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(id='CONFIRMATION_OK_BUTTON')
        self.btn_cancel = WebButton(id='cancel')
        self.btn_save = WebButton(id="save")

        # display backup service level page
        self.lbl_select_action_for_backup = WebLabel(
            xpath='//div[@title="Please Select Action for Backup Service Level:"]')
        self.btn_select_action = WebButton(xpath='//table[@id="provider-currentAction"]/tbody/tr/td[2]')
        self.lbl_action_list = WebLabel(xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')
        self.btn_open_additional_email_dropdown = WebButton(xpath='//*[@id="provider-eMail"]/tbody/tr/td[2]')
        self.txt_email_address = WebTextBox(id='provider-emailAddress')

        self.lbl_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
