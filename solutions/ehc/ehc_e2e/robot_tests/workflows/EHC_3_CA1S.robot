*** Settings ***
Library           ehc_e2e.workflow.BaseWorkflow

*** Variables ***

*** Test Cases ***
E2E-3-C2: Deploy CA1S VM Without Data Protection
    [Documentation]    E2E-3-C2: As a cloud end user, I would like to request and manage VMs in different types' Cluster over the cloud without DP in CA1S.
    [Tags]    EHC E2E Workflow    DP
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-3-CA1S.config.yaml    /root/automation/ehc/config/generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment