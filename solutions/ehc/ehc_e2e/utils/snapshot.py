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

import os
import stat
import sys
import time
from robot.api import logger
from ehc_e2e.workflow.setting import take_screen_shot_on_failure
from ehc_e2e.auc.reusable.inspector import get_caller_keywords_name
from ehc_e2e.auc.reusable.context_util import get_driver, get_context

"""
Used to take screen shot
Example:

from ehc_e2e.utils.snapshot import SnapShot
SnapShot.takes_screen_shot()

"""


class SnapShot(object):

    @staticmethod
    def get_snapshot_dir():
        try:
            _parent_dir = None
            # put screen shot into report path in linux
            if 'win' not in sys.platform:
                _wf_context = get_context()
                _parent_dir = getattr(_wf_context, 'history_dir', None)
            if not _parent_dir:
                _cd = os.path.dirname(os.path.realpath(__file__))
                _parent_dir = os.path.abspath(os.path.join(_cd, os.pardir))
            snapshot_dir = os.path.join(_parent_dir, 'snapshot')
            if not os.path.exists(snapshot_dir):
                os.mkdir(os.path.abspath(snapshot_dir))
            return snapshot_dir
        except:
            logger.warn('Encounter exception in method: get_snapshotshot_dir, more info: '.format(sys.exc_info()))

    # Type of current_driver: WebDriver
    @staticmethod
    def takes_screen_shot(current_driver=None, file_name=None):

        try:
            # If switch of taking screen shot is False, will give up take screen shot
            if not take_screen_shot_on_failure:
                logger.info('The switch of "take_screen_shot_on_failure" is {}'.format(
                    take_screen_shot_on_failure), False, True)
                return

            # If caller didn't provide webdriver, will use current browser
            if not current_driver:
                current_driver = get_driver()

            # If caller didn't provide screen shot name, will use current AUC or keyword as name
            if not file_name:
                file_name = get_caller_keywords_name()

            if not current_driver:
                logger.warn(msg='Parameter current_driver provided is None. Cannot take current screen shot. '
                                'Maybe there is no browser opened.')
                return
            formatter = '%I%M%S%p'
            file_name_full = file_name + time.strftime(formatter, time.localtime()) + '-Failed.png'
            snapshot_dir = SnapShot.get_snapshot_dir()

            file_path = os.path.join(snapshot_dir, file_name_full)
            current_driver.get_screenshot_as_file(file_path)
            logger.info('Saved Snapshot in path: ' + file_path, False, True)

            logger.info('<p><img src="{}" alt="HTML5 Icon" style="width:768px;height:432px;"></p>'.format(file_path),
                        True, False)
        except:
            logger.warn('Encounter exception in method: takes_screen_shot, more info: '.format(sys.exc_info()))

    @staticmethod
    def delete_screen_shot():
        try:
            _cd = SnapShot.get_snapshot_dir()
            files = os.listdir(_cd)
            for fi in files:
                if fi.endswith('.png'):
                    file_path = os.path.join(_cd, fi)
                    os.chmod(file_path, stat.S_IWRITE | stat.S_IWOTH)
                    os.remove(file_path)
                    logger.info('Removed snapshot file: ' + fi, False, True)
        except:
            logger.warn('Encounter exception in method: delete_screen_shot, more info: '.format(sys.exc_info()))
