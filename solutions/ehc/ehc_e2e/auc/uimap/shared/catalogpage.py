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

from uiacore.modeling.webui.controls import (
    WebTextBox, WebButton, WebLabel, WebLink)
from .basepage import BasePage
from .mainpage import MainPage
from robot.api import logger
import sys


class CatalogPage(BasePage):

    def __init__(self):
        self.url_self_service_gadget = \
            'https://com.vmware.csp.core.cafe.catalog.plugin.vproxy//selfservice/SelfServiceGadget.gadget.xml'
        self.lnk_site_maintenance = WebLink(
            xpath='//a[@title="Site Maintenance"]')
        self.btn_site_maintenance_request = WebButton(
            xpath='//div[@id="CATALOG_ITEM_Site Maintenance"]/div/div/div'
                  '[@id="CATALOG_ITEM_REQUEST_BUTTON"]')
        self.lbl_gadget_2_frame = WebLabel(id='__gadget_2')
        self.lbl_catalog_page = WebLabel(id='CATALOG_PAGE')
        self.btn_add_site_request = WebButton(id='submit')
        self.gadget_2_frame_id = '__gadget_2'
        self.lbl_service_catalog = WebLabel(
            xpath='//div[text()="Service Catalog"]')
        self.lbl_all_service = WebLabel(
            xpath='//div[text()="All Services"]')
        self.btn_cloud_storage = WebButton(xpath='//div[text()="Cloud Storage"]')
        self.btn_hwi_maintenance_request = WebButton(
            xpath='//div[@id="CATALOG_ITEM_Hardware Island Maintenance"]/div/div/div[@id="CATALOG_ITEM_REQUEST_BUTTON"]'
        )
        self.btn_vcenter_endpoint_request = WebButton(xpath='//div[@id="CATALOG_ITEM_vCenter Endpoint Maintenance"]'
                                                            '/div/div/div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')
        self.btn_vcenter_relationship_request = WebButton(xpath=
                                                          '//div[@id="CATALOG_ITEM_vCenter Relationship Maintenance"]'
                                                          '/div/div/div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')
        self.btn_cluster_maintenance_request = WebButton(
            xpath='//div[@id="CATALOG_ITEM_Cluster Maintenance"]/'
                  'div/div/div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')
        self.lbl_services_catalog = WebLabel(
            xpath='//*[@id="CATALOG_PAGE"]/div[2]/div/div[3]/div/div[2]/div/'
                  'div[3]/div')
        self.btn_arr_maintenance_request = WebButton(
            xpath='//div[@id="CATALOG_ITEM_Avamar Replication Relationship (ARR) Maintenance"]/'
                  'div/div/div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')
        self.btn_asr_maintenance_request = WebButton(
            xpath='//div[@id="CATALOG_ITEM_Avamar Site Relationship (ASR) '
                  'Maintenance"]/div/div/div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')
        self.txt_search = WebTextBox(
            xpath='//*[@id="CATALOG_ITEM_LIST_TABLE_TABLEVIEW_SEARCH_TEXTBOX"]')
        self.btn_search = WebButton(
            xpath='//*[@id="CATALOG_ITEM_LIST_TABLE_TABLEVIEW_SEARCH_IMG_SEARCH'
                  '_OR_CLEAR"]')
        self.btn_ok = WebButton(xpath='//*[@id="CONFIRMATION_OK_BUTTON"]')
        self.lbl_success = WebLabel(xpath='//*[@id="CONFIRMATION_OK_BUTTON"]')
        self.btn_blueprint_req_xpath_template = '//div[@id="CATALOG_ITEM_{}"]' \
                                                '/div/div/div[@id=' \
                                                '"CATALOG_ITEM_REQUEST_BUTTON"]'
        self.btn_provision_cloud_storage_request = WebButton(
            xpath='//div[@id="CATALOG_ITEM_Provision Cloud Storage"]/div/div/div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')

        self.btn_datastore_maintenance_request = WebButton(
            xpath='//div[@id="CATALOG_ITEM_Datastore Maintenance"]/div/div/div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')
        self.lnk_ehc_configuration = WebLink(xpath='//div[text()="EHC Configuration"]')
        self.lnk_data_protection_services = WebLink(xpath='//div[text()="Data Protection Services"]')
        self.btn_avamar_grid_maintenance_request = WebButton(
            xpath='//div[@id="CATALOG_ITEM_Avamar Grid Maintenance"]/div/div/div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')


        self.btn_backup_service_level_request = WebButton(xpath=
                                                          '//div[@id="CATALOG_ITEM_Backup Service Level Maintenance"]'
                                                          '/div/div/div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')

        self.btn_run_admin_report_request = WebButton(xpath='//div[@id="CATALOG_ITEM_Run Admin Report"]'
                                                            '/div/div/div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')
        self.btn_avamar_proxy_maintenance_request = WebButton(
            xpath='//div[@id="CATALOG_ITEM_Avamar Proxy Maintenance"]/div/div/div[@id="CATALOG_ITEM_REQUEST_BUTTON"]')

    def navigate_to_catalog(self, current_browser, wait_loading_time=3):
        _browser = current_browser.instance._browser.current
        navigate_to_catalog_successful = False
        try:
            _browser.switch_to.frame(None)
            if MainPage().btn_catalog.exists():
                MainPage().btn_catalog.click()
                self.wait_for_loading_complete(wait_loading_time)

                # BENSON: remove original implementation, we will use accurate
                #        iframe location strategy.
                self_service_frame_id = self.get_accurate_frameid(current_browser,
                                                                  self.url_self_service_gadget)
                if self_service_frame_id is not None:
                    logger.debug('Catalog page found self_service frame: {}'
                                 ''.format(self_service_frame_id))
                    _browser.switch_to.frame(self_service_frame_id)
                    logger.debug('Catalog page switched to self_service frame: {}'
                                 ''.format(self_service_frame_id))
                    if self.lbl_all_service.exists(10):
                        navigate_to_catalog_successful = True
                    elif self.lbl_catalog_page.exists(10):
                        navigate_to_catalog_successful = True
                else:
                    logger.error('Catalog page looking for self_service frame failed.')
            else:
                logger.error('Catalog button does not exist in page.')
        except:
            logger.error(
                'Navigating to Catalog page encounters error, error detail: {}'.format(sys.exc_info()))

        return navigate_to_catalog_successful

    def retrieve_blueprint_request_buttons(self, blueprint_names):
        """
         retrieving blueprint request buttons on the fly within catalog page.
        :param blueprint_names: A list of blueprint name.
        :return:A dict of blueprint_name:blueprint_request_button pairs.

        """
        ret = {}
        if isinstance(blueprint_names, str):
            print self.btn_blueprint_req_xpath_template.format(blueprint_names)
            ret.update({blueprint_names: WebButton(xpath=
                                                   self.btn_blueprint_req_xpath_template.format(blueprint_names))})
        elif isinstance(blueprint_names, list):
            for bp_name in blueprint_names:
                ret.update({bp_name: WebButton(xpath=
                                               self.btn_blueprint_req_xpath_template.format(bp_name))})
        else:
            pass

        return ret
