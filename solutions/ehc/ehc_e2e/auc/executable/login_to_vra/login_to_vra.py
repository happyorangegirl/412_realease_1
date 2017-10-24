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

from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared import LoginPage, MainPage, BasePage
from robot.api import logger


class LoginTovRA(BaseUseCase):
    """
    Login vRA
    """
    Login_Flag = False

    def test_login_to_vra(self):
        login_page = LoginPage()
        main_page = MainPage()
        logger.info('Start to login, user: <{}>'.format(self.username))
        # if had login to vRA, click logout, then login user as expected.
        if BasePage().element_exists(main_page.xpath_btn_logout, self.driver, timeout=3):
            logger.info('vRA has been logged in, try to logout and then login as <{}>.'.format(self.username), False,
                        True)
            main_page.btn_logout.click()
            logger.info('Clicked logout button.', False, True)
            if login_page.btn_back_to_login_page.exists():
                logger.info('Found <Back to login page>.', False, True)
                login_page.btn_back_to_login_page.click()
                logger.info('Clicked <Back to login page>.', False, True)

        # Check whether in page select domain
        if BasePage().element_exists(login_page.next_xpath, self.driver, timeout=3):
            logger.info('Select your domain', False, True)
            if self.domain is not None:
                login_page.select_domain.select(by_visible_text=self.domain)
            login_page.ckb_save_password.click()
            login_page.btn_next.click()
            logger.info('Domain {} selected'.format(self.domain), False, True)

            if login_page.txt_username.exists():
                login_page.login(self.username, self.password)
        # Check whether in page fill username and password
        elif login_page.txt_username.exists():
            login_page.login(self.username, self.password)

        else:
            self.fail(msg='Cannot login to vRA, the current page nether displayed domain to select '
                          'nor textbox of username and password to input.')

        self.assertTrue(MainPage().lbl_login_greeting.exists(), 'No label found: "Welcome,...", failed to login.')
        welcome_texts = MainPage().lbl_login_greeting.value
        # wlecome_texts: Welcome, ehc_sysadmin.
        welcome_user = welcome_texts.split(',')[-1].split('.')[0]
        assert welcome_user.strip() == self.username.strip(), \
            'Current user logged is {}, not {}'.format(welcome_user, self.username)
        LoginTovRA.Login_Flag = True

    def runTest(self):
        self.test_login_to_vra()

    def _validate_input_args(self, current_browser, username, password, domain):
        assert username is not None, 'Please provide user name of vRA Cloud Admin.'
        assert password is not None, 'Please provide password of vRA Cloud Admin.'
        assert current_browser is not None, 'Please open browser.'
        if not domain:
            logger.warn("User didn't provide domain, will use the default domain.")

        self.username = username
        self.password = password
        self.domain = domain
        self.driver = current_browser.instance._browser.current
        self.is_login = current_browser.is_login

    def _finalize_context(self):
        if LoginTovRA.Login_Flag:
            logger.info("User <{}> logged in vRA successful.".format(self.username), False, True)
            setattr(self.ctx_out, 'current_user', self.username)
            setattr(self.ctx_out, 'is_login', True)
