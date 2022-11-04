from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")

HOST = env.str('DB_HOST')
PASSWORD = env.str('DB_PASS')
USER = env.str('DB_USER')
DATABASE = env.str('DB_NAME')
PORT = env.str('DB_PORT')