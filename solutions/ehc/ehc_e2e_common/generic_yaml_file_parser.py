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

# pylint: disable=no-member, too-few-public-methods

from ehc_e2e.utils.context.datacontext import DataContext
import generic_yaml_file_attr as generic_attr
import os
import platform
from robot.api import logger


class GenericYamlFileParser(object):
    context = DataContext(None)
    GLOBAL_CONFIG_FILE = 'GC'

    @classmethod
    def parse_context(cls,):
        """
        Parse generic.yaml file to YAML data object.
        Args:
            ctx:

        Returns: None
        generic.yaml:
        launch_browser:
            browserType: *browser
            baseUrl: *baseUrl

        vra:
            tenant: *tenant
            business_group: *business_group

        vro:
            address: *vro_address
            username: *vro_username
            password: *vro_password

        user_roles:
            Config_Admin:
                username: *config_admin
                password: *config_admin_password
                domain: *config_admin_domain
            Backup_Admin:
                username: *backup_admin
                password: *backup_admin_password
                domain: *backup_admin_domain
            Storage_Admin:
                username: *storage_admin
                password: *storage_admin_password
                domain: *storage_admin_domain
            Tenant_BG_User:
                username: *tenant_bg_user
                password: *tenant_bg_user_password
                domain: *tenant_bg_user_domain

        vipr:
            address: *vipr_address
            username: *vipr_username
            password: *vipr_password

        """
        sys_attr = platform.system()
        if sys_attr == 'Windows':
            _cd = os.path.dirname(os.path.realpath(__file__))
            _parent_dir = os.path.abspath(os.path.join(_cd, os.pardir))
            global_file = os.path.join(_parent_dir, 'ehc_e2e/conf/generic.yaml')
            logger.info("Operate system is Windows, using {}".format(global_file))
        elif sys_attr == 'Linux':
            global_file = '/root/automation/ehc/config/generic.yaml'
            logger.info("Operate system is Linux, using {}".format(global_file))
        else:
            logger.error("Can not recognize the operate system.")
            global_file = None

        logger.info("Start to parse generic.yaml file.")
        ctx = DataContext(None)
        assert os.path.isfile(global_file), '"{}" is not provided.'.format(global_file)
        ctx.update_context(global_file, cls.GLOBAL_CONFIG_FILE)
        global_context = ctx.__getattribute__(cls.GLOBAL_CONFIG_FILE)

        #vra
        setattr(cls.context, generic_attr.VRA_HOST, global_context.launch_browser.baseUrl)
        setattr(cls.context, generic_attr.VRA_TENANT, global_context.vra.tenant)
        setattr(cls.context, generic_attr.VRA_BUSINESS_GROUP, global_context.vra.business_group)

        #vro
        setattr(cls.context, generic_attr.VRO_HOST, global_context.vro.address)
        setattr(cls.context, generic_attr.VRO_USERNAME, global_context.vro.username)
        setattr(cls.context, generic_attr.VRO_PASSWORD, global_context.vro.password)

        #config admin
        setattr(cls.context, generic_attr.CONFIG_ADMIN_USERNAME, global_context.user_roles.Config_Admin.username)
        setattr(cls.context, generic_attr.CONFIG_ADMIN_PASSWORD, global_context.user_roles.Config_Admin.password)
        setattr(cls.context, generic_attr.CONFIG_ADMIN_DOMAIN, global_context.user_roles.Config_Admin.domain)

        #backup admin
        setattr(cls.context, generic_attr.BACKUP_ADMIN_USERNAME, global_context.user_roles.Backup_Admin.domain)
        setattr(cls.context, generic_attr.BACKUP_ADMIN_PASSWORD, global_context.user_roles.Backup_Admin.password)
        setattr(cls.context, generic_attr.BACKUP_ADMIN_DOMAIN, global_context.user_roles.Backup_Admin.domain)

        # storage admin
        setattr(cls.context, generic_attr.STORAGE_ADMIN_USERNAME, global_context.user_roles.Storage_Admin.domain)
        setattr(cls.context, generic_attr.STORAGE_ADMIN_PASSWORD, global_context.user_roles.Storage_Admin.password)
        setattr(cls.context, generic_attr.STORAGE_ADMIN_DOMAIN, global_context.user_roles.Storage_Admin.domain)

        # tenant business group user
        setattr(cls.context, generic_attr.TENANT_BG_USERNAME, global_context.user_roles.Tenant_BG_User.domain)
        setattr(cls.context, generic_attr.TENANT_BG_PASSWORD, global_context.user_roles.Tenant_BG_User.password)
        setattr(cls.context, generic_attr.TENANT_BG_DOMAIN, global_context.user_roles.Tenant_BG_User.domain)

        # vipr
        setattr(cls.context, generic_attr.VIPR_HOST, global_context.vipr.address)
        setattr(cls.context, generic_attr.VIPR_USERNAME, global_context.vipr.username)
        setattr(cls.context, generic_attr.VIPR_PASSWORD, global_context.vipr.password)

        return cls.context

