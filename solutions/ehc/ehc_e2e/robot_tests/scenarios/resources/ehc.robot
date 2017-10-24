*** Settings ***
Library           ehc_e2e.scenario.BaseScenario

*** Variables ***
${SkipTeardown}    False
${CONF DIR}       /root/automation/ehc/config/
#${CONF DIR}       C:/git_repo/solutions/ehc/ehc_e2e/conf/

*** Keywords ***
Cloud Administrator Onboard LC1S Cluster For Scenario
    Prepare Workflow Data    ${CONF DIR}generic.yaml    ${CONF DIR}scenario_conf/E2ESN-1-LC1S.config.yaml
    Cloud Administrator Opens Browser
    Login To Vra As Config Admin
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Logout
    Login To Vra As Backup Admin
    Cloud Administrator Adds Avamar Grid Unselect Proxy
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Adds Avamar Proxy
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Logout
    Login To Vra As Storage Admin
    Cloud Administrator Provision Multiple Cloud Storage
    Cloud Administrator Logout
    Login To Vra As Config Admin
    Cloud Administrator Assigns Datastores And Reservation Policy To Reservation
    Cloud Administrator Logout
    Login To Vra As Tenant Bg User
    Cloud Administrator Deploys Vm Parallel
    Cloud Administrator Closes Browser
    Update Scenario Context

Cloud Administrator Onboard CA1S Cluster For Scenario
    Prepare Workflow Data    ${CONF DIR}generic.yaml    ${CONF DIR}scenario_conf/E2ESN-1-CA1S.config.yaml
    Cloud Administrator Opens Browser
    Login To Vra As Config Admin
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Logout
    Login To Vra As Backup Admin
    Cloud Administrator Adds Avamar Grid Unselect Proxy
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Adds Avamar Proxy
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Logout
    Login To Vra As Storage Admin
    Cloud Administrator Provision Multiple Cloud Storage
    Cloud Administrator Logout
    Login To Vra As Config Admin
    Cloud Administrator Assigns Datastores And Reservation Policy To Reservation
    Cloud Administrator Logout
    Login To Vra As Tenant Bg User
    Cloud Administrator Deploys Vm Parallel
    Cloud Administrator Closes Browser
    Update Scenario Context

Cloud Administrator Onboard CA2S Cluster For Scenario
    Prepare Workflow Data    ${CONF DIR}generic.yaml    ${CONF DIR}scenario_conf/E2ESN-1-CA2S.config.yaml
    Cloud Administrator Opens Browser
    Login To Vra As Config Admin
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboard Cluster
    Cloud Administrator Logout
    Login To Vra As Backup Admin
    Cloud Administrator Adds Avamar Grid Unselect Proxy
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Adds Avamar Proxy
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Logout
    Login To Vra As Storage Admin
    Cloud Administrator Provision Multiple Cloud Storage
    Cloud Administrator Logout
    Login To Vra As Config Admin
    Cloud Administrator Assigns Datastores And Reservation Policy To Reservation
    Cloud Administrator Assigns Storage Reservation Policy To Blueprint
    Cloud Administrator Logout
    Login To Vra As Tenant Bg User
    Cloud Administrator Deploys Vm Parallel
    Cloud Administrator Closes Browser
    Update Scenario Context

Cloud Administrator Onboard DR2S Cluster For Scenario
    Prepare Workflow Data    ${CONF DIR}generic.yaml    ${CONF DIR}scenario_conf/E2ESN-1-DR2S.config.yaml
    Cloud Administrator Opens Browser
    Login To Vra As Config Admin
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Extends Vcenter Relationship
    Cloud Administrator Onboard Cluster
    Cloud Administrator Logout
    Login To Vra As Backup Admin
    Cloud Administrator Adds Avamar Grid Unselect Proxy
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Adds Avamar Proxy
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Logout
    Login To Vra As Storage Admin
    Cloud Administrator Provision Multiple Cloud Storage
    Cloud Administrator Logout
    Login To Vra As Config Admin
    Cloud Administrator Assigns Datastores And Reservation Policy To Reservation
    Cloud Administrator Logout
    Login To Vra As Tenant Bg User
    Cloud Administrator Deploys Vm Parallel
    Cloud Administrator Closes Browser
    Update Scenario Context

Cloud Administrator Onboard DR2S Cluster Add Vceneter Relationship For Scenario
    Prepare Workflow Data    ${CONF DIR}generic.yaml    ${CONF DIR}scenario_conf/E2ESN-1-DR2S-Add-VR.config.yaml
    Cloud Administrator Opens Browser
    Login To Vra As Config Admin
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Cloud Administrator Adds Vcenter Relationship
    Cloud Administrator Onboard Cluster
    Cloud Administrator Logout
    Login To Vra As Backup Admin
    Cloud Administrator Adds Avamar Grid Unselect Proxy
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Adds Avamar Proxy
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Logout
    Login To Vra As Storage Admin
    Cloud Administrator Provision Multiple Cloud Storage
    Cloud Administrator Logout
    Login To Vra As Config Admin
    Cloud Administrator Assigns Datastores And Reservation Policy To Reservation
    Cloud Administrator Logout
    Login To Vra As Tenant Bg User
    Cloud Administrator Deploys Vm Parallel
    Cloud Administrator Closes Browser
    Update Scenario Context

Cloud Administrator Tear Down Scenario
    Merge Context
    Cloud Administrator Opens Browser
    Login To Vra As Tenant Bg User
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Login
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Deletes Rp4vm Policy
    Cloud Administrator Deletes VRPA Clusters
    Cloud Administrator Deletes Datastore
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Deletes Cluster
    Cloud Administrator Deletes Vcenter Relationship
    Cloud Administrator Deletes Hwi
    Cloud Administrator Deletes Vcenter
    Cloud Administrator Deletes Site
    Cloud Administrator Removes Reservation Policy From Reservation
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    Reset Scenario Context

Cloud Administrator Onboard RP4VM Cluster For Scenario
    Prepare Workflow Data    ${CONF DIR}generic.yaml    ${CONF DIR}scenario_conf/E2ESN-1-RP4VM.config.yaml
    Cloud Administrator Opens Browser
    Login To Vra As Config Admin
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Rp4vm Vcenter Relationship
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboards Local Cluster
    Cloud Administrator Adds VRPA Clusters
    Cloud Administrator Adds Rp4vm Policy
    Cloud Administrator Logout
    Login To Vra As Backup Admin
    Cloud Administrator Adds Avamar Grid Unselect Proxy
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Adds Avamar Proxy
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Logout
    Login To Vra As Storage Admin
    Cloud Administrator Provision Multiple Cloud Storage
    Cloud Administrator Logout
    Login To Vra As Config Admin
    Cloud Administrator Assigns Datastores And Reservation Policy To Reservation
    Cloud Administrator Logout
    Login To Vra As Tenant Bg User
    Cloud Administrator Deploys Vm Parallel
    Cloud Administrator Closes Browser
    Update Scenario Context

Basic DR2S with Data Protection
    Prepare Workflow Data    ${CONF DIR}generic.yaml    ${CONF DIR}scenario_conf/E2ESN-4-BASIC-DR2S.config.yaml
    Cloud Administrator Opens Browser
    Login To Vra As Config Admin
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Hwi
    Write Added Hwi From Current Workflow To Scenario
    Cloud Administrator Adds Vcenter Relationship
    Cloud Administrator Onboard Cluster
    Cloud Administrator Logout
    Login To Vra As Backup Admin
    Cloud Administrator Adds Avamar Grid Unselect Proxy
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Associates Cluster To Asr
    Write Added Asr From Current Workflow To Scenario
    Cloud Administrator Adds Avamar Proxy
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Logout
    Login To Vra As Storage Admin
    Cloud Administrator Provision Multiple Cloud Storage
    Cloud Administrator Logout
    Login To Vra As Config Admin
    Cloud Administrator Assigns Datastores And Reservation Policy To Reservation
    Cloud Administrator Logout
    Login To Vra As Tenant Bg User
    Cloud Administrator Deploys Vm Parallel
    Cloud Administrator Closes Browser
    Update Scenario Context

Additional DR2S Clusters in Existing VC DR-Pair with Data Protection
    Prepare Workflow Data    ${CONF DIR}generic.yaml    ${CONF DIR}scenario_conf/E2ESN-4-ADDITIONAL-DR2S.config.yaml
    Cloud Administrator Opens Browser
    Login To Vra As Config Admin
    Write Added Hwi From Scenario To Current Workflow
    Reverse Added Hwi In Current Workflow
    Cloud Administrator Onboard Cluster
    Cloud Administrator Logout
    Login To Vra As Backup Admin
    Write Added Asr From Scenario To Current Workflow
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Adds Avamar Proxy
    Cloud Administrator Logout
    Login To Vra As Storage Admin
    Generate Parameters For Provision Cloud Storage
    Cloud Administrator Provision Multiple Cloud Storage
    Cloud Administrator Logout
    Login To Vra As Config Admin
    Cloud Administrator Assigns Datastores And Reservation Policy To Reservation
    Cloud Administrator Logout
    Login To Vra As Tenant Bg User
    Cloud Administrator Deploys Vm Parallel
    Cloud Administrator Closes Browser
    Update Scenario Context

Basic LC1S And RP4VM Deployment with Data Protection
    Prepare Workflow Data    ${CONF DIR}generic.yaml    ${CONF DIR}scenario_conf/E2ESN-3-RP4VM.config.yaml
    Initialize Workflow Relation Mapping
    Cloud Administrator Opens Browser
    Login To Vra As Config Admin
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Rp4vm Vcenter Relationship
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboards Local Cluster
    Cloud Administrator Adds VRPA Clusters
    Cloud Administrator Adds Rp4vm Policy
    Cloud Administrator Logout
    Login To Vra As Backup Admin
    Cloud Administrator Adds Avamar Grid Unselect Proxy
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Adds Avamar Proxy
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Logout
    Login To Vra As Storage Admin
    Cloud Administrator Provision Multiple Cloud Storage
    Cloud Administrator Logout
    Login To Vra As Config Admin
    Cloud Administrator Assigns Datastores And Reservation Policy To Reservation With Mapping
    Update Backup Service Level To Mapping Relation
    Cloud Administrator Logout
    Login To Vra As Tenant Bg User
    Cloud Administrator Deploys Vm Parallel For Relation Mappings
    Cloud Administrator Closes Browser
    Write Workflow Relation Mappings From Current Workflow To Scenario
    Update Scenario Context

Basic Provision Local Workloads to Existing LC1S And RP4VM with DP
    Prepare Workflow Data    ${CONF DIR}generic.yaml    ${CONF DIR}scenario_conf/E2ESN-3-LC1S.config.yaml
    Write Workflow Relation Mappings From Scenario To Current Workflow
    Cloud Administrator Opens Browser
    Login To Vra As Config Admin
    Update Blueprints To Mapping Relation
    Cloud Administrator Logout
    Login To Vra As Tenant Bg User
    Cloud Administrator Deploys Vm Parallel For Relation Mappings
    Cloud Administrator Closes Browser
    Update Scenario Context

VSAN LC1S And RP4VM Deployment with Data Protection
    Prepare Workflow Data    ${CONF DIR}generic.yaml    ${CONF DIR}scenario_conf/E2ESN-2-RP4VM.config.yaml
    Initialize Workflow Relation Mapping
    Cloud Administrator Opens Browser
    Login To Vra As Config Admin
    Cloud Administrator Adds Site
    Cloud Administrator Adds Vcenter
    Cloud Administrator Adds Rp4vm Vcenter Relationship
    Cloud Administrator Adds Hwi
    Cloud Administrator Onboards Vsan Cluster
    Cloud Administrator Adds VRPA Clusters
    Cloud Administrator Adds Rp4vm Policy
    Cloud Administrator Logout
    Login To Vra As Backup Admin
    Cloud Administrator Adds Avamar Grid Unselect Proxy
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Adds Avamar Proxy
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Logout
    Login To Vra As Storage Admin
    Cloud Administrator Assigns Datastores And Reservation Policy To Reservation With Mapping
    Update Backup Service Level To Mapping Relation
    Cloud Administrator Logout
    Login To Vra As Tenant Bg User
    Cloud Administrator Deploys Vm Parallel For Relation Mappings
    Cloud Administrator Closes Browser
    Write Workflow Relation Mappings From Current Workflow To Scenario
    Update Scenario Context

LC1S Cluster Pairs with Data Protection and Existing Vcenter Relationship
    Prepare Workflow Data    ${CONF DIR}generic.yaml    ${CONF DIR}scenario_conf/Basic-LC1S-Deployment-with-DP-and-Existing-VC-Relationship.config.yaml
    Initialize Workflow Relation Mapping
    Cloud Administrator Opens Browser
    Site With Same Name Exists
    Vcenter With Same Name Exists
    Hwi with Same Name Exists
    Vcenter Relationship With Same Name Exists
    Login To Vra As Config Admin
    Cloud Administrator Onboards Local Cluster
    Cloud Administrator Logout
    Login To Vra As Backup Admin
    Cloud Administrator Adds Avamar Grid Unselect Proxy
    Cloud Administrator Adds Avamar Site Relationship
    Cloud Administrator Adds An Avamar Replication Relationship
    Cloud Administrator Associates Cluster To Asr
    Cloud Administrator Adds Backup Service Level
    Cloud Administrator Logout
    Login To Vra As Storage Admin
    Cloud Administrator Provision Multiple Cloud Storage
    Cloud Administrator Logout
    Login To Vra As Config Admin
    Cloud Administrator Assigns Datastores And Reservation Policy To Reservation With Mapping
    Cloud Administrator Logout
    Login To Vra As Tenant Bg User
    Cloud Administrator Deploys Vm Parallel For Relation Mappings
    Cloud Administrator Adds Avamar Proxy
    Cloud Administrator Closes Browser

Cloud Administrator Tear Down Scenario And Keep Existing Vcenter Relationship
    Merge Context
    Cloud Administrator Opens Browser
    Login To Vra As Tenant Bg User
    Pass Execution If    ${SkipTeardown}    Checking whether to skip tear down by user input
    Cloud Administrator Destroy Vms
    Cloud Administrator Login
    Cloud Administrator Deletes Backup Service Level
    Cloud Administrator Deletes Rp4vm Policy
    Cloud Administrator Deletes VRPA Clusters
    Cloud Administrator Deletes Datastore
    Cloud Administrator Deletes An Avamar Replication Relationship
    Cloud Administrator Deletes An Avamar Site Relationship
    Cloud Administrator Deletes Avamar Grid
    Cloud Administrator Deletes Cluster
    Cloud Administrator Removes Reservation Policy From Reservation
    Cloud Administrator Logout
    Cloud Administrator Closes Browser
    Reset Scenario Context
