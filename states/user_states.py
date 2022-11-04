from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):

    # updating level of the language
    set_level = State()
    new_level = State()

    choose_level = State()

    # states for adding new words to the A1 table
    title_for_a1 = State()
    translation_for_a1 = State()

    # states for adding new words to the A2 table
    word_for_a2 = State()
    part_of_speech_for_a2 = State()
    definition_for_a2 = State()

    # states for adding new words to the B1 table
    word_for_b1 = State()
    definition_for_b1 = State()

    # start practicing
    begin_game = State()
