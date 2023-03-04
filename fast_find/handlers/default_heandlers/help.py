from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS] + \
           '/nОнлайн ресурс, чьей основной задачей является предоставление гражданам необходимой информации.'
    bot.reply_to(message, '\n'.join(text))
