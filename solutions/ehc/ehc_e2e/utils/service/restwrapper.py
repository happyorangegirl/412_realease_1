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

import json
from urlparse import urljoin

from svcacore.restacore import ISession

from ehc_e2e.utils.context.model import YAMLData


class RESTWrapper(ISession):
    def __init__(self, base_url, username, password, domain=None):
        super(RESTWrapper, self).__init__(username, password, domain)

        self.base_url = base_url

    def get(self, res_location, **kwargs):
        url = urljoin(self.base_url, res_location)

        return super(RESTWrapper, self).get(url, **kwargs)

    def put(self, res_location, data=None, **kwargs):
        url = urljoin(self.base_url, res_location)

        return super(RESTWrapper, self).put(url, data, **kwargs)

    def post(self, res_location, data=None, json=None, **kwargs):
        url = urljoin(self.base_url, res_location)

        return super(RESTWrapper, self).post(url, data, json, **kwargs)

    def delete(self, res_location, **kwargs):
        url = urljoin(self.base_url, res_location)

        return super(RESTWrapper, self).delete(url, **kwargs)

    def _set_auth(self):
        super(RESTWrapper, self)._set_auth()
        self.headers['Content-Type'] = 'application/json'

    @staticmethod
    def decode(json_string):
        _model = YAMLData()
        try:
            _model = YAMLData(**json.loads(json_string))
        except:
            pass

        return _model

    @staticmethod
    def encode(model):
        def _unicode_encoder(data):
            _json = {}

            for key, value in data.__dict__.iteritems():
                if isinstance(value, YAMLData):
                    value = _unicode_encoder(value)

                _json[key] = value

            return _json

        if not isinstance(model, YAMLData):
            # Arbitrarily raise any potential exception
            return json.dumps(model)

        return json.dumps(_unicode_encoder(model))
