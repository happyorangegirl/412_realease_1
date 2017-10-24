"""
     Copyright 2016 EMC GSE SW Automation

     Licensed under the Apache License, Version 2.0 (the "License");
     you may not use this file except in compliance with the License.
     You may obtain a copy of the License at

         http://www.apache.org/licenses/LICENSE-2.0

     Unless required by applicable law or agreed to in writing, software
     distributed under the License is distributed on an "AS IS" BASIS,
     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
     See the License for the specific language governing permissions and
     limitations under the License.
"""


from robot.api import logger
from ehc_e2e.workflow.baseworkflow import BaseWorkflow
from ehc_e2e.auc.executable.avamar_fail_action import AvamarFailAction
from ehc_e2e.auc.executable.generic import RequestChecker


class AvamarFailActionWorkflow(BaseWorkflow):

    def cloud_administrator_failovers_avamar_grids_after_site_failure(self):
        cur_browser = self.wf_context.shared.current_browser
        kwargs = {
            'data': self.wf_context.added_sites[0]
        }
        AvamarFailAction(
            self.cloud_administrator_failovers_avamar_grids_after_site_failure.__name__,
            method_name=AvamarFailAction.Func.FAILOVER_SITE,
            browser=cur_browser,
            **kwargs
        ).run()

        logger.info("Failover Site {data}".format(data=kwargs["data"]), False, True)

        RequestChecker(self.cloud_administrator_failovers_avamar_grids_after_site_failure.__name__,
                       description=AvamarFailAction.Func.FAILOVER_SITE).run()

    def cloud_administrator_failbacks_avamar_policies_after_site_restoration(self):
        cur_browser = self.wf_context.shared.current_browser
        kwargs = {
            'data': self.wf_context.added_sites[0]
        }
        AvamarFailAction(
            self.cloud_administrator_failbacks_avamar_policies_after_site_restoration.__name__,
            method_name=AvamarFailAction.Func.FAILBACK_SITE,
            browser=cur_browser,
            **kwargs
        ).run()

        logger.info("Failback Site {data}".format(data=kwargs["data"]), False, True)

        RequestChecker(self.cloud_administrator_failbacks_avamar_policies_after_site_restoration.__name__,
                       description=AvamarFailAction.Func.FAILBACK_SITE).run()

    def cloud_administrator_failovers_avamar_policies_for_offline_avamar_grid(self):
        cur_browser = self.wf_context.shared.current_browser
        kwargs = {
            'data': self.wf_context.add_avamar_grid[0].avamar_grid_name
                    # self.wf_context.added_avamar_grid[0]
        }
        AvamarFailAction(
            self.cloud_administrator_failovers_avamar_policies_for_offline_avamar_grid.__name__,
            method_name=AvamarFailAction.Func.FAILOVER_GRID,
            browser=cur_browser,
            **kwargs
        ).run()

        logger.info("Failover Grid {data}".format(data=kwargs["data"]), False, True)

        RequestChecker(self.cloud_administrator_failovers_avamar_policies_for_offline_avamar_grid.__name__,
                       description=AvamarFailAction.Func.FAILOVER_GRID).run()

    def cloud_administrator_failbacks_avamar_policies_after_restoring_avamar_grid(self):
        cur_browser = self.wf_context.shared.current_browser
        kwargs = {
            'data': self.wf_context.add_avamar_grid[0].avamar_grid_name
        }
        AvamarFailAction(
            self.cloud_administrator_failbacks_avamar_policies_after_restoring_avamar_grid.__name__,
            method_name=AvamarFailAction.Func.FAILBACK_GRID,
            browser=cur_browser,
            **kwargs
        ).run()

        logger.info("Failback Grid {data}".format(data=kwargs["data"]), False, True)

        RequestChecker(self.cloud_administrator_failbacks_avamar_policies_after_restoring_avamar_grid.__name__,
                       description=AvamarFailAction.Func.FAILBACK_GRID).run()
