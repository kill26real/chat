from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS
from config_data.config import COMMANDS


def set_commands(bot):
    """Функция, которая добавляет команды"""
    bot.set_my_commands(
        [BotCommand(*i) for i in COMMANDS]
    )


def set_default_commands(bot):
    """Функция, которая добавляет команды по умолчанию"""
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )


