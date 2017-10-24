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


import sys
import inspect
from robot.api import logger


def get_caller_keywords_name():
    """
    retrieve caller keywords name
    :return: keyword name which starts with cloud_administrator.
    """
    suffix = ['cloud_administrator', 'user', 'login']

    return get_caller_name(suffix)


def get_caller_name(caller_name_filter):
    """
    Get caller name which contains at least one item in caller_name_filter
    :param caller_name_filter: type: []
    :return: the caller name
    """
    try:
        steps = inspect.stack()
        for step in steps:
            for content in step:
                if isinstance(content, str):
                    if any(i in content for i in caller_name_filter):
                        return content
    except:
        logger.warn('Encounter error in get_caller_keywords_name, detail info: {}'.format(sys.exc_info()))

    return ''
