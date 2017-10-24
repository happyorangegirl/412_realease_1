#  Copyright 2016 EMC GSE SW Automation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from robot.api import logger


class Context_Onboard_Local_Cluster(object):
    def __init__(self):
        self.act_to_perform = 'Onboard Local Cluster'
        self.select_a_hwi = ''
        self.unprepared_cluster = ''
        self.onboard_local_cluster_entity = None

    def get_entity(self, action, added_hwi):
        onboard_local_cluster = action
        self.unprepared_cluster = onboard_local_cluster.select_unprepared_cluster
        assert self.unprepared_cluster is not None, \
            'No select_unprepared_cluster info  when you onboard local cluster'

        if onboard_local_cluster.select_a_hardware_island is not None:
            self.select_a_hwi = onboard_local_cluster.select_a_hardware_island
        elif len(added_hwi) >= 1:
            if len(added_hwi) > 1:
                logger.warn(msg='Only need one hardware island, you provide {0} hardware island info, '
                                'default use the first hardware island: {1}.'.format(str(len(added_hwi)), added_hwi[0]))
            self.select_a_hwi = added_hwi[0]
        else:
            assert False, 'Please provide hardware island in YAML item onboard_local_cluster,' \
                          'or add one hardware island.'

        self.onboard_local_cluster_entity = Onobard_Local_Cluster_Entity(self.act_to_perform,
                                                                         self.select_a_hwi,
                                                                         self.unprepared_cluster)
        return self.onboard_local_cluster_entity


class Onobard_Local_Cluster_Entity(object):
    cluster_action_to_perform = ''
    select_a_hwi = ''
    unprepared_cluster = ''

    def __init__(self, action_to_perform, select_a_hwi, unprepared_cluster):
        self.cluster_action_to_perform = action_to_perform
        self.select_a_hwi = select_a_hwi
        self.unprepared_cluster = unprepared_cluster


class Context_Onboard_Vsan_Cluster(object):
    def __init__(self):
        self.act_to_perform = 'Onboard VSAN Cluster'
        self.select_a_hwi = ''
        self.unprepared_cluster = ''
        self.onboard_vsan_cluster_entity = None

    def get_entity(self, action, added_hwi):
        onboard_vsan_cluster = action
        self.unprepared_cluster = onboard_vsan_cluster.select_unprepared_cluster
        assert self.unprepared_cluster is not None, \
            'No select_unprepared_cluster info when you onboard vsan cluster'

        if onboard_vsan_cluster.select_a_hardware_island is not None:
            self.select_a_hwi = onboard_vsan_cluster.select_a_hardware_island
        elif len(added_hwi) >= 1:
            if len(added_hwi) > 1:
                logger.warn(msg='Only need one hardware island, you provide {0} hardware island info, '
                                'default use the first hardware island: {1}.'.format(str(len(added_hwi)), added_hwi[0]))
            self.select_a_hwi = added_hwi[0]
        else:
            assert False, 'Please provide hardware island in YAML item onboard_vsan_cluster,' \
                          'or add one hardware island.'

        self.onboard_vsan_cluster_entity = Onobard_Vsan_Cluster_Entity(
            self.act_to_perform, self.select_a_hwi, self.unprepared_cluster)
        return self.onboard_vsan_cluster_entity


class Onobard_Vsan_Cluster_Entity(object):
    cluster_action_to_perform = ''
    select_a_hwi = ''
    unprepared_cluster = ''

    def __init__(self, action_to_perform, select_a_hwi, unprepared_cluster):
        self.cluster_action_to_perform = action_to_perform
        self.select_a_hwi = select_a_hwi
        self.unprepared_cluster = unprepared_cluster


class Context_Onboard_CA_Cluster(object):

    def __init__(self):
        self.cluster_action_to_perform = 'Onboard CA Cluster'
        self.select_hwi_1 = ''
        self.unprepared_cluster = ''
        self.choose_inter_site_vs_intra_site = ''
        self.select_hwi_2 = ''
        self.hosts_for_hwi_1 = ''
        self.hosts_for_hwi_2 = ''
        self.onboard_ca_cluster_entity = None

    def get_entity(self, action, added_hwi):
        onboard_ca_cluster = action
        self.select_unprepared_cluster = onboard_ca_cluster.select_unprepared_cluster
        self.choose_inter_site_vs_intra_site = onboard_ca_cluster.choose_inter_site_vs_intra_site

        assert self.select_unprepared_cluster is not None, \
            'No select_unprepared_cluster info when you onboard ca cluster'
        assert self.choose_inter_site_vs_intra_site is not None, \
            'No choose_inter_site_vs_intra_site info when you onboard ca cluster'
        logger.info('The informations of onboard_ca_cluster in YAML file are all provided.')

        if onboard_ca_cluster.select_hardward_island_1 is not None and \
                        onboard_ca_cluster.select_hardward_island_2 is not None:
            self.select_hwi_1 = onboard_ca_cluster.select_hardward_island_1
            self.select_hwi_2 = onboard_ca_cluster.select_hardward_island_2
        elif len(added_hwi) >= 2:
            if len(added_hwi) > 2:
                logger.warn(msg='Only need two hardware island, you provide {0} hardware island info, '
                                'default use the first hardware island as Select Hardware Island 1: {1},'
                                'use the second hardware island as Select Hardware Island 2:: {2}.'.format(
                                    str(len(added_hwi)), added_hwi[0], added_hwi[1]))
            self.select_hwi_1 = added_hwi[0]
            self.select_hwi_2 = added_hwi[1]
        else:
            assert False, 'Please provide select_hardward_island_1, ' \
                          'select_hardward_island_2 in YAML item onboard_ca_cluster,' \
                          'or add two hardware island.'

        if onboard_ca_cluster.select_hosts_for_hardware_island_1 is not None \
                and onboard_ca_cluster.select_hosts_for_hardware_island_2 is not None:
            self.hosts_for_hwi_1 = onboard_ca_cluster.select_hosts_for_hardware_island_1
            self.hosts_for_hwi_2 = onboard_ca_cluster.select_hosts_for_hardware_island_2
        else:
            self.hosts_for_hwi_1 = ''
            self.hosts_for_hwi_2 = ''
        self.onboard_ca_cluster_entity = Onobard_CA_Cluster_Entity(self.cluster_action_to_perform,
                                                                   self.select_hwi_1,
                                                                   self.select_unprepared_cluster,
                                                                   self.choose_inter_site_vs_intra_site,
                                                                   self.select_hwi_2,
                                                                   self.hosts_for_hwi_1,
                                                                   self.hosts_for_hwi_2)
        return self.onboard_ca_cluster_entity


class Onobard_CA_Cluster_Entity(object):
    cluster_action_to_perform = ''
    select_hwi_1 = ''
    unprepared_cluster = ''
    choose_inter_site_vs_intra_site = ''
    select_hwi_2 = ''
    hosts_for_hwi_1 = ''
    hosts_for_hwi_2 = ''

    def __init__(self, action_to_perform, select_hwi_1, unprepared_cluster,
                 choose_inter_site_vs_intra_site, select_hwi_2, hosts_for_hwi_1, hosts_for_hwi_2):
        self.cluster_action_to_perform = action_to_perform
        self.select_hwi_1 = select_hwi_1
        self.unprepared_cluster = unprepared_cluster
        self.choose_inter_site_vs_intra_site = choose_inter_site_vs_intra_site
        self.select_hwi_2 = select_hwi_2
        self.hosts_for_hwi_1 = hosts_for_hwi_1
        self.hosts_for_hwi_2 = hosts_for_hwi_2


class Context_Onboard_DR_Cluster(object):
    def __init__(self):
        self.act_to_perform = 'Onboard DR Cluster'
        # onboard dr cluster
        self.hwi_for_protected_cluster = ''
        self.hwi_for_recovery_cluster = ''
        self.unprepared_protected_cluster = ''
        self.unprepared_recovery_cluster = ''
        self.onboard_dr_cluster_entity = None

    def get_entity(self, action, added_hwi):
        onboard_dr_cluster = action
        self.unprepared_protected_cluster = onboard_dr_cluster.select_unprepared_protected_cluster
        self.unprepared_recovery_cluster = onboard_dr_cluster.select_unprepared_recovery_cluster

        assert self.unprepared_protected_cluster is not None, \
            'No select_unprepared_protected_cluster info  when you onboard dr cluster'
        assert self.unprepared_recovery_cluster is not None, \
            'No select_unprepared_recovery_cluster info  when you onboard dr cluster'
        logger.info('The informations of onboard_dr_cluster in YAML file are all provided.')

        if onboard_dr_cluster.select_a_hwi_for_the_protected_cluster is not None \
                and onboard_dr_cluster.select_a_hwi_for_the_recovery_cluster is not None:
            self.hwi_for_protected_cluster = onboard_dr_cluster.select_a_hwi_for_the_protected_cluster
            self.hwi_for_recovery_cluster = onboard_dr_cluster.select_a_hwi_for_the_recovery_cluster
        elif len(added_hwi) >= 2:
            if len(added_hwi) > 2:
                logger.warn(msg='Only need two hardware island, you provide {0} hardware island info, '
                                'default use the first hardware island for protected cluster: {1},'
                                'use the second hardware island for recovery cluster: {2}.'.format(
                                    str(len(added_hwi)), added_hwi[0], added_hwi[1]))
            self.hwi_for_protected_cluster = added_hwi[0]
            self.hwi_for_recovery_cluster = added_hwi[1]
        else:
            assert False, 'Please provide hardware island for protected cluster, ' \
                          'hardware island for recovery cluster in YAML item onboard_dr_cluster,' \
                          'or add two hardware island.'

        self.onboard_dr_cluster_entity = Onobard_DR_Cluster_Entity(self.act_to_perform,
                                                                   self.hwi_for_protected_cluster,
                                                                   self.unprepared_protected_cluster,
                                                                   self.hwi_for_recovery_cluster,
                                                                   self.unprepared_recovery_cluster)
        return self.onboard_dr_cluster_entity


class Onobard_DR_Cluster_Entity(object):
    cluster_action_to_perform = ''
    hwi_for_protected_cluster = ''
    unprepared_protected_cluster = ''
    hwi_for_recovery_cluster = ''
    unprepared_recovery_cluster = ''

    def __init__(self, action_to_perform, hwi_for_protected_cluster, unprepared_protected_cluster,
                 hwi_for_recovery_cluster, unprepared_recovery_cluster):
        self.cluster_action_to_perform = action_to_perform
        self.hwi_for_protected_cluster = hwi_for_protected_cluster
        self.unprepared_protected_cluster = unprepared_protected_cluster
        self.hwi_for_recovery_cluster = hwi_for_recovery_cluster
        self.unprepared_recovery_cluster = unprepared_recovery_cluster


class Context_Onboard_MP_Cluster(object):
    def __init__(self):
        self.act_to_perform = 'Onboard MP Cluster'
        self.select_hwi_1 = ''
        self.choose_inter_site_vs_intra_site = ''
        self.select_hwi_2 = ''
        self.unprepared_protected_cluster = ''
        self.hosts_for_hwi_1 = ''
        self.hosts_for_hwi_2 = ''
        self.select_hwi_3 = ''
        self.unprepared_recovery_cluster = ''
        self.onboard_mp_cluster_entity = None

    def get_entity(self, action, added_hwi):
        onboard_mp_cluster = action
        self.choose_inter_site_vs_intra_site = onboard_mp_cluster.choose_inter_site_vs_intra_site_protected_cluster
        self.unprepared_protected_cluster = onboard_mp_cluster.select_unprepared_protected_cluster
        self.unprepared_recovery_cluster = onboard_mp_cluster.select_unprepared_recovery_cluster

        assert self.choose_inter_site_vs_intra_site is not None, \
            'Please Choose Inter-site vs Intra-site protected cluster when onboard mp cluster'
        assert self.unprepared_protected_cluster is not None, \
            'No select_unprepared_protected_cluster info when you onboard mp cluster'
        assert self.unprepared_recovery_cluster is not None, \
            'No select_unprepared_recovery_cluster info when you onboard mp cluster'
        logger.info('The informations of onboard_mp_cluster in YAML file are all provided.')

        if onboard_mp_cluster.select_hardward_island_1 is not None \
                and onboard_mp_cluster.select_hardward_island_2 is not None \
                and onboard_mp_cluster.select_hardward_island_3 is not None:
            self.select_hwi_1 = onboard_mp_cluster.select_hardward_island_1
            self.select_hwi_2 = onboard_mp_cluster.select_hardward_island_2
            self.select_hwi_3 = onboard_mp_cluster.select_hardward_island_3
        elif len(added_hwi) >= 3:
            if len(added_hwi) > 3:
                logger.warn(msg='Only need three hardware island, you provide {0} hardware island info, '
                                'default use the first as Hardware Island 1: {1},'
                                'use the second as Hardware Island 2: {2},'
                                'use the third as Hardware Island 3:{3}.'.format(
                                    str(len(added_hwi)), added_hwi[0], added_hwi[1], added_hwi[2]))
            self.select_hwi_1 = added_hwi[0]
            self.select_hwi_2 = added_hwi[1]
            self.select_hwi_3 = added_hwi[2]
        else:
            assert False, 'Please provide Hardware Island 1, Hardware Island 2, ' \
                          'Hardware Island 3 in YAML item onboard_mp_cluster,' \
                          'or add three hardware island.'

        if onboard_mp_cluster.select_hosts_from_cluster_that_are_from_hardware_island_1 is not None and \
                        onboard_mp_cluster.select_hosts_from_cluster_that_are_from_hardware_island_2 is not None:
            self.hosts_for_hwi_1 = onboard_mp_cluster.select_hosts_from_cluster_that_are_from_hardware_island_1
            self.hosts_for_hwi_2 = onboard_mp_cluster.select_hosts_from_cluster_that_are_from_hardware_island_2
        else:
            self.hosts_for_hwi_1 = ''
            self.hosts_for_hwi_2 = ''
        self.onboard_mp_cluster_entity = Onobard_MP_Cluster_Entity(self.act_to_perform,
                                                                   self.select_hwi_1,
                                                                   self.choose_inter_site_vs_intra_site,
                                                                   self.select_hwi_2,
                                                                   self.unprepared_protected_cluster,
                                                                   self.hosts_for_hwi_1,
                                                                   self.hosts_for_hwi_2,
                                                                   self.select_hwi_3,
                                                                   self.unprepared_recovery_cluster)

        return self.onboard_mp_cluster_entity


class Onobard_MP_Cluster_Entity(object):
    cluster_action_to_perform = ''
    select_hwi_1 = ''
    choose_inter_site_vs_intra_site = ''
    select_hwi_2 = ''
    unprepared_protected_cluster = ''
    hosts_for_hwi_1 = ''
    hosts_for_hwi_2 = ''
    select_hwi_3 = ''
    unprepared_recovery_cluster = ''

    def __init__(self, action_to_perform, select_hwi_1, choose_inter_site_vs_intra_site,
                 select_hwi_2, unprepared_protected_cluster, hosts_for_hwi_1, hosts_for_hwi_2,
                 select_hwi_3, unprepared_recovery_cluster):
        self.cluster_action_to_perform = action_to_perform
        self.select_hwi_1 = select_hwi_1
        self.choose_inter_site_vs_intra_site = choose_inter_site_vs_intra_site
        self.select_hwi_2 = select_hwi_2
        self.unprepared_protected_cluster = unprepared_protected_cluster
        self.hosts_for_hwi_1 = hosts_for_hwi_1
        self.hosts_for_hwi_2 = hosts_for_hwi_2
        self.select_hwi_3 = select_hwi_3
        self.unprepared_recovery_cluster = unprepared_recovery_cluster
