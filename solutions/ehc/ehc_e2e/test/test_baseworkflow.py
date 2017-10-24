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

from __future__ import absolute_import
import os
import pickle
import unittest


class TestBaseWorkflow(unittest.TestCase):
    def setUp(self):
        self._cd = os.path.dirname(os.path.realpath(__file__))
        self._current_dir = os.path.abspath(os.path.join(self._cd, os.curdir))
        self._dump_yaml = os.path.join(self._current_dir, 'test_data/test_data_context_compare_update_dump.yaml')
        self._wf_yaml = os.path.join(self._current_dir, 'test_data/test_data_context_compare_update_WF-E2E-1-LC1S.yaml')
        self._data_context_compare_update_result_yaml = os.path.join(
            self._current_dir, 'test_data/test_data_context_compare_update_result.yaml')
        self._dump_f = open(self._dump_yaml, 'r')
        self._expect_result_f = open(self._data_context_compare_update_result_yaml, 'r')

    def test_data_context_attributes_compare_update(self):
        from ehc_e2e.workflow import BaseWorkflow
        from ehc_e2e.utils.context import DataContext
        wf_context = DataContext(None, 'WORKFLOW_CONTEXT')
        wf_context.update_context(self._wf_yaml, 'WORKFLOW_CONTEXT')
        dump_context = pickle.load(self._dump_f)
        self._dump_f.close()
        self._dump_f = open(self._dump_yaml, 'r')
        expected_result_context_string = self._expect_result_f.read()
        baseworkflow = BaseWorkflow()
        from uiacore.modeling.webui.browser import Browser
        exclusive_keys = ['added', 'existed', 'backup_service_levels']
        self.assertTrue(
            baseworkflow.data_context_attributes_compare_update(
                dump_context, wf_context.WORKFLOW_CONTEXT, [Browser], exclusive_keys, ['blueprint_machine_pairs']),
            'data_context_attributes_compare_update failed.'
        )
        self.assertIsNotNone(dump_context)
        self.assertIsNotNone(wf_context)

        # NOTE: YAMLDATA equality is not implemented neat enough, so will do string representation comparision for
        # YAMLDATA objects.
        dump_context_string = None
        with open('temp', 'w') as f:
            pickle.dump(dump_context, f)
        f.close()
        with open('temp', 'r') as f2:
            dump_context_string = f2.read()
        f2.close()
        self.assertTrue(dump_context_string == expected_result_context_string, 'datacontext compare and update failed.')

    def tearDown(self):
        self._dump_f.close()
        self._expect_result_f.close()
        if os.path.exists('temp'):
            os.remove('temp')
