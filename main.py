import time
import logging
import menu
from aiogram import Bot, Dispatcher, executor, types

from haversine import haversine, Unit

TOKEN = '5832582610:AAHnBKGpVEeIT__6eRq9-6u831j8i0BzaIc'
bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    await message.answer(f'Привет {user_full_name}', reply_markup=menu.mainMenu)


players = {}
race_done_mark = False

@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def handle_location(message: types.Message):
    global race_done_mark
    username = message.from_user.username
    full_name = message.from_user.full_name
    start_latitude = message.location.latitude
    start_longitude = message.location.longitude
    if username in players and race_done_mark:
        finish_latitude = message.location.latitude
        finish_longitude = message.location.longitude
        distance = round(haversine(players[username], (finish_latitude, finish_longitude)), 3) * 1000
        await message.answer(f'{full_name}, вы прошли {distance} метра')
        del players[username]
    else:
        players[username] = [start_latitude, start_longitude]
        print(players)
        secs = 5
        while secs != 0:
            time.sleep(1)
            await message.answer(f'Осталось {secs} секунд до конца гонки!')
            secs -= 1
        race_done_mark = True
        await message.answer(f'Гонка завершена')
        await message.answer(f'Жми на кнопку!', reply_markup=menu.mainMenuFinish)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
