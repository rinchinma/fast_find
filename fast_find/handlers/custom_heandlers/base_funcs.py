from datetime import date, timedelta
from loader import bot
from states.all_states import UserChoiceState
from rapid_api import \
    event_founding, category_founding, final_message

from keyboards.inline.all_markup \
    import category_markup, results_num_markup

from loguru import logger
from telegram_bot_calendar import LSTEP, WYearTelegramCalendar


@bot.message_handler(commands=['start', 'go'])
@logger.catch
def start(message):
    bot.reply_to(message, f"Привет😁, {message.from_user.full_name}!")
    bot.set_state(
        message.from_user.id, UserChoiceState.event_type, message.chat.id
    )
    with bot.retrieve_data(message.from_user.id, message.chat.id) as bot_data:
        bot_data['user_name'] = message.from_user.full_name

    bot.send_message(
        message.from_user.id,
        '✍Выберите категорию отдыха:',
        reply_markup=category_markup(category_founding()))


@bot.callback_query_handler(func=lambda call: call.data.endswith(']'))
@logger.catch
def get_event(call):
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as bot_data:
        words = call.data[:-1].split(' ')
        bot_data['category'] = words[1]
        bot_data['category_name'] = words[0]

    today = date.today()

    calendar, step = WYearTelegramCalendar(calendar_id='in',
                                              min_date=today,
                                              max_date=today + timedelta(days=31)).build()

    ru_steps = {'m': 'месяц', 'd': 'день'}
    bot.send_message(call.message.chat.id, f'📆Выберите дату: \n{ru_steps[step]}', reply_markup=calendar)


@bot.callback_query_handler(func=WYearTelegramCalendar.func(calendar_id='in'))
@logger.catch
def call_back_check_in(call):
    today = date.today()

    result, key, step = WYearTelegramCalendar(
        calendar_id='in',
        locale='ru',
        min_date=today,
        max_date=today + timedelta(days=31)
    ).process(call.data)

    ru_steps = {'m': 'месяц', 'd': 'день'}

    if not result and key:

        bot.edit_message_text(f"Выберите: {ru_steps[step]}",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=key)
    elif result:

        bot.send_message(
            call.message.chat.id, '💃Сколько мероприятий показать?', reply_markup=results_num_markup()
        )
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as bot_data:
            bot_data['check_in'] = result


@bot.callback_query_handler(func=lambda call: call.data.endswith('num'))
@logger.catch
def get_event(call):
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as bot_data:
        events_num = int(call.data[:-3])
        bot_data['events_num'] = events_num

        events_list = event_founding(
                category=bot_data['category'],
                start_date=bot_data['check_in']
            )
        final_message(
            events_list=events_list.get('results'),
            user_id=call.from_user.id,
            events_count=events_num,
            category_name=bot_data['category_name']
        )
