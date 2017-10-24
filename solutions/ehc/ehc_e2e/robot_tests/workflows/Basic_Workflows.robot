*** Settings ***
Library           ehc_e2e.workflow.BaseWorkflow

*** Variables ***
${CONF DIR}  /root/automation/ehc/config/
${SkipTeardown}    False

*** Test Cases ***
E2E-1-C1: Deploy LC1S cluster with Data Protection
    [Documentation]    As a cloud administrator, I would like to deploy LC1S cluster with Data Protection
    [Tags]    EHC E2E Workflow    LC1S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-1-LC1S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Adds Backup Service Level
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
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Deletes Datastore
    Cloud Administrator Edits An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Edits Avamar Grid
    Cloud Administrator Edits Avamar Grid Admin Full
    Cloud Administrator Deletes Avamar Grid
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

E2E-1-C2: Deploy CA1S cluster with Data Protection
    [Documentation]    As a cloud administrator, I would like to deploy CA1S cluster with Data Protection
    [Tags]    EHC E2E Workflow    CA1S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-1-CA1S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Provisions Cloud Storage
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Creates Reservation
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Assigns Storage Reservation Policy To Blueprint
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator Sets No Protection Backup Service Level
    Cloud Administrator Sets Origin Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Deletes Datastore
    Cloud Administrator Edits An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Edits Avamar Grid
    Cloud Administrator Edits Avamar Grid Admin Full
    Cloud Administrator Deletes Avamar Grid
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

E2E-1-C3: Deploy CA2S cluster with Data Protection
    [Documentation]    As a cloud administrator, I would like to deploy CA2S cluster with Data Protection
    [Tags]    EHC E2E Workflow    CA2S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-1-CA2S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Provisions Cloud Storage
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Creates Reservation
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Assigns Storage Reservation Policy To Blueprint
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator Sets No Protection Backup Service Level
    Cloud Administrator Sets Origin Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Deletes Datastore
    Cloud Administrator Edits An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Edits Avamar Grid
    Cloud Administrator Edits Avamar Grid Admin Full
    Cloud Administrator Deletes Avamar Grid
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

E2E-1-C4: Deploy DR2S cluster with Data Protection
    [Documentation]    As a cloud administrator, I would like to deploy DR2S cluster with Data Protection
    [Tags]    EHC E2E Workflow    DR2S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-1-DR2S.config.yaml    ${CONF DIR}generic.yaml
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
    Cloud Administrator Checks Protection Group Created For Datastore
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
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Deletes Datastore
    Cloud Administrator Edits An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Edits Avamar Grid
    Cloud Administrator Edits Avamar Grid Admin Full
    Cloud Administrator Deletes Avamar Grid
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

E2E-1-C5: Deploy MP2S cluster with Data Protection
    [Documentation]    As a cloud administrator, I would like to deploy MP2S cluster with Data Protection
    [Tags]    EHC E2E Workflow    MP2S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-1-MP2S.config.yaml    ${CONF DIR}generic.yaml
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
    Cloud Administrator Adds Backup Service Level
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
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Deletes Datastore
    Cloud Administrator Edits An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Edits Avamar Grid
    Cloud Administrator Edits Avamar Grid Admin Full
    Cloud Administrator Deletes Avamar Grid
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

E2E-1-C6: Deploy MP3S cluster with Data Protection
    [Documentation]    As a cloud administrator, I would like to deploy MP3S cluster with Data Protection
    [Tags]    EHC E2E Workflow    MP3S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-1-MP3S.config.yaml    ${CONF DIR}generic.yaml
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
    Cloud Administrator Adds Backup Service Level
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
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Deletes Datastore
    Cloud Administrator Edits An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Edits Avamar Grid
    Cloud Administrator Edits Avamar Grid Admin Full
    Cloud Administrator Deletes Avamar Grid
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

E2E-1-C8: Deploy VS1S cluster with Data Protection
    [Documentation]    E2E-1 VS1S As a cloud administrator, I would like to deploy VS1S cluster with Data Protection
    [Tags]    EHC E2E Workflow
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-1-VS1S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Adds Backup Service Level
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
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Edits An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Edits Avamar Grid
    Cloud Administrator Edits Avamar Grid Admin Full
    Cloud Administrator Deletes Avamar Grid
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

E2E-2-C1: Deploy LC1S cluster without Data Protection
    [Documentation]    As a cloud administrator, I would like to deploy LC1S cluster without Data Protection
    [Tags]    EHC E2E Workflow    LC1S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-2-LC1S.config.yaml    ${CONF DIR}generic.yaml
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
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
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

E2E-2-C2: Deploy CA1S Cluster Without Data Protection
    [Documentation]    As a Service Architect, I need to deploy a CA1S cluster without Data Protection.
    [Tags]    EHC E2E Workflow    CA1S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-2-CA1S.config.yaml    /${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Provisions Cloud Storage
    Cloud Administrator Creates Reservation
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Assigns Storage Reservation Policy To Blueprint
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
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
    Cloud Administrator Removes Reservation Policy From Reservation
    Cloud Administrator Deletes Reservation
    Cloud Administrator Removes Reservation Policy From Blueprint
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-2-C3: Deploy CA2S Cluster Without Data Protection
    [Documentation]    As a Service Architect, I need to deploy a CA2S cluster without Data Protection.
    [Tags]    EHC E2E Workflow    CA2S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-2-CA2S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Provisions Cloud Storage
    Cloud Administrator Creates Reservation
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Assigns Storage Reservation Policy To Blueprint
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
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
    Cloud Administrator Removes Reservation Policy From Reservation
    Cloud Administrator Deletes Reservation
    Cloud Administrator Removes Reservation Policy From Blueprint
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-2-C4: Deploy DR2S cluster without Data Protection
    [Documentation]    As a cloud administrator, I would like to deploy DR2S cluster without Data Protection.
    [Tags]    EHC E2E Workflow    DR2S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-2-DR2S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Adds Vcenter Relationship
    Cloud Administrator Onboard Cluster
    Cloud Administrator Provisions Cloud Storage
    Cloud Administrator Checks Protection Group Created For Datastore
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Creates Reservation
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
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
    Cloud Administrator Removes Reservation Policy From Blueprint
    Cloud Administrator Deletes Reservation
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-2-C5: Deploy MP2S cluster without Data Protection
    [Documentation]    As a cloud administrator, I would like to deploy MP2S cluster without Data Protection
    [Tags]    EHC E2E Workflow    MP2S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-2-MP2S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Adds Vcenter Relationship
    Cloud Administrator Onboard Cluster
    Cloud Administrator Provisions Cloud Storage
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Creates Reservation
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Assigns Storage Reservation Policy To Blueprint
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
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
    Cloud Administrator Removes Reservation Policy From Blueprint
    Cloud Administrator Deletes Reservation
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-2-C6: Deploy MP3S Cluster Without Data Protection
    [Documentation]    As a Service Architect, I need to deploy a MP3S cluster without Data Protection.
    [Tags]    EHC E2E Workflow    MP3S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-2-MP3S.config.yaml    ${CONF DIR}generic.yaml
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
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
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
    Cloud Administrator Removes Reservation Policy From Reservation
    Cloud Administrator Deletes Reservation
    Cloud Administrator Removes Reservation Policy From Blueprint
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-2-C8: Deploy VS1S cluster without Data Protection
    [Documentation]    As a cloud administrator, I would like to deploy VS1S cluster without Data Protection
    [Tags]    EHC E2E Workflow    VS1S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-2-VS1S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Creates Reservation
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
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

E2E-3-C1: Request and manage VMs in LC1S without Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in LC1S cluster over the cloud without DP.
    [Tags]    EHC E2E Workflow    LC1S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-3-LC1S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-3-C2: Request and manage VMs in CA1S without Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in CA1S cluster over the cloud without DP.
    [Tags]    EHC E2E Workflow    CA1S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-3-CA1S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-3-C3: Request and manage VMs in CA2S without Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in CA2S cluster over the cloud without DP.
    [Tags]    EHC E2E Workflow    CA2S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-3-CA2S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-3-C4: Request and manage VMs in DR2S without Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in DR2S cluster over the cloud without DP.
    [Tags]    EHC E2E Workflow    DR2S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-3-DR2S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-3-C5: Request and manage VMs in MP2S without Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in MP2S cluster over the cloud without DP
    [Tags]    EHC E2E Workflow    MP2S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-3-MP2S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-3-C6: Request and manage VMs in MP3S without Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in MP3S cluster over the cloud without DP
    [Tags]    EHC E2E Workflow    MP3S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-3-MP3S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-3-C8: Request and manage VMs in VS1S without Data Protection
    [Documentation]    As a cloud administrator, I would like to request and manage VMs in VS1S Cluster over the cloud without DP in LC1S.
    [Tags]    EHC E2E Workflow    VS1S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-3-VS1S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-4-C1: Request and manage VMs in LC1S with Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in LC1S cluster over the cloud with DP
    [Tags]    EHC E2E Workflow    LC1S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-4-LC1S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator Sets No Protection Backup Service Level
    Cloud Administrator Sets Origin Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-4-C2: Request and manage VMs in CA1S with Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in CA1S cluster over the cloud with DP
    [Tags]    EHC E2E Workflow    CA1S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-4-CA1S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator Sets No Protection Backup Service Level
    Cloud Administrator Sets Origin Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-4-C3: Request and manage VMs in CA2S with Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in CA2S cluster over the cloud with DP
    [Tags]    EHC E2E Workflow    CA2S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-4-CA2S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator Sets No Protection Backup Service Level
    Cloud Administrator Sets Origin Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-4-C4: Request and manage VMs in DR2S with Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in DR2S cluster over the cloud with DP
    [Tags]    EHC E2E Workflow    DR2S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-4-DR2S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator Sets No Protection Backup Service Level
    Cloud Administrator Sets Origin Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-4-C5: Request and manage VMs in MP2S with Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in MP2S cluster over the cloud with DP
    [Tags]    EHC E2E Workflow    MP2S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-4-LC1S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator Sets No Protection Backup Service Level
    Cloud Administrator Sets Origin Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-4-C6: Request and manage VMs in MP3S with Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in MP3S Cluster over the cloud with out DP
    [Tags]    EHC E2E Workflow    MP3S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-4-MP3S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator Sets No Protection Backup Service Level
    Cloud Administrator Sets Origin Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-4-C8: Request and manage VMs in VS1S with Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in VS1S cluster over the cloud with DP
    [Tags]    EHC E2E Workflow    VS1S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-4-VS1S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator Sets No Protection Backup Service Level
    Cloud Administrator Sets Origin Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-5: maintain datastore
    [Documentation]    E2E-5: As a cloud administrator, I would like to maintain datastore
    [Tags]    EHC E2E Workflow
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-1-LC1S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Provisions Cloud Storage
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Deletes Datastore
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-7-C1: Maintain LC1S DP features
    [Documentation]    As a cloud administrator, I would like to maintain LC1S DP features
    [Tags]    EHC E2E Workflow    LC1S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-7-C1-LC1S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Displays Backup Service Level
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Edits An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Edits Avamar Grid
    Cloud Administrator Edits Avamar Grid Admin Full
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-7-C2: Maintain CA1S DP features
    [Documentation]    As a cloud administrator, I would like to maintain CA1S DP features
    [Tags]    EHC E2E Workflow    CA1S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-7-C2-CA1S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Displays Backup Service Level
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Edits An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Edits Avamar Grid
    Cloud Administrator Edits Avamar Grid Admin Full
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-7-C3: Maintain CA2S DP features
    [Documentation]    As a cloud administrator, I would like to maintain CA2S DP features
    [Tags]    EHC E2E Workflow    CA2S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-7-C3-CA2S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Displays Backup Service Level
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Edits An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Edits Avamar Grid
    Cloud Administrator Edits Avamar Grid Admin Full
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-7-C4: Maintain DR2S DP features
    [Documentation]    As a cloud administrator, I would like to maintain DR2S DP features
    [Tags]    EHC E2E Workflow    DR2S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-7-C4-DR2S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Displays Backup Service Level
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Edits An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Edits Avamar Grid
    Cloud Administrator Edits Avamar Grid Admin Full
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-7-C5: Maintain MP2S DP features
    [Documentation]    As a cloud administrator, I would like to maintain MP2S DP features
    [Tags]    EHC E2E Workflow    MP2S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-7-C5-MP2S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Displays Backup Service Level
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Edits An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Edits Avamar Grid
    Cloud Administrator Edits Avamar Grid Admin Full
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-7-C6: Maintain MP3S DP features
    [Documentation]    As a cloud administrator, I would like to maintain MP3S DP features
    [Tags]    EHC E2E Workflow    MP3S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-7-C6-MP3S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Displays Backup Service Level
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Edits An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Edits Avamar Grid
    Cloud Administrator Edits Avamar Grid Admin Full
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-7-C7: Maintain RP4VM DP features
    [Documentation]    As a cloud administrator, I would like to maintain RP4VM DP features
    [Tags]    EHC E2E Workflow    RP4VM
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-7-C7-RP4VM.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Displays Backup Service Level
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Edits An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Edits Avamar Grid
    Cloud Administrator Edits Avamar Grid Admin Full
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-7-C8: Maintain VS1S DP features
    [Documentation]    As a cloud administrator, I would like to maintain VS1S DP features
    [Tags]    EHC E2E Workflow    VS1S
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-7-C8-VS1S.config.yaml    ${CONF DIR}generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Displays Backup Service Level
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Edits An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Edits Avamar Grid
    Cloud Administrator Edits Avamar Grid Admin Full
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-10: Deploy Multiple VMs
    [Documentation]    E2E-10 As a cloud administrator, I would like to deploy multiple VMs by one deployment
    [Tags]    EHC E2E Workflow
    [Setup]    Apply Settings From Files    ${CONF DIR}generic.yaml    ${CONF DIR}E2EWF-10.config.yaml    ${CONF DIR}generic.yaml
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
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
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
