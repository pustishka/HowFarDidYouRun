import asyncio
import time
import menu
from database import insert_into_base
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
import threading
from concurrent.futures import ThreadPoolExecutor
from haversine import haversine

TOKEN = '5832582610:AAHnBKGpVEeIT__6eRq9-6u831j8i0BzaIc'  # Token from @BotFather
bot = Bot(TOKEN)
dp = Dispatcher(bot)

players = {}  # hashtable for accumulating members of bot
race_done_mark = False  # Mark using for access to second step (generate leader_board)
finished_players = {'Kat': [384713574, 150.0], 'ed': [384713574, 3500.0]}  # hashtable for players whom done first step


# main start handler for command in bot /start
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_full_name = message.from_user.full_name  # get full_name of user from message
    await message.answer(f'Привет, {user_full_name}', reply_markup=menu.mainMenu)  # bot sent 'Hello' to user


# main handler for set location and make all calculation
@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def handle_location(message: types.Message):
    username = message.from_user.username
    full_name = message.from_user.full_name
    start_latitude = message.location.latitude  # get latitude and longitude from message location
    start_longitude = message.location.longitude

    # func for generate leaderboard and sent to every user in finished players
    async def generate_leaderboard(distance):
        global finished_players
        ids = message.from_user.id  # get id of user from message
        finished_players[username] = [ids, distance]  # contain key=user, value=id and distance in list

        insert_into_base(username, distance)
        del players[username]  # delete player if player now in finished hashtable
        leader_board = ''  # string of leader_board
        if 3 <= len(finished_players) <= 5:  # condition for limit players count in leader_board (3-5)
            await message.answer(f'Таблица лидеров:')  # sent to user title of leader_board
            for idx, pl in enumerate(
                    dict(sorted(finished_players.items(), key=lambda x: x[1][1], reverse=True)), start=1):
                # enumerate count and username to leader_board in decreasing order
                leader_board += f'{idx}. {pl} - {finished_players[pl][1]} метра\n'
            for ids in finished_players.values():
                await bot.send_message(chat_id=ids[0],
                                       text=leader_board)  # sent leader_board to every champion
            finished_players = {}  # clear for next race

    # function for limit timing of race
    async def set_timeouts():
        secs = 2
        timeout = secs / 2
        while secs > 0:
            await message.answer(f'Осталось {secs} секунд до конца гонки!')
            await asyncio.sleep(timeout)
            secs -= int(timeout)

    # func for calculation difference of lat and long and convert to meters
    async def calculate_distance():
        global race_done_mark
        if username in players and race_done_mark:  # condition for access to second step calc distance
            finish_latitude = message.location.latitude
            finish_longitude = message.location.longitude
            distance = round(haversine(players[username], (finish_latitude, finish_longitude)),
                             3) * 1000  # haversine can calculate distance
            await message.answer(f'{full_name}, вы прошли {distance} метра',
                                 reply_markup=menu.mainMenu)  # sent to user passed distance
            await generate_leaderboard(distance)  # call function
        else:
            players[username] = [start_latitude, start_longitude]  # add player to all pool
            await message.answer(text='Гонка началась!',
                                 reply_markup=ReplyKeyboardRemove())  # close button until race not finished
            await set_timeouts()
            race_done_mark = True
            await message.answer(f'Гонка завершена')  # bot sent 'Race over' to user
            await message.answer(
                f'Нажми на кнопку "Узнать результат" в течении 30 секунд или дисквалификация...',
                reply_markup=menu.mainMenuFinish)  # Forces user to set second point of his location

    await calculate_distance()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
