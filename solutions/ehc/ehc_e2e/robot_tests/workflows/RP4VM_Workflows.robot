*** Settings ***
Library           ehc_e2e.workflow.RP4VMWorkflow

*** Variables ***
${CONF DIR}  /root/automation/ehc/config/
${SkipTeardown}    False

*** Test Cases ***

E2E-101-C7: Initialize RP4VM support in EHC without Data Protection
    [Documentation]    E2E-101 As a RP4VM system administrator, I want to initialize RP4VM support in EHC without DP
    [Tags]    EHC E2E Workflow
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-101-RP4VM.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Adds Rp4vm Vcenter Relationship
    Cloud Administrator Onboards Local Cluster
    Cloud Administrator Provisions Cloud Storage
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Creates Reservation
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Adds VRPA Clusters
    Cloud Administrator Adds Rp4vm Policy
    Cloud Administrator Deploys Vm
    Cloud Administrator Protects Vm Using New Cg
    Cloud Administrator Provisions Rp4vm Using New Cg
    Cloud Administrator Provisions Rp4vm Using Existing Cg
    Cloud Administrator Changes To An Existing Cg
    Cloud Administrator Changes Boot Sequence
    Cloud Administrator Performs Failover On Protected Vms
    Cloud Administrator Adds Post Failover Synchronization
    Cloud Administrator Deploys Vm
    Cloud Administrator Performs Failover On Protected Vms
    Cloud Administrator Adds Post Failover Synchronization
    Cloud Administrator Protects Vm Using Existing Cg
    Cloud Administrator Changes To A New Cg
    Cloud Administrator Unprotects All Vms
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Rp4vm Policy
    Cloud Administrator Deletes VRPA Clusters
    Cloud Administrator Deletes Datastore
    Cloud Administrator Deletes Cluster
    Cloud Administrator Deletes Rp4vm Vcenter Relationship
    Cloud Administrator Deletes Hwi
    Cloud Administrator Deletes Vcenter
    Cloud Administrator Deletes Site
    Cloud Administrator Removes Reservation Policy From Blueprint
    Cloud Administrator Removes Reservation Policy From Reservation
    Cloud Administrator Deletes Reservation
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-102-C7: Initialize RP4VM support in EHC with Data Protection
    [Documentation]    E2E-102 As a RP4VM system administrator, I want to initialize RP4VM support in EHC with DP
    [Tags]    EHC E2E Workflow
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-102-RP4VM-DP.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Adds Rp4vm Vcenter Relationship
    Cloud Administrator Onboards Local Cluster
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds Backup Service Level For Deploy Vm
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Provisions Cloud Storage
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Creates Reservation
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Adds VRPA Clusters
    Cloud Administrator Adds Rp4vm Policy
    Cloud Administrator Deploys Vm
    Cloud Administrator Protects Vm Using New Cg
    Cloud Administrator Provisions Rp4vm Using New Cg
    Cloud Administrator Provisions Rp4vm Using Existing Cg
    Cloud Administrator Changes To An Existing Cg
    Cloud Administrator Changes Boot Sequence
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Prefailovers Stage Cgs
    Cloud Administrator Performs Failover On Protected Vms
    Cloud Administrator Adds Post Failover Synchronization
    Cloud Administrator Adds Backup Service Level For Set Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Prefailovers Stage Cgs
    Cloud Administrator Performs Failover On Protected Vms
    Cloud Administrator Adds Post Failover Synchronization
    Cloud Administrator Prefailovers Stage Cgs
    Cloud Administrator Prefailovers Unstage Cgs
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Deploys Vm
    Cloud Administrator Protects Vm Using Existing Cg
    Cloud Administrator Changes To A New Cg
    Cloud Administrator Unprotects All Vms
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level All
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Deletes Rp4vm Policy
    Cloud Administrator Deletes VRPA Clusters
    Cloud Administrator Deletes Datastore
    Cloud Administrator Deletes Cluster
    Cloud Administrator Deletes Rp4vm Vcenter Relationship
    Cloud Administrator Deletes Hwi
    Cloud Administrator Deletes Vcenter
    Cloud Administrator Deletes Site
    Cloud Administrator Removes Reservation Policy From Blueprint
    Cloud Administrator Removes Reservation Policy From Reservation
    Cloud Administrator Deletes Reservation
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-101-C8: Initialize VSAN RP4VM support in EHC without Data Protection
    [Documentation]    E2E-101 As a RP4VM system administrator, I want to initialize VSAN RP4VM support in EHC without DP
    [Tags]    EHC E2E Workflow
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-101-C8-RP4VM.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Adds Rp4vm Vcenter Relationship
    Cloud Administrator Onboards vsan cluster
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Creates Reservation
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Adds VRPA Clusters
    Cloud Administrator Adds Rp4vm Policy
    Cloud Administrator Deploys Vm
    Cloud Administrator Protects Vm Using New Cg
    Cloud Administrator Provisions Rp4vm Using New Cg
    Cloud Administrator Provisions Rp4vm Using Existing Cg
    Cloud Administrator Changes To An Existing Cg
    Cloud Administrator Changes Boot Sequence
    Cloud Administrator Performs Failover On Protected Vms
    Cloud Administrator Adds Post Failover Synchronization
    Cloud Administrator Deploys Vm
    Cloud Administrator Performs Failover On Protected Vms
    Cloud Administrator Adds Post Failover Synchronization
    Cloud Administrator Protects Vm Using Existing Cg
    Cloud Administrator Changes To A New Cg
    Cloud Administrator Unprotects All Vms
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Rp4vm Policy
    Cloud Administrator Deletes VRPA Clusters
    Cloud Administrator Deletes Cluster
    Cloud Administrator Deletes Rp4vm Vcenter Relationship
    Cloud Administrator Deletes Hwi
    Cloud Administrator Deletes Vcenter
    Cloud Administrator Deletes Site
    Cloud Administrator Removes Reservation Policy From Blueprint
    Cloud Administrator Removes Reservation Policy From Reservation
    Cloud Administrator Deletes Reservation
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-102-C8: Initialize VSAN RP4VM support in EHC with Data Protection
    [Documentation]    E2E-102 As a RP4VM system administrator, I want to initialize RP4VM and VSAN support in EHC with DP
    [Tags]    EHC E2E Workflow
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-102-RP4VM-VSAN-DP.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Adds Rp4vm Vcenter Relationship
    Cloud Administrator Onboards Vsan Cluster
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds Backup Service Level For Deploy Vm
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Creates Reservation
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Adds VRPA Clusters
    Cloud Administrator Adds Rp4vm Policy
    Cloud Administrator Deploys Vm
    Cloud Administrator Protects Vm Using New Cg
    Cloud Administrator Provisions Rp4vm Using New Cg
    Cloud Administrator Provisions Rp4vm Using Existing Cg
    Cloud Administrator Changes To An Existing Cg
    Cloud Administrator Changes Boot Sequence
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Prefailovers Stage Cgs
    Cloud Administrator Performs Failover On Protected Vms
    Cloud Administrator Adds Post Failover Synchronization
    Cloud Administrator Adds Backup Service Level For Set Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Prefailovers Stage Cgs
    Cloud Administrator Performs Failover On Protected Vms
    Cloud Administrator Adds Post Failover Synchronization
    Cloud Administrator Prefailovers Stage Cgs
    Cloud Administrator Prefailovers Unstage Cgs
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Deploys Vm
    Cloud Administrator Protects Vm Using Existing Cg
    Cloud Administrator Changes To A New Cg
    Cloud Administrator Unprotects All Vms
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level All
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Deletes Rp4vm Policy
    Cloud Administrator Deletes VRPA Clusters
    Cloud Administrator Deletes Cluster
    Cloud Administrator Deletes Rp4vm Vcenter Relationship
    Cloud Administrator Deletes Hwi
    Cloud Administrator Deletes Vcenter
    Cloud Administrator Deletes Site
    Cloud Administrator Removes Reservation Policy From Blueprint
    Cloud Administrator Removes Reservation Policy From Reservation
    Cloud Administrator Deletes Reservation
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment