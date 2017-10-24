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
from robot.api import logger
import sys


class LoadingTable(object):
    def wait_loading(self, current_browser, timeout=30):
        _loading_table_list = []
        try:
            current_browser.instance._browser.current.implicitly_wait(1)
            _loading_table_list = current_browser.instance._browser.current.find_elements_by_class_name(
                "dxgvLoadingPanel_VMware")
            for _loading_table in _loading_table_list:
                # Only check the loading table that is showing in the page
                if 'display: none' not in _loading_table.get_attribute('style'):
                    while timeout > 0 and 'display: none' not in _loading_table.get_attribute('style'):
                        print _loading_table.get_attribute('style')
                        logger.info('Waiting for loading table completion...', False,
                                    True)
                        time.sleep(1)
                        timeout -= 1
                    else:
                        logger.error('Wait loading table failed, exceeded timeout!')
        except:
            logger.error(
                'Encountered exception when waiting for loading table. Error details: {}'.format(sys.exc_info()[:2]))
        finally:
            current_browser.instance._browser.current.implicitly_wait(30)
