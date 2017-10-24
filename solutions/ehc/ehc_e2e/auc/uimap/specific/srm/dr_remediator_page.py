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

from uiacore.modeling.webui.controls import WebCheckbox, WebLabel, WebTextBox
from robot.api import logger
from ehc_e2e.auc.uimap.extension import WebCombo
from ehc_e2e.auc.uimap.shared.generic import (
    NavigationBar, RequestInfoTab, RequestResult)


class DRRemediatorPage(
        NavigationBar, RequestInfoTab, RequestResult
):
    def __init__(self, datastores_to_protect=None, vms_to_protect=None):
        super(DRRemediatorPage, self).__init__()

        self.cbo_protected_cluster = WebCombo(id='provider-ProtectedCluster')

        self.lst_unprotected_datastores = WebLabel(id='provider-UnprotectedDatastores')

        self.lst_unprotected_vms = WebLabel(id='provider-UnprotectedMachines')

        self.txt_site_status = WebTextBox(id='provider-SiteStatus')

        self.chk_protect_all_datastores = WebCheckbox(id='provider-ProtectDatastores')

        self.chk_protect_all_vms = WebCheckbox(id='provider-ProtectMachines')

        self.datastore_list = datastores_to_protect

        self.vm_list = vms_to_protect

    def get_datastores_checkbox_list(self):
        if self.datastore_list:
            _checkbox_list = []
            for item in self.datastore_list:
                _checkbox = self._get_corresponding_checkbox(self.lst_unprotected_datastores, item)
                if _checkbox:
                    _checkbox_list.append(_checkbox)
                else:
                    logger.warn('Datastore {0} did not need to be protected, '
                                'not find in DropDownList choose individual datastores to protect.'.format(item))
            return _checkbox_list
        else:
            raise ValueError('Input arg datastore_list is None.')

    def get_vms_checkbox_list(self):
        if self.vm_list:
            _checkbox_list = []
            for item in self.vm_list:
                _checkbox = self._get_corresponding_checkbox(self.lst_unprotected_vms, item)
                if _checkbox:
                    _checkbox_list.append(_checkbox)
                else:
                    logger.warn('VM {0} did not need to be protected, '
                                'not find in DropDownList choose individual machines to protect.'.format(item))
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
