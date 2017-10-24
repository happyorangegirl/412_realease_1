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

from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared import CatalogPage
from ehc_e2e.auc.uimap.shared import LoadingWindow
from ehc_e2e.auc.uimap.specific import SiteMaintenancePage


class SiteManager(BaseUseCase):
    class Func(object):
        ADD_SITES, EDIT_SITES, DELETE_SITES = (
            'test_add_site',
            'test_edit_site',
            'test_delete_site'
        )

    def __init__(self, name=None, method_name=Func.ADD_SITES, **kwargs):
        super(SiteManager, self).__init__(
            name, method_name, **kwargs)
        _auc_name = ' '.join([word.capitalize() for word in name.split('_')])
        self._formatter = ('Running on: ' + _auc_name + ' - FAILED, "{step}"').format

    def setUp(self):
        self._site_page = SiteMaintenancePage()
        self._loading_window = LoadingWindow()

    def test_add_site(self):
        action = 'Add Site'
        self._added_ok_site = None

        self._start_site_maintenance()
        try:
            self._choose_action(action)
            self._fill_add_site_items()
            self._review_submit_items(action, self._add_site)
            self._added_ok_site = self._add_site
        except AssertionError:
            self._handle_assert_exception()
        except:
            ex = sys.exc_info()[:2]
            self._handle_other_exception(ex)

    def test_delete_site(self):
        action = 'Delete Site'
        self._start_site_maintenance()
        try:
            self._choose_action(action)
            self._fill_delete_site_items()
            self._review_submit_items(action, self._delete_site)
        except AssertionError:
            self._handle_assert_exception()
        except:
            ex = sys.exc_info()[:2]
            self._handle_other_exception(ex)

    def test_edit_site(self):
        action = 'Edit Site'
        self._start_site_maintenance()
        try:
            self._choose_action(action)
            self._fill_edit_site_items()
            self._review_submit_items(action, self._edit_site_name, self._new_site_name)
        except AssertionError:
            self._handle_assert_exception()
        except:
            ex = sys.exc_info()[:2]
            self._handle_other_exception(ex)

    def _start_site_maintenance(self):
        self.catalog_page = CatalogPage()
        self.assertTrue(self.catalog_page.navigate_to_catalog(self._current_browser),
                        msg=self._formatter(step='failed to switch to catalog frame.'))
        self.assertTrue(self.catalog_page.lnk_ehc_configuration.exists(),
                        msg=self._formatter(step='cannot find EHC Configuration card in the left page.'))
        self.catalog_page.lnk_ehc_configuration.click()
        self.catalog_page.wait_for_loading_complete(3)
        self.assertTrue(self.catalog_page.btn_site_maintenance_request.exists(),
                        msg=self._formatter(step='cannot find Site Maintenance card in the right page.'))
        self.catalog_page.btn_site_maintenance_request.click()
        self._loading_window.wait_loading(self._current_browser, 30)

    def _choose_action(self, action):
        logger.info(msg='Start to fill info in tab: Request information')
        self.assertTrue(self._site_page.txt_describe.exists(),
                        msg=self._formatter(step='there is no description textbox.'))
        self._site_page.txt_describe.set(self._description)
        logger.info('Filled {} in description textbox.'.format(self._description))
        time.sleep(3)
        self._click_next_button()
        logger.info(msg='Complete fill info in tab: Request information')
        logger.info(msg='Start to fill info in tab: Action Choice')
        self.assertTrue(self._site_page.lnk_action_to_be_performed_menu.exists,
                        msg=self._formatter(step='Action DropDownList open button does not exist.'))

        self._site_page.lnk_action_to_be_performed_menu.click()
        self.assertTrue(self._site_page.click_drop_down_list(
            self._site_page.lnk_action_to_be_performed_dropdownlist,
            'div', action), msg=self._formatter(step='there is no Action: {}'.format(action)))

        self._loading_window.wait_loading(self._current_browser, 30)
        self._click_next_button()

        logger.info(msg='Complete fill info in tab: Action Choice')

    def _fill_add_site_items(self):
        logger.info(msg='Start to fill info in tab: Add Site')
        self.assertTrue(self._site_page.txt_site_name.exists(),
                        msg=self._formatter(step='can not find Site Name textbox.'))
        time.sleep(3)
        self._site_page.txt_site_name.set(self._add_site)
        logger.info(msg='Filled {0} in Site Name textbox.'.format(self._add_site))
        time.sleep(2)
        self._click_next_button()
        logger.info(msg='Complete fill info in tab: Add Site')

    def _fill_edit_site_items(self):
        logger.info(msg='Start to fill info in tab: Edit Site')
        self.assertTrue(self._site_page.lnk_edit_site_menu.exists(),
                        msg=self._formatter(step='Site DropDownList open button does not exist.'))

        self._site_page.lnk_edit_site_menu.click()
        self.assertTrue(self._site_page.click_drop_down_list(self._site_page.lnk_edit_site_dropdownlist,
                                                             'div', self._edit_site_name),
                        msg=self._formatter(step='target site {0} does not exist in Site DropDownList.')
                        .format(self._edit_site_name))

        self._loading_window.wait_loading(self._current_browser, 30)
        self.assertTrue(self._site_page.txt_new_site_name.exists(),
                        msg=self._formatter(step='cannot find New Site Name textbox.'))
        time.sleep(3)
        self._site_page.txt_new_site_name.set(self._new_site_name)
        logger.info(msg='Filled {0} in New Site Name textbox.'.format(self._new_site_name))
        self._loading_window.wait_loading(self._current_browser, 30)
        self._click_next_button()
        logger.info(msg='Complete fill info in tab: Edit Site')

    def _fill_delete_site_items(self):
        logger.info(msg='Start to fill info in tab: Delete Site')
        self.assertTrue(self._site_page.lnk_delete_site_menu.exists(),
                        msg=self._formatter(step='Site DropDownList open button does not exist.'))

        self._site_page.lnk_delete_site_menu.click()

        self.assertTrue(self._site_page.click_drop_down_list(self._site_page.lnk_delete_site_dropdownlist,
                                                             'div', self._delete_site),
                        msg=self._formatter(step='target site {0} does not exist in Site DropDownList.')
                        .format(self._delete_site))
        logger.info('Selected site {} to delete.'.format(self._delete_site))
        self._loading_window.wait_loading(self._current_browser, 30)
        self.assertTrue(self._site_page.lnk_confirm_delete_site_menu.exists(),
                        msg=self._formatter(step='Confirm DropDownList open button does not exist.'))
        self._site_page.lnk_confirm_delete_site_menu.click()

        self.assertTrue(self._site_page.click_drop_down_list(self._site_page.lnk_confirm_delete_site_dropdownlist,
                                                             'div', 'Confirm'),
                        msg=self._formatter(step='Confirm does not exist in Confirm DropDownList.')
                        .format(self._delete_site))
        self._loading_window.wait_loading(self._current_browser, 30)
        self._click_next_button()
        logger.info(msg='Complete fill info in tab: Delete Site')

    def _review_submit_items(self, action=None, site=None, new_site=None):
        logger.info(msg='Start to fill info in tab: Review and Submit.')
        self.assertTrue(self._site_page.lbl_review_action.exists(),
                        msg=self._formatter(step='Action label in tab Review and Submit: does not exist.'))

        if action:
            _final_action = self._site_page.lbl_review_action.value
            self.assertEquals(_final_action, action,
                              msg=self._formatter(step='Action does not match with the user choice, user choice:'
                                                       ' {0}, Action: {1}.'.format(action, _final_action)))
        if site:
            if not self._site_page.wait_to_replace_default_site_in_review_action(site):
                self.fail(self._formatter(step='Site is not {0}.'.format(site)))

        if new_site:
            _final_new_site = self._site_page.lbl_review_new_site.value
            self.assertEquals(_final_new_site,
                              new_site,
                              msg=self._formatter(
                                  action=action, step='New Site does not match with the user choice, user choice: '
                                                      '{0}, New Site: {1}.'.format(new_site, _final_new_site)))
        self.assertTrue(self._site_page.btn_submit.exists(),
                        msg=self._formatter(step='there is no Submit button.'))
        self._site_page.btn_submit.click()
        logger.info('Clicked Submit button.')
        time.sleep(3)
        self.assertTrue(
            self._site_page.lbl_confirmation_success.exists(),
            msg=self._formatter(step='label "The request has been submitted successfully" does not exist.'))

        self.assertTrue(
            self._site_page.btn_ok.exists(),
            msg=self._formatter(step='there is no OK button.'))
        self._site_page.btn_ok.click()
        logger.info('Click OK button.')
        logger.info(msg='Complete fill info in tab: Review and Submit.')

    def _click_next_button(self):
        self.assertTrue(self._site_page.btn_next.exists(),
                        msg=self._formatter(step='there is no Next button.'))

        self._site_page.btn_next.click()
        logger.info('Clicked Next button.')
        self._loading_window.wait_loading(self._current_browser, 30)

    def _handle_assert_exception(self):
        self._site_page.save_request()

        raise

    def _handle_other_exception(self, err_message):
        self._site_page.save_request()
        self.fail(msg=self._formatter(step='encounters error: {0}, have clicked Save button to save request.'.
                                      format(err_message)))

    def _validate_input_args(self, **kwargs):
        if self._testMethodName == self.Func.ADD_SITES:
            self.__validate_args_of_add_sites(**kwargs)
        elif self._testMethodName == self.Func.EDIT_SITES:
            self.__validate_args_of_edit_sites(**kwargs)
        elif self._testMethodName == self.Func.DELETE_SITES:
            self.__validate_args_of_delete_sites(**kwargs)
        else:
            raise ValueError('Unsupported test method.')

    def __validate_browser_info(self, current_browser, is_login):
        assert current_browser is not None, \
            self._formatter(step='current_browser is None, may be there is no active browser.')
        assert is_login is True, self._formatter(step="can't do anything if you didn't login.")
        self._current_browser = current_browser

    def __validate_args_of_add_sites(self, current_browser=None, is_login=False, site_name=None,
                                     description=None, output=None):
        self.__validate_browser_info(current_browser, is_login)
        self._add_site = site_name
        self._description = description
        assert site_name is not None, self._formatter(step='the site name is None.')

    def __validate_args_of_edit_sites(self, current_browser=None, is_login=False,
                                      site_name=None, new_site_name=None, description=None):
        self.__validate_browser_info(current_browser, is_login)
        assert site_name is not None, self._formatter(step='the site name is None.')
        assert new_site_name is not None, self._formatter(step='the new site name is None.')
        self._edit_site_name = site_name
        self._new_site_name = new_site_name
        self._description = description

    def __validate_args_of_delete_sites(self, current_browser=None, is_login=False, site_name=None, description=None):
        self.__validate_browser_info(current_browser, is_login)
        self._delete_site = site_name
        self._description = description

    def _finalize_output_params(self):
        if self._testMethodName == self.Func.ADD_SITES:
            if self._added_ok_site:
                self._output.append(self._added_ok_site)
        else:
            pass
