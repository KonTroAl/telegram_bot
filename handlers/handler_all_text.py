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

    def pressed_btn_order(self, message):
        self.step = 0

        count = self.DB.select_all_products_id()
        quantity = self.DB.select_order_quantity(count[self.step])

        self.send_message_order(count[self.step], quantity, message)

    def send_message_order(self, product_id, quantity, message):
        self.bot.send_message(message.chat.id,
                              MESSAGES['order_number'].format(
                                  self.step+1
                              ),
                              parse_mode='HTML')
        self.bot.send_message(message.chat.id,
                              MESSAGES['order'].format(
                                  self.DB.select_single_product_name(product_id),
                                  self.DB.select_single_product_title(product_id),
                                  self.DB.select_single_product_price(product_id),
                                  self.DB.select_order_quantity(product_id)

                              ),
                              parse_mode='HTML',
                              reply_markup=self.keyboards.orders_menu(self.step, quantity))

    def pressed_up_btn(self, message):
        count = self.DB.select_all_products_id()
        quantity_order = self.DB.select_order_quantity(count[self.step])

        quantity_product = self.DB.select_single_product_quantity(count[self.step])

        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1

            self.DB.update_order_value(count[self.step], 'quantity', quantity_order)
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)

        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_down_btn(self, message):
        count = self.DB.select_all_products_id()
        quantity_order = self.DB.select_order_quantity(count[self.step])

        quantity_product = self.DB.select_single_product_quantity(count[self.step])

        if quantity_product > 0:
            quantity_order -= 1
            quantity_product += 1

            self.DB.update_order_value(count[self.step], 'quantity', quantity_order)
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)

        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_x_btn(self, message):

        count = self.DB.select_all_products_id()

        if count.__len__() > 0:
            quantity_order = self.DB.select_order_quantity(count[self.step])
            quantity_product = self.DB.select_single_product_quantity(count[self.step])

            quantity_product += quantity_order

            self.DB.delete_order(count[self.step])
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)

            self.step -= 1

        count = self.DB.select_all_products_id()

        if count.__len__() > 0:
            quantity_order = self.DB.select_order_quantity(count[self.step])
            self.send_message_order(count[self.step], quantity_order, message)
        else:
            self.bot.send_message(message.chat.id,
                                  MESSAGES['no_orders'],
                                  parse_mode='HTML',
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
            elif message.text == settings.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')
            elif message.text == settings.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')

            elif message.text == settings.KEYBOARD['ORDER']:
                if self.DB.count_row_orders() > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(message.chat.id,
                                          MESSAGES['no_orders'],
                                          parse_mode='HTML',
                                          reply_markup=self.keyboards.category_menu())
            elif message.text == settings.KEYBOARD['UP']:
                self.pressed_up_btn(message)
            elif message.text == settings.KEYBOARD['DOUWN']:
                self.pressed_down_btn(message)
            elif message.text == settings.KEYBOARD['X']:
                self.pressed_x_btn(message)