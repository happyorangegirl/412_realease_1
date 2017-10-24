*** Settings ***
Library           ehc_e2e.workflow.BaseWorkflow

*** Test Cases ***
E2E-2-C8: Deploy VS1S cluster without Data Protection
    [Documentation]    As a cloud administrator, I would like to deploy VS1S cluster without Data Protection
    [Tags]    EHC E2E Workflow    VS1S
    [Setup]    Apply Settings From Files    C:\\ehc_challenger\\solutions\\ehc\\ehc_e2e\\conf\\generic.yaml    C:\\ehc_challenger\\solutions\\ehc\\ehc_e2e\\conf\\E2EWF-2-VS1S.config.yaml    C:\\ehc_challenger\\solutions\\ehc\\ehc_e2e\\conf\\generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Comment    Cloud Administrator Creates Reservation Policy
    Comment    Cloud Administrator Creates Reservation
    Comment    Cloud Administrator Assigns Reservation Policy To Reservation
    Comment    Cloud Administrator Assigns Reservation Policy To Blueprint
    Comment    Cloud Administrator Deploys Vm
    Comment    Cloud Administrator Operates Vm
    Comment    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Cluster
    Cloud Administrator Edits Hwi
    Cloud Administrator Deletes Hwi
    Comment    Cloud Administrator Edits Vcenter
    Comment    Cloud Administrator Deletes Vcenter
    Comment    Cloud Administrator Edits Site
    Comment    Cloud Administrator Deletes Site
    Comment    Cloud Administrator Removes Reservation Policy From Blueprint
    Comment    Cloud Administrator Removes Reservation Policy From Reservation
    Comment    Cloud Administrator Deletes Reservation
    Comment    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment
