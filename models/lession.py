from math import fabs
from mongoengine import *


class Lessions(EmbeddedDocument):
    title = StringField(max_length=100, required=True)
    link = StringField(max_length=100, required=False)
    