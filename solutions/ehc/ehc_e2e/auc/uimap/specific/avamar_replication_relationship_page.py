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
from ehc_e2e.auc.uimap.shared.loadingwindow import LoadingWindow
from robot.api import logger


class ARRPage(BasePage):
    def __init__(self):
        super(ARRPage, self).__init__()
        # request info tab
        self.lbl_description = WebLabel(xpath='//div[@title="Description:"]')
        self.txt_description = WebTextBox(id='description')
        self.btn_next = WebButton(id='next')
        # chose option tab
        self.lbl_operation_type = WebLabel(xpath='//div[@title="Action:"]')
        self.lnk_operation_type_menu = WebLink(
            xpath='//*[@id="provider-operationType"]/tbody/tr/td[@align="right"]')
        self.lnk_select_dropdownlist = WebLink(
            xpath='//*[@class="listBoxEx"]/div/table/tbody')
        # Add ARR tab
        self.lbl_asr_name = WebLabel(xpath='//div[@title="Avamar Site Relationship:"]')
        self.lnk_asr_menu = WebLink(
            xpath='//*[@id="provider-asrName"]/tbody/tr/td[@align="right"]')
        self.lbl_site1_avamar_grid = WebLabel(xpath='//div[@title="Site 1 Avamar Grid:"]')
        self.lnk_site1_avamar_menu = WebLink(
            xpath='//*[@id="provider-site1AvamarGrid"]/tbody/tr/td[@align="right"]')
        self.lbl_site2_avamar_grid = WebLabel(xpath='//div[@title="Site 2 Avamar Grid:"]')
        self.lnk_site2_avamar_menu = WebLink(
            xpath='//*[@id="provider-site2AvamarGrid"]/tbody/tr/td[@align="right"]')
        self.lbl_site3_avamar_grid = WebLabel(xpath='//div[@title="Site 3 Avamar Grid:"]')
        self.lnk_site3_avamar_menu = WebLink(
            xpath='//*[@id="provider-site3AvamarGrid"]/tbody/tr/td[@align="right"]')
        # submit request tab
        self.btn_submit = WebButton(id="submit")
        self.lbl_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(id="CONFIRMATION_OK_BUTTON")
        self.btn_save = WebButton(id="save")
        self.btn_cancel = WebButton(id="cancel")

        # delete arr
        self.lbl_delete_arr = WebLabel(xpath='//div[@title="ARR:"]')
        self.lnk_delete_arr_menu = WebLink(
            xpath='//*[@id="provider-deleteARR"]/tbody/tr/td[@align="right"]')
        self.lnk_delete_confirm_menu = WebLink(
            xpath='//*[@id="provider-deleteConfirmation"]/tbody/tr/td[@align="right"]')
        # edit arr
        self.lnk_edit_arr_menu = WebLink(xpath='//*[@id="provider-arrName"]/tbody/tr/td[@align="right"]')
        self.lnk_admin_full_menu = WebLink(xpath='//*[@id="provider-adminFull"]/tbody/tr/td[@align="right"]')

    def add_arr(self, current_browser, cluster_type, arr_entity):
        logger.debug(msg='In step: Select Avamar Site Relationship Name.')
        if self.lnk_asr_menu.exists():
            self.lnk_asr_menu.click()
            if not self.click_drop_down_list(self.lnk_select_dropdownlist, 'div', arr_entity.asr_name):
                logger.error('In DropDownList select Avamar Site Relationship cannot find ASR:' + arr_entity.asr_name)
                return None
            LoadingWindow().wait_loading(current_browser)
        else:
            logger.error(msg='After clicking next button,'
                             'Avamar Site Relationship DropDownList open button does not exist.')
            return None

        logger.debug(msg='In step: Select Site1 Avamar Grid.')
        if self.lnk_site1_avamar_menu.exists():
            self.lnk_site1_avamar_menu.click()
            # select the first option default if it is not provided, else select the option provided.
            # if arr_entity.site1_grid == '[ choose instance ]':
            if arr_entity.site1_grid == '':
                site1_grid = self.select_drop_down_list_by_index(self.lnk_select_dropdownlist,
                                                                 'div',
                                                                 0)
                if site1_grid is not None:
                    arr_entity.site1_grid = site1_grid
                else:
                    logger.error('Failed to select the first option in DropDownList: Site1 Avamar Grid.')
                    return None
            else:
                if not self.click_drop_down_list(self.lnk_select_dropdownlist, 'div', arr_entity.site1_grid):
                    logger.error('In DropDownList Site1 Avamar Grid cannot find Avamar Grid:' + arr_entity.site1_grid)
                    return None
            LoadingWindow().wait_loading(current_browser)
        else:
            logger.error(msg='Site1 Avamar Grid DropDownList open button does not exist.')
            return None
        if cluster_type not in ['LC1S', 'CA1S', 'VS1S']:
            logger.debug(msg='In step: Select Site2 Avamar Grid.')
            if self.lnk_site2_avamar_menu.exists():
                self.lnk_site2_avamar_menu.click()
                # select the first option default if it is not provided, else select the option provided.
                # if arr_entity.site2_grid == '[ choose instance ]':
                if arr_entity.site2_grid == '':
                    site2_grid = self.select_drop_down_list_by_index(self.lnk_select_dropdownlist,
                                                                     'div',
                                                                     0)
                    if site2_grid is not None:
                        arr_entity.site2_grid = site2_grid
                    else:
                        logger.error('Failed to select the first option in DropDownList: Site2 Avamar Grid.')
                        return None
                else:
                    if not self.click_drop_down_list(self.lnk_select_dropdownlist, 'div', arr_entity.site2_grid):
                        logger.error('In DropDownList Site2 Avamar Grid cannot find Avamar Grid:' +
                                     arr_entity.site2_grid)
                        return None
                LoadingWindow().wait_loading(current_browser)
            else:
                logger.error(msg='Site2 Avamar Grid DropDownList open button does not exist.')
                return None
        if cluster_type == 'MP3S':
            logger.debug(msg='In step: Select Site3 Avamar Grid.')
            if self.lnk_site3_avamar_menu.exists():
                self.lnk_site3_avamar_menu.click()
                # select the first option default if it is not provided, else select the option provided.
                # if arr_entity.site3_grid == '[ choose instance ]':
                if arr_entity.site3_grid == '':
                    site3_grid = self.select_drop_down_list_by_index(self.lnk_select_dropdownlist,
                                                                     'div',
                                                                     0)
                    if site3_grid is not None:
                        arr_entity.site3_grid = site3_grid
                    else:
                        logger.error('Failed to select the first option in DropDownList: Site3 Avamar Grid.')
                        return None
                else:
                    if not self.click_drop_down_list(self.lnk_select_dropdownlist, 'div', arr_entity.site3_grid):
                        logger.error('In DropDownList Site3 Avamar Grid cannot find Avamar Grid:' +
                                     arr_entity.site3_grid)
                        return None
                LoadingWindow().wait_loading(current_browser)
            else:
                logger.error(msg='Site3 Avamar Grid DropDownList open button does not exist.')
                return None
        if self.btn_next.exists():
            self.send_tab_key(self.btn_next)
            self.btn_next.click()
        else:
            logger.error(msg='Next button does not exist.')
            return None
        LoadingWindow().wait_loading(current_browser)

        return arr_entity

    @staticmethod
    def get_add_arr_from_all(arr_list, arr_entity):
        if len(arr_list) == 0:
            logger.error(msg='The ARRs list get from vRO is empty')
            return None
        arr_filtered_list = []

        for arr in arr_list:
            if arr.parent_asr == arr_entity.parent_asr and \
                            arr.arr_type == arr_entity.arr_type and \
                            arr.site1_grid == arr_entity.site1_grid and \
                            arr.site2_grid == arr_entity.site2_grid and \
                            arr.site3_grid == arr_entity.site3_grid:
                arr_filtered_list.append(arr)

        if len(arr_filtered_list) == 0:
            logger.error(
                'ARR with specified condition arr_type:{0}, parent_asr:{1},'
                ' site1_grid:{2}, site2_grid:{3}, site3_grid:{4} is not found in vRO.'
                ''.format(arr_entity.arr_type, arr_entity.parent_asr, arr_entity.site1_grid,
                          arr_entity.site2_grid, arr_entity.site3_grid))
            return None
        max_arr = arr_filtered_list[0]
        for arr in arr_filtered_list:
            if int(arr.id) > int(max_arr.id):
                max_arr = arr

        return max_arr
