*** Settings ***
Library           ehc_e2e.workflow.BaseWorkflow

*** Variables ***

*** Test Cases ***
E2E-2-C6: Deploy MP3S Cluster Without Data Protection
    [Documentation]    As a Service Architect, I need to deploy a MP3S cluster without Data Protection.
    [Tags]    EHC E2E Workflow    MP3S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-2-MP3S.config.yaml    /root/automation/ehc/config/generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Adds Vcenter Relationship
    Cloud Administrator Onboard Cluster
    Cloud Administrator Provisions Cloud Storage
    Cloud Administrator Creates Reservation
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Assigns Storage Reservation Policy To Blueprint
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Datastore
    Cloud Administrator Edits Cluster Hwi
    Cloud Administrator Deletes Cluster
    Cloud Administrator Deletes Vcenter Relationship
    Cloud Administrator Edits Hwi
    Cloud Administrator Deletes Hwi
    Cloud Administrator Edits Vcenter
    Cloud Administrator Deletes Vcenter
    Cloud Administrator Edits Site
    Cloud Administrator Deletes Site
    Cloud Administrator Removes Reservation Policy From Reservation
    Cloud Administrator Deletes Reservation
    Cloud Administrator Removes Reservation Policy From Blueprint
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment
