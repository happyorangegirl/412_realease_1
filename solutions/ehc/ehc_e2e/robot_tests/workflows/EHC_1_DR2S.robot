*** Settings ***
Library           ehc_e2e.workflow.BaseWorkflow

*** Test Cases ***
E2E-1-C4: Deploy DR2S cluster with Data Protection
    [Documentation]    As a cloud administrator, I would like to deploy DR2S cluster with Data Protection
    [Tags]    EHC E2E Workflow
    [Setup]    Apply Settings From Files    C:\\ehc_challenger\\solutions\\ehc\\ehc_e2e\\conf\\generic.yaml    C:\\ehc_challenger\\solutions\\ehc\\ehc_e2e\\conf\\E2EWF-1-DR2S.config.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Adds Vcenter Relationship
    Cloud Administrator Onboard Cluster
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Adds Backup Service Level For Deploy Vm
    Cloud Administrator Adds Backup Service Level For Set Vm
    Cloud Administrator Provisions Cloud Storage
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Creates Reservation
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator Sets No Protection Backup Service Level
    Cloud Administrator Sets Origin Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level
#    Cloud Administrator Run Admin Report
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Deletes Datastore
    Cloud Administrator Edits An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Edits Avamar Grid
    Cloud Administrator Edits Avamar Grid Admin Full
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Edits Cluster Site
    Cloud Administrator Edits Cluster Hwi
    Cloud Administrator Deletes Cluster
    Cloud Administrator Deletes Vcenter Relationship
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
