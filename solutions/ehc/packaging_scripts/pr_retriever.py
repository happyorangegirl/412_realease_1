
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

import sys
import requests
from requests.auth import HTTPBasicAuth

BITBUCKET_PULL_REQUEST_MERGED_URL = 'https://pie6.rtp.lab.emc.com/rest/api/1.0/projects/TAF/repos/solutions/pull-requests?state=MERGED'
BITBUCKET_BRANCHES = 'https://pie6.rtp.lab.emc.com/rest/api/1.0/projects/TAF/repos/solutions/branches'

BITBUCKET_USER='e2e_auto1'
BITBUCKET_PASSWORD='Password123!'

class BitbucketInfo(object):
    def __init__(self, user, password, **kwargs):
        requests.packages.urllib3.disable_warnings()
        self._auth = HTTPBasicAuth(user, password)
        self._kwargs = kwargs
        
    def get_latest_pr(self, target_branch_head_ref):
        requests.packages.urllib3.disable_warnings()
        r = None
        try:
            r = requests.get(
                BITBUCKET_PULL_REQUEST_MERGED_URL, auth=self._auth, verify=False)
        except:
            print '[ERROR] Encountered error when connecting to Bitbucket server..., error:{}'.format(sys.exc_info())
        k = r.json()
        pr_list = k['values']
        description = title = owner = ''
        found_pr_for_target_ref = False
        if target_branch_head_ref and target_branch_head_ref not in self.get_all_branches():
            print '[ERROR] Specified target_branch_head_ref: {} is not in Git repo.'.format(target_branch_head_ref)
        if len(pr_list) > 0:
            for pr in pr_list:
                title = pr['title']
                owner = pr['author']['user']['emailAddress']
                if 'description' in pr:
                    description = pr['description']
                if not target_branch_head_ref:
                    break
                else:
                    if pr['toRef']['id'] == target_branch_head_ref:
                        found_pr_for_target_ref = True
                        break

        if target_branch_head_ref and not found_pr_for_target_ref:
            print '[ERROR] Failed to find latest PR merged to ref:{}'.format(target_branch_head_ref)
        print 'Commit title: \n{}\n\nOwner: \n{}\n\nDetails: \n{}'.format(title, owner, description)


    def get_all_branches(self):
        requests.packages.urllib3.disable_warnings()
        r = None
        try:
            r = requests.get(BITBUCKET_BRANCHES, auth=self._auth, **self._kwargs)
        except:
            print '[ERROR] Encountered error when connecting to Bitbucket server..., error:{}'.format(sys.exc_info())
        k = r.json()
        branche_ref_names = [branch['id'] for branch in k['values']]
        return branche_ref_names


if __name__=='__main__':
    target_ref = None
    if len(sys.argv) >= 2 :
        target_ref = sys.argv[1] #'refs/heads/release/ehc412_release_scenario'
    btbkt = BitbucketInfo(BITBUCKET_USER, BITBUCKET_PASSWORD, verify=False)
    btbkt.get_latest_pr(target_ref)


