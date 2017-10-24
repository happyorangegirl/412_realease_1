import logging
import sys
import atexit
from requests.exceptions import ConnectionError
from vra_session import VRASession
from vra_rest_cleanup import VRARestCleanup
from ehc_object_fetcher import EHCObjectFetcher
from ehc_rest_utilities.session_manager import ViPRSession
from ehc_e2e_common.generic_yaml_file_parser import GenericYamlFileParser

logging.getLogger("requests").setLevel(logging.WARNING)


@atexit.register
def log_on_exit():
    logging.info('Autoclear exited.')


def __main__():
    logging.info('Start to parse generic.yaml file...')
    global_context = GenericYamlFileParser.parse_context()

    vra_host = global_context.vra_host
    vra_host = vra_host.replace('https://', '').replace('/vcac/org/', '')
    vra_tenant = global_context.vra_tenant
    vra_username = global_context.config_admin_username
    vra_password = global_context.config_admin_password

    vro_host = global_context.vro_host
    vro_username = global_context.vro_username
    vro_password = global_context.vro_password

    vipr_host = global_context.vipr_host
    vipr_username = global_context.vipr_username
    vipr_password = global_context.vipr_password

    if len(sys.argv) > 1:
        vra_tenant_arg = sys.argv[1]
        if vra_tenant_arg != vra_tenant:
            print 'Tenant not match the one in generic! Clean up canceled.'
            return
    else:
        confirm = raw_input("Everything in tenant {0} will be deleted!\n"
                            "Enter 'CONFIRM' to continue: ".format(vra_tenant))
        if confirm.upper() != 'CONFIRM':
            print 'Cleanup task canceled.'
            return

    vra_session = vipr_session = None
    try:
        vra_session = VRASession(vra_host, vra_tenant, vra_username, vra_password)
    except ConnectionError:
        logging.error(
            'Building connection to vRA host:{} for tenant:{} encounters error, error details:{}'.format(
                vra_host, vra_tenant, sys.exc_info()))
        logging.info(
            'Exit autoclear now, Please check vRA configuration in generic.yaml or vRA health, then rerun autoclear.')
        exit(-1)

    vro_fetcher = EHCObjectFetcher(vro_host, vro_username, vro_password)
    try:
        vipr_session = ViPRSession(vipr_host, vipr_username, vipr_password)
    except ConnectionError:
        logging.error(
            'Building connection to Vipr host:{} encounters error, error details:{}'.format(vipr_host, sys.exc_info())
        )
        logging.info('Exit autoclear now, Please check vipr configuration in generic.yaml or vipr connectivity, then '
                     'rerun autoclear.')
        exit(-1)

    try:
        cleaner = VRARestCleanup(vra_session, vro_fetcher, vipr_session)
        cleaner.destroy_all_vm()
        # remove reservation and reservation policy temporarily since new scenario and WF require reservation exists
        # cleaner.delete_all_res_and_rp()
        cleaner.delete_all_ehc_objects()
        cleaner.present_simple_report()
    finally:
        vipr_session.logout()

main = __main__

if __name__ == '__main__':
    __main__()