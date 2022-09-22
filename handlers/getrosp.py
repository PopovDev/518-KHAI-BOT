from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton,CallbackQuery
import datetime
from aiogram.utils.keyboard import InlineKeyboardBuilder
from models.day import Days

router = Router()


@router.message(commands=['getrosp'])
async def message_with_text(message: Message):
    day = datetime.datetime.today().weekday()
    td = Days.objects(num=day).first()
    print(td)
    msg = f"День: <b>{td.name}</b>\n"
    for i in range(4):
        msg += f"<b>{i+1}</b> {td.lessions[i].title}\n"

    builder = InlineKeyboardBuilder()
    # buttons for lessions with title and callback_data
    for i in range(4):
        builder.add(InlineKeyboardButton(
            text=f"{i+1}", callback_data=f'lession:{day}@{i}'))
    # buttons for days with title and callback_data

    builder.row()

    await message.answer(msg, parse_mode="HTML", reply_markup=builder.as_markup())

@router.callback_query(lambda callback_query: callback_query.data.startswith('lession:'))
async def send_random_value(callback: CallbackQuery):
    
    day, num = callback.data.split(':')[1].split('@')

    await callback.message.answer(f"Вы выбрали {int(num)+1} пару")
    await callback.answer()
    await callback.message.delete_reply_markup()
