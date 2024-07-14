from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from utils.set_bot_commands import set_commands
from database.database_history import init_db

if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    set_commands(bot)
    init_db()
    bot.infinity_polling()

