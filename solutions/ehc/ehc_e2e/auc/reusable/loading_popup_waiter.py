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

import time
from unittest import TestCase

from ehc_e2e.auc.uimap.shared import LoadingWindow
from ehc_e2e.auc.uimap.shared.generic import Popups
from .context_util import get_last_baseworkflow_instance


class LoadingPopupWaiter(object):
    def __init__(self, case_owner, browser=None):
        if case_owner and isinstance(case_owner, TestCase):
            self._case_checker = case_owner
        else:
            raise RuntimeError('Unable to validate page objects')

        baseworkflow = get_last_baseworkflow_instance()

        self._browser = baseworkflow.wf_context.shared.current_browser

    def wait_for_popup_loading_finish(self):
        LoadingWindow().wait_loading(self._browser)

    def wait_for_popup_loading_finish_deprecated(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        _popups = Popups()

        _wait_time_in_secs = 30
        if self._browser:
            _wait_time_in_secs = self._browser._implicit_wait

            self._browser.current.implicitly_wait(1)
            self._browser._implicit_wait = 1

        timeout = 300
        while timeout > 0:
            if _popups.lbl_loading_popup.exists():
                time.sleep(1)
                timeout -= 1
            else:
                break

        self._case_checker.assertFalse(
            _popups.lbl_loading_popup.exists(), msg=_formatter(step='Timed out for loading popup'))

        if self._browser:
            self._browser.current.implicitly_wait(_wait_time_in_secs)
            self._browser._implicit_wait = _wait_time_in_secs
