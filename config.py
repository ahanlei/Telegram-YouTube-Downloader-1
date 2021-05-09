import  os

TOKEN = os.environ.get("TOKEN")
APP_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")

youtube_next_fetch = 0  # time in minute


EDIT_TIME = 5