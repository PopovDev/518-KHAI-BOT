from models.day import Days
from datetime import datetime, time
import pytz

EDIT_MODE = {
    'mode': True
}

TIMES_DEF = {
    1: (time(8, 00), time(9, 35)),
    2: (time(9, 50), time(11, 25)),
    3: (time(11, 55), time(13, 30)),
    4: (time(13, 45), time(15, 20))}


def format_rosp(day_num):
    day = Days.objects(num=day_num).first()
    nomin = get_nomitaror_denomitaror()
    ntext = 'Чис' if not nomin else 'Знам'
    text = f"Расписание на <b>{day.name} ({ntext})</b>:\n\n"

    for i, (l1, l2) in enumerate(day.lessions):
        num = f"<b>{i+1}.</b> "
        is_now = ""
        if get_now()[0] == day_num and get_now()[1] >= TIMES_DEF[i+1][0] and get_now()[1] <= TIMES_DEF[i+1][1]:
            is_now = "🔥"
        text += f"{num} {TIMES_DEF[i+1][0].strftime('%H:%M')} - {TIMES_DEF[i+1][1].strftime('%H:%M')}:"

        if l1.empty and l2.empty:
            text += f"  <b>Нет пар</b>\n"
        elif l1.empty or l2.empty:
            l = l1 if not l1.empty else l2
            text += f"\n>    {l.title} {is_now}\n"
        else:
            if (nomin):
                text += f"\n> Ч: {l1.title}\n> З: <u><b>{l2.title}</b></u> {is_now}\n"
            else:
                text += f"\n> Ч: <u><b>{l1.title}</b></u> {is_now}\n> З: {l2.title}\n"
        text += "\n"

    return text


def format_lession(day_num, num, n, headless=False):
    day = Days.objects(num=day_num).first()
    lession = day.lessions[num][n]
    text = ""
    if not headless:
        text += f"День: <b>{day.name}</b>\n"
        text += f"Лекция <b>{num+1}</b>:\n\n"
    text += f"<b>{lession.title}</b>\n\n"
    text += f"Преподаватель: <b>{lession.teacher}</b>\n\n"
    text += f"Платформа лекции: <b>{lession.link_platform}</b>\n\n"
    text += f"Ссылка на лекцию: <b>{lession.link}</b>\n\n"

    return text


def get_now():
    tz = pytz.timezone('Europe/Kiev')
    now = datetime.now(tz)
    return now.weekday(), now.time()


def get_nomitaror_denomitaror():
    tz = pytz.timezone('Europe/Kiev')
    now = datetime.now(tz)
    return 1 if (now.isocalendar()[1]) % 2 == 0 else 0
