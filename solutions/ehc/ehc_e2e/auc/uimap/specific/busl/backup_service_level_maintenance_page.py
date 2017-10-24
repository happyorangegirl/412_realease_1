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

from uiacore.modeling.webui.controls import WebLabel, WebTextBox

from ehc_e2e.auc.uimap.extension import WebCombo
from ehc_e2e.auc.uimap.shared.generic import (
    NavigationBar, RequestInfoTab, RequestResult)


class BackupServiceLevelPage(NavigationBar, RequestInfoTab, RequestResult):
    def __init__(self):
        super(BackupServiceLevelPage, self).__init__()

        self.cbo_operation = WebCombo(id='provider-currentAction')
        self.cbo_busl_to_delete = WebCombo(id='provider-SvcLevelToDelete')
        self.cbo_confirm = WebCombo(id='provider-ConfirmDelete')

        self.txt_busl_to_add = WebTextBox(id='provider-ServiceLevelName')
        self.cbo_bkup_schedule_type = WebCombo(id='provider-BackupSchedule')
        self.txt_bkup_daily_time = WebTextBox(id='provider-DailyScheduleTime')
        self.cbo_bkup_weekly_day = WebCombo(id='provider-WeekDay')
        self.cbo_bkup_monthly_week = WebCombo(id='provider-WeekNumber')

        self.cbo_retention_policy = WebCombo(id='provider-RetentionTime')
        self.txt_long_term_retention_years = WebTextBox(id='provider-DefinedLongTermRetentionPolicies')
        self.txt_retention_for_number = WebTextBox(id='provider-RetentionForNumber')
        self.cbo_retention_for_units = WebCombo(id='provider-RetentionCustomPhrase')
        self.txt_retention_until_date = WebTextBox(id='provider-RetainUntil_DATE_BOX-input')
        self.txt_retention_until_time = WebTextBox(id='provider-RetainUntil_TIME_BOX-input')
        self.txt_retention_adv_daily = WebTextBox(id='provider-advDailyForNum')
        self.cbo_retention_dv_daily_unit = WebCombo(id='provider-advDaysKeepFor')
        self.txt_retention_adv_weekly = WebTextBox(id='provider-advWeeklyForNum')
        self.cbo_retention_dv_weekly_unit = WebCombo(id='provider-advKeepForWeeks')
        self.txt_retention_adv_monthly = WebTextBox(id='provider-advMonthlyForNum')
        self.cbo_retention_dv_monthly_unit = WebCombo(id='provider-advKeepForMonths')
        self.txt_retention_adv_yearly = WebTextBox(id='provider-advYearlyForNum')
        self.cbo_retention_dv_yearly_unit = WebCombo(id='provider-advKeepForYears')

        self.cbo_rp_schedule_type = WebCombo(id='provider-ReplicationSchedule')
        self.txt_rp_daily_time = WebTextBox(id='provider-ReplicationDailyScheduleTime')
        self.cbo_rp_weekly_day = WebCombo(id='provider-ReplicationWeekDay')
        self.cbo_rp_monthly_week = WebCombo(id='provider-ReplicationWeekNumber')

        self.lbl_review_action = WebLabel(id='provider-reviewAction')
