"""
API Client for OPAL applications
"""
import attrdict
import requests

class Error(Exception): pass
class OMGError(Error): pass

class OPALAttrDict(attrdict.AttrDict):

    def __repr__(self):
        as_string = '\nRecord: \n\n'
        as_string += '\n'.join('{0}:{1}'.format(key.rjust(25), self[key]) for key in self.keys())
        return as_string


def decide_whether_to_bail_for_response(response):
    """
    Inspect RESPONSE and raise a suitable error if required
    """
    if response.status_code != 200:
        msg = 'Unexpected status code from server: {0}'.format(
            response.status_code)
        raise OMGError(msg)

class APIGet(object):
    """
    Perform the actual work of GETing data from the API
    """

    def __init__(self, client):
        self.client = client

    def __getattr__(self, name):
        return self.get_resource_fn(name)

    def get_resource_fn(self, name):
        def get_resource(record_id=None):

            if record_id is None:
                if name == 'patient':
                    raise Error('Sorry, OPAL has no list patient API.')

            headers = {'Authorization': 'Token {0}'.format(self.client.token)}
            r = requests.get(
                self.client.record_url(name, record_id=record_id),
                headers=headers
            )
            decide_whether_to_bail_for_response(r)
            return OPALAttrDict(r.json())
        return get_resource


class Client(object):
    """
    Main API Client
    """

    def __init__(self, host, port, token):
        """
        Initialise the client with HOST, PORT and TOKEN.
        """
        self.host  = host
        self.port  = port
        self.token = token

    @property
    def base_url(self):
        """
        Return the base server url as a string
        """
        return 'http://{0}:{1}'.format(self.host, self.port)

    def record_url(self, name, record_id=None):
        """
        Return the API URL for the record named NAME.
        If we pass in RECORD_ID, retrieve an individual record
        """
        if record_id is None:
            return '{0}/api/v0.1/{1}/'.format(self.base_url, name)
        return '{0}/api/v0.1/{1}/{2}/'.format(self.base_url, name, record_id)

    @property
    def get(self):
        """
        Proxy for GET requests to the API
        """
        return APIGet(self)
