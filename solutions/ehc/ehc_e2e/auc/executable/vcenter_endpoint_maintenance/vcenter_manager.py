
import sys

from robot.api import logger
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared import CatalogPage
from ehc_e2e.auc.uimap.shared import LoadingWindow
from ehc_e2e.auc.uimap.specific.vcenter_maintenance_page import VCenterMaintenancePage


class VCenterManager(BaseUseCase):

    class Func(object):
        ADD_VCENTER, EDIT_VCENTER, DELETE_VCENTER = (
            'test_adding_vCenter',
            'test_editing_vCenter',
            'test_deleting_vCenter')

    def __init__(self, name=None, method_name=Func.ADD_VCENTER, **kwargs):
        super(VCenterManager, self).__init__(
            name, method_name, **kwargs)
        self._related_vcenter = None
        _auc_name = ' '.join([word.capitalize() for word in name.split('_')])
        self._formatter = ('Running on: ' + _auc_name + ' - FAILED, "{step}"').format

    # Wrap assertTrue method to log the message of current operation
    def assertTrue(self, expr, msg=None):
        super(VCenterManager, self).assertTrue(expr, self._formatter(step='{} {}'.format(msg, 'failed')))
        logger.info('Completed {}'.format(msg), False, True)

    def setUp(self):
        self.vcenter_request_page = VCenterMaintenancePage()
        self.catalog_page = CatalogPage()
        self.loading_window = LoadingWindow()

    def test_adding_vCenter(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._add_vcenter_operation()

    def test_editing_vCenter(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._edit_vcenter_operation()

    def test_deleting_vCenter(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._delete_vcenter_operation()

    def _start_new_service_request(self):
        self.assertTrue(self.catalog_page.navigate_to_catalog(self.current_browser), 'can not switch to catalog frame')

        self.assertTrue(self.vcenter_request_page.ehc_configure.exists(),
                        'Checking if navigation button <EHC Configuration> exists')
        self.vcenter_request_page.ehc_configure.click()

        self.assertTrue(self.catalog_page.btn_vcenter_endpoint_request.exists(),
                        'Checking if Catalog Item button <Request> exists')
        self.catalog_page.btn_vcenter_endpoint_request.click()
        self.loading_window.wait_loading(self.current_browser)
        
        logger.info('Request button clicked. Going to vCenter Endpoint Maintenance page', False, True)

    def _fill_out_request_info(self):
        self.assertTrue(self.vcenter_request_page.txt_description.exists(),
                        'Checking if  textbox <Description> exists')
        self.vcenter_request_page.txt_description.set(self._testMethodName)

        self.assertTrue(self.vcenter_request_page.txt_reasons.exists(), 'can not find textbox <Reasons>')
        self.vcenter_request_page.txt_reasons.set(self._name)

        self.assertTrue(self.vcenter_request_page.btn_next.exists(),
                        'Checking if button <Next> exists to proceed to next tab')
        self.vcenter_request_page.btn_next.click()

        logger.info('Request information filled out. Going to the next tab', False, True)

    def _add_vcenter_operation(self):
        try:
            self.assertTrue(self.vcenter_request_page.select_action.exists(), 'can not find drop down list <Action>')
            self.vcenter_request_page.select_action.click()

            self.assertTrue(
                self.vcenter_request_page.click_drop_down_list(self.vcenter_request_page.parent_element, 'div',
                                                               self.select_operation),
                'selecting "action" {} in drop down list'.format(self.select_operation))
            logger.info(self.select_operation + ' is selected', False, True)
            self.loading_window.wait_loading(self.current_browser, 60)

            self.assertTrue(self.vcenter_request_page.btn_next.exists(),
                            'Checking if button <Next> exists')
            self.vcenter_request_page.btn_next.click()
            self.loading_window.wait_loading(self.current_browser, 60)

            self.assertTrue(self.vcenter_request_page.select_vc_fqdn_to_add,
                            'Checking if drop down list <vCenter FQDN> exits')
            self.vcenter_request_page.select_vc_fqdn_to_add.click()

            self.assertTrue(
                self.vcenter_request_page.click_drop_down_list(self.vcenter_request_page.parent_element, 'div',
                                                               self.select_vc_fqdn_to_add),
                'selecting vCenter FQDN {} in drop down list'.format(self.select_vc_fqdn_to_add))
            self.loading_window.wait_loading(self.current_browser, 60)

            driver = self.current_browser.instance._browser.current
            for site in self.new_vcenter_associated_sites:
                try:
                    site_checkbox = driver.find_element_by_xpath(
                        self.vcenter_request_page.new_vcenter_associated_sites_xpath.format(site))
                    site_checkbox.click()
                    self.loading_window.wait_loading(self.current_browser, 60)
                except:
                    import sys
                    logger.info('Exception: {}'.format(sys.exc_info()), False, True)
                    self.fail(self._formatter(step='Checking if checkbox for site: "{}" exists'.format(site)))

            self.assertTrue(self.vcenter_request_page.select_datacenter.exists(),
                            'Checking if drop down list <Datacenter> exists')
            self.vcenter_request_page.select_datacenter.click()

            self.assertTrue(
                self.vcenter_request_page.click_drop_down_list(self.vcenter_request_page.parent_element, 'div',
                                                               self.datacenter_to_add),
                'selecting Datacenter {} in drop down list'.format(self.datacenter_to_add))
            logger.info(self.datacenter_to_add + ' is selected', False, True)
            self.loading_window.wait_loading(self.current_browser, 60)

            self.assertTrue(self.vcenter_request_page.txt_name_for_vcenter.exists(),
                            'Checking if text input <vCenter> exists')
            self.vcenter_request_page.txt_name_for_vcenter.set(self.name_for_vcenter_endpoint)
            self.loading_window.wait_loading(self.current_browser, 60)
            self.vcenter_request_page.send_tab_key(self.vcenter_request_page.txt_name_for_vcenter)
            self.loading_window.wait_loading(self.current_browser, 60)
            self.assertTrue(self.vcenter_request_page.btn_next.exists(),
                            'Checking if button <Next> exits')
            self.vcenter_request_page.btn_next.click()
            self.loading_window.wait_loading(self.current_browser, 60)

            self.assertTrue(self.vcenter_request_page.btn_submit.exists(), 'checking if button <Submit> exists')
            self.vcenter_request_page.btn_submit.click()
        except AssertionError:
            self.vcenter_request_page.save_request()
            raise
        except:
            import sys
            logger.info('Exception <{}> occurred...Trying to save the request'.format(sys.exc_info()), False, True)
            self.vcenter_request_page.save_request()
            raise

        self.assertTrue(self.vcenter_request_page.btn_ok.exists(), 'checking if button <OK> exists in after-submission page')
        self.vcenter_request_page.btn_ok.click()

        self._related_vcenter = self.name_for_vcenter_endpoint

    def _edit_vcenter_operation(self):
        try:
            self.assertTrue(self.vcenter_request_page.select_action.exists(), 'checking if drop down list <Action> exists')
            self.vcenter_request_page.select_action.click()

            self.assertTrue(
                self.vcenter_request_page.click_drop_down_list(self.vcenter_request_page.parent_element, 'div',
                                                               self.select_operation),
                'selecting action {} from drop down list'.format(self.select_operation))
            logger.info(self.select_operation + ' is selected', False, True)
            self.loading_window.wait_loading(self.current_browser, 30)

            self.assertTrue(self.vcenter_request_page.btn_next.exists(),
                            'checking if button <Next> exists to proceed to next tab')
            self.vcenter_request_page.btn_next.click()
            self.loading_window.wait_loading(self.current_browser, 30)

            self.assertTrue(self.vcenter_request_page.btn_existing_vcenter.exists(),
                            'checking if drop down list <Existing vCenter>')
            self.vcenter_request_page.btn_existing_vcenter.click()
            self.assertTrue(
                self.vcenter_request_page.click_drop_down_list(self.vcenter_request_page.parent_element, 'div',
                                                               self.existing_vcenter_object),
                'selecting existing vCenter {} in drop down list'.format(self.existing_vcenter_object))
            logger.info(self.existing_vcenter_object + ' is selected', False, True)
            self.loading_window.wait_loading(self.current_browser, 30)

            self.assertTrue(self.vcenter_request_page.txt_vcenter_name.exists(),
                            'checking if textbox <vCenter Name> exists')
            self.vcenter_request_page.txt_vcenter_name.set('')
            self.vcenter_request_page.send_tab_key(self.vcenter_request_page.txt_vcenter_name)
            self.loading_window.wait_loading(self.current_browser, 30)
            self.vcenter_request_page.txt_vcenter_name.set(self.vcenter_name)
            self.vcenter_request_page.send_tab_key(self.vcenter_request_page.txt_vcenter_name)
            self.loading_window.wait_loading(self.current_browser, 30)
            self.assertTrue(self.vcenter_request_page.btn_vcenter_fqdn.exists(),
                            'checking if drop down list <vCenter FQDN> exists')
            self.vcenter_request_page.btn_vcenter_fqdn.click()
            self.assertTrue(
                self.vcenter_request_page.click_drop_down_list(self.vcenter_request_page.parent_element, 'div',
                                                               self.vcenter_fqdn),
                'selecting vCenter FQDN {} from drop down list'.format(self.vcenter_fqdn))
            logger.info(self.vcenter_fqdn + ' is selected', False, True)
            self.loading_window.wait_loading(self.current_browser, 30)

            self.assertTrue(self.vcenter_request_page.btn_datacenter.exists(),
                            'checking if drop down list <Datacenter> exists')
            self.vcenter_request_page.btn_datacenter.click()
            self.assertTrue(
                self.vcenter_request_page.click_drop_down_list(self.vcenter_request_page.parent_element, 'div',
                                                               self.datacenter),
                'selecting Datacenter {} in drop down list'.format(self.datacenter))
            logger.info(self.vcenter_fqdn + ' is selected', False, True)
            self.loading_window.wait_loading(self.current_browser, 30)

            driver = self.current_browser.instance._browser.current
            logger.info('Start to clear all checkboxes', False, True)
            try:
                cb_list = driver.find_elements_by_xpath('//input[@checked]')
                for i in range(len(cb_list)):
                    # dynamic checkbox, need to find again
                    driver.find_element_by_xpath('//input[@checked]').click()
                    self.loading_window.wait_loading(self.current_browser, 30)
            except Exception as e:
                self.fail('Exception <{}> occurred while trying to clear all checkboxes'.format(type(e).__name__))

            for site in self.sites:
                logger.info('Find and select checkbox for site ' + site, False, True)
                logger.info('xpath:{}'.format(self.vcenter_request_page.new_vcenter_associated_sites_xpath.format(site)), False, True)
                site_checkbox = driver.find_element_by_xpath(
                    self.vcenter_request_page.new_vcenter_associated_sites_xpath.format(site))
                try:
                    site_checkbox.click()
                    self.loading_window.wait_loading(self.current_browser, 30)
                except:
                    self.fail(self._formatter(step='checking existence and selecting checkbox for site {}'.format(site)))

            self.assertTrue(self.vcenter_request_page.btn_next.exists(),
                            'checking if button <Next> exists to proceed to next tab')
            self.vcenter_request_page.btn_next.click()
            self.loading_window.wait_loading(self.current_browser, 30)

            self.assertTrue(self.vcenter_request_page.btn_submit.exists(), 'checking if button <Submit> exists')
            self.vcenter_request_page.btn_submit.click()

        except Exception as e:
            logger.error('Exception <{}> occurred...Trying to save the request'.format(type(e).__name__))
            self.vcenter_request_page.save_request()
            raise

        self.assertTrue(self.vcenter_request_page.btn_ok.exists(), 'checking if button <OK> exists in page after-submission')
        self.vcenter_request_page.btn_ok.click()

        self._related_vcenter = self.vcenter_name

    def _delete_vcenter_operation(self):
        try:
            self.assertTrue(self.vcenter_request_page.select_action.exists(), 'can not find drop down list <Action>')
            self.vcenter_request_page.select_action.click()

            self.assertTrue(
                self.vcenter_request_page.click_drop_down_list(self.vcenter_request_page.parent_element, 'div',
                                                               self.select_operation),
                'selecting action {} from drop down list'.format(self.select_operation))
            logger.info(self.select_operation + ' is selected', False, True)
            self.loading_window.wait_loading(self.current_browser, 30)

            self.assertTrue(self.vcenter_request_page.btn_next.exists(),
                            'checking if button <Next> exists to proceed to next tab')
            self.vcenter_request_page.btn_next.click()
            self.loading_window.wait_loading(self.current_browser, 30)

            self.assertTrue(self.vcenter_request_page.btn_vcenter_to_del.exists(),
                            'checking if drop down list <vCenter> exists')
            self.vcenter_request_page.btn_vcenter_to_del.click()
            self.assertTrue(
                self.vcenter_request_page.click_drop_down_list(self.vcenter_request_page.lbl_select_vcenterlist_value,
                                                               'tr', self.select_vcenter_name),
                'selecting vCenter {} from drop down list'.format(self.select_vcenter_name))
            logger.info(self.select_vcenter_name + ' is selected', False, True)
            self.loading_window.wait_loading(self.current_browser, 30)

            self.assertTrue(self.vcenter_request_page.btn_confirm_to_del.exists(),
                            'checking if drop down list <Confirm> exist')
            self.vcenter_request_page.btn_confirm_to_del.click()
            self.assertTrue(
                self.vcenter_request_page.click_drop_down_list(self.vcenter_request_page.lbl_select_confirmlist_value,
                                                               'tr', self.ensure_delete_info),
                'selecting {} from drop down list'.format(self.ensure_delete_info))
            logger.info(self.ensure_delete_info + ' is selected', False, True)
            self.loading_window.wait_loading(self.current_browser, 30)

            self.assertTrue(self.vcenter_request_page.btn_next.exists(),
                            'checking if button <Next> exists to proceed to next tab')
            self.vcenter_request_page.btn_next.click()
            self.loading_window.wait_loading(self.current_browser, 30)

            self.assertTrue(self.vcenter_request_page.btn_submit.exists(),
                            'checking if button <Submit> exist')
            self.vcenter_request_page.btn_submit.click()
        except Exception as ex:
            logger.error('Exception <{}> occurred...Trying to save the request'.format(type(ex).__name__))
            self.vcenter_request_page.save_request()
            raise

        self.assertTrue(self.vcenter_request_page.btn_ok.exists(), 'checking if button <OK> exists in page after-submission')
        self.vcenter_request_page.btn_ok.click()

    def _validate_input_args(self, **kwargs):
        if self._testMethodName == self.Func.ADD_VCENTER:
            self._validate_args_of_adding_vcenter(**kwargs)
        elif self._testMethodName == self.Func.EDIT_VCENTER:
            self._validate_args_of_editing_vcenter(**kwargs)
        elif self._testMethodName == self.Func.DELETE_VCENTER:
            self._validate_args_of_deleting_vcenter(**kwargs)

    def _finalize_output_params(self):
        if self._testMethodName == self.Func.ADD_VCENTER and self._related_vcenter:
            self._output.append(self._related_vcenter)
        elif self._testMethodName == self.Func.EDIT_VCENTER:
            self._output.append(self._related_vcenter)

    def _validate_args_of_adding_vcenter(self, **kwargs):
        self.current_browser = kwargs.get('current_browser')
        self.select_operation = kwargs.get('select_operation')
        self.name_for_vcenter_endpoint = kwargs.get('name_for_vcenter_endpoint')
        self.select_vc_fqdn_to_add = kwargs.get('select_vc_fqdn_to_add')
        self.new_vcenter_associated_sites = kwargs.get('new_vcenter_associated_sites')
        self.datacenter_to_add = kwargs.get('select_datacenter_to_add')
        self.add_sites = kwargs.get('add_sites')
        self.add_vcenters = kwargs.get('add_vcenter')
        self.onboard_cluster_type = kwargs.get('onboard_cluster_type')

    def _validate_args_of_editing_vcenter(self, **kwargs):
        self.current_browser = kwargs.get('current_browser')
        self.select_operation = kwargs.get('select_operation')
        self.existing_vcenter_object = kwargs.get('existing_vcenter_object')
        self.vcenter_name = kwargs.get('vcenter_name')
        self.vcenter_fqdn = kwargs.get('vcenter_fqdn')
        self.datacenter = kwargs.get('datacenter')
        self.sites = kwargs.get('sites')
        self.vcenter_username = kwargs.get('vcenter_username')
        self.vcenter_password = kwargs.get('vcenter_password')

    def _validate_args_of_deleting_vcenter(self, **kwargs):
        self.current_browser = kwargs.get('current_browser')
        self.select_operation = kwargs.get('select_operation')
        self.select_vcenter_name = kwargs.get('select_vcenter_name')
        self.ensure_delete_info = kwargs.get('ensure_delete_info')
