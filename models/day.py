from models.lession import Lessions

from mongoengine import *


class Days(Document):
    num = IntField(required=True, primary_key=True)
    name = StringField(max_length=30, required=True)
    lessions= ListField(EmbeddedDocumentField(Lessions))
