*** Settings ***
Library           ehc_e2e.workflow.AvamarFailActionWorkflow

*** Test Cases ***
E2E-8-C2-CA2S-test: As a cloud administrator, I would like to maintain CA2S Avamar grid failover/failback features
    [Documentation]    As a cloud administrator, I would like to maintain CA2S Avamar grid failover/failback features
    [Tags]    EHC E2E Workflow
    [Setup]    Apply Settings From Files    C:/Users/xiongb2/GitRepo/Dozer/solutions/ehc/ehc_e2e/conf/generic.yaml    C:/Users/xiongb2/GitRepo/Dozer/solutions/ehc/ehc_e2e/conf/E2EWF-1-LC1S.config.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm Parellel
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment