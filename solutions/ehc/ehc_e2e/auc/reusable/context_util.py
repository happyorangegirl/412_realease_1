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
from robot.api import logger

import ehc_e2e.workflow


def get_last_baseworkflow_instance():
    weak_instances = list(ehc_e2e.workflow.BaseWorkflow.weak_instances)

    # We normally will have only one item.
    if weak_instances:
        if len(weak_instances) == 1:
            logger.debug('Found one live instance of BaseWorkflow.')
            return weak_instances[0]
        else:
            logger.warn('Found {} live instances of BaseWorkflow, There is '
                        'normally only one, just return None.'.format(len(weak_instances)))
            return None
    else:
        logger.warn('No BaseWorkflow instance found in current context.')

    # This should not happen!!
    return None


def get_driver():
    try:
        _context = get_context()
        if hasattr(_context, 'shared') and hasattr(_context.shared, 'current_browser') and \
            hasattr(_context.shared.current_browser, 'instance') and \
            hasattr(_context.shared.current_browser.instance, '_browser'):
            _driver = _context.shared.current_browser.instance._browser.current
            return _driver
        logger.info('The driver get from get_driver is None.')
        return None
    except:
        import traceback
        logger.error(traceback.print_stack())
        logger.error('Encounter error in get_driver, detail info: {}'.format(sys.exc_info()))
        raise


def get_context():
    try:
        wf_context = get_last_baseworkflow_instance().wf_context
        return wf_context
    except:
        logger.error('Encounter error in get_context, detail info: {}'.format(sys.exc_info()))
        raise
