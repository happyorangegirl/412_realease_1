*** Settings ***
Library           ehc_e2e.scenario.BaseScenario
Resource          /root/automation/ehc/resources/ehc.robot


*** Test Cases ***
E2E-SN-1: Deploy LC1S RP4VM and DR2S cluster
    [Documentation]    As a cloud administrator, I would like to deploy LC1S, RP4VM, DR2S cluster with Data Protection in the same tenant
    [Tags]    EHC E2E Scenario    LC1S    RP4VM    DR2S
    [Setup]    Apply Settings For Scenario
    Cloud Administrator Onboard LC1S Cluster For Scenario
    Cloud Administrator Onboard RP4VM Cluster For Scenario
    Cloud Administrator Onboard DR2S Cluster For Scenario
    Cloud Administrator Tear Down Scenario
    [Teardown]    Clean Up Environment For Scenario

E2E-SN-2: Deploy VSAN LC1S and RP4VM clusters pair
    [Documentation]    As an EHC Tester, I want to have a partner-pair of LC1S Clusters and provision both Replicated and Non-Replicated VMs with Data Protection.
    [Tags]    EHC E2E Scenario  VSAN  RP4VM    LC1S
    [Setup]    Apply Settings For Scenario
    VSAN LC1S And RP4VM Deployment with Data Protection
    Basic Provision Local Workloads to Existing LC1S And RP4VM with DP
    Cloud Administrator Tear Down Scenario
    [Teardown]    Clean Up Environment For Scenario


E2E-SN-3: Deploy LC1S and RP4VM clusters pair
    [Documentation]    As a cloud administrator, I would like to deploy a partner-pair of LC1S Clusters and Provision both Replicated and Non-Replicated VMs with Data Protection in the same tenant.
    [Tags]    EHC E2E Scenario    RP4VM    LC1S
    [Setup]    Apply Settings For Scenario
    Basic LC1S And RP4VM Deployment with Data Protection
    Basic Provision Local Workloads to Existing LC1S And RP4VM with DP
    Cloud Administrator Tear Down Scenario
    [Teardown]    Clean Up Environment For Scenario


E2E-SN-4: Deploy Bidirectional DR2S clusters
    [Documentation]    As a cloud administrator, I would like to deploy bi-directional DR2S cluster with workload replication in the same tenant
    [Tags]    EHC E2E Scenario    DR2S    Bi-directional
    [Setup]    Apply Settings For Scenario
    Basic DR2S with Data Protection
    Additional DR2S Clusters in Existing VC DR-Pair with Data Protection
    Cloud Administrator Tear Down Scenario
    [Teardown]    Clean Up Environment For Scenario


E2E-SN-5: Deploy CA2S CA1S and RP4VM cluster
    [Documentation]    As a cloud administrator, I would like to deploy CA2S, CA1S, RP4VM cluster with Data Protection in the same tenant
    [Tags]    EHC E2E Scenario    CA2S    CA1S    RP4VM
    [Setup]    Apply Settings For Scenario
    Cloud Administrator Onboard CA2S Cluster For Scenario
    Cloud Administrator Onboard CA1S Cluster For Scenario
    Cloud Administrator Onboard RP4VM Cluster For Scenario
    Cloud Administrator Tear Down Scenario
    [Teardown]    Clean Up Environment For Scenario

E2E-SN-6: Deploy CA2S DR and RP4VM cluster
    [Documentation]    As a cloud administrator, I would like to deploy CA2S, DR, RP4VM cluster with Data Protection in the same tenant
    [Tags]    EHC E2E Scenario    CA2S    DR    RP4VM
    [Setup]    Apply Settings For Scenario
    Cloud Administrator Onboard CA2S Cluster For Scenario
    Cloud Administrator Onboard DR2S Cluster Add Vceneter Relationship For Scenario
    Cloud Administrator Onboard RP4VM Cluster For Scenario
    Cloud Administrator Tear Down Scenario
    [Teardown]    Clean Up Environment For Scenario

E2E-SN-C9: Deploy LC1S Cluster Pairs with Data Protection and Existing Vcenter Rleationship
    [Documentation]    As a cloud administrator, I would like to deploy LC1S cluster with Data Protection
    [Tags]    EHC E2E Scenario    LC1S    Pair
    [Setup]    Apply Settings For Scenario
    LC1S Cluster Pairs with Data Protection and Existing Vcenter Relationship
    Cloud Administrator Tear Down Scenario And Keep Existing Vcenter Relationship
    [Teardown]    Clean Up Environment For Scenario
