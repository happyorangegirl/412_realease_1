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

"""
Description: This module contains tests for the generic yaml file Functionality.

"""

import unittest

from ehc_e2e_common.generic_yaml_file_parser import GenericYamlFileParser

class TestGenericYamlFileParser(unittest.TestCase):
    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test_generic_parser(self):
        global_context = GenericYamlFileParser.parse_context()
        assert global_context is not None, "Failed to parse the config file."
        for key, value in global_context.__dict__.iteritems():
            assert value is not None, "The {} attribute of global_context is None".format(key)

if __name__ == "__main__":

    unittest.main()
