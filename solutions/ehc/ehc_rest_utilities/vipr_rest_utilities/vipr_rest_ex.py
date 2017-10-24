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

import logging
import time
from vipr_rest_base import ViPRRestBase
from ehc_rest_utilities.parameters.vipr_rest_apis import VOLUME_API, FILTER, EXPORT_API


class ViPRRestEx(ViPRRestBase):

    def find_volume_id(self, vol_name):
        json_data = self.vipr_session.call_api_json(
            'GET', '{host}/{api}/{filter}'.format(host=self.host, api=VOLUME_API,
                                                  filter=FILTER.format(key='name', value=vol_name)), 200)
        if not json_data:
            return None

        for volume in json_data.get('resource', []):
            if vol_name == volume.get('match'):
                return volume['id']

        logging.warning('Volume {0} not found in ViPR'.format(vol_name))
        return None

    def get_export_id_for_volume(self,vol_name):
        vol_id = self.find_volume_id(vol_name)
        json_data = self.vipr_session.call_api_json(
            'GET', '{host}/{api}/{vol_id}/exports'.format(host=self.host, api=VOLUME_API, vol_id=vol_id),200)
        if not json_data:
            return None
        for itl in json_data.get('itl', []):
            export = itl.get('export')
            return export['id']
    
    def remove_volume_from_export_group(self, volume_name, timeout=300, interval=10):
        volume_id = self.find_volume_id(volume_name)
        if not volume_id:
            return False
        export_id = self.get_export_id_for_volume(volume_name)
        if not export_id:
            return False
        update_exports = {
        "cluster_changes": {},
        "host_changes": {},
        "initiator_changes": {},
        "volume_changes": {"remove":[volume_id]}
        }
        remove_vol_from_export = self.vipr_session.call_api_json(
            'PUT', '{host}/{api}/{id}'.format(host=self.host, api=EXPORT_API, id=export_id,), 200,
            json=update_exports)
        time.sleep(40)
        return remove_vol_from_export   
        
    def get_vols_in_project(self, project_id):
        json_data = self.vipr_session.call_api_json('GET', '{host}/{api}/{project_id}/resources'.format(
        host=self.host, api=PROJECT_API, project_id=project_id), 200)
        if not json_data:
            return None
        volumes=[]
        for name in json_data.get('project_resource'):
            if name.get('resource_type') == 'volume':
                volumes.append(name.get('name'))
        return volumes
        
    def delete_volume(self, volume_name, timeout=300, interval=10):
        volume_id = self.find_volume_id(volume_name)
        if not volume_id:
            return False
        volume = self.vipr_session.call_api_json(
            'GET', '{host}/{api}/{id}'.format(host=self.host, api=VOLUME_API, id=volume_id), 200)
        if not volume:
            return False

        delete_volume_dict = {
            'project': volume['project']['id'],
            'volumes': volume_id,
            'deletionType': 'FULL'}

        order = self.order_catalog_service('RemoveBlockVolumes', **delete_volume_dict)
        if not order:
            return False

        order_id = order.get('id')
        if not order_id:
            logging.error('ViPR REST API does not return valid values. Please check')
            return False

        return self.check_order_status(order_id, timeout, interval)
