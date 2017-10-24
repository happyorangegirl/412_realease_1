*** Settings ***
Library           ehc_e2e.workflow.BaseWorkflow

*** Test Cases ***
E2E-3-C3: Request and manage VMs over CA2S without DP
    [Documentation]    E2E-3-C3: As a cloud end user, I would like to request and manage VMs in different types' cluster over the cloud without DP in CA2S.
    [Tags]    EHC E2E Workflow
    [Setup]    Apply Settings From Files    C:/taf/solutions/ehc/ehc_e2e/conf/generic.yaml    C:/taf/solutions/ehc/ehc_e2e/conf/E2EWF-3-CA2S.config.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment
