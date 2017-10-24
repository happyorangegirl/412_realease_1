import atexit
import logging
from ehc_rest_utilities.session_manager import ViPRSession
from ehc_rest_utilities.vipr_rest_utilities import ViPRRestEx

logging.getLogger("requests").setLevel(logging.WARNING)


def close_vipr_session(vipr_session):
    vipr_session.logout()


def __main__():

    # ViPR tutorial
    # learn ViPR rest APIs on EMC official website

    # the first step is session initialization
    vipr_session = ViPRSession('vipr.vlab.local', 'root', 'Password123!')

    # make sure ViPR session is closed after use
    atexit.register(close_vipr_session, vipr_session)

    # then pass the session to create a ViPR rest utility instance
    vipr = ViPRRestEx(vipr_session)

    # one of the most common use is to order a catalog service
    # find required parameters in ViPR rest api document

    # take delete datastore as an example
    # find datastore id firstly
    ds_id = vipr.find_volume_id('CRK-XIO-Local_1493971405961')

    # provide necessary input parameters
    parameters = {
        'volumes': ds_id,
        'deletionType': 'FULL'
    }

    # order catalog service and get resource of the order
    order = vipr.order_catalog_service('RemoveBlockVolumes', **parameters)

    # request failure will not stop execution so assertion is needed
    # if something goes wrong, None will be returned and an error will be logged
    assert order, 'something went wrong'

    # finally, check order result with order id
    assert vipr.check_order_status(order['id']), 'execution did not succeed'

    # find more useful methods in ViPRRestBase and ViPRRestEX

main = __main__
if __name__ == '__main__':
    __main__()
