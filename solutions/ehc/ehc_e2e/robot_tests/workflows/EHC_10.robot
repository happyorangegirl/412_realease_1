*** Settings ***
Library           ehc_e2e.workflow.BaseWorkflow

*** Test Cases ***
E2E-10: Deploy Multiple VMs
    [Documentation]    E2E-10 As a cloud administrator, I would like to deploy multiple VMs by one deployment
    [Tags]    EHC E2E Workflow
    [Setup]    Apply Settings From Files    C:\\taf\\solutions\\ehc\\ehc_e2e\\conf\\generic.yaml    C:\\taf\\solutions\\ehc\\ehc_e2e\\conf\\E2EWF-10.config.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies with Cluster
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Provisions Cloud Storage
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Creates Reservation
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Rp To All Vsphere Blueprint
    Cloud Administrator Deploys Multiple Vms
    Cloud Administrator Operates Vm B
    Cloud Administrator On Demand Backup Vm B
    Cloud Administrator On Demand Restore Vm B
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Deletes Datastore
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Deletes Cluster
    Cloud Administrator Deletes Hwi
    Cloud Administrator Deletes Vcenter
    Cloud Administrator Deletes Site
    Cloud Administrator Removes Reservation Policy From Reservation
    Cloud Administrator Deletes Reservation
    Cloud Administrator Removes Rp From All Vsphere Blueprint
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment
