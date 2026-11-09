from os import getenv
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = getenv('TOKEN')

ADMIN_ID = int(os.getenv('ADMIN_ID', 0))