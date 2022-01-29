import abc
from telegram_bot.markup.markup import Keyboards
from telegram_bot.data_base.dbalchemy import DBManager

class Handler(metaclass=abc.ABC):

    def __init__(self, bot):
        self.bot = bot
        self.keyboards = Keyboards()
        self.DB = DBManager()

    @abc.abstractmethod
    def handle(self):
        pass