*** Settings ***
Library           ehc_e2e.workflow.RP4VMWorkflow

*** Test Cases ***
E2E-1:Deploy LC1S cluster with Data Protection
    [Documentation]    As a cloud administrator, I would like to deploy LC1S cluster with Data Protection
    [Tags]    EHC E2E Workflow    LC1S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-1-LC1S.config.yaml    /root/automation/ehc/config/generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds Backup Service Level
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
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Run Admin Report
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
    Cloud Administrator Removes Reservation Policy From Blueprint
    Cloud Administrator Removes Reservation Policy From Reservation
    Cloud Administrator Deletes Reservation
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-2:Deploy LC1S cluster without Data Protection
    [Documentation]    As a cloud administrator, I would like to deploy LC1S cluster without Data Protection
    [Tags]    EHC E2E Workflow    LC1S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-2-LC1S.config.yaml    /root/automation/ehc/config/generic.yaml
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
    Cloud Administrator Edits Cluster Site
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

E2E-3: Request and manage VMs in LC1S without Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in LC1S Cluster over the cloud without DP
    [Tags]    EHC E2E Workflow    LC1S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-3-LC1S.config.yaml    /root/automation/ehc/config/generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-3-C1: Request and manage VMs in different types' Cluster over the cloud without DP in LC1S
    [Documentation]    As a cloud end user, I would like to request and manage VMs in different types' Cluster over the cloud without DP in LC1S
    [Tags]    EHC E2E Workflow    LC1S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-3-C1-LC1S.config.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment


E2E-7-C1: Maintain LC1S DP features
    [Documentation]    As a cloud administrator, I would like to maintain LC1S DP features
    [Tags]    EHC E2E Workflow    LC1S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-7-C1-LC1S.config.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Run Admin Report
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
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-7-C2-CA1S.config.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Run Admin Report
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
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-7-C3-CA2S.config.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Run Admin Report
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
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-7-C4-DR2S.config.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Run Admin Report
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
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-7-C5-MP2S.config.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Run Admin Report
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
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-7-C6-MP3S.config.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Run Admin Report
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
    [Documentation]    As a cloud administrator, I would like to maintain CA1S DP features
    [Tags]    EHC E2E Workflow    RP4VM
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-7-C7-RP4VM.config.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Edits An Avamar Site Relationship
    Cloud Administrator Gets Asrs From Vro
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Gets Arrs From Vro
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Run Admin Report
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

E2E-4:Request and manage VMs in LC1S with Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in LC1S cluster over the cloud with DP
    [Tags]    EHC E2E Workflow    LC1S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-4-LC1S.config.yaml    /root/automation/ehc/config/generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Run Admin Report
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-5: maintain datastore
    [Documentation]    E2E-5: As a cloud administrator, I would like to maintain datastore
    [Tags]    EHC E2E Workflow
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-5.config.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Provisions Cloud Storage
    Cloud Administrator Deletes Datastore
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-1: Deploy CA2S Cluster With Data Protection
    [Documentation]    As a Service Architect, I need to deploy a CA2S cluster with Data Protection.
    [Tags]    EHC E2E Workflow    CA2S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-1-CA2S.config.yaml    /root/automation/ehc/config/generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Provisions Cloud Storage
    Cloud Administrator Creates Reservation
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Runs Backup Service Level
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
    Cloud Administrator Removes Reservation Policy From Blueprint
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-2: Deploy CA2S Cluster Without Data Protection
    [Documentation]    As a Service Architect, I need to deploy a CA2S cluster without Data Protection.
    [Tags]    EHC E2E Workflow    CA2S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-2-CA2S.config.yaml    /root/automation/ehc/config/generic.yaml
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
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Datastore
    Cloud Administrator Deletes Cluster
    Cloud Administrator Deletes Hwi
    Cloud Administrator Deletes Vcenter
    Cloud Administrator Deletes Site
    Cloud Administrator Removes Reservation Policy From Reservation
    Cloud Administrator Deletes Reservation
    Cloud Administrator Removes Reservation Policy From Blueprint
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-3:Request and manage VMs in CA2S without Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in CA2S Cluster over the cloud without DP
    [Tags]    EHC E2E Workflow    CA2S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-3-CA2S.config.yaml    /root/automation/ehc/config/generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-4:Deploy CA2S cluster with Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in CA2S cluster over the cloud with DP
    [Tags]    EHC E2E Workflow    CA2S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-4-CA2S.config.yaml    /root/automation/ehc/config/generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Run Admin Report
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-1: Deploy DR2S cluster with Data Protection
    [Documentation]    E2E-2 DR2S As a cloud administrator, I would like to deploy DR2S cluster with Data Protection
    [Tags]    EHC E2E Workflow    DR2S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-1-DR2S.config.yaml    /root/automation/ehc/config/generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Adds Vcenter Relationship
    Cloud Administrator Onboard Cluster
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds Backup Service Level
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
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Run Admin Report
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level
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

E2E-2: Deploy DR2S cluster without Data Protection
    [Documentation]    As a cloud administrator, I would like to deploy DR2S cluster without Data Protection.
    [Tags]    EHC E2E Workflow    DR2S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-2-DR2S.config.yaml    /root/automation/ehc/config/generic.yaml
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
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Datastore
    Cloud Administrator Edits Cluster Hwi
    Cloud Administrator Edits Cluster Site
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

E2E-3: Request and manage VMs in in DR2S without Data Protection
    [Documentation]    As a cloud end user, I would like to request and manage VMs in DR2S cluster over the cloud without DP.
    [Tags]    EHC E2E Workflow    DR2S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-3-DR2S.config.yaml    /root/automation/ehc/config/generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-4: Request and manage VMs in in DR2S with Data Protection
    [Documentation]    E2E-4 DR2S As a cloud end user, I would like to request and manage VMs in DR2S Cluster over the cloud with DP
    [Tags]    EHC E2E Workflow    DR2S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-4-DR2S.config.yaml    /root/automation/ehc/config/generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Run Admin Report
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-1: Deploy MP3S cluster with Data Protection
    [Documentation]    E2E-1 MP3S As a cloud administrator, I would like to deploy MP3S cluster with Data Protection
    [Tags]    EHC E2E Workflow    MP3S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-1-MP3S.config.yaml    /root/automation/ehc/config/generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Adds Vcenter Relationship
    Cloud Administrator Onboard Cluster
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Associates Avamar Proxies With Cluster
    Cloud Administrator Adds Backup Service Level
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
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Run Admin Report
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Deletes Datastore
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Deletes Cluster
    Cloud Administrator Deletes Vcenter Relationship
    Cloud Administrator Deletes Hwi
    Cloud Administrator Deletes Vcenter
    Cloud Administrator Deletes Site
    Cloud Administrator Deletes Reservation
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-2: Deploy MP3S cluster without Data Protection
    [Documentation]    E2E-2 MP3S As a cloud administrator, I would like to deploy MP3S cluster without Data Protection
    [Tags]    EHC E2E WorkFlow    MP3S
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
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Datastore
    Cloud Administrator Deletes Cluster
    Cloud Administrator Deletes Vcenter Relationship
    Cloud Administrator Deletes Hwi
    Cloud Administrator Deletes Vcenter
    Cloud Administrator Deletes Site
    Cloud Administrator Removes Reservation Policy From Reservation
    Cloud Administrator Deletes Reservation
    Cloud Administrator Removes Reservation Policy From Blueprint
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser

E2E-3: Request and manage VMs in MP3S without Data Protection
    [Documentation]    E2E-3 MP3S As a cloud end user, I would like to request and manage VMs in MP3S cluster over the cloud without Data Protection.
    [Tags]    EHC E2E WorkFlow    MP3S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-3-MP3S.config.yaml    /root/automation/ehc/config/generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-4: Request and manage VMs in MP3S with Data Protection
    [Documentation]    E2E-4 MP3S As a cloud end user, I would like to request and manage VMs in MP3S cluster over the cloud with Data Protection.
    [Tags]    EHC E2E WorkFlow    MP3S
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-4-MP3S.config.yaml    /root/automation/ehc/config/generic.yaml
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Deploys Vm
    Cloud Administrator Operates Vm
    Cloud Administrator Sets Backup Service Level
    Cloud Administrator On Demand Backup Vm
    Cloud Administrator On Demand Restore Vm
    Cloud Administrator Displays Backup Service Level
    Cloud Administrator Run Admin Report
    Cloud Administrator Destroy Vms
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment

E2E-101: Initialize RP4VM support in EHC without Data Protection
    [Documentation]    E2E-101 As a RP4VM system administrator, I want to initialize RP4VM support in EHC without DP
    [Tags]    EHC E2E Workflow    RP4VM
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-101-RP4VM.config.yaml    /root/automation/ehc/config/generic.yam
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Adds Rp4vm Vcenter Relationship
    Cloud Administrator Onboards Local Cluster
    Cloud Administrator Provisions Cloud Storage
    Cloud Administrator Adds VRPA Clusters
    Cloud Administrator Adds Rp4vm Policy
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Creates Reservation
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Provisions Rp4vm Using New Cg
    Cloud Administrator Provisions Rp4vm Using Existing Cg
    Cloud Administrator Deploys Vm
    Cloud Administrator Protects Vm Using New Cg
    Cloud Administrator Deploys Vm
    Cloud Administrator Protects Vm Using Existing Cg
    Cloud Administrator Changes To An Existing Cg
    Cloud Administrator Changes Boot Sequence
    Cloud Administrator Performs Failover On Protected Vms
    Cloud Administrator Adds Post Failover Synchronization
    Cloud Administrator Provisions Rp4vm Using Existing Cg
    Cloud Administrator Deploys Vm
    Cloud Administrator Protects Vm Using Existing Cg
    Cloud Administrator Changes To An Existing Cg
    Cloud Administrator Changes Boot Sequence
    Cloud Administrator Unprotects All Vms
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Rp4vm Vcenter Relationship
    Cloud Administrator Deletes Rp4vm Policy
    Cloud Administrator Deletes VRPA Clusters
    Cloud Administrator Deletes Datastore
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

E2E-102: Initialize RP4VM support in EHC with Data Protection
    [Documentation]    E2E-102 As a RP4VM system administrator, I want to initialize RP4VM support in EHC with DP
    [Tags]    EHC E2E Workflow    RP4VM
    [Setup]    Apply Settings From Files    /root/automation/ehc/config/generic.yaml    /root/automation/ehc/config/E2EWF-102-RP4VM-DP.config.yaml    /root/automation/ehc/config/generic.yam
    Cloud Administrator Opens Browser
    Cloud Administrator Login
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Adds Rp4vm Vcenter Relationship
    Cloud Administrator Onboards Local Cluster
    Cloud Administrator Provisions Cloud Storage
    Cloud Administrator Adds Avamar Grid
    Cloud Administrator Adds VRPA Clusters
    Cloud Administrator Adds Rp4vm Policy
    Cloud Administrator Creates Reservation Policy
    Cloud Administrator Creates Reservation
    Cloud Administrator Assigns Reservation Policy To Reservation
    Cloud Administrator Assigns Reservation Policy To Blueprint
    Cloud Administrator Provisions Rp4vm Using New Cg
    Cloud Administrator Provisions Rp4vm Using Existing Cg
    Cloud Administrator Deploys Vm
    Cloud Administrator Protects Vm Using New Cg
    Cloud Administrator Deploys Vm
    Cloud Administrator Protects Vm Using Existing Cg
    Cloud Administrator Changes To An Existing Cg
    Cloud Administrator Changes Boot Sequence
    Cloud Administrator Performs Failover On Protected Vms
    Cloud Administrator Adds Post Failover Synchronization
    Cloud Administrator Provisions Rp4vm Using Existing Cg
    Cloud Administrator Deploys Vm
    Cloud Administrator Protects Vm Using Existing Cg
    Cloud Administrator Changes To An Existing Cg
    Cloud Administrator Changes Boot Sequence
    Cloud Administrator Unprotects All Vms
    Cloud Administrator Destroy Vms
    Cloud Administrator Deletes Rp4vm Vcenter Relationship
    Cloud Administrator Deletes Rp4vm Policy
    Cloud Administrator Deletes VRPA Clusters
    Cloud Administrator Deletes Datastore
    Cloud Administrator Deletes Cluster
    Cloud Administrator Deletes Hwi
    Cloud Administrator Deletes Vcenter
    Cloud Administrator Deletes Site
    Cloud Administrator Deletes Reservation
    Cloud Administrator Deletes Reservation Policy
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    [Teardown]    Clean Up Environment
