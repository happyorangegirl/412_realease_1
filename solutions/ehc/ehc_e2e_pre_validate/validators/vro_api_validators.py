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

from .vro_api_validator_base import VROAPIValidator


class VROHealthValidator(VROAPIValidator):
    VRO_HEALTH_REST_RELATIVE_URL = 'healthstatus'

    def response_validation(self, response_data):
        health_status = None
        state = response_data.get('state', None)
        if response_data.get('health-status'):
            health_status = response_data['health-status'].get('state', None)

        return (
            state == 'RUNNING' and health_status == 'OK',
            'vRO Health status:(Status:{}, HealthStatus:{})'.format(state, health_status)
        )



class VROEHCPackagesValidator(VROAPIValidator):
    def response_validation(self, response_data):
        result = any(u'vco/api/packages/com.emc.ehc.foundation/' in pkg_str for pkg_str in
                     [pkg['href'] for pkg in response_data['link']])

        return (
            result,
            'EHC foundation package is imported in vRO' if result else 'EHC foundation package is not imported in vRO'
        )


class VROEHCFoundationPluginValidator(VROAPIValidator):
    def response_validation(self, response_data):
        result = any('EHCFoundation' in plugin.get('displayName') for plugin in response_data.get('plugin', {}))

        return (
            result,
            'EHC foundation plugin is installed in vRO' if result else 'EHC foundation plugin is not installed in vRO'
        )

class VROViprPluginValidator(VROAPIValidator):
    def response_validation(self, response_data):
        result = any('EMC ViPR Plugin' in plugin.get('displayName') for plugin in response_data.get('plugin', {}))

        return (result, 'EHC Vipr plugin is installed in vRO' if result else 'EHC Vipr plugin is not installed in vRO')

class VRORP4VMPackageValidator(VROAPIValidator):
    def response_validation(self, response_data):
        result = any(
            u'vco/api/packages/com.emc.ehc.rp4vm/' in pkg_str for pkg_str in
            [pkg['href'] for pkg in response_data['link']]
        )
        return (
            result,
            'EHC RP4VM package is imported in vRO' if result else 'EHC RP4VM package is not imported in vRO'
        )
