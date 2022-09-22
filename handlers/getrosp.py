from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from models.day import Days
from service import format_lession, format_rosp, get_now

router = Router()


def get_keyboard_lessions(day_num):
    buttons = [[]]
    lessions = Days.objects(num=day_num).first().lessions
    for i, (a, b) in enumerate(lessions):
        if a.empty and b.empty:
            continue
        is_duo = not a.empty and not b.empty
        if not a.empty:
            txt = f"{i+1}"
            if is_duo:
                txt += ': Ч'
            buttons[0].append(InlineKeyboardButton(
                text=txt, callback_data=f"lession:{day_num}@{i}@0"))
        if not b.empty:
            txt = f"{i+1}"
            if is_duo:
                txt += ': З'
            buttons[0].append(InlineKeyboardButton(
                text=txt, callback_data=f"lession:{day_num}@{i}@1"))
    buttons.append([InlineKeyboardButton(
        text='Назад', callback_data=f'back_w:{day_num}')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@router.message(commands=['getrosp'])
async def commad_handle(message: Message):
    day_num = get_now()[0]
    await message.answer(format_rosp(day_num), parse_mode='HTML', reply_markup=get_keyboard_lessions(day_num))


@router.callback_query(lambda callback_query: callback_query.data.startswith('lession:'))
async def open_lession(callback: CallbackQuery):

    day_num, lession_num, lession_type = map(
        int, callback.data.split(':')[1].split('@'))
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data=f'back_l:{day_num}')]
    ])

    text = format_lession(day_num, lession_num, lession_type)
    await callback.message.edit_text(text, parse_mode='HTML', reply_markup=back_keyboard, disable_web_page_preview=True)
    await callback.answer()


@router.callback_query(lambda callback_query: callback_query.data.startswith('back_l:'))
async def back_to_rosp(callback: CallbackQuery):
    day_num = int(callback.data.split(':')[1])
    await callback.message.edit_text(format_rosp(day_num), parse_mode='HTML', reply_markup=get_keyboard_lessions(day_num), disable_web_page_preview=True)
    await callback.answer()
