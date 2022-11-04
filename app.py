from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Set default commands
    await set_default_commands(dispatcher)

    # Notify about startup
    await on_startup_notify(dispatcher)

    # Creation of tables for users
    await db.create_user_table()
    await db.create_game_table()

    # Creation of А1 tables

    await db.create_education_a1_table()
    await db.create_questions_a1_table()
    await db.create_answers_a1_table()

    # Creation of А2 tables

    await db.create_education_a2_table()
    await db.create_questions_a2_table()
    await db.create_answers_a2_table()

    # Creation of B1 tables

    await db.create_education_b1_table()
    await db.create_questions_b1_table()
    await db.create_answers_b1_table()

    # Creation of clues tables
    await db.clues_for_questions_a2_table()
    await db.clues_for_questions_b1_table()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
