from aiogram import types


def close_poll_keyboard(user_id: str):
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Закрыть голосование', callback_data=user_id)
    )
