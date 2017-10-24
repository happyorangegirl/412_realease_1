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
import time

from robot.api import logger
from uiacore.modeling.webui.browser import Browser
from .context_util import get_last_baseworkflow_instance
from ehc_e2e.utils.context.model import YAMLData


def close_relaunch_browser_operation():
    # We suppose there should be only one instance of BaseWorkflow type or its subclass.
    baseworkflow_instance = get_last_baseworkflow_instance()
    if not baseworkflow_instance:
        logger.warn('BaseWorkflow instance not found, will not proceed relaunch operation.')
        return False

    ctx = baseworkflow_instance.wf_context
    launch_url = ctx.launch_browser.baseUrl + ctx.vra.tenant
    ctx_browser = ctx.shared.current_browser.instance

    try:
        # We forced the vRA to logout before closing browser since we observed chance that relaunch browser
        #  bypassed the authentication.
        ctx_browser._browser.current.switch_to.default_content()
        time.sleep(1)
        from uiacore.modeling.webui.controls import WebButton
        btn_logout = WebButton(id='SHELL_LOGOUT')
        if btn_logout.exists():
            logger.info(
                'vRA is logged in, try to click logout button to force logout vRA before relaunching browser',
                False, True)
            btn_logout.click()
            logger.info('vRA has been logged out successfully.', False, True)
        time.sleep(1)
        ctx_browser.close()
        logger.info('Closed Browser successfully.', False, True)
        setattr(ctx, 'is_login', False)
        logger.info('Sleeping 5 seconds before relaunching browser.', False, True)
        time.sleep(5)
        new_browser = Browser(ctx.launch_browser.browserType, name='EHC_UI')
        new_browser.launch(launch_url)
        new_browser.maximize()
        ctx.shared.current_browser.instance = new_browser
        logger.info(
            'Done setting context.shared.current_browser.instance to new Browser instance.', False, True)
        logger.info('Sleeping 2 seconds after relaunching browser.', False, True)
        time.sleep(2)

        logger.info('Trying to login vRA again.', False, True)

        # Get the user to login.
        _current_browser = ctx.shared.current_browser
        _current_user = getattr(ctx.shared.current_browser, 'current_user')
        _users = getattr(ctx, 'user_roles', YAMLData(**{}))
        kwargs = {}
        for key, value in _users.__dict__.items():
            if value['username'] == _current_user:
                kwargs = {
                    'current_browser': _current_browser,
                    'username': _current_user,
                    'password': value['password'],
                    'domain': value['domain']
                }
        from ehc_e2e.auc.executable.login_to_vra import LoginTovRA
        LoginTovRA(
            'user_login', ctx_in=ctx, ctx_out=ctx.shared.current_browser, **kwargs).run()
        logger.info('Completed login in vRA again.', False, True)

        return True
    except:
        logger.error(
            'Trying to close and relaunch browser encounters error, error details:{}'.format(
                sys.exc_info()))
        raise
