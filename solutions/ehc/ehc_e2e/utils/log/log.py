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

# This log module is monkey-patch, which SHOULD ONLY be used in development mode, and it can make all levels of
# RobotFramework logger message visible.
#
# DO NOT IMPORT THIS MODULE IN PRODUCTION MODE.
#
# On Windows PowerShell, it's output is colorful.
#
# Usage steps:
#
#     1. Insert one line import into your Python workflow file:
#         ~~~ ehc_e2e/keywords/your_workflow_file.py ~~~
#         ...
#         + from ehc_e2e.utils.log import log
#
#           my_workflow = BaseWorkflow()
#           my_workflow.do_something()
#         ...
#         ~~~
#
#     2. Passing Python script parameters `--log_level` will enable logger handler of STDOUT, which means that, logger
#        will be wrought into STDOUT instead of RobotFramework report.
#
#         $ python ehc_e2e/keywords/your_workflow_file.py --log_level=debug
#         > C:\Python27\python.exe C:/Users/fanm1/emc/solutions/ehc/ehc_e2e/keywords/7-C3-CA2S.py --log_level=debug
#           2016-09-05 22:36:05,220 - e2e - WARNING - DO NOT IMPORT THIS PACKAGE INTO PRODUCTION ENV
#            "C:\Users\fanm1\emc\solutions\ehc\ehc_e2e\utils\log\log.py":138 in <module>()
#           2016-09-05 22:36:08,927 - e2e - INFO - [AUC] - "Cloud Administrator Opens Browser" - PASSED
#            "C:\Users\fanm1\emc\solutions\ehc\ehc_e2e\auc\executable\baseusecase.py":166 in run()
#           2016-09-05 22:36:13,178 - e2e - INFO - Login to vRA successful.
#       "C:\Users\fanm1\emc\solutions\ehc\ehc_e2e\auc\executable\login_to_vra\login_to_vra.py":52 in test_login_to_vra()
#           2016-09-05 22:36:13,187 - e2e - INFO - [AUC] - "Cloud Administrator Login" - PASSED
#             "C:\Users\fanm1\emc\solutions\ehc\ehc_e2e\auc\executable\baseusecase.py":166 in run()
#           ...
#
#     * The level value is not parsed.
#     * GNU bash colorful have not been tested yet.


import argparse
import logging.config
import os

import yaml
from robot.api import logger

from ehc_e2e.utils import get_e2e_file_pathname

_logger_conf = 'utils/log/logging.yaml'
LOGGER_CONF = get_e2e_file_pathname(_logger_conf)


def findCaller(self):
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.
    """
    f = logging.currentframe()
    # On some versions of IronPython, currentframe() returns None if
    # IronPython isn't run with -X:Frames.
    if f is not None:
        f = f.f_back
    if f is not None:
        f = f.f_back
    rv = "(unknown file)", 0, "(unknown function)"
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if filename == logging._srcfile:
            f = f.f_back
            continue
        rv = (co.co_filename, f.f_lineno, co.co_name)
        break
    return rv

logging.Logger.findCaller = findCaller


def setup_logging(config_file=LOGGER_CONF, level=logging.INFO):
    """Setup logging configuration"""
    if os.path.exists(config_file):
        with open(config_file, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)


def _get_logger(name='e2e'):
    """You should call setup_logging() method first before you use `e2e` logger"""

    my_logger = logging.getLogger(name)
    return my_logger


def _get_console_handler():
    """If got handler, its in development environment"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-ll", "--log_level", type=str,
                        help="developer logger level")
    args = parser.parse_args()
    if args.log_level:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        return ch
    else:
        return None


def debug(msg):
    setup_logging()
    _log = _get_logger()
    _log.debug(msg)


def info(msg):
    setup_logging()
    _log = _get_logger()
    _log.info(msg)


def warn(msg):
    setup_logging()
    _log = _get_logger()
    _log.warn(msg)


def error(msg):
    setup_logging()
    _log = _get_logger()
    _log.error(msg)


if _get_console_handler():
    logger.trace = debug
    logger.write = debug
    logger.debug = debug
    logger.info = info
    logger.warn = warn
    logger.error = error

    logger.warn('DO NOT IMPORT THIS PACKAGE INTO PRODUCTION ENV')
