from aiogram import Router
from aiogram.types import Message
import datetime

from models.day import Days

router = Router()


@router.message(commands=['getrosp'])
async def message_with_text(message: Message):
    day = datetime.datetime.today().weekday()
    td = Days.objects(num=day).first()
    print(td)
    msg = f"День: <b>{td.name}</b>\n"
    for i in range(4):
        msg += f"<b>{i}</b> {td.lessions[i].title}\n"

    await message.answer(msg, parse_mode="HTML")
