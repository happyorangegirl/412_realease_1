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
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared import CatalogPage, LoadingWindow
from ehc_e2e.auc.uimap.specific import ProvisionCloudStoragePage


class ProvisionCloudStorage(BaseUseCase):
    REQUEST_SUCCESSFUL = 'Successful'
    _formatter = 'Running on step:"Provision cloud storage"- FAILED, {}.'

    def test_provision_cloud_storage(self):
        loading_window = LoadingWindow()

        catalog_page = CatalogPage()
        self.assertTrue(
            catalog_page.navigate_to_catalog(self.current_browser),
            self._formatter.format('failed to navigate to catalog page.'))
        provision_cloud_storage_page = ProvisionCloudStoragePage()
        # This loop check was added if the "Cloud admin" button does not exists
        if not catalog_page.btn_cloud_storage.exists() and catalog_page.btn_provision_cloud_storage_request.exists():
            logger.debug('"Cloud Storage" button does not exists. Clicking "Provision Cloud Storage" as it exists')
            catalog_page.btn_provision_cloud_storage_request.click()
            loading_window.wait_loading2(self.current_browser, 180)
        else:
            self.assertTrue(
                catalog_page.btn_cloud_storage.exists(),
                self._formatter.format('"Cloud Storage" button does not exist in catalog page.'))
            # click Provision Cloud Storage request in catalog page.
            catalog_page.btn_cloud_storage.click()
            self.assertTrue(
                catalog_page.btn_provision_cloud_storage_request.exists(),
                self._formatter.format('"Provision Cloud Storage" button does not exist.'))
            catalog_page.btn_provision_cloud_storage_request.click()
            loading_window.wait_loading2(self.current_browser, 180)

        try:
            # input description.
            self.assertTrue(provision_cloud_storage_page.txt_description.exists(),
                            self._formatter.format('description textbox does not exist.'))
            provision_cloud_storage_page.txt_description.set(self.description)

            # reason is not mandatory, so just set it if it exists.
            if provision_cloud_storage_page.txt_reasons.exists():
                provision_cloud_storage_page.txt_reasons.set(self.description)
            provision_cloud_storage_page.btn_next.click()
            logger.info('Request information filled out. Going to the next tab', False, True)

            # input password.
            self.assertTrue(provision_cloud_storage_page.txt_password.exists(),
                            self._formatter.format('Authentication tab "password" textbox does not exist.'))
            provision_cloud_storage_page.txt_password.set(self.password)
            provision_cloud_storage_page.btn_next.click()
            loading_window.wait_loading(self.current_browser, 30)
            logger.info('Authentication information filled out. Going to the next tab', False, True)

            # choose cluster name.
            self.assertTrue(
                provision_cloud_storage_page.btn_choose_cluster_name.exists(),
                self._formatter.format('vCenter cluster drop down list does not exist.'))
            provision_cloud_storage_page.btn_choose_cluster_name.click()
            self.assertTrue(
                provision_cloud_storage_page.click_drop_down_list(
                    provision_cloud_storage_page.lnk_dropdownlist_menu, 'div', self.cluster_name),
                self._formatter.format(
                    'failed to select vCenter cluster: {}.'.format(self.cluster_name)))
            logger.info('vCenter cluster: {} is selected.'.format(self.cluster_name), False, True)
            loading_window.wait_loading(self.current_browser, 30)
            provision_cloud_storage_page.btn_next.click()
            loading_window.wait_loading(self.current_browser, 30)

            # select HWI.
            self.assertTrue(provision_cloud_storage_page.btn_select_hwi_name.exists(),
                            self._formatter.format('Hardware Island drop down list open button does not exist'))
            provision_cloud_storage_page.btn_select_hwi_name.click()
            self.assertTrue(
                provision_cloud_storage_page.click_drop_down_list(
                    provision_cloud_storage_page.lnk_dropdownlist_menu, 'div', self.hwi_name),
                self._formatter.format('failed to select Hardware Island: {}'.format(self.hwi_name)))
            logger.info('Hardware Island : {} is selected.'.format(self.hwi_name), False, True)
            loading_window.wait_loading(self.current_browser, 30)
            provision_cloud_storage_page.btn_next.click()
            loading_window.wait_loading(self.current_browser, 30)

            # select Datastore type.
            self.assertTrue(
                provision_cloud_storage_page.btn_choose_storage_type.exists(),
                self._formatter.format('Datastore type drop down list open button does not exist.'))
            loading_window.wait_loading(self.current_browser, 30)
            provision_cloud_storage_page.btn_choose_storage_type.click()
            self.assertTrue(
                provision_cloud_storage_page.click_drop_down_list(
                    provision_cloud_storage_page.lnk_dropdownlist_menu, 'div', self.storage_type),
                self._formatter.format(
                    'failed to select Datastore type: {}.'.format(self.storage_type)))
            logger.info('Datastore type: {} is selected.'.format(self.storage_type), False, True)
            loading_window.wait_loading(self.current_browser, 30)
            provision_cloud_storage_page.btn_next.click()
            loading_window.wait_loading(self.current_browser, 30)

            # select Storage Tier.
            self.assertTrue(provision_cloud_storage_page.btn_choose_vipr_storage_tier.exists(),
                            self._formatter.format('Storage Tier drop down list open button does not exist.'))
            provision_cloud_storage_page.btn_choose_vipr_storage_tier.click()
            storage_tier_selected = provision_cloud_storage_page.select_drop_down_list_filter_undefined_by_index(
                provision_cloud_storage_page.lnk_dropdownlist_menu, 'div', self.vipr_storage_tier)
            self.assertIsNotNone(storage_tier_selected, self._formatter.format(
                'failed to select VIPR storage tier: {}.'.format(self.vipr_storage_tier)))
            logger.info('VIPR storage tier: {} is selected.'.format(self.vipr_storage_tier), False,
                        True)
            loading_window.wait_loading(self.current_browser, 30)
            provision_cloud_storage_page.btn_next.click()
            loading_window.wait_loading(self.current_browser, 30)

            # specify Datastore Size.
            self.assertTrue(provision_cloud_storage_page.txt_size_in_gb.exists(),
                            self._formatter.format('Datastore Size text box does not exist.'))
            provision_cloud_storage_page.txt_size_in_gb.set(self.size_in_gb)
            logger.info('Datastore Size is filled with :{}'.format(self.size_in_gb), False, True)
            provision_cloud_storage_page.btn_next.click()
            loading_window.wait_loading(self.current_browser, 30)

            # Submit request.
            provision_cloud_storage_page.btn_submit.click()
            logger.info('Clicked submit button.', False, True)
            loading_window.wait_loading(self.current_browser, 30)
            self.assertTrue(provision_cloud_storage_page.lbl_confirmation_success.exists(),
                            self._formatter.format('label: "confirm information in Review and Submit, '
                                                   'click submit button" does not exist'))
            provision_cloud_storage_page.btn_ok.click()
            logger.info('Clicked ok button in confirm success page.', False, True)
        except AssertionError:
            provision_cloud_storage_page.save_request()
            raise
        except:
            logger.error('Provision cloud storage encounters error: {}.'
                         .format(sys.exc_info()))
            provision_cloud_storage_page.save_request()
            raise

    def runTest(self):
        self.test_provision_cloud_storage()

    def _validate_input_args(self, **kwargs):
        self.current_browser = kwargs["current_browser"]
        self.description = kwargs["description"]
        self.hwi_name = kwargs["hwi_name"]
        self.storage_type = kwargs["storage_type"]
        self.vipr_storage_tier = kwargs["vipr_storage_tier"]
        self.size_in_gb = kwargs["size_in_gb"]
        self.password = kwargs["password"]
        self.cluster_name = kwargs["cluster_name"]
        self.vro = kwargs["vro"]

    def _finalize_output_params(self):
        pass
