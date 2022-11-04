import asyncio
import asyncpg
from data import config


class Database:
    """All functions of database"""

    def __init__(self):
        loop = asyncio.get_event_loop()
        self.pool: asyncio.pool.Pool = loop.run_until_complete(
            asyncpg.create_pool(
                user=config.USER,
                password=config.PASSWORD,
                database=config.DATABASE,
                host=config.HOST,
                port=config.PORT
            )
        )

    # Creation of all tables

    async def create_user_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS "user"(
            id integer NOT NULL,
            name character varying NOT NULL,
            level character varying NOT NULL,
            words integer NOT NULL DEFAULT 0,
            CONSTRAINT user_pkey PRIMARY KEY (id)
            )
            '''
        await self.pool.execute(sql)

    async def create_game_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS "game"(
            user_id integer NOT NULL,
            points integer NOT NULL,
            CONSTRAINT userid_pkey PRIMARY KEY (user_id),
            CONSTRAINT ouser_fkey FOREIGN KEY (user_id)
                REFERENCES public."user" (id) MATCH SIMPLE
            )'''
        await self.pool.execute(sql)

    async def create_education_a1_table(self):
        sql = """CREATE TABLE IF NOT EXISTS "education_a1"(
            id serial NOT NULL,
            title character varying NOT NULL,
            translation character varying NOT NULL,
            CONSTRAINT a1id_pkey PRIMARY KEY (id)
            )
            """
        await self.pool.execute(sql)

    async def create_questions_a1_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS "questions_a1"(
            id serial NOT NULL,
            title character varying NOT NULL,
            word_group integer NOT NULL,
            CONSTRAINT qa1id_pkey PRIMARY KEY (id),
            CONSTRAINT qa1group_fkey FOREIGN KEY (word_group)
                REFERENCES public."education_a1" (id) MATCH SIMPLE
            )'''
        await self.pool.execute(sql)

    async def create_answers_a1_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS "answers_a1"(
            id serial NOT NULL,
            answer character varying NOT NULL,
            question integer NOT NULL,            
            is_correct bool NOT NULL,
            CONSTRAINT answa1id_pkey PRIMARY KEY (id),
            CONSTRAINT questa1_fkey FOREIGN KEY (question)
                 REFERENCES public."questions_a1" (id) MATCH SIMPLE
            )
            '''
        await self.pool.execute(sql)

    async def create_education_a2_table(self):
        sql = """CREATE TABLE IF NOT EXISTS "education_a2"(
            id serial NOT NULL,
            word character varying NOT NULL,
            part_of_speech character varying NOT NULL,
            definition character varying NOT NULL,
            CONSTRAINT a2id_pkey PRIMARY KEY (id)
            )
            """
        await self.pool.execute(sql)

    async def create_questions_a2_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS "questions_a2"(
            id serial NOT NULL,
            title character varying NOT NULL,
            word_group integer NOT NULL,
            CONSTRAINT qa2id_pkey PRIMARY KEY (id),
            CONSTRAINT qa2group_fkey FOREIGN KEY (word_group)
                REFERENCES public."education_a2" (id) MATCH SIMPLE
            )'''
        await self.pool.execute(sql)

    async def create_answers_a2_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS "answers_a2"(
            id serial NOT NULL,
            answer character varying NOT NULL,
            question integer NOT NULL,
            is_correct bool NOT NULL,
            CONSTRAINT answa2id_pkey PRIMARY KEY (id),
            CONSTRAINT questa2_fkey FOREIGN KEY (question)
                 REFERENCES public."questions_a2" (id) MATCH SIMPLE
            )
            '''
        await self.pool.execute(sql)

    async def create_education_b1_table(self):
        sql = """CREATE TABLE IF NOT EXISTS "education_b1"(
            id serial NOT NULL,
            title character varying NOT NULL,
            definition character varying NOT NULL,
            CONSTRAINT b1id_pkey PRIMARY KEY (id)
            )
            """
        await self.pool.execute(sql)

    async def create_questions_b1_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS "questions_b1"(
            id serial NOT NULL,
            title character varying NOT NULL,
            word_group integer NOT NULL,
            CONSTRAINT qb1id_pkey PRIMARY KEY (id),
            CONSTRAINT qb1group_fkey FOREIGN KEY (word_group)
                REFERENCES public."education_b1" (id) MATCH SIMPLE
            )'''
        await self.pool.execute(sql)

    async def create_answers_b1_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS "answers_b1"(
            id serial NOT NULL,
            answer character varying NOT NULL,
            question integer NOT NULL,
            is_correct bool NOT NULL,
            CONSTRAINT answb1id_pkey PRIMARY KEY (id),
            CONSTRAINT questb1_fkey FOREIGN KEY (question)
                 REFERENCES public."questions_b1" (id) MATCH SIMPLE
            )
            '''
        await self.pool.execute(sql)

    async def clues_for_questions_a2_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS "clues_a2"(
              question integer NOT NULL,            
              clue character varying NOT NULL,
              CONSTRAINT questa2id_pkey PRIMARY KEY (question),
              CONSTRAINT questa2_fkey FOREIGN KEY (question)
                   REFERENCES public."questions_a2" (id) MATCH SIMPLE
              )
              '''
        await self.pool.execute(sql)

    async def clues_for_questions_b1_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS "clues_b1"(
              question integer NOT NULL,            
              clue character varying NOT NULL,
              CONSTRAINT questb1id_pkey PRIMARY KEY (question),
              CONSTRAINT questb1_fkey FOREIGN KEY (question)
                   REFERENCES public."questions_b1" (id) MATCH SIMPLE
              )
              '''
        await self.pool.execute(sql)

    # Insert data into tables

    async def add_user(self, user_id, user_name, user_level):
        sql = f"""INSERT INTO "user"(id, name, level) 
        VALUES ({user_id}, '{user_name}', '{user_level}')"""
        try:
            await self.pool.execute(sql)
        except:
            pass

    async def add_word_a1(self, title, translation):
        sql = f"""INSERT INTO "education_a1"(title, translation)
        VALUES ('{title}', '{translation}')"""
        await self.pool.execute(sql)

    async def add_word_a2(self, title, part, defenition):
        sql = f"""INSERT INTO education_a2(word, part_of_speech, definition)
        VALUES('{title}', '{part}', '{defenition}')"""
        await self.pool.execute(sql)

    async def add_word_b1(self, title, defenition):
        sql = f"""INSERT INTO education_b1(title, definition)
        VALUES('{title}', '{defenition}')"""
        await self.pool.execute(sql)

    async def add_user_to_game(self, user_id):
        sql = f"""INSERT INTO "game"(user_id, points)
        VALUES({user_id}, 0)"""
        try:
            await self.pool.execute(sql)
        except:
            pass

    # Update data

    async def new_level(self, id, level):
        """Update level of the user"""
        sql = f"""UPDATE "user"
        SET level='{level}'
        WHERE id={id}"""
        await self.pool.execute(sql)

    async def update_points(self, points, user_id):
        sql = f'SELECT * FROM "game" WHERE user_id = {user_id}'
        data = await self.pool.fetchrow(sql)
        points_data = [data['points']]
        sql_i = f"""UPDATE "game"
        SET points={points + points_data[0]}
        WHERE user_id={user_id} AND points + {points} >= 0;"""
        await self.pool.execute(sql_i)
        sql_d = f"""UPDATE "game"
        SET points=0
        WHERE user_id={user_id} AND points + {points} < 0;"""
        await self.pool.execute(sql_d)

    async def new_amount_of_words(self, id, old_amount, word):
        sql = f"""UPDATE "user"
        SET words={old_amount + word}
        WHERE id={id}"""
        await self.pool.execute(sql)

    # Get level for practicing

    async def level_of_user(self, user_id):
        sql = f"""SELECT level FROM "user" WHERE id={user_id}"""
        level = await self.pool.fetchrow(sql)
        return level['level']

    # Get questions and answers for game

    async def num_of_questions(self, level):
        sql = f'''SELECT MAX(id) FROM education_{str(level.lower())}'''
        max_num = await self.pool.fetchrow(sql)
        return max_num['max']

    async def get_questions(self, level, num):
        q_table = f"questions_{str(level.lower())}"
        e_table = f"education_{str(level.lower())}"
        sql = f'''SELECT {q_table}.id, {q_table}.title FROM "{e_table}"
        JOIN {q_table} ON {e_table}.id={q_table}.word_group
        WHERE {q_table}.word_group={num}'''
        data = await self.pool.fetch(sql)
        question = []
        for i in data:
            question += [
                {
                    'id': i['id'],
                    'title': i['title']
                }
            ]
        return question

    async def get_answers(self, level, question_id):
        sql = f'SELECT answer FROM "answers_{str(level.lower())}" WHERE question={question_id}'
        data = await self.pool.fetch(sql)
        answers = []
        for i in data:
            answers.append(i['answer'])
        return answers

    async def get_correct_answer(self, level, question_id):
        sql = f'SELECT answer FROM "answers_{str(level.lower())}" WHERE question={question_id} AND is_correct = true'
        data = await self.pool.fetchrow(sql)
        correct = ''
        correct += data['answer']
        return correct

    # Learn new words
    async def learn_new_words_a1(self, ids):
        sql = f"""SELECT title, translation FROM "education_a1"
        WHERE id={ids}"""
        data = await self.pool.fetchrow(sql)
        return {'word': data['title'], 'translation': data['translation']}

    async def learn_new_words_a2(self, ids):
        sql = f"""SELECT word, part_of_speech, definition FROM "education_a2"
        WHERE id={ids}"""
        data = await self.pool.fetchrow(sql)
        return {'word': data['word'], 'part': data['part_of_speech'], 'definition': data['definition']}

    async def learn_new_words_b1(self, ids):
        sql = f"""SELECT title, definition FROM "education_b1"
        WHERE id={ids}"""
        data = await self.pool.fetchrow(sql)
        return {'word': data['title'], 'definition': data['definition']}

    # Get explanation for poll

    async def get_or_check_clue(self, level, question):
        sql = f"""SELECT clue FROM "clues_{level.lower()}" WHERE question={question}"""
        try:
            data = await self.pool.fetchrow(sql)
            if not data:
                return None
            else:
                return data['clue']
        except:
            return None

    # Additional functions

    async def stats(self, user_id):
        sql = f"""SELECT name, words FROM "user" WHERE id={user_id}"""
        data = await self.pool.fetchrow(sql)
        return data

    async def game_exist(self, user_id):
        sql = f'SELECT * FROM "game" WHERE user_id = {user_id}'
        data = await self.pool.fetch(sql)
        return data

    async def num_of_words(self, user_id):
        sql = f'''SELECT name, words FROM "user" WHERE id={user_id}'''
        data = await self.pool.fetchrow(sql)
        return data

    async def top3_game_users(self):
        sql = f'''SELECT name, points FROM "game" JOIN "user" ON game.user_id = "user".id 
        ORDER BY -points LIMIT 3'''
        data = await self.pool.fetch(sql)
        top3_data = []
        for u in data:
            top3_data += [
                {
                    "name": u['name'],
                    "points": u['points']
                }
            ]
        if len(top3_data) == 3:
            return top3_data
        else:
            return False

    async def check_word_exists_a1(self, title):
        sql = f"""SELECT id FROM education_a1 WHERE title='{title}'"""
        data = await self.pool.fetchrow(sql)
        return data

    async def check_word_exists_a2(self, title):
        sql = f"""SELECT id FROM education_a2 WHERE word='{title}'"""
        data = await self.pool.fetchrow(sql)
        return data

    async def check_word_exists_b1(self, title):
        sql = f"""SELECT id FROM education_b1 WHERE title='{title}'"""
        data = await self.pool.fetchrow(sql)
        return data
