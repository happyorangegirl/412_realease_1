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

from uiacore.modeling.webui.controls import (WebTextBox, WebButton, WebLink)


class BlueprintPage(object):
    def __init__(self):

        # Common area
        self.btn_ok = WebButton(
            xpath='//*[@id="Content"]/div[4]/a[@name="DefaultButton" '
                  'and @value="OK"]')
        self.btn_cancel = WebButton(
            xpath='//*[@id="Content"]/div[4]/a[@name="ctl00$ctl00$MasterContent'
                  '$MainContentPlaceHolder$ctl01" and @value="Cancel"]')

        # Blueprint information tab
        self.txt_reservation_policy = WebTextBox(
            id='ctl00_ctl00_MasterContent_MainContentPlaceHolder_BlueprintTabs_PolicyPicker_I'
        )
        self.lnk_blueprint_edit_reservation_policy_menu = WebLink(
            xpath='//*[@id="ctl00_ctl00_MasterContent_MainContentPlaceHolder_'
                  'BlueprintTabs_PolicyPicker_DDD_L_LBT"]')
        self.btn_blueprint_edit_reservation_policy_open = WebButton(
            xpath='//*[@id="ctl00_ctl00_MasterContent_MainContentPlaceHolder_'
                  'BlueprintTabs_PolicyPicker_B-1"]')
        self.lnk_blueprint_edit_machine_prefix_menu = WebLink(
            xpath='//*[@id="ctl00_ctl00_MasterContent_MainContentPlaceHolder_'
                  'BlueprintTabs_ddPrefixOverride_DDD_L_LBT"]'
        )
        self.btn_blueprint_edit_machine_prefix_open = WebButton(
            xpath='//*[@id="ctl00_ctl00_MasterContent_MainContentPlaceHolder_'
                  'BlueprintTabs_ddPrefixOverride_B-1"]'
        )
        self.txt_blueprint_name = WebTextBox(
            xpath='//*[@id="ctl00_ctl00_MasterContent_MainContentPlaceHolder'
                  '_BlueprintTabs_txtName_I"]'
        )
        self.txt_description = WebTextBox(
            xpath='//*[@id="ctl00_ctl00_MasterContent_MainContentPlaceHolder'
                  '_BlueprintTabs_txtDescription_I"]'
        )
