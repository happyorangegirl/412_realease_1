import sys
from robot.api import logger
from .add_vcenter_relationship_obj import AddVcenterRelationObj
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.specific import AddVcenterRelationshipPage
from ehc_e2e.auc.uimap.shared import CatalogPage
from ehc_e2e.auc.uimap.shared import RequestsPage
from ehc_e2e.auc.uimap.shared import LoadingWindow


class AddVcenterRelationship(BaseUseCase):
    """
    Add Vcenter Relationship
    """
    def __init__(self, name=None, method_name='runTest', ctx_in=None, ctx_out=None, extend_rp4vm=False,
                 **kwargs):
        super(AddVcenterRelationship, self).__init__(name, method_name, ctx_in, ctx_out, **kwargs)
        self.auc_info = 'Extend RP4VM vCenter Relationship with SRMDR' if extend_rp4vm else 'Add vCenter Relationship'
        self.extend_rp4vm = extend_rp4vm

    def test_add_vcenter_relationship(self, add_vcenter_relationship_obj=None):
        self.catalog_page = CatalogPage()
        self.loading_window = LoadingWindow()
        self.assertTrue(self.catalog_page.navigate_to_catalog(self.current_browser),
                        msg='Running on step: "{0}" - FAILED, switch to catalog frame failed.'.format(self.auc_info))

        self.add_vcenter_relationship_page = AddVcenterRelationshipPage()
        self.add_vcenter_relationship_page.ehc_configure.click()
        self.catalog_page.btn_vcenter_relationship_request.click()

        logger.info('Request button clicked. Going to vCenter Relationship Maintenance page')

        _formatter = 'Running on step: ' + self.auc_info + ' - FAILED, {step}'
        try:
            self.assertTrue(
                self.add_vcenter_relationship_page.txt_description.exists(),
                msg=_formatter.format(step='Description textbox does not exist.')
            )
            self.add_vcenter_relationship_page.txt_description.set(
                add_vcenter_relationship_obj.description)
            logger.info('Typed description: {}.'.format(add_vcenter_relationship_obj.description), False, True)
            self.add_vcenter_relationship_page.txt_reasons.set(add_vcenter_relationship_obj.reasons)
            self.loading_window.wait_loading(self.current_browser, 30)
            self.add_vcenter_relationship_page.btn_next.click()
            logger.info('Clicked Next button.', False, True)

            logger.info('Request information filled out. Going to Action Choice tab', False, True)

            self.assertTrue(
                self.add_vcenter_relationship_page.lab_select_operation.exists(),
                msg=_formatter.format(step="Drop down list: Action does not exist.")
            )
            self.add_vcenter_relationship_page.btn_select_the_operation.click()
            logger.info('Clicked drop down list: Action.', False, True)
            parent_element = self.add_vcenter_relationship_page.select_parent_element

            if self.add_vcenter_relationship_page.click_drop_down_list(
                    parent_element, 'div', add_vcenter_relationship_obj.please_select_the_operation) is False:
                self.fail(msg='{} does not exist in drop down list.'
                          .format(add_vcenter_relationship_obj.please_select_the_operation))
            else:
                self.loading_window.wait_loading(self.current_browser, 30)
                self.assertTrue(self.add_vcenter_relationship_page.btn_next.exists(),
                                msg=_formatter.format(step='Next button does not exist after selected action.'))
                self.assertIsNotNone(self.add_vcenter_relationship_page.btn_next.current.
                                     location_once_scrolled_into_view,
                                     msg=_formatter.format(
                                         step='Can not scroll Next button into view'))
                self.add_vcenter_relationship_page.send_tab_key(self.add_vcenter_relationship_page.btn_next)
                self.add_vcenter_relationship_page.btn_next.click()
                logger.info('Clicked Next button. Going to vCenter Information tab', False, True)
                self.loading_window.wait_loading(self.current_browser, 30)
                self.assertTrue(
                    self.add_vcenter_relationship_page.protected_vcenter_title.exists(),
                    msg=_formatter.format(step='Navigate to Protected vCenter Information page')
                )
                self.add_vcenter_relationship_page.protected_vcenter.click()
                if self.add_vcenter_relationship_page.click_drop_down_list(
                        parent_element, 'div', add_vcenter_relationship_obj.protected_vcenter) is False:
                    self.fail(msg='{} does not exist.'.format(add_vcenter_relationship_obj.protected_vcenter))
                else:
                    if not self.extend_rp4vm:
                        self.loading_window.wait_loading(self.current_browser, 30)
                        self.add_vcenter_relationship_page.txt_protected_vcenter_username.set(
                            add_vcenter_relationship_obj.protected_vcenter_username)
                        self.add_vcenter_relationship_page.txt_protected_vcenter_password.set(
                            add_vcenter_relationship_obj.protected_vcenter_password)

                    self.assertTrue(
                        self.add_vcenter_relationship_page.recovery_vcenter.exists(),
                        msg=_formatter.format(step='Navigate to Recovery vCenter Information page')
                    )
                    self.add_vcenter_relationship_page.recovery_vcenter.click()
                    if self.add_vcenter_relationship_page.click_drop_down_list(
                            parent_element, 'div', add_vcenter_relationship_obj.recovery_vcenter) is False:
                        self.fail(msg="recovery vCenter does not exist")
                    else:
                        if not self.extend_rp4vm:
                            self.loading_window.wait_loading(self.current_browser, 30)
                            self.add_vcenter_relationship_page.txt_recovery_vcenter_username.set(
                                add_vcenter_relationship_obj.recovery_vcenter_username)
                            self.add_vcenter_relationship_page.txt_recovery_vcenter_password.set(
                                add_vcenter_relationship_obj.recovery_vcenter_password)
                        self.loading_window.wait_loading(self.current_browser, 30)
                        self.add_vcenter_relationship_page.btn_next.click()
                        if not self.extend_rp4vm:
                            logger.info('vCenter information filled out. Going to NSX Manager Host Configurations tab',
                                        False, True)
                            self.assertTrue(
                                self.add_vcenter_relationship_page.nsx_available_for_this_setup.exists(),
                                msg=_formatter.format(step='Failed to navigate to NSX Available page')
                            )
                            if add_vcenter_relationship_obj.nsx_available_for_this_setup:
                                self.add_vcenter_relationship_page.nsx_available_for_this_setup.click()
                                if self.add_vcenter_relationship_page.click_drop_down_list(
                                        parent_element, 'div', 'Yes') is False:
                                    self.fail(msg="nsx available for this setup does not exist")
                                else:
                                    self.loading_window.wait_loading(self.current_browser, 30)
                                    self.assertTrue(
                                        self.add_vcenter_relationship_page
                                        .txt_enter_protected_site_nsx_manager_fqdn.exists(),
                                        msg=_formatter.format(step='Failed to navigate to NSX Configurations page'))
                                    self.add_vcenter_relationship_page.txt_enter_protected_site_nsx_manager_fqdn.set(
                                        add_vcenter_relationship_obj.enter_protected_site_nsx_manager_fqdn)
                                    self.add_vcenter_relationship_page.txt_protected_site_nsx_manager_username.set(
                                        add_vcenter_relationship_obj.protected_site_nsx_manager_username)
                                    self.add_vcenter_relationship_page.txt_protected_site_nsx_manager_password.set(
                                        add_vcenter_relationship_obj.protected_site_nsx_manager_password)

                                    self.add_vcenter_relationship_page.txt_enter_recovery_site_nsx_manager_fqdn.set(
                                        add_vcenter_relationship_obj.enter_recovery_site_nsx_manager_fqdn)
                                    self.add_vcenter_relationship_page.txt_recovery_site_nsx_manager_username.set(
                                        add_vcenter_relationship_obj.recovery_site_nsx_manager_username)
                                    self.add_vcenter_relationship_page.txt_recovery_site_nsx_manager_password.set(
                                        add_vcenter_relationship_obj.recovery_site_nsx_manager_password)
                            self.loading_window.wait_loading(self.current_browser, 30)
                            self.add_vcenter_relationship_page.btn_next.click()
                            logger.info('NSX information filled out. Going to SRM Plugin Information tab', False, True)
                        # if not exists
                        self.assertTrue(
                            self.add_vcenter_relationship_page.select_protected_srm_site.exists(),
                            msg=_formatter.format(step='Navigate to srm plugin information page')
                        )
                        self.add_vcenter_relationship_page.select_protected_srm_site.click()
                        if self.add_vcenter_relationship_page.click_drop_down_list(
                                parent_element, 'div',
                                add_vcenter_relationship_obj.select_protected_srm_site.lower()) is False:
                            self.fail(msg="select protected srm site does not exist")
                        else:
                            self.add_vcenter_relationship_page.txt_protected_srm_username_with_privileges_to_srm.set(
                                add_vcenter_relationship_obj.protected_srm_username_with_privileges_to_srm)
                            self.add_vcenter_relationship_page.txt_protected_srm_password.set(
                                add_vcenter_relationship_obj.srm_protected_password)
                            self.add_vcenter_relationship_page.select_recovery_srm_site.click()
                            if self.add_vcenter_relationship_page.click_drop_down_list(
                                    parent_element, 'div',
                                    add_vcenter_relationship_obj.select_recovery_srm_site.lower()) is False:
                                self.fail(msg="select recovery srm site does not exist")
                            else:
                                self.add_vcenter_relationship_page.txt_recovery_srm_username_with_privileges_to_srm.set(
                                    add_vcenter_relationship_obj.recovery_srm_username_with_privileges_to_srm)
                                self.add_vcenter_relationship_page.txt_srm_recovery_password.set(
                                    add_vcenter_relationship_obj.srm_recovery_password)
                                self.add_vcenter_relationship_page.btn_next.click()
                                logger.info('SRM Plugin Information filled out. Going to SRM SQL Server '
                                            'Information tab', False, True)
                                # srm sql information
                                self.assertTrue(self.add_vcenter_relationship_page.
                                                txt_srm_protected_site_sql_database_host.exists(),
                                                msg=_formatter
                                                .format(step='Failed to navigate to srm sql site information page'))
                                self.add_vcenter_relationship_page.txt_srm_protected_site_sql_database_host.set(
                                    add_vcenter_relationship_obj.srm_protected_site_sql_database_host)
                                self.add_vcenter_relationship_page.txt_protected_site_sql_database_port.set(
                                    add_vcenter_relationship_obj.protected_site_sql_database_port)
                                self.add_vcenter_relationship_page.protected_select_authentication_type.click()
                                if self.add_vcenter_relationship_page.click_drop_down_list(
                                        parent_element, 'div',
                                        add_vcenter_relationship_obj.protected_select_authentication_type) is False:
                                    self.fail(msg="protected select authentication type does not exist")
                                else:
                                    self.loading_window.wait_loading(self.current_browser, 30)
                                    self.add_vcenter_relationship_page.txt_protected_site_sql_username.set(
                                        add_vcenter_relationship_obj.protected_site_sql_username)
                                    self.add_vcenter_relationship_page.txt_protected_site_sql_password.set(
                                        add_vcenter_relationship_obj.protected_site_sql_password)
                                    if add_vcenter_relationship_obj.protected_select_authentication_type == 'Domain':
                                        self.add_vcenter_relationship_page.txt_protected_site_sql_user_domain.set(
                                            add_vcenter_relationship_obj.protected_site_sql_user_domain)
                                    self.add_vcenter_relationship_page.txt_protected_site_sql_database_name.set(
                                        add_vcenter_relationship_obj.protected_site_sql_database_name)

                                    self.add_vcenter_relationship_page.txt_srm_recovery_site_sql_database_host.set(
                                        add_vcenter_relationship_obj.srm_recovery_site_sql_database_host)
                                    self.add_vcenter_relationship_page.txt_recovery_site_sql_database_port.set(
                                        add_vcenter_relationship_obj.recovery_site_sql_database_port)
                                    self.add_vcenter_relationship_page.recovery_select_authentication_type.click()
                                    if self.add_vcenter_relationship_page.click_drop_down_list(
                                            parent_element, 'div',
                                            add_vcenter_relationship_obj.recovery_select_authentication_type) is False:
                                        self.fail(msg="recovery select authentication type does not exist")
                                    else:
                                        self.loading_window.wait_loading(self.current_browser, 30)
                                        self.add_vcenter_relationship_page.txt_recovery_site_sql_username.set(
                                            add_vcenter_relationship_obj.recovery_site_sql_username)
                                        self.add_vcenter_relationship_page.txt_recovery_site_sql_Password.set(
                                            add_vcenter_relationship_obj.recovery_site_sql_password)
                                        if add_vcenter_relationship_obj.\
                                                protected_select_authentication_type == 'Domain':
                                            self.add_vcenter_relationship_page.txt_recovery_site_sql_user_domain.set(
                                                add_vcenter_relationship_obj.recovery_site_sql_user_domain)
                                        self.add_vcenter_relationship_page.txt_recovery_site_sql_database_name.set(
                                            add_vcenter_relationship_obj.recovery_site_sql_database_name)
                                        self.loading_window.wait_loading(self.current_browser, 30)
                                        self.add_vcenter_relationship_page.btn_next.click()
                                        logger.info('SRM SQL Server Information filled out. Going to '
                                                    'SRM SOAP Information tab', False, True)
                                        # srm soap information
                                        self.assertTrue(
                                            self.add_vcenter_relationship_page.txt_protected_srm_soap_host_fqdn
                                            .exists(),
                                            msg=_formatter
                                            .format(step='Failed to navigate to srm soap information page'))

                                        self.add_vcenter_relationship_page.txt_protected_srm_soap_host_fqdn.set(
                                            add_vcenter_relationship_obj.protected_srm_soap_host_fqdn)
                                        self.add_vcenter_relationship_page.txt_protected_srm_soap_username.set(
                                            add_vcenter_relationship_obj.protected_srm_soap_username)
                                        self.add_vcenter_relationship_page.txt_protected_srm_soap_password.set(
                                            add_vcenter_relationship_obj.protected_srm_soap_password)
                                        self.add_vcenter_relationship_page.txt_recovery_srm_soap_host_fqdn.set(
                                            add_vcenter_relationship_obj.recovery_srm_soap_host_fqdn)
                                        self.add_vcenter_relationship_page.txt_recovery_srm_soap_username.set(
                                            add_vcenter_relationship_obj.recovery_srm_soap_username)
                                        self.add_vcenter_relationship_page.txt_recovery_srm_soap_password.set(
                                            add_vcenter_relationship_obj.recovery_srm_soap_password)
                                        self.loading_window.wait_loading(self.current_browser, 30)
                                        self.add_vcenter_relationship_page.btn_next.click()
                                        self.loading_window.wait_loading(self.current_browser, 30)
                                        logger.info('SRM SOAP Information filled out. Going to Review and Submit tab',
                                                    False, True)

                                        self.assertTrue(
                                            self.add_vcenter_relationship_page.btn_submit.exists(),
                                            msg=_formatter.format(step='Failed to navigate to review and submit page')
                                        )
                                        self.add_vcenter_relationship_page.btn_submit.click()
                                        self.loading_window.wait_loading(self.current_browser, 30)

        except AssertionError:
            self.add_vcenter_relationship_page.save_request()
            raise
        except Exception:
            self.add_vcenter_relationship_page.save_request()
            self.fail(msg=_formatter.format(step='more error info: {}'.format(sys.exc_info()[:2])))

        self.assertTrue(
            self.add_vcenter_relationship_page.lab_confirmation_success.exists(),
            msg='Running on step: "{0}" - FAILED,'
                'after clicking submit button, cannot find the label: '
                'The request has been submitted successfully.'.format(self.auc_info))
        self.add_vcenter_relationship_page.btn_ok.click()
        logger.info('Request has been submitted successfully', False, True)
        # switch to request
        self.assertTrue(RequestsPage().navigate_to_request(self.current_browser),
                        msg='Running on step: "{0}" - FAILED, '
                            'switch to request frame failed.'.format(self.auc_info))

        # check the request
        self.request_result = RequestsPage().get_request_result(
            add_vcenter_relationship_obj.description)
        self.assertIsNotNone(self.request_result,
                             msg='Running on step: "{0}" - FAILED, '
                                 'failed to get the request result.'.format(self.auc_info))

    def runTest(self):
        self.test_add_vcenter_relationship(self.vcenter_relationship_obj)

    def _validate_context(self):
        if self.ctx_in:
            self.request_result = None
            self.current_browser = self.ctx_in.shared.current_browser
            assert self.current_browser is not None, 'current_browser in yaml is None, ' \
                                                     'may be there is no active browser'
            self.assertTrue(self.current_browser.is_login,
                            msg='Please login to vRA, The flag value is_login is: False.')

            if self.extend_rp4vm:
                self.extend_vcenter_relationship = self.ctx_in.extend_vcenter_relationship
                self.extend_vcenter_relationship_obj = AddVcenterRelationObj(self.extend_vcenter_relationship,
                                                                             self.extend_rp4vm)
                assert self.extend_vcenter_relationship.protected_vcenter_name is not None, \
                    'extend_vcenter_relationship.protected_vcenter_name does not exist in YAML'
                assert self.extend_vcenter_relationship.recovery_vcenter_name is not None, \
                    'extend_vcenter_relationship.recovery_vcenter_name does not exist in YAML'
                self.extend_vcenter_relationship_obj.protected_vcenter = \
                    self.extend_vcenter_relationship.protected_vcenter_name
                self.extend_vcenter_relationship_obj.recovery_vcenter = \
                    self.extend_vcenter_relationship.recovery_vcenter_name
                self.vcenter_relationship_obj = self.extend_vcenter_relationship_obj

            else:
                self.add_vcenter_relationships = self.ctx_in.add_vcenter_relationship
                self.add_vcenter_relationship_obj = AddVcenterRelationObj(self.add_vcenter_relationships)
                if self.ctx_in.added_vcenter is not None:
                    self.assertTrue(len(self.ctx_in.added_vcenter) > 1, msg="please provide two vcenter")
                    self.add_vcenter_relationship_obj.protected_vcenter = self.ctx_in.added_vcenter[0]
                    self.add_vcenter_relationship_obj.recovery_vcenter = self.ctx_in.added_vcenter[1]
                else:
                    assert self.ctx_in.add_vcenter_relationship.\
                        protected_vcenter_information.protected_vcenter is not None, \
                        "yaml data of protected_vcenter does not exist"
                    assert self.ctx_in.add_vcenter_relationship.recovery_vcenter_information.recovery_vcenter \
                        is not None, \
                        "yaml data of recovery_vcenter does not exist"
                    self.add_vcenter_relationship_obj.protected_vcenter = \
                        self.ctx_in.add_vcenter_relationship.protected_vcenter_information.protected_vcenter
                    self.add_vcenter_relationship_obj.recovery_vcenter = \
                        self.ctx_in.add_vcenter_relationship.recovery_vcenter_information.recovery_vcenter
                self.vcenter_relationship_obj = self.add_vcenter_relationship_obj

    def _finalize_context(self):
        if not isinstance(getattr(self.ctx_out, 'added_vcenter_relationship', None), list):
            setattr(self.ctx_out, 'added_vcenter_relationship', [])
        if self.request_result is not None:
            self.assertTrue(self.request_result.status == 'Successful',
                            'the request status is: {status}, the status details is: {status_details}'.format(
                                name=self.request_result.description,
                                status=self.request_result.status,
                                status_details=self.request_result.status_details))
            getattr(self.ctx_out, 'added_vcenter_relationship').append(self.vcenter_relationship_obj)
        else:
            logger.error(msg='Running on step: "{0}" - FAILED. Failed to get the request result.'.format(self.auc_info))
