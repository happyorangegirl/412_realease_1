*** Settings ***
Library           ehc_e2e.workflow.BaseWorkflow
*** Test Cases ***

E2E-2-C1: Deploy LC1S cluster without Data Protection
    [Documentation]    As a cloud administrator, I would like to deploy LC1S cluster without Data Protection
    [Tags]    EHC E2E Workflow    LC1S
    [Setup]    Apply Settings From Files    C:/git_repo/solutions/ehc/ehc_e2e/conf/generic.yaml    C:/git_repo/solutions/ehc/ehc_e2e/conf/E2EWF-2-LC1S.config.yaml    C:/git_repo/solutions/ehc/ehc_e2e/conf/generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Provisions Cloud Storage
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Creates Reservation
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Datastore
    Cloud Administrator Edits Cluster Hwi
    Cloud Administrator Deletes Cluster
    Cloud Administrator Edits Hwi
    Cloud Administrator Deletes Hwi
    Cloud Administrator Edits Vcenter
    Cloud Administrator Deletes Vcenter
    Cloud Administrator Edits Site
    Cloud Administrator Deletes Site
    Cloud Administrator Removes Reservation Policy From Blueprint
    Cloud Administrator Removes Reservation Policy From Reservation
    Cloud Administrator Deletes Reservation
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment