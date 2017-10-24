*** Settings ***
Library           ehc_e2e.workflow.BaseWorkflow

*** Variables ***

*** Test Cases ***
E2E-3: Deploy MP3S Cluster Without Data Protection
    [Documentation]    As a Service Architect, I need to deploy a MP3S cluster without Data Protection.
    [Tags]    EHC E2E Workflow    MP3S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-3-C6-MP3S.config.yaml    /root/automation/ehc/config/generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment
