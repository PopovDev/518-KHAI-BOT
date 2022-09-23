from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from models.day import Days
from service import format_lession, format_rosp, get_now, EDIT_MODE


router = Router()


def get_keyboard(day_num: int):
    buttons = [[], []]
    lessions = Days.objects(num=day_num).first().lessions
    for i, (a, b) in enumerate(lessions):
        buttons[0].append(InlineKeyboardButton(
            text=f"{i+1}: Ч(о)", callback_data=f"edit_lession:{day_num}@{i}@0@0"))
        buttons[1].append(InlineKeyboardButton(
            text=f"{i+1}: З", callback_data=f"edit_lession:{day_num}@{i}@1@0"))
    buttons.append([InlineKeyboardButton(
        text='Назад', callback_data=f'back_l:{day_num}')])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(commands=['enable_edit'])
async def commad_handle(message: Message):
    EDIT_MODE['mode'] = True
    await message.answer("Режим редактирования включен")


@router.message(commands=['disable_edit'])
async def commad_handle(message: Message):
    EDIT_MODE['mode'] = False
    await message.answer("Режим редактирования выключен")


@router.callback_query(lambda callback_query: callback_query.data.startswith('edit_mode:'))
async def edit_mode(callback: CallbackQuery):
    day_num = int(callback.data.split(':')[1])
    await callback.message.edit_text(format_rosp(day_num), parse_mode='HTML', reply_markup=get_keyboard(day_num), disable_web_page_preview=True)
    await callback.answer()

# edit_lession


@router.callback_query(lambda callback_query: callback_query.data.startswith('edit_lession:'))
async def edit_lession(callback: CallbackQuery):
    day_num, lession_num, lession_type, command = map(
        int, callback.data.split(':')[1].split('@'))
    day = Days.objects(num=day_num).first()
    lession = day.lessions[lession_num][lession_type]

    match command:
        case 1:
            lession.empty = not lession.empty
            day.save()

    buttons = []

    buttons.append([InlineKeyboardButton(
        text=f"Активировать" if lession.empty else f"Деактивировать", callback_data=f"edit_lession:{day_num}@{lession_num}@{lession_type}@1")])

    #update button
    buttons.append([InlineKeyboardButton(
        text=f"Обновить", callback_data=f"edit_lession:{day_num}@{lession_num}@{lession_type}@0")])

    buttons.append([InlineKeyboardButton(
        text='Назад', callback_data=f'edit_mode:{day_num}')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    text = f"Редактирование:\n{day.name} : {lession_num+1}:{lession_type} пара\n\n"
    text += f"Активна: {not lession.empty}\n\n"
    text += f"1. Название: {lession.title}\n\n"
    text += f"2. Преподаватель: {lession.teacher}\n\n"
    text += f"3. Платформа: {lession.link_platform}\n\n"
    text += f"4. Ссылка: {lession.link}\n\n"
    text += f"/set {day_num}{lession_num}{lession_type} (num) (значение)\n"

    try:
        await callback.message.edit_text(text, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)
    except Exception as e:
        print(e)

    await callback.answer()

#set command
@router.message(commands=['set'])
async def set_value(message: Message):
    try:
        text = message.text.split(' ')
        if len(text) <3:
            return

        day_num, lession_num, lession_type = map(int, text[1])
        day = Days.objects(num=day_num).first()
        lession = day.lessions[lession_num][lession_type]
        num = int(text[2])
        print(num)
        match num:
            case 1:
                lession.title = ' '.join(text[3:])
            case 2:
                lession.teacher = ' '.join(text[3:])
            case 3:
                lession.link_platform = ' '.join(text[3:])
            case 4:
                lession.link = ' '.join(text[3:])
        day.save()
        await message.delete()
    except Exception as e:
        pass


