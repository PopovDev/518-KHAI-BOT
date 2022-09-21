import config
from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
import logging

print(config.HEROKU_APP_NAME)
print(config.WEBHOOK_URL)