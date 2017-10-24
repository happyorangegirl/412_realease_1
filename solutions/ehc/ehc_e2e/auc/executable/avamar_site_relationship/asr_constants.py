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

backup_env_type_prefix_three_copies = '3C'
backup_env_type_prefix_two_copies = '2C'
backup_env_type_prefix_single_copy = '1C'

# Mapping backup_env_type to selection items.
backup_env_type_map = {
    '1C1VC': 'One backup copy. VMs on one site only. (One vCenter). (Local and single-site CA)',
    '2C1VC': 'Two backup copies. VMs move between two sites. (One vCenter). (Stretched cluster CA)',
    '2C2VC': 'Two backup copies. VMs move between two sites. (Two vCenters).',
    '3C2VC': 'Three backup copies. VMs move between three sites. (Two vCenters) (3-site MP)',
    'MC2VC': 'Mixed copies. VMs may move between two sites. (Two vCenters) (RP4VM)'
}

# mapping cluster type to its corresponding backup_env_type.
cluster_type_to_backup_env_type = {'LC1S': '1C1VC', 'CA1S': '1C1VC', 'CA2S': '2C1VC', 'DR2S': '2C2VC', 'MP2S': '2C2VC',
                                   'MP3S': '3C2VC', 'LC2S': 'MC2VC', 'VS1S': '1C1VC', 'VS2S': 'MC2VC'}
