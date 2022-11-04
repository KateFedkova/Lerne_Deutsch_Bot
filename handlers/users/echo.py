import random
import time

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards import choose_level, game_keyboard, yes_keyboard
from loader import dp, db
from states import UserStates


@dp.message_handler(state=UserStates.set_level, text=["A1", "A2", "B1"])
async def get_level(message: types.Message, state: FSMContext):
    level = message.text
    await db.add_user(message.from_user.id, message.from_user.first_name, level)
    await db.add_user_to_game(message.from_user.id)
    await state.finish()
    await message.answer("""Супер!
    
Як вчити слова описано тут: 
/how_to_learn""")


@dp.message_handler(commands="how_to_learn")
async def get_level(message: types.Message):
    await message.answer("""1️⃣ Після того як ти обрав свій рівень, я запропоную тобі слова для вивчення /learn 

2️⃣ Після розбору нових слів, ти можеш виконати вправи, щоб перевірити свої знання

🔈 Якщо обраний тобою рівень занадто легкий для тебе або ти вже вивчив усі слова, натисни /update_level та обери наступний рівень""")


@dp.message_handler(commands="update_level")
async def bot_start(message: types.Message):
    await UserStates.new_level.set()
    await message.answer(f"{message.from_user.full_name}, я радий, що допомогаю тобі вчитися!", reply_markup=choose_level)


@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    """Allow user to cancel any action"""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.answer('OK')


@dp.message_handler(state=UserStates.new_level, text=["A1", "A2", "B1"])
async def get_level(message: types.Message, state: FSMContext):
    level = message.text
    await db.new_level(message.from_user.id, level)
    await state.finish()
    await message.answer("Так тримати!")
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEOpoRjVmbq1dGaP23AI9kVd-bveEzrwwACZgAD29t-AAGTzMPQDS2PbCoE")


@dp.message_handler(commands="add_word", is_admin=True)
async def add_word_level(message: types.Message):
    await UserStates.choose_level.set()
    await message.answer("Оберіть рівень")


# Add word to the A1 table

@dp.message_handler(text="A1", state=UserStates.choose_level)
async def add_title_a1(message: types.Message):
    await UserStates.title_for_a1.set()
    await message.answer("Крок 1️⃣ із 2️⃣\n\nВведіть слово")


@dp.message_handler(state=UserStates.title_for_a1)
async def add_translation_a1(message: types.Message, state: FSMContext):
    if message.text.replace(' ', '').isalpha():
        word_exist = await db.check_word_exists_a1(message.text)
        if not word_exist:
            await state.update_data({'title': message.text})
            await UserStates.translation_for_a1.set()
            await message.answer("Крок 2️⃣ із 2️⃣\n\nВведіть переклад")
        else:
            await message.answer("Це слово вже існує")
    else:
        await message.answer("Це не схоже на слово")


@dp.message_handler(state=UserStates.translation_for_a1)
async def insert_word_a1(message: types.Message, state: FSMContext):
    if message.text.replace(' ', '').isalpha():
        await state.update_data({'translation': message.text})
        data = await state.get_data()
        await db.add_word_a1(data['title'], data['translation'])
        await state.finish()
        await message.answer("Успішно додано")
    else:
        await message.answer("Це не схоже на слово")


# Add word to the A2 table

@dp.message_handler(text="A2", state=UserStates.choose_level)
async def add_title_a2(message: types.Message):
    await UserStates.word_for_a2.set()
    await message.answer("Крок 1️⃣ із 3️⃣\n\nВведіть слово")


@dp.message_handler(state=UserStates.word_for_a2)
async def add_part_a2(message: types.Message, state: FSMContext):
    if message.text.replace(' ', '').isalpha():
        word_exist = await db.check_word_exists_a2(message.text)
        if not word_exist:
            await state.update_data({'title': message.text})
            await UserStates.part_of_speech_for_a2.set()
            await message.answer("Крок 2️⃣ із 3️⃣\n\nВведіть, яка це частина мови")
        else:
            await message.answer("Це слово вже існує")
    else:
        await message.answer("Це не схоже на слово")


@dp.message_handler(state=UserStates.part_of_speech_for_a2)
async def add_definition_a2(message: types.Message, state: FSMContext):
    if message.text.replace(' ', '').isalpha():
        await state.update_data({'part': message.text})
        await UserStates.definition_for_a2.set()
        await message.answer("Крок 3️⃣ із 3️⃣\n\nВведіть визначення цього слова")
    else:
        await message.answer("Це не схоже на слово")


@dp.message_handler(state=UserStates.definition_for_a2)
async def insert_word_a2(message: types.Message, state: FSMContext):
    if message.text.replace(' ', '').isalpha():
        await state.update_data({'definition': message.text})
        data = await state.get_data()
        await db.add_word_a2(data['title'], data['part'], data['definition'])
        await state.finish()
        await message.answer("Успішно додано")
    else:
        await message.answer("Це не схоже на слова")


# Add word to the B1 table

@dp.message_handler(text="B1", state=UserStates.choose_level)
async def add_title_b1(message: types.Message):
    await UserStates.word_for_b1.set()
    await message.answer("Крок 1️⃣ із 2️⃣\n\nВведіть слово")


@dp.message_handler(state=UserStates.word_for_b1)
async def add_definition_b1(message: types.Message, state: FSMContext):
    if message.text.replace(' ', '').isalpha():
        word_exist = await db.check_word_exists_b1(message.text)
        if not word_exist:
            await state.update_data({'title': message.text})
            await UserStates.definition_for_b1.set()
            await message.answer("Крок 2️⃣ із 2️⃣\n\nВведіть визначення слова")
        else:
            await message.answer("Це слово вже існує")
    else:
        await message.answer("Це не схоже на слово")


@dp.message_handler(state=UserStates.definition_for_b1)
async def insert_word_b1(message: types.Message, state: FSMContext):
    if message.text.replace(' ', '').isalpha():
        await state.update_data({'definition': message.text})
        data = await state.get_data()
        await db.add_word_b1(data['title'], data['definition'])
        await state.finish()
        await message.answer("Успішно додано")
    else:
        await message.answer("Це не схоже на слова")


# Learn new words + poll

@dp.message_handler(commands="learn")
async def choose_words_for_level(message: types.Message, state: FSMContext):
    if await db.game_exist(message.from_user.id):
        level = await db.level_of_user(message.from_user.id)
        num_of_questions = [random.randint(1, await db.num_of_questions(level)) for i in range(3)]
        user_id = message.from_user.id
        await UserStates.begin_game.set()
        await state.update_data({'level': level, 'questions': num_of_questions, 'id': user_id})
        await message.answer("Підбираю для вас слова")
        await message.answer_sticker(sticker="CAACAgIAAxkBAAEOroFjWRv2wZSUqkKHF5PUocChbGE9LwACXwAD29t-AAGEsFSbEa7K4yoE")
        time.sleep(1)
        await message.answer("Натисніть: так, якщо готовий", reply_markup=yes_keyboard)
    else:
        await message.answer("Спочатку оберіть рівень")


@dp.message_handler(text="так", state=UserStates.begin_game)
async def choose_words_for_level(message: types.Message, state: FSMContext):
    data = await state.get_data()
    for i in data['questions']:
        if data['level'] == "A1":
            new_word = await db.learn_new_words_a1(i)
            await message.answer(f"""👩🏼‍🏫 Neues Wort (нове слово): {new_word['word']}

📚 Die Übersetzung (переклад): {new_word['translation']}""")

        elif data['level'] == "A2":
            new_word = await db.learn_new_words_a2(i)
            await message.answer(f"""👩🏼‍🏫 Neues Wort: {new_word['word']}

Der Wortart (частина мови): {new_word['part']}

Der Begriff (визначення): {new_word['definition']}""")

        elif data['level'] == "B1":
            new_word = await db.learn_new_words_b1(i)
            await message.answer(f"""👩🏼‍🏫 Neues Wort: {new_word['word']}

Der Begriff (визначення): {new_word['definition']}""")
        time.sleep(3)
    await UserStates.begin_game.set()
    time.sleep(1)
    await message.answer("Готовий потренуватися?", reply_markup=game_keyboard)


@dp.callback_query_handler(text="ready", state=UserStates.begin_game)
async def create_poll(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    for i in data['questions']:
        questions = await db.get_questions(data['level'], i)
        for question in questions:
            explanations = await db.get_or_check_clue(data['level'], question['id'])
            answers = await db.get_answers(data['level'], question['id'])
            correct_option = answers.index(await db.get_correct_answer(data['level'], question['id']))
            poll = await call.message.answer_poll(
                question=question['title'],
                options=answers,
                type="quiz",
                correct_option_id=correct_option,
                is_anonymous=False,
                explanation=explanations)
            dp.polls_storage = {poll.poll.id: poll.poll.correct_option_id}
            time.sleep(15)
    await call.message.answer("Ти молодець! Не забувай повторювати слова")
    learned_words = await db.num_of_words(data['id'])
    await db.new_amount_of_words(data['id'], learned_words['words'], len(set(data['questions'])))
    word = await db.stats(data['id'])
    await call.message.answer(f"""{word['name']}, сьогодні ти вивчив(ла) {len(set(data['questions']))} слова
Загалом вивчено слів: {word['words']} """)
    await state.finish()


@dp.poll_answer_handler()
async def poll_answer(poll_answer: types.PollAnswer):
    answer_id = poll_answer.option_ids[0]
    user_id = poll_answer.user.id
    if answer_id == dp.polls_storage[poll_answer.poll_id]:
        await db.update_points(10, user_id)
    else:
        await db.update_points(-5, user_id)


@dp.message_handler(commands="top")
async def top_3_users(message: types.Message):
    if await db.top3_game_users():
        users = await db.top3_game_users()
        await message.answer(f"""🥇 {users[0]['name']}: {users[0]['points']} балів
🥈 {users[1]['name']}: {users[1]['points']} балів
🥉 {users[2]['name']}: {users[2]['points']} балів""")
    else:
        await message.answer("Замало даних для складання таблиці")


# Handles all messages of any state
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message):
    await message.answer(f"""Упс! Я не розумію, що робити. 
Можливо цієї команди поки не існує або вона доступна тільки для адміна""")
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEOqeNjV7s0hcY-FrUbZB6kPQzCiKfz1QACYwAD29t-AAGMnQU950KD5yoE")
