from models.day import Days
from datetime import datetime
import pytz

def format_rosp(day_num):
    day = Days.objects(num=day_num).first()
    text = f"Расписание на {day.name}:\n"
    for i,lession in enumerate(day.lessions):
        text += f"{i+1}. {lession.title}\n"
    return text

def get_now_day():
    tz = pytz.timezone('Europe/Kiev')
    now = datetime.now(tz)
    return now.weekday()