from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def category_markup(result) -> InlineKeyboardMarkup:
    """
    Функция для создания кнопок
    :param result: Список (Функция
    уже возвращает список словарей с нужным именем и id)
    :return: Кнопки для выбора части города
    """
    destinations = InlineKeyboardMarkup()
    first = ''
    second = ''
    count = 0
    for field in result:
        if count % 2 == 0:
            first = InlineKeyboardButton(text=field['name'], callback_data=f'{field["name"]} {field["slug"]}' + ']')
        else:
            second = InlineKeyboardButton(text=field['name'], callback_data=f'{field["name"]} {field["slug"]}' + ']')
            destinations.add(first, second)
        count += 1

    return destinations


def results_num_markup() -> InlineKeyboardMarkup:
    """
    Функция для создания кнопок
    :return: Кнопки для выбора количества результатов
    """
    destinations = InlineKeyboardMarkup()
    first = InlineKeyboardButton(text='🤔 3 мероприятия?', callback_data='3num')
    second = InlineKeyboardButton(text='🫣5 Мероприятий??!', callback_data='5num')
    third = InlineKeyboardButton(text='😳10 МЕРОПРИЯТИЙ??!?!?', callback_data='10num')
    destinations.add(first)
    destinations.add(second)
    destinations.add(third)

    return destinations


def first_markup():
    return None
