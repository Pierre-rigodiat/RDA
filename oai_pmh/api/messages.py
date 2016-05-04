################################################################################
#
# Class Name: messages
#
# Description:   Serializer for OAI-PMH Registries
#
# Author: Pierre Francois RIGODIAT
#         pierre-francois.rigodiat@nist.gov
#
################################################################################


class APIMessage:
    label = 'message'

    @staticmethod
    def getMessageLabelled(message):
        return {APIMessage.label: message}