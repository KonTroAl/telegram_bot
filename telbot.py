from telebot import TeleBot

from settings import settings

from handlers.handler_main import HandlerMain

class TelBot:

    __version__ = settings.VERSION
    __author__ = settings.AUTHOR

    def __init__(self):
        self.token = settings.TOKEN
        self.bot = TeleBot(self.token)

        self.handler = HandlerMain(self.bot)

    def start(self):
        self.handler.handle()

    def run_bot(self):
        self.start()

        self.bot.polling(none_stop=True)

if __name__ == '__main__':
    bot = TelBot()
    bot.run_bot()