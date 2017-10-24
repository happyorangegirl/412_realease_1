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

from uiacore.modeling.webui.controls import WebButton

from ehc_e2e.auc.uimap.shared.generic import CatalogTab


class CatalogPage(CatalogTab):
    def __init__(self):
        super(CatalogPage, self).__init__()

        self.btn_prepare_for_srm_dp_failover_request = WebButton(
            xpath='.//div[@id="CATALOG_ITEM_Prepare Avamar for SRM DR Failover"]'
                  '//div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')

        self.btn_dr_post_failover_updater_request = WebButton(
            xpath='.//div[@id="CATALOG_ITEM_Remediate Management of SRM DR Protected Workloads"]'
                  '//div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')
        self.btn_dr_remediator_request = WebButton(
            xpath='.//div[@id="CATALOG_ITEM_Validate Protection for SRM DR Workloads"]'
                  '//div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')
