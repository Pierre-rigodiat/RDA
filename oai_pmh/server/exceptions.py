class OAIExceptions(Exception):
    def __init__(self, errors):
        self.message = 'Error'
        self.code = 'OAIExceptions'
        self.errors = errors

    def __str__(self):
        return self.errors

class OAIException (Exception):
    def __init__(self):
        self.message = 'Error'
        self.code = 'OAIException'

    def __str__(self):
        return repr(self.message)

class badArgument(OAIException):
    def __init__(self):
        self.message = 'The request includes illegal arguments, is missing required arguments, includes a repeated' \
                       ' argument, or values for arguments have an illegal syntax.'
        self.code = 'badArgument'

class badResumptionToken(OAIException):
    def __init__(self, resumptionToken):
        self.message = 'The value of the resumptionToken argument (%s) is invalid or expired.' %resumptionToken
        self.code = 'badResumptionToken'

class badVerb(OAIException):
    def __init__(self, message):
        self.message = message
        self.code = 'badVerb'

class cannotDisseminateFormat(OAIException):
    def __init__(self, metadataPrefix):
        self.message = 'The metadata format identified by the value given for the metadataPrefix argument' \
                       ' (%s) is not supported by the item or by the repository.' % metadataPrefix
        self.code = 'cannotDisseminateFormat'

class idDoesNotExist(OAIException):
    def __init__(self, identifier):
        self.message = 'The value of the identifier argument (%s) is unknown or illegal in this repository.' %identifier
        self.code = 'idDoesNotExist'

class noRecordsMatch(OAIException):
    def __init__(self):
        self.message = 'The combination of the values of the from, until, set and metadataPrefix arguments ' \
                       'results in an empty list.'
        self.code = 'noRecordsMatch'

class noMetadataFormat(OAIException):
    def __init__(self):
        self.message = 'There are no metadata formats available for the specified item.'
        self.code = 'noMetadataFormat'

class noSetHierarchy(OAIException):
    def __init__(self):
        self.message = 'The repository does not support sets.'
        self.code = 'noSetHierarchy'
