enum_clusters = (
    'VS1S'
)


# TODO: use true data source
def all_workflows():
    workflows = []
    workflows.append(
        {'id': 0, 'group': 'Common Configuration', 'workflow': 'Generic configuration for all workflows'})
    workflows.append(
        {'id': 1, 'group': 'Basic Workflows', 'workflow': 'E2E-1-C1: Deploy LC1S cluster with Data Protection'})
    workflows.append(
        {'id': 2, 'group': 'Basic Workflows', 'workflow': 'E2E-1-C2: Deploy CA1S cluster with Data Protection'})
    workflows.append(
        {'id': 3, 'group': 'Basic Workflows', 'workflow': 'E2E-1-C3: Deploy CA2S cluster with Data Protection'})
    workflows.append(
        {'id': 4, 'group': 'Basic Workflows', 'workflow': 'E2E-1-C4: Deploy DR2S cluster with Data Protection'})
    workflows.append(
        {'id': 5, 'group': 'Basic Workflows', 'workflow': 'E2E-1-C5: Deploy MP2S cluster with Data Protection'})
    workflows.append(
        {'id': 6, 'group': 'Basic Workflows', 'workflow': 'E2E-1-C6: Deploy MP3S cluster with Data Protection'})
    workflows.append(
        {'id': 7, 'group': 'Basic Workflows', 'workflow': 'E2E-1-C8: Deploy VS1S cluster with Data Protection'})
    workflows.append(
        {'id': 8, 'group': 'Basic Workflows', 'workflow': 'E2E-2-C1: Deploy LC1S cluster without Data Protection'})
    workflows.append(
        {'id': 9, 'group': 'Basic Workflows', 'workflow': 'E2E-2-C2: Deploy CA1S cluster without Data Protection'})
    workflows.append(
        {'id': 10, 'group': 'Basic Workflows', 'workflow': 'E2E-2-C3: Deploy CA2S cluster without Data Protection'})
    workflows.append(
        {'id': 11, 'group': 'Basic Workflows', 'workflow': 'E2E-2-C4: Deploy DR2S cluster without Data Protection'})
    workflows.append(
        {'id': 12, 'group': 'Basic Workflows', 'workflow': 'E2E-2-C5: Deploy MP2S cluster without Data Protection'})
    workflows.append(
        {'id': 13, 'group': 'Basic Workflows', 'workflow': 'E2E-2-C6: Deploy MP3S cluster without Data Protection'})
    workflows.append(
        {'id': 14, 'group': 'Basic Workflows', 'workflow': 'E2E-2-C8: Deploy VS1S cluster without Data Protection'})
    workflows.append(
        {'id': 15, 'group': 'Basic Workflows',
         'workflow': 'E2E-3-C1: Request and manage VM in LC1S cluster without Data Protection'})
    workflows.append(
        {'id': 16, 'group': 'Basic Workflows',
         'workflow': 'E2E-3-C2: Request and manage VM in CA1S cluster without Data Protection'})
    workflows.append(
        {'id': 17, 'group': 'Basic Workflows',
         'workflow': 'E2E-3-C3: Request and manage VM in CA2S cluster without Data Protection'})
    workflows.append(
        {'id': 18, 'group': 'Basic Workflows',
         'workflow': 'E2E-3-C4: Request and manage VM in DR2S cluster without Data Protection'})
    workflows.append(
        {'id': 19, 'group': 'Basic Workflows',
         'workflow': 'E2E-3-C5: Request and manage VM in MP2S cluster without Data Protection'})
    workflows.append(
        {'id': 20, 'group': 'Basic Workflows',
         'workflow': 'E2E-3-C6: Request and manage VM in MP3S cluster without Data Protection'})
    workflows.append(
        {'id': 21, 'group': 'Basic Workflows',
         'workflow': 'E2E-3-C8: Request and manage VM in VS1S cluster without Data Protection'})
    workflows.append(
        {'id': 22, 'group': 'Basic Workflows',
         'workflow': 'E2E-4-C1: Request and manage VM in LC1S cluster with Data Protection'})
    workflows.append(
        {'id': 23, 'group': 'Basic Workflows',
         'workflow': 'E2E-4-C2: Request and manage VM in CA1S cluster with Data Protection'})
    workflows.append(
        {'id': 24, 'group': 'Basic Workflows',
         'workflow': 'E2E-4-C3: Request and manage VM in CA2S cluster with Data Protection'})
    workflows.append(
        {'id': 25, 'group': 'Basic Workflows',
         'workflow': 'E2E-4-C4: Request and manage VM in DR2S cluster with Data Protection'})
    workflows.append(
        {'id': 26, 'group': 'Basic Workflows',
         'workflow': 'E2E-4-C5: Request and manage VM in MP2S cluster with Data Protection'})
    workflows.append(
        {'id': 27, 'group': 'Basic Workflows',
         'workflow': 'E2E-4-C6: Request and manage VM in MP3S cluster with Data Protection'})
    workflows.append(
        {'id': 28, 'group': 'Basic Workflows',
         'workflow': 'E2E-4-C8: Request and manage VM in VS1S cluster with Data Protection'})
    workflows.append(
        {'id': 30, 'group': 'Basic Workflows', 'workflow': 'E2E-7-C1: Maintain LC1S DP Features'})
    workflows.append(
        {'id': 31, 'group': 'Basic Workflows', 'workflow': 'E2E-7-C2: Maintain CA1S DP Features'})
    workflows.append(
        {'id': 32, 'group': 'Basic Workflows', 'workflow': 'E2E-7-C3: Maintain CA2S DP Features'})
    workflows.append(
        {'id': 33, 'group': 'Basic Workflows', 'workflow': 'E2E-7-C4: Maintain DR2S DP Features'})
    workflows.append(
        {'id': 34, 'group': 'Basic Workflows', 'workflow': 'E2E-7-C5: Maintain MP2S DP Features'})
    workflows.append(
        {'id': 35, 'group': 'Basic Workflows', 'workflow': 'E2E-7-C6: Maintain MP3S DP Features'})
    workflows.append(
        {'id': 36, 'group': 'Basic Workflows', 'workflow': 'E2E-7-C7: Maintain RP4VM DP Features'})
    workflows.append(
        {'id': 37, 'group': 'Basic Workflows', 'workflow': 'E2E-7-C8: Maintain VS1S DP Features'})
    workflows.append(
        {'id': 38, 'group': 'Failover Workflows',
         'workflow': 'E2E-8-C3-1-CA2S: Maintain CA2S Avamar grid failover/failback features'})
    workflows.append(
        {'id': 39, 'group': 'Failover Workflows',
         'workflow': 'E2E-8-C3-2-CA2S: Maintain CA2S Avamar failover/failback features after site failure'})
    workflows.append(
        {'id': 42, 'group': 'Migration Workflows', 'workflow': 'E2E-9-C4: Perform planned migration in DR2S'})
    workflows.append(
        {'id': 43, 'group': 'Migration Workflows', 'workflow': 'E2E-9-C5: Perform planned migration in MP2S'})
    workflows.append(
        {'id': 44, 'group': 'Migration Workflows', 'workflow': 'E2E-9-C6: Perform planned migration in MP3S'})
    workflows.append(
        {'id': 45, 'group': 'RP4VM Workflows',
         'workflow': 'E2E-101-C7: Initial RP4VM support in EHC without Data Protection'})
    workflows.append(
        {'id': 46, 'group': 'RP4VM Workflows',
         'workflow': 'E2E-102-C7: Initial RP4VM support in EHC with Data Protection'})
    workflows.append(
        {'id': 47, 'group': 'RP4VM Workflows',
         'workflow': 'E2E-101-C8: Initial RP4VM VSAN support in EHC without Data Protection'})

    return workflows

def sc_sub_workflows():
    sc_sub_workflows = []
    sc_sub_workflows.append(
        {'id': 48, 'group': 'Scenario Basic Verification Workflows',
         'workflow': 'E2ESN-1-DR2S: Deploy DR2S cluster with Data Protection'})
    sc_sub_workflows.append(
        {'id': 49, 'group': 'Scenario Basic Verification Workflows',
         'workflow': 'E2ESN-1-LC1S: Deploy LC1S cluster with Data Protection'})
    sc_sub_workflows.append(
        {'id': 50, 'group': 'Scenario Basic Verification Workflows',
         'workflow': 'E2ESN-1-RP4VM: Deploy RP4VM cluster with Data Protection'})
    sc_sub_workflows.append(
        {'id': 51, 'group': 'Scenario Basic Verification Workflows',
         'workflow': 'E2ESN-3-RP4VM: Basic LC1S And RP4VM Deployment with Data Protection'})
    sc_sub_workflows.append(
        {'id': 52, 'group': 'Scenario Basic Verification Workflows',
         'workflow': 'E2ESN-2/3-LC1S: Basic Provision Local Workloads to Existing LC1S And RP4VM with DP'})
    sc_sub_workflows.append(
        {'id': 53, 'group': 'Scenario Basic Verification Workflows',
         'workflow': 'E2ESN-4-Basic-DR2S: Basic DR2S with Data Protection'})
    sc_sub_workflows.append(
        {'id': 54, 'group': 'Scenario Basic Verification Workflows',
         'workflow': 'E2ESN-4-Extend-DR2S: Additional DR2S Clusters in Existing VC DR Pair with Data Protection'})
    sc_sub_workflows.append(
        {'id': 55, 'group': 'Scenario Basic Verification Workflows',
         'workflow': 'E2ESN-5-CA2S: Cloud Administrator Onboard CA2S Cluster For Scenario'})
    sc_sub_workflows.append(
        {'id': 56, 'group': 'Scenario Basic Verification Workflows',
         'workflow': 'E2ESN-5-CA1S: Cloud Administrator Onboard CA1S Cluster For Scenario'})
    sc_sub_workflows.append(
        {'id': 57, 'group': 'Scenario Basic Verification Workflows',
         'workflow': 'E2ESN-2-RP4VM: Vsan LC1S And RP4VM Deployment with Data Protection'})
    return sc_sub_workflows


def sc_workflows():
    sc_workflows = []
    sc_workflows.append(
        {'id': 101, 'group': 'scenario workflows', 'workflows inside': [48, 49, 50],
         'workflow': '1: Basic Verification 1 LC1S DR2S RP4VM'})
    sc_workflows.append(
        {'id': 105, 'group': 'scenario workflows', 'workflows inside': [57, 52],
         'workflow': '2: Basic Verification 2 LC1S RP4VM DP Local and Replicated Workloads'})
    sc_workflows.append(
        {'id': 102, 'group': 'scenario workflows', 'workflows inside': [51, 52],
         'workflow': '3: Basic Verification 3 LC1S RP4VM DP Local and Replicated Workloads'})
    sc_workflows.append(
        {'id': 103, 'group': 'scenario workflows', 'workflows inside': [53, 54],
         'workflow': '4: Basic Verification 4 SRM DR Bi Directional Workload Replication'})
    sc_workflows.append(
        {'id': 104, 'group': 'scenario workflows', 'workflows inside': [55, 56, 50],
         'workflow': '5: Basic Verification 5 CA1S CA2S LC1S RP4VM with Data Protection'})
    return sc_workflows


def run_workflow(wf_id, wf_group, wf_name):
    import subprocess
    cmd = ['python', './foo.py']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout = proc.communicate()[0]
    return stdout


def main():
    print all_workflows()


if __name__ == '__main__':
    main()
