from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = f"""Список команд:
/start - Запустити бота
/help - Вивести довідку
/how_to_learn - Пояснення як користуватися
/update_level - Новий рівень
/learn - Почати навчання
/top - Найкращі гравці
/cancel - Скасувати команду

Вчіть нові слова немецької мови 📚
🥇 Змагайтесь з іншими
Мінімум теорії та багато практики 🌸"""
    await message.answer(text)
