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

from uiacore.modeling.webui.controls import WebTextBox, WebButton

from ehc_e2e.auc.uimap.extension import WebCombo
from ehc_e2e.auc.uimap.shared.generic import (
    NavigationBar, RequestInfoTab, RequestResult)


class PostFailoverUpdaterPage(
        NavigationBar, RequestInfoTab, RequestResult
):
    def __init__(self):
        super(PostFailoverUpdaterPage, self).__init__()

        self.cbo_recovery_cluster = WebCombo(id='provider-DesComputeClusterName')
        self.txt_email = WebTextBox(id='provider-EmailTarget')
        self.btn_next = WebButton(id='next')
