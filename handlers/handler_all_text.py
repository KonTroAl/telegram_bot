from .handler import Handler
from settings import settings
from settings.message import MESSAGES

class HandlerAllText(Handler):

    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_info(self, message):
        self.bot.send_message(message.chat.id,
                              MESSAGES['trading_store'],
                              parse_mode="HTML",
                              reply_markup=self.keyboards.start_info())

    def pressed_btn_settings(self, message):
        self.bot.send_message(message.chat.id,
                              MESSAGES['settings'],
                              parse_mode="HTML",
                              reply_markup=self.keyboards.settings_menu())

    def pressed_btn_back(self, message):
        self.bot.send_message(message.chat.id,
                              "You're back to the main menu!",
                              reply_markup=self.keyboards.start_menu())

    def pressed_btn_choose_goods(self, message):
        self.bot.send_message(message.chat.id,
                              "You're now in products categories!",
                              reply_markup=self.keyboards.remove_menu())
        self.bot.send_message(message.chat.id,
                              'Please, choose category!',
                              reply_markup=self.keyboards.category_menu())

    def pressed_btn_product(self, message, product):
        self.bot.send_message(message.chat.id,
                              "You're in category: " + settings.KEYBOARD[product],
                              reply_markup=self.keyboards.chosen_category(settings.CATEGORY[product]))
        self.bot.send_message(message.chat.id,
                              'Ok',
                              reply_markup=self.keyboards.category_menu())

    def handle(self):

        @self.bot.message_handler(func=lambda message: True)
        def handle(message):

            if message.text == settings.KEYBOARD['INFO']:
                self.pressed_btn_info(message)
            elif message.text == settings.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)
            elif message.text == settings.KEYBOARD['<<']:
                self.pressed_btn_back(message)
            elif message.text == settings.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_choose_goods(message)
            elif message.text == settings.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')