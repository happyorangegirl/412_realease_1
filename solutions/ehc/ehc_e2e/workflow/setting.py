#  Copyright 2016 EMC HCE SW Automation
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

# Indicate whether to fail the whole workflow if any failure here
#   True:   Workflow will continue execution until end even if failure occurs during execution.
#   False:  Workflow will stop execution if failure occurs during execution.
workflow_continue_on_failure = False
cleanup_before_workflow_execution = False

# Indicate whether to take screen shot if encounter assert error or exception
# True: take screen shot
# False: don't take screen shot
take_screen_shot_on_failure = True

# Indicate if resume will use workflow yaml data to merge into dump data.
# True: will use workflow yaml data to merge into dump data.
# False: will use dump file data directly.
resume_also_include_workflow_yaml_file = False
