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

import sys
import time
from robot.api import logger
from uiacore.modeling.webui.controls import WebLabel, WebLink
from selenium.webdriver.remote.webdriver import WebDriver
from ehc_e2e.auc.uimap.extension import WebFrame
from ehc_e2e.entity import RequestDetailEntity
from .basepage import BasePage
from .mainpage import MainPage
from .requestdetailspage import RequestDetailsPage
from .loadingwindow import LoadingWindow
from ehc_rest_utilities.vra_rest_utilities.vra_rest_base import VRARestBase
from ehc_rest_utilities.session_manager.session_manager import VRASession
from ehc_e2e.auc.reusable.context_util import get_context, get_driver


class RequestsPage(BasePage):
    FINAL_RESULT_STATUS = ("Successful", "Failed", "Unsubmitted")

    def __init__(self, browser=None):
        super(RequestsPage, self).__init__()
        self.is_last_updated_sorted_positive = False
        self.browser = browser
        self.frm_requests = WebFrame(
            onload='request/RequestGadget.gadget.xml',
            extensionid='csp.catalog.request')

        self.lbl_request_page = WebLabel(xpath='//*[text()="Requests"]')
        self.lbl_request_data = WebLink(
            xpath='//table[@id="REQUESTS_TABLE_DATA"]/tbody[2]')
        self.lnk_request_title_last_updated = WebLink(
            xpath='//span[text()="Last Updated"]')
        self.request_data_request_id_xpath = './/td[@cellindex="0"]/div/a/b'
        self.request_data_item_xpath = './/td[@cellindex="1"]/div/div/span'
        self.request_data_description_xpath = './/td[@cellindex="2"]/div/div'
        self.request_data_cost_xpath = './/td[@cellindex="3"]/div/div'
        self.request_data_least_cost_xpath = './/td[@cellindex="4"]/div/div'
        self.request_data_status_xpath = './/td[@cellindex="5"]/div/div'
        self.request_data_submitter_xpath = './/td[@cellindex="6"]/div/div'
        self.request_data_submitted_xpath = './/td[@cellindex="7"]/div/div'
        self.request_data_last_updated_xpath = './/td[@cellindex="8"]/div/div'
        self.lbl_request_data_request_id = WebLabel(
            xpath='//td[@cellindex="0"]')
        self.url_self_request_gadget = \
            'https://com.vmware.csp.core.cafe.catalog.plugin.vproxy//request/RequestGadget.gadget.xml'
        self.xpath_loading = '//*[text()="Loading..."]'
        self.lnk_request_refresh = WebLink(xpath='//div[@id="REQUESTS_TABLE_REFRESH_ICON"]')
        self.xpath_btn_ok = './/*[@id="cancel"]'

    def get_request_link_by_id(self, request_id):
        return WebLink(xpath='//a[@title="{request_id}"]'.format(request_id=request_id))

    def retry_to_get_element_current(self, element_to_get, element_name, retry_counter=3, wait_interval_each_time=2):
        _current = element_to_get.current
        if not _current:
            for i in xrange(retry_counter):
                self.wait_for_loading_complete(wait_time=wait_interval_each_time)
                if element_to_get.exists():
                    _current = element_to_get.current
                    if _current:
                        return _current
                    else:
                        logger.warn(
                            'Retry in {} attempt to get current of element: {}, current is still None.'
                            .format(i+1, element_name))
                else:
                    logger.warn('Retry in {} attempt to get current of element: {}, element does not exist.'
                                .format(i+1, element_name))

            logger.warn('Retried {} times to get current of element: {}, failed to get current.'
                        .format(retry_counter, element_name))
        else:
            logger.debug('Getting current of element: {} succeeded.'.format(element_name), False)

        return _current

    def get_request_result_in_ui(
            self, selector_text, selector_xpath, timeout, slp, firstwaitduration, fuzzymatch=False,
            fuzzymatchstringlist=None):
        # get the current request in ui and return the request info
        logger.debug('Start to get current result in ui.')
        request_details_page = RequestDetailsPage()
        times = 0
        max_times = timeout / slp
        time.sleep(firstwaitduration)

        logger.info('Submiited request, start to get current request.', False, True)
        current_request = self.get_current_request(selector_xpath, selector_text, fuzzymatch, fuzzymatchstringlist)
        if current_request is not None:
            status = self.get_current_request_item_text(current_request, self.request_data_status_xpath)
            logger.debug('Done getting request item "status" text.')
        else:
            logger.warn('Cannot find current request in the Request table.')
            return None

        while status not in self.__class__.FINAL_RESULT_STATUS:
            logger.debug('Request is still in progress, Status is: {}'.format(status), False)
            time.sleep(slp)
            times += 1
            try:
                logger.debug(
                    'Try to get refresh button element.', False)
                if not self.retry_for_element_exists(self.lnk_request_refresh, 'refresh button in request page', 10, 3):
                    return None

                container = self.retry_to_get_element_current(self.lnk_request_refresh, 'refresh button', 10, 3)
                if not container:
                    return None

                self.lnk_request_refresh.click()
                self.wait_loading_for_request_refresh(container)

            except:
                logger.warn('Encounter exception in method: get_request_result_in_ui when clicking refresh button. '
                            'Error details: {}'.format(sys.exc_info()[:2]))
                return None

            logger.debug('Request table refresh is completed, start to get current request details.', False)
            current_request = self.get_current_request(selector_xpath, selector_text)
            if current_request is not None:
                status = self.get_current_request_item_text(current_request, self.request_data_status_xpath)
            else:
                logger.warn('Cannot find current request in the Request table.')
                return None

            if times > max_times:
                logger.warn('Wait so long time, but the status is not '
                            'Successful or Failed.')
                return None

        request_id = self.get_current_request_item_text(current_request, self.request_data_request_id_xpath)
        item = self.get_current_request_item_text(current_request, self.request_data_item_xpath)
        description = self.get_current_request_item_text(current_request, self.request_data_description_xpath)
        cost = self.get_current_request_item_text(current_request, self.request_data_cost_xpath)
        least_cost = self.get_current_request_item_text(current_request, self.request_data_least_cost_xpath)
        status = self.get_current_request_item_text(current_request, self.request_data_status_xpath)
        submitter = self.get_current_request_item_text(current_request, self.request_data_submitter_xpath)
        submitted = self.get_current_request_item_text(current_request, self.request_data_submitted_xpath)
        last_updated = self.get_current_request_item_text(current_request, self.request_data_last_updated_xpath)
        business_group = None
        status_details = None
        try:
            request_id_element = current_request.find_element_by_xpath(
                self.request_data_request_id_xpath)
            if request_id_element is None:
                logger.warn('Cannot get current request id in the request table.')
                return None
            request_id_element.click()
            logger.debug('The current request has been completed, Status: {}, '
                         'clicked request id to enter request details page.'.format(status))

            # wait until the loading window finishes running.
            BasePage().wait_for_loading_complete(2)
            current_browser = request_id_element.parent
            LoadingWindow().wait_loading(current_browser=request_id_element.parent, timeout=30)
        except:
            logger.warn('Encounter exception when clicking current request id and goto request details page. '
                        'Error details: {}'.format(sys.exc_info()[:2]))
            return None

        try:
            if current_browser:
                if not self.retry_for_element_exists_by_xpath(current_browser,
                                                              request_details_page.xpath_btn_ok,
                                                              'OK button in request details page', 10, 5):
                    return None
            else:
                if not self.retry_for_element_exists(request_details_page.btn_ok,
                                                     'OK button in request details page', 10, 5):
                    return None
            business_group = request_details_page.lbl_business_group_context.value
            # In PPGReen, UI changed, some requests can click status to get status detailss.
            # but some requests cannot click status, then set the status details 'No status details'

            container = self.retry_to_get_element_current(request_details_page.btn_ok,
                                                          'OK button in request details page', 10, 3)
            if not container:
                return None

            if BasePage.element_exists(request_details_page.lnk_status_result_xpath, container, 5):
                request_details_page.lnk_status_result.click()
                self.wait_for_loading_complete(2)
                if request_details_page.lbl_status_details_context.exists():
                    status_details = request_details_page.lbl_status_details_context.value
                    request_details_page.btn_ok_status_details_dialog.click()
            elif BasePage.element_exists(request_details_page.lbl_status_result_xpath, container, 5):
                status_details = 'No status details.'
            else:
                logger.warn('No status link and status label in the request details page.')
                return None
            self.wait_for_loading_complete(2)
            request_details_page.btn_ok.click()
            logger.debug('Get request status succeed. Clicked OK button to close request detail page.')

        except:
            logger.warn('Encounter exception when clicking ok button in request details page. '
                        'Error details: {}'.format(sys.exc_info()[:2]))
            return None

        request_detail_entity = RequestDetailEntity(
            request_id, item, description, cost, least_cost, submitter,
            submitted, last_updated, business_group, status, status_details)
        logger.info('Get current request succeed', False, True)
        return request_detail_entity

    def get_request_result_in_rest(self, key, value, timeout, slp, fuzzymatch=False, fuzzymatchstringlist=None):
        # Get request result in rest and return current request
        # TODO [BENSON]need to figureout the accurate vRA API query string for using item to filter.
        logger.debug('Start to get current request in rest.')
        if not (key and value):
            logger.error('The value of "key" or "value" is not provided in get_request_result_in_rest.')
            return None

        max_timeout = timeout
        wf_contect = get_context()
        _host_url = getattr(wf_contect.launch_browser, 'baseUrl')
        host = _host_url.replace('https://', '').replace('/vcac/org/', '')
        tenant = getattr(wf_contect.vra, 'tenant')
        vra_user = getattr(wf_contect.user_roles.Config_Admin, 'username')
        vra_pwd = getattr(wf_contect.user_roles.Config_Admin, 'password')
        logger.info('Host: {}, Tenant: {}, vra user: {}, vra password: {}'.format(
            host, tenant, vra_user, vra_pwd), False, True)
        vra_session = VRASession(host,
                                 tenant,
                                 vra_user,
                                 vra_pwd)

        vra = VRARestBase(vra_session)
        try:
            current_request_json = vra.get_current_request_by_filter(filter_key=key, filter_value=value)
            if not current_request_json:
                return None

            state_name = current_request_json.get('stateName')
            id = current_request_json.get('requestNumber')
            logger.info('Get current request, request id: {}'.format(id), False, True)
            # if request status is not in: ["Successful", "Failed", "Unsubmitted"], used request id to get request
            # and wait util status is in: ["Successful", "Failed", "Unsubmitted"]
            key = 'requestNumber'
            value = id
            while state_name not in self.__class__.FINAL_RESULT_STATUS and timeout > 0:
                current_request_json = vra.get_current_request_by_filter(filter_key=key, filter_value=value)
                time.sleep(slp)
                timeout -= slp
                if not current_request_json:
                    return None

                state_name = current_request_json.get('stateName')
                logger.debug('The current request state: {}'.format(state_name))

            if state_name in self.__class__.FINAL_RESULT_STATUS:
                detail_status = current_request_json.get('requestCompletion').get('completionDetails')
                request = RequestDetailEntity(request=str(id), status=state_name, status_details=detail_status)
                logger.info('Get current request succeed', False, True)
                return request

            if timeout <= 0:
                logger.warn('Wait {}, but the status is not in: {}'.format(max_timeout,
                                                                           self.__class__.FINAL_RESULT_STATUS))
                return None
        except:
            logger.warn('Encounter error when execute method: get_current_request_by_rest, '
                        'detail info: {}'.format(sys.exc_info()))
            return None

    def retry_for_element_exists(self, element, element_name, retry_counter=3, wait_interval_each_time=2):
        logger.debug('Retry to check existence for element:"{}"'.format(element_name if element_name else 'element'))
        try:
            for i in xrange(retry_counter):
                if self.browser:
                    try:
                        if self.navigate_to_request(self.browser):
                            logger.info(msg='navigate to request frame successful.')
                    except:
                        pass
                self.wait_for_loading_complete(wait_interval_each_time)
                if element.exists():
                    logger.debug('Element: {} "exists" succeeded after {} attempts.'.format(element_name, i+1), False)
                    return True
                else:
                    logger.warn(
                        'The {} attempt to check element: {} "exists" failed, continue new attempt.'.format(
                            i+1, element_name))

            logger.warn('Element: {} "exists" failed after {} attempts.'.format(element_name, retry_counter))
        except:
            logger.warn('Encounter error in retry_for_element_exists, detail info: {}'.format(sys.exc_info()))
        return False

    def retry_for_element_exists_by_xpath(self, driver, element_xpath,
                                          element_name, retry_counter=3, wait_interval_each_time=2):
        logger.debug('Using retry to check existence for element:"{}" xpath:"{}"'.format(element_name if element_name else 'element', element_xpath))
        try:
            for i in xrange(retry_counter):
                self.wait_for_loading_complete(wait_interval_each_time)
                element = driver.find_element_by_xpath(element_xpath)
                if element:
                    scroll_result = True if element.location_once_scrolled_into_view else False
                    logger.debug('Scrolled {} into view, no need to retry.'.format(element_name), False)
                    return scroll_result
                else:
                    logger.warn(
                        'The {} attempt to check element: {} "exists" failed, continue new attempt.'.format(
                            i + 1, element_name))
            snap_shot_file_name = time.strftime('%y_%m_%d_%H_%M_%S')
            from ehc_e2e.utils.snapshot import SnapShot
            SnapShot.takes_screen_shot(driver, 'retry_for_element_exists_by_xpath' + snap_shot_file_name)
            logger.warn('Element: {} "exists" failed after {} attempts.'.format(element_name, retry_counter))
        except:
            logger.warn('Encounter error in retry_for_element_exists_by_xpath, error info: {}'.format(sys.exc_info()))
        return False

    def get_current_request(self, selector_xpath, selector_text, fuzzy_match=False, fuzzy_match_string_list=None):
        if fuzzy_match and fuzzy_match_string_list:
            logger.debug(
                'Try to get current request, using fuzzy match strategy, match string list:{}'.format(
                    fuzzy_match_string_list)
            )
        else:
            logger.debug(
                'Try to get current request for selector_text:{}.'.format(selector_xpath, selector_text), False
            )
        if not self.retry_for_element_exists(self.lbl_request_data, 'request table', 2, 3):
            return None
        if not self.retry_for_element_exists(self.lbl_request_data_request_id, 'request id column', 2, 3):
            return None

        logger.debug('Start to get "current" of the request_data table element.', False)
        container = self.retry_to_get_element_current(self.lbl_request_data, 'request table', 2, 3)
        if not container:
            return None

        requests = container.find_elements_by_tag_name('tr')
        if len(requests) >= 2:
            # if there are more than two requests, compare the request
            # submitted date to judge whether they are sorted positive,
            # click two time to make it sorted positive
            # logger.debug(msg='Column sort positive.')
            try:
                if not self.is_last_updated_sorted_positive:
                    logger.debug(msg='Last updated column sort not positive.')
                    if not self.retry_for_element_exists(self.lnk_request_title_last_updated,
                                                         'last update title', 2, 3):
                        logger.warn('Column header "last update" does not exist.')
                        return None
                    logger.debug(msg='Try to click last updated column header twice.')
                    self.lnk_request_title_last_updated.click()
                    self.wait_loading_for_request_refresh(container)
                    self.lnk_request_title_last_updated.click()
                    logger.debug(msg='Clicked last updated column header twice.')
                    self.wait_loading_for_request_refresh(container)

                    logger.debug(
                        'After sorting request rows, try to get current of the request_data table element.', False)
                    container = self.retry_to_get_element_current(self.lbl_request_data, 'request table', 2, 3)
                    if not container:
                        return None

                    requests = container.find_elements_by_tag_name('tr')
                    self.is_last_updated_sorted_positive = True
            except:
                logger.warn(
                    'Encounter exception when sort last updated column. Error details: {}'.format(
                        sys.exc_info()[:2]))
                return None

            for request in requests:
                request_text_ui = request.find_element_by_xpath(selector_xpath).text
                if fuzzy_match and fuzzy_match_string_list:
                    if all(f in request_text_ui for f in fuzzy_match_string_list):
                        current_request = request
                        return current_request
                else:
                    if request.find_element_by_xpath(selector_xpath).text == \
                        selector_text:
                        current_request = request
                        return current_request
        elif len(requests) == 1:
            if requests[0].find_element_by_xpath(selector_xpath).text == \
                    selector_text:
                current_request = requests[0]
                return current_request
            else:
                logger.warn("The request doesn't exist in the Request "
                            "table list.")
                return None
        else:
            logger.warn("The Request table list is empty.")
            return None
        logger.warn("The request doesn't exist in the Request table list.")
        return None

    def get_current_request_item_id(self, descripton):
        current_request = self.get_current_request(self.request_data_description_xpath, descripton)
        if current_request:
            id_element = current_request.find_element_by_xpath(self.request_data_request_id_xpath)
            return id_element.text
        else:
            logger.warn('The request with description:"{}" not found, getting request id failed.'.format(descripton))
            return None

    def get_current_request_item_text(self, current_request, xpath):
        request = current_request.find_element_by_xpath(xpath).text
        return request

    def navigate_to_request(self, current_browser):
        _browser = current_browser if isinstance(current_browser,
                                                 WebDriver) else current_browser.instance._browser.current
        mainpage = MainPage()
        is_requests_flag = False
        try:
            _browser.switch_to.frame(None)
            if mainpage.btn_requests.exists():
                mainpage.btn_requests.click()
            else:
                print 'After switch default content, cannot find Request tab button.'
                logger.error('After switch default content, cannot find Request tab button.')
                return False

            self.wait_for_loading_complete(3)
            self_request_frame_id = self.get_accurate_frameid(current_browser,
                                                              self.url_self_request_gadget)
            if self_request_frame_id is not None:
                logger.debug('Found request frame: {}'.format(self_request_frame_id))
                _browser.switch_to.frame(self_request_frame_id)
                logger.debug('Switched to request frame: {}'.format(self_request_frame_id))
            else:
                logger.error('Looking for request frame failed.')
                return False

            if self.lbl_request_page.exists(10):
                is_requests_flag = True
        except:
            is_requests_flag = False

        return is_requests_flag

    def wait_loading_for_request_refresh(self, container, timeout=90):
        _loading_window = []
        try:
            container.parent.implicitly_wait(1)
            _loading_window = container.find_elements_by_xpath(
                self.xpath_loading)
            while len(_loading_window) > 0 and timeout > 0:
                # logger.debug('Waiting request refresh', False)
                time.sleep(3)
                timeout -= 3
                _loading_window = container.find_elements_by_xpath(
                    self.xpath_loading)
            if len(_loading_window) == 0:
                logger.debug('Request refresh done.', False)
            else:
                logger.error('Request refresh failed, loading exceeded timeout!')
        except:
            logger.error(
                'Encounter exception when request refresh. Error details: {}'.format(sys.exc_info()[:2]))
        finally:
            container.parent.implicitly_wait(30)

    def click_ok_or_cancel(self):
        # Try to check and click cancel or ok button to close detail page.
        # Xpath of Cancel and OK button: id="cancel". Texts in UI: Cancel, OK
        try:
            logger.debug(
                'Try to check if there is "OK" button in current UI and click it if it exists. '
                'otherwise take no action.')
            _browser = get_driver()
            if self.element_exists(self.xpath_btn_ok, _browser, 10):
                _browser.find_element_by_xpath(self.xpath_btn_ok).click()
                logger.debug('"OK" button exists, clicked it.')
            else:
                logger.debug('Did not find "OK" button, just skip clicking it.')
        except:
            logger.warn('Encounter error in check_ok_or_cancel, detail info: {}'.format(sys.exc_info()))

    def get_request_result(
            self, description=None, timeout=2500, item=None, slp=20, firstwaitduration=0, fuzzymatch=False,
            fuzzymatchstringlist=None):
        """
        Get the current request and return the request info,
        First get current request in UI, if failed to get request in UI will get current request by REST.
        :param description: to filter current request
        :param timeout: set the long time to wait the request result to failed or successful
        :param item: to filter current request
        :param slp: refresh interval, default value 20s
        :param firstwaitduration: set the wait time before getting request result the first.
                                  Specially for provision cloud
        :param fuzzymatch: indicate if you want the search to do a fuzzy match for string.
        :param fuzzymatchstringlist: the list of strings that the fuzzy match strategy will use. the strategy will
                                     check if all the givin strings are in the text when doing comparison.
        storage and deploy which time to get the request result may be long 1.5h, the slp for these two keywords will
        be 5 minutes in order to reduce the refresh times
        :return:  request object (from ehc_e2e.entity import RequestDetailEntity)
        """
        selector_xpath = None
        selector_text = None
        selector_key_in_rest = None
        if description is not None:
            selector_xpath = self.request_data_description_xpath
            selector_text = description
            selector_key_in_rest = 'description'

        if item is not None:
            selector_xpath = self.request_data_item_xpath
            selector_text = item
            selector_key_in_rest = 'catalog item'


        # Try to check and click cancel or ok button to close detail page.
        self.click_ok_or_cancel()

        request_result = self.get_request_result_in_ui(
            selector_text, selector_xpath, timeout, slp, firstwaitduration, fuzzymatch, fuzzymatchstringlist)
        if request_result:
            logger.debug('Getting request result from UI succeeded, returning request result.')
            return request_result
        else:
            logger.warn('Failed to get request result in ui.')

        from ehc_e2e.utils.snapshot import SnapShot
        SnapShot.takes_screen_shot(file_name='take_snapshot_before_get_request_result_in_rest')

        # Try to get request result in rest after failed to get request in ui and relaunch browser
        request_result = self.get_request_result_in_rest(
            selector_key_in_rest, selector_text, timeout, slp, fuzzymatch, fuzzymatchstringlist)
        if request_result:
            logger.debug('Getting request result from REST API succeeded, returning request result.')
            # Try to check and click cancel or ok button to close detail page.
            # Xpath of Cancel and OK button: id="cancel". Texts in UI: Cancel, OK
            self.click_ok_or_cancel()

            return request_result
        else:
            logger.warn('Failed to get request result in rest.')

        return None
