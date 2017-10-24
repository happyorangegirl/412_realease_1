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

from robot.api import logger
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from uiacore.modeling.webui.browser import Browser


class LaunchBrowser(BaseUseCase):
    """
    Launch browser and navigate to the specified URL
    """
    IS_LAUNCHED = False

    def test_launch_browser(self):
        self.browser = Browser(self.ctx_in.launch_browser.browserType, name='EHC_UI')
        self.browser.launch(self.launch_url)
        self.browser.maximize()
        logger.info('Launched browser.', False, True)
        LaunchBrowser.IS_LAUNCHED = True

    def runTest(self):
        self.test_launch_browser()

    def _validate_context(self):
        self.browser = None

        if self.ctx_in:
            assert self.ctx_in.launch_browser.baseUrl is not None, 'baseUrl in yaml is None'
            assert self.ctx_in.launch_browser.browserType is not None, 'browserType in yaml is None'
            assert self.ctx_in.vra.tenant is not None, 'tenant is None'
            self.launch_url = self.ctx_in.launch_browser.baseUrl + self.ctx_in.vra.tenant

    def _finalize_context(self):
        if LaunchBrowser.IS_LAUNCHED:
            setattr(self.ctx_out.shared.current_browser, 'instance', self.browser)
            setattr(self.ctx_out.shared.current_browser, 'launched', LaunchBrowser.IS_LAUNCHED)
