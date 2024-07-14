from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_photo() -> InlineKeyboardMarkup:
    """Функция, создающая Inline кнопки с выбором выводить фотографии или нет"""
    photo_markup = InlineKeyboardMarkup()
    key_yes = InlineKeyboardButton(text='Yes', callback_data='yes')
    key_no = InlineKeyboardButton(text='No', callback_data='no')
    photo_markup.add(key_yes, key_no)
    return photo_markup

def photo_amount() -> InlineKeyboardMarkup:
    """Функция, создающая Inline кнопки с выбором количества выводимых фотографий"""

    photos_markup = InlineKeyboardMarkup(row_width=3)
    h_1 = InlineKeyboardButton(text='Info', callback_data='1')
    h_2 = InlineKeyboardButton(text='Shop', callback_data='2')

    photos_markup.add(h_1,)
    photos_markup.add(h_2,)

    return photos_markup
