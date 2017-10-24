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


class CloseBrowser(BaseUseCase):
    """
    Close the launched browser
    """

    def test_close_browser(self):
        self.ctx_in.instance.close()

    def runTest(self):
        self.test_close_browser()

    def _validate_context(self):
        if self.ctx_in:
            assert self.ctx_in.instance is not None

    def _finalize_context(self):
        setattr(self.ctx_out, 'instance', None)
        setattr(self.ctx_out, 'launched', False)
        setattr(self.ctx_out, 'is_login', False)
        setattr(self.ctx_out, 'current_user', None)
