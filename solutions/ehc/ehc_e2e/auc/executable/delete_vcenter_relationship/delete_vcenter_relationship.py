from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.specific import DeleteVcenterRelationshipPage
from ehc_e2e.auc.uimap.shared import CatalogPage
from ehc_e2e.auc.uimap.shared import RequestsPage
from ehc_e2e.auc.uimap.shared import LoadingWindow
from robot.api import logger
import sys


class DeleteVcenterRelationship(BaseUseCase):
    """
    Delete Vcenter Relationship
    """
    step_failed_msg = 'Running on step: "Delete Vcenter Relationship"-FAILED'
    delete_failed_flag = False

    def test_delete_vcenter_relationship(self):
        self.catalog_page = CatalogPage()
        self.loading_window = LoadingWindow()
        self.assertTrue(self.catalog_page.navigate_to_catalog(self.current_browser),
                        msg='Running on step:"Delete Vcenter Relationship"-FAILED, '
                            'switch to catalog frame failed.')
        self.delete_vcenter_relationship_page = DeleteVcenterRelationshipPage()
        self.delete_vcenter_relationship_page.ehc_configure.click()
        self.catalog_page.btn_vcenter_relationship_request.click()

        logger.info('Request button clicked. Going to vCenter Relationship Maintenance page', False, True)

        _formatter = 'Running on step: "{step}" - FAILED'
        try:
            self.assertTrue(
                self.delete_vcenter_relationship_page.txt_description.exists(),
                msg=_formatter.format(step='Navigate to vCenter Relationship Maintenance Request page')
            )
            self.delete_vcenter_relationship_page.txt_description.set(
                self.description)
            self.delete_vcenter_relationship_page.txt_reasons.set(self.description)
            self.loading_window.wait_loading(self.current_browser, 30)
            self.delete_vcenter_relationship_page.btn_next.click()

            logger.info('Request information filled out. Going to Action Choice tab', False, True)

            self.assertTrue(
                self.delete_vcenter_relationship_page.btn_select_the_operation.exists(),
                msg=_formatter.format(step='Navigate to Please select the action page')
            )
            self.delete_vcenter_relationship_page.btn_select_the_operation.click()
            parent_element = self.delete_vcenter_relationship_page.select_parent_element
            if self.delete_vcenter_relationship_page.click_drop_down_list(
                    parent_element, 'div',
                    self.action) is False:
                logger.error("please_select_the_operation is not exist")
                self.delete_vcenter_relationship_page.btn_cancel.click()
                self.fail(msg="please_select_the_operation is not exist")
            else:
                self.loading_window.wait_loading(self.current_browser, 30)
                self.delete_vcenter_relationship_page.btn_next.click()
                logger.info('Action selected. Going to vCenter Information tab', False, True)
                self.assertTrue(
                    self.delete_vcenter_relationship_page.lab_protected_vcenter_name.exists(),
                    msg=_formatter.format(step='Navigate to Paired vCenter Information page')
                )
                self.delete_vcenter_relationship_page.btn_protected_vcenter_name.click()
                self.loading_window.wait_loading(self.current_browser, 30)
                if self.delete_vcenter_relationship_page.click_drop_down_list(parent_element, 'div',
                                                                              self.protected_name) is False:
                    logger.error("protected_vcenter_name is not exist")
                    self.delete_vcenter_relationship_page.btn_cancel.click()
                    self.fail(msg="protected_vcenter_name is not exist")
                else:
                    self.loading_window.wait_loading(self.current_browser, 30)
                    self.delete_vcenter_relationship_page.btn_recovery_vcenter_name.click()
                    if self.delete_vcenter_relationship_page.click_drop_down_list(parent_element, 'div',
                                                                                  self.recovery_name) is False:
                        logger.error("recovery_vcenter_name is not exist")
                        self.delete_vcenter_relationship_page.btn_cancel.click()
                        self.fail(msg="recovery_vcenter_name is not exist")
                    else:
                        self.loading_window.wait_loading(self.current_browser, 30)

                        # Temporary fix...This AUC need to be rewritten in future
                        self.assertTrue(self.delete_vcenter_relationship_page.btn_confirm_to_del.exists(),
                                        'Drop down list <Confirm> does not exist')
                        self.delete_vcenter_relationship_page.btn_confirm_to_del.click()
                        self.assertTrue(
                            self.delete_vcenter_relationship_page.click_drop_down_list(
                                self.delete_vcenter_relationship_page.lbl_confirmlist, 'tr', 'Confirm'),
                            'Cannot find item Confirm in drop down list')
                        logger.info('Confirm is selected', False, True)
                        self.loading_window.wait_loading(self.current_browser, 30)

                        if self.delete_vcenter_relationship_page.btn_next.exists():
                            self.delete_vcenter_relationship_page.btn_next.click()
                        self.loading_window.wait_loading(self.current_browser, 30)
                        self.assertTrue(
                            self.delete_vcenter_relationship_page.btn_submit.exists(),
                            msg=_formatter.format(step='Navigate to Review and Submit page')
                        )
                        self.delete_vcenter_relationship_page.btn_submit.click()

        except AssertionError:
            self.delete_vcenter_relationship_page.save_request()
            raise
        except:
            self.delete_vcenter_relationship_page.save_request()
            self.fail(self.step_failed_msg + ', more error info: {}'.format(sys.exc_info()[:2]))

        self.assertTrue(self.delete_vcenter_relationship_page.lab_confirmation_success.exists(),
                        msg='Running on step:"Delete Vcenter Relationship"-FAILED,'
                            'after clicking submit button, cannot find the label: '
                            'The request has been submitted successfully.')
        self.delete_vcenter_relationship_page.btn_ok.click()
        logger.info('Request has been submitted successfully', False, True)

        # switch to request
        self.assertTrue(RequestsPage().navigate_to_request(self.current_browser),
                        msg='Running on step:"Delete Vcenter Relationship"-FAILED, '
                            'switch to request frame failed.')

        # check the request
        self.request_result = RequestsPage().get_request_result(
            self.description)
        self.assertIsNotNone(self.request_result, msg='Running on step:"Delete Vcenter Relationship"-FAILED, '
                             'failed to get the request result.')
        logger.info('Checking request result for delete vcenter relationship. Protected vCenter: {}, '
                    'recovery vCenter: {}.'.format(self.protected_name, self.recovery_name), False, True)
        if self.request_result.status == 'Successful':
            logger.info('Deleted vcenter relationship successfully. ', False, True)
        else:
            logger.error('Deleting vcenter relationship failed. Status: {}, status details: {}.'.format(
                self.request_result.status, self.request_result.status_detail))
            DeleteVcenterRelationship.delete_failed_flag = True

    def runTest(self):
        for vc_obj in self.vcenter_relationships_to_delete:
            self.protected_name = vc_obj.protected_vcenter
            self.recovery_name = vc_obj.recovery_vcenter
            logger.info('Start to delete vCenter relationship. Protected vCenter: {}, recovery vCenter: {}.'.format(
                self.protected_name, self.recovery_name), False, True)
            self.description = 'delete_vcenter_relationship_{}_{}'.format(self.protected_name,self.recovery_name)
            self.test_delete_vcenter_relationship()

    def _validate_context(self):
        if self.ctx_in:
            self.request_result = None
            self.current_browser = self.ctx_in.shared.current_browser
            assert self.current_browser is not None, 'current_browser in yaml is None, ' \
                                                     'may be there is no active browser'
            self.assertTrue(self.current_browser.is_login,
                            msg='Please login to vRA, The flag value is_login is: False.')
            self.action = 'Delete vCenter Relationship'

            if not isinstance(getattr(self.ctx_in, 'added_vcenter_relationship', None), list):
                setattr(self.ctx_in, 'added_vcenter_relationship', [])

            added_vcenter_relationship = getattr(self.ctx_in, 'added_vcenter_relationship', [])
            self.vcenter_relationships_to_delete = vcenter_relationship_unique(added_vcenter_relationship)

    def _finalize_context(self):
        self.assertFalse(DeleteVcenterRelationship.delete_failed_flag,
                         'Running on step:"delete vCenter relationship"-FAILED')


# remove repeat and null pair of vcenter relationship from list which will be delete.
def vcenter_relationship_unique(vr_list):
    for counter, vr_obj in enumerate(vr_list):
        protected_vcenter = vr_obj.protected_vcenter
        recovery_vcenter = vr_obj.recovery_vcenter
        if not protected_vcenter or not recovery_vcenter:
            vr_list.remove(vr_obj)
            logger.debug('Removed from added_vcenter_relationship, protected_vcenter: {}, recovery_vcenter: {}'.format(
                protected_vcenter, recovery_vcenter
            ))
            continue

        cmp_list = vr_list[counter + 1:]
        for cmp_vr_obj in cmp_list:
            if cmp_vr_obj.protected_vcenter == protected_vcenter and cmp_vr_obj.recovery_vcenter == recovery_vcenter:
                vr_list.remove(cmp_vr_obj)
    return vr_list

