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

from uiacore.modeling.webui.controls import WebTextBox, WebButton, WebCombo


class LoginPage(object):
    def __init__(self):

        self.txt_username = WebTextBox(id='username')
        self.txt_pwd = WebTextBox(id='password')
        self.btn_submit = WebButton(xpath='//*[@type="submit"]')
        self.btn_next = WebButton(xpath='//*[@id="userStoreFormSubmit"]')
        self.next_xpath = '//*[@id="userStoreFormSubmit"]'
        self.btn_back_to_login_page = WebButton(xpath='//button[text()="Go back to login page"]')
        self.btn_back_to_login_page_xpath = '//button[text()="Go back to login page"]'
        self.select_domain = WebCombo(xpath='//*[@id="userStoreDomain"]')
        self.select_domain_xpath = '//*[@id="userStoreDomain"]'
        self.ckb_save_password = WebButton(id="remember")

    def login(self, username, password):
        self.txt_username.set(username)
        self.txt_pwd.set(password)
        self.btn_submit.click()
