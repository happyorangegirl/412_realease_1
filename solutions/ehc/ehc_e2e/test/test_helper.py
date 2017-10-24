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

import unittest
import os
from ehc_e2e.workflow import BaseWorkflow


class TestHelper(unittest.TestCase):

    def setUp(self):
        # Workflow
        self.wf = BaseWorkflow()
        _curr_dir = os.path.dirname(os.path.realpath(__file__))
        _parent_dir = os.path.abspath(os.path.join(_curr_dir, os.pardir))
        self._global_file = os.path.join(_parent_dir, 'conf/generic.yaml')
        self._workflow_files = [
            os.path.join(_parent_dir, 'conf/specific.yaml'),
        ]
        self.wf.apply_settings_from_files(self._global_file, *self._workflow_files)

        self.wf.cloud_administrator_opens_browser()
        self.wf.cloud_administrator_login()

    def tearDown(self):
        self.wf.cloud_administrator_logout()
        self.wf.cloud_administrator_closes_browser()
