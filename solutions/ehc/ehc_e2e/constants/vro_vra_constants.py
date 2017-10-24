# vro_constants.py

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
"""
Description: This provides constants for VMware vRO related APIs.

"""


# vRO constants.
PROTOCOL = 'https://'
PORT = ':8281'
DYNAMIC_TYPES_API = '/vco/api/inventory/DynamicTypes/DynamicNamespaceDefinition/EHC/'
SITE_API = 'EHC.SiteFolder/Sites/'
VCENTER_API = 'EHC.vCenterFolder/vCenters/'
AVAMARGRID_API = 'EHC.AvamarGridFolder/AvamarGrids/'
HARDWARE_ISLAND_API = 'EHC.HardwareIslandFolder/HardwareIslands/'
CLUSTER_API = 'EHC.ClusterFolder/Clusters'
ASR_ISLAND_API = 'EHC.ASRFolder/ASRs/'
RP4VM_POLICY_API = 'EHC.RP4VMPolicyFolder/RP4VMPolicies'
HTTP_SUCCESS_RESPONSE = 200

#vRA constants.
DEPLOYED_MACHINE_ITEMS = 'catalog-service/api/consumer/resources/types/Infrastructure.Machine'

