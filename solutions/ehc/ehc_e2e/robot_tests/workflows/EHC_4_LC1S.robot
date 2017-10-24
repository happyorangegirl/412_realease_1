*** Settings ***
Library           ehc_e2e.workflow.BaseWorkflow

*** Test Cases ***
E2E-4:Request and manage VMs in LC1S with Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in LC1S cluster over the cloud with DP
    [Tags]    EHC E2E Workflow    LC1S
    [Setup]    Apply Settings From Files    C:\\ehc_challenger\\solutions\\ehc\\ehc_e2e\\conf\\generic.yaml    C:\\ehc_challenger\\solutions\\ehc\\ehc_e2e\\conf\\E2EWF-4-LC1S.config.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator Sets No Protection Backup Service Level
    Cloud Administrator Sets Origin Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Run Admin Report
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment
