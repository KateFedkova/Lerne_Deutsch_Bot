from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# keyboard for choosing level
choose_level = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("A1")
        ],
        [
            KeyboardButton("A2")
        ],
        [
            KeyboardButton("B1")
        ]
    ],
    one_time_keyboard=True,
    input_field_placeholder="Оберіть свій рівень"
)

# keyboard for checking if the user is ready to learn new words
yes_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("так")
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
