# CloudFlare client API module

import requests

CF_URL = 'https://www.cloudflare.com/api_json.html'

class Client:
    def __init__(self, email, token):
        '''Contruct a CloudFlare Client API object'''
        self.__user = email
        self.__key  = token

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

    def _makeCall(self, params):
        '''Calls through to the CF API with params provided'''
        # Splice in auth details, overriding existing
        params.update({ 'email' : self.__user, 'tkn' : self.__key})
        res = requests.post(CF_URL, data = params).json()
        #TODO handle errors
        return res
