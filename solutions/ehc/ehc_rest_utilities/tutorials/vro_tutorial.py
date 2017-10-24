import logging
from ehc_rest_utilities.session_manager import VROSession
from ehc_rest_utilities.vro_rest_utilities import VRORestBase

logging.getLogger("requests").setLevel(logging.WARNING)


def __main__():

    # vRO tutorial
    # learn vRO rest APIs with https://{vro_host}/vco/api/docs/index.html

    # the first step is session initialization
    vro_session = VROSession('192.168.3.166', 'luw7@vlab', 'Password123!')

    # then pass the session to create a vRO rest utility instance
    vro = VRORestBase(vro_session)

    # one of the most common use is to execute a workflow
    # investigate required parameters in vRO

    # take add site as an example
    # provide necessary input parameters
    parameters = {
        'currentAction': 'Add Site',
        'entityName': 'Site999',
        'reviewAction': 'Add Site',
        'reviewSite': 'Site999'
    }

    # request workflow and get the URL of the execution resource (rest call itself returns URL not designed by me)
    exec_url = vro.execute_workflow('Site Maintenance', **parameters)

    # request failure will not stop execution so assertion is needed
    # if something goes wrong, None will be returned and an error will be logged
    assert exec_url, 'something went wrong'

    # finally, check execution result with request id
    assert vro.check_wf_execution_status(exec_url), 'execution did not succeed'

    # another common use is to execute actions via vRO rest utility
    # steps are very similar to executing a workflow but execution output is directly returned
    exec_output = vro.execute_action('getAllDatacentersForAllvCenters')

    # sometimes output is in sdk-object (vRO specific) format and not readable
    # call below method to get object names (in a list)
    print vro.extract_sdk_objects(exec_output)

    # if a workflow or an action takes parameters of sdk-objects (looks like XX:YY, e.g. VC:ClusterComputeResource)
    # then the input template should be positively generated and manually append the object as a parameter
    # for example

    clusters = vro.execute_action('getAllClusters')
    for cluster in clusters['value']['array']['elements']:

        # generate input template
        input_template = vro.create_input_template()

        # append parameter
        vro.append_parameter(input_template, 'cluster', cluster, 'VC:ClusterComputeResource')

        # execute action with the input template
        print vro.execute_action('getAllDRSVmGroupPerCluster', input_template)
        
    # find more useful methods in VRORestBase and VRORestEX

main = __main__
if __name__ == '__main__':
    __main__()
