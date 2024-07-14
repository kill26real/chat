from telebot.types import Message
from config_data.config import COMMANDS
from loader import bot
from config_data.config import DEFAULT_COMMANDS


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """Функция-хэндлер. Обрабатывает команду start и выводит все существующие команды."""
    text = [f'/{command} - {desk}' for command, desk in COMMANDS]
    commands = '\n'.join(text)
    bot.reply_to(message,
                 f"Привет, {message.from_user.full_name}!Это бот по поиску отелей по всему миру (кроме РФ).\n Выбери команду: \n{commands}")

