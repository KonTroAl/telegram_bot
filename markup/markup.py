from telebot.types import KeyboardButton

from telegram_bot.settings import settings
from telegram_bot.data_base.dbalchemy import DBManager

class Keyboards:
    def __init__(self):
        self.markup = None
        self.DB = DBManager()

    def set_btn(self, name, step=0, quantity=0):
        return KeyboardButton(settings.KEYBOARD[name])