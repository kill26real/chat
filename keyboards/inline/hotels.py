from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def hotels() -> InlineKeyboardMarkup:
    """Функция, создающая Inline кнопки с выбором количества выводимых отелей"""

    hotels_markup = InlineKeyboardMarkup(row_width=3)

    h_1 = InlineKeyboardButton(text='1', callback_data='1')
    h_2 = InlineKeyboardButton(text='2', callback_data='2')
    h_3 = InlineKeyboardButton(text='3', callback_data='3')
    h_4 = InlineKeyboardButton(text='4', callback_data='4')
    h_5 = InlineKeyboardButton(text='5', callback_data='5')
    h_6 = InlineKeyboardButton(text='6', callback_data='6')

    hotels_markup.add(h_1, h_2, h_3)
    hotels_markup.add(h_4, h_5, h_6)

    return hotels_markup
