from mongoengine import *


class Lessions(EmbeddedDocument):
    empty = BooleanField(default=True)
    title = StringField(max_length=100, required=False)
    teacher = StringField(max_length=100, required=False)
    link_platform = StringField(max_length=100, required=False)
    link = StringField(max_length=200, required=False)