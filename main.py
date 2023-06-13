import time
import menu
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove

from haversine import haversine

TOKEN = '5832582610:AAHnBKGpVEeIT__6eRq9-6u831j8i0BzaIc'
bot = Bot(TOKEN)
dp = Dispatcher(bot)

players = {}
race_done_mark = False
finished_players = {'ed': [384713574, 150], 'ed1': [384713574, 3500]}


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_full_name = message.from_user.full_name
    await message.answer(f'Привет, {user_full_name}', reply_markup=menu.mainMenu)


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

            async def generate_leaderboard():
                global finished_players
                ids = message.from_user.id
                finished_players[username] = [ids, distance]
                del players[username]
                leader_board = ''
                if 3 <= len(finished_players) <= 5:
                    await message.answer(f'Таблица лидеров:')
                    for idx, pl in enumerate(dict(sorted(finished_players.items(), key=lambda x: x[1], reverse=True)),
                                             start=1):
                        leader_board += f'{idx}. {pl} - {finished_players[pl][1]} метра\n'
                    for ids in finished_players.values():
                        await bot.send_message(chat_id=ids[0], text=leader_board)
                    finished_players = {}

            await generate_leaderboard()
        else:
            players[username] = [start_latitude, start_longitude]
            await message.answer(text='Гонка началась!', reply_markup=ReplyKeyboardRemove())

            async def set_timeouts():
                secs = 2
                timeout = secs / 2
                while secs > 0:
                    time.sleep(timeout)
                    await message.answer(f'Осталось {secs} секунд до конца гонки!')
                    secs -= int(timeout)

            await set_timeouts()
            race_done_mark = True
            await message.answer(f'Гонка завершена')
            await message.answer(
                f'Нажми на кнопку "Узнать результат" в течении 30 секунд или дисквалификация...',
                reply_markup=menu.mainMenuFinish)

    await calculate_distance()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
