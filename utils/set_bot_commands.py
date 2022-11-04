from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустити бота"),
            types.BotCommand("help", "Вивести довідку"),
            types.BotCommand("how_to_learn", "Пояснення як користуватися"),
            types.BotCommand("update_level", "Новий рівень"),
            types.BotCommand("learn", "Почати навчання"),
            types.BotCommand("top", "Найкращі гравці"),
            types.BotCommand("add_word", "Додати нове слово"),
            types.BotCommand("cancel", "Скасувати команду"),
        ]
    )
