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

from uiacore.modeling.webui.controls import WebButton, WebLabel


class MainPage(object):
    def __init__(self):
        self.btn_home = WebButton(id='csp.home')
        self.btn_catalog = WebButton(id='csp.catalog.selfservice')
        self.btn_items = WebButton(id='csp.catalog.item')
        self.btn_requests = WebButton(id='csp.catalog.request')
        self.btn_administration = WebButton(id='vcac.administration')
        self.btn_infrastructure = WebButton(id='csp.places.iaas')
        self.lbl_login_greeting = WebLabel(id='SHELL_GREETING')
        self.btn_logout = WebButton(id='SHELL_LOGOUT')
        self.xpath_btn_logout = '//a[@id="SHELL_LOGOUT"]'

    def navigate_to_mainpage(self, current_browser):
        _browser = current_browser.instance._browser.current
        self.is_mainpage_flag = False
        try:
            _browser.switch_to.frame(None)
            self.is_mainpage_flag = self.btn_requests.exists()
        except:
            self.is_mainpage_flag = False
        return self.is_mainpage_flag
