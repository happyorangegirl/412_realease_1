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
import logging

PRE_STEPS = ['Opens Browser To Resume', 'Login Browser To Resume']


class EHCAutoCLIListener(object):

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        print '*********listener started***************'
        # Setup also requires one keyword, so the starter is -1
        self.step_index = -1
        self.keyword_first_failed = ''
        self.is_first = True
        self.fail_step = 0
        self.pre_step_executed = 0

    def start_keyword(self, name, attrs):
        self.step_index += 1
        if attrs['kwname'] in PRE_STEPS:
            self.pre_step_executed += 1

    def end_keyword(self, name, attrs):
        status = attrs['status']
        # save first failed keyword name as failed step name,
        # because it will go back to execute parent keyword after sub-keyword failed.
        if status == 'FAIL' and self.is_first:
            self.fail_step = self.step_index
            self.keyword_first_failed = attrs['kwname']
            self.is_first = False

    def close(self):

        if self.fail_step > 0:
            # don't count pre-steps: login and open browser into fail_step
            self.fail_step -= self.pre_step_executed
            # if pre step failed, will still start from steps follow pre step.
            if self.keyword_first_failed in PRE_STEPS:
                self.fail_step += 1
            print ''
            print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
            print '@ {} -- Failed                   '.format(self.keyword_first_failed)
            print '@ Workflow can be resumed at step {}'.format(self.fail_step)
            print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
            print ''
