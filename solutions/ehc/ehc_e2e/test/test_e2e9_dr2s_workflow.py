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

import os

from ehc_e2e.workflow import SRMDRWorkflow

if __name__ == '__main__':
    _cd = os.path.dirname(os.path.realpath(__file__))
    _parent_dir = os.path.abspath(os.path.join(_cd, os.pardir))
    _global = os.path.join(_parent_dir, 'conf/generic.yaml')
    _wf = [
        os.path.join(_parent_dir, 'conf/E2EWF-9-C4-DR2S.config.yaml'),
    ]

    srm_dr = SRMDRWorkflow()
    srm_dr.apply_settings_from_files(_global, *_wf)
    srm_dr.cloud_administrator_opens_browser()
    srm_dr.cloud_administrator_login()
    srm_dr.cloud_administrator_adds_site()
    # srm_dr.cloud_administrator_validates_protection_for_srm_dr_workloads()
    # srm_dr.cloud_administrator_performs_srm_dr_recovery()
    # srm_dr.cloud_administrator_performs_srm_dr_reprotect()
    # srm_dr.cloud_administrator_remediate_manages_srm_dr_protected_workloads()
    # srm_dr.cloud_administrator_closes_browser()
    # srm_dr.reset_settings()
