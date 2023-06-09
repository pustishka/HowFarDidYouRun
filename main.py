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
finished_players = {}

@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def handle_location(message: types.Message):
    username = message.from_user.username
    full_name = message.from_user.full_name
    start_latitude = message.location.latitude
    start_longitude = message.location.longitude
    async def calculate_distance():
        global race_done_mark
        if username in players and race_done_mark:
            finish_latitude = message.location.latitude
            finish_longitude = message.location.longitude
            distance = round(haversine(players[username], (finish_latitude, finish_longitude)), 3) * 1000
            await message.answer(f'{full_name}, вы прошли {distance} метра', reply_markup=menu.mainMenu)
            await message.answer(f'Таблица лидеров:')
            finished_players[username]=distance
            for idx, pl in enumerate(sorted(finished_players), start=1):
                await message.answer(f'{idx}. {pl} - {finished_players[pl]} метра')
            print(finished_players)
            del players[username]

        else:
            players[username] = [start_latitude, start_longitude]
            print(players)
            secs = 2
            timeout = secs / 2
            while secs != 0:
                time.sleep(timeout)
                await message.answer(f'Осталось {secs} секунд до конца гонки!')
                secs -= int(timeout)
            race_done_mark = True
            await message.answer(f'Гонка завершена')
            await message.answer(f'Жми на кнопку!', reply_markup=menu.mainMenuFinish)
    if 1:
        await calculate_distance()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
