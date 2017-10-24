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

        self.btn_failover_avamar_site_request = WebButton(
            xpath='.//div[@id="CATALOG_ITEM_Failover Avamar Grids after Site Failure"]'
                  '//div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')

        self.btn_failback_avamar_site_request = WebButton(
            xpath='.//div[@id="CATALOG_ITEM_Failback Avamar Policies after Site Restoration"]'
                  '//div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')

        self.btn_failover_avamar_grid_request = WebButton(
            xpath='.//div[@id="CATALOG_ITEM_Failover Avamar Policies for Offline Avamar Grid"]'
                  '//div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')

        self.btn_failback_avamar_grid_request = WebButton(
            xpath='.//div[@id="CATALOG_ITEM_Failback Avamar Policies after Restoring Avamar Grid"]'
                  '//div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')
