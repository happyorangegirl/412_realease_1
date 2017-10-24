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
import xml.etree.ElementTree as cET
from robot.api import logger
from ehc_e2e.utils.service import SoapWrapper


class SrmClient(SoapWrapper):
    def __init__(self, hostname, username, password, domain=None):
        super(SrmClient, self).__init__(
            'https://{}:9086/vcdr/extapi/sdk'.format(hostname),
            username, password, domain)

        self.ns_prefix = 'srm'
        self.ns_uri = '{urn:srm0}'
        self.default_param = '<srm:_this type="SrmServiceInstance">SrmServiceInstance</srm:_this>'
        self.soap_env = """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:srm="urn:srm0">
            <soapenv:Body>
                <srm:{op}>
                    {params}
                </srm:{op}>
            </soapenv:Body>
        </soapenv:Envelope>
        """
        self.soap_header = {
            'Content-Type': 'text/xml;charset=UTF-8',
            'SOAPAction': 'urn:srm0/4.0'}

    def __enter__(self):
        _params = """
        <{prefix}:_this type="SrmServiceInstance">SrmServiceInstance</{prefix}:_this>
        <{prefix}:username>{username}</{prefix}:username>
        <{prefix}:password>{password}</{prefix}:password>
        """.format(prefix=self.ns_prefix,
                   username=self.session.credential.username,
                   password=self.session.credential.password)

        try:
            self.session.headers.update(self.soap_header)
            _request = self.post(self.soap_env.format(
                op='SrmLoginLocale', params=_params))

            if not _request.ok:
                fault = cET.fromstring(_request.text).find('.//faultstring').text
                if 'AlreadyLoggedInFault' in fault:
                    pass
                else:
                    raise RuntimeError(fault)
        except Exception as ex:
            if self.session:
                self.session.close()

            raise ex
        else:
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            try:
                _request = self.post(self.soap_env.format(
                    op='SrmLogoutLocale', params=self.default_param))

                if not _request.ok:
                    raise RuntimeError(cET.fromstring(_request.text).find('.//faultstring').text)
            finally:
                self.session.close()

    def open(self):
        self.__enter__()

    def close(self):
        self.__exit__(None, None, None)

    def start(self, moref, mode):
        mode_enums = ('test', 'cleanupTest', 'failover', 'migrate', 'reprotect', 'revert')

        if mode not in mode_enums:
            logger.error(msg='Invalid Recovery Mode, mode shoulb be in {}'.format(mode_enums))
            return False

        _params = """
        <{prefix}:_this type="SrmRecoveryPlan">{moref}</{prefix}:_this>
        <{prefix}:mode>{mode}</{prefix}:mode>
        """.format(prefix=self.ns_prefix, moref=moref, mode=mode)

        try:
            _request = self.post(self.soap_env.format(op='Start', params=_params))
            logger.info(msg='For response of request {mode}, status_code is {status_code}, text is {text}'.
                        format(mode=mode, status_code=_request.status_code, text=_request.text))
            if not _request.ok:
                logger.error(msg='The response  status code of {mode} is {status_code}'.
                             format(mode=mode, status_code=_request.status_code))
                return False
            return True
        except:
            logger.error(msg='Encounter error when post request {0}, details info: {1}'.
                         format(mode, sys.exc_info()))
            return False

    def cancel(self, moref):
        _params = """
        <{prefix}:_this type="SrmRecoveryPlan">{moref}</{prefix}:_this>
        """.format(prefix=self.ns_prefix, moref=moref)

        try:
            self.post(self.soap_env.format(op='Cancel', params=_params))
        except:
            pass

    def get_site_name(self):
        site_name = 'unknown'

        _request = self.post(self.soap_env.format(
            op='GetSiteName', params=self.default_param))

        if _request.ok:
            site_name = cET.fromstring(_request.text).find(
                './/{}returnval'.format(self.ns_uri)).text

        return site_name

    def get_paired_site_name(self):
        site_name = 'unknown'

        _request = self.post(self.soap_env.format(
            op='GetPairedSite', params=self.default_param))

        if _request.ok:
            site_name = cET.fromstring(_request.text).find(
                './/{}name'.format(self.ns_uri)).text

        return site_name

    def get_recovery_plans(self):
        recovery_plans = {}

        _request = self.post(self.soap_env.format(
            op='ListPlans',
            params='<{prefix}:_this type="SrmRecovery">SrmRecovery</{prefix}:_this>'.format(
                prefix=self.ns_prefix)))
        if _request.ok:
            for plan in cET.fromstring(_request.text).findall(
                    './/{}returnval'.format(self.ns_uri)):
                _request = self.post(self.soap_env.format(
                    op='RecoveryPlanGetInfo',
                    params='<{prefix}:_this type="SrmRecoveryPlan">{moref}</{prefix}:_this>'.format(
                        prefix=self.ns_prefix, moref=plan.text)))

                if _request.ok:
                    _retval_node = cET.fromstring(_request.text).find(
                        './/{}returnval'.format(self.ns_uri))

                    _name = _retval_node.find('.//{}name'.format(self.ns_uri)).text
                    _state = _retval_node.find('.//{}state'.format(self.ns_uri)).text
                    _groups = [gp.text for gp in _retval_node.findall(
                        './/{}protectionGroups'.format(self.ns_uri))]

                    recovery_plans[_name] = dict(moref=plan.text, state=_state, groups=_groups)

        return recovery_plans

    def get_recovery_state_of_recovery_plan(self, moref):
        state = 'unknown'

        _params = """
        <{prefix}:_this type="SrmRecoveryPlan">{moref}</{prefix}:_this>
        """.format(prefix=self.ns_prefix, moref=moref)

        _request = self.post(self.soap_env.format(
            op='RecoveryPlanGetInfo', params=_params))

        if _request.ok:
            state = cET.fromstring(_request.text).find(
                './/{}state'.format(self.ns_uri)).text
        else:
            logger.error(msg='For response of RecoveryPlanGetInfo request, '
                             'status_code is {status_code}, text is {text}'.
                         format(status_code=_request.status_code, text=_request.text))
        return state

    def get_peer_recovery_plan(self, moref):
        peer_moref = 'unknown'

        _params = """
        <{prefix}:_this type="SrmRecoveryPlan">{moref}</{prefix}:_this>
        """.format(prefix=self.ns_prefix, moref=moref)

        _request = self.post(self.soap_env.format(
            op='RecoveryPlanGetPeer', params=_params))

        if _request.ok:
            peer_moref = cET.fromstring(_request.text).find(
                './/{}plan'.format(self.ns_uri)).text

        return peer_moref

    def get_recovery_result(self, moref, length=1):
        recovery_result = []

        _params = """
        <{prefix}:_this type="SrmRecovery">SrmRecovery</{prefix}:_this>
        <{prefix}:plan type="SrmRecoveryPlan">{moref}</{prefix}:plan>
        """.format(prefix=self.ns_prefix, moref=moref)

        _request = self.post(
            self.soap_env.format(op='GetHistory', params=_params))

        if _request.ok:
            history_moref = cET.fromstring(_request.text).find(
                './/{}returnval'.format(self.ns_uri)).text

            _params = """
            <{prefix}:_this type="SrmRecoveryHistory">{moref}</{prefix}:_this>
            <{prefix}:length>{length}</{prefix}:length>
            """.format(prefix=self.ns_prefix, moref=history_moref, length=length)

            _request = self.post(
                self.soap_env.format(op='GetRecoveryResult', params=_params))

            if _request.ok:
                for result in cET.fromstring(_request.text).findall(
                        './/{}returnval'.format(self.ns_uri)):
                    _record = {}

                    for element in result.findall('.//*'):
                        _record[element.tag[self.ns_uri.__len__():]] = element.text

                    _record.pop('key')
                    _record.pop('plan')

                    recovery_result.append(_record)

        return recovery_result
