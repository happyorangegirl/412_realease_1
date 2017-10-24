import sys
import logging
import requests
from requests.auth import HTTPBasicAuth

logging.basicConfig(level=logging.INFO)


class EHCObjectFetcher(object):
    """
      EHC object in vRO.Inventory.DynamicTypes
    """
    _vro_folder_path = 'https://{host}:8281/vco/api/inventory/DynamicTypes/DynamicNamespaceDefinition/EHC/'
    _vra_reservation_path = 'https://{host}/reservation-service/api/reservations/policies'
    __vCO_http_headers = {
        'Accept': "application/json",
        'Content-Type': "application/xml;charset=UTF-8"
    }

    def __init__(self, host, username, password):
        self.auth = HTTPBasicAuth(username, password)
        self.host = host

    def _get_response(self, target_folder):
        """
        get request from target url
        :param target_folder: target EHC objedct folder path string
        :return: target EHC objedct name list
        """
        vro_folder = self._vro_folder_path.format(host=self.host)
        url = ''.join((vro_folder, target_folder))
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url, auth=self.auth, headers=self.__vCO_http_headers, verify=False)
        try:
            response_dic = response.json()
            return response_dic
        except:
            logging.error('Get response failed. The target URL is {} .'.format(url))
            raise Exception(response, response.reason)

    def get_object_names(self, target_folder):

        elements = self._get_ehc_object(target_folder)
        names = []
        if elements:
            names = [element.get('name') for element in elements if 'name' in element]
        return names

    def _get_ehc_object(self, target_folder):
        """
        get common EHC object
        :param target_folder:
        :return: list
        """
        try:
            response_dic = self._get_response(target_folder)
            if not response_dic:
                raise RuntimeError('Failed to retrieve Dynamic Types from vRO (Suggest to reboot vRO machine).')

            relation = response_dic.get('relations')
            element_list = relation.get('link')

            elements = []

            for each_attributes in element_list:
                if 'attributes' in each_attributes:
                    attribute = each_attributes.get('attributes')
                    if attribute:
                        each_dic = {each_key.get('name'): each_key.get('value') for each_key in attribute if 'name' and
                                    'value' in each_key}
                        elements.append(each_dic)
            return elements
        except:
            ex = sys.exc_info()[:2]
            logging.error('Get EHC object from vRO failed. Encounter error {}'.format(ex))
            raise

    def get_vcenter_relationships(self, target_folder):
        vcenters = self._get_ehc_object(target_folder)
        return [(c.get('name'), c.get('dr_partner_name')) for c in vcenters if c.get('dr_designation') == 'Protected']

    def get_clusters(self, target_folder):
        clusters = self._get_ehc_object(target_folder)
        return [c.get('name') for c in clusters if c.get('designation') != 'Recovery']

    def get_datastores(self, target_folder):
        datastores = self._get_ehc_object(target_folder)
        datastore_names = [d.get('name') for d in datastores if d.get('storage_type') != 'VS1S']
        return filter(lambda x: not any(n != x and x.startswith(n) for n in datastore_names), datastore_names)

    def get_vrpa_clusters(self, target_folder):
        vrpa_clusters = self._get_ehc_object(target_folder)
        vrpa_cluster_dict = {vc.get('name'): (vc.get('partner_vRPA_cluster'), vc.get('id')) for vc in vrpa_clusters}
        vrpa_cluster_pairs = []
        for k, v in vrpa_cluster_dict.iteritems():
            if v[0] in vrpa_cluster_dict and v[1] < vrpa_cluster_dict[v[0]][1]:
                vrpa_cluster_pairs.append((k, v[0]))
        return vrpa_cluster_pairs

    def get_asr_name(self, target_folder):
        """
        get asr Name with details
        :param target_folder:
        :return: list
        """
        asr_name_list = []
        asrs = self._get_ehc_object(target_folder)
        asr_name = ''
        if asrs:
            for asr in asrs:
                if 'name' in asr and asr['name']:
                    asr_name = asr['name'] + '-['
                if 'asr_type' in asr and asr['asr_type']:
                    asr_name += asr['asr_type'] + '-'
                for index in range(1, 5):
                    key = 'site{}'.format(index)
                    if key in asr and asr[key] != '':
                        if index > 1:
                            asr_name += '-'
                        asr_name += asr[key]
                asr_name += ']-UsedByARR:'
                if 'arrs' in asr and asr['arrs']:
                    if len(asr['arrs']) > 2:
                        asr_name += 'True'
                    else:
                        asr_name += 'False'
                asr_name_list.append(asr_name)
        return asr_name_list

    def get_arr_name(self, target_folder):
        """
        get asr Name with details
        :param target_folder:
        :return: list
        """
        arr_name_list = []
        arrs = self._get_ehc_object(target_folder)
        arr_name = ''
        if arrs:
            for arr in arrs:
                if 'name' in arr and arr['name']:
                    arr_name = arr['name'] + ' ('
                if 'arr_type' in arr and arr['arr_type']:
                    arr_name += arr['arr_type'] + '-'
                for index in range(1, 5):
                    key = 'site{}_grid'.format(index)
                    if key in arr and arr[key] != '':
                        if index > 1:
                            arr_name += '-'
                        arr_name += arr[key]
                arr_name += ')'
                arr_name_list.append(arr_name)
        return arr_name_list
