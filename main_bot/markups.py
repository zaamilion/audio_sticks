from aiogram import types

markup_subscribe = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='ПОДПИСАЛСЯ', callback_data='sub')]])
cancel = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='отмена', callback_data='cancel')]])

def generate_tariffs_markup(bot_tarifs):
    return types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text=f'{tarif.name}, {tarif.quantity} стикеров', callback_data=tarif.name)] for tarif in bot_tarifs.keys()])