from aiogram import Router
from aiogram.types import Message
from dbaccess import state
import datetime

router = Router()


@router.message(commands=['getrosp'])
async def message_with_text(message: Message):
    day = datetime.datetime.today().weekday()
    td = state.days[day]
    msg = f"Сегодня: <b>{td.name}</b>\n"
    for i,g in enumerate(td.lessions):
        msg+=f"{i+1}. {g.name}\n"

    await message.answer(msg, parse_mode="HTML")
