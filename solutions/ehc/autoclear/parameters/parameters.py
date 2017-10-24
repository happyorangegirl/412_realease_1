# Internal use. Do not modify
PARAMETERS = {
    'cleanup_sequence': [
        'RP4VM Policy',
        'RP4VM vRPA Cluster',
        'Backup Service Level',
        'Datastore',
        'ARR',
        'ASR',
        'Avamar Grid',
        'Cluster',
        'vCenter Relationship',
        'HWI',
        'vCenter',
        'Site'
    ],

    'Site': {
        'vro_get_api': 'EHC.SiteFolder/Sites',
        'workflow_name': 'Site Maintenance',
        'delete_key': 'entityToDelete',
        'confirmation': 'Confirm',
        'currentAction': 'Delete Site',
        'reviewAction': 'test',
        'reviewSite': 'test'},

    'vCenter': {
        'vro_get_api': 'EHC.vCenterFolder/vCenters',
        'workflow_name': 'vCenter Endpoint Maintenance',
        'delete_key': 'vCenterToDelete',
        'confirmToDelete': 'Confirm',
        'vCenterAction': 'Delete vCenter',
        'reviewAction': 'test',
        'reviewvCenterSelected': 'test'
    },

    'HWI': {
        'vro_get_api': 'EHC.HardwareIslandFolder/HardwareIslands',
        'workflow_name': 'Hardware Island Maintenance',
        'delete_key': 'hardwareIslandToDelete',
        'confirmation': 'Confirm',
        'HIAction': 'Delete Hardware Island',
        'reviewAction': 'test',
        'reviewActionConfirmation': 'Confirm',
        'reviewHardwareIslandName': 'test'
    },

    'vCenter Relationship': {
        'vro_get_api': 'EHC.vCenterFolder/vCenters',
        'workflow_name': 'vCenter Relationship Maintenance',
        'protectedvCenterName1': 'test',
        'recoveryvCenterName1': 'test',
        'param1': 'ProtectedVCenterDTName',
        'param2': 'RecoveryVCenterDTName',
        'mainAction': 'Delete vCenter Relationship',
        'confirmation': 'Confirm',
        'confirmationReview': 'test'
    },

    'Cluster': {
        'vro_get_api': 'EHC.ClusterFolder/Clusters',
        'workflow_name': 'Cluster Maintenance',
        'delete_key': 'clusterToDelete',
        'deleteConfirmation': 'Confirm',
        'reviewCluster': 'test',
        'reviewAction': 'test',
        'mainAction': 'Delete Cluster'
    },

    'Datastore': {
        'vro_get_api': 'EHC.DatastoreFolder/Datastores',
        'workflow_name': 'Datastore Maintenance',
        'delete_key': 'selectedDatastore',
        'datastoreReview': 'test',
        'confirm': 'Confirm'
    },

    'Backup Service Level': {
        'vro_get_api': 'EHC.BackupServiceLevelFolder/BackupServiceLevels',
        'workflow_name': 'Backup Service Level Maintenance',
        'delete_key': 'SvcLevelToDelete',
        'ConfirmDelete': 'Confirm',
        'currentAction': 'Delete Backup Service Level',
        'reviewServiceLevelToDelete': 'test',
        'reviewAction': 'test'
    },

    'Avamar Grid': {
        'vro_get_api': 'EHC.AvamarGridFolder/AvamarGrids',
        'workflow_name': 'Avamar Grid Maintenance',
        'delete_key': 'delAvamarGrid',
        'delCon': 'Confirm',
        'operationType': 'Delete Avamar Grid',
        'reviewAction': 'test',
        'reviewGridName': 'test'
    },

    'ASR': {
        'vro_get_api': 'EHC.ASRFolder/ASRs',
        'workflow_name': 'Avamar Site Relationship (ASR) Maintenance',
        'delete_key': 'asrNameWithDetails2',
        'selectAction': 'Delete ASR',
        'reviewAction': 'test',
        'confirmDeleteASR': 'Confirm',
        'reviewConfirmASRDelete': 'Confirm'
    },

    'ARR': {
        'vro_get_api': 'EHC.ARRFolder/ARRs',
        'workflow_name': 'Avamar Replication Relationship (ARR) Maintenance',
        'delete_key': 'deleteARR',
        'operationType': 'Delete ARR',
        'deleteConfirmation': 'Confirm'
    },

    'RP4VM vRPA Cluster': {
        'vro_get_api': 'EHC.vRPAClusterFolder/vRPAClusters',
        'workflow_name': 'RP4VM vRPA Cluster Maintenance',
        'param1': 'primaryVrpaClusterToDelete',
        'param2': 'secondaryVrpaClusterToDelete',
        'mainAction': 'Delete vRPA Cluster Pair',
        'forceDelete': 'Yes',
        'deleteConfirmation': 'Confirm'
    },

    'RP4VM Policy': {
        'vro_get_api': 'EHC.RP4VMPolicyFolder/RP4VMPolicies',
        'workflow_name': 'RP4VM Policy Maintenance',
        'delete_key': 'policyNameToDelete',
        'deleteConfirmation': 'Confirm',
        'mainAction': 'Delete Policy'
    }

}
