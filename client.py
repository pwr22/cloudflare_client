# CloudFlare client API module

import requests
from upstream_error import UpstreamError

CF_URL = 'https://www.cloudflare.com/api_json.html'

# Specify object explicitly for Python 2 support
class Client (object):
    def __init__(self, email, token):
        '''Contruct a CloudFlare Client API object'''
        self.__user = email
        self.__key  = token

    def _makeCall(self, params):
        '''Calls through to the CF API with params provided'''
        # Splice in auth details, overriding existing
        params.update({ 'email' : self.__user, 'tkn' : self.__key})
        #TODO does requests raise on http errors?
        res = requests.post(CF_URL, data = params).json()
        if res['result'] == 'error':
            # err_code could be missing
            raise UpstreamError(res['msg'], res.get('err_code'))
        return res

    def __getattr__(self, callType):
        '''Overridden to auto create methods wrapping CF API actions'''
        # Generate wrapper
        def callFunc(self, **params):
            # Splice in the action, override anything existing
            params.update({ 'a' : callType })
            return self._makeCall(params)
        # Avoid unnecessary redefinitions by installing in class
        setattr(Client, callType, callFunc)
        # Accessed this way to turn into method
        # All these selfs because what if crazy inheritance?
        return type(self).__dict__[callType].__get__(self, type(self))
