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

from ehc_e2e.auc.uimap.extension import WebFrame


class CatalogTab(object):
    def __init__(self):
        super(CatalogTab, self).__init__()

        self.frm_catalog = WebFrame(
            onload='selfservice/SelfServiceGadget.gadget.xml')

        self.lnk_all_services = WebLink(
            xpath='//div[@id="SERVICE_All Services"]')

        self.lnk_ehc_configuration = WebLink(
            xpath='//div[@id="SERVICE_EHC Configuration"]')
        self.lnk_data_protection_services = WebLink(
            xpath='//div[@id="SERVICE_Data Protection Services"]')
        self.lnk_cloud_storage = WebLink(
            xpath='//div[@id="SERVICE_Cloud Storage"]')

        self.btn_cluster_maintenance_request = WebButton(
            xpath='//div[@id="CATALOG_ITEM_Cluster Maintenance"]'
                  '//div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')
        self.btn_vcenter_relationship_request = WebButton(
            xpath='//div[@id="CATALOG_ITEM_vCenter Relationship Maintenance"]'
                  '//div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')


class ItemsTab(object):
    def __init__(self):
        super(ItemsTab, self).__init__()

        self.frm_items = WebFrame(onload='item/ItemGadget.gadget.xml')
