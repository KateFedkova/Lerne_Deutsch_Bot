from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# keyboard for checking if the user is ready to practice new words
game_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Так", callback_data=f"ready")
        ]
    ]
)
