from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(commands=['start'])
async def message_with_text(message: Message):
    await message.answer("aboba")