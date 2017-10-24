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

from .vro_action_validator_base import VROActionValidator


class VROVCenterValidator(VROActionValidator):
    def response_validation(self, response_data):
        vcenter_fqdns = self._kwargs.get('vcenter_fqdns', [])
        vro_vcenters = []
        if response_data.get('value', {}) and response_data['value'].get('array', {}) and \
                response_data['value']['array'].get('elements', []):
            vro_vcenters = [vc['string']['value'] for vc in response_data['value']['array']['elements']]
            if vro_vcenters:
                return (
                    all(fqdn in vro_vcenters for fqdn in vcenter_fqdns),
                    'Specified vCenter fqdn:{}, vRO configured vCenter fqdn:{}'.format(
                        ', '.join(vcenter_fqdns), ', '.join(vro_vcenters))
                )
            else:
                return (False, 'No vCenter configured in vRO yet, please check Dynamic Type of vRO to double confirm.')

        return (
            False,
            'Failed to get vRO configured vCenter information, Specified vCenter fqdn:{}'.format(
                ', '.join(vcenter_fqdns))
        )
