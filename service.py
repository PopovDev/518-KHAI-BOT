from models.day import Days
from datetime import datetime
import pytz


def format_rosp(day_num):
    day = Days.objects(num=day_num).first()
    nomin = get_nomitaror_denomitaror()
    ntext = 'Чис' if not nomin else 'Знам'
    text = f"Расписание на <b>{day.name} ({ntext})</b>:\n"
    for i, (l1, l2) in enumerate(day.lessions):
        num = f"<b>{i+1}.</b>"
        if l1.empty and l2.empty:
            text += f"{num} Нет пар\n"
        elif l1.empty or l2.empty:
            l = l1 if not l1.empty else l2
            text += f"{num} {l.title}\n"
        else:
            if (nomin):
                text += f"{num} ч: {l1.title}\n     з: <u><b>{l2.title}</b></u>\n"
            else:
                text += f"{num} ч: <u><b>{l1.title}</b></u>\n     з: {l2.title}\n"

    return text


def get_now_day():
    tz = pytz.timezone('Europe/Kiev')
    now = datetime.now(tz)
    return now.weekday()


def get_nomitaror_denomitaror():
    tz = pytz.timezone('Europe/Kiev')
    now = datetime.now(tz)
    return 1 if (now.isocalendar()[1]) % 2 == 0 else 0

