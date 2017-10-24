CREATE_TENANT_TEMPLATE = {
    '@type': 'Tenant',
    'id': '',
    'urlName': '',
    'name': '',
    'contactEmail': '',
    'description': '',
    'defaultTenant': False
}

ADD_USER_TEMPLATE = {
    '@type': 'User',
    'firstName': '',
    'lastName': '',
    'emailAddress': '',
    'locked': False,
    'disabled': False,
    'password': '',
    'principalId': {
        'domain': 'vsphere.local',
        'name': ''
    }
}

ADD_DIRECTORY_TEMPLATE = {
    'name': 'vlab.local',
    'type': 'AD',
    'userNameDn': 'cn=adbind_vra,OU=EHC,DC=vlab,DC=local',
    'groupBaseSearchDn': 'ou=EHC,DC=vlab,DC=local',
    'password': 'Password123!',
    'url': 'ldap://vlab.local:389',
    'userBaseSearchDn': 'ou=EHC,DC=vlab,DC=local',
    'domain': 'vlab.local',
    'groupBaseSearchDnstrustAll': True,
    'useGlobalCatalog': False
}

ALL_ROLES_TEMPLATE = [
    'SOFTWARE_SERVICE_SOFTWARE_ARCHITECT',
    'COMPOSITION_SERVICE_INFRASTRUCTURE_ARCHITECT',
    'CATALOG_SERVICE_CATALOG_ADMIN',
    'CSP_APPROVAL_ADMIN',
    'COMPOSITION_SERVICE_APPLICATION_ARCHITECT'
]
