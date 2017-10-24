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
from ehc_e2e.auc.uimap.specific import ClusterMaintenancePage
from ehc_e2e.auc.uimap.shared import RequestsPage
from ehc_e2e.auc.uimap.shared import CatalogPage
from ehc_e2e.auc.uimap.shared import LoadingWindow


class AssociateAvamarProxiesWithCluster(BaseUseCase):
    """As a Service Architect, I need to associated avamar proxies to target cluster.
    Preconditions:
    1. Import newest foundation package and run workflow "Initialization EHC Foundation"
    successfully under vRO path "EHC->Foundation".
    2. Import newest DP package and run workflow "Initialization EHC DP" successfully
    under vRO path "EHC->Data Protection".
    3. Target ASR/ARR should be created.
    4. Target cluster should be onboarded.
    Relationship between cluster type and backup type.
    LC1S cluster - 1C1VC backup type
    CA1S cluster - 2C1VC backup type
    CA2S cluster - 2C1VC backup type
    DR2S cluster - 2C2VC backup type
    MP2S cluster - 3C2VC backup type
    MP3S cluster - 3C2VC backup type
    5. AUC-66 Associate cluster to ASR has been executed.

    Returns: None

    """
    associated_result_list = []
    _formatter = '"Running on step: Associate Avamar Proxies to Cluster" - FAILED, {step}'

    def test_associate_avamar_proxies_with_cluster(self):
        """UI operations for associating avamar proxies with cluster.

        """

        logger.info('Associate avamar proxies with cluster.')
        associate_result = {}

        # Navigate to catalog page
        self.loading_window = LoadingWindow()
        self.catalog_page = CatalogPage()
        self.assertTrue(self.catalog_page.navigate_to_catalog(self.current_browser),
                        msg=self._formatter.format(step='switch to catalog frame'))
        self.catalog_page.lnk_ehc_configuration.click()
        self.catalog_page.btn_cluster_maintenance_request.click()
        self.loading_window.wait_loading(self.current_browser, 30)
        logger.info('Navigated to catalog page')
        self.loading_window.wait_loading2(self.current_browser, 240)

        try:
            # Fill in description and reasons
            self.assertTrue(self.associate_avamar_proxies_with_cluster_page.txt_description.exists(),
                            msg=self._formatter.format(step='Try to fill in operation description'))
            self.associate_avamar_proxies_with_cluster_page.txt_description.set(self.description)
            logger.info('Fill in operation description {}'.format(self.description))
            self.assertTrue(self.associate_avamar_proxies_with_cluster_page.txt_reason.exists(),
                            msg=self._formatter.format(step='Try to fill in operation reason'))
            self.associate_avamar_proxies_with_cluster_page.txt_reason.set(self.reasons)
            logger.info('Filled in operation reason {}'.format(self.reasons))
            self.assertTrue(
                self.associate_avamar_proxies_with_cluster_page.btn_next.exists(),
                msg=self._formatter.format(step='Try to find next button'))
            self.associate_avamar_proxies_with_cluster_page.btn_next.click()

            # select "Associate Avamar Proxies with Cluster"
            self.assertTrue(
                self.associate_avamar_proxies_with_cluster_page.btn_cluster_action.exists(),
                msg=self._formatter.format(step='Try to select "Associate Avamar Proxies with Cluster"'))
            self.associate_avamar_proxies_with_cluster_page.btn_cluster_action.click()
            _click_result = self.associate_avamar_proxies_with_cluster_page.click_drop_down_list(
                self.associate_avamar_proxies_with_cluster_page.lst_action_values,
                'tr',
                self.cluster_action
            )
            self.assertTrue(
                _click_result,
                msg=self._formatter.format(step='Try to select "Associate Avamar Proxies with Cluster"')
            )

            logger.info('Selected action {} to perform'.format(self.cluster_action))
            self.loading_window.wait_loading(self.current_browser, 30)
            self.assertTrue(
                self.associate_avamar_proxies_with_cluster_page.btn_next.exists(),
                msg=self._formatter.format(step='Try to find "next" button')
            )

            self.associate_avamar_proxies_with_cluster_page.send_tab_key(
                self.associate_avamar_proxies_with_cluster_page.btn_next)

            self.associate_avamar_proxies_with_cluster_page.btn_next.click()
            self.associate_avamar_proxies_with_cluster_page.wait_for_loading_complete()

            # Select cluster name and proxies name
            self.assertTrue(
                self.associate_avamar_proxies_with_cluster_page.btn_select_cluster_to_avamar.exists(),
                msg=self._formatter.format(step='Try to select the specific cluster to associate')
            )
            self.associate_avamar_proxies_with_cluster_page.btn_select_cluster_to_avamar.click()
            _click_result = self.associate_avamar_proxies_with_cluster_page.click_drop_down_list(
                self.associate_avamar_proxies_with_cluster_page.lst_action_values,
                'tr',
                self.cluster)
            self.assertTrue(_click_result,
                            msg=self._formatter.format(step='Try to select cluster name to associate'))
            logger.info('Select cluster {} to perform'.format(self.cluster))
            self.loading_window.wait_loading(self.current_browser, 30)

            # Avamar proxies
            self.assertTrue(
                self.associate_avamar_proxies_with_cluster_page.tbl_select_avamar_proxies.exists(),
                msg=self._formatter.format(step='Try to find avamar proxies content')
            )

            all_avamar_proxies_elements = \
                self.associate_avamar_proxies_with_cluster_page.tbl_select_avamar_proxies \
                    .current.find_elements_by_tag_name('tr')
            self.assertIsNotNone(all_avamar_proxies_elements,
                                 msg='Can not find avamar proxies')
            if self.select_all_proxies:
                # select all proxies
                logger.info('Select all proxies', False, True)
                for proxy_element in all_avamar_proxies_elements:
                    proxy_checkbox = proxy_element.find_element_by_tag_name('input')
                    proxy_label = proxy_element.find_element_by_tag_name('label')
                    self.assertIsNotNone(proxy_checkbox,
                                         msg=self._formatter.format(
                                             step="Can't find avamar proxy checkbox."
                                         ))
                    self.assertIsNotNone(proxy_label,
                                         msg=self._formatter.format(
                                             step="Can't find avamar proxy contents."
                                         ))
                    self.assertTrue(proxy_label.text != 'Proxies are not found.',
                                    msg=self._formatter.format(
                                        step="Proxies are not found."
                                    ))
                    if not proxy_checkbox.is_selected():
                        proxy_checkbox.click()

            else:
                if len(self.avamar_proxies_list) == 0:
                    logger.info('Select the first one proxy.', False, True)
                    # Select the first one
                    for index, proxy_element in enumerate(all_avamar_proxies_elements):
                        proxy_checkbox = proxy_element.find_element_by_tag_name('input')
                        proxy_label = proxy_element.find_element_by_tag_name('label')
                        self.assertIsNotNone(proxy_checkbox,
                                             msg=self._formatter.format(
                                                 step="Can't find avamar proxy checkbox."
                                             ))
                        self.assertIsNotNone(proxy_label,
                                             msg=self._formatter.format(
                                                 step="Can't find avamar proxy contents."
                                             ))
                        self.assertTrue(proxy_label.text != 'Proxies are not found.',
                                        msg=self._formatter.format(
                                            step="Proxies are not found."
                                        ))
                        if index == 0:
                            if proxy_checkbox.is_selected():
                                continue
                            else:
                                proxy_checkbox.click()
                        else:
                            if proxy_checkbox.is_selected():
                                proxy_checkbox.click()
                            else:
                                continue
                else:
                    logger.info('Select customer provided avamar proxies', False, True)
                    # Select customer provided avamar proxies
                    for avamar_proxy in self.avamar_proxies_list:
                        avamar_proxy_found = False
                        for index, proxy_element in enumerate(all_avamar_proxies_elements):
                            proxy_checkbox = proxy_element.find_element_by_tag_name('input')
                            proxy_label = proxy_element.find_element_by_tag_name('label')
                            self.assertIsNotNone(proxy_checkbox,
                                                 msg="Can't find avamar proxy checkbox.")
                            self.assertIsNotNone(proxy_label,
                                                 msg="Can't find avamar proxy contents.")
                            self.assertTrue(proxy_label.text != 'Proxies are not found.',
                                            msg=self._formatter.format(
                                                step="Proxies are not found."))
                            # Select proxies indicated in self.avamar_proxies_list, un select those are not
                            if proxy_label.text in avamar_proxy:
                                avamar_proxy_found = True
                                if proxy_checkbox.is_selected():
                                    continue
                                else:
                                    proxy_checkbox.click()
                            else:

                                if proxy_checkbox.is_selected():
                                    proxy_checkbox.click()
                                else:
                                    continue
                        self.assertTrue(avamar_proxy_found,
                                        msg=self._formatter.format(
                                            step='Try to find avamar proxy {} '
                                                 'in "Registered Proxy list"'.format(avamar_proxy)))

            self.loading_window.wait_loading(self.current_browser, 30)
            self.associate_avamar_proxies_with_cluster_page.btn_next.click()

            # Review cluster action and cluster name
            self.assertTrue(
                self.cluster_action in
                self.associate_avamar_proxies_with_cluster_page.lbl_review_chosen_action.value,
                msg=self._formatter.format(step='Try to review "Associate avamar proxies with cluster" action'))
            self.assertTrue(
                self.cluster in
                self.associate_avamar_proxies_with_cluster_page.lbl_review_cluster_name.value,
                msg=self._formatter.format(step='Try to review "Cluster Name"'))
            logger.info('Reviewed cluster action and cluster name')
            # Submit the requests
            self.assertTrue(
                self.associate_avamar_proxies_with_cluster_page.btn_submit.exists(),
                msg=self._formatter.format(step='Try to find the submit button'))
            self.associate_avamar_proxies_with_cluster_page.btn_submit.click()

        except AssertionError:
            self.associate_avamar_proxies_with_cluster_page.save_request()
            raise
        except:
            self.associate_avamar_proxies_with_cluster_page.save_request()
            logger.error('"Associate Avamar Proxies with Cluster" encounters an error, more info: {}'
                         .format(sys.exc_info()[:2]))
            raise

        request_status = ''
        try:
            self.assertTrue(
                self.associate_avamar_proxies_with_cluster_page.btn_ok.exists(),
                msg=self._formatter.format(step='Find the OK button'))
            self.associate_avamar_proxies_with_cluster_page.btn_ok.click()

            # Switch to request page to check the association result.
            logger.info('Switched to request page to check the association result')
            self.assertTrue(
                RequestsPage().navigate_to_request(self.current_browser),
                msg=self._formatter.format(step='Try to switch to request page.')
            )
            request_result = RequestsPage().get_request_result(self.description)
            self.assertIsNotNone(
                request_result,
                msg=self._formatter.format(step='Try to get request result of {}'.format(self.description)))
            associate_result.update(
                cluster_name=self.cluster,
                avamar_proxies_list=self.avamar_proxies_list,
                status=request_result.status,
                status_details=request_result.status_details)
            self.associated_result_list.append(associate_result)
            request_status = request_result.status
        except AssertionError:
            self.catalog_page.navigate_to_catalog(self.current_browser)
            request_status = 'Fail'
        except:
            self.catalog_page.navigate_to_catalog(self.current_browser)
            logger.error('"Associate avamar proxies with cluster" encounters an error, more info: {}'
                         .format(sys.exc_info()[:2]))
            request_status = 'Fail'
        return request_status

    def runTest(self):
        """Parse custom input data and run the test

        Returns:

        """
        self.existed_clusters = self.ctx_in.existed_clusters
        request_status = 'Successful'
        for index, item in enumerate(self.cluster_avamar_proxies):
            # Associate according to existed_clusters
            if index >= len(self.ctx_in.existed_clusters) or request_status != 'Successful':
                break
            self.associate_avamar_proxies_with_cluster_page = ClusterMaintenancePage()
            timestamp = self.associate_avamar_proxies_with_cluster_page.make_timestamp()
            self.description = 'associate avamar proxies with cluster' + '' + timestamp
            self.reasons = 'testing'
            self.cluster_action = 'Associate Avamar Proxies with Cluster'
            self.cluster = self.existed_clusters[index]
            self.select_all_proxies = getattr(item, 'select_all_proxies', False)
            if item.avamar_proxies is not None:
                self.avamar_proxies_list = item.avamar_proxies
            request_status = self.test_associate_avamar_proxies_with_cluster()

    def _validate_context(self):
        """Input configuration validation check.
        """

        if self.ctx_in:
            self.assertTrue(
                self.ctx_in.shared.current_browser.is_login,
                msg='Please login to vRA.'
            )
            self.current_browser = self.ctx_in.shared.current_browser
            self.onboard_cluster_type = self.ctx_in.onboard_cluster_type
            self.assertIsNotNone(self.onboard_cluster_type,
                                 msg="Onboard cluster is not provided.")
            self.cluster_avamar_proxies = self.ctx_in.avamar_proxies_cluster_to_associate
            self.assertTrue(isinstance(self.cluster_avamar_proxies, list),
                            msg='Avamar proxies is not list type.')
            self.assertTrue(
                len(self.cluster_avamar_proxies) > 0,
                msg="yaml data of associate avamar proxies with cluster is not provided."
            )
            self.assertTrue(isinstance(self.ctx_in.existed_clusters, list),
                            msg='Existed clusters is not list type.')
            self.assertTrue(len(self.ctx_in.existed_clusters) > 0,
                            msg='Cluster name is not provided.')

    def _finalize_context(self):
        """

        Returns:

        """
        association_success = True
        associated_avamar_proxy_cluster_list = []
        self.assertTrue(self.catalog_page.navigate_to_catalog(self.current_browser),
                        msg=self._formatter.format(step='Switch back to catalog frame'))
        if len(self.associated_result_list) > 0:
            for association_item in self.associated_result_list:
                cluster_name = association_item['cluster_name']
                avamar_proxies_list = "".join(association_item['avamar_proxies_list'])
                status = association_item['status']
                status_details = association_item['status_details']
                more_details = "{" + cluster_name + ", " + \
                               avamar_proxies_list + ", " + \
                               status + ", " + \
                               status_details + "}"
                if status == 'Successful':
                    logger.info(
                        msg=('Associate Avamar proxy with cluster: {0} successfully, for more details: {1}'
                             .format(cluster_name, more_details)))
                    associated_avamar_proxy_cluster_dict = {}
                    associated_avamar_proxy_cluster_dict.setdefault(cluster_name, avamar_proxies_list)
                    associated_avamar_proxy_cluster_list.append(associated_avamar_proxy_cluster_dict)
                else:
                    association_success = False
                    logger.error(
                        'Failed to associate Avamar proxy with cluster: {0}, for more detailed: {1}'.
                        format(cluster_name, more_details))
        else:
            association_success = False
        setattr(self.ctx_out, 'associated_avamar_proxy_cluster', associated_avamar_proxy_cluster_list)
        self.assertTrue(association_success,
                        msg='Running on step: "Associate Avamar proxies with Cluster"-FAILED.')
