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
from ehc_e2e.auc.uimap.shared import LogoutPage
from ehc_e2e.auc.uimap.shared import LoginPage
from robot.api import logger


class LogoutFromvRA(BaseUseCase):
    """
    Logout vRA
    """
    Logout_Flag = False

    def test_logout_from_vra(self):
        self.driver.switch_to.frame(None)
        self.logout_page = LogoutPage()
        self.assertTrue(self.logout_page.btn_logout.exists(), 'Logout button does not exist')
        logger.info('Found "Logout" button', False, True)
        self.logout_page.btn_logout.click()
        logger.info('Clicked "Logout" button')
        # Louis: when testing, found that general it will jumped into "go back .." page,
        # but one or twice it will go into page: input username and password.
        if self.logout_page.element_exists(self.logout_page.btn_back_to_login_page_xpath, self.driver, 5):
            self.logout_page.btn_back_to_login_page.click()
        self.assertTrue(LoginPage().btn_next.exists(), 'Failed to logout from vRA')
        logger.info('Logout from vRA successfully')

        LogoutFromvRA.Logout_Flag = True

    def runTest(self):
        self.test_logout_from_vra()

    def _validate_context(self):
        if self.ctx_in:
            self.current_browser = self.ctx_in.shared.current_browser
            assert self.current_browser is not None, 'Current_browser in yaml is None. Maybe there is no active browser'
            self.assertTrue(self.current_browser.is_login, 'You are not logged in, please login to vRA.')
            self.driver = self.current_browser.instance._browser.current

    def _finalize_context(self):
        if LogoutFromvRA.Logout_Flag:
            setattr(self.ctx_out.shared.current_browser, 'is_login', False)
            setattr(self.ctx_out.shared.current_browser, 'current_user', None)

