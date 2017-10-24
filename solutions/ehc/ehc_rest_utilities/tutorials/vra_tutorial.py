import logging
from ehc_rest_utilities.session_manager import VRASession
from ehc_rest_utilities.vra_rest_utilities import VRARestBase

logging.getLogger("requests").setLevel(logging.WARNING)


def __main__():

    # vRA tutorial
    # learn vRA rest APIs on VMware official website

    # the first step is session initialization
    vra_session = VRASession('vra-vip.vlab.local', 'dev166', 'ehc_sysadmin', 'Password123!')

    # then pass the session to create a vra rest utility instance
    vra = VRARestBase(vra_session)

    # one of the most common use is to request a catalog item
    # investigate required parameters from corresponding workflow in vRO

    # take add site as an example
    # provide necessary input parameters
    parameters = {
        'currentAction': 'Add Site',
        'entityName': 'Site998',
        'reviewAction': 'Add Site',
        'reviewSite': 'Site998'
    }

    # request catalog item and get the request resource
    add_site_request = vra.request_catalog_item('Site Maintenance', **parameters)

    # request failure will not stop execution so assertion is needed
    # if something goes wrong, None will be returned and an error will be logged
    assert add_site_request, 'something went wrong'

    # get request id from returned resource
    request_id = add_site_request['id']

    # finally, check request result with request id
    assert vra.check_request_status(request_id), 'request did not succeed'

    # another example is to create a tenant
    # create a new session of vRA administrator
    vra_session = VRASession('vra-vip.vlab.local', 'vsphere.local', 'administrator', 'Password123!')

    # change the session of vRA utility
    vra.set_vra_session(vra_session)

    # create a new tenant
    vra.create_tenant(urlName='dev998', id='dev998', name='dev998')

    # find more useful methods in VRARestBase and VRARestEX

main = __main__
if __name__ == '__main__':
    __main__()
