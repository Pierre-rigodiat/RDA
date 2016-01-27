################################################################################
#
# File Name: models.py
# Application: Informatics Core
# Description:
#
# Author: Marcus Newrock
#         marcus.newrock@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################
from mongoengine import StringField, Document, URLField, DictField

class Registry(Document):
    """
        A registry object
    """
    name           = StringField(required=True, unique=True)
    url            = URLField(required=True)
    harvestrate    = StringField(required=False)
    metadataprefix = StringField(required=False)
    identity       = DictField(required=False)
    sets           = DictField(required=False)
    description    = StringField(required=False)

class Record(Document):
    """
        A record object
    """
    content = DictField(required=True)

class Identity(Document):
    """
        An identity object
    """
    content = DictField(required=True)

class Sets(Document):
    """
        A set object
    """
    content = DictField(required=True)

class UpdateRecord(Document):
    """
        A record object
    """
    identifier = StringField(required=True)
    content = DictField(required=True)

class DeleteRecord(Document):
    """
        Delete record model
    """
    identifier = StringField(required=True)

class SelectRecord(Document):
    """
        A record object
    """
    identifier = StringField(required=True)

class UpdateRegistry(Document):
    """
        A registry object
    """
    name           = StringField(required=True, unique=True)
    url            = URLField(required=True)
    harvestrate    = StringField(required=False)
    metadataprefix = StringField(required=False)
    identity       = DictField(required=False)
    sets           = DictField(required=False)
    description    = StringField(required=False)
    identifier     = StringField(required=True)

class DeleteRegistry(Document):
    """
        Delete registry model
    """
    name = StringField(required=True)