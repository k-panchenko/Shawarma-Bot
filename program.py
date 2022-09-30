import logging

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.utils.executor import start_polling

from bot import keyboard
from bot.model import MessageContainer
from env.const import OPTIONS
from env.environment import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

message_container = MessageContainer()


@dp.message_handler(commands='start')
async def start_command(message: types.Message):
    if message_container.message:
        message.message_id = message_container.message.message_id
        await message.reply('Кто-уже собирается пойти за шаурмой, присоединяйтесь!')
        return
    markup = keyboard.close_poll_keyboard(message.from_user.id)
    message_container.message = await message.answer_poll(question='It\'s shawarma time!',
                                                          options=list(OPTIONS),
                                                          is_anonymous=False,
                                                          allows_multiple_answers=True,
                                                          reply_markup=markup)


@dp.callback_query_handler(lambda callback_query: callback_query.data.isdigit())
async def stop_query_handler(query: types.CallbackQuery):
    creator, user_id = query.data, query.from_user.id
    if creator != str(user_id):
        await query.answer('Вы не открывали голосование, чтобы его закрывать :)')
        return
    await bot.stop_poll(query.message.chat.id, query.message.message_id)
    message_container.message = None


def main():
    start_polling(dp)


if __name__ == '__main__':
    main()
