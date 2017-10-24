*** Settings ***
Library           ehc_e2e.workflow.BaseWorkflow
*** Test Cases ***
E2E-3-C8: Deploy VS1S cluster without Data Protection
    [Documentation]    As a cloud administrator, I would like to request and manage VMs in VS1S Cluster over the cloud without DP in LC1S.
    [Tags]    EHC E2E Workflow    VS1S
    [Setup]    Apply Settings From Files    C:/ehc_challenger/solutions/ehc/ehc_e2e/conf/generic.yaml    C:/ehc_challenger/solutions/ehc/ehc_e2e/conf/E2EWF-3-LC1S.config.yaml    C:/ehc_challenger/solutions/ehc/ehc_e2e/conf/generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment