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


from ehc_e2e.auc.uimap.extension import WebCombo
from ehc_e2e.auc.uimap.shared.generic import (RequestInfoTab, SelectOperationTab,
                                              NavigationBar, RequestResult)
from uiacore.modeling.webui.controls import WebCheckbox, WebLabel


class PreFailoverMaintenancePage(RequestInfoTab, SelectOperationTab,
                                 NavigationBar, RequestResult):
    def __init__(self):
        super(PreFailoverMaintenancePage, self).__init__()

        self.cbo_operation = WebCombo(id='provider-preFailoverAction')

        self.cbo_stage_bussiness_group = WebCombo(id='provider-stageOwner')

        self.cbo_unstage_bussiness_group = WebCombo(id='provider-unstageOwner')

        self.lst_stage_cgs = WebLabel(id='provider-consistencyGroups')

        self.lst_unstage_cgs = WebLabel(id='provider-unstageConsistencyGroups')

        self.cbo_stage_confirm = WebCombo(id='provider-stageConfirmDeny')

        self.cbo_unstage_confirm = WebCombo(id='provider-unstageConfirmDeny')

    def get_cg_checkbox_list(self, cgs_dropdown, cglist):
        if cglist:
            _checkbox_list = []
            for item in cglist:
                _checkbox = self._get_corresponding_checkbox(cgs_dropdown, item)
                if _checkbox:
                    _checkbox_list.append(_checkbox)
                else:
                    raise ValueError('Unable to locate checkbox for vm: {}'.format(item))
            return _checkbox_list
        else:
            raise ValueError('Input arg vm_list is None.')

    def _get_corresponding_checkbox(self, container, visible_text):
        if container.current:
            _checkbox_list = container.current.find_elements_by_class_name('gwt-CheckBox')
            if len(_checkbox_list) > 0:
                for item in _checkbox_list:
                    try:
                        _label = item.find_element_by_tag_name('label')
                        if _label.text.find(visible_text) > -1:
                            return WebCheckbox(element=item.find_element_by_tag_name('input'))
                    except:
                        pass
        return None
