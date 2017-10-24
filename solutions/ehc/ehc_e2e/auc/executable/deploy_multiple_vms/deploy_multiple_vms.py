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

from robot.api import logger
from ehc_e2e.auc.uimap.shared.catalogpage import CatalogPage
from ehc_e2e.auc.uimap.shared.requestspage import RequestsPage
from ehc_e2e.auc.uimap.specific.deployvmcommonpage import DeployVMCommonPage
from ehc_e2e.auc.uimap.specific.deployvmrequestpage import DeployVmRequestPage
from ehc_e2e.auc.uimap.shared.loadingwindow import LoadingWindow
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared.basepage import BasePage
import time


class DeployMultipleVM(BaseUseCase):

    def assertTrue(self, expr, msg=None):
        logger.info(msg, False, True)
        super(DeployMultipleVM, self).assertTrue(expr, 'Running on step: "Deploy Multiple VMs" - FAILED. Failed at: ' + msg)

    def test_deploy_vm(self):
        rp4vm_bp_list = []
        dp_bp_list = []
        description = 'Test Deploy Multiple VMs'
        driver_ref = self.current_browser.instance._browser.current

        catalog_page = CatalogPage()
        request_page = RequestsPage()
        loading_window = LoadingWindow()
        deploy_page = DeployVMCommonPage(self.blueprint)

        self.assertTrue(catalog_page.navigate_to_catalog(self.current_browser), 'Go to catalog page')
        self.assertTrue(deploy_page.btn_bp_entitlement.exists(), 'Find entitlement button for the blueprint')
        deploy_page.btn_bp_entitlement.click()
        loading_window.wait_loading(self.current_browser)

        self.assertTrue(deploy_page.btn_bp_request.exists(), 'Find request button for the blueprint')
        deploy_page.btn_bp_request.click()
        loading_window.wait_loading(self.current_browser)
        loading_window.wait_loading_deploy_vm_page(self.current_browser)

        with deploy_page.iframe_bp:
            self.assertTrue(deploy_page.txt_description.exists(), 'Find description textbox')
            deploy_page.txt_description.set(description)

            # find and visit all vsphere blueprint of designated blueprint
            vsphere_bp_label_list = driver_ref.find_elements_by_xpath(
                '//span[text()="{}" and contains(@class, "x-tree-node-text")]/../../../../../following-sibling::'
                'table/tbody/tr/td/div/span[contains(@class, "x-tree-node-text")]'.format(self.blueprint))

            for vsphere_bp_label in vsphere_bp_label_list:
                vsphere_bp_name = vsphere_bp_label.text
                self.assertTrue(vsphere_bp_name in self.properties_dict, 'Check vsphere blueprint {} in vRA is valid in YAML'.format(vsphere_bp_name))
                properties = self.properties_dict[vsphere_bp_name].__dict__ if self.properties_dict[vsphere_bp_name] else {}
                del self.properties_dict[vsphere_bp_name]

                vsphere_bp_label.click()
                loading_window.wait_loading(self.current_browser)

                if BasePage.element_exists(deploy_page.txt_cg_xpath, driver_ref, 5):
                    self.assertTrue('cg' in properties, 'Check deployment_properties.cg exists in YAML')
                    cg = properties['cg']
                    del properties['cg']

                    if cg is None or (isinstance(cg, str) and cg.isspace()):
                        logger.info('deployment_properties.cg is empty in YAML. Make up a new one', False, True)
                        cg = 'CG-' + time.strftime('%y%m%d%H%M%S')
                    else:
                        self.fail('Invalid deployment_properties.cg')
                    deploy_page.txt_cg.set(cg)
                    rp4vm_bp_list.append(vsphere_bp_name)

                if BasePage.element_exists(deploy_page.txt_boot_priority_xpath, driver_ref, 5):
                    self.assertTrue('boot_priority' in properties, 'Check deployment_properties.boot_priority exists in YAML')
                    boot_priority = properties['boot_priority']
                    del properties['boot_priority']

                    if boot_priority is None or (isinstance(boot_priority, str) and boot_priority.isspace()):
                        logger.info('deployment_properties.boot_priority is empty in YAML. Set to 1 by default', False, True)
                        boot_priority = '1'
                    else:
                        self.fail('Invalid deployment_properties.boot_priority')
                    deploy_page.txt_boot_priority.set(boot_priority)

                if BasePage.element_exists(deploy_page.cb_policy_xpath, driver_ref, 5):
                    self.assertTrue('policy' in properties, 'Check deployment_properties.policy exists in YAML')
                    policy = properties['policy']
                    del properties['policy']

                    self.assertTrue(policy and isinstance(policy, str) and not policy.isspace(), 'Check deployment_properties.boot_priority is valid in YAML')
                    deploy_page.cb_policy.select(by_visible_text=policy)

                if BasePage.element_exists(deploy_page.cb_backup_service_xpath, driver_ref, 5):
                    self.assertTrue('backup_service_level' in properties, 'Check deployment_properties.backup_service_level exists in YAML')
                    bsl = properties['backup_service_level']
                    del properties['backup_service_level']

                    self.assertTrue(bsl and isinstance(bsl, str) and not bsl.isspace(), 'Check deployment_properties.backup_service_level is valid in YAML')
                    deploy_page.cb_backup_service.select(by_visible_text=bsl)
                    dp_bp_list.append(vsphere_bp_name)

                self.assertTrue(len(properties) == 0, 'Check all VM properties defined in YAML have been configured in vRA')
                deploy_page.wait_for_loading_complete(5)

        self.assertTrue(len(self.properties_dict) == 0,
                        'Check all vsphere blueprints defined in YAML are found in vRA and properties have been configured')
        # Finish setting attributes -> submit
        with deploy_page.iframe_catalog:
            self.assertTrue(deploy_page.btn_submit.exists(), 'Find submit button')
            deploy_page.btn_submit.click()
            self.assertTrue(deploy_page.btn_ok.exists(), 'Find OK button after submission')
            deploy_page.btn_ok.click()

        # Check request result
        self.assertTrue(request_page.navigate_to_request(self.current_browser), 'Go to request page')
        request_result = request_page.get_request_result(description, timeout=7200, slp=300, firstwaitduration=60)
        self.assertTrue(request_result is not None, 'Get request result')
        request_page.wait_for_loading_complete(3)
        try:
            driver_ref.find_element_by_xpath('//td[@cellindex="0"]/div/a/b[text()="' + request_result.request + '"]').click()
        except:
            self.fail('Failed to deploy VMs. Cannot find and click request id element')
        request_page.wait_for_loading_complete(10)
        self.deployed_vms = DeployVmRequestPage().get_deployed_vms()

        # self.assertTrue(request_page.navigate_to_request(self.current_browser), 'Go to request page')
        # try:
        #     driver_ref.find_element_by_xpath('//td[@cellindex="0"]/div/a/b[text()="' + request_result.request + '"]').click()
        # except:
        #     self.fail('Failed to deploy VMs. Cannot find and click request id element')
        # request_page.wait_for_loading_complete(10)
        # self.rp4vm_vms = DeployVmRequestPage().get_deployed_vms(bp_filter=True, bp_list=rp4vm_bp_list)

        self.assertTrue(request_page.navigate_to_request(self.current_browser), 'Go to request page')
        try:
            driver_ref.find_element_by_xpath('//td[@cellindex="0"]/div/a/b[text()="' + request_result.request + '"]').click()
        except:
            self.fail('Failed to deploy VMs. Cannot find and click request id element')
        request_page.wait_for_loading_complete(10)
        self.dp_vms = DeployVmRequestPage().get_deployed_vms(bp_filter=True, bp_list=dp_bp_list)

        if request_result.status == 'Successful':
            logger.info('Deploy multiple VMs: request succeeded', False, True)
        else:
            logger.error('Deploy multiple VMs: request No.{} failed'.format(request_result.request))
            self.fail('Failed to deploy VMs. Request result is failed')

    def runTest(self):
        self.test_deploy_vm()

    def _validate_context(self):
        self.deployed_vms = []
        self.dp_vms = []
        self.rp4vm_vms = []
        self.properties_dict = {}
        self.current_browser = self.ctx_in.shared.current_browser
        assert hasattr(self.ctx_in, 'deploy_multiple_vms'), 'deploy_multiple_vms does not exist in YAML'

        self.blueprint = getattr(self.ctx_in.deploy_multiple_vms, 'blueprint', None)
        assert self.blueprint and isinstance(self.blueprint, str) and not self.blueprint.isspace(),\
            'deploy_multiple_vms.blueprint should be valid and not empty in YAML'

        self.vm_settings = getattr(self.ctx_in.deploy_multiple_vms, 'vm_settings', None)
        assert self.vm_settings and isinstance(self.vm_settings, list), 'deploy_multiple_vms.vm_settings is invalid in YAML'

        for vm_setting in self.vm_settings:
            vsphere_id = getattr(vm_setting, 'vsphere_id', None)
            assert vsphere_id and isinstance(vsphere_id, str) and not vsphere_id.isspace(),\
                'In deploy_multiple_vms.vm_settings: vsphere_id should be valid and not empty in YAML'
            assert vsphere_id not in self.properties_dict, 'In deploy_multiple_vms.vm_settings: duplicated vsphere_id {}'.format(vsphere_id)
            assert hasattr(vm_setting, 'deployment_properties'), 'In deploy_multiple_vms.vm_settings: deployment_properties does not exist in YAML'
            self.properties_dict[vsphere_id] = vm_setting.deployment_properties

    def _finalize_context(self):
        logger.info('Deployed VMs: {}'.format(self.deployed_vms), False, True)
        setattr(self.ctx_out, 'deployed_vms', self.deployed_vms + getattr(self.ctx_in, 'deployed_vms', []))
        logger.info('DP protected VMs: {}'.format(self.dp_vms), False, True)
        setattr(self.ctx_out, 'dp_vms', self.dp_vms + getattr(self.ctx_in, 'dp_vms', []))
        logger.info('RP4VM protected VMs: {}'.format(self.rp4vm_vms), False, True)
        setattr(self.ctx_out, 'rp4vm_vms', self.rp4vm_vms + getattr(self.ctx_in, 'rp4vm_vms', []))
