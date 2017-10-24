"""
 Copyright 2016 EMC GSE SW Automation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import sys

from robot.api import logger
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared.basepage import BasePage
from ehc_e2e.auc.uimap.shared.catalogpage import CatalogPage
from ehc_e2e.auc.uimap.shared.loadingwindow import LoadingWindow
from ehc_e2e.auc.uimap.specific.avamarsiterelationshippage import AvamarSiteRelationshipPage
from .asr_constants import (backup_env_type_prefix_single_copy,
                            backup_env_type_prefix_two_copies,
                            backup_env_type_prefix_three_copies,
                            backup_env_type_map)


def _generate_asr_full_name(asr_name, backup_env_type, sites):

    full_name = asr_name + '-' + \
                '[' + '-'.join([backup_env_type] + sites) + ']'
    return full_name


class ASRManager(BaseUseCase):
    """
        For adding Avamar site relationship,
        currently supports one site, two sites, three sites backup.
    """

    class Func(object):
        ADD_ASR, EDIT_ASR, DELETE_ASR = (
            'test_add_avamar_site_relationship',
            'test_edit_avamar_site_relationship',
            'test_delete_avamar_site_relationship'
        )

    def __init__(self, name=None, method_name=Func.ADD_ASR, **kwargs):
        super(ASRManager, self).__init__(
            name, method_name, **kwargs)
        _auc_name = ' '.join([word.capitalize() for word in name.split('_')])
        self._formatter = ('Running on: ' + _auc_name + ' - FAILED, {}.').format

    def setUp(self):
        self._asr_page = AvamarSiteRelationshipPage()
        self._loading_window = LoadingWindow()
        self._catalog_page = CatalogPage()

    def test_add_avamar_site_relationship(self):
        self.start_avamar_site_relationship_maintenance()
        try:
            self.fill_description()
            self.choose_action()
            self.fill_add_asr_item()
            self.submit_request()

        except AssertionError:
            self._asr_page.save_request()
            raise
        except:
            self._asr_page.save_request()
            self.fail(
                'Add Avamar Site Relationship encounters error: {}.'.format(sys.exc_info()[:2]))

    def test_edit_avamar_site_relationship(self):
        self.start_avamar_site_relationship_maintenance()
        try:
            self.fill_description()
            self.choose_action()
            self.fill_edit_asr_item()
            self.submit_request()

        except AssertionError:
            self._asr_page.save_request()
            raise
        except:
            self._asr_page.save_request()
            self.fail(
                'Edit Avamar Site Relationship encounters error: {}.'.format(sys.exc_info()[:2]))

    def test_delete_avamar_site_relationship(self):
        self.start_avamar_site_relationship_maintenance()
        try:
            self.fill_description()
            self.choose_action()
            self.fill_delete_asr_item()
            self.submit_request()
        except AssertionError:
            self._asr_page.save_request()
            raise
        except:
            self._asr_page.save_request()
            self.fail(
                'Delete Avamar Site Relationship encounters error: {}.'.format(sys.exc_info()[:2]))

    def start_avamar_site_relationship_maintenance(self):
        self.assertTrue(
            self._catalog_page.navigate_to_catalog(self.current_browser),
            msg=self._formatter('switch to catalog page failed.'))

        self.assertTrue(self._catalog_page.lnk_data_protection_services.exists(),
                        msg=self._formatter(
                            'cannot find Data Protection Services button in the left pane.'))

        self._catalog_page.lnk_data_protection_services.click()
        BasePage().wait_for_loading_complete(2)

        self.assertTrue(self._catalog_page.btn_asr_maintenance_request.exists(),
                        msg=self._formatter(
                            'cannot find Avamar Site Relationship (ASR) '
                            'Maintenance card in the right page.'))
        self._catalog_page.btn_asr_maintenance_request.click()
        logger.info(
            msg='Clicked Avamar Site Relationship (ASR) Maintenance request '
                'button.')
        LoadingWindow().wait_loading(self.current_browser, 30)

    def fill_description(self):
        logger.info(msg='Start to fill info in Tab: Request information.')
        self.assertTrue(
            self._asr_page.lbl_description.exists(),
            msg=self._formatter(
                'there is no textbox Description')
        )
        self._asr_page.txt_description.set(self.description)
        logger.info(
            msg='Filled in the description: {} for Add Avamar Site '
                'Relationship'.format(self.description))
        self.click_next_button()
        logger.info(msg='Complete filling into in Tab: Request information.')

    def choose_action(self):
        logger.info(msg='Start to fill info in Tab: Action Choice.')
        self.assertTrue(self._asr_page.lbl_select_action.exists(),
                        msg=self._formatter(
                            'failed to go to "select an action" tab.'))
        self.assertTrue(self._asr_page.lnk_select_action_menu_open.exists(),
                        msg=self._formatter('"choose action" drop down list does not exist.'))
        self._asr_page.lnk_select_action_menu_open.click()
        self.assertTrue(
            self._asr_page.click_drop_down_list(
                self._asr_page.lnk_dropdownlist,
                'div',
                self.action
            ),
            msg=self._formatter(
                'failed to select action {}'.format(self.action)))
        LoadingWindow().wait_loading(self.current_browser, 30)
        logger.info(msg='Selected action {} for Avamar Site Relationship'.format(self.action))
        self.click_next_button()
        logger.info(msg='Complete filling into in Tab: Action Choice.')

    def click_next_button(self):
        self.assertTrue(self._asr_page.btn_next.exists(),
                        msg=self._formatter('there is no Next button.'))
        self._asr_page.btn_next.click()
        logger.info('Clicked Next button.')
        self._loading_window.wait_loading(self.current_browser, 30)

    def submit_request(self):
        logger.info('Start to submit request and confirm success info.')
        self.assertTrue(self._asr_page.btn_submit.exists(),
                        msg=self._formatter('there is no Submit button.'))

        self._asr_page.btn_submit.click()
        logger.info('Clicked Submit button.')
        self._loading_window.wait_loading(self.current_browser, 30)
        self.assertTrue(
            self._asr_page.lbl_confirmation_success.exists(),
            msg=self._formatter(
                'Label "The request has been submitted successfully" does not '
                'exist.')
        )
        self._asr_page.btn_ok.click()

    def fill_add_asr_item(self):
        logger.info(msg='Start to fill info in Tab: Add ASR.')
        backup_env_type_selection = backup_env_type_map.get(
            self.backup_env_type)
        self.assertIsNotNone(
            backup_env_type_selection,
            msg=self._formatter(
                '{} is not a supported backup_environment_type.'
                ''.format(self.backup_env_type)))
        if self.backup_env_type.startswith(backup_env_type_prefix_two_copies) \
                or self.backup_env_type == "MC2VC":
            self._add_asr_two_sites(
                self.current_browser, self._asr_page, backup_env_type_selection,
                self.site_first, self.site_second)
        elif self.backup_env_type.startswith(
                backup_env_type_prefix_three_copies):
            self._add_asr_three_sites(
                self.current_browser,
                self._asr_page, backup_env_type_selection, self.site_first,
                self.site_second, self.site_third)
        elif self.backup_env_type.startswith(
                backup_env_type_prefix_single_copy
        ):
            self._add_asr_one_site(
                self.current_browser, self._asr_page,
                backup_env_type_selection, self.site_first)
        else:
            raise NotImplementedError(
                '"{}" is not a supported backup environment type.'
                ''.format(backup_env_type_selection))
        self.click_next_button()
        logger.info('Complete filling info in Tab: Add ASR.')

    def fill_edit_asr_item(self):
        logger.info(msg='Start to fill info in Tab: Edit ASR.')
        if self.backup_env_type.startswith(backup_env_type_prefix_two_copies) or self.backup_env_type == "MC2VC":
            self._edit_asr_two_sites(self.current_browser, self._asr_page, self.site_first, self.site_second)
        elif self.backup_env_type.startswith(
                backup_env_type_prefix_three_copies):
            self._edit_asr_three_sites(
                self.current_browser, self._asr_page, self.site_first,
                self.site_second, self.site_third
            )
        elif self.backup_env_type.startswith(
                backup_env_type_prefix_single_copy):
            self._edit_asr_one_site(
                self.current_browser, self._asr_page, self.site_first
            )
        else:
            raise NotImplementedError(
                '"{}" is not a supported backup environment type.'
                ''.format(self.backup_env_type))
        self.click_next_button()
        logger.info('Complete filling info in Tab: Edit ASR.')

    def fill_delete_asr_item(self):
        logger.info('Start to fill info in Tab: Delete ASR.')
        self.assertTrue(self._asr_page.lbl_asr_name.exists(),
                        self._formatter('failed to go to "Delete ASR" tab.'))
        self.assertTrue(self._asr_page.lnk_select_asr_name_menu_open.exists(),
                        self._formatter('"ASR" drop down list does not exist.'))
        self._asr_page.lnk_select_asr_name_menu_open.click()
        self.assertTrue(
            BasePage().click_drop_down_list(
                self._asr_page.lnk_dropdownlist, 'div',
                self.avamar_site_relationship_name),
            msg=self._formatter(
                'failed to select Avamar Site Relationship: {} to delete.'.format(
                    self.avamar_site_relationship_name))
        )
        LoadingWindow().wait_loading(self.current_browser, 30)
        self.assertTrue(
            self._asr_page.btn_confirm_dropdonwlist_open.exists(),
            self._formatter('open confirm dropdownlist button does not exist.')
        )
        self._asr_page.btn_confirm_dropdonwlist_open.click()
        self.assertTrue(
            BasePage().click_drop_down_list(
                self._asr_page.lnk_dropdownlist, 'div',
                'Confirm'
            ),
            self._formatter('failed to select "Confirm" for delete.')
        )
        LoadingWindow().wait_loading(self.current_browser, 30)
        self.click_next_button()
        logger.info('Complete filling info in Tab: Delete ASR.')

    def _add_asr_one_site(self, current_browser, asr_page, backup_env_type, site_first):
        _browser = current_browser
        self.assertTrue(asr_page.lbl_select_backup_env_type.exists(),
                        msg=self._formatter(
                            'failed to go to "Add ASR" tab.'))
        asr_page.lnk_select_backup_env_type_menu_open.click()
        self.assertTrue(
            asr_page.click_drop_down_list(asr_page.lnk_dropdownlist, 'div',
                                          backup_env_type, compare_contains=True),
            msg=self._formatter(
                'select {} for backup_env_type.'.format(self.backup_env_type)))
        LoadingWindow().wait_loading(_browser, 30)
        self.assertTrue(asr_page.lbl_select_first_asr_site.exists(),
                        msg=self._formatter(
                            '"Select first site" in "Add an ASR" tab does not '
                            'exist.'))
        asr_page.lnk_select_first_asr_site_menu_open.click()
        logger.info('Trying to select first site: {}'.format(site_first), False, True)
        self.assertTrue(
            asr_page.click_drop_down_list(asr_page.lnk_dropdownlist, 'div',
                                          site_first),
            msg=self._formatter(
                '"{}" not found to be selected as first site.'.format(site_first)))
        LoadingWindow().wait_loading(_browser, timeout=30)

    def _add_asr_two_sites(self, current_browser, asr_page, backup_env_type,
                           site_first, site_second):
        _browser = current_browser
        self._add_asr_one_site(current_browser, asr_page, backup_env_type,
                               site_first)
        self.assertTrue(asr_page.lbl_select_second_asr_site.exists(),
                        msg=self._formatter(
                            '"Select second site" in "Add an ASR" tab does not '
                            'exist.'))
        logger.info('Trying to select second site: {}'.format(site_second), False,
                    True)
        asr_page.lnk_select_second_asr_site_menu_open.click()
        self.assertTrue(
            asr_page.click_drop_down_list(
                asr_page.lnk_dropdownlist, 'div', site_second),
            msg=self._formatter(
                '"{}" not found to be selected as second site.'.format(
                    site_second)))
        LoadingWindow().wait_loading(_browser, 30)

    def _add_asr_three_sites(self, current_browser, asr_page, backup_env_type,
                             site_first, site_second, site_third):
        _browser = current_browser
        self._add_asr_two_sites(current_browser, asr_page, backup_env_type,
                                site_first, site_second)
        self.assertTrue(
            asr_page.lbl_select_second_asr_site.exists(),
            msg=self._formatter(
                '"Select third site" in "Add an ASR" tab does not exist.'))
        logger.info('Trying to select third site: {}'.format(site_third), False,
                    True)
        asr_page.lnk_select_third_asr_site_menu_open.click()
        self.assertTrue(
            asr_page.click_drop_down_list(asr_page.lnk_dropdownlist, 'div',
                                          site_third),
            msg=self._formatter(
                '"{}" not found to be selected as third site.'.format(
                    site_third)))
        LoadingWindow().wait_loading(_browser, 30)

    def _validate_input_args(self, **kwargs):
        if self._testMethodName == self.Func.ADD_ASR:
            self._validate_args_of_add_asr(**kwargs)
        elif self._testMethodName == self.Func.EDIT_ASR:
            self._validate_args_of_edit_asr(**kwargs)
        elif self._testMethodName == self.Func.DELETE_ASR:
            self._validate_args_of_delete_asr(**kwargs)
        else:
            raise ValueError('Unsupported test method.')

    def _validate_args_of_add_asr(self, **kwargs):
        self.backup_env_type = kwargs['backup_env_type']
        self.current_browser = kwargs['current_browser']
        self.description = kwargs['description']
        _sites = kwargs['sites']
        self.site_first = _sites[0]
        self.site_second = _sites[1] if len(_sites) > 1 else ''
        self.site_third = _sites[2] if len(_sites) > 2 else ''
        self.action = 'Add ASR'

    def _validate_args_of_delete_asr(self, **kwargs):
        self.action = 'Delete ASR'
        self.current_browser = kwargs['current_browser']
        self.description = kwargs['description']
        added_asr = kwargs['added_asr']

        self.avamar_site_relationship_name = \
            _generate_asr_full_name(
                added_asr.asr_name, added_asr.backup_env_type, added_asr.sites)

    def _validate_args_of_edit_asr(self, **kwargs):
        self.current_browser = kwargs['current_browser']
        self.description = kwargs['description']
        sites = kwargs['sites']
        self.site_first = sites[0]
        self.site_second = sites[1]
        self.site_third = sites[2]
        self.action = 'Edit ASR'
        added_asr = kwargs['added_asr']
        self.backup_env_type = added_asr.backup_env_type
        self.avamar_site_relationship_name = _generate_asr_full_name(
            added_asr.asr_name, added_asr.backup_env_type, added_asr.sites)
        logger.info('avamar_site_relationship_name: {} is to be edited.'
                    .format(self.avamar_site_relationship_name), False, True)

    def _edit_asr_one_site(self, current_browser, asr_page, site_first):
        _browser = current_browser
        self.assertTrue(asr_page.lbl_tab_edit_asr.exists(),
                        msg=self._formatter(
                            'failed to go to "Edit ASR" tab.'))
        asr_page.lnk_edit_asr_select_asr_site_menu_open.click()
        self.assertTrue(
            asr_page.click_drop_down_list(asr_page.lnk_dropdownlist, 'div',
                                          self.avamar_site_relationship_name,
                                          compare_contains=True),
            msg=self._formatter(
                'failed to select ASR: {} to edit.'.format(
                    self.avamar_site_relationship_name)))
        LoadingWindow().wait_loading(_browser, 30)
        asr_page.wait_for_loading_complete(5)
        logger.info('Trying to select first site: {}'.format(site_first), False,
                    True)
        asr_page.lnk_edit_asr_select_first_asr_site_menu_open.click()
        self.assertTrue(
            asr_page.click_drop_down_list(asr_page.lnk_dropdownlist, 'div',
                                          site_first),
            msg=self._formatter(
                '"{}" not found to be selected as first site.'.format(
                    site_first)))
        LoadingWindow().wait_loading(_browser, timeout=30)

    def _edit_asr_two_sites(self, current_browser, asr_page, site_first, site_second):
        _browser = current_browser
        self._edit_asr_one_site(current_browser, asr_page, site_first)
        logger.info('Trying to select second site: {}'.format(site_second),
                    False, True)
        asr_page.lnk_edit_asr_select_second_asr_site_menu_open.click()
        self.assertTrue(
            asr_page.click_drop_down_list(asr_page.lnk_dropdownlist, 'div', site_second),
            msg=self._formatter('"{}" not found to be selected as second site.'.format(site_second)))
        LoadingWindow().wait_loading(_browser, 30)

    def _edit_asr_three_sites(self, current_browser, asr_page, site_first, site_second, site_third):
        _browser = current_browser
        self._edit_asr_two_sites(current_browser, asr_page, site_first, site_second)
        logger.info('Trying to select third site: {}'.format(site_third),
                    False, True)
        asr_page.lnk_edit_asr_select_third_asr_site_menu_open.click()
        self.assertTrue(
            asr_page.click_drop_down_list(asr_page.lnk_dropdownlist, 'div',
                                          site_third),
            msg=self._formatter(
                '"{}" not found to be selected as third site.'.format(
                    site_third)))
        LoadingWindow().wait_loading(_browser, 30)
