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

from uiacore.modeling.webui.controls import (WebTextBox, WebButton,
                                             WebLabel)
from ehc_e2e.auc.uimap.shared.basepage import BasePage


class ClusterMaintenancePage(BasePage):
    """ This class is defined to indicate elements' identities in Delete Cluster Page.

    Attributes:
        # lbl_catalog: catalog label element.
        # lbl_cluster_title: cluster maintenance title element.
        # lnk_cluster_request: cluster maintenance request link element.

        txt_description: cluster operation description textbox element.
        txt_reason: cluster operation reason textbox element.
        btn_next: next button element.

        lbl_cluster_action: cluster action label element.
        btn_cluster_action: cluster action button element.
        lst_action_values: cluster actions provided by the web page.
        lbl_select_cluster: select cluster label element.
        btn_select_cluster: select cluster button element.
        # select_cluster_values_list: cluster names provided by the web page.

        lbl_confirm_action: confirm cluster action label.
        btn_confirm_action: confirm cluster action button.
        # confirm_action_values_list: confirm or deny the action.

        lbl_review_chosen_action: review the chosen action label element.
        lbl_review_cluster_name: review the chosen cluster name label element.

        btn_submit: submit button element.
        btn_ok: ok button element.
    """

    def __init__(self):
        super(ClusterMaintenancePage, self).__init__()
        self.txt_description = WebTextBox(id="description")
        self.txt_reason = WebTextBox(id="reasons")
        self.btn_next = WebButton(id="next")

        self.btn_cluster_action = WebButton(xpath='//*[@id="provider-mainAction"]/tbody/tr/td[2]')
        self.lst_action_values = WebLabel(xpath='//div[@class="popupContent"]'
                                                '/div[@class="listBoxEx"]/div/table')

        # Delete cluster
        self.btn_select_cluster = WebButton(xpath='//*[@id="provider-clusterToDelete"]/tbody/tr/td[2]')
        self.btn_confirm_action = WebButton(xpath='//*[@id="provider-deleteConfirmation"]/tbody/tr/td[2]')

        # Associate cluster to ASR
        self.btn_select_cluster_to_associate = WebButton(
            xpath='//*[@id="provider-ASR_clusterName"]/tbody/tr/td[2]'
        )
        self.btn_select_asr = WebButton(
            xpath='//*[@id="provider-ASR_asrName"]/tbody/tr/td[2]'
        )

        # Associate avamar proxies with cluster
        self.btn_select_cluster_to_avamar = WebButton(
            xpath='//*[@id="provider-Proxy_clusterName"]/tbody/tr/td[2]'
        )
        self.tbl_select_avamar_proxies = WebLabel(
            xpath='//*[@id="provider-Proxy_proxies"]/div/table'
        )

        self.lbl_review_chosen_action = WebLabel(id="provider-reviewAction")
        self.lbl_review_cluster_name = WebLabel(id="provider-reviewCluster")

        self.btn_save = WebButton(id="save")
        self.btn_submit = WebButton(id="submit")
        self.btn_ok = WebButton(id="CONFIRMATION_OK_BUTTON")
        self.btn_cancel = WebButton(id="cancel")
