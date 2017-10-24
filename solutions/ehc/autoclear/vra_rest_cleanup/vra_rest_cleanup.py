import time
import logging
from autoclear.parameters.parameters import PARAMETERS
from ehc_rest_utilities.vipr_rest_utilities import ViPRRestEx
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


class VRARestCleanup(object):

    def __init__(self, vra_session, vro_fetcher, vipr_session):
        self.vra_session = vra_session
        self.vro_fetcher = vro_fetcher
        self.vipr_session = vipr_session
        self.simple_report = []

    def destroy_all_vm(self):
        # get all VMs
        logging.info('Start to destroy all VMs')
        response = self.vra_session.get(
            'https://{host}/catalog-service/api/consumer/resources/types/Infrastructure.Machine'.format(
                host=self.vra_session.host))
        if response.status_code != 200:
            logging.error('Failed to GET VM resources from vRA. HTTP status = {0}'.format(response.status_code))
            return

        json_data = response.json()

        # check if there is RP4VM pair.
        vm_list = [(vm['name'], vm['id']) for vm in json_data['content']]
        rp4vm_pair_list = [(vm1, vm2) for vm1 in vm_list for vm2 in vm_list if vm1 != vm2 and vm1[0]+'.copy' in vm2[0]]
        protected_vm_list = [rp4vm_pair[0] for rp4vm_pair in rp4vm_pair_list]
        copy_vm_list = [rp4vm_pair[1] for rp4vm_pair in rp4vm_pair_list]
        common_vm_list = [vm for vm in vm_list if vm not in copy_vm_list and vm not in protected_vm_list]

        num_of_vms = len(vm_list)
        num_of_success = 0
        logging.info('Found {0} VM(s) in total.'.format(num_of_vms))

        num_of_rp4vm_vm = len(rp4vm_pair_list)
        if num_of_rp4vm_vm > 0:
            logging.info('Found {0} VM(s) possibly protected by RP4VM.'.format(len(rp4vm_pair_list)))
            logging.warning('Estimated 30-60 minutes to destroy each.')

        # destroy all RP4VM protected/recovery VMs
        for rp4vm_pair in rp4vm_pair_list:
            logging.info('Start to destroy protected VM {0} in a brute-force way.'.format(rp4vm_pair[0][0]))
            if self.operate_vm_by_id(rp4vm_pair[0][1], 'Destroy') and self.check_vm_status_by_id(rp4vm_pair[0][1],
                                                                                                 'DELETED', 3600, 60):
                logging.info('Protected VM destroyed.')
                num_of_success += 1
            else:
                logging.warning('Failed to destroy protected VM.')

            # check if copy is deleted together. if not, try again
            logging.info('Start to check the copy of protected VM {0}.'.format(rp4vm_pair[1][0]))
            if self.check_vm_status_by_id(rp4vm_pair[1][1], 'DELETED'):
                logging.info('Copy of protected VM {0} destroyed.'.format(rp4vm_pair[1][0]))
                num_of_success += 1
            else:
                logging.warning('Failed to destroy copy -> Force to destroy again')
                if self.operate_vm_by_id(rp4vm_pair[1][1], 'Destroy') and self.check_vm_status_by_id(rp4vm_pair[1][1],
                                                                                                     'DELETED'):
                    logging.info('Copy of protected VM {0} destroyed.'.format(rp4vm_pair[1][0]))
                    num_of_success += 1
                else:
                    logging.warning('Failed to destroy again.')

        # destroy all common VM
        for vm in common_vm_list:
            logging.info('Start to destroy VM {0}.'.format(vm[0]))
            if self.operate_vm_by_id(vm[1], 'Destroy') and self.check_vm_status_by_id(vm[1], 'DELETED'):
                logging.info('VM destroyed.')
                num_of_success += 1
            else:
                logging.warning('Failed to destroy VM.')

        logging.info('Destroy VMs: {0} found, {1} destroyed.'.format(num_of_vms, num_of_success))
        self.simple_report.append(('VM', num_of_vms, num_of_success))

    def check_vm_status_by_id(self, vm_id, status, timeout=600, retry_interval=10):
        if not (vm_id and status):
            logging.error('Failed to check VM status by id: Invalid input parameter')
            return False

        logging.info('Start to check VM status.')

        while timeout > 0:
            timeout -= retry_interval
            time.sleep(retry_interval)
            response = self.vra_session.get('https://{host}/catalog-service/api/consumer/resources/{id}'
                                            .format(host=self.vra_session.host, id=vm_id))
            if response.status_code == 200:
                json_data = response.json()
                if status == json_data['status']:
                    return True
            elif response.status_code == 404:
                logging.error('404 error: VM not found.')
                return False

        logging.warning('Timed out to check VM status.')
        return False

    def operate_vm_by_id(self, vm_id, operation_name):
        logging.info('Start to operate VM. Operation: {0}.'.format(operation_name))

        # get Destroy VM operation id from VM resource
        response = self.vra_session.get('https://{host}/catalog-service/api/consumer/resources/{id}'
                                        .format(host=self.vra_session.host, id=vm_id))
        if response.status_code != 200:
            logging.error('Failed to GET VM resource. HTTP status = {0}'.format(response.status_code))
            return False

        json_data = response.json()
        for operation in json_data['operations']:
            if operation_name == operation['name']:
                operation_id = operation['id']
                break
        else:
            logging.error('Failed to operate VM {0}. Cannot find operation {1}'
                          .format(json_data['name'], operation_name))
            return False

        # make request body then post the request
        body = {
            "@type": "ResourceActionRequest",
            "resourceRef": {"id": vm_id},
            "resourceActionRef": {"id": operation_id},
            "organization": json_data['organization'],
            "state": "SUBMITTED",
        }
        response = self.vra_session.post(url='https://{host}/catalog-service/api/consumer/requests'
                                         .format(host=self.vra_session.host), json=body)
        if response.status_code != 201:
            logging.error('Failed to POST operate VM request. HTTP status = {0}'.format(response.status_code))
            return False

        # check if VM is deleted.
        logging.info('Request posted.')
        return True

    def request_catalog_item(self, catalog_item_name, **kwargs):
        logging.info('Start to request catalog item {0}'.format(catalog_item_name))

        # find catalog item resource
        response = self.vra_session.get("https://{host}/catalog-service/api/consumer/entitledCatalogItemViews"
                                        "?$filter=name eq '{item}'"
                                        .format(host=self.vra_session.host, item=catalog_item_name))
        if response.status_code != 200:
            logging.error('Failed to GET catalog item resource of {0}. HTTP status = {1}'
                          .format(catalog_item_name, response.status_code))
            return False

        json_data = response.json()
        if json_data['metadata']['totalElements'] < 1:
            logging.error('Cannot find catalog item {0}'.format(catalog_item_name))
            return False

        get_request_template_url = json_data['content'][0]['links'][0]['href'].split('{')[0]
        post_request_url = json_data['content'][0]['links'][1]['href'].split('{')[0]

        # get request template
        response = self.vra_session.get(get_request_template_url)
        if response.status_code != 200:
            logging.error('Failed to get request template of catalog item {0}'.format(catalog_item_name))
            return False

        json_data = response.json()

        # update request template then post it
        json_data['data'].update((k, kwargs[k]) for k in json_data['data'].viewkeys() & kwargs.viewkeys())
        response = self.vra_session.post(url=post_request_url, json=json_data)
        if response.status_code != 201:
            logging.error('Failed to POST submit request for catalog item {0}. HTTP status = {1}'
                          .format(catalog_item_name, response.status_code))
            return False

        logging.info('Request posted.')
        json_data = response.json()
        request_id = json_data['id']

        return self.check_request(request_id)

    def check_request(self, request_id, timeout=900, retry_interval=10):
        logging.info('Start to check request state.')

        while timeout > 0:
            timeout -= retry_interval
            time.sleep(retry_interval)
            response = self.vra_session.get('https://{host}/catalog-service/api/consumer/requests/{id}'
                                            .format(host=self.vra_session.host, id=request_id))
            if response.status_code == 200:
                json_data = response.json()
                if json_data['stateName'] == 'Successful':
                    logging.info('Request state is Successful')
                    return True
                elif json_data['stateName'] == 'Failed':
                    logging.warning('State of request No.{0} {1} is Failed'.format(json_data['requestNumber'],
                                                                                   json_data['requestedItemName']))
                    return False

        logging.warning('Timed out to get final request status')
        return False

    def delete_all_res_and_rp(self):
        # get reservation resources
        logging.info('Start to delete all Reservations and Reservation Policies.')
        response = self.vra_session.get(
            "https://{host}/reservation-service/api/reservations/?$filter=tenantId eq '{tnt}'".format(
                host=self.vra_session.host, tnt=self.vra_session.tenant))
        if response.status_code != 200:
            logging.error('Failed to GET Reservations resources. HTTP status: {0}'.format(response.status_code))
            return

        # need to store referenced reservation policy when deleting a reservation
        rp_list = []

        # delete reservations
        json_data = response.json()
        num_of_reservations = json_data['metadata']['totalElements']
        num_of_success = 0
        logging.info('Found {0} Reservations in total.'.format(num_of_reservations))

        for i in range(num_of_reservations):
            pid = json_data['content'][i]['reservationPolicyId']
            if pid:
                rp_list.append(pid)
            logging.info('Delete Reservation {0}'.format(json_data['content'][i]['name']))
            response = self.vra_session.delete('https://{host}/reservation-service/api/reservations/{id}'
                                               .format(host=self.vra_session.host, id=json_data['content'][i]['id']))
            if response.status_code != 204:
                logging.warning('Failed to DELETE Reservation resource. HTTP status: {0}'.format(response.status_code))
            else:
                logging.info('Reservation deleted.')
                num_of_success += 1

        logging.info('Delete Reservations: {0} found, {1} deleted.'.format(num_of_reservations, num_of_success))
        self.simple_report.append(('Reservation', num_of_reservations, num_of_success))

        # delete reservation policies
        rp_list = list(set(rp_list))
        num_of_rp = len(rp_list)
        logging.info('Found {0} Reservation Policies in total.'.format(num_of_rp))
        num_of_success = 0
        for pid in rp_list:
            logging.info('Delete Reservation Policy {0}'.format(pid))
            response = self.vra_session.delete('https://{host}/reservation-service/api/reservations/policies/{id}'
                                               .format(host=self.vra_session.host, id=pid))
            if response.status_code != 204:
                logging.warning('Failed to DELETE Reservation Policy resource. May be referenced by another tenant. '
                                'HTTP status: {0}'.format(response.status_code))
            else:
                logging.info('Reservation Policy Deleted.')
                num_of_success += 1

        logging.info('Delete Reservation Policies: {0} found, {1} deleted.'.format(num_of_rp, num_of_success))
        self.simple_report.append(('Reservation Policy', num_of_rp, num_of_success))

    def delete_all_ehc_objects(self):
        for object_type in PARAMETERS['cleanup_sequence']:
            logging.info('Start to delete all {0}s'.format(object_type))
            params = PARAMETERS[object_type]
            vro_get_api = params['vro_get_api']

            if object_type == 'ASR':
                object_names = self.vro_fetcher.get_asr_name(vro_get_api)
            elif object_type == 'ARR':
                object_names = self.vro_fetcher.get_arr_name(vro_get_api)
            elif object_type == 'vCenter Relationship':
                object_names = self.vro_fetcher.get_vcenter_relationships(vro_get_api)
            elif object_type == 'Cluster':
                object_names = self.vro_fetcher.get_clusters(vro_get_api)
            elif object_type == 'Datastore':
                object_names = self.vro_fetcher.get_datastores(vro_get_api)
            elif object_type == 'RP4VM vRPA Cluster':
                object_names = self.vro_fetcher.get_vrpa_clusters(vro_get_api)
            else:
                object_names = self.vro_fetcher.get_object_names(vro_get_api)

            num_of_obj = len(object_names)
            logging.info('Found {0} {1}s in total.'.format(num_of_obj, object_type))
            num_of_success = 0
            for object_name in object_names:
                if object_type == 'vCenter Relationship' or object_type == 'RP4VM vRPA Cluster':
                    logging.info('Start to delete {0} ({1}, {2}).'.format(object_type, object_name[0], object_name[1]))
                    params[params['param1']] = object_name[0]
                    params[params['param2']] = object_name[1]
                else:
                    logging.info('Start to delete {0} {1}.'.format(object_type, object_name))
                    params[params['delete_key']] = object_name

                if self.request_catalog_item(params['workflow_name'], **params):
                    num_of_success += 1
                    logging.info('{0} deleted.'.format(object_type))

                    if object_type == 'Datastore':
                        logging.info('Start to delete datastore {0} in ViPR'.format(object_name))
                        vipr_ex = ViPRRestEx(self.vipr_session)
                        if vipr_ex.remove_volume_from_export_group(object_name):
                            logging.info('Removed Datastore from Export Group')
                        if vipr_ex.delete_volume(object_name):
                            logging.info('Datastore deleted')

                elif object_type == 'Cluster':
                    cluster_left_num = len(self.vro_fetcher.get_datastores(vro_get_api))
                    if cluster_left_num == num_of_obj - num_of_success - 1:
                        logging.warning('The Cluster was deleted along with the previous one (Possible RP4VM).')
                        num_of_success += 1

            logging.info('Delete {0}s: {1} found, {2} deleted.'.format(object_type, num_of_obj, num_of_success))
            self.simple_report.append((object_type, num_of_obj, num_of_success))

    def present_simple_report(self):
        time.sleep(1)   # sleep or disable execution optimizations to correctly display the report table.
        print 'Presenting a simple cleanup report:'
        print '+--------------------------+-----------+-----------+'
        print '| Object                   | Found     | Deleted   |'
        print '+--------------------------+-----------+-----------+'

        for row in self.simple_report:
            print '| ' + str(row[0]).ljust(25, ' ') + '|'\
                  + str(row[1]).rjust(10, ' ') + ' |' + str(row[2]).rjust(10, ' ') + ' |'
            print '+--------------------------+-----------+-----------+'
