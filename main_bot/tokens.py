from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('token')
owner = os.getenv('owner')
base_path = os.getenv('BASE_PATH')
self_path = os.getenv('SELF_PATH')
base_bot_path = os.getenv('BASE_BOT_PATH')