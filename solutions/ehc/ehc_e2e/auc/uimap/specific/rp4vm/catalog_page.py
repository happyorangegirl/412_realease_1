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

from uiacore.modeling.webui.controls import WebButton, WebLink

from ehc_e2e.auc.uimap.shared.generic import CatalogTab


class CatalogPage(CatalogTab):
    def __init__(self):
        super(CatalogPage, self).__init__()

        self.btn_RP4VM_deploy_request = WebButton(
            xpath='.//div[@id="CATALOG_ITEM_RP4VM Deploy"]'
                  '//div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')
        self.lnk_ehc_recoverpoint_for_vms = WebLink(
            xpath='//div[@id="SERVICE_EHC RecoverPoint for VMs"]')
        self.lnk_vm_deploy = WebLink(
            xpath='//div[@id="SERVICE_VM Deploy]')
        self.btn_RP4VM_policy_maintenance_request = WebButton(
            xpath='.//div[@id="CATALOG_ITEM_RP4VM Policy Maintenance"]'
                  '//div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')
        self.btn_RP4VM_vRPA_cluster_maintenance_request = WebButton(
            xpath='.//div[@id="CATALOG_ITEM_RP4VM vRPA Cluster Maintenance"]'
                  '//div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')
        self.btn_RP4VM_post_failover_request = WebButton(
            xpath='.//div[@id="CATALOG_ITEM_RP4VM Post Failover Synchronization"]'
                  '//div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')
        self.btn_RP4VM_pre_failover_request = WebButton(
            xpath='.//div[@id="CATALOG_ITEM_RP4VM Pre Failover Maintenance"]'
                  '//div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')
