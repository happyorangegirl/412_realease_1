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

import time
import sys
from robot.api import logger
from selenium.webdriver.remote.webelement import WebElement
from uiacore.modeling.webui.controls import (WebTextBox, WebButton, WebLabel,
                                             WebLink)
from .mainpage import MainPage
from .basepage import BasePage
from ehc_e2e.auc.uimap.shared.loadingwindow import LoadingWindow


class InfrastructurePage(BasePage):

    def __init__(self):
        self.gadget_2_frame_id = '__gadget_2'
        self.gadget_3_frame_id = '__gadget_3'

        # Wenda: iframe id is dynamic in badger. temporarily use extensionid instead
        self.infra_reservation_edit_frame_extensionid = 'com.vmware.vcac.core.cafe.reservation.reservations'
        self.reservation_edit_detail_frame_extensionid = 'com.vmware.vcac.iaas.reservation.details'
        self.infra_reservation_policy_edit_frame_extensionid = \
            'com.vmware.vcac.core.cafe.reservation.reservationPolicies'
        self.infra_network_profiles_edit_frame_extensionid = 'com.vmware.csp.component.ipam.service.network.profiles'
        self.extensionid_iaas = 'csp.places.iaas'

        self.lbl_gadget_2_frame = WebLabel(id='__gadget_2')
        self.lnk_infrastructure_default = WebLink(
            xpath='//*[@id="csp.places.iaas.Default"]'
        )

        self.url_iaas_gadget = \
            'https://com.vmware.csp.component.iaas.proxy.provider.plugin.vproxy//iaas/IaasGadget.gadget.xml'
        self.url_gadget = 'https://com.vmware.vcac.core.cafe.reservation.plugin.vproxy//gadget.xml'

        self.title_blueprint_edit_page = 'Edit Blueprint - vSphere'
        self.btn_anchor_infrastructure = WebButton(
            xpath='//*[@id="csp.places.iaas" and @class="gwt-Label navCell backCell"]')

        # sub function related page elements.
        self.lnk_reservation_items_list_grid = WebLink(
            xpath='//*[starts-with(@id, "reservation-listGrid-") and contains(@id, "-body")]'
        )
        self.lnk_reservation_items_list_grid_sub1 = WebLink(
            xpath='//*[@id="reservation-listGrid-1035-body"]/div/div[2]/table[1]/tbody/')
        self.reservation_filter_result_first_element_xpath = \
            '//*[starts-with(@id, "reservation-listGrid-") and contains(@id, "-body")]' \
            '/div/div[2]/table[1]/tbody/tr/td[1]/div/span[2]'
        self.lbl_reservation_edit_title = WebLabel(
            xpath='//div[starts-with(@id, "vcacpageheader") and contains(@id, "innerCt")]'
                  '/div[text()="Edit Reservation - vSphere (vCenter)"]'
        )

        self.txt_reservation_edit_reservation_policy = WebTextBox(
            xpath='//*[@id="ctl00_ctl00_MasterContent_MainContentPlaceHolder'
                  '_ReservationTabs_policyPicker_I"]'
        )
        self.txt_reservation_edit_reservation_name = WebTextBox(
            xpath='//*[@id="ctl00_ctl00_MasterContent_MainContentPlaceHolder'
                  '_ReservationTabs_txtHostReservationName_I"]'
        )

        self.blueprint_filter_result_first_element_xpath = \
            '//*[@id="ctl00_ctl00_MasterContent_MainContentPlaceHolder_' \
            'pnlTemplates_gridControl_templateGrid_cell0_0_mnuTemplate_DXI0_T"]/span'

        # TODO: this has been changed, it needs to be removed.
        self.xpath_lbl_blueprint_edit_title = ''
        self.lbl_blueprint_edit_title = WebLabel(
            xpath=self.xpath_lbl_blueprint_edit_title
        )

        self.btn_back_to_infrastructure = WebButton(
            xpath='//*[@id="csp.places.iaas"]/div')
        self.btn_recent_events = WebButton(
            xpath='//*[@id="csp.places.iaas.Default"]/div')
        self.btn_machines = WebButton(
            xpath='//*[@id="csp.places.iaas.Machines"]/div')
        self.btn_groups = WebButton(
            xpath='//*[@id="csp.places.iaas.Groups"]/div')
        self.btn_endpoints = WebButton(
            xpath='//*[@id="csp.places.iaas.Endpoints"]/div')
        self.btn_reservations = WebButton(
            xpath='//*[@id="csp.places.iaas.Reservations"]/div')
        self.btn_computer_resources = WebButton(
            xpath='//*[@id="csp.places.iaas.ComputeResources"]/div')
        self.btn_blueprints = WebButton(
            xpath='//*[@id="csp.places.iaas.Blueprints"]')
        self.btn_infrastructure_orgnanizer = WebButton(
            xpath='//*[@id="csp.places.iaas.Discovery"]/div')
        self.btn_administration = WebButton(
            xpath='//*[@id="csp.places.iaas.Administration"]/div')
        self.btn_monitering = WebButton(
            xpath='//*[@id="csp.places.iaas.Monitoring"]/div')

        self.btn_dest_managed_machines = WebButton(
            xpath='//*[@id="csp.places.iaas.EnterpriseAdmin'
                  '.ManageVirtualMachines"]/div'
        )
        self.btn_dest_reserved_machines = WebButton(
            xpath='//*[@id="csp.places.iaas.GroupAdmin'
                  '.ManageVirtualMachines"]/div'
        )
        self.btn_dest_fabric_groups = WebButton(
            xpath='//*[@id="csp.places.iaas.VMPSAdmin.ViewEntAdmins"]/div'
        )
        self.btn_dest_business_groups = WebButton(
            xpath='//*[@id="csp.places.iaas.EnterpriseAdmin.ViewGroups"]/div'
        )
        self.btn_dest_endpoints = WebButton(
            xpath='//*[@id="csp.places.iaas.VMPSAdmin.ViewEndpoints"]/div'
        )
        self.btn_dest_credentials = WebButton(
            xpath='//*[@id="csp.places.iaas.VMPSAdmin.EditCredentials"]/div'
        )
        self.btn_dest_agents = WebButton(
            xpath='//*[@id="csp.places.iaas.VMPSAdmin.AgentConfiguration"]/div'
        )
        self.btn_dest_reservations = WebButton(
            xpath='//*[@id="com.vmware.vcac.core.cafe.reservation.reservations"]/div'   # id is changed in badger
        )                                                              # not only this one, plz check other items
        self.btn_dest_reservation_policies = WebButton(
            xpath='//*[@id="com.vmware.vcac.core.cafe.reservation.reservationPolicies"]/div'
        )
        self.btn_dest_network_profiles = WebButton(
            xpath='//*[@id="csp.places.iaas.EnterpriseAdmin'
                  '.ListStaticIPv4NetworkProfiles"]/div'
        )
        self.btn_dest_key_pairs = WebButton(
            xpath='//*[@id="csp.places.iaas.EnterpriseAdmin.EditKeyPairs"]/div'
        )
        self.btn_dest_computer_resources = WebButton(
            xpath='//*[@id="csp.places.iaas.EnterpriseAdmin.ViewHosts"]/div'
        )
        self.btn_dest_cost_profiles = WebButton(
            xpath='//*[@id="csp.places.iaas.EnterpriseAdmin'
                  '.EditCostProfiles"]/div'
        )
        self.btn_dest_ebs_volums = WebButton(
            xpath='//*[@id="csp.places.iaas.EnterpriseAdmin'
                  '.ManageEBSVolumes"]/div'
        )
        self.btn_dest_blueprints = WebButton(
            xpath='//*[@id="csp.places.iaas.GroupAdmin.ViewTemplates"]/div'
        )
        self.btn_dest_build_prifiles = WebButton(
            xpath='//*[@id="csp.places.iaas.EnterpriseAdmin'
                  '.ViewGlobalProfiles"]/div'
        )
        self.btn_dest_property_dictionary = WebButton(
            xpath='//*[@id="csp.places.iaas.EnterpriseAdmin'
                  '.ViewGlobalProfiles"]/div'
        )
        self.btn_dest_machine_prefixes = WebButton(
            xpath='//*[@id="csp.places.iaas.EnterpriseAdmin'
                  '.EditHostnamePrefixes"]/div'
        )
        self.btn_dest_instance_types = WebButton(
            xpath='//*[@id="csp.places.iaas.VMPSAdmin.EditInstanceTypes"]/div'
        )

        # Content area.
        self.lbl_reservation_advanced_search_header = WebLabel(
            xpath='//*[starts-with(@id, "reservation-searchPanel-") and contains(@id, "-placeholder-innerCt")]'
        )
        self.btn_reservation_advanced_search_search = WebButton(
            xpath='//span[text()="Search"]'
        )
        self.lbl_reservation_advanced_search_not_found = WebLabel(
            xpath='//div[text()="No data to display"]'
        )

        # reservation search result container
        self.xpath_reservation_search_result_grid = \
            '//*[starts-with(@id, "reservation-listGrid-") and contains(@id, "-body")]'
        self.txt_reservation_name = WebTextBox(
            xpath=('//*[starts-with(@id, "reservation-searchPanel-") and contains(@id, "-targetEl")]'
                   '/div/div/table/tbody/tr[1]/td[1]/div/div/div/div/input')
        )
        self.txt_blueprint_name = WebTextBox(
            xpath='//*[@id="ctl00_ctl00_MasterContent_MainContentPlaceHolder_'
                  'pnlTemplates_gridControl_templateGrid_DXFREditorcol0_I"]'
        )

        self.lnk_blueprint_filters_clear = WebLink(
            xpath='//*[@id="ctl00_ctl00_MasterContent_MainContentPlaceHolder'
                  '_pnlTemplates_gridControl_templateGrid_DXFilterBar"]/tbody/'
                  'tr/td[5]'
        )
        self.policy_name = 'dev17_DR'
        self.btn_reservation_policy_dropdown = WebButton(
            id='reservation-reservationPolicyComboBox-1024-trigger-picker'
        )

        self.btn_reservation_advanced_search_open = WebButton(
            xpath='//*[starts-with(@id, "reservation-searchPanel-") and '
                  'contains(@id, "-placeholder-targetEl")]/div[2]/div'
        )
        self.btn_tenant_dropdown_open = WebButton(
            xpath='//div[starts-with(@id, "reservation-searchPanel") and contains(@id, "targetEl")]'
                  '/div/div/table/tbody/tr[1]/td[3]/div/div/div/div[2]')
        self.lst_tenant = WebLabel(xpath='//*[starts-with(@id, "boundlist") and contains(@id, "listEl")]')

    def back_to_infrastructure_default_page(self, current_browser):
        # when swith to default content, next time go into this page will in the default page will not influence other
        # case, back to the default menu is better, if failed, log the error info and no need to failed the workflow.
        _browser = current_browser.instance._browser.current
        try:
            self.wait_for_loading_complete(5)
            _browser.switch_to.default_content()
            iaas_gadget_frame_id = self.get_accurate_frameid(
                current_browser, self.extensionid_iaas, from_top_document=True, attribute_name='extensionid')
            if iaas_gadget_frame_id:
                _browser.switch_to.frame(iaas_gadget_frame_id)
                logger.debug('Switched to iaas iframe: "{}".'.format(iaas_gadget_frame_id))
            else:
                logger.warn('The iaas iframe is failed to found.')

            if self.btn_anchor_infrastructure.exists():
                self.btn_anchor_infrastructure.click()
                self.wait_for_loading_complete(2)
                logger.info('Clicked Infrastructure back button.', False, True)

                if self.btn_recent_events.exists():
                    self.btn_recent_events.click()
                    self.wait_for_loading_complete(2)
                    logger.info(
                        'Clicked "Recent Event" button and navigated back to '
                        'Infrastructure default page done.', False, True)
                    _browser.switch_to.default_content()
                    return True
                else:
                    # Some time may encounter environment error: blank page when back to default page
                    logger.warn('Button "Recent Events" does not exist, '
                                'failed to navigate back to "Recent Events" page.')
            else:
                logger.warn(
                    'Infrastructure page "Infrastructure" button does not exists, failed to '
                    'navigate back to Infrustracture default page.')
        except:
            ex = sys.exc_info()[0]
            logger.warn('Navigate back to Infrastructure default page failed, '
                        'exception: {}'.format(ex))
        snap_shot_file_name = time.strftime('%y_%m_%d_%H_%M_%S')
        from ehc_e2e.utils.snapshot import SnapShot
        SnapShot.takes_screen_shot(_browser, 'Back_to_infra_default' + snap_shot_file_name)
        return False

    def navigate_to_iframe(self, current_browser, attribute_name='', url_in_attribute=''):
        '''
        navigate to an iframe the iframe will be located by given conditions, attribute_name:url
        NOTE: this only supports navigate to iframe which resides at following level.
        Args:
            current_browser:
            attribute_name:
            url_in_attribute:

        Returns:

        '''
        try:
            _browser = current_browser.instance._browser.current
            iframe_id = self.get_accurate_frameid(current_browser,
                                                  url_in_attribute, False, attribute_name)
            if not iframe_id:
                logger.error('"iframe_id" returned by get_accurate_frameid is None')
                return False
            _browser.switch_to.frame(iframe_id)
            self.wait_for_loading_complete(1)
            logger.info('Infrastructure navigate to iframe, switched to'
                        ' iframe: {}.'.format(iframe_id), False, True)
            return True
        except:
            logger.error('Encounter exception in method navigate_to_iframe, detail info: ' + sys.exc_info())
        return False

    def navigate_to_reservation_detail_1st_frame(self, current_browser,):
        '''
        navigate to the first frame within reservation details page, edit section.
         hierarchy is as:
         root->iaas_gadget->com.vmware.vcac.core.cafe.reservation.reservations
        Args:
            current_browser:

        Returns: True if

        '''
        _browser = current_browser.instance._browser.current
        try:
            _browser.switch_to.default_content()
            iaas_gadget_frame_id = BasePage().get_accurate_frameid(current_browser,
                                                                   self.url_iaas_gadget)
            _browser.switch_to.frame(iaas_gadget_frame_id)
            logger.info(
                'Switched to iaas gadget frame, id:{}'.format(iaas_gadget_frame_id),
                False, True)

            reservation_details_1st_frame_id = BasePage().get_accurate_frameid(
                current_browser, self.infra_reservation_edit_frame_extensionid, False,
                attribute_name='extensionid')
            _browser.switch_to.frame(reservation_details_1st_frame_id)
            logger.info('Switched to reservation details first frame, id:{}'.format(
                reservation_details_1st_frame_id), False, True)
        except:
            logger.error(
                'Switching to reservation edit detail first frame encounters error: {}'
                ''.format(sys.exc_info()[:2])
            )
            return False

        return True

    def navigate_to_dest_page(self, current_browser,
                              btn_first_level,
                              btn_dest):
        """
         Navigate to the destination page by clicking two buttons in
         two consequential levels, first level and dest. It will switch to
         the frame in the destination page where right table content resides.
         e.g.:
            below call will navigate to reservations page and switch to
            self.dest_edit_page_frame_id frame.
                ret_navigate_dest = self.navigate_to_dest_page(
                self.current_browser,
                self.btn_reservations,
                self.btn_dest_reservations)
        Args:
            current_browser: The browser object passed between workflow context.
            btn_first_level: The WebButton object for the first level in left
                                pane of Infrastructure page.
            btn_dest: The destination WebButton object you want to navigate to.

        Returns: True if navigated to the specified destination page.

        """
        _browser = current_browser.instance._browser.current

        try:
            for i in xrange(10):
                # Switch to infrastructure page-> gadget_2_frame first.
                navigate_to_infra = self.navigate_to_infrastructure(current_browser)

                if navigate_to_infra is False:
                    logger.error('Navigate to infrastructure page failed.')
                    return False
                self.wait_for_loading_complete(5)
                # The tree menu may different when go into infrastructure page,
                # if the last time leave page difference, maybe in the first menu page, maybe in dest menu page.
                if btn_first_level.exists():
                    btn_first_level.click()
                    logger.info(
                        'Infrastructure page navigating to destination page clicked'
                        ' first level button.', False, True)
                    self.wait_for_loading_complete(3)

                    if btn_dest.exists():
                        btn_dest.click()
                        self.wait_for_loading_complete(1)
                        logger.info(
                            'Infrastructure page navigating to destination page clicked'
                            ' destination page button.', False, True)

                        return True
                    else:
                        logger.error(
                            'Infrastructure page destination level button '
                            'does not exist in {} attempts.'.format(i+1), True)
                elif btn_dest.exists():
                    btn_dest.click()
                    self.wait_for_loading_complete(1)
                    logger.info(
                        'Infrastructure page navigating to destination page clicked'
                        ' destination page button.', False, True)

                    return True
                else:
                    logger.error(
                        'Infrastructure page first level button and dest button '
                        'all does not exist in {} attempt.'.format(i+1), True)
            logger.error('After 10 times attempts, first level button and dest button still does not exist.', True)
        except:
            ex = sys.exc_info()[:2]
            if btn_dest:
                logger.error('Navigating to Infrastructure destination page '
                             '{0} failed with exception {1}'
                             .format(btn_dest.current.text, ex))
            else:
                logger.error('Navigating to Infrastructure dest page failed'
                             ' with exception {0}'
                             .format(ex))

        snap_shot_file_name = time.strftime('%y_%m_%d_%H_%M_%S')
        from ehc_e2e.utils.snapshot import SnapShot
        SnapShot.takes_screen_shot(_browser, 'navigate_to_dest_page' + snap_shot_file_name)
        logger.error('Navigating to Infrastructure destination page failed.')
        return False

    def filter_reservation(self, current_browser, reservation_name, tenant_name=None):
        """
         filter out the weblink of given reservation
        Args:
            current_browser: the browser object passed between workflow context.
            reservation_name: the name of reservation to filter.
            tenant_name: the name of tenant.
        Returns: a WebLink object if the given reservation is found.

        """
        if not current_browser or not reservation_name:
            logger.error('Parameter passed to filter_reservation:current_brower'
                         ' or reservation_name is None.')
            return None

        logger.info('Navigating to reservation filter page.', False, True)
        _browser = current_browser.instance._browser.current
        _browser.switch_to.default_content()
        self.wait_for_loading_complete(2)
        iaas_gadget_frame_id = self.get_accurate_frameid(
            current_browser, self.url_iaas_gadget)
        _browser.switch_to.frame(iaas_gadget_frame_id)
        logger.info(
            'Navigated to reservation page, switched to iframe {}'.format(
                iaas_gadget_frame_id), False, True)
        self.wait_for_loading_complete(2)
        gadget_iframe_id = self.get_accurate_frameid(
            current_browser, self.url_gadget, from_top_document=False)
        _browser.switch_to.frame(gadget_iframe_id)
        logger.info(
            'Navigated to reservation page, switched to'
            ' gadget iframe: {}.'.format(gadget_iframe_id), False, True)

        if self.lbl_reservation_advanced_search_header.exists():
            logger.info('Opened reservation search block.', False, True)
            if self.btn_reservation_advanced_search_open.exists():
                self.btn_reservation_advanced_search_open.click()
                self.wait_for_loading_complete(1)
                logger.info('Opened reservation advanced search.')
            if tenant_name:
                if self.btn_tenant_dropdown_open.exists():
                    self.btn_tenant_dropdown_open.click()
                    self.wait_for_loading_complete(5)
                    if self.click_drop_down_list(self.lst_tenant, 'li', tenant_name, strip_text=True):
                        logger.info('Tenant {} is found and select.'.format(tenant_name), False, True)
                    else:
                        logger.error('Can not select tenant: {}.'.format(tenant_name))
                        return None
                else:
                    logger.error('Reservatioin search tenant open button does not exist.')
                    return None
            if self.txt_reservation_name.exists():

                # BUG: Maybe a bug in underlying selenium webelement sendkeys() method.
                # if the textbox here contains reservation_name already,
                # webtextbox's set()(where it has clear and sendkeys method called)
                # will have problem, so set to empty string in the first.
                self.txt_reservation_name.set('')
                logger.info('Cleared reservation name text box', False, True)
                self.wait_for_loading_complete(2)
                self.txt_reservation_name.set(reservation_name)
                logger.info('Input reservation name {} to try to search it out.'
                            .format(reservation_name), False, True)
                if self.btn_reservation_advanced_search_search.exists():
                    self.btn_reservation_advanced_search_search.click()
                    self.wait_for_loading_complete(5)
                    logger.info('Waited 5 seconds for searching done!', False, True)
                else:
                    logger.warn(
                        'Reservation advanced search search button does not exist.')
                    return None
            else:
                logger.error('Reservation search name input textbox is not found.')
                return None

            # Check to see if there is search result.
            current_browser.instance._browser.current.implicitly_wait(2)
            if self.lbl_reservation_advanced_search_not_found.exists():
                snap_shot_file_name = time.strftime('%y_%m_%d_%H_%M_%S')
                from ehc_e2e.utils.snapshot import SnapShot
                SnapShot.takes_screen_shot(_browser, 'Search_for_Reservation_' + snap_shot_file_name)
                logger.warn(
                    'No record found for reservation with name: {}'.format(reservation_name))
                return None
            current_browser.instance._browser.current.implicitly_wait(30)

            reservation_items_list = _browser.find_element_by_xpath(self.xpath_reservation_search_result_grid)
            search_result_items = reservation_items_list.find_elements_by_tag_name('table')

            for i, resv_result in enumerate(search_result_items):
                first_row_tds = resv_result.find_elements_by_tag_name('td')
                if first_row_tds is not None:
                    resv_name = first_row_tds[0].text.strip()
                    if resv_name == reservation_name.strip():
                        logger.info(
                            'Reservation "{}" is found and filtered.'.format(reservation_name),
                            False, True
                        )

                        # the actual UI element that navigates to edit page is following below hierarchy.
                        # /td/span[2]
                        result_element_spans = first_row_tds[0].find_elements_by_tag_name('span')
                        if result_element_spans and len(result_element_spans) == 2:
                            logger.debug('Found "span" element for reservation item.')
                        else:
                            logger.error('The "span" element for reservation item not found.')

                        return result_element_spans[1]
                else:
                    logger.error('Finding "td" elements for reservation search result row {0} item failed.'.format(i+1))

        logger.info('Reservation {} is not found.'.format(reservation_name), False, True)
        return None

    def filter_blueprint(self, current_browser, blueprint_name):
        """
         filter out the weblink of given blueprint
        Args:
            current_browser: the browser object passed between workflow context.
            blueprint_name: the name of reservation to filter.

        Returns: a WebLink object if the given blueprint is found.

        """
        if not current_browser or not blueprint_name:
            logger.error('Parameter passed to filter_blueprint:current_brower'
                         ' or blueprint_name is None.')
            return None

        logger.debug('Navigating to blueprint filter page.')
        _browser = current_browser.instance._browser.current
        _browser.switch_to.default_content()
        iaas_gadget_frame_id = self.get_accurate_frameid(current_browser,
                                                         self.url_iaas_gadget)
        _browser.switch_to.frame(iaas_gadget_frame_id)
        logger.debug(
            'Switched to iaas_gadget frame {}'.format(iaas_gadget_frame_id))

        if self.txt_blueprint_name.exists():

            # same issue as filter reservation.
            self.txt_blueprint_name.set('')
            print 'Cleared blueprint name text box'
            self.wait_for_loading_complete(2)
            self.txt_blueprint_name.set(blueprint_name)
            logger.info(
                'Input blueprint name {} to try to filter it out.'.format(
                    blueprint_name))
            self.wait_for_loading_complete(5)
        else:
            logger.error('Blueprint filter input textbox is not found.')
            return None

        # why a common filter clear item is not used???:(
        if self.lnk_blueprint_filters_clear.exists():
            logger.debug('Filter blueprint operation done.')
            first_item_found_blueprint = WebLink(
                xpath=self.blueprint_filter_result_first_element_xpath)
            if (
                    first_item_found_blueprint and
                    first_item_found_blueprint.exists() and
                    first_item_found_blueprint.text == blueprint_name):
                logger.info(
                    'blueprint {} is found and filtered.'.format(blueprint_name),
                    False, True
                )
                return first_item_found_blueprint

        logger.info('Blueprint {} is not found.'.format(blueprint_name), False, True)
        self.txt_blueprint_name.set('')
        return None

    def select_reservation_to_edit(self,
                                   current_browser,
                                   lnk_filtered_reservation_to_edit):
        return self.select_filtered_result_to_edit(
            current_browser,
            lnk_filtered_reservation_to_edit,
            self.lbl_reservation_edit_title
        )

    def select_blueprint_to_edit(self,
                                 current_browser,
                                 lnk_filtered_blueprint_to_edit):
        return self.select_filtered_result_to_edit(
            current_browser,
            lnk_filtered_blueprint_to_edit,
            self.lbl_blueprint_edit_title
        )

    def select_filtered_result_to_edit(self,
                                       current_browser,
                                       lnk_filtered_result_to_edit,
                                       lbl_target_to_edit_title):
        """
         Select a give Weblink of reservation to go to its edit page.
        Args:
            current_browser: The browser object passed between workflow context.
            lnk_filtered_result_to_edit: The weblink object returned by
                                        self.filter_reservation
            lbl_target_to_edit_title: The WebLabel object representing the title
                                      of the edit page of target.

        Returns: True if the given reservation edit page is navigated.

        """
        _browser = current_browser.instance._browser.current
        BasePage().wait_for_loading_complete(2)
        if not lnk_filtered_result_to_edit or not lbl_target_to_edit_title:
            return False

        filtered_result = \
            lnk_filtered_result_to_edit.text \
                if isinstance(lnk_filtered_result_to_edit, WebElement) else lnk_filtered_result_to_edit.current.text
        try:
            lnk_filtered_result_to_edit.click()
            logger.info('Selected filtered result {} to edit.'
                        .format(filtered_result), False, True)
            LoadingWindow().wait_loading(current_browser, 10)
            if lbl_target_to_edit_title.exists():
                logger.info('Navigated to:{} edit page'.format(filtered_result), False, True)

            _browser.switch_to.default_content()
            self.wait_for_loading_complete(2)
            iaas_gadget_frame_id = BasePage().get_accurate_frameid(
                current_browser, self.url_iaas_gadget)
            _browser.switch_to.frame(iaas_gadget_frame_id)
            logger.info(
                'Switched to iaas gadget frame, id:{}'.format(iaas_gadget_frame_id), False, True)

            reservation_details_1st_frame_id = BasePage().get_accurate_frameid(
                current_browser, self.infra_reservation_edit_frame_extensionid, False, attribute_name='extensionid')
            _browser.switch_to.frame(reservation_details_1st_frame_id)
            logger.info('Switched to reservation details first frame, id:{}'.format(
                reservation_details_1st_frame_id), False, True)

            # Benson: We have chance that the iframe for com.vmware.vcac.iaas.reservation.details is
            # yet initialized, this iframe resides under div[@class="dialogContent"], So we add code
            # to to make sure div[@class="dialogContent"] is enabled already before taking further
            # actions.
            self.wait_for_loading_complete(wait_time=2)
            edit_page_dialog_content = WebLink(xpath='//div[@class="dialogContent"]')
            if edit_page_dialog_content.exists():
                logger.info('Reservation edit page edit content area exists.', False, True)
            else:
                logger.warn(
                    'Reservation edit page edit content area not found, following step of switching '
                    'to iframe:{} may fail..'.format(self.reservation_edit_detail_frame_extensionid)
                )

            reservation_details_2nd_frame_id = BasePage().get_accurate_frameid(
                current_browser, self.reservation_edit_detail_frame_extensionid,
                False, attribute_name='extensionid')
            _browser.switch_to.frame(reservation_details_2nd_frame_id)
            logger.info(
                'Switched to reservation details second frame, id:{}'.format(
                    reservation_details_2nd_frame_id), False, True)
            self.wait_for_loading_complete(1)

            return True
        except:
            logger.error(
                'Navigating to {} edit page failed'.format(filtered_result))
            return False

    def navigate_to_infrastructure(self, current_browser):
        _browser = current_browser.instance._browser.current
        is_infrastructure_flag = False
        try:
            _browser.switch_to.frame(None)
            is_infrastructure_flag = MainPage().btn_infrastructure.exists()
        except:
            pass

        if is_infrastructure_flag:
            MainPage().btn_infrastructure.click()
            logger.info(
                'Clicked inrastructure page button to try to navigate to '
                'infrastructure page.', False, True)
            self.wait_for_loading_complete(2)
            try:
                iaas_gadget_frame_id = self.get_accurate_frameid(
                    current_browser, self.url_iaas_gadget)
                _browser.switch_to.frame(iaas_gadget_frame_id)
                logger.info(
                    'Navigate to infrastructure page switched to iframe {}'
                    ''.format(iaas_gadget_frame_id))

                if self.btn_recent_events.exists():
                    is_infrastructure_flag = True
                    return is_infrastructure_flag

                if self.btn_anchor_infrastructure.exists():
                    is_infrastructure_flag = True
                    return is_infrastructure_flag

            except:
                is_infrastructure_flag = False
                logger.warn(
                    'Switching to infrastructure page iaas gadget frame '
                    'encounters exception: {}'.format(sys.exc_info()[:2]))

        return is_infrastructure_flag
