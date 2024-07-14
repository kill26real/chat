from telebot.types import Message
from telebot.apihelper import ApiTelegramException, ApiInvalidJSONException
from loader import bot
from states.price_state import States
from keyboards.inline.locations import city_markup
from keyboards.inline.date import calendar, calendar_1, MyTranslationCalendar
from keyboards.inline.correct import correct
from keyboards.inline.hotels import hotels
from keyboards.inline.get_photo import get_photo, photo_amount
from bot_requests.hotels_request import find_hotels, find_best_hotel
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date
import datetime
from requests.exceptions import ReadTimeout, ConnectTimeout, ConnectionError
import os
import sqlite3 as sq
from handlers.hotel_search.history import history


@bot.message_handler(commands=['anton', 'shop'])
def price(message: Message) -> None:
    """Функция-хэндлер. Обрабатывает команды с поиском отелей, присваивает состояние и спрашивает город."""
    bot.set_state(message.from_user.id, States.first, message.chat.id)
    #bot.send_message(message.from_user.id, f"{message.from_user.first_name}, what do you want?")
    bot.send_message(message.from_user.id, 'Please specify:', reply_markup=photo_amount())


@bot.message_handler(state=States.first)
def city(message) -> None:
    """Функция-хэндлер. Ловит состояние пользователя,
    вызывает функцию, создающую кнопки с локациями и выводит пользователю."""
    if message.text == '1':
        bot.send_message(message.from_user.id, 'Lorem ipsum, or lipsum as it is sometimes known, is dummy text used i distract from the layout. A practice not without controversy, laying out pages with meaningless filler text can be very useful when the focus is meant to be on design, not content.')
    else:
        bot.send_message(message.from_user.id, 'Вы попали в магазин!!!!!1')

    animation = bot.send_animation(message.chat.id, r'https://i.gifer.com/7kRE.gif')

    bot.set_state(message.from_user.id, States.second, message.chat.id)
    #bot.send_message(message.from_user.id, 'Please specify:', reply_markup=city_markup(message.text))
    bot.delete_message(message.chat.id, animation.id)



@bot.callback_query_handler(func=lambda call: True, state=States.first)
def city_callback(call) -> None:
    """Функция, ловит callback нажатой пользователем кнопки с локацией и вызывает функцию, создающую кнопки с датой заселения"""
    if call.data == '1':
        bot.set_state(call.from_user.id, States.second, call.message.chat.id)
        bot.send_message(call.message.from_user.id, "Информация")
    else:
        bot.send_message(call.message.from_user.id, 'Select the check-in date:', reply_markup=calendar())


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(), state=States.third)
def date_in_callback(c):
    """Функция, ловит callback нажатой пользователем кнопки с датой и вызывает функцию, создающую кнопки с датой выселения"""
    result, key, step = DetailedTelegramCalendar(min_date=date.today(), max_date=datetime.date(2024, 12, 31)).process(
        c.data)
    if not result and key:
        word = 'дату'
        if LSTEP[step] == 'year':
            word = 'год'
        elif LSTEP[step] == 'month':
            word = 'месяц'
        elif LSTEP[step] == 'day':
            word = 'день'
        bot.edit_message_text(f"Choose {word}", c.message.chat.id, c.message.message_id, reply_markup=key)
    elif result:
        bot.edit_message_text(f"Check-in date: {result}", c.message.chat.id, c.message.message_id)
        bot.set_state(c.from_user.id, States.third, c.message.chat.id)
        with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
            data['date_in'] = result
        bot.send_message(c.message.chat.id, 'Select the check-out date:', reply_markup=calendar_1(result))


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(), state=States.third)
def date_out_callback(c):
    """Функция, ловит callback нажатой пользователем кнопки с датой и вызывает функцию,
     создающую кнопки с подтверждением корректности данных"""
    with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
        date = data['date_in']
    dates = str(date).split('-')

    result, key, step = DetailedTelegramCalendar(min_date=datetime.date(int(dates[0]), int(dates[1]), int(dates[2]) + 1),
                                              max_date=datetime.date(2024, 12, 31)).process(c.data)
    if not result and key:
        word = 'дату'
        if LSTEP[step] == 'year':
            word = 'год'
        elif LSTEP[step] == 'month':
            word = 'месяц'
        elif LSTEP[step] == 'day':
            word = 'день'
        bot.edit_message_text(f"Choose {word}", c.message.chat.id, c.message.message_id, reply_markup=key)

    elif result:
        bot.edit_message_text(f"Check-out date: {result}", c.message.chat.id, c.message.message_id)
        bot.set_state(c.from_user.id, States.third, c.message.chat.id)
        with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
            data['date_out'] = result
        bot.send_message(c.message.chat.id, 'Is the data correct?', reply_markup=correct())


@bot.callback_query_handler(func=lambda call: True, state=States.fourth)
def correct_callback(call) -> None:
    """Функция, ловит callback нажатой пользователем кнопки: если данные корректны - вызывает функцию,
     создающую кнопки с количеством отелей, если нет - спрашивает все заново"""
    if call.data == 'yes':
        bot.edit_message_text("I've recorded the data!", call.message.chat.id, call.message.message_id)
        bot.set_state(call.from_user.id, States.third, call.message.chat.id)
        bot.send_message(call.message.chat.id, 'Select the number of hotels you want to display: ',
                         reply_markup=hotels())
    elif call.data == 'no':
        bot.edit_message_text("Let's try it again", call.message.chat.id, call.message.message_id)
        bot.set_state(call.from_user.id, States.first, call.message.chat.id)
        bot.send_message(call.from_user.id,
                         f"{call.from_user.first_name}, write the city where you want to see the hotels.")


@bot.callback_query_handler(func=lambda call: True, state=States.fourth)
def hotels_callback(call) -> None:
    """Функция, ловит callback нажатой пользователем кнопки с количеством отелей и вызывает функцию,
     создающую кнопки с выводом фотографий"""
    bot.edit_message_text(f"You have choosen {call.data} hotels", call.message.chat.id, call.message.message_id)
    bot.set_state(call.from_user.id, States.fifth, call.message.chat.id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['hotels'] = int(call.data)
    bot.send_message(call.message.chat.id, 'Do I need to display photos?', reply_markup=get_photo())


