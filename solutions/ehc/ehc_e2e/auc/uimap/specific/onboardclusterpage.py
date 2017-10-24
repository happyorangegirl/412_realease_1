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

from uiacore.modeling.webui.controls import WebTextBox, WebButton, WebLabel, WebLink
from ehc_e2e.auc.uimap.shared.basepage import BasePage
from ehc_e2e.auc.uimap.shared.loadingwindow import LoadingWindow


class OnboardClusterPage(BasePage):

    def __init__(self):
        super(OnboardClusterPage, self).__init__()
        self.login_window = LoadingWindow()
        # onboard local cluster data item
        self.lbl_description = WebLabel(xpath='//div[@title="Description:"]')
        self.txt_description = WebTextBox(id='description')
        self.btn_next = WebButton(id='next')
        self.lbl_cluster_action_to_perform = WebLabel(xpath='//div[@title="Cluster action to perform:"]')
        self.lnk_cluster_action_to_perform_menu = WebLink(
            xpath='//*[@id="provider-mainAction"]/tbody/tr/td[@align="right"]')
        self.lnk_cluster_action_to_perform_dropdownlist = WebLink(
            xpath='//*[@class="listBoxEx"]/div/table/tbody')
        self.lbl_select_a_hwi = WebLabel(xpath='//div[@title="Select a Hardware Island:"]')
        self.lnk_select_a_local_hwi_menu = WebLink(
            xpath='//*[@id="provider-Local_hwIslandSelected"]/tbody/tr/td[@align="right"]')
        self.lnk_select_local_unprepared_cluster_menu = WebLink(
            xpath='//*[@id="provider-Local_clusterName"]/tbody/tr/td[@align="right"]')
        self.lbl_action_chosen = WebLabel(xpath='//div[@title="Action:"]')
        self.lbl_txt_action_chosen = WebLabel(id="provider-reviewAction")
        self.lbl_txt_cluster_name = WebLabel(id="provider-reviewCluster")
        self.btn_submit = WebButton(id="submit")
        self.lbl_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(id="CONFIRMATION_OK_BUTTON")
        self.btn_save = WebButton(id="save")
        self.xpath_btn_save = '//*[@id="save"]'

        # onboard vsan cluster data item
        self.lnk_select_a_hwi_menu = WebLink(
            xpath='//*[@id="provider-vsan_hwIslandSelected"]/tbody/tr/td[@align="right"]')
        self.lnk_select_unprepared_cluster_menu = WebLink(
            xpath='//*[@id="provider-vsan_clusterName"]/tbody/tr/td[@align="right"]')

        # onboard mp cluster data item
        self.lnk_select_hwi_1_mp_menu = WebLink(
            xpath='//*[@id="provider-DR_MP_hwIsland1"]/tbody/tr/td[@align="right"]')
        self.lnk_inter_site_vs_intra_site_mp_menu = WebLink(
            xpath='//*[@id="provider-DR_MP_siteCATypeChoice"]/tbody/tr/td[@align="right"]')
        self.lnk_select_hwi_2_mp_menu = WebLink(
            xpath='//*[@id="provider-DR_MP_hwIsland2"]/tbody/tr/td[@align="right"]')
        self.lnk_unprepared_protected_cluster_mp_menu = WebLink(
            xpath='//*[@id="provider-DR_MP_clusterName1"]/tbody/tr/td[@align="right"]')
        self.lbl_hosts_from_cluster_that_are_from_hwi_1 = WebLabel(id="provider-DR_MP_hostListHwIsland1")
        self.lbl_hosts_from_cluster_that_are_from_hwi_2 = WebLabel(id="provider-DR_MP_hostListHwIsland2")
        self.lnk_select_hwi_3_mp_menu = WebLink(
            xpath='//*[@id="provider-DR_MP_recoverySiteHW"]/tbody/tr/td[@align="right"]')
        self.btn_unprepared_recovery_cluster_mp_menu = WebLink(
            xpath='//*[@id="provider-DR_MP_clusterName2"]/tbody/tr/td[@align="right"]')

        # onboard ca cluster data item
        self.lbl_select_hwi_1 = WebLabel(xpath='//div[@title="Select Hardware Island 1:"]')
        self.lnk_select_hwi_1_menu = WebLink(
            xpath='//*[@id="provider-CA_hwIslandSelected"]/tbody/tr/td[@align="right"]')
        self.lnk_unprepared_cluster_menu = WebLink(
            xpath='//*[@id="provider-CA_clusterName"]/tbody/tr/td[@align="right"]')
        self.lnk_choose_inter_site_vs_intra_site_munu = WebLink(
            xpath='//*[@id="provider-CA_CASiteType"]/tbody/tr/td[@align="right"]')
        self.lnk_select_hwi_2_menu = WebLink(
            xpath='//*[@id="provider-CA_hwIslandSelected2"]/tbody/tr/td[@align="right"]')
        self.lbl_select_hosts_for_hardware_island_1 = WebLabel(id="provider-CA_hostListHwIsland1")
        self.lbl_select_hosts_for_hardware_island_2 = WebLabel(id="provider-CA_hostListHwIsland2")

        # onboard_dr_cluster_data_item
        self.lbl_select_a_hwi_for_the_protected_cluster = WebLabel(
            xpath='//div[@title="Select a Hardware Island for the Protected cluster :"]')
        self.lnk_select_a_hwi_for_the_protected_cluster_menu = WebLink(
            xpath='//*[@id="provider-DR_hwIsland1"]/tbody/tr/td[@align="right"]')
        self.lnk_select_dropdownlist = WebLink(
            xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table/tbody')
        self.lnk_select_unprepared_protected_cluster_menu = WebLink(
            xpath='//*[@id="provider-DR_clusterName1"]/tbody/tr/td[@align="right"]')
        self.lnk_select_the_hwi_for_the_recovery_cluster_menu = WebLink(
            xpath='//*[@id="provider-DR_hwIsland2"]/tbody/tr/td[@align="right"]')
        self.lnk_select_unprepared_recovery_cluster_menu = WebLink(
            xpath='//*[@id="provider-DR_clusterName2"]/tbody/tr/td[@align="right"]')

        # Delete cluster
        self.btn_select_cluster = WebButton(xpath='//*[@id="provider-clusterToDelete"]/tbody/tr/td[2]')
        self.btn_confirm_action = WebButton(xpath='//*[@id="provider-deleteConfirmation"]/tbody/tr/td[2]')
        self.lst_action_values = WebLabel(xpath='//div[@class="popupContent"]'
                                                '/div[@class="listBoxEx"]/div/table')

        # Edit cluster hwi
        self.btn_edit_cluster_hwi = WebButton(xpath='//*[@id="provider-clusterToEditHWI"]/tbody/tr/td[@align="right"]')
        self.btn_hwi_1 = WebButton(xpath='//*[@id="provider-clusterToEditHWINewHWI1"]/tbody/tr/td[@align="right"]')
        self.btn_hwi_2 = WebButton(xpath='//*[@id="provider-clusterToEditHWINewHWI2"]/tbody/tr/td[@align="right"]')
        self.xpath_btn_hwi_2 = '//*[@id="provider-clusterToEditHWINewHWI2"]/tbody/tr/td[@align="right"]'
        self.xpath_btn_hwi_2_hidden =\
            '//*[@id="provider-clusterToEditHWINewHWI2" and @aria-hidden="true"]/tbody/tr/td[@align="right"]'

        # Edit cluster site
        self.btn_edit_cluster_site = WebButton(xpath='//*[@id="provider-clusterToEdit"]/tbody/tr/td[@align="right"]')
        self.btn_site = WebButton(xpath='//*[@id="provider-clusterToEditNewSiteName"]/tbody/tr/td[@align="right"]')
        self.btn_hwi = WebButton(xpath='//*[@id="provider-clusterToEditNewHWI1"]/tbody/tr/td[@align="right"]')

        # Associate cluster to ASR
        self.btn_select_cluster_to_associate = WebButton(
            xpath='//*[@id="provider-ASR_clusterName"]/tbody/tr/td[2]'
        )
        self.btn_select_asr = WebButton(
            xpath='//*[@id="provider-ASR_asrName"]/tbody/tr/td[2]'
        )