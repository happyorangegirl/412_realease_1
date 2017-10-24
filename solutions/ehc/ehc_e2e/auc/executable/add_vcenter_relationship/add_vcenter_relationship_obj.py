class AddVcenterRelationObj(object):
    description = ""
    reasons = ""
    please_select_the_operation = ""
    protected_vcenter = ""
    protected_vcenter_username = ""
    Protected_vcenter_password = ""
    recovery_vcenter = ""
    recovery_vcenter_username = ""
    recovery_vcenter_password = ""
    nsx_available_for_this_setup = ""
    protected_site_nsx_endpoint_name = ""
    enter_protected_site_nsx_manager_fqdn = ""
    protected_site_nsx_manager_username = ""
    protected_site_nsx_manager_password = ""
    the_recovery_site_nsx_endpoint_name = ""
    enter_recovery_site_nsx_manager_fqdn = ""
    recovery_site_nsx_manager_username = ""
    recovery_site_nsx_manager_password = ""
    select_protected_srm_site = ""
    protected_srm_username_with_privileges_to_srm = ""
    srm_protected_password = ""
    select_recovery_srm_site = ""
    recovery_srm_username_with_privileges_to_srm = ""
    srm_recovery_password = ""
    protected_srm_sql_host_name = ""
    srm_protected_site_sql_database_host = ""
    protected_site_sql_database_port = ""
    protected_select_authentication_type = ""
    protected_site_sql_username = ""
    protected_site_sql_password = ""
    protected_site_sql_user_domain = ""
    protected_site_sql_database_name = ""
    recovery_srm_sql_host_name = ""
    srm_recovery_site_sql_database_host = ""
    recovery_site_sql_database_port = ""
    recovery_select_authentication_type = ""
    recovery_site_sql_username = ""
    recovery_site_sql_password = ""
    recovery_site_sql_user_domain = ""
    recovery_site_sql_database_name = ""
    protected_srm_soap_host_name = ""
    protected_srm_soap_host_fqdn = ""
    protected_srm_soap_username = ""
    protected_srm_soap_password = ""
    recovery_srm_soap_host_name = ""
    recovery_srm_soap_host_fqdn = ""
    recovery_srm_soap_username = ""
    recovery_srm_soap_password = ""
    action_chosen = ""
    primary_vcenter_selected = ""
    secondary_vcenter_selected = ""
    request = ""

    def __init__(self, add_vcenter_relationship=None, extend_rp4vm=False):
        if not add_vcenter_relationship:
            return
        error_message = 'yaml data of "{step}" value is None'
        assert add_vcenter_relationship.description is not None, \
            error_message.format(step='description')
        self.description = add_vcenter_relationship.description
        self.reasons = add_vcenter_relationship.reasons
        assert add_vcenter_relationship.please_select_the_operation is not None, \
            error_message.format(step='please_select_the_operation')
        self.please_select_the_operation = add_vcenter_relationship.please_select_the_operation

        if not extend_rp4vm:
            assert add_vcenter_relationship.protected_vcenter_information.protected_vcenter_username is not None,\
                error_message.format(step='protected_vcenter_username')
            self.protected_vcenter_username = add_vcenter_relationship.protected_vcenter_information.\
                protected_vcenter_username
            assert add_vcenter_relationship.protected_vcenter_information.protected_vcenter_password is not None,\
                error_message.format(step='protected_vcenter_password')
            self.protected_vcenter_password = add_vcenter_relationship.protected_vcenter_information.\
                protected_vcenter_password

            assert add_vcenter_relationship.recovery_vcenter_information.recovery_vcenter_username is not None,\
                error_message.format(step='recovery_vcenter_username')
            self.recovery_vcenter_username = add_vcenter_relationship.recovery_vcenter_information.\
                recovery_vcenter_username
            assert add_vcenter_relationship.recovery_vcenter_information.recovery_vcenter_password is not None,\
                error_message.format(step='recovery_vcenter_password')
            self.recovery_vcenter_password = add_vcenter_relationship.recovery_vcenter_information.\
                recovery_vcenter_password
            assert add_vcenter_relationship.nsx_available_for_this_setup is not None,\
                error_message.format(step='nsx_available_for_this_setup')
            self.nsx_available_for_this_setup = add_vcenter_relationship.nsx_available_for_this_setup

            assert add_vcenter_relationship\
                .protected_site_nsx_configurations.enter_protected_site_nsx_manager_fqdn is not None, \
                error_message.format(step='enter_protected_site_nsx_manager_fqdn')
            self.enter_protected_site_nsx_manager_fqdn = add_vcenter_relationship.protected_site_nsx_configurations.\
                enter_protected_site_nsx_manager_fqdn
            assert add_vcenter_relationship\
                .protected_site_nsx_configurations.protected_site_nsx_manager_username is not None,\
                error_message.format(step='protected_site_nsx_manager_username')
            self.protected_site_nsx_manager_username = add_vcenter_relationship.protected_site_nsx_configurations.\
                protected_site_nsx_manager_username
            assert add_vcenter_relationship\
                .protected_site_nsx_configurations.protected_site_nsx_manager_password is not None,\
                error_message.format(step='protected_site_nsx_manager_password')
            self.protected_site_nsx_manager_password = add_vcenter_relationship.protected_site_nsx_configurations.\
                protected_site_nsx_manager_password
            assert add_vcenter_relationship\
                .recovery_site_nsx_configurations.enter_recovery_site_nsx_manager_fqdn is not None,\
                error_message.format(step='enter_recovery_site_nsx_manager_fqdn')
            self.enter_recovery_site_nsx_manager_fqdn = add_vcenter_relationship.recovery_site_nsx_configurations.\
                enter_recovery_site_nsx_manager_fqdn
            assert add_vcenter_relationship\
                .recovery_site_nsx_configurations.recovery_site_nsx_manager_username is not None,\
                error_message.format(step='recovery_site_nsx_manager_username')
            self.recovery_site_nsx_manager_username = add_vcenter_relationship.recovery_site_nsx_configurations.\
                recovery_site_nsx_manager_username
            assert add_vcenter_relationship\
                .recovery_site_nsx_configurations.recovery_site_nsx_manager_password is not None,\
                error_message.format(step='recovery_site_nsx_manager_password')
            self.recovery_site_nsx_manager_password = add_vcenter_relationship.recovery_site_nsx_configurations.\
                recovery_site_nsx_manager_password

        assert add_vcenter_relationship.srm_plugin_protected_site.select_protected_srm_site is not None,\
            error_message.format(step='select_protected_srm_site')
        self.select_protected_srm_site = add_vcenter_relationship.srm_plugin_protected_site.select_protected_srm_site
        assert add_vcenter_relationship.srm_plugin_protected_site.\
            protected_srm_username_with_privileges_to_srm is not None,\
            error_message.format(step='protected_srm_username_with_privileges_to_srm')
        self.protected_srm_username_with_privileges_to_srm = add_vcenter_relationship.srm_plugin_protected_site.\
            protected_srm_username_with_privileges_to_srm
        assert add_vcenter_relationship.srm_plugin_protected_site.srm_protected_password is not None,\
            error_message.format(step='srm_protected_password')
        self.srm_protected_password = add_vcenter_relationship.srm_plugin_protected_site.srm_protected_password
        assert add_vcenter_relationship.srm_plugin_recovery_site.select_recovery_srm_site is not None,\
            error_message.format(step='select_recovery_srm_site')
        self.select_recovery_srm_site = add_vcenter_relationship.srm_plugin_recovery_site.select_recovery_srm_site
        assert add_vcenter_relationship.srm_plugin_recovery_site.\
            recovery_srm_username_with_privileges_to_srm is not None,\
            error_message.format(step='recovery_srm_username_with_privileges_to_srm')
        self.recovery_srm_username_with_privileges_to_srm = add_vcenter_relationship.srm_plugin_recovery_site.\
            recovery_srm_username_with_privileges_to_srm
        assert add_vcenter_relationship.srm_plugin_recovery_site.srm_recovery_password is not None,\
            error_message.format(step='srm_recovery_password')
        self.srm_recovery_password = add_vcenter_relationship.srm_plugin_recovery_site.srm_recovery_password

        assert add_vcenter_relationship.srm_sql_protected_site.srm_protected_site_sql_database_host is not None,\
            error_message.format(step='srm_protected_site_sql_database_host')
        self.srm_protected_site_sql_database_host = add_vcenter_relationship.srm_sql_protected_site.\
            srm_protected_site_sql_database_host
        assert add_vcenter_relationship.srm_sql_protected_site.protected_site_sql_database_port is not None,\
            error_message.format(step='protected_site_sql_database_port')
        self.protected_site_sql_database_port = add_vcenter_relationship.srm_sql_protected_site.\
            protected_site_sql_database_port
        assert add_vcenter_relationship.srm_sql_protected_site.protected_select_authentication_type is not None,\
            error_message.format(step='protected_select_authentication_type')
        self.protected_select_authentication_type = add_vcenter_relationship.srm_sql_protected_site.\
            protected_select_authentication_type
        assert add_vcenter_relationship.srm_sql_protected_site.protected_site_sql_username is not None,\
            error_message.format(step='protected_site_sql_username')
        self.protected_site_sql_username = add_vcenter_relationship.srm_sql_protected_site.protected_site_sql_username
        assert add_vcenter_relationship.srm_sql_protected_site.protected_site_sql_password is not None,\
            error_message.format(step='protected_site_sql_password')
        self.protected_site_sql_password = add_vcenter_relationship.srm_sql_protected_site.protected_site_sql_password
        if self.protected_select_authentication_type == "Domain":
            assert add_vcenter_relationship.srm_sql_protected_site.protected_site_sql_user_domain is not None,\
                error_message.format(step='protected_site_sql_user_domain')
            self.protected_site_sql_user_domain = add_vcenter_relationship.srm_sql_protected_site.\
                protected_site_sql_user_domain
        assert add_vcenter_relationship.srm_sql_protected_site.protected_site_sql_database_name is not None,\
            error_message.format(step='protected_site_sql_database_name')
        self.protected_site_sql_database_name = add_vcenter_relationship.srm_sql_protected_site.\
            protected_site_sql_database_name

        assert add_vcenter_relationship.srm_sql_recovery_site.srm_recovery_site_sql_database_host is not None,\
            error_message.format(step='srm_recovery_site_sql_database_host')
        self.srm_recovery_site_sql_database_host = add_vcenter_relationship.srm_sql_recovery_site.\
            srm_recovery_site_sql_database_host
        assert add_vcenter_relationship.srm_sql_recovery_site.recovery_site_sql_database_port is not None,\
            error_message.format(step='recovery_site_sql_database_port')
        self.recovery_site_sql_database_port = add_vcenter_relationship.srm_sql_recovery_site.\
            recovery_site_sql_database_port
        assert add_vcenter_relationship.srm_sql_recovery_site.recovery_select_authentication_type is not None,\
            error_message.format(step='recovery_select_authentication_type')
        self.recovery_select_authentication_type = add_vcenter_relationship.srm_sql_recovery_site.\
            recovery_select_authentication_type
        assert add_vcenter_relationship.srm_sql_recovery_site.recovery_site_sql_username is not None,\
            error_message.format(step='recovery_site_sql_username')
        self.recovery_site_sql_username = add_vcenter_relationship.srm_sql_recovery_site.recovery_site_sql_username
        assert add_vcenter_relationship.srm_sql_recovery_site.recovery_site_sql_password is not None,\
            error_message.format(step='recovery_site_sql_password')
        self.recovery_site_sql_password = add_vcenter_relationship.srm_sql_recovery_site.recovery_site_sql_password
        if self.recovery_select_authentication_type == 'Domain':
            assert add_vcenter_relationship.srm_sql_recovery_site.recovery_site_sql_user_domain is not None,\
                error_message.format(step='recovery_site_sql_user_domain')
            self.recovery_site_sql_user_domain \
                = add_vcenter_relationship.srm_sql_recovery_site.recovery_site_sql_user_domain
        assert add_vcenter_relationship.srm_sql_recovery_site.recovery_site_sql_database_name is not None,\
            error_message.format(step='recovery_site_sql_database_name')
        self.recovery_site_sql_database_name = add_vcenter_relationship.srm_sql_recovery_site.\
            recovery_site_sql_database_name
        assert add_vcenter_relationship.protected_srm.protected_srm_soap_host_fqdn is not None,\
            error_message.format(step='protected_srm_soap_host_fqdn')
        self.protected_srm_soap_host_fqdn = add_vcenter_relationship.protected_srm.protected_srm_soap_host_fqdn
        assert add_vcenter_relationship.protected_srm.protected_srm_soap_username is not None,\
            error_message.format(step='protected_srm_soap_username')
        self.protected_srm_soap_username = add_vcenter_relationship.protected_srm.protected_srm_soap_username
        assert add_vcenter_relationship.protected_srm.protected_srm_soap_password is not None,\
            error_message.format(step='protected_srm_soap_password')
        self.protected_srm_soap_password = add_vcenter_relationship.protected_srm.protected_srm_soap_password
        assert add_vcenter_relationship.recovery_srm.recovery_srm_soap_host_fqdn is not None,\
            error_message.format(step='recovery_srm_soap_host_fqdn')
        self.recovery_srm_soap_host_fqdn = add_vcenter_relationship.recovery_srm.recovery_srm_soap_host_fqdn
        assert add_vcenter_relationship.recovery_srm.recovery_srm_soap_username is not None,\
            error_message.format(step='recovery_srm_soap_username')
        self.recovery_srm_soap_username = add_vcenter_relationship.recovery_srm.recovery_srm_soap_username
        assert add_vcenter_relationship.recovery_srm.recovery_srm_soap_password is not None,\
            error_message.format(step='recovery_srm_soap_password')
        self.recovery_srm_soap_password = add_vcenter_relationship.recovery_srm.recovery_srm_soap_password
        self.request = ""
