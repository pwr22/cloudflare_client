class UpstreamError (Exception):
    def __init__(self, message, errorCode = None):
        self.__message   = message
        self.__errorCode = errorCode
    def __str__(self):
        return 'Code: {0} Message: {1}'.format(self.__errorCode, self.__message)
