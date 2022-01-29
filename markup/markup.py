from telebot.types import KeyboardButton

from settings import settings
from data_base import DBManager

class Keyboards:
    def __init__(self):
        self.markup = None
        self.DB = DBManager()

    def set_btn(self, name, step=0, quantity=0):
        return KeyboardButton(settings.KEYBOARD[name])