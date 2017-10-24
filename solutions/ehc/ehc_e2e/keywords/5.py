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

import string
from ehc_e2e.workflow import BaseWorkflow, RP4VMWorkflow
from ehc_e2e.utils.dir import get_e2e_workflow_conf_path

WF_SETTINGS = 'E2EWF-5.config.yaml'


def workflow():
    _global_settings = get_e2e_workflow_conf_path('generic.yaml')
    _wf_settings = get_e2e_workflow_conf_path(WF_SETTINGS)
    wf = BaseWorkflow()

    wf.apply_settings_from_files(_global_settings, _wf_settings)
    return wf


def gen_aucs():
    wf = workflow()
    aucs = (
        wf.cloud_administrator_opens_browser,
        wf.cloud_administrator_login,

        wf.cloud_administrator_adds_site,
        wf.cloud_administrator_adds_vcenter,
        wf.cloud_administrator_adds_hwi,

        # AUC  # 5 Onboard DR2S cluster

        wf.cloud_administrator_onboard_cluster,

        # AUC  # 7 Onboard CA1S cluster
        # AUC  # 8 Onboard CA2S cluster
        # AUC  # 9 Onboard MP2S cluster
        # AUC  # 10 Onboard MP3S cluster
        wf.cloud_administrator_provisions_cloud_storage,
        wf.cloud_administrator_deletes_datastore,
        wf.cloud_administrator_logout,
        wf.cloud_administrator_closes_browser,
        wf.clean_up_environment
    )
    return aucs


def gen_keywords():
    aucs = gen_aucs()
    for i in aucs:
        name = i.__name__
        print ' '.join([string.capitalize(j) for j in name.split('_')])


def main():
    wf = workflow()
    aucs = gen_aucs()
    for i in aucs:
        func = getattr(wf, i.__name__)
        func()


if __name__ == '__main__':
    main()
    # gen_keywords()
