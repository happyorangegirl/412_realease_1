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
from ehc_e2e.auc.rest.get_asr_from_vro import GetASRFromvRO
from ehc_e2e.auc.uimap.shared.basepage import BasePage
from ehc_e2e.auc.uimap.shared.catalogpage import CatalogPage
from ehc_e2e.auc.uimap.shared.loadingwindow import LoadingWindow
from ehc_e2e.auc.uimap.shared.requestspage import RequestsPage
from ehc_e2e.auc.uimap.specific.avamarsiterelationshippage import AvamarSiteRelationshipPage
from .asr_helper import filter_latest_added_asr
from .avamar_site_relationship_Info import AvamarSiteRelationshipInfo
from .asr_constants import (backup_env_type_prefix_single_copy,
                            backup_env_type_prefix_two_copies,
                            backup_env_type_prefix_three_copies)


class EditAvamarSiteRelationship(BaseUseCase):
    """
    Test editing avamar site relationship.
    """

    failed_msg_formatter = 'Running on step:"Edit Avamar Site Relationship" -FAILED, {}'

    def test_edit_avamar_site_relationship(self):
        catalog_page = CatalogPage()

        self.assertTrue(
            catalog_page.navigate_to_catalog(self.current_browser),
            msg=self.failed_msg_formatter.format(
                'switch to catalog page failed.'))

        self.assertTrue(catalog_page.lnk_data_protection_services.exists(),
                        msg=self.failed_msg_formatter.format(
                            'cannot find Data Protection Services button in the'
                            ' left pane.'))

        catalog_page.lnk_data_protection_services.click()
        BasePage().wait_for_loading_complete(2)

        self.assertTrue(catalog_page.btn_asr_maintenance_request.exists(),
                        msg=self.failed_msg_formatter.format(
                            'cannot find Avamar Site Relationship (ASR) '
                            'Maintenance card in the right page.'))
        catalog_page.btn_asr_maintenance_request.click()
        logger.info(
            msg='Clicked Avamar Site Relationship (ASR) Maintenance request '
                'button.')
        LoadingWindow().wait_loading(self.current_browser, 30)

        add_asr_page = AvamarSiteRelationshipPage()

        try:
            # Description tab.
            self.assertTrue(add_asr_page.lbl_description.exists(),
                            msg=self.failed_msg_formatter.format('there is no Description label.'))
            add_asr_page.txt_description.set(self.description)
            logger.info(
                msg='Filled in the description: {} for Edit Avamar Site '
                    'Relationship'.format(self.description))
            add_asr_page.btn_next.click()
            LoadingWindow().wait_loading(self.current_browser, 30)
            logger.debug(
                'Done for description tab, go to "Select an action tab."')

            # Select action tab.
            self.assertTrue(add_asr_page.lbl_select_action.exists(),
                            msg=self.failed_msg_formatter.format(
                                'failed to go to "select an action" tab.'))
            add_asr_page.lnk_select_action_menu_open.click()
            self.assertTrue(add_asr_page.click_drop_down_list(add_asr_page.lnk_dropdownlist, 'div', self.action),
                            msg=self.failed_msg_formatter.format('failed to select action {}'.format(self.action)))
            LoadingWindow().wait_loading(self.current_browser, 30)
            logger.info(
                msg='Selected action {} for Avamar Site Relationship'.format(
                    self.action))
            if add_asr_page.btn_next.exists():
                add_asr_page.btn_next.click()
            logger.info(
                'Done for "Select an action" tab, move to "Edit an ASR" tab.', False, True)

            # Edit an ASR tab.
            if self.backup_env_type.startswith(backup_env_type_prefix_two_copies) or self.backup_env_type == "MC2VC":
                self._add_asr_two_sites(self.current_browser, add_asr_page, self.site_first, self.site_second)
            elif self.backup_env_type.startswith(
                    backup_env_type_prefix_three_copies):
                self._add_asr_three_sites(
                    self.current_browser, add_asr_page, self.site_first,
                    self.site_second, self.site_third
                )
            elif self.backup_env_type.startswith(
                    backup_env_type_prefix_single_copy):
                self._add_asr_one_site(
                    self.current_browser, add_asr_page, self.site_first
                )
            else:
                raise NotImplementedError(
                    '"{}" is not a supported backup environment type.'
                    ''.format(self.backup_env_type))

            # Submit request.
            add_asr_page.btn_next.click()
            logger.debug(
                'Done for "Add an ASR" tab, go to "Submit request" tab.')
            if add_asr_page.btn_submit.exists():
                add_asr_page.btn_submit.click()

        except AssertionError:
            add_asr_page.save_request()
            raise
        except:
            logger.error(
                'Edit Avamar Site Relationship encounters error: {}.'.format(
                    sys.exc_info()[:2]))
            add_asr_page.save_request()
            raise

        self.assertTrue(add_asr_page.lbl_confirmation_success.exists(),
                        msg=self.failed_msg_formatter.format(
                            'label "The request has been submitted successfully" does not exist.'))
        add_asr_page.btn_ok.click()

        # Go to request.
        logger.info('Navigate to Request frame.')
        self.assertTrue(
            RequestsPage().navigate_to_request(self.current_browser),
            msg=self.failed_msg_formatter.format(
                ' failed to navigate to Request frame.'))

        # check the request
        logger.info('Checking Request result')
        self.request_result = RequestsPage().get_request_result(
            self.description)
        self.assertIsNotNone(self.request_result,
                             msg=self.failed_msg_formatter.format('failed to get the request result.'))

        if self.request_result.status == 'Successful':
            logger.info('Add Avamar Site Relationship request succeeded.')
        else:
            logger.error(
                'Add Avamar Site Relationship request failed. error '
                'details: {0}'.format(self.request_result.status_details))
            raise AssertionError(self.failed_msg_formatter.format(
                'Add Avamar Site Relationship request failed.'))

    def _add_asr_one_site(self, current_browser, asr_page,
                          site_first):
        _browser = current_browser
        self.assertTrue(asr_page.lbl_tab_edit_asr.exists(),
                        msg=self.failed_msg_formatter.format(
                            'failed to go to "Edit ASR" tab.'))

        asr_page.lnk_edit_asr_select_asr_site_menu_open.click()
        self.assertTrue(
            asr_page.click_drop_down_list(asr_page.lnk_dropdownlist, 'div',
                                          self.avamar_site_relationship_name,
                                          compare_contains=True),
            msg=self.failed_msg_formatter.format(
                'failed to select ASR: {} to edit.'.format(
                    self.avamar_site_relationship_name)))
        LoadingWindow().wait_loading(_browser, 30)
        asr_page.wait_for_loading_complete(5)

        # self.assertTrue(asr_page.lbl_select_first_asr_site.exists(),
        #                 msg=self.failed_msg_formatter.format(
        #                     '"Select first site" in "Edit an ASR" tab does not '
        #                     'exist.'))
        logger.info('Trying to select first site: {}'.format(site_first), False,
                    True)
        asr_page.lnk_edit_asr_select_first_asr_site_menu_open.click()
        self.assertTrue(
            asr_page.click_drop_down_list(asr_page.lnk_dropdownlist, 'div',
                                          site_first),
            msg=self.failed_msg_formatter.format(
                '"{}" not found to be selected as first site.'.format(
                    site_first)))
        LoadingWindow().wait_loading(_browser, timeout=30)

    def _add_asr_two_sites(self, current_browser, asr_page,
                           site_first, site_second):
        _browser = current_browser
        self._add_asr_one_site(current_browser, asr_page,
                               site_first)
        # self.assertTrue(asr_page.lbl_select_second_asr_site.exists(),
        #                 msg=self.failed_msg_formatter.format(
        #                     '"Select second site" in "Edit an ASR" tab does not '
        #                     'exist.'))
        logger.info('Trying to select second site: {}'.format(site_second),
                    False, True)
        asr_page.lnk_edit_asr_select_second_asr_site_menu_open.click()
        self.assertTrue(
            asr_page.click_drop_down_list(asr_page.lnk_dropdownlist, 'div', site_second),
            msg=self.failed_msg_formatter.format('"{}" not found to be selected as second site.'.
                                                 format(site_second)))
        LoadingWindow().wait_loading(_browser, 30)

    def _add_asr_three_sites(self, current_browser, asr_page,
                             site_first, site_second, site_third):
        _browser = current_browser
        self._add_asr_two_sites(current_browser, asr_page,
                                site_first, site_second)

        # self.assertTrue(asr_page.lbl_select_second_asr_site.exists(),
        #     msg=self.failed_msg_formatter.format(
        #         '"Select third site" in "Edit an ASR" tab does not exist.'))
        logger.info('Trying to select third site: {}'.format(site_third),
                    False, True)
        asr_page.lnk_edit_asr_select_third_asr_site_menu_open.click()
        self.assertTrue(
            asr_page.click_drop_down_list(asr_page.lnk_dropdownlist, 'div',
                                          site_third),
            msg=self.failed_msg_formatter.format(
                '"{}" not found to be selected as third site.'.format(
                    site_third)))
        LoadingWindow().wait_loading(_browser, 30)

    def _generate_asr_full_name(self, asr_name, backup_env_type, sites):
        # template is ASR00001-[2C2VC-NewYork-Seattle]-UsedByARRorCluster
        full_name = asr_name + '-' + '[' + '-'.join(
            [backup_env_type] + sites) + ']'

        return full_name

    def runTest(self):
        self.test_edit_avamar_site_relationship()

    def _validate_context(self):
        self.request_result = None
        self.site_first = ''
        self.site_second = ''
        self.site_third = ''

        assert self.ctx_in.added_avamar_site_relationship is not None, \
            self.failed_msg_formatter.format('added_avamar_site_relationship should not be None.')
        assert self.ctx_in.edit_avamar_site_relationship.site_first is not None, \
            self.failed_msg_formatter.format('site_first should not be None.')
        assert self.ctx_in.edit_avamar_site_relationship.site_second is not None, \
            self.failed_msg_formatter.format('site_second should not be None.')
        assert self.ctx_in.edit_avamar_site_relationship.site_third is not None, \
            self.failed_msg_formatter.format('site_third should not be None.')
        self.site_first = self.ctx_in.edit_avamar_site_relationship.site_first
        self.site_second = self.ctx_in.edit_avamar_site_relationship.site_second
        self.site_third = self.ctx_in.edit_avamar_site_relationship.site_third
        self.current_browser = self.ctx_in.shared.current_browser
        self.description = 'Edit an ASR test'
        self.action = 'Edit ASR'
        self.vro = self.ctx_in.vro
        logger.info('site_first:{0}, site_second:{1}, site_third:{2}'.format(self.site_first, self.site_second,
                                                                             self.site_third))
        added_asr = self.ctx_in.added_avamar_site_relationship
        self.backup_env_type = added_asr.backup_env_type
        logger.info('added ASR: {}'.format(added_asr), False, True)
        self.avamar_site_relationship_name = self._generate_asr_full_name(
            added_asr.asr_name, added_asr.backup_env_type, added_asr.sites)
        logger.info('avamar_site_relationship_name:{}'.format(self.avamar_site_relationship_name), False, True)
        assert self.avamar_site_relationship_name is not None, \
            self.failed_msg_formatter.format('Avamar Site Relationship name should not be None')

    def _finalize_context(self):
        added_asr_obj = None
        list_asr = GetASRFromvRO().get_asr_from_vro(self.ctx_in.vro)
        if not list_asr:
            logger.warn(
                'No ASR information retrieved from vRO, will not update '
                'added_avamar_site_relationship as such.')
        else:
            for item in list_asr:
                logger.debug('list_asr: {}'.format(item), False)
            self.assertIsNotNone(list_asr, self.failed_msg_formatter.format(
                'ASR get from VRO is None.'))
            asr_name = filter_latest_added_asr(list_asr, self.backup_env_type, self.site_first,
                                               self.site_second, self.site_third)
            assert asr_name is not None, \
                self.failed_msg_formatter.format('Retrieving ASR name from vRO:{} failed'.format(self.vro.address))
            added_asr_obj = AvamarSiteRelationshipInfo(asr_name, self.backup_env_type, self.site_first,
                                                       self.site_second, self.site_third)
            logger.info('edited avamar_site_relationship: {} .'
                        ''.format(added_asr_obj), False, True)

        setattr(self.ctx_out, 'added_avamar_site_relationship', added_asr_obj)
