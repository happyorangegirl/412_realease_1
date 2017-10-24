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
from robot.errors import ExecutionFailed
from ehc_e2e.utils.log import log

WF_SETTINGS = 'E2EWF-7-C4-DR2S.config.yaml'


def workflow():
    _global_settings = get_e2e_workflow_conf_path('generic.yaml')
    _wf_settings = get_e2e_workflow_conf_path(WF_SETTINGS)
    wf = RP4VMWorkflow()

    wf.apply_settings_from_files(_global_settings, _wf_settings)
    return wf


def gen_aucs():
    """
    3 AUC request result will failed, maybe backend error:
        cloud_administrator_displays_backup_service_level
        cloud_administrator_run_admin_report
        cloud_administrator_edits_avamar_grid_admin_full
    """
    wf = workflow()

    aucs = (
        wf.cloud_administrator_opens_browser,
        wf.cloud_administrator_login,

        wf.cloud_administrator_adds_avamar_grid,
        wf.cloud_administrator_adds_avamar_site_relationship,
        wf.cloud_administrator_edits_an_avamar_site_relationship,
        wf.cloud_administrator_gets_ASRs_from_vRO,
        wf.cloud_administrator_adds_an_avamar_replication_relationship,
        wf.cloud_administrator_gets_ARRs_from_vRO,
        wf.cloud_administrator_associates_cluster_to_asr,
        wf.cloud_administrator_associates_avamar_proxies_with_cluster,

        wf.cloud_administrator_adds_backup_service_level,
        wf.cloud_administrator_displays_backup_service_level,
        wf.cloud_administrator_run_admin_report,
        wf.cloud_administrator_deletes_backup_service_level,

        wf.cloud_administrator_edits_an_avamar_replication_relationship,
        wf.cloud_administrator_deletes_an_avamar_replication_relationship,
        wf.cloud_administrator_deletes_an_avamar_site_relationship,
        wf.cloud_administrator_edits_avamar_grid,
        wf.cloud_administrator_edits_avamar_grid_admin_full,
        wf.cloud_administrator_deletes_avamar_grid,

        wf.cloud_administrator_logout,
        wf.cloud_administrator_closes_browser,
        wf.clean_up_environment
    )

    _aucs = (
        wf.cloud_administrator_opens_browser,
        wf.cloud_administrator_login,
        # wf.cloud_administrator_adds_vcenter_relationship


        # wf.cloud_administrator_deletes_backup_service_level,
        # wf.cloud_administrator_deletes_an_avamar_replication_relationship,
        # wf.cloud_administrator_deletes_an_avamar_site_relationship,
        # wf.cloud_administrator_deletes_avamar_grid,
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
        if i.__name__ in ('cloud_administrator_adds_backup_service_level',
                          'cloud_administrator_displays_backup_service_level',
                          'cloud_administrator_edits_avamar_grid_admin_full'):
            try:
                func()
            except ExecutionFailed, e:
                print e
        else:
            func()


if __name__ == '__main__':
    main()
    # gen_keywords()

