import abc
from markup.markup import Keyboards
from data_base import DBManager

class Handler(metaclass=abc.ABC):

    def __init__(self, bot):
        self.bot = bot
        self.keyboards = Keyboards()
        self.DB = DBManager()

    @abc.abstractmethod
    def handle(self):
        pass