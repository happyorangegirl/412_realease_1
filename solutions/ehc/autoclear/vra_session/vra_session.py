from requests.sessions import Session
import requests
requests.packages.urllib3.disable_warnings()


class VRASession(Session):

    def __init__(self, host, tenant, username, password):
        super(VRASession, self).__init__()
        self.verify = False     # disable SSL
        self.host = host
        self.tenant = tenant

        _headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '}

        _body = {
            'username': username,
            'password': password,
            'tenant': tenant}

        _response = self.post(url='https://{host}/identity/api/tokens'.format(host=self.host),
                              headers=_headers, json=_body)

        if _response.status_code == 200:
            _headers['Authorization'] += _response.json()['id']
        else:
            raise RuntimeError('Failed to authenticate: ' + _response.json()['errors'][0]['systemMessage'])

        # save header to session
        self.headers.update(_headers)
