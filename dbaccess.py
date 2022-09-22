from mongoengine import *
from config import MONGO_STR

from models.day import Days

client = connect(host=MONGO_STR, db = 'KHAI_BOT')


def init_days():
    if Days.objects.count() !=5:
        Days(num=0, name='Понедельник').save()
        Days(num=1, name='Вторник').save()
        Days(num=2, name='Среда').save()
        Days(num=3, name='Четверг').save()
        Days(num=4, name='Пятница').save()

init_days()
