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

from robot.api import logger

from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.reusable import PageNavigator
from ehc_e2e.auc.reusable import RequestManager
from ehc_e2e.auc.reusable import LoadingPopupWaiter
from ehc_e2e.auc.uimap.specific.rp4vm import CatalogPage
from ehc_e2e.auc.uimap.specific.rp4vm import PostFailoverSyncPage
from ehc_e2e.utils.service import RESTWrapper


class VRPAProtectedVMsManager(BaseUseCase):
    class Func(object):
        FAILOVER, RECOVER_PRODUCTION, POST_FAILOVER_SYNC = (
            'test_vrpa_failover',
            'test_vrpa_recover_production',
            'test_rp4vm_post_failover_sync'
        )

    def __init__(self, name=None, method_name=Func.FAILOVER, **kwargs):
        super(VRPAProtectedVMsManager, self).__init__(
            name, method_name, **kwargs)

    def tearDown(self):
        if self._testMethodName == self.Func.POST_FAILOVER_SYNC:
            RequestManager(self).save_unsubmitted_request()

    def test_vrpa_failover(self):
        self._enable_image_access()
        self._check_image_access_status()
        self._failover()

    def test_vrpa_recover_production(self):
        raise NotImplementedError('Placeholder - Recover Production')

    def test_rp4vm_post_failover_sync(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._submit_request()

    def _enable_image_access(self):
        _formatter = 'Running on step: "{step}" - FAILED ' \
                     '(reason:{reason})'.format

        _copies_res_loc = 'groups/{gid}/clusters/{cid}/copies/{copyid}'.format(
            gid=self.cg_id, cid=self.cluster_id, copyid=self.copy_id)

        # _snapshots_res_loc = _copies_res_loc + '/snapshots'
        # _snapshots_request = self.vrpa_client.get(_snapshots_res_loc)
        # self.assertTrue(
        #     _snapshots_request.ok,
        #     msg=_formatter(step='GET snapshots',
        #                    reason=_snapshots_request.reason))
        #
        # _snapshots_model = RESTWrapper.decode(_snapshots_request.text)
        # self.assertTrue(
        #     hasattr(_snapshots_model, 'snapshots'),
        #     msg=_formatter(step='Get all snapshots',
        #                    reason='No "snapshots" attribute'))
        #
        # snapshot = None
        # for snapshot in iter(_snapshots_model.snapshots):
        #     if _snapshots_model.latest.timeInMicroSeconds == \
        #             snapshot.closingTimeStamp.timeInMicroSeconds:
        #         break
        #
        # _image_access_res_loc = _copies_res_loc + '/enable_image_access'
        # _image_access_params = '{"snapshot":' + RESTWrapper.encode(snapshot) + \
        #                        ', "mode": "LOGGED_ACCESS", "scenario": "FAILOVER"}'
        # _enable_image_access_request = self.vrpa_client.put(
        #     _image_access_res_loc, _image_access_params)
        # self.assertTrue(
        #     _enable_image_access_request.ok,
        #     msg=_formatter(step='PUT enable_image_access',
        #                    reason=_enable_image_access_request.reason))

        _latest_image_access_res_loc = _copies_res_loc + '/image_access/latest/enable'
        _latest_image_access_params = '{"mode": "LOGGED_ACCESS", "scenario": "FAILOVER"}'
        retry_count = 5
        counter = 1
        _enable_latest_image_access_request = self.vrpa_client.put(
            _latest_image_access_res_loc, _latest_image_access_params)
        logger.debug('Response from {} is: {}.'.format(_latest_image_access_res_loc,
                                                       _enable_latest_image_access_request))
        while not _enable_latest_image_access_request.ok and retry_count >= 0:
            time.sleep(60)
            logger.debug(
                'Error reason for {}th call: "{}"'.format(counter, _enable_latest_image_access_request.reason))
            logger.warn('Retry {} attempts for requesting: "{}".'.format(counter + 1, _latest_image_access_res_loc))
            _enable_latest_image_access_request = self.vrpa_client.put(
                _latest_image_access_res_loc, _latest_image_access_params)
            logger.debug(
                'Response body for {}th call from {} is: "{}".'.format(
                    counter + 1, _latest_image_access_res_loc, _enable_latest_image_access_request))
            counter += 1
            retry_count -= 1

        self.assertTrue(
            _enable_latest_image_access_request.ok,
            msg=_formatter(step='PUT image_access/latest/enable',
                           reason=_enable_latest_image_access_request.reason))

    def _check_image_access_status(self):
        _formatter = 'Running on step: "{step}" - FAILED ' \
                     '(reason:{reason})'.format

        _copies_res_loc = 'groups/{gid}/clusters/{cid}/copies/{copyid}'.format(
            gid=self.cg_id, cid=self.cluster_id, copyid=self.copy_id)
        _settings_rec_loc = _copies_res_loc + '/settings'

        _settings_model = None
        timeout_in_sec = 60
        _now = time.time()
        while timeout_in_sec > (time.time() - _now):
            try:
                _settings_request = self.vrpa_client.get(_settings_rec_loc)
                logger.debug('Response from {} is: {}.'.format(_settings_rec_loc, _settings_request))
                _settings_model = RESTWrapper.decode(_settings_request.text)
                if hasattr(_settings_model, 'imageAccessInformation') and \
                            getattr(_settings_model.imageAccessInformation, 'imageAccessEnabled', None):
                    # Internal synchronization takes time for image accessing
                    time.sleep(60)
                    break
            except Exception as ex:
                logger.debug(ex.message)
                logger.info('Getting response from {} failed, try again.'.format(_settings_rec_loc))
            time.sleep(5)
            logger.debug('Waiting for another 5 seconds for imageAccessInfo synchronization done.')

        self.assertTrue(
            _settings_request.ok,
            msg=_formatter(step='GET settings',
                           reason=_settings_request.reason))

        self.assertTrue(
            _settings_model.imageAccessInformation.imageAccessEnabled,
            msg=_formatter(step='Validate image access status',
                           reason='Timed out'))

    def _failover(self):
        _formatter = 'Running on step: "{step}" - FAILED ' \
                     '(reason:{reason})'.format

        _cg_rec_loc = 'groups/{gid}'.format(gid=self.cg_id)
        _copies_res_loc = 'groups/{gid}/clusters/{cid}/copies/{copyid}'.format(
            gid=self.cg_id, cid=self.cluster_id, copyid=self.copy_id)

        _settings = RESTWrapper.decode(self.vrpa_client.get(
            _copies_res_loc + '/settings').text)
        _msg = 'Starting failover process:\n\t'
        _msg += 'Copy Name:\t{name}\n\tRole:\t\t{role}'.format(
            name=_settings.name, role=_settings.roleInfo.role)
        logger.info(_msg, False, True)

        _failover_rec_loc = _copies_res_loc + '/failover'
        _failover_request = self.vrpa_client.put(_failover_rec_loc)
        _retry_failover_count = 1
        while not _failover_request.ok and _retry_failover_count < 5:
            time.sleep(15)
            logger.debug(
                'Response from last request for {} was not OK, reason: {}.'.format(
                    _failover_rec_loc, _failover_request.reason + '[' + _failover_request.content + ']'))

            _failover_request = self.vrpa_client.put(_failover_rec_loc)
            logger.debug('Resent put request for "{}" 15 seconds after last request.'.format(_failover_rec_loc))
            _retry_failover_count += 1

        self.assertTrue(
            _failover_request.ok,
            msg=_formatter(step='PUT failover',
                           reason=_failover_request.reason + '[' + _failover_request.content + ']'))
        time.sleep(5)

        _start_cg_transfer_rec_loc = _cg_rec_loc + '/start_transfer'
        _start_cg_transfer_request = self.vrpa_client.put(_start_cg_transfer_rec_loc)
        _retry_transfer_count = 1
        while not _start_cg_transfer_request.ok and _retry_transfer_count < 5:
            time.sleep(15)
            logger.debug(
                'Response from last request for {} was not OK, reason: {}.'.format(
                    _start_cg_transfer_rec_loc,
                    _start_cg_transfer_request.reason + '[' + _start_cg_transfer_request.content + ']'))

            _start_cg_transfer_request = self.vrpa_client.put(_start_cg_transfer_rec_loc)
            logger.debug('Resent put request for "{}" 15 seconds after last request.'.format(_start_cg_transfer_rec_loc))
            _retry_transfer_count += 1
        self.assertTrue(
            _start_cg_transfer_request.ok,
            msg=_formatter(step='PUT start_transfer',
                           reason=_start_cg_transfer_request.reason))
        time.sleep(60)

        _cg_info_rec_loc = _cg_rec_loc + '/information'
        _cg_info_request = self.vrpa_client.get(_cg_info_rec_loc)
        self.assertTrue(
            _cg_info_request.ok,
            msg=_formatter(step='GET information',
                           reason=_cg_info_request.reason))

        _info_model = RESTWrapper.decode(_cg_info_request.text)
        self.assertTrue(
            _info_model.enabled,
            msg=_formatter(step='Validate consistency group status',
                           reason='Invalid status'))
        self.assertEqual(
            _info_model.productionCopiesUID[0].globalCopyUID.clusterUID.id,
            self.cluster_id,
            msg=_formatter(step='Validate production cluster',
                           reason='Production cluster is incorrect'))

        _settings = RESTWrapper.decode(self.vrpa_client.get(
            _copies_res_loc + '/settings').text)
        _msg = 'Finalizing failover process:\n\t'
        _msg += 'Copy Name:\t{name}\n\tRole:\t\t{role}'.format(
            name=_settings.name, role=_settings.roleInfo.role)
        logger.info(_msg, False, True)

    def _start_new_service_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        PageNavigator(self).go_to_catalog_page()
        _catalog_page = CatalogPage()

        with _catalog_page.frm_catalog:
            _catalog_page.lnk_ehc_recoverpoint_for_vms.click()

            self.assertTrue(
                _catalog_page.btn_RP4VM_post_failover_request.exists(),
                msg=_formatter(
                    step='Validate Request button of RP4VM Post Failover Synchronization')
            )

            _catalog_page.btn_RP4VM_post_failover_request.click()

    def _fill_out_request_info(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self._request_page.frm_catalog:
            self.assertTrue(
                self._request_page.txt_description.exists(60),
                msg=_formatter(step='Display Description text box')
            )

            self._request_page.txt_description.set(self._testMethodName)
            self._request_page.txt_reasons.set(self._name)
            self._request_page.btn_next.click()

    def _submit_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self._request_page.frm_catalog:
            self.assertTrue(self._request_page.cbo_confirm.exists(),
                            msg=_formatter(step='Confirm to post failover.'))
            self._request_page.cbo_confirm.select(by_visible_text='Confirm')
            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(self._request_page.btn_submit.exists(),
                            msg=_formatter(step='Click submit button'))

            self._request_page.btn_submit.click()

        with self._request_page.frm_catalog:
            self.assertTrue(self._request_page.lbl_success_msg.exists(),
                            msg='Failed to submit request')
            self._request_page.btn_ok.click()

    def _validate_input_args(self, **kwargs):
        if self._testMethodName == self.Func.FAILOVER:
            self.__validate_args_of_failover(**kwargs)
        elif self._testMethodName == self.Func.POST_FAILOVER_SYNC:
            self._request_page = PostFailoverSyncPage()
            self.wait_loading = LoadingPopupWaiter(
                self, browser=kwargs['browser'].instance._browser)
        else:
            raise ValueError('Unsupported test method')

    def __validate_args_of_failover(
            self, hostname_ip_adds, port, username, password,
            cg_name, cluster_name='', copy_name=''):
        assert hostname_ip_adds, 'Please provide host ip'
        assert port, 'Please provide port'
        assert username, 'Please provide username'
        assert password, 'Please provide password'

        self.vrpa_client = self.__create_vrpa_api_client(
            hostname_ip_adds, port, username, password)

        if not self.__validate_vrpa_state(self.vrpa_client):
            self.vrpa_client.close()
            self.fail("Unable to get vRPA state")

        if not self.__validate_cg_info_within_global_settings(
                self.vrpa_client, cg_name, cluster_name, copy_name):
            self.vrpa_client.close()
            self.fail('Unable to get group info within global settings')

        copies = self.__get_valid_copies_by_names(
            self.vrpa_client, cg_name, cluster_name, copy_name)

        if not copies:
            self.vrpa_client.close()
            self.fail('Failed to find valid consistency group copy')

        self.cg_id = copies[0].groupUID.id
        self.cluster_id = copies[0].globalCopyUID.clusterUID.id
        self.copy_id = copies[0].globalCopyUID.copyUID

    def __create_vrpa_api_client(
            self, host, port, username, password):
        _scheme = 'https' if port in (443, '443') else 'http'
        _netloc = '{host}:{port}'.format(host=host, port=port)
        _path = 'fapi/rest/4_3_1/'
        _base_url = '{scheme}://{netloc}/{path}'.format(
            scheme=_scheme, netloc=_netloc, path=_path)

        return RESTWrapper(_base_url, username, password)

    def __validate_vrpa_state(self, proxy):
        return proxy.get('state').ok

    def __validate_cg_info_within_global_settings(
            self, proxy, cg, cluster='', copy=''):
        _settings = proxy.get('settings')
        if _settings.ok:
            logger.info('Response from "settings", result:"{}".'.format(_settings.status_code), False, True)
            logger.debug('Response settings.content is:{}'.format(_settings.content))

        return False if not _settings.ok else \
            _settings.content and (cg.lower() in _settings.content.lower()) \
            and (cluster in _settings.content) and (copy in _settings.content)

    def __get_valid_copies_by_names(self, proxy, cg_name, cluster_name='', copy_name=''):
        _valid_copies = []

        try:
            for group in iter(RESTWrapper.decode(proxy.get(
                    'groups').text).innerSet):
                logger.debug('innerSet of response from "groups" is: {}'.format(group))
                if cg_name.lower() == RESTWrapper.decode(proxy.get(
                        'groups/{gid}/name'.format(
                            gid=group.id)).text).string.lower():
                    copies = RESTWrapper.decode(proxy.get(
                        'groups/{gid}/copies/settings'.format(
                            gid=group.id)).text).innerSet
                    logger.info(
                        'innerSet of response from {} is: {}.'.format(
                            'groups/{gid}/copies/settings'.format(gid=group.id), copies
                        )
                    )
                    _valid_copies = [copy.copyUID for copy in copies if (
                        copy.roleInfo.role == 'REPLICA') and copy.enabled]
                    break

            if copy_name:
                _valid_copies = [copy for copy in _valid_copies if (
                    copy_name == RESTWrapper.decode(proxy.get(
                        'groups/{gid}/clusters/{cid}/copies/{cpid}/name'.format(
                            gid=copy.groupUID.id,
                            cid=copy.globalCopyUID.clusterUID.id,
                            cpid=copy.globalCopyUID.copyUID
                        )).text).string)]

            if cluster_name:
                _valid_copies = [copy for copy in _valid_copies if (
                    cluster_name == RESTWrapper.decode(proxy.get(
                        'clusters/{cid}/name'.format(
                            cid=copy.globalCopyUID.clusterUID.id
                        )).text).string)]
        except:
            pass

        return _valid_copies
