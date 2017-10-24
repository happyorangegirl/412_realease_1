*** Settings ***

Library           ehc_e2e.workflow.SRMDRWorkflow

*** Test Cases ***
E2E-9-C4: Perform planned migration in DR2S
    [Documentation]    As a cloud administrator, I would like to do planned migration (DR/MP) in DR2S
    [Tags]    EHC E2E Workflow    DR2S
    [Setup]    Apply Settings From Files    C:\\ehc_challenger\\solutions\\ehc\\ehc_e2e\\conf\\generic.yaml    C:\\ehc_challenger\\solutions\\ehc\\ehc_e2e\\conf\\E2EWF-9-C4-DR2S.config.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Adds Vcenter Relationship
    Cloud Administrator Onboard Cluster

    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Provisions Cloud Storage

    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Creates Reservation
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Adds Backup Service Level For Deploy Vm
    Cloud Administrator Adds Backup Service Level For Set Vm
    Cloud Administrator Deploys Vm

    Cloud Administrator Operates Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator Sets No Protection Backup Service Level
    Cloud Administrator Sets Origin Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
# Start to failover
    Cloud Administrator Prepares For Srm Dp Failover
    Cloud Administrator Performs Srm Dr Recovery
    Cloud Administrator Performs Srm Dr Reprotect
    Cloud Administrator Remediate Manages Srm Dr Protected Workloads
 # Start to check status of faileover
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
#  start to failback
    Cloud Administrator Prepares For Srm Dp Failover
    Cloud Administrator Performs Srm Dr Recovery
    Cloud Administrator Performs Srm Dr Reprotect
    Cloud Administrator Remediate Manages Srm Dr Protected Workloads
# start to check status of failback
    Cloud Administrator Adds Backup Service Level For Set Vm
    Cloud Administrator Deploys Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level All
# start to tear down
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level All
    Cloud Administrator Removes Reservation Policy From Blueprint
    Cloud Administrator Removes Reservation Policy From Reservation
    Cloud Administrator Deletes Reservation
    Cloud Administrator Deletes Reservation Policy

    Cloud Administrator Deletes Datastore
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Deletes Avamar Grid

    Cloud Administrator Deletes Cluster
    Cloud Administrator Deletes Vcenter Relationship
    Cloud Administrator Deletes Hwi
    Cloud Administrator Deletes Vcenter
    Cloud Administrator Deletes Site

    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment
