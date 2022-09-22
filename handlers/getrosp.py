from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
import datetime
from aiogram.utils.keyboard import InlineKeyboardBuilder
from models.day import Days
from service import format_lession, format_rosp, get_now

router = Router()


def get_keyboard(day_num, lessions):
    builder = InlineKeyboardBuilder()
    for i, (a, b) in enumerate(lessions):
        if (a.empty and b.empty):
            continue
        is_duo = not a.empty and not b.empty
        if not a.empty:
            txt = f"{i+1}"
            if is_duo:
                txt += ':ч'
            builder.add(InlineKeyboardButton(
                text=txt, callback_data=f"lession:{day_num}@{i}@0"))
        if not b.empty:
            txt = f"{i+1}"
            if is_duo:
                txt += ':з'
            builder.add(InlineKeyboardButton(
                text=txt, callback_data=f"lession:{day_num}@{i}@1"))

    builder.row()
    return builder.as_markup()


@router.message(commands=['getrosp'])
async def message_with_text(message: Message):
    day_num = get_now()[0]
    day = Days.objects(num=day_num).first()

    await message.answer(format_rosp(day_num), parse_mode='HTML', reply_markup=get_keyboard(day_num, day.lessions))


@router.callback_query(lambda callback_query: callback_query.data.startswith('lession:'))
async def open_lession(callback: CallbackQuery):

    day_num, lession_num, lession_type = map(
        int, callback.data.split(':')[1].split('@'))
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data=f'back:{day_num}')]
    ])

    text = format_lession(day_num, lession_num, lession_type)
    await callback.message.edit_text(text, parse_mode='HTML', reply_markup=back_keyboard)
    await callback.answer()


@router.callback_query(lambda callback_query: callback_query.data.startswith('back:'))
async def back(callback: CallbackQuery):
    day_num = int(callback.data.split(':')[1])
    lessions = Days.objects(num=day_num).first().lessions
    await callback.message.edit_text(format_rosp(day_num), parse_mode='HTML', reply_markup=get_keyboard(day_num, lessions))
    await callback.answer()
