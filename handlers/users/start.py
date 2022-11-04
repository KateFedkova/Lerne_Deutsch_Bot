from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards import choose_level
from loader import dp
from states import UserStates


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await UserStates.set_level.set()
    await message.answer(f"Hallo, {message.from_user.full_name}!", reply_markup=choose_level)
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEOpnpjVmRoAzY_2mPyHDqF4IsGT1V42wACbwAD29t-AAGZW1Coe5OAdCoE")
