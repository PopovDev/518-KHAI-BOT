import os

BOT_KEY = os.getenv('BOT_KEY')

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

WEBHOOK_URL = f'https://{HEROKU_APP_NAME}.herokuapp.com/webhook/{BOT_KEY}'

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT'))