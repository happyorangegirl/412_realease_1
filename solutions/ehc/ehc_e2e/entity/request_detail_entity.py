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


class RequestDetailEntity(object):

    def __init__(self, request=None, item=None, description=None, cost=None,
                 least_cost=None, submitter=None, submitted=None, last_updated=None,
                 business_group=None, status=None, status_details=None):
        self.request = request
        self.item = item
        self.description = description
        self.cost = cost
        self.least_cost = least_cost
        self.submitter = submitter
        self.submitted = submitted
        self.last_updated = last_updated
        self.business_group = business_group
        self.status = status
        self.status_details = status_details
