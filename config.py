import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.environ.get('BOT')
db_login = os.environ.get('LOGIN')
db_pass = os.environ.get('PASS')
db_host = os.environ.get('HOST')



db_name = os.environ.get('DBNAME')

