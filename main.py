import time
import logging
import menu
from aiogram import Bot, Dispatcher, executor, types

TOKEN = '5832582610:AAHnBKGpVEeIT__6eRq9-6u831j8i0BzaIc'
bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    await message.answer(f'Привет {user_full_name}', reply_markup=menu.mainMenu)
    # await message.s
    print(user_id)

@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text == 'Начать гонку🟢':
        print('Поехалииии')

if __name__ == '__main__':
    executor.start_polling(dp)