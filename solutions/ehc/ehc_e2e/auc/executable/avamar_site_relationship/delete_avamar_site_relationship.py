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
from ehc_e2e.auc.uimap.shared.requestspage import RequestsPage
from ehc_e2e.auc.uimap.shared.loadingwindow import LoadingWindow
from ehc_e2e.auc.uimap.specific.avamarsiterelationshippage import \
    AvamarSiteRelationshipPage


class DeleteAvamarSiteRelationship(BaseUseCase):
    """
        Test deleting Avamar site relationship.
    """

    deleted_avamar_site_relationship = []
    failure_formatter = ('Running on step:"Delete Avamar Site Relationship"'
                         '-FAILED, {}')
    format_asr_selection_full = '{}-UsedByARR:false'
    delete_succeed = False

    def test_delete_avamar_site_relationship(self):
        catalog_page = CatalogPage()

        self.assertTrue(
            catalog_page.navigate_to_catalog(
                self.current_browser),
            msg=self.failure_formatter.format('switch to catalog page failed.')
        )

        self.assertTrue(catalog_page.lnk_data_protection_services.exists(),
                        msg=self.failure_formatter.format(
                            'cannot find Data Protection Services button in the'
                            ' left pane.'))

        catalog_page.lnk_data_protection_services.click()
        BasePage().wait_for_loading_complete(2)

        self.assertTrue(catalog_page.btn_asr_maintenance_request.exists(),
                        msg=self.failure_formatter.format(
                            'cannot find Avamar Site Relationship (ASR) '
                            'Maintenance card in the right page.'))
        catalog_page.btn_asr_maintenance_request.click()
        logger.info(
            msg='Clicked Avamar Site Relationship (ASR) Maintenance request '
                'button.')
        LoadingWindow().wait_loading(self.current_browser, 30)

        asr_page = AvamarSiteRelationshipPage()

        try:
            # Description tab.
            self.assertTrue(
                asr_page.lbl_description.exists(),
                msg=self.failure_formatter.format(
                    'There is no Description label')
            )
            asr_page.txt_description.set(self.description)
            logger.info(
                msg='Filled in the description: {} for Delete Avamar Site '
                    'Relationship'.format(self.description))
            self.assertTrue(
                asr_page.btn_next.exists(),
                msg=self.failure_formatter.format(
                    'Next button in Description tab does not exist.')
            )
            asr_page.btn_next.click()
            LoadingWindow().wait_loading(self.current_browser, 30)
            logger.debug(
                'Done for description tab, go to "Select an action tab."')

            # Select action tab.
            self.assertTrue(asr_page.lbl_select_action.exists(),
                            msg=self.failure_formatter.format(
                                'failed to go to "select an action" tab.'))
            asr_page.lnk_select_action_menu_open.click()
            self.assertTrue(
                asr_page.click_drop_down_list(
                    asr_page.lnk_dropdownlist,
                    'div',
                    self.action
                ),
                msg=self.failure_formatter.format(
                    'select action {}'.format(self.action)))
            LoadingWindow().wait_loading(self.current_browser, 30)
            logger.info(msg='Selected action {} for Avamar Site Relationship'.format(self.action))
            asr_page.btn_next.click()
            logger.debug(
                'Done for "Select an action" tab, go to "Delete an ASR" tab.')

            # Delete an ASR tab.
            self.assertTrue(
                asr_page.lbl_tab_delete_asr.exists(),
                msg=self.failure_formatter.format(
                    '"Delete ASR" tab does not exist.')
            )

            # In Challenger, we don't have postfix anymore.
            asr_selection_full_name = self.avamar_site_relationship_name
            logger.info('The avamar site relationship selection full name is {}'.format(asr_selection_full_name))

            if asr_page.lnk_select_asr_name_menu_open.exists():
                asr_page.lnk_select_asr_name_menu_open.click()
                # Check to see if the ASR is okay to delete, only those ending
                # with 'false' can be deleted.
                # self.assertTrue(
                #     self._asr_is_deletable(
                #         asr_page.lnk_dropdownlist, asr_selection_full_name),
                #     msg=self.failure_formatter.format(
                #         'the specified ASR: "{}" selection is true, only false can be deleted.'
                #             .format(self.avamar_site_relationship_name)
                #     )
                # )
                self.assertTrue(
                    BasePage().click_drop_down_list(
                        asr_page.lnk_dropdownlist, 'div',
                        asr_selection_full_name),
                    msg=self.failure_formatter.format(
                        'failed to select Avamar Site Relationship: {} to delete.'.format(
                            self.avamar_site_relationship_name))
                )
                LoadingWindow().wait_loading(self.current_browser, 30)
                self.assertTrue(
                    asr_page.btn_confirm_dropdonwlist_open.exists(),
                    self.failure_formatter.format('Open confirm dropdownlist button does not exist.')
                )
                asr_page.btn_confirm_dropdonwlist_open.click()
                self.assertTrue(
                    BasePage().click_drop_down_list(
                        asr_page.lnk_dropdownlist, 'div',
                        'Confirm'
                    ),
                    self.failure_formatter.format('select "Confirm" for delete failed.')
                )
            LoadingWindow().wait_loading(self.current_browser, 30)
            # Submit request.
            asr_page.btn_next.click()
            logger.info(
                'Done for "Delete ASR" tab, clicked next button to go to "Submit request" tab.', False, True)
            if asr_page.btn_submit.exists():
                asr_page.btn_submit.click()

        except AssertionError:
            asr_page.save_request()
            raise
        except:
            logger.error('Delete Avamar Site Relationship encounters error: {}.'
                         .format(sys.exc_info()[:2]))
            asr_page.save_request()
            raise

        self.assertTrue(
            asr_page.lbl_confirmation_success.exists(),
            msg=self.failure_formatter.format(
                'label "The request has been submitted successfully" does not '
                'exist.')
        )

        LoadingWindow().wait_loading(self.current_browser, 30)
        asr_page.btn_ok.click()

        # Go to request.
        logger.info('Navigate to Request frame.')
        self.assertTrue(
            RequestsPage().navigate_to_request(self.current_browser),
            msg=self.failure_formatter.format(' failed to navigate to Request frame.')
        )

        # check the request
        logger.info('Checking Request result')
        self.request_result = RequestsPage().get_request_result(
            self.description)
        self.assertIsNotNone(
            self.request_result,
            msg=self.failure_formatter.format(
                'failed to get the request result.')
        )

    def _asr_is_deletable(self, dropdownlist_element, asr_name):
        # delete ASR selection items: ASR00001-[2C2VC-NewYork-Seattle]-UsedByARR:false
        all_tag_elements = \
            dropdownlist_element.current.find_elements_by_tag_name('div')
        all_asr_full_name_items = (
            [element.text for element in all_tag_elements]
            if all_tag_elements else [])
        for item in all_asr_full_name_items:
            if asr_name in item:
                # Those only ends with 'false' can be deleted.
                if item.endswith('false'):
                    logger.info(
                        'Find {0} corresponding selection {1}, okay to be '
                        'delete.'.format(asr_name, item))
                    return True
                else:
                    logger.info(
                        'Find {0} corresponding selection {1}, but is not '
                        'applicable to delete.'.format(asr_name, item)
                    )

        return False

    def _generate_asr_full_name(self, asr_name, backup_env_type, sites):
        # template is ASR00001-[2C2VC-NewYork-Seattle]
        full_name = asr_name + '-' + \
                    '[' + '-'.join([backup_env_type] + sites) + ']'

        return full_name

    def runTest(self):
        self.test_delete_avamar_site_relationship()

    def _validate_context(self):
        self.request_result = None
        assert self.ctx_in.added_avamar_site_relationship is not None, \
            self.failure_formatter.format('added_avamar_site_relationship should not be None.')
        self.current_browser = self.ctx_in.shared.current_browser
        self.description = 'Delete an ASR test'
        self.action = 'Delete ASR'
        added_asr = self.ctx_in.added_avamar_site_relationship
        self.avamar_site_relationship_name = \
            self._generate_asr_full_name(
                added_asr.asr_name,
                added_asr.backup_env_type,
                added_asr.sites
            )
        assert self.avamar_site_relationship_name is not None, \
            self.failure_formatter.format('added Avamar Site Relationship name should not be None')

    def _finalize_context(self):
        setattr(self.ctx_out, 'deleted_avamar_site_relationship', [])
        if self.request_result:
            if self.request_result.status == 'Successful':
                logger.info(
                    'Delete Avamar Site Relationship: {} request succeeded.'
                    ''.format(self.avamar_site_relationship_name))

                setattr(self.ctx_out, 'deleted_avamar_site_relationship', [self.avamar_site_relationship_name])
            else:
                logger.error(
                    'Delete Avamar Site Relationship: {0} request failed. error '
                    'details: {1}'.format(
                        self.avamar_site_relationship_name,
                        self.request_result.status_details))
                self.fail(msg=self.failure_formatter.format('request result failed.'))
        else:
            logger.error(
                'Delete Avamar Site Relationship: {0} failed, failed to get '
                'request result.'.format(self.avamar_site_relationship_name))
            self.fail(msg=self.failure_formatter.format('the request result from get_request_result is None.'))
