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
from ehc_e2e.auc.uimap.shared import CatalogPage
from ehc_e2e.auc.uimap.specific import OnboardClusterPage
from ehc_e2e.auc.uimap.shared.loadingwindow import LoadingWindow
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from .context_onboard_cluster_manager import Context_Onboard_DR_Cluster
from .context_onboard_cluster_manager import Context_Onboard_Local_Cluster
from .context_onboard_cluster_manager import Context_Onboard_Vsan_Cluster
from .context_onboard_cluster_manager import Context_Onboard_CA_Cluster
from .context_onboard_cluster_manager import Context_Onboard_MP_Cluster


class ClusterManager(BaseUseCase):
    class Func(object):
        ONBOARD_CLUSTER, \
        DELETE_CLUSTER, \
        EDIT_CLUSTER_SITE, \
        EDIT_CLUSTER_HWI, \
        ASSOCIATE_CLUSTER_TO_ASR = (
            'test_onboard_cluster',
            'test_delete_cluster',
            'test_edit_cluster_site',
            'test_edit_cluster_hwi',
            'test_associate_cluster_to_asr'
        )

    def __init__(self, name=None, method_name=Func.ONBOARD_CLUSTER, **kwargs):
        super(ClusterManager, self).__init__(
            name, method_name, **kwargs)
        self._request_result = None
        self._onboard_cluster = OnboardClusterPage()
        self._catalog_page = CatalogPage()
        self._loading_window = LoadingWindow()
        _auc_name = ' '.join([word.capitalize() for word in name.split('_')])
        self._step_failed_msg = ('Running on: ' + _auc_name + ' - FAILED, "{step}"').format

    def _validate_input_args(self, **kwargs):
        if self._testMethodName == self.Func.ONBOARD_CLUSTER:
            self._validate_args_of_onboard_cluster()
        elif self._testMethodName == self.Func.DELETE_CLUSTER:
            self._validate_args_of_delete_cluster()
        elif self._testMethodName == self.Func.EDIT_CLUSTER_SITE:
            self._validate_args_of_edit_cluster_site()
        elif self._testMethodName == self.Func.EDIT_CLUSTER_HWI:
            self._validate_args_of_edit_cluster_hwi()
        elif self._testMethodName == self.Func.ASSOCIATE_CLUSTER_TO_ASR:
            self._validate_args_of_associate_cluster_to_asr()
        else:
            raise ValueError('Unsupported test method.')
        # According to method name or onboard cluster type to get the AUC action choice.
        self._get_action_chosen()

    def _validate_args_of_onboard_cluster(self):
        self._onboard_cluster_entity = None
        __get_onboard_cluster_entity = {
            'LC1S': Context_Onboard_Local_Cluster().get_entity,
            'VS1S': Context_Onboard_Vsan_Cluster().get_entity,
            'DR2S': Context_Onboard_DR_Cluster().get_entity,
            'CA1S': Context_Onboard_CA_Cluster().get_entity,
            'CA2S': Context_Onboard_CA_Cluster().get_entity,
            'MP2S': Context_Onboard_MP_Cluster().get_entity,
            'MP3S': Context_Onboard_MP_Cluster().get_entity
        }
        self._current_browser = self._kwargs.get('current_browser')
        self._onboard_cluster_type = self._kwargs.get('onboard_cluster_type')
        action = self._kwargs.get('action')
        self.added_hwi = self._kwargs.get('added_hwi')
        self._onboard_cluster_entity = __get_onboard_cluster_entity.get(self._onboard_cluster_type)(action,
                                                                                                    self.added_hwi)

    def _validate_args_of_delete_cluster(self):
        self._current_browser = self._kwargs.get('current_browser')
        self._cluster_to_cluster = self._kwargs.get('delete_cluster')
        self._confirm = 'Confirm'

    def _validate_args_of_edit_cluster_site(self):
        self._current_browser = self._kwargs.get('current_browser')
        edit_cluster = self._kwargs.get('edit_cluster_site')

        self.cluster_to_edit = edit_cluster.cluster
        self.site_to_edit = edit_cluster.site
        self.hwi_to_edit = edit_cluster.hwi

        self.assertIsNotNone(self.cluster_to_edit, 'Please provide value of item: cluster.')
        self.assertIsNotNone(self.site_to_edit, 'Please provide value of item: site.')
        self.assertIsNotNone(self.hwi_to_edit, 'Please provide value of item: hwi.')

    def _validate_args_of_edit_cluster_hwi(self):
        self._current_browser = self._kwargs.get('current_browser')
        edit_cluster = self._kwargs.get('edit_cluster_hwi')

        self.cluster_to_edit = edit_cluster.cluster
        self.hwi_1_to_edit = edit_cluster.hwi_1
        self.hwi_2_to_edit = edit_cluster.hwi_2

        self.assertIsNotNone(self.cluster_to_edit,
                             self._step_failed_msg(step='please provide value of item: cluster.'))
        self.assertIsNotNone(self.hwi_1_to_edit, self._step_failed_msg(
            step='please provide the first hwi for cluster in YAML item: hwi_1.'))

    def _validate_args_of_associate_cluster_to_asr(self):
        self._current_browser = self._kwargs.get('current_browser')
        self.asr = self._kwargs.get('asr')
        self.clusters = self._kwargs.get('cluster')

        self.assertTrue(self.clusters > 0,
                            msg='Cluster name is not provided.')

        self.assertIsNotNone(self.asr[0].asr_name,
                             msg='ASR short name is not provided.')
        self.assertIsNotNone(self.asr[0].backup_env_type,
                             msg='Backup service level is not provided.')
        self.assertTrue(isinstance(self.asr[0].sites, list),
                        msg='Sites in added avamar site relationship is not list type.')
        self.assertTrue(len(self.asr[0].sites) > 0,
                        msg='yaml data of site in avamar site relationship is not provided')

    def _finalize_context(self):
        if self._testMethodName == self.Func.ONBOARD_CLUSTER:
            self._output.append(self._onboard_cluster_entity)

    def test_onboard_cluster(self):
        __onboar_cluster = {
            'LC1S': self._onboard_local_cluster,
            'VS1S': self._onboard_vsan_cluster,
            'DR2S': self._onboard_dr_cluster,
            'CA1S': self._onboard_ca_cluster,
            'CA2S': self._onboard_ca_cluster,
            'MP2S': self._onboard_mp_cluster,
            'MP3S': self._onboard_mp_cluster
        }
        self._start_new_service_request()
        try:
            self._fill_out_request_info()
            self._fill_out_action_info()
            __onboar_cluster.get(self._onboard_cluster_type)()
            self._confirm_info_in_review()
        except AssertionError:
            self._handle_assert_exception()
        except:
            ex = sys.exc_info()
            self._handle_other_exception(ex)

        self._submit_request()

    def test_delete_cluster(self):
        self._start_new_service_request()
        try:
            self._fill_out_request_info()
            self._fill_out_action_info()
            self._delete_cluster()
            self._confirm_info_in_review()
        except AssertionError:
            self._handle_assert_exception()
            raise
        except:
            ex = sys.exc_info()
            self._handle_other_exception(ex)

        self._submit_request()

    def test_edit_cluster_site(self):
        self._start_new_service_request()
        try:
            self._fill_out_request_info()
            self._fill_out_action_info()
            self._edit_cluster_site()
            self._confirm_info_in_review()
        except AssertionError:
            self._handle_assert_exception()
        except:
            ex = sys.exc_info()
            self._handle_other_exception(ex)

        self._submit_request()

    def test_edit_cluster_hwi(self):
        self._start_new_service_request()
        try:
            self._fill_out_request_info()
            self._fill_out_action_info()
            self._edit_cluster_hwi()
            self._confirm_info_in_review()
        except AssertionError:
            self._handle_assert_exception()
        except:
            ex = sys.exc_info()
            self._handle_other_exception(ex)

        self._submit_request()

    def test_associate_cluster_to_asr(self):
        self._start_new_service_request()
        try:
            self._fill_out_request_info()
            self._fill_out_action_info()
            self._associate_cluster_to_asr()
            self._confirm_info_in_review()
        except AssertionError:
            self._handle_assert_exception()
        except:
            ex = sys.exc_info()
            self._handle_other_exception(ex)

        self._submit_request()

    def _associate_cluster_to_asr(self):
        self.cluster_name = self.clusters[0]
        self.asr_name = ''
        self.asr_name = self.asr[0].asr_name + ' ' + \
                        self.asr[0].backup_env_type + '-'
        for index, item in enumerate(self.asr[0].sites):
            self.asr_name += item
            if index is not len(self.asr[0].sites) - 1:
                self.asr_name += '-'
        self.assertIsNotNone(self.asr_name,
                             msg='Could not parse asr full name.')
        self.assertTrue(
            self._onboard_cluster.btn_select_cluster_to_associate.exists(),
            msg=self._step_failed_msg(step='Try to find the cluster selecting button.')
        )
        self._onboard_cluster.btn_select_cluster_to_associate.click()
        _click_result = self._onboard_cluster.click_drop_down_list(
            self._onboard_cluster.lst_action_values,
            'tr',
            self.cluster_name)
        self.assertTrue(_click_result,
                        msg=self._step_failed_msg(step='Try to select cluster name to associate'))
        logger.info('Selected cluster {}'.format(self.cluster_name))
        self._onboard_cluster.wait_for_loading_complete()
        self.assertTrue(
            self._onboard_cluster.btn_select_asr.exists(),
            msg=self._step_failed_msg(step='Try to find the ASR selecting button.')
        )
        self._onboard_cluster.btn_select_asr.click()
        _click_result = self._onboard_cluster.click_drop_down_list(
            self._onboard_cluster.lst_action_values,
            'tr',
            self.asr_name
        )
        self.assertTrue(_click_result,
                        msg=self._step_failed_msg(step='Try to Select ASR name.'))
        logger.info('Selected ASR {}'.format(self.cluster_name))
        self._loading_window.wait_loading(self._current_browser, 30)
        self._onboard_cluster.btn_next.click()


    def _start_new_service_request(self):
        logger.info(msg='Start to switch to catalog frame')
        _navigate_to_catalog = self._catalog_page.navigate_to_catalog(self._current_browser)
        self.assertTrue(_navigate_to_catalog,
                        msg=self._step_failed_msg(step='switch to catalog frame failed.'))
        self.assertTrue(self._catalog_page.lnk_ehc_configuration.exists(),
                        msg=self._step_failed_msg(step='cannot find EHC Configuration card in the left page.'))
        self._catalog_page.lnk_ehc_configuration.click()
        self._catalog_page.wait_for_loading_complete(3)
        logger.info(msg='Start to click the Cluster Maintenance request button.')
        self.assertTrue(self._catalog_page.btn_cluster_maintenance_request.exists(),
                        msg=self._step_failed_msg(step='cannot find Cluster Maintenance card in the right page.'))
        self._catalog_page.btn_cluster_maintenance_request.click()

    def _fill_out_request_info(self):
        logger.info(msg='Start to fill items in the Request information tab')
        self._loading_window.wait_loading(self._current_browser, 90)
        self._loading_window.wait_loading2(self._current_browser, 240)
        self.assertTrue(self._onboard_cluster.txt_description.exists(),
                        msg=self._step_failed_msg(step='there is no textbox: Description.'))
        self._onboard_cluster.txt_description.set(self._testMethodName)
        self._onboard_cluster.wait_for_loading_complete(3)
        self.assertTrue(self._onboard_cluster.btn_next.exists(),
                        msg=self._step_failed_msg(step='there is no button: Next.'))
        self._onboard_cluster.btn_next.click()

    def _fill_out_action_info(self):
        logger.info(msg='Start to fill items in the Action Choice tab')
        self._loading_window.wait_loading(self._current_browser, 240)
        self.assertTrue(self._onboard_cluster.lnk_cluster_action_to_perform_menu.exists(),
                        msg=self._step_failed_msg(step='Action DropDownList open button does not exist.'))

        self._onboard_cluster.lnk_cluster_action_to_perform_menu.click()
        result = self._onboard_cluster.click_drop_down_list(self._onboard_cluster.lnk_select_dropdownlist,
                                                            'div',
                                                            self.action_chosen)
        if not result:
            # take screen shot to locate the random issue:
            # No element with name:Onboard VSAN Cluster found! Items are: [u'[ choose action ]',
            # u'Associate Avamar Proxies with Cluster', u'Associate Cluster to ASR',
            # u'Delete Cluster', u'Edit Cluster Hardware Island', u'Edit Cluster Site',
            # u'Onboard CA Cluster', u'Onboard DR Cluster', u'Onboard Local Cluster', u'Onboard MP Cluster']
            self.fail(msg=self._step_failed_msg(step='failed to select item Action:' + self.action_chosen))
        self._loading_window.wait_loading(self._current_browser, 240)
        self.assertTrue(self._onboard_cluster.btn_next.exists(),
                        msg=self._step_failed_msg(step='there is no button: Next.'))
        self._onboard_cluster.btn_next.click()

    def _delete_cluster(self):
        logger.info(msg='Start to fill items in the Delete Cluster tab')
        # Check if the cluster to delete exists
        self._loading_window.wait_loading(self._current_browser, 30)
        self.assertTrue(self._onboard_cluster.btn_select_cluster.exists(),
                        msg=self._step_failed_msg(step='Cluster DropDownList open button does not exist.'))
        self._onboard_cluster.btn_select_cluster.click()
        self._onboard_cluster.wait_for_loading_complete(3)
        _click_result = self._onboard_cluster.click_drop_down_list(self._onboard_cluster.lst_action_values,
                                                                   'tr',
                                                                   self._cluster_to_cluster)
        # If the cluster name exists, complete the following operations
        self.assertTrue(_click_result,
                        msg=self._step_failed_msg(
                            step='failed to select the cluster name:' + self._cluster_to_cluster))
        self._loading_window.wait_loading(self._current_browser, 30)
        logger.info('Selected cluster name: %s' % self._cluster_to_cluster)
        self._loading_window.wait_loading(self._current_browser, 30)

        self.assertTrue(self._onboard_cluster.btn_confirm_action.exists(),
                        msg=self._step_failed_msg(step='Confirm DropDownList open button does not exist.'))
        self._onboard_cluster.btn_confirm_action.click()
        _click_result = self._onboard_cluster.click_drop_down_list(
            self._onboard_cluster.lst_action_values,
            'tr',
            self._confirm)
        self.assertTrue(_click_result,
                        msg=self._step_failed_msg(step='failed to select: Confirm'))
        logger.info('Selected Confirm option: %s' % self._confirm)
        self._loading_window.wait_loading(self._current_browser, 30)
        self.assertTrue(self._onboard_cluster.btn_next.exists(),
                        msg=self._step_failed_msg(step='there is no button: Next.'))
        self._onboard_cluster.btn_next.click()

    def _edit_cluster_site(self):

        logger.info('Start to fill edit cluster site tab')
        self._loading_window.wait_loading(self._current_browser, 30)
        self.assertTrue(self._onboard_cluster.btn_edit_cluster_site.exists(),
                        msg=self._step_failed_msg(step='Cluster DropDownList open button does not exist.'))
        self._onboard_cluster.btn_edit_cluster_site.click()
        _click_result = self._onboard_cluster.click_drop_down_list(self._onboard_cluster.lst_action_values,
                                                                   'tr',
                                                                   self.cluster_to_edit)
        self.assertTrue(_click_result,
                        msg=self._step_failed_msg(step='Failed to select cluster:' + self.cluster_to_edit))

        self._loading_window.wait_loading(self._current_browser, 30)
        self.assertTrue(self._onboard_cluster.btn_site.exists(),
                        msg=self._step_failed_msg(step='Site Name DropDownList open button does not exist.'))
        self._onboard_cluster.btn_site.click()
        _click_result = self._onboard_cluster.click_drop_down_list(
            self._onboard_cluster.lst_action_values,
            'tr',
            self.site_to_edit)
        self.assertTrue(_click_result,
                        msg=self._step_failed_msg(step='failed to select Site Name:' + self.site_to_edit))

        self._loading_window.wait_loading(self._current_browser, 30)
        self.assertTrue(self._onboard_cluster.btn_hwi.exists(),
                        msg=self._step_failed_msg(step='Hardware Island DropDownList open button does not exist.'))
        self._onboard_cluster.btn_hwi.click()
        _click_result = self._onboard_cluster.click_drop_down_list(
            self._onboard_cluster.lst_action_values,
            'tr',
            self.hwi_to_edit)
        self.assertTrue(_click_result,
                        msg=self._step_failed_msg(step='failed to select Hardware Island:' + self.hwi_to_edit))
        self._loading_window.wait_loading(self._current_browser, 30)
        self.assertTrue(self._onboard_cluster.btn_next.exists(),
                        msg=self._step_failed_msg(step='there is no button: Next.'))
        self._onboard_cluster.btn_next.click()

    def _edit_cluster_hwi(self):

        logger.info('Start to fill edit cluster hwi tab')
        self._loading_window.wait_loading(self._current_browser, 30)
        self.assertTrue(self._onboard_cluster.btn_edit_cluster_hwi.exists(),
                        msg=self._step_failed_msg(step='Cluster DropDownList open button does not exist.'))
        self._onboard_cluster.btn_edit_cluster_hwi.click()
        _click_result = self._onboard_cluster.click_drop_down_list(self._onboard_cluster.lst_action_values,
                                                                   'tr',
                                                                   self.cluster_to_edit)
        self.assertTrue(_click_result, 'Failed to select cluster:' + self.cluster_to_edit)

        self._loading_window.wait_loading(self._current_browser, 30)
        logger.info('Start to select Hardware Island 1', False, True)
        self.assertTrue(self._onboard_cluster.btn_hwi_1.exists(),
                        msg=self._step_failed_msg(step='Hardware Island 1 DropDownList open button does not exists'))
        self._onboard_cluster.btn_hwi_1.click()
        _click_result = self._onboard_cluster.click_drop_down_list(
            self._onboard_cluster.lst_action_values,
            'tr',
            self.hwi_1_to_edit)
        self.assertTrue(_click_result,
                        msg=self._step_failed_msg(step='failed to select Hardware Island 1:' + self.hwi_1_to_edit))

        self._loading_window.wait_loading(self._current_browser, 30)

        container = self._current_browser.instance._browser.current
        if OnboardClusterPage.element_exists(self._onboard_cluster.xpath_btn_hwi_2_hidden, container, timeout=5):
            pass
        elif OnboardClusterPage.element_exists(self._onboard_cluster.xpath_btn_hwi_2, container, timeout=5):
            logger.info('Start to select Hardware Island 2', False, True)
            self.assertIsNotNone(self.hwi_2_to_edit, msg=self._step_failed_msg(
                step='Please provide new Hardware Island 2.'))
            self._onboard_cluster.btn_hwi_2.click()
            _click_result = self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lst_action_values,
                'tr',
                self.hwi_2_to_edit)
            self.assertTrue(_click_result,
                            msg=self._step_failed_msg(step='failed to select Hardware Island 2:' + self.hwi_2_to_edit))
            self._loading_window.wait_loading(self._current_browser, 30)
        self.assertTrue(self._onboard_cluster.btn_next.exists(),
                        msg=self._step_failed_msg(step='there is no button: Next.'))
        self._onboard_cluster.btn_next.click()

    def _onboard_local_cluster(self):
        logger.info(msg='Start to fill item in Onboard Local Cluster tab')
        self.assertTrue(self._onboard_cluster.lnk_select_a_local_hwi_menu.exists(),
                        msg=self._step_failed_msg(step='Hardware Island DropDownList open button does not exist.'))
        self._onboard_cluster.lnk_select_a_local_hwi_menu.click()
        if not (self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lnk_select_dropdownlist, 'div',
                self._onboard_cluster_entity.select_a_hwi)):
            self.fail(msg=self._step_failed_msg(
                step='failed to select hardware island:' + self._onboard_cluster_entity.select_a_hwi))

        self._loading_window.wait_loading(self._current_browser, 120)
        self.assertTrue(self._onboard_cluster.lnk_select_local_unprepared_cluster_menu.exists(),
                        msg=self._step_failed_msg(step='Cluster DropDownList open button does not exist.'))
        self._onboard_cluster.lnk_select_local_unprepared_cluster_menu.click()
        if not (self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lnk_select_dropdownlist, 'div',
                self._onboard_cluster_entity.unprepared_cluster)):
            self.fail(msg=self._step_failed_msg(
                step='failed to select cluster:' + self._onboard_cluster_entity.unprepared_cluster))

        self._loading_window.wait_loading(self._current_browser, 120)
        self.assertTrue(self._onboard_cluster.btn_next.exists(),
                        msg=self._step_failed_msg(step='there is no button: Next.'))
        self._onboard_cluster.btn_next.click()

    def _onboard_vsan_cluster(self):
        logger.info(msg='Start to fill item in Onboard VSAN Cluster tab')
        self.assertTrue(self._onboard_cluster.lnk_select_a_hwi_menu.exists(),
                        msg=self._step_failed_msg(step='Hardware Island DropDownList open button does not exist.'))
        self._onboard_cluster.lnk_select_a_hwi_menu.click()
        if not (self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lnk_select_dropdownlist, 'div',
                self._onboard_cluster_entity.select_a_hwi)):
            self.fail(self._step_failed_msg(
                step='failed to select a hardware island:' + self._onboard_cluster_entity.select_a_hwi))

        self._loading_window.wait_loading(self._current_browser, 120)
        self.assertTrue(self._onboard_cluster.lnk_select_unprepared_cluster_menu.exists(),
                        msg=self._step_failed_msg(step='Cluster open button does not exist.'))
        self._onboard_cluster.lnk_select_unprepared_cluster_menu.click()
        if not (self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lnk_select_dropdownlist, 'div',
                self._onboard_cluster_entity.unprepared_cluster)):
            self.fail(self._step_failed_msg(
                step='failed to select unprepared cluster:' + self._onboard_cluster_entity.unprepared_cluster))

        self._loading_window.wait_loading(self._current_browser, 120)
        self.assertTrue(self._onboard_cluster.btn_next.exists(),
                        msg=self._step_failed_msg(step='there is no button: Next.'))
        self._onboard_cluster.btn_next.click()

    def _onboard_ca_cluster(self):
        logger.info(msg='Start to fill item in Onboard CA Cluster tab')
        self.assertTrue(self._onboard_cluster.lnk_select_hwi_1_menu.exists(),
                        msg=self._step_failed_msg(step='Hardware Island 1 DropDownList open button does not exist.'))

        self._onboard_cluster.lnk_select_hwi_1_menu.click()
        self._onboard_cluster.wait_for_loading_complete(2)
        self.assertTrue(
                self._onboard_cluster.click_drop_down_list(
                    self._onboard_cluster.lnk_select_dropdownlist, 'div',
                    self._onboard_cluster_entity.select_hwi_1),
                self._step_failed_msg(
                    step='failed to select Hardware Island 1:' + self._onboard_cluster_entity.select_hwi_1
                )
        )

        self._loading_window.wait_loading(self._current_browser, 120)
        self.assertTrue(self._onboard_cluster.lnk_unprepared_cluster_menu.exists(),
                        msg=self._step_failed_msg(step='Cluster DropDownList open button does not exist.'))

        self._onboard_cluster.lnk_unprepared_cluster_menu.click()
        self.assertTrue(
            self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lnk_select_dropdownlist, 'div',
                self._onboard_cluster_entity.unprepared_cluster),
            self._step_failed_msg(
                step='failed to select unprepared cluster:' + self._onboard_cluster_entity.unprepared_cluster)
        )
        self._loading_window.wait_loading(self._current_browser, 120)
        self.assertTrue(self._onboard_cluster.lnk_choose_inter_site_vs_intra_site_munu.exists(),
                        msg=self._step_failed_msg(
                            step='Inter-site vs Intra-site DropDownList open button does not exist.'))
        self._onboard_cluster.lnk_choose_inter_site_vs_intra_site_munu.click()
        self.assertTrue(
            self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lnk_select_dropdownlist, 'div',
                self._onboard_cluster_entity.choose_inter_site_vs_intra_site),
            msg=self._step_failed_msg(
                step='failed to select Choose Inter-site vs Intra-site:' +
                self._onboard_cluster_entity.choose_inter_site_vs_intra_site)
            )
        self._loading_window.wait_loading(self._current_browser, 120)
        self.assertTrue(self._onboard_cluster.lnk_select_hwi_2_menu.exists(),
                        msg=self._step_failed_msg(step='Hardware Island 2 DropDownList open button does not exist.'))
        self._onboard_cluster.lnk_select_hwi_2_menu.click()
        self.assertTrue(
            self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lnk_select_dropdownlist, 'div',
                self._onboard_cluster_entity.select_hwi_2),
            msg=self._step_failed_msg(
                step='failed to select Hardware Island 2:' + self._onboard_cluster_entity.select_hwi_2)
        )

        self._loading_window.wait_loading(self._current_browser, 120)

        self.assertTrue(self._onboard_cluster.lbl_select_hosts_for_hardware_island_1.exists(),
                        msg=self._step_failed_msg(
                            step='Hardware Island 1 Hosts DropDownList open button does not exist.'))

        host_hwi_1 = None
        if not self._onboard_cluster_entity.hosts_for_hwi_1:
            logger.info(
                'HardwareIsland 1 Host is not specified in config, will select first one in Dropdownlist.', False, True)
            host_hwi_1 = self._onboard_cluster.select_listbox_by_index(
                    self._onboard_cluster.lbl_select_hosts_for_hardware_island_1, 'span', 0)
            self.assertIsNotNone(
                host_hwi_1, self._step_failed_msg(step='failed to select the first option of Hardware Island 1 Host'))
            logger.info(
                'Selected Host:{} for HWI:{}'.format(host_hwi_1, self._onboard_cluster_entity.select_hwi_1),
                False, True)
        else:
            self.assertTrue(
                self._onboard_cluster.select_listbox_by_value(
                    self._onboard_cluster.lbl_select_hosts_for_hardware_island_1,
                    'span',
                    self._onboard_cluster_entity.hosts_for_hwi_1),
                self._step_failed_msg(
                    step='failed to select Host for Hardware Island 1:' + self._onboard_cluster_entity.hosts_for_hwi_1))
            logger.info(
                'HardwareIsland 1 Host is selected as :{}'.format(
                    self._onboard_cluster_entity.hosts_for_hwi_1), False, True)
            host_hwi_1 = self._onboard_cluster_entity.hosts_for_hwi_1


        self._loading_window.wait_loading(self._current_browser, 120)

        self.assertTrue(self._onboard_cluster.lbl_select_hosts_for_hardware_island_2.exists(),
                        self._step_failed_msg(step='Hardware Island 2 Hosts DropDownList '
                                                       'open button does not exist.'))
        host_hwi_2 = None
        if not self._onboard_cluster_entity.hosts_for_hwi_2:
            logger.info(
                'HardwareIsland 2 Host is not specified in config, will select first one in Dropdownlist.', False, True)
            host_hwi_2 = self._onboard_cluster.select_listbox_by_index(
                self._onboard_cluster.lbl_select_hosts_for_hardware_island_2, 'span', 0)
            self.assertIsNotNone(
                host_hwi_2,  self._step_failed_msg(step='failed to select the first option of Hardware Island 2 Host'))
            logger.info(
                'Selected Host:{} for HWI:{}'.format(host_hwi_2, self._onboard_cluster_entity.select_hwi_2),
                False, True)
        else:
            self.assertTrue(self._onboard_cluster.select_listbox_by_value(
                self._onboard_cluster.lbl_select_hosts_for_hardware_island_2, 'span',
                self._onboard_cluster_entity.lbl_select_hosts_for_hardware_island_2),
                self._step_failed_msg(
                    step='failed to select Host for Hardware Island 2:' + self._onboard_cluster_entity.hosts_for_hwi_2))
            logger.info(
                'HardwareIsland 2 Host is selected as :{}'.format(
                    self._onboard_cluster_entity.hosts_for_hwi_2), False, True)
            host_hwi_2 = self._onboard_cluster_entity.hosts_for_hwi_2

        # we want to write hwi-host mapping back to context.
        hwi_host_pairs = {}
        hwi_host_pairs.update({self._onboard_cluster_entity.select_hwi_1: host_hwi_1})
        hwi_host_pairs.update({self._onboard_cluster_entity.select_hwi_2: host_hwi_2})
        # adding a property to onboard_cluster_entity object with a dict for hwi-host pairs.
        setattr(self._onboard_cluster_entity, 'hwi_host_pairs', hwi_host_pairs)

        self._loading_window.wait_loading(self._current_browser, 120)
        self.assertTrue(self._onboard_cluster.btn_next.exists(),
                        msg=self._step_failed_msg(step='there is no button: Next.'))
        self._onboard_cluster.btn_next.click()

    def _onboard_dr_cluster(self):
        self.assertTrue(self._onboard_cluster.lnk_select_a_hwi_for_the_protected_cluster_menu.exists(),
                        msg=self._step_failed_msg(step='Protected Hardware Island DropDownList '
                                                       'open button does not exist.'))

        logger.info(msg='In the operation: Select a hardware island for the protected cluster')
        self._onboard_cluster.lnk_select_a_hwi_for_the_protected_cluster_menu.click()
        if not (self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lnk_select_dropdownlist, 'div',
                self._onboard_cluster_entity.hwi_for_protected_cluster)):
            self.fail(msg=self._step_failed_msg(
                step='failed to select a hardware island for the protected cluster:' +
                self._onboard_cluster_entity.hwi_for_protected_cluster))

        self._loading_window.wait_loading(self._current_browser, 120)
        logger.info(msg='In the operation: Select unprepared protected cluster')
        self.assertTrue(self._onboard_cluster.lnk_select_unprepared_protected_cluster_menu.exists(), msg=
                        self._step_failed_msg(step='Protected Cluster DropDownList open button does not exist.'))

        self._onboard_cluster.lnk_select_unprepared_protected_cluster_menu.click()
        if not self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lnk_select_dropdownlist, 'div',
                self._onboard_cluster_entity.unprepared_protected_cluster):
            self.fail(msg=self._step_failed_msg(
                step='failed to select unprepared protected cluster:' +
                self._onboard_cluster_entity.unprepared_protected_cluster))

        self._loading_window.wait_loading(self._current_browser, 120)
        logger.info(msg='In the operation: Select the Hardware Island for the Recovery cluster')
        self.assertTrue(self._onboard_cluster.lnk_select_the_hwi_for_the_recovery_cluster_menu.exists(), msg=
                        self._step_failed_msg(step='Recovery Hardware Island DropDownList open button does not exist.'))
        self._onboard_cluster.lnk_select_the_hwi_for_the_recovery_cluster_menu.click()
        if not self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lnk_select_dropdownlist, 'div',
                self._onboard_cluster_entity.hwi_for_recovery_cluster):
            self.fail(msg=self._step_failed_msg(
                step='failed to select the Hardware Island for the Recovery cluster:' +
                self._onboard_cluster_entity.hwi_for_recovery_cluster))

        self._loading_window.wait_loading(self._current_browser, 120)

        logger.info(msg='In the operation: Select unprepared Recovery cluster')
        self.assertTrue(self._onboard_cluster.lnk_select_unprepared_recovery_cluster_menu.exists(),
                        msg=self._step_failed_msg(step='Recovery cluster DropDownList open button does not exist.'))
        self._onboard_cluster.lnk_select_unprepared_recovery_cluster_menu.click()
        if not self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lnk_select_dropdownlist, 'div',
                self._onboard_cluster_entity.unprepared_recovery_cluster):
            self.fail(msg=self._step_failed_msg(
                step='failed to select unprepared Recovery cluster:' +
                self._onboard_cluster_entity.unprepared_recovery_cluster))

        self._loading_window.wait_loading(self._current_browser, 120)
        self.assertTrue(self._onboard_cluster.btn_next.exists(),
                        msg=self._step_failed_msg(step='there is no button: Next.'))
        self._onboard_cluster.btn_next.click()

    def _onboard_mp_cluster(self):
        logger.info(msg='Start to fill item in Onboard MP Cluster tab')
        self.assertTrue(self._onboard_cluster.lnk_select_hwi_1_mp_menu.exists(),
                        msg=self._step_failed_msg(
                            step='Protected Hardware Island 1 DropDownList open button does not exist.'))

        self._onboard_cluster.lnk_select_hwi_1_mp_menu.click()
        self._onboard_cluster.wait_for_loading_complete(2)
        if not (self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lnk_select_dropdownlist, 'div',
                self._onboard_cluster_entity.select_hwi_1)):
            self.fail(msg=self._step_failed_msg(
                step='failed to select Hardware Island 1:' + self._onboard_cluster_entity.select_hwi_1))

        self._loading_window.wait_loading(self._current_browser, 120)
        self.assertTrue(self._onboard_cluster.lnk_inter_site_vs_intra_site_mp_menu.exists(),
                        msg=self._step_failed_msg(
                            step='Inter-site vs Intra-site DropDownList open button does not exist.'))
        self._onboard_cluster.lnk_inter_site_vs_intra_site_mp_menu.click()
        if not (self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lnk_select_dropdownlist, 'div',
                self._onboard_cluster_entity.choose_inter_site_vs_intra_site)):
            self.fail(msg=self._step_failed_msg(
                step='failed to choose Inter-site vs Intra-site:' +
                self._onboard_cluster_entity.choose_inter_site_vs_intra_site))

        self._loading_window.wait_loading(self._current_browser, 120)
        self.assertTrue(self._onboard_cluster.lnk_select_hwi_2_mp_menu.exists(),
                        msg=self._step_failed_msg(
                            step='Protected Hardware Island 2 DropDownList open button does not exist.'))
        self._onboard_cluster.lnk_select_hwi_2_mp_menu.click()
        if not (self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lnk_select_dropdownlist, 'div',
                self._onboard_cluster_entity.select_hwi_2)):
            self.fail(msg=self._step_failed_msg(
                step='failed to select Hardware Island 2:' +
                self._onboard_cluster_entity.select_hwi_2))

        self._loading_window.wait_loading(self._current_browser, 120)
        self.assertTrue(self._onboard_cluster.lnk_unprepared_protected_cluster_mp_menu.exists(),
                        msg=self._step_failed_msg(step='Protected Cluster DropDownList open button does not exist.'))
        self._onboard_cluster.lnk_unprepared_protected_cluster_mp_menu.click()
        if not (self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lnk_select_dropdownlist, 'div',
                self._onboard_cluster_entity.unprepared_protected_cluster)):
            self.fail(msg=self._step_failed_msg(
                step='failed to select unprepared Protected cluster:' +
                self._onboard_cluster_entity.unprepared_protected_cluster))

        self._loading_window.wait_loading(self._current_browser, 120)

        self.assertTrue(self._onboard_cluster.lbl_hosts_from_cluster_that_are_from_hwi_1.exists(),
                        msg=self._step_failed_msg(
                            step='Hardware Island 1 Hosts DropDownList open button does not exist.'))

        if self._onboard_cluster_entity.hosts_for_hwi_1 == '':
            if not (self._onboard_cluster.select_listbox_by_index(
                    self._onboard_cluster.lbl_hosts_from_cluster_that_are_from_hwi_1, 'span', 0)):
                self.fail(msg=self._step_failed_msg(
                    step='failed to select the first option of Hardware Island 1 Hosts'))
        else:
            if not (self._onboard_cluster.select_listbox_by_value(
                    self._onboard_cluster.lbl_hosts_from_cluster_that_are_from_hwi_1, 'span',
                    self._onboard_cluster_entity.hosts_for_hwi_1)):
                self.fail(msg=self._step_failed_msg(
                    step='failed to select Hardware Island 1 Hosts:' + self._onboard_cluster_entity.hosts_for_hwi_1))

        self._loading_window.wait_loading(self._current_browser, 120)

        self.assertTrue(self._onboard_cluster.lbl_hosts_from_cluster_that_are_from_hwi_2.exists(),
                        msg=self._step_failed_msg(
                            step='Hardware Island 2 Hosts DropDownList open button does not exist.'))

        if self._onboard_cluster_entity.hosts_for_hwi_2 == '':
            if not (self._onboard_cluster.select_listbox_by_index(
                    self._onboard_cluster.lbl_hosts_from_cluster_that_are_from_hwi_2, 'span', 0)):
                self.fail(
                    msg=self._step_failed_msg(step='failed to select the first option of Hardware Island 2 Hosts'))
        else:
            if not (self._onboard_cluster.select_listbox_by_value(
                    self._onboard_cluster.lbl_hosts_from_cluster_that_are_from_hwi_2, 'span',
                    self._onboard_cluster_entity.hosts_for_hwi_2)):
                self.fail(msg=self._step_failed_msg(
                    step='failed to select Hardware Island 2 Hosts:' + self._onboard_cluster_entity.hosts_for_hwi_2))

        self._loading_window.wait_loading(self._current_browser, 120)
        self.assertTrue(self._onboard_cluster.lnk_select_hwi_3_mp_menu.exists(),
                        msg=self._step_failed_msg(
                            step='Recovery Hardware Island DropDownList open button does not exist.'))
        self._onboard_cluster.lnk_select_hwi_3_mp_menu.click()
        if not (self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lnk_select_dropdownlist, 'div',
                self._onboard_cluster_entity.select_hwi_3)):
            self.fail(msg=self._step_failed_msg(
                step='failed to select Recovery Hardware Island:' + self._onboard_cluster_entity.select_hwi_3))

        self._loading_window.wait_loading(self._current_browser, 120)
        self.assertTrue(self._onboard_cluster.btn_unprepared_recovery_cluster_mp_menu.exists(),
                        msg=self._step_failed_msg(
                            step='Recovery Cluster DropDownList open button does not exist.'))
        self._onboard_cluster.btn_unprepared_recovery_cluster_mp_menu.click()
        if not (self._onboard_cluster.click_drop_down_list(
                self._onboard_cluster.lnk_select_dropdownlist, 'div',
                self._onboard_cluster_entity.unprepared_recovery_cluster)):
            self.fail(msg=self._step_failed_msg(
                step='failed to select Recovery cluster:' + self._onboard_cluster_entity.unprepared_recovery_cluster))

        self._loading_window.wait_loading(self._current_browser, 120)
        self.assertTrue(self._onboard_cluster.btn_next.exists(),
                        msg=self._step_failed_msg(step='there is no button: Next.'))
        self._onboard_cluster.btn_next.click()

    def _confirm_info_in_review(self):
        logger.info(msg='Start to confirm information in Review and Submit tab')
        self._loading_window.wait_loading(self._current_browser, 30)

        self.assertTrue(self._onboard_cluster.btn_submit.exists(),
                        msg=self._step_failed_msg(step='there is no button: Submit'))
        self._onboard_cluster.btn_submit.click()
        self._loading_window.wait_loading(self._current_browser, 30)

    def _get_action_chosen(self):
        self.action_chosen = ''
        map_action_chosen = {
            'LC1S': 'Onboard Local Cluster',
            'VS1S': 'Onboard VSAN Cluster',
            'CA2S': 'Onboard CA Cluster',
            'CA1S': 'Onboard CA Cluster',
            'DR2S': 'Onboard DR Cluster',
            'MP2S': 'Onboard MP Cluster',
            'MP3S': 'Onboard MP Cluster',
            'test_delete_cluster': 'Delete Cluster',
            'test_edit_cluster_hwi': 'Edit Cluster Hardware Island',
            'test_edit_cluster_site': 'Edit Cluster Site',
            'test_associate_cluster_to_asr': 'Associate Cluster to ASR'
        }
        if self._testMethodName == self.Func.ONBOARD_CLUSTER:
            self.action_chosen = map_action_chosen.get(self._onboard_cluster_type)
        else:
            self.action_chosen = map_action_chosen.get(self._testMethodName)

    def _submit_request(self):
        logger.info(msg='Go into the request has been submitted successully page')
        self.assertTrue(self._onboard_cluster.lbl_confirmation_success.exists(),
                        msg=self._step_failed_msg(
                            step='there is no label: The request has been submitted successfully'))

        # wait to load frame
        self._onboard_cluster.wait_for_loading_complete(wait_time=2)
        self.assertTrue(self._onboard_cluster.btn_ok.exists(),
                        msg=self._step_failed_msg(step='there is no button: OK'))
        self._onboard_cluster.btn_ok.click()

    def _handle_assert_exception(self):
        self._onboard_cluster.save_request()

    def _handle_other_exception(self, err_message):
        self._onboard_cluster.save_request()
        self.fail(msg=self._step_failed_msg(
            step='encounters error in {0}, details error info: {1}'.format(self._testMethodName, err_message)))
