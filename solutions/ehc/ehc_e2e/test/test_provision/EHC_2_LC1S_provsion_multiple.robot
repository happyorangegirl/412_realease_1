*** Settings ***
Library           ehc_e2e.workflow.BaseWorkflow
*** Test Cases ***

E2E-2-C1: Deploy LC1S cluster without Data Protection
    [Documentation]    As a cloud administrator, I would like to deploy LC1S cluster without Data Protection
    [Tags]    EHC E2E Workflow    LC1S
    [Setup]    Apply Settings From Files    C:/Users/yinl1/ehc_45/solutions/ehc/ehc_e2e/conf/generic.yaml    C:/Users/yinl1/ehc_45/solutions/ehc/ehc_e2e/conf/E2EWF-2-LC1S_provision_multiple.config.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    #Cloud Administrator Adds Vcenter
    #Cloud Administrator Adds Hwi
    #Cloud Administrator Onboard Cluster
    #Cloud Administrator Provisions Cloud Storage
    Cloud Administrator Provision Multiple Cloud Storage
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment