*** Settings ***

Library           ehc_e2e.workflow.SRMDRWorkflow

*** Test Cases ***
E2E-9-C4: Perform planned migration in DR2S
    [Documentation]    As a cloud administrator, I would like to do planned migration (DR/MP) in DR2S
    [Tags]    EHC E2E Workflow    DR2S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-9-C4-DR2S.config.yaml    /root/automation/ehc/config/generic.yaml
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

    Cloud Administrator Prepares For Srm Dp Failover
    Cloud Administrator Validates Protection For Srm Dr Workloads
    Cloud Administrator Performs Srm Dr Recovery
    Cloud Administrator Performs Srm Dr Reprotect
    Cloud Administrator Remediate Manages Srm Dr Protected Workloads
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm

    Cloud Administrator Prepares For Srm Dp Failover
    Cloud Administrator Validates Protection For Srm Dr Workloads
    Cloud Administrator Performs Srm Dr Recovery
    Cloud Administrator Performs Srm Dr Reprotect
    Cloud Administrator Remediate Manages Srm Dr Protected Workloads

    Cloud Administrator Adds Backup Service Level For Set Vm
    Cloud Administrator Deploys Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level All
    Cloud Administrator Run Admin Report

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

E2E-9-C5: Perform planned migration in MP2S
    [Documentation]    As a cloud administrator, I would like to do planned migration (DR/MP) in MP2S
    [Tags]    EHC E2E Workflow    MP2S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-9-C5-MP2S.config.yaml    /root/automation/ehc/config/generic.yaml
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

    Cloud Administrator Prepares For Srm Dp Failover
    Cloud Administrator Validates Protection For Srm Dr Workloads
    Cloud Administrator Performs Srm Dr Recovery
    Cloud Administrator Performs Srm Dr Reprotect
    Cloud Administrator Remediate Manages Srm Dr Protected Workloads
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm

    Cloud Administrator Prepares For Srm Dp Failover
    Cloud Administrator Validates Protection For Srm Dr Workloads
    Cloud Administrator Performs Srm Dr Recovery
    Cloud Administrator Performs Srm Dr Reprotect
    Cloud Administrator Remediate Manages Srm Dr Protected Workloads

    Cloud Administrator Adds Backup Service Level For Set Vm
    Cloud Administrator Deploys Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level All
    Cloud Administrator Run Admin Report

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

E2E-9-C6: Perform planned migration in MP3S
    [Documentation]    As a cloud administrator, I would like to do planned migration (DR/MP) in MP3S
    [Tags]    EHC E2E Workflow    MP3S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-9-C6-MP3S.config.yaml    /root/automation/ehc/config/generic.yaml
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

    Cloud Administrator Prepares For Srm Dp Failover
    Cloud Administrator Validates Protection For Srm Dr Workloads
    Cloud Administrator Performs Srm Dr Recovery
    Cloud Administrator Performs Srm Dr Reprotect
    Cloud Administrator Remediate Manages Srm Dr Protected Workloads
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm

    Cloud Administrator Prepares For Srm Dp Failover
    Cloud Administrator Validates Protection For Srm Dr Workloads
    Cloud Administrator Performs Srm Dr Recovery
    Cloud Administrator Performs Srm Dr Reprotect
    Cloud Administrator Remediate Manages Srm Dr Protected Workloads

    Cloud Administrator Adds Backup Service Level For Set Vm
    Cloud Administrator Deploys Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level All
    Cloud Administrator Run Admin Report

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
