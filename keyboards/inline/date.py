from datetime import date
import datetime
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP


my_translation_months = ['Янв', 'Фев', 'Март', 'Апр', 'Май', 'Июнь', 'Июль', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
my_translation_days_of_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']


class MyTranslationCalendar(DetailedTelegramCalendar):
    """Функция, создающая кастомный календарь с русскими названиями месяцов и дней недели"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.days_of_week['yourtransl'] = my_translation_days_of_week
        self.months['yourtransl'] = my_translation_months
        self.locale = 'ru'

def calendar():
    """Функция, создающая Inline кнопки с датой заселения"""
    today = date.today()
    next_year = today.year + 1
    calendar_2, step = DetailedTelegramCalendar(min_date=today, max_date=datetime.date(next_year, 12, 31)).build()
    return calendar_2

def calendar_1(res_date):
    """Функция, создающая Inline кнопки с датой выселения"""
    dates = str(res_date).split('-')
    next_year = date.today().year + 1
    calendar_3, step_1 = DetailedTelegramCalendar(min_date=datetime.date(int(dates[0]), int(dates[1]), int(dates[2]) + 1),
                                                  max_date=datetime.date(next_year, 12, 31)).build()
    return calendar_3
