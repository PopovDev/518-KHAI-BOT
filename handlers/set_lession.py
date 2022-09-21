from aiogram import Router
from aiogram.types import Message
import datetime

from models.day import Days
from models.day import Lessions

router = Router()


@router.message(commands=['setlession'])
async def message_with_text(message: Message):
    # day num
    _, day, num, title = message.text.split(' ')
    
    Day = Days.objects(num=int(day)).first()
    Day.lessions[int(num)].title = title
    Day.save()

    await message.answer("Ok", parse_mode="HTML")
