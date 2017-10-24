*** Settings ***
Library           ehc_e2e.workflow.AvamarFailActionWorkflow

*** Variables ***
${CONF DIR}   /root/automation/ehc/config/
${SkipTeardown}    False

*** Test Cases ***
E2E-8-C3-1-CA2S: As a cloud administrator, I would like to maintain CA2S Avamar grid failover/failback features
    [Documentation]    As a cloud administrator, I would like to maintain CA2S Avamar grid failover/failback features
    [Tags]    EHC E2E Workflow
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-8-C3-CA2S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
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
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Failovers Avamar Policies For Offline Avamar Grid
    Cloud Administrator Adds Backup Service Level For Set Vm
    Cloud Administrator Deploys Vm
    Cloud Administrator Sets Backup Service Level For All Vms
    Cloud Administrator On Demand Backup For All Vms
    Cloud Administrator On Demand Restore For All Vms
    Cloud Administrator Failbacks Avamar Policies After Restoring Avamar Grid
    Cloud Administrator Adds Backup Service Level For Set Vm
    Cloud Administrator Deploys Vm
    Cloud Administrator Sets Backup Service Level For All Vms
    Cloud Administrator On Demand Backup For All Vms
    Cloud Administrator On Demand Restore For All Vms
    Cloud Administrator Displays Backup Service Level All
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level All
    Cloud Administrator Deletes Datastore
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Deletes Cluster
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

E2E-8-C3-2-CA2S: As a cloud administrator, I would like to maintain CA2S Avamar failover/failback features after site failure
    [Documentation]    As a cloud administrator, I would like to maintain CA2S Avamar failover/failback features after site failure
    [Tags]    EHC E2E Workflow
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-8-C3-CA2S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
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
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Failovers Avamar Grids After Site Failure
    Cloud Administrator Adds Backup Service Level For Set Vm
    Cloud Administrator Deploys Vm
    Cloud Administrator Sets Backup Service Level For All Vms
    Cloud Administrator On Demand Backup For All Vms
    Cloud Administrator On Demand Restore For All Vms
    Cloud Administrator Failbacks Avamar Policies After Site Restoration
    Cloud Administrator Adds Backup Service Level For Set Vm
    Cloud Administrator Deploys Vm
    Cloud Administrator Sets Backup Service Level For All Vms
    Cloud Administrator On Demand Backup For All Vms
    Cloud Administrator On Demand Restore For All Vms
    Cloud Administrator Displays Backup Service Level All
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level All
    Cloud Administrator Deletes Datastore
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Deletes Cluster
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

E2E-8-C5-MP2S: As a cloud administrator, I would like to maintain MP2S Avamar failover/failback features
    [Documentation]    As a cloud administrator, I would like to maintain MP2S Avamar failover/failback features
    [Tags]    EHC E2E Workflow
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-8-C5-MP2S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Adds Vcenter Relationship
    Cloud Administrator Onboard Cluster
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
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
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Failovers Avamar Grids After Site Failure
    Cloud Administrator Failovers Avamar Policies For Offline Avamar Grid
    Cloud Administrator Adds Backup Service Level For Set Vm
    Cloud Administrator Sets Backup Service Level For All Vms
    Cloud Administrator On Demand Backup For All Vms
    Cloud Administrator On Demand Restore For All Vms
    Cloud Administrator Failbacks Avamar Policies After Site Restoration
    Cloud Administrator Failbacks Avamar Policies After Restoring Avamar Grid
    Cloud Administrator Adds Backup Service Level For Set Vm
    Cloud Administrator Deploys Vm
    Cloud Administrator Sets Backup Service Level For All Vms
    Cloud Administrator On Demand Backup For All Vms
    Cloud Administrator On Demand Restore For All Vms
    Cloud Administrator Displays Backup Service Level All
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level All
    Cloud Administrator Deletes Datastore
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Deletes Cluster
    Cloud Administrator Deletes Vcenter Relationship
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

E2E-8-C6-MP3S: As a cloud administrator, I would like to maintain MP3S Avamar failover/failback features
    [Documentation]    As a cloud administrator, I would like to maintain MP3S Avamar failover/failback features
    [Tags]    EHC E2E Workflow MP3S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-8-C6-MP3S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Adds Vcenter Relationship
    Cloud Administrator Onboard Cluster
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
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
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Failovers Avamar Grids After Site Failure
    Cloud Administrator Failovers Avamar Policies For Offline Avamar Grid
    Cloud Administrator Adds Backup Service Level For Set Vm
    Cloud Administrator Sets Backup Service Level For All Vms
    Cloud Administrator On Demand Backup For All Vms
    Cloud Administrator On Demand Restore For All Vms
    Cloud Administrator Failbacks Avamar Policies After Site Restoration
    Cloud Administrator Failbacks Avamar Policies After Restoring Avamar Grid
    Cloud Administrator Adds Backup Service Level For Set Vm
    Cloud Administrator Deploys Vm
    Cloud Administrator Sets Backup Service Level For All Vms
    Cloud Administrator On Demand Backup For All Vms
    Cloud Administrator On Demand Restore For All Vms
    Cloud Administrator Displays Backup Service Level All
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level All
    Cloud Administrator Deletes Datastore
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Deletes Cluster
    Cloud Administrator Deletes Vcenter Relationship
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

