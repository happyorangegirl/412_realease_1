import os
import yaml
import time
from ehc_e2e.workflow import BaseWorkflow
from ehc_rest_utilities.session_manager import VRASession, VROSession, ViPRSession
from ehc_rest_utilities.vra_rest_utilities import VRARestEx
from ehc_rest_utilities.vro_rest_utilities import VRORestEx
from ehc_rest_utilities.vipr_rest_utilities import ViPRRestEx


# Maintenance and development in future

# 1. refine config
# 2. add validations
# 3. dependency enhancement


class Autosetup(object):

    config = None
    vra_util = None
    vro_util = None
    vipr_util = None

    def load_config(self, path):
        with open(path) as file_pointer:
            self.config = yaml.load(file_pointer)

    def init_vra_util(self):
        param = self.config['init_vra_util']
        self.vra_util = VRARestEx(VRASession(param['host'], param['tenant'], param['username'], param['password']))

    def init_vro_util(self):
        param = self.config['init_vro_util']
        self.vro_util = VRORestEx(VROSession(param['host'], param['username'], param['password']))

    def init_vipr_util(self):
        param = self.config['init_vipr_util']
        self.vipr_util = ViPRRestEx(ViPRSession(param['host'], param['username'], param['password']))

    # don't forget to close vipr session
    def close_vipr_session(self):
        self.vipr_util.close_vipr_session()

    # api does not validate local user
    def create_a_tenant(self):
        tenant = self.config['create_a_tenant']
        tenant_name = tenant['name']
        assert not self.vra_util.if_tenant_exists(tenant_name), 'Tenant {0} already exists'.format(tenant_name)
        assert self.vra_util.create_tenant(urlName=tenant_name, id=tenant_name, name=tenant_name), \
            'Failed to create a new tenant'

        time.sleep(3)
        local_user = tenant['local_user']
        assert self.vra_util.add_local_user(tenant_name, firstName=local_user['first_name'],
                                            lastName=local_user['last_name'], emailAddress=local_user['email'],
                                            password='Password123!', principalId={'name': local_user['username']}), \
            'Failed to add local user to tenant'

        local_user_account = '{0}@{1}'.format(local_user['username'], local_user['default_domain'])
        assert self.vra_util.assign_role(tenant_name, local_user_account, 'CSP_TENANT_ADMIN') is not None, \
            'Failed to assign tenant admin role to local user'
        assert self.vra_util.assign_role(tenant_name, local_user_account, 'COM_VMWARE_IAAS_IAAS_ADMINISTRATOR') is not None, \
            'Failed to assign IaaS admin role to local user'

    # sometimes fails
    def create_an_ad(self):
        ad = self.config['create_an_ad']
        assert not self.vra_util.get_directory(ad['tenant_name']).get('content', []), 'Active Directory already added'

        assert self.vra_util.add_directory(ad['tenant_name'], userNameDn=ad['bind_dn'], password=ad['password'],
                                           groupBaseSearchDn=ad['base_dn'], userBaseSearchDn=ad['base_dn']) is not None, \
            'Failed to add Active Directory to Tenant {0}'.format(ad['tenant_name'])

    # api always changes. it does not validate input as well. return 201 no matter succeed of fail
    def assign_roles(self):
        assign_roles = self.config['assign_roles']

        for admin in assign_roles['tenant_admins']:
            assert self.vra_util.assign_role(assign_roles['tenant_name'], admin, 'CSP_TENANT_ADMIN') is not None, \
                'Failed to assign Tenant admin role to user {0}'.format(admin)

        for admin in assign_roles['iaas_admins']:
            assert self.vra_util.assign_role(assign_roles['tenant_name'], admin, 'COM_VMWARE_IAAS_IAAS_ADMINISTRATOR') is not None, \
                'Failed to assign IaaS admin role to user {0}'.format(admin)

        for admin in assign_roles['xaas_admins']:
            assert self.vra_util.assign_multi_roles(assign_roles['tenant_name'], admin) is not None, \
                'Failed to assign XaaS admin role to user {0}'.format(admin)

    def add_a_vra_host(self):
        vra_host = self.config['add_a_vra_host']
        params = {
            'name': vra_host['name'],
            'url': 'https://{0}'.format(vra_host['host']),
            'tenant': vra_host['tenant'],
            'authUsername': vra_host['username'],
            'authPassword': vra_host['password'],
            'connectionTimeout': 30,
            'operationTimeout': 500,
            'sessionMode': 'Shared Session',
            'acceptAllCertificates': False
        }
        res = self.vro_util.add_vra_host(**params)
        assert res and self.vro_util.check_wf_execution_status(res), 'Failed to add vRA host in vRO'

    def add_an_iaas_host(self):
        iaas_host = self.config['add_an_iaas_host']
        params = {
            'name': iaas_host['name'],
            'hostAddress': 'https://{0}'.format(iaas_host['host']),
            'authUserName': iaas_host['username'],
            'authPassword': iaas_host['password'],
            'domain': iaas_host['domain'],
            'authentication': 'NTLM',
            'defaultConnectionSettings': True,
            'addProxySettings': False,
            'autoAccept': False
        }
        res = self.vro_util.add_iaas_host(**params)
        assert res and self.vro_util.check_wf_execution_status(res), 'Failed to add IaaS host in vRO'

    def create_machine_prefixes(self):
        for prefix in self.config['create_machine_prefixes']:
            if self.vro_util.get_machine_prefix(prefix['prefix']):
                continue

            params = {
                'machinePrefix': prefix['prefix'],
                'numberOfDigits': prefix['number_digits'],
                'nextNumber': prefix['next_number']
            }
            res = self.vro_util.create_machine_prefix(prefix['iaas_host_name'], **params)
            assert res and self.vro_util.check_wf_execution_status(res), \
                'Failed to create Machine Prefix {0}'.format(prefix['prefix'])

    def create_business_groups(self):
        for bg in self.config['create_business_groups']:
            if self.vro_util.get_business_group(bg['name']):
                continue

            params = {
                'name': bg['name'],
                'activeDirectoryContainer': bg['ad_container'],
                'administrators': bg['group_manager_role'],
                'administratorEmail': bg['manager_email'],
                'support': bg['support_role'],
                'users': bg['user_role']
            }
            res = self.vro_util.create_business_group(bg['vra_host_name'], bg['machine_prefix'], **params)
            assert res and self.vro_util.check_wf_execution_status(res), \
                'Failed to create Business Group {0}'.format(bg['name'])

    # seems credentials are gone in vra 7.3
    def create_credentials(self):
        for cred in self.config['create_credentials']:
            if self.vro_util.get_credential(cred['name']):
                continue

            params = {
                'credentialName': cred['name'],
                'username': cred['username'],
                'password': cred['password']
            }
            res = self.vro_util.create_credential(cred['iaas_host_name'], **params)
            assert res and self.vro_util.check_wf_execution_status(res), \
                'Failed to create vRO Credential {0}'.format(cred['name'])

    # api does not support nsx when adding vcenter endpoints. not sure in vra 7.3
    def create_endpoints(self):
        for ep in self.config['create_endpoints']:
            if self.vro_util.get_endpoint(ep['name']):
                continue

            params = {
                'managementUrl': ep['fqdn'],
                'vcoPriority': ep['vco_priority'],
                'endpointName': ep['name'],
            }
            res = self.vro_util.create_endpoint(ep['iaas_host_name'], ep['platform_type'], ep['credential'], **params)
            assert res and self.vro_util.check_wf_execution_status(res), \
                'Failed to create vRO Endpoint {0}'.format(ep['name'])

    def update_vro_config(self):
        vro_conf = self.config['update_vro_config']
        params = {
            'useDefault': False,
            'name': vro_conf['conn_name'],
            'orchestratorHost': vro_conf['vro_host'],
            'port': '8281',
            'useSSO': False,
            'username': vro_conf['vro_username'],
            'password': vro_conf['vro_password']
        }
        res = self.vro_util.update_vro_config(vro_conf['vra_host_name'], **params)
        assert res and self.vro_util.check_wf_execution_status(res), 'Failed to configure external vRO'

    # make sure the vra host will be removed if you added one
    def remove_a_vra_host(self):
        re = self.config['remove_a_vra_host']
        self.vro_util.remove_vra_host_by_name(re['name'])

    # make sure the iaas host will be removed if you added one
    def remove_an_iaas_host(self):
        re = self.config['remove_an_iaas_host']
        self.vro_util.remove_iaas_host_by_name(re['name'])

    def create_a_vipr_project(self):
        vipr_project = self.config['create_a_vipr_project']
        res = self.vipr_util.create_project(vipr_project['name'])
        assert res, 'Failed to create ViPR project {0}'.format(vipr_project['name'])

        project_id = res['id']
        self.vipr_util.update_project(project_id, owner=vipr_project['owner'])
        for acl_user in vipr_project['acl_users']:
            assert self.vipr_util.add_acl(project_id, acl_user, 'user', 'ALL'), \
                'Failed to add ACL user {0} to Project {1}'.format(acl_user, vipr_project['name'])
        for acl_group in vipr_project['acl_groups']:
            assert self.vipr_util.add_acl(project_id, acl_group, 'group', 'ALL'), \
                'Failed to add ACL user {0} to Project {1}'.format(acl_group, vipr_project['name'])

    # implement by web-ui. sometimes admin list will be missing. try send an enter or a tab
    def create_a_fabric_group(self):
        fg = self.config['create_a_fabric_group']

        _cd = os.path.dirname(os.path.realpath(__file__))
        _parent_dir = os.path.abspath(os.path.join(_cd, os.pardir))
        _global = os.path.join(_parent_dir, 'ehc_e2e/conf/generic.yaml')

        wf = BaseWorkflow()
        wf.apply_settings_from_files(_global)
        wf.cloud_administrator_opens_browser()
        wf.cloud_administrator_login()

        wf.cloud_administrator_add_fabric_group(fg['name'], fg['admins'])

        wf.cloud_administrator_logout()
        wf.cloud_administrator_closes_browser()
        wf.reset_settings()
