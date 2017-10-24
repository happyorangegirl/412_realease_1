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

from ehc_e2e.auc.uimap.extension import WebCombo, WebFrame


class RequestInfoTab(object):
    def __init__(self):
        super(RequestInfoTab, self).__init__()

        self.frm_catalog = WebFrame(onload='selfservice/SelfServiceGadget.gadget.xml')
        self.txt_description = WebTextBox(id='description')
        self.txt_reasons = WebTextBox(id='reasons')


class SelectOperationTab(object):
    def __init__(self):
        super(SelectOperationTab, self).__init__()

        self.cbo_operation = WebCombo(id='provider-mainAction')


class NavigationBar(object):
    def __init__(self):
        super(NavigationBar, self).__init__()

        self.btn_next = WebButton(id='next')
        self.btn_save = WebButton(id='save')
        self.btn_submit = WebButton(id='submit')
        self.btn_cancel = WebButton(id='cancel')


class RequestResult(object):
    def __init__(self):
        super(RequestResult, self).__init__()

        self.lbl_success_msg = WebLabel(
            xpath='.//div[contains(text(), "The request has been submitted successfully.")]')
        self.btn_ok = WebButton(id='CONFIRMATION_OK_BUTTON')


class Popups(object):
    def __init__(self):
        super(Popups, self).__init__()

        self.lbl_loading_popup = WebLabel(xpath='.//div[@class="gwt-PopupPanelGlass"]')
