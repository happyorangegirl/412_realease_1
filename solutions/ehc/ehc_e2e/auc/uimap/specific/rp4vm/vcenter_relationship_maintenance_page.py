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

from uiacore.modeling.webui.controls import WebTextBox, WebLabel

from ehc_e2e.auc.uimap.extension import WebCombo, WebFrame
from ehc_e2e.auc.uimap.shared.generic import (
    NavigationBar, RequestInfoTab, SelectOperationTab, RequestResult)


class vCenterInfoTab(object):
    def __init__(self):
        super(vCenterInfoTab, self).__init__()

        self.cbo_protected_vcenter = WebCombo(id='provider-ProtectedVCenterDTName')
        self.txt_prorected_vcenter_username = WebTextBox(id='provider-ProtectedVCenterUsername')
        self.txt_prorected_vcenter_pwd = WebTextBox(id='provider-ProtectedVCenterPassword')
        self.cbo_recovery_vcenter = WebCombo(id='provider-RecoveryVCenterDTName')
        self.txt_recovery_vcenter_username = WebTextBox(id='provider-RecoveryVCenterUsername')
        self.txt_recovery_vcenter_pwd = WebTextBox(id='provider-RecoveryVCenterPassword')


class NSXMgrHostConfigTab(object):
    def __init__(self):
        super(NSXMgrHostConfigTab, self).__init__()

        self.cbo_NSX_available = WebCombo(id='provider-NSXAvailableRP4VM')
        self.txt_protect_site_NSX_mgr_url = WebTextBox(id='provider-protectedNSXHostURLRP4VM')
        self.txt_protect_site_NSX_mgr_user = WebTextBox(id='provider-protectedNSXuserNameRP4VM')
        self.txt_protect_site_NSX_mgr_pwd = WebTextBox(id='provider-protectedNSXPasswordRP4VM')
        self.txt_recovery_site_NSX_mgr_url = WebTextBox(id='provider-NSXRecoverySiteHostURLRP4VM')
        self.txt_recovery_site_NSX_mgr_user = WebTextBox(id='provider-recoveryNSXUserNameRP4VM')
        self.txt_recovery_site_NSX_mgr_pwd = WebTextBox(id='provider-recoveryNSXPasswordRP4VM')


class ReviewAndSubmitTab(object):
    def __init__(self):
        super(ReviewAndSubmitTab, self).__init__()

        self.lbl_operation_type = WebLabel(id='provider-reviewId')
        self.lbl_protected_vcenter_name = WebLabel(id='provider-protectedvCenterName1')
        self.lbl_recovery_vcenter_name = WebLabel(id='provider-recoveryvCenterName1')


class vCenterRelationshipMaintenancePage(
        RequestInfoTab, SelectOperationTab,
        vCenterInfoTab, NavigationBar,
        RequestResult, NSXMgrHostConfigTab,
        ReviewAndSubmitTab
):
    def __init__(self):
        super(vCenterRelationshipMaintenancePage, self).__init__()

        self.cbo_confirm_vcenter_relationship = WebCombo(id='provider-confirmation')
        self.frm_catalog = WebFrame(onload='selfservice/SelfServiceGadget.gadget.xml')
